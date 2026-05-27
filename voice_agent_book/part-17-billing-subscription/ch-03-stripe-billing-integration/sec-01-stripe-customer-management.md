# Section 01: Stripe Customer Management

## Customer Creation on Signup

When a user signs up, a Stripe Customer object is created in parallel with the internal tenant record. The Stripe Customer serves as the billing identity for the tenant, holding payment methods, subscription references, and billing metadata.

The customer creation happens asynchronously after the tenant record is established. If Stripe creation fails, the tenant is created without billing capability and retried via a background job.

```typescript
interface StripeCustomerReference {
  id: string;
  tenantId: string;
  stripeCustomerId: string;
  status: 'pending' | 'active' | 'error';
  errorMessage?: string;
  createdAt: string;
  syncedAt: string;
}

class CustomerService {
  async createCustomer(tenantId: string): Promise<StripeCustomerReference> {
    const tenant = await this.tenantService.getTenant(tenantId);

    try {
      const customer = await stripe.customers.create({
        email: tenant.email,
        name: tenant.companyName,
        metadata: {
          tenant_id: tenantId,
          signup_source: tenant.signupSource,
          account_created_at: tenant.createdAt,
        },
        preferred_locales: [tenant.locale],
        address: tenant.billingAddress
          ? {
              line1: tenant.billingAddress.line1,
              city: tenant.billingAddress.city,
              state: tenant.billingAddress.state,
              postal_code: tenant.billingAddress.postalCode,
              country: tenant.billingAddress.country,
            }
          : undefined,
      });

      const ref = await this.db.stripeCustomers.create({
        tenantId,
        stripeCustomerId: customer.id,
        status: 'active',
        createdAt: new Date().toISOString(),
        syncedAt: new Date().toISOString(),
      });

      await this.cache.set(`stripe_customer:${tenantId}`, customer.id);

      return ref;
    } catch (error) {
      logger.error('Failed to create Stripe customer', { tenantId, error });
      await this.db.stripeCustomers.create({
        tenantId,
        status: 'error',
        errorMessage: error.message,
        createdAt: new Date().toISOString(),
      });
      throw error;
    }
  }
}
```

## Metadata Sync

Tenant metadata is synced bidirectionally between our system and Stripe. When a tenant updates their company name, billing address, or email, the change propagates to Stripe to keep records consistent.

```typescript
class MetadataSyncService {
  async syncTenantToStripe(tenantId: string): Promise<void> {
    const tenant = await this.tenantService.getTenant(tenantId);
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    await stripe.customers.update(stripeCustomerId, {
      email: tenant.email,
      name: tenant.companyName,
      metadata: {
        tenant_id: tenantId,
        company_size: tenant.companySize?.toString(),
        industry: tenant.industry,
        updated_at: new Date().toISOString(),
      },
    });
  }

  async syncStripeToTenant(stripeCustomerId: string): Promise<void> {
    const customer = await stripe.customers.retrieve(stripeCustomerId);
    const tenantId = customer.metadata.tenant_id;

    if (customer.deleted) {
      await this.handleCustomerDeleted(tenantId);
      return;
    }

    // Update internal tenant with Stripe data
    await this.tenantService.updateBillingInfo(tenantId, {
      email: customer.email,
      billingAddress: customer.address
        ? {
            line1: customer.address.line1,
            city: customer.address.city,
            state: customer.address.state,
            postalCode: customer.address.postal_code,
            country: customer.address.country,
          }
        : undefined,
    });

    // Sync default payment method
    if (customer.invoice_settings?.default_payment_method) {
      await this.paymentMethodService.setDefaultMethod(
        tenantId,
        customer.invoice_settings.default_payment_method
      );
    }
  }
}
```

## Customer Portal

Stripe's hosted Customer Portal provides a self-service interface for customers to manage their billing. It supports updating payment methods, viewing invoices, updating subscription, and downloading receipts.

```typescript
class CustomerPortalService {
  async createPortalSession(
    tenantId: string,
    returnUrl: string
  ): Promise<string> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    const session = await stripe.billingPortal.sessions.create({
      customer: stripeCustomerId,
      return_url: returnUrl,
      flow_data: {
        type: 'payment_method_update',
        after_completion: {
          type: 'redirect',
          redirect: { url: returnUrl },
        },
      },
    });

    return session.url;
  }

  async createPortalSessionForInvoice(
    tenantId: string,
    invoiceId: string,
    returnUrl: string
  ): Promise<string> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    const session = await stripe.billingPortal.sessions.create({
      customer: stripeCustomerId,
      return_url: returnUrl,
      flow_data: {
        type: 'invoice_list',
      },
    });

    return session.url;
  }
}
```

## Multi-Account Handling

Enterprise customers may have multiple sub-accounts or divisions that share billing. Stripe supports this through customer hierarchy or through a single customer with multiple subscriptions. Our approach uses a parent-child tenant model with a single billing account.

```typescript
interface TenantBillingHierarchy {
  billingTenantId: string;   // The tenant that pays
  subTenants: string[];      // Tenants under this billing
  allocation: 'auto' | 'manual';
  invoiceMerge: boolean;     // Merge invoices or separate
}
```

## Open-Source Tools

- **Stripe API** (Proprietary, free tier) — Customer management
- **PostgreSQL** — Internal customer reference storage
- **Redis** — Customer ID caching for low-latency lookups
- **BullMQ** — Background sync jobs between internal and Stripe

## Integration Points

Customer management connects to the tenant service (for user data), the authentication service (for signup flow), the subscription service (for plan assignment), and the notification service (for billing-related communications).

## Production Considerations

- Handle Stripe rate limits (100 reads/s, 100 writes/s by default)
- Implement idempotency for customer creation retries
- Cache Stripe customer IDs aggressively in Redis
- Monitor customer sync failures and set up alerts
- Handle Stripe API deprecations with version pinning

## Open-Source First Philosophy

Stripe's free tier provides customer management with no monthly fee — only transaction fees apply. PostgreSQL and Redis provide the caching and persistence layers at no licensing cost. BullMQ handles background synchronization without requiring enterprise job schedulers. This approach minimizes fixed costs while maintaining enterprise billing capabilities.
