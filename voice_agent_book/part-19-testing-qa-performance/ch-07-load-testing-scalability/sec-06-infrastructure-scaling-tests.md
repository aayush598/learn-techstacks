# Section 06: Infrastructure Scaling Tests

## Overview

Infrastructure scaling tests validate that auto-scaling mechanisms work correctly under varying load. These tests verify that Kubernetes HPA triggers at the right thresholds, pods scale up quickly, and the cluster autoscaler adds nodes before resources are exhausted. Tests cover multiple scenarios: sudden spikes, gradual increases, steady-state, and scale-down.

## Design Decisions

- **HPA Validation**: Test that Horizontal Pod Autoscaler triggers correctly
- **Scale-Up Speed**: Measure time from load increase to pod readiness
- **Scale-Down Grace**: Ensure scale-down doesn't drop active connections
- **Node Autoscaler**: Verify cluster autoscaler adds nodes on demand

## Implementation Approach

```typescript
test('HPA scales up pods when CPU exceeds threshold', async () => {
  await sendLoad({ rps: 10, duration: '1m' });
  const initialPods = await getPodCount('voice-service');
  await sendLoad({ rps: 200, duration: '5m' });
  const startTime = Date.now();
  let pods;
  while (Date.now() - startTime < 300000) {
    pods = await getPodCount('voice-service');
    if (pods > initialPods) break;
    await sleep(5000);
  }
  expect(pods).toBeGreaterThan(initialPods);
  const latencyAfter = await getLatencyStats();
  expect(latencyAfter.p95).toBeLessThan(500);
  await sendLoad({ rps: 5, duration: '10m' });
  const scaledDown = await waitForScaleDown(initialPods, 300000);
  expect(scaledDown).toBe(true);
});
```

## Integration Points

- **Kubernetes API**: Direct interaction for pod monitoring
- **Prometheus**: HPA metrics read from Prometheus
- **Cluster Autoscaler**: Tests interact with CA logs

## Open-Source Tools

- **k6-operator** (AGPL 3.0): Kubernetes-native k6 execution
- **Kubernetes Metrics Server** (Apache 2.0): HPA metrics
- **Cluster Autoscaler** (Apache 2.0): Node scaling

## Production Considerations

- **Test Isolation**: Run in isolated namespaces
- **Cost Impact**: Monitor resource costs during scaling tests
