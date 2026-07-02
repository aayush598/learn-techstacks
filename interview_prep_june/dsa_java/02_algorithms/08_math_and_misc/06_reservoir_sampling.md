# Reservoir Sampling

**Problem**: Select k random items from a stream of unknown size n, where each item has equal probability k/n of being selected.

## Algorithm

```java
public int[] reservoirSample(int[] stream, int k) {
    int[] reservoir = new int[k];
    Random rand = new Random();

    // Fill reservoir with first k items
    for (int i = 0; i < k; i++) {
        reservoir[i] = stream[i];
    }

    // For each subsequent item, replace with probability k/i
    for (int i = k; i < stream.length; i++) {
        int j = rand.nextInt(i + 1);
        if (j < k) {
            reservoir[j] = stream[i];
        }
    }

    return reservoir;
}
```

## Proof of Uniform Probability

For item i (where i ≥ k):
- Probability of being in reservoir when processed = k/(i+1)
- Probability of staying = Π (1 - 1/j) for j from i+2 to n = (i+1)/n
- Total probability = k/(i+1) × (i+1)/n = k/n ✓

## Key Insight

> Reservoir sampling solves the problem of random sampling from streams. Each item has exactly k/n probability of being in the final sample.
