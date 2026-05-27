# Section 05: Return & Refund Processing

## Overview

Return and refund processing enables callers to initiate returns and request refunds through voice conversations. The service handles the complete return workflow: checking return eligibility (based on order status, product type, time since purchase), selecting items to return, choosing the return reason, generating return labels (in-store drop-off, carrier pickup, prepaid label), tracking the return shipment, and processing the refund once the return is received.

Return processing is more complex than it first appears because different e-commerce platforms have different return models. Shopify has a Return API with return line items and a disposition (restock, refund). WooCommerce uses Refund API with line item and quantity selection. Magento uses Credit Memos for refunds with optional return to stock. The unified return service normalizes these variations and handles the complete lifecycle — authorization, shipping, receipt, inspection, and refund. The service also handles partial returns (some items from a multi-item order) and exchange flows (return the original, ship the replacement).

## Architecture

```
                    Return & Refund Processing Workflow

   Caller: "I need to return an item"
        |
        v
   +------------------+
   | Eligibility Check |
   | • Order status    |
   | • Return window   |
   | • Product type    |
   | • Restocking fee  |
   +------------------+
        |
        v
   +------------------+
   | Item Selection    |
   | • Which items?    |
   | • Quantity        |
   | • Reason          |
   +------------------+
        |
        v
   +----------------------------------------------------+
   |              Return Processing Pipeline              |
   |                                                    |
   |  1. Create Return in e-commerce platform            |
   |  2. Generate return label (carrier API)             |
   |  3. Send return instructions to customer            |
   |  4. Track return shipment                           |
   |  5. On receipt: inspect → process refund            |
   |  6. Update inventory (restock)                     |
   |  7. Notify customer of refund                      |
   +----------------------------------------------------+
```

## Design Decisions

- **Platform-native return creation with label generation:** Returns are created through the e-commerce platform's native return/refund API, ensuring platform-specific workflows (restock preferences, return reasons, disposition rules) are respected. Return labels are generated through the platform's shipping integration or a separate carrier API (Shippo, EasyPost). Trade-off: platform-native returns lock the platform into each e-commerce's return capabilities; some platforms have limited return APIs.

- **Configurable return policies per merchant:** Return policies vary by merchant: return window (30 days, 60 days, 90 days), condition requirements (unopened, like-new, used), restocking fees (none, 15%, 20% for opened items), and return shipping responsibility (merchant-paid, customer-paid, free with store credit). The policy engine evaluates all rules and communicates the outcome to the caller during the voice conversation. Trade-off: complex policy evaluation can make the voice conversation lengthy; clear TTS presentation of policy terms is essential.

- **Two-phase refund (authorization → capture):** Refunds are authorized first (reserved in the payment gateway) and captured only after the return is received and inspected. This handles the case where a return shipment is lost or the returned item is damaged — the refund authorization expires and the merchant doesn't lose money. For store credit refunds, the credit is issued immediately. Trade-off: two-phase refunds require tracking return receipt status and automating the capture step.

## Implementation Approach

```
interface ReturnRequest {
  orderNumber: string;
  platform: string;
  items: { lineItemId: string; sku: string; quantity: number; reason: string }[];
  returnMethod: 'mail' | 'store_drop' | 'pickup';
  refundMethod: 'original_payment' | 'store_credit' | 'exchange';
  metadata?: Record<string, any>;
}

interface ReturnResult {
  returnId: string;
  rmaNumber: string;
  status: 'pending_approval' | 'approved' | 'label_generated' | 'in_transit' | 'received' | 'refunded' | 'rejected';
  labelUrl?: string;
  carrier?: string;
  trackingNumber?: string;
  instructions: string;
  refundEstimate: { amount: number; currency: string; method: string; eta: string };
}

class ReturnProcessingService {
  async initiateReturn(request: ReturnRequest): Promise<AdapterResponse<ReturnResult>> {
    // Check eligibility
    const eligibility = await this.checkEligibility(request);
    if (!eligibility.allowed) {
      return { success: false, error: eligibility.reason };
    }

    // Create return in e-commerce platform
    const adapter = this.adapterFactory.getAdapter(request.platform);
    const platformReturn = await adapter.createReturn({
      orderId: request.orderNumber,
      items: request.items,
      returnMethod: request.returnMethod
    });

    // Generate return label
    const labelResult = request.returnMethod === 'mail'
      ? await this.labelService.generateLabel({
          toAddress: platformReturn.returnAddress,
          fromAddress: platformReturn.customerAddress,
          weight: platformReturn.totalWeight,
          carrier: 'auto'
        })
      : null;

    // Send instructions
    await this.notificationService.sendReturnInstructions({
      email: platformReturn.customerEmail,
      rmaNumber: platformReturn.rmaNumber,
      instructions: this.buildReturnInstructions(request.returnMethod, labelResult),
      labelUrl: labelResult?.labelUrl
    });

    // Schedule follow-up tracking
    if (labelResult?.trackingNumber) {
      await this.trackingScheduler.monitorReturn(labelResult.trackingNumber, platformReturn.rmaNumber);
    }

    return {
      success: true,
      data: {
        returnId: platformReturn.id,
        rmaNumber: platformReturn.rmaNumber,
        status: 'approved',
        labelUrl: labelResult?.labelUrl,
        carrier: labelResult?.carrier,
        trackingNumber: labelResult?.trackingNumber,
        instructions: 'Print the prepaid label and drop off at any carrier location.',
        refundEstimate: {
          amount: eligibility.refundAmount,
          currency: eligibility.currency,
          method: request.refundMethod,
          eta: '5-7 business days after receipt'
        }
      }
    };
  }

  async processReturnReceipt(rmaNumber: string, condition: 'new' | 'used' | 'damaged'): Promise<AdapterResponse<void>> {
    const platformReturn = await this.findReturnByRMA(rmaNumber);

    // Determine refund amount based on condition
    const refundAmount = condition === 'new'
      ? platformReturn.totalAmount
      : condition === 'used'
        ? platformReturn.totalAmount * (1 - (platformReturn.restockingFeePercent / 100))
        : 0; // Damaged items may not be refundable

    // Process refund
    const adapter = this.adapterFactory.getAdapter(platformReturn.platform);
    if (refundAmount > 0) {
      await adapter.processRefund(platformReturn.orderId, {
        amount: refundAmount,
        reason: `Return received (${condition})`,
        lineItems: platformReturn.items
      });
    }

    // Restock items
    for (const item of platformReturn.items) {
      await adapter.restockItem(item.sku, item.quantity);
    }

    // Notify customer
    await this.notificationService.sendRefundNotification({
      email: platformReturn.customerEmail,
      rmaNumber,
      refundAmount,
      refundMethod: platformReturn.refundMethod
    });

    return { success: true, data: undefined };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Shippo** (MIT) | Shipping | Return label generation |
| **EasyPost** (MIT) | Shipping | Carrier label API |
| **BullMQ** (MIT) | Queue | Return processing pipeline |

## Production Considerations

**Scaling:** Return processing involves multiple sequential steps (eligibility check → platform API → label generation → notification → tracking). Use a state machine with queue-based processing for reliability. Each return request is processed as a job in BullMQ with step-by-step execution.

**Security:** Return processing involves financial transactions (refunds). Implement approval workflows for refunds above configurable thresholds. Verify caller identity before processing returns. Log all return and refund actions for audit.

**Monitoring:** Track return initiation rate, return completion rate (started → refunded), return-to-refund cycle time, refund amount distribution, cost of return (shipping labels + restocking), and fraud rate (suspicious return patterns). Alert on high fraud rate, long cycle times, and excessive return rates for specific merchants.
