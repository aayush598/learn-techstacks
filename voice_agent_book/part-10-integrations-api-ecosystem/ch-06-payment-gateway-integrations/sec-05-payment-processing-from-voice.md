# Section 05: Payment Processing from Voice

## Overview

Payment processing from voice calls is the core differentiator of a voice agent payment system. The voice agent collects payment information (card number, expiration, CVV) through Dual-Tone Multi-Frequency (DTMF) keypad entry, processes the payment through the appropriate gateway adapter, and confirms the result verbally to the caller. This section covers the end-to-end flow of collecting payment details during a live call, handling PCI compliance requirements, managing payment state within the call conversation, and dealing with error scenarios (declined cards, insufficient funds, network failures).

The voice payment flow integrates closely with the call state machine: the agent must pause the conversation, enter secure payment collection mode, capture DTMF digits without logging them, process the payment, and resume the conversation with a result announcement. The system supports both immediate one-time payments and payment method registration for future recurring charges. PCI compliance requires that raw DTMF tones are never logged, stored, or transmitted unencrypted.

## Architecture

```
               Voice Payment Processing Flow

   Caller ←→ Voice Agent ←→ Payment Gateway ←→ Payment Adapter
                |
   +------------------------------------------------------------+
   |               Voice Payment State Machine                  |
   |                                                            |
   |  [Offer Payment] → [Collect Card # (DTMF)] ─┐             |
   |       ↑                                     ↓             |
   |       |                              [Collect Expiry]      |
   |       |                                     ↓             |
   |       |                              [Collect CVV]         |
   |       |                                     ↓             |
   |       |                              [Process Payment]     |
   |       |                                /        \         |
   |       |                         [Success]    [Failure]    |
   |       └───────────────────────────┘              ↓        |
   |                                            [Retry/Offer]  |
   +------------------------------------------------------------+
```

## Design Decisions

- **DTMF capture with PCI-scoped masking over recording:** The voice platform captures DTMF tones using the telephony API's built-in digit collection (e.g., Twilio's `<Gather>` with `finishOnKey`). When PCI mode is active, the platform strips DTMF audio from recordings, suppresses DTMF log output, and uses masked display (`****-****-****-1234`). The raw DTMF data is passed directly to the payment adapter without intermediate storage. Trade-off: PCI-scoped masking requires careful integration with recording and logging systems but reduces PCI audit scope significantly.

- **Payment intent-first flow over direct charge approach:** Before collecting payment details, the system creates a PaymentIntent (Stripe), transaction request (Braintree), or checkout session (Adyen) with the amount and currency. This generates an idempotency key and validates the amount before the caller enters card details. If the payment fails, the intent can be retried without recreating. Trade-off: intent-first adds a pre-authorization API call before card collection but reduces the window for double charges.

- **Barge-in disabled during DTMF collection over allowing interruption:** During payment digit collection, barge-in (the caller interrupting the agent) is disabled to prevent the caller from accidentally canceling the payment flow. The agent clearly announces: "Please enter your 16-digit card number. You will not be able to interrupt during entry." After all digits are collected, barge-in is re-enabled. Trade-off: disabling barge-in creates a less natural interaction but prevents payment flow corruption.

## Implementation Approach

```
interface VoicePaymentSession {
  callSid: string;
  paymentAdapter: string;
  state: PaymentState;
  paymentIntentId?: string;
  collectedData: {
    cardNumber?: string;    // Never logged, stored only in memory
    expiryMonth?: string;
    expiryYear?: string;
    cvv?: string;
  };
  result?: PaymentResult;
  error?: PaymentError;
  retryCount: number;
  createdAt: Date;
}

enum PaymentState {
  INITIATED = 'initiated',
  COLLECTING_NUMBER = 'collecting_number',
  COLLECTING_EXPIRY = 'collecting_expiry',
  COLLECTING_CVV = 'collecting_cvv',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

const PCI_MASKED_LOG = (digits: string): string => {
  if (digits.length <= 4) return '***';
  return '****-****-****-' + digits.slice(-4);
};

class VoicePaymentHandler {
  private sessions = new Map<string, VoicePaymentSession>();
  private paymentGateway: PaymentGateway;
  private audioRouter: AudioRouter;

  async initiatePayment(callSid: string, params: {
    amount: number;
    currency: string;
    adapter: string;
  }): Promise<TwiMLResult> {
    const intent = await this.paymentGateway.createIntent(params.adapter, {
      amount: params.amount,
      currency: params.currency,
      metadata: { callSid },
    });

    this.sessions.set(callSid, {
      callSid,
      paymentAdapter: params.adapter,
      state: PaymentState.COLLECTING_NUMBER,
      paymentIntentId: intent.id,
      collectedData: {},
      retryCount: 0,
      createdAt: new Date(),
    });

    return this.buildGatherPrompt(
      'Please enter your 16-digit card number, followed by the pound key.',
      { numDigits: 16, finishOnKey: '#', timeout: 15 }
    );
  }

  async handleDigits(callSid: string, digits: string): Promise<TwiMLResult> {
    const session = this.sessions.get(callSid);
    if (!session) return this.respondError('Payment session not found');

    switch (session.state) {
      case PaymentState.COLLECTING_NUMBER:
        session.collectedData.cardNumber = digits;
        logger.info(`Card number collected for ${callSid}`, { masked: PCI_MASKED_LOG(digits) });
        session.state = PaymentState.COLLECTING_EXPIRY;
        return this.buildGatherPrompt(
          'Please enter the expiration month and year as two digits, two digits. For example, zero one two six for January 2026.',
          { numDigits: 4, finishOnKey: '#', timeout: 10 }
        );

      case PaymentState.COLLECTING_EXPIRY:
        session.collectedData.expiryMonth = digits.slice(0, 2);
        session.collectedData.expiryYear = digits.slice(2, 4);
        session.state = PaymentState.COLLECTING_CVV;
        return this.buildGatherPrompt(
          'Please enter the 3-digit security code on the back of your card.',
          { numDigits: 3, finishOnKey: '#', timeout: 10 }
        );

      case PaymentState.COLLECTING_CVV:
        session.collectedData.cvv = digits;
        session.state = PaymentState.PROCESSING;
        await this.audioRouter.say(callSid, 'Processing your payment. Please wait.');
        return this.processAndRespond(session);

      default:
        return this.respondError('Invalid payment state');
    }
  }

  private async processAndRespond(session: VoicePaymentSession): Promise<TwiMLResult> {
    try {
      const result = await this.paymentGateway.confirmPayment(session.paymentAdapter, {
        paymentIntentId: session.paymentIntentId!,
        cardData: session.collectedData,
      });

      session.state = PaymentState.COMPLETED;
      session.result = result;

      await this.audioRouter.say(
        session.callSid,
        `Your payment of ${result.amount} ${result.currency} was successful. ` +
        `Your confirmation number is ${result.transactionId}.`
      );
      return this.respondSuccess(result);
    } catch (error) {
      session.state = PaymentState.FAILED;
      session.error = { message: (error as Error).message, retryable: true };

      if (session.retryCount < 2) {
        session.retryCount++;
        session.state = PaymentState.COLLECTING_NUMBER;
        return this.buildGatherPrompt(
          'Your payment was declined. Please try a different card. Enter the 16-digit card number followed by the pound key.',
          { numDigits: 16, finishOnKey: '#', timeout: 15 }
        );
      }

      await this.audioRouter.say(
        session.callSid,
        'We were unable to process your payment after multiple attempts. A payment link will be sent to your phone.'
      );
      return this.respondError('Payment declined after retries');
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Twilio SDK (MIT) | Node.js | DTMF `<Gather>` handling |
| PCI Proxy SDK | Commercial | PCI-compliant tokenization |
| Pino (MIT) | Logging | Masked payment logging |

## Production Considerations

**Scaling:** Voice payment sessions are memory-bound — each session holds card data in memory for the duration of the call (typically 30-90 seconds). Use a distributed in-memory cache (Redis) with TTL equal to the call timeout to share session state across horizontally scaled voice servers. The payment gateway connection pool must scale with the number of concurrent voice calls processing payments.

**Security:** PCI DSS SAQ D applies if card data is transmitted through your server. Use PCI-compliant DTMF relay services (Twilio PCI DSS v3 compliant) that pass card data directly from the phone to the payment processor without touching your application servers. If server-side processing is required, ensure all card data is encrypted in memory and zeroed after use. Never log raw card data, never write it to disk, and never include it in error messages.

**Monitoring:** Track voice payment conversion rates (initiated-to-completed), average collection time per digit set, retry rates, decline reasons, and payment amount distribution. Alert on payment completion rates below 70%, retry rates above 20%, and any detection of raw card data in logs (via log scanner). Monitor gateway-side authorization rates for voice-originated payments versus web-originated payments.
