# Reservoir Sampling

**Problem**: Select k random items from a stream of unknown size n, where each item has equal probability k/n of being selected.

## Algorithm R (Knuth's Algorithm)

The classic algorithm by Alan Waterman (presented by Knuth in TAOCP Vol 2):

1. Fill a reservoir of size k with the first k items.
2. For each subsequent item i (i ≥ k), generate a random index j in [0, i].
3. If j < k, replace reservoir[j] with the current item.

```java
import java.util.Random;

public class ReservoirSampling {

    private final Random rand;

    public ReservoirSampling() {
        this.rand = new Random();
    }

    public int[] sample(int[] stream, int k) {
        if (stream.length < k) {
            throw new IllegalArgumentException("Stream smaller than k");
        }

        int[] reservoir = new int[k];

        // Fill reservoir with first k items
        for (int i = 0; i < k; i++) {
            reservoir[i] = stream[i];
        }

        // For each subsequent item, replace with probability k/i
        for (int i = k; i < stream.length; i++) {
            int j = rand.nextInt(i + 1);  // random index in [0, i]
            if (j < k) {
                reservoir[j] = stream[i];
            }
        }

        return reservoir;
    }

    public static void main(String[] args) {
        int[] stream = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5};
        ReservoirSampling rs = new ReservoirSampling();
        int[] sample = rs.sample(stream, 3);
        // Sample of 3 items from the stream
        for (int val : sample) {
            System.out.print(val + " ");
        }
    }
}
```

## Proof of Uniform Probability

Each item in the stream must have probability k/n of being in the final sample.

**For initial items** (i < k):
- Initially in reservoir with probability 1
- For each later item at position t (t ≥ k), probability it replaces this item = k/(t+1) × 1/k = 1/(t+1)
- Probability of survival through all t = Π (1 - 1/(t+1)) for t from k to n-1
- = Π (t/(t+1)) = k/n

**For items after k** (i ≥ k):
- Probability of entering at step i = k/(i+1) (j < k out of i+1 choices)
- Probability of surviving subsequent steps = Π (1 - 1/(t+1)) for t from i+1 to n-1 = (i+1)/n
- Total probability = k/(i+1) × (i+1)/n = k/n ✓

Every element has exactly k/n probability — the algorithm is correct.

## Weighted Reservoir Sampling

When items have different weights (probability proportional to weight):

```java
public class WeightedReservoirSampling {

    private final Random rand;

    public WeightedReservoirSampling() {
        this.rand = new Random();
    }

    public int[] weightedSample(int[] stream, int[] weights, int k) {
        if (stream.length < k) return null;

        int[] reservoir = new int[k];
        // Store cumulative weight for reservoir items (A-Chao algorithm)
        double[] key = new double[k];

        // Fill first k items with random keys based on weight
        for (int i = 0; i < k; i++) {
            reservoir[i] = stream[i];
            key[i] = Math.pow(rand.nextDouble(), 1.0 / weights[i]);
        }

        // For remaining items
        for (int i = k; i < stream.length; i++) {
            double newKey = Math.pow(rand.nextDouble(), 1.0 / weights[i]);
            // Find smallest key in reservoir
            int minIdx = 0;
            for (int j = 1; j < k; j++) {
                if (key[j] < key[minIdx]) minIdx = j;
            }
            // Replace if new item has larger key (higher weight priority)
            if (newKey > key[minIdx]) {
                reservoir[minIdx] = stream[i];
                key[minIdx] = newKey;
            }
        }

        return reservoir;
    }
}
```

This is the A-Chao algorithm: each item gets a random key = U^(1/w), where U ~ Uniform(0,1) and w is the weight. The k items with the largest keys are selected.

## Application: Random Shuffle (Fisher-Yates via Reservoir)

Reservoir sampling with k = n gives a random permutation:

```java
public class ReservoirShuffle {

    public static void shuffle(int[] arr) {
        Random rand = new Random();
        for (int i = arr.length - 1; i > 0; i--) {
            int j = rand.nextInt(i + 1);
            // Swap arr[i] with arr[j]
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
}
```

This is Fisher-Yates shuffle — equivalent to reservoir sampling where k = n.

## Application: Random Row from Database

```java
public class DatabaseRandomRow {

    // Simulate selecting random row from table without knowing count
    public static Object selectRandomRow(java.sql.ResultSet rs) throws Exception {
        Object selected = null;
        int count = 0;
        Random rand = new Random();

        while (rs.next()) {
            count++;
            // Probability 1/count of picking this row (k=1 reservoir)
            if (rand.nextInt(count) == 0) {
                selected = rs.getObject(1); // or construct row object
            }
        }

        return selected; // each row had 1/n probability
    }
}
```

## Application: Load Balancing (Random Server Selection)

```java
public class LoadBalancer {

    private final Random rand = new Random();
    private String selected;
    private int count;

    // Using reservoir sampling with k=1 to pick a random server from a stream
    // (e.g., from a list of healthy servers received in chunks)
    public void addServer(String server) {
        count++;
        if (rand.nextInt(count) == 0) {
            selected = server;
        }
    }

    public String getSelectedServer() {
        return selected;
    }
}
```

## Edge Cases and Variations

```java
public class ReservoirEdgeCases {

    public static void main(String[] args) {
        ReservoirSampling rs = new ReservoirSampling();

        // k = 1: equivalent to uniformly random element
        int[] stream = {10, 20, 30, 40, 50};
        int[] single = rs.sample(stream, 1);
        // Each element has 1/5 probability

        // k = n: full shuffle (all elements selected)
        int[] all = rs.sample(stream, stream.length);
        // Returns all elements but in random order (same as Fisher-Yates)

        // k = 0: no elements (edge case)
        // int[] empty = rs.sample(stream, 0); // would throw

        // Large stream: works with any length, O(n) time
        int[] large = new int[1_000_000];
        for (int i = 0; i < large.length; i++) large[i] = i;
        int[] sample = rs.sample(large, 100); // 100 random elements
    }

    // Streaming variant (doesn't need array — processes one element at a time)
    public static class StreamingSampler {
        private final int[] reservoir;
        private final Random rand;
        private int count;

        public StreamingSampler(int k) {
            this.reservoir = new int[k];
            this.rand = new Random();
            this.count = 0;
        }

        public void process(int value) {
            if (count < reservoir.length) {
                reservoir[count] = value;
            } else {
                int j = rand.nextInt(count + 1);
                if (j < reservoir.length) {
                    reservoir[j] = value;
                }
            }
            count++;
        }

        public int[] getSample() {
            return reservoir;
        }
    }
}
```

## Complexity

| Aspect | Value |
|--------|-------|
| Time | O(n) — one pass through the stream |
| Space | O(k) — reservoir size |
| Random calls | O(n) — one per element |

## Key Insight

> Reservoir sampling solves the problem of random sampling from streams. The elegant property is that when item i arrives, it has probability k/(i+1) of entering the reservoir, and the current reservoir is always a uniform random k-subset of the items seen so far. No extra passes or O(n) storage needed.
