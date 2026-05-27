# Section 08: Chaos Engineering & Resilience

## Overview

Chaos engineering proactively tests system resilience by introducing controlled failures. Experiments validate that the platform survives pod failures, network partitions, latency spikes, resource exhaustion, and dependency outages. Each experiment has a hypothesis, controlled variables, and blast radius measurement.

## Architecture

```
Experiment Types:
- Pod kill: Delete pods during load
- CPU hog: Saturate CPU on target pods
- Network latency: Inject delay between services
- Packet loss: Drop network packets
- DNS failure: Make DNS resolution fail
- Disk pressure: Fill disk on nodes
```

## Design Decisions

- **Blast Radius Control**: Experiments limited to staging
- **Hypothesis-Driven**: Each experiment has expected outcome
- **Automated Rollback**: Failed experiments auto-rollback
- **Graduated Complexity**: Start simple, increase complexity

## Implementation Approach

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: voice-service-chaos
spec:
  appinfo:
    appns: 'voice-staging'
    applabel: 'app=voice-service'
    appkind: 'deployment'
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'
            - name: CHAOS_INTERVAL
              value: '10'
            - name: FORCE
              value: 'true'
        probe:
          - name: 'check-availability'
            type: 'httpProbe'
            httpProbe/inputs:
              url: 'http://voice-service:3000/health'
              expectedStatusCode: 200
```

```typescript
test('system survives pod failures during load', async () => {
  const baselineLatency = await getLatencyStats();
  const baselinePods = await getPodCount('voice-service');
  await startLoad({ concurrency: 100, duration: '5m' });
  await chaosEngine.run('pod-delete', { replicas: 2 });
  const recoveryTime = await waitForLatencyRecovery(baselineLatency, 60000);
  expect(recoveryTime).toBeLessThan(30000);
  const podsAfter = await getPodCount('voice-service');
  expect(podsAfter).toBeGreaterThanOrEqual(baselinePods);
});
```

## Integration Points

- **Monitoring Stack**: Real-time monitoring during experiments
- **Alerting**: Coordinate with on-call during experiments
- **CI/CD Pipeline**: Chaos tests before production deployments

## Open-Source Tools

- **LitmusChaos** (Apache 2.0): Chaos engineering platform
- **Chaos Mesh** (Apache 2.0): Kubernetes chaos
- **PowerfulSeal** (Apache 2.0): Chaos testing for Kubernetes

## Production Considerations

- **Safety Measures**: Always have kill switch
- **Business Hours**: Run experiments when engineers are available
- **Blast Radius**: Start with 1 pod, low traffic
