# Section 07: Customer Account Management

## Overview

Customer account management enables callers to manage their e-commerce account through voice conversations. Account management covers profile updates (name, email, phone, password reset), address management (add, update, remove shipping/billing addresses), payment method management (view saved methods, update expiry, remove expired cards), communication preferences (email/SMS opt-in, marketing preferences), and account linking (link guest orders to account).

Account management requires careful security and authentication. The caller must be authenticated before making account changes. Authentication methods include phone number verification (SMS code to registered number), knowledge-based authentication (verify details from past orders), or out-of-band verification (send a one-time link to email). The service supports progressive profiling — gradually collecting and updating customer information over multiple calls rather than asking for everything at once.

## Architecture

```
                    Customer Account Management

   Caller: "Update my address"
        |
        v
   +------------------+
   | Identity Verify   |
   | • Phone OTP       |
   | • Security Q      |
   | • Order knowledge |
   +------------------+
        |
        v
   +----------------------------------------------------+
   |              Account Management Service             |
   |                                                    |
   |  +------------------+  +------------------+        |
   |  | Profile          |  | Address          |        |
   |  | • Name update    |  | • Add address     |        |
   |  | • Email change   |  | • Edit address    |        |
   |  | • Phone change   |  | • Set default    |        |
   |  +------------------+  +------------------+        |
   |  +------------------+  +------------------+        |
   |  | Payment Methods  |  | Preferences     |        |
   |  | • View methods   |  | • Email opt-in   |        |
   |  | • Update expiry  |  | • SMS opt-in     |        |
   |  | • Remove card    |  | • Marketing      |        |
   |  +------------------+  +------------------+        |
   +----------------------------------------------------+
```

## Design Decisions

- **Progressive verification with escalating security:** Low-risk changes (email preferences) require one-factor verification (caller ID matches registered phone). High-risk changes (change email, add new address for shipping) require two-factor verification (phone OTP + knowledge-based question). Payment method changes require the highest level (OTP + email confirmation link). This balances security with user experience. Trade-off: high-security requirements for sensitive operations can frustrate callers who expect immediate changes.

- **Update confirmation with review opportunity:** Before committing any account change, the system reads back the proposed change and asks for confirmation. For destructive changes (remove address, delete payment method), the system requires explicit confirmation and doesn't use implicit confirmation. For additive changes (add address), implicit confirmation is acceptable. Trade-off: confirmation adds conversation turns but prevents unintended changes.

- **Multi-platform account synchronization:** Some customers have accounts on the voice platform and the e-commerce platform, possibly with different information. The account management service syncs changes to all connected platforms where the customer has an account. The source of truth is configurable — the voice platform can be authoritative, or changes are propagated bidirectionally with conflict resolution. Trade-off: multi-platform sync adds complexity but ensures consistency across systems.

## Implementation Approach

```
interface AccountChangeRequest {
  contactId: string;
  verificationLevel: 'low' | 'medium' | 'high';
  changes: {
    type: 'profile' | 'address' | 'payment' | 'preferences';
    action: 'add' | 'update' | 'remove';
    field: string;
    newValue: any;
    oldValue?: any;
  }[];
}

class AccountManagementService {
  async processAccountChange(request: AccountChangeRequest): Promise<AdapterResponse<{ applied: string[]; failed: string[] }>> {
    // Verify caller identity
    const verified = await this.identityVerifier.verify(request.contactId, request.verificationLevel);
    if (!verified) {
      return { success: false, error: 'Identity verification failed' };
    }

    const applied: string[] = [];
    const failed: string[] = [];

    for (const change of request.changes) {
      try {
        switch (change.type) {
          case 'profile':
            await this.updateProfile(request.contactId, change);
            applied.push(`${change.field}_${change.action}`);
            break;
          case 'address':
            await this.updateAddress(request.contactId, change);
            applied.push(`address_${change.action}`);
            break;
          case 'payment':
            await this.updatePayment(request.contactId, change);
            applied.push(`payment_${change.action}`);
            break;
          case 'preferences':
            await this.updatePreferences(request.contactId, change);
            applied.push(`preferences_${change.field}`);
            break;
        }
      } catch (error) {
        failed.push(`${change.type}_${change.field}: ${error.message}`);
      }
    }

    return { success: true, data: { applied, failed } };
  }

  async updateProfile(contactId: string, change: any) {
    const platformCallbacks = {
      email: async (value: string) => {
        await this.shopifyAdapter.updateCustomer(contactId, { email: value });
        await this.wooCommerceAdapter.updateCustomer(contactId, { email: value });
      },
      phone: async (value: string) => {
        await this.shopifyAdapter.updateCustomer(contactId, { phone: value });
      }
    };

    const callback = platformCallbacks[change.field];
    if (callback) await callback(change.newValue);

    await this.profileStore.update(contactId, {
      [change.field]: change.newValue,
      updatedAt: new Date().toISOString()
    });
  }

  async updateAddress(contactId: string, change: any) {
    const platforms = await this.getConnectedPlatforms(contactId);
    for (const platform of platforms) {
      const adapter = this.adapterFactory.getAdapter(platform);
      if (change.action === 'add') {
        await adapter.addCustomerAddress(contactId, change.newValue);
      } else if (change.action === 'update') {
        await adapter.updateCustomerAddress(contactId, change.newValue.id, change.newValue);
      } else if (change.action === 'remove') {
        await adapter.deleteCustomerAddress(contactId, change.oldValue.id);
      }
    }
  }

  async updatePayment(contactId: string, change: any) {
    // Payment method changes require highest verification
    if (!await this.identityVerifier.verify(contactId, 'high')) {
      throw new Error('High-level verification required for payment changes');
    }
    // Payment methods are typically managed through the payment gateway, not the e-commerce API
    // For security, changes are logged and a confirmation is sent to the customer
    await this.auditLogger.log('payment_change', {
      contactId, action: change.action, field: change.field,
      timestamp: new Date().toISOString()
    });
    // Send confirmation email
    await this.notificationService.sendPaymentChangeConfirmation(contactId, change);
  }

  async updatePreferences(contactId: string, change: any) {
    await this.profileStore.updatePreferences(contactId, {
      [change.field]: change.newValue
    });

    // Sync to connected platforms
    const platforms = await this.getConnectedPlatforms(contactId);
    for (const platform of platforms) {
      const adapter = this.adapterFactory.getAdapter(platform);
      await adapter.updateCustomerPreferences(contactId, {
        [change.field]: change.newValue
      });
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Redis** (BSD) | Cache | Session and verification state |
| **BullMQ** (MIT) | Queue | Async platform sync |
| **PostgreSQL** (PostgreSQL) | Data store | Customer profile storage |

## Production Considerations

**Scaling:** Account management operations are write-heavy and must be synchronized across platforms. Use a write queue to serialize changes per customer (prevent concurrent conflicting updates). Cache customer profiles in Redis for fast read access during calls.

**Security:** Account management is the highest-security integration area. All changes must be logged with caller identity, verification method, and timestamp. Implement rate limiting on account changes (prevent brute force). Support account freeze (disable changes) if suspicious activity is detected. Require additional verification for email and payment method changes.

**Monitoring:** Track account change volume by type, verification success rate, multi-platform sync success rate, and conflict rate. Alert on verification failure rate exceeding 30% (may indicate verification system issues), sync failures across platforms, and unusual patterns of changes (possible account takeover).
