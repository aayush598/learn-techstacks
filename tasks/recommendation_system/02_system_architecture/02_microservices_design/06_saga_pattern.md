# Saga Pattern for Recommendation Systems

## 1. Saga Fundamentals

### 1.1 What is a Saga
A Saga is a sequence of local transactions where each transaction updates data within a single service. If any transaction fails, the saga executes compensating transactions to undo the changes of previously completed transactions.

### 1.2 Why Sagas for Recommendations
Recommendation systems involve multi-service workflows where:
- Operations span multiple services (user onboarding, model deployment)
- Each service has its own database (database per service pattern)
- Distributed transactions (2PC) are impractical at scale
- Eventual consistency is acceptable for most operations

### 1.3 Choreography vs Orchestration

**Choreography**:
- Each service listens for events and decides what to do next
- No central coordinator
- Services publish events when they complete their step
- Services compensate by publishing compensation events
- **Pros**: Loose coupling; no single point of failure
- **Cons**: Hard to understand the full flow; debugging is difficult; circular dependencies possible

**Orchestration**:
- Central orchestrator coordinates the entire saga
- Orchestrator tells each service what to do
- Orchestrator handles compensation on failure
- **Pros**: Clear flow; easy to understand; centralized error handling
- **Cons**: Single point of failure (the orchestrator); tighter coupling

---

## 2. Recommendation System Sagas

### 2.1 User Onboarding Saga (Orchestration Pattern)

**Trigger**: New user registers

**Steps**:
1. **User Service**: Create user account → Success
2. **Preference Service**: Initialize default preferences → Success
3. **Feature Service**: Compute initial user features → Success
4. **Experiment Service**: Assign user to experiments → Success
5. **Recommendation Service**: Generate initial recommendations → Success

**Failure Handling**:
- Step 3 fails → Compensate: Delete user preferences (Step 2), Delete user account (Step 1)
- Step 5 fails → Compensate: Remove experiment assignments (Step 4), Remove features (Step 3), Remove preferences (Step 2), Delete account (Step 1)

**Compensation Design**:
- Each step has a corresponding compensating action
- Compensations are idempotent (can be retried safely)
- Compensations are logged for audit purposes
- Partial compensation is acceptable (e.g., if account deletion fails, flag for manual cleanup)

### 2.2 Model Deployment Saga (Orchestration Pattern)

**Trigger**: New model ready for deployment

**Steps**:
1. **Model Registry**: Upload model artifacts → Transition to "staging"
2. **Validation Service**: Run automated quality gates → Pass
3. **Deployment Service**: Deploy to canary (5% traffic) → Active
4. **Monitoring Service**: Monitor for 24 hours → Metrics positive
5. **Deployment Service**: Gradual traffic increase (25% → 50% → 100%) → Complete

**Failure Handling**:
- Step 2 fails → Compensate: Transition model back to "development"
- Step 4 fails (metrics degrade) → Compensate: Reduce canary traffic to 0%, rollback to previous model
- Step 5 fails at 50% → Compensate: Rollback to previous model, transition new model to "failed"

### 2.3 Data Pipeline Saga (Choreography Pattern)

**Trigger**: Daily data processing job starts

**Steps** (choreography via Kafka events):
1. **Data Extractor**: Extracts raw data → Publishes `data_extracted` event
2. **Data Validator**: Validates data quality → Publishes `data_validated` event
3. **Feature Computer**: Computes batch features → Publishes `features_computed` event
4. **Training Data Assembler**: Assembles training dataset → Publishes `training_data_ready` event
5. **Model Trainer**: Trains model → Publishes `model_trained` event
6. **Model Validator**: Validates model → Publishes `model_validated` event

**Failure Handling**:
- Step 3 fails → Feature Computer publishes `features_computation_failed` event
- Downstream consumers (Training Data Assembler) stop processing
- Data Engineer investigates and triggers re-computation

### 2.4 Recommendation Delivery Saga (Choreography Pattern)

**Trigger**: User requests recommendations

**Steps** (synchronous within request, async for logging):
1. API Gateway → User Profile Service (get user profile)
2. API Gateway → Candidate Generation Service (get candidates)
3. API Gateway → Feature Store (get features)
4. API Gateway → Ranking Service (rank candidates)
5. API Gateway → Re-ranking Service (apply business rules)
6. API Gateway → Response to client
7. **Async**: Interaction Service logs recommendation (Kafka event)
8. **Async**: Feature Store updates impression features (Kafka event)

**Failure Handling**:
- Synchronous steps use circuit breakers and fallbacks
- Asynchronous logging failures do not affect recommendation delivery
- Failed interactions are retried via dead letter queue

---

## 3. Saga Implementation Patterns

### 3.1 State Machine Design
```
States: CREATED → STEP_1_PENDING → STEP_1_COMPLETE → STEP_2_PENDING → STEP_2_COMPLETE → ... → COMPLETED
Failure: Any step → COMPENSATING → STEP_N_COMPENSATING → ... → STEP_1_COMPENSATING → FAILED
```

### 3.2 Saga Log
The saga orchestrator maintains a log of all steps:
```json
{
  "saga_id": "uuid",
  "saga_type": "model_deployment",
  "status": "step_3_complete",
  "steps": [
    {"step": 1, "status": "complete", "timestamp": "..."},
    {"step": 2, "status": "complete", "timestamp": "..."},
    {"step": 3, "status": "complete", "timestamp": "..."}
  ],
  "started_at": "...",
  "last_updated": "..."
}
```

### 3.3 Saga Timeout Handling
- Each step has a maximum execution time
- If step exceeds timeout, saga transitions to compensating state
- Timeout triggers compensating transactions for completed steps
- Timeout prevents saga from hanging indefinitely

### 3.4 Idempotency in Sagas
- All saga steps must be idempotent
- Use saga_id + step_number as idempotency key
- Services must handle duplicate step invocations gracefully
- Compensations must also be idempotent

---

## 4. Compensation Strategies

### 4.1 Compensation Types

**Semantic Compensation**:
- Log the failure but don't undo the operation
- Accept the inconsistency and flag for manual review
- Use when: Compensation is too complex or operation is non-critical

**Data Compensation**:
- Delete or revert data changes made by the failed step
- Use when: Clear data rollback is possible

**Action Compensation**:
- Send message/notification to undo the effect
- Use when: Operation affected external systems
- Example: Send cancellation email for failed booking

### 4.2 Compensation Failure Handling
1. **Retry Compensation**: Retry the compensating transaction
2. **Manual Intervention**: Alert operations team for manual cleanup
3. **Dead Letter**: Store failed compensations for later processing
4. **Accept Inconsistency**: Log the issue and accept the data inconsistency

---

## 5. Saga Testing

### 5.1 Testing Strategies
- **Unit Test**: Test individual saga steps and compensations
- **Integration Test**: Test saga flow with real services
- **Chaos Test**: Inject failures at various points to test compensation
- **Load Test**: Test saga behavior under high load
- **Long-Running Test**: Test saga with realistic timing and delays

### 5.2 Testing Checklist
- [ ] Happy path: All steps complete successfully
- [ ] Failure at each step: Verify compensation for all previous steps
- [ ] Double compensation: Verify idempotency of compensations
- [ ] Timeout: Verify saga handles step timeouts
- [ ] Concurrent sagas: Verify no interference between sagas
- [ ] Partial compensation: Verify system handles incomplete compensation
- [ ] Recovery: Verify saga can resume after orchestrator restart
