# Fractional Knapsack

**Problem**: Items with weight and value. You can take fractions of items. Maximize total value for given capacity.

**Greedy**: Sort by value/weight ratio descending. Take as much as possible of the best ratio item.

```java
class Item {
    int value, weight;
    double ratio;
    Item(int v, int w) {
        value = v; weight = w; ratio = (double) v / w;
    }
}

public double fractionalKnapsack(int[] values, int[] weights, int capacity) {
    int n = values.length;
    Item[] items = new Item[n];
    for (int i = 0; i < n; i++) {
        items[i] = new Item(values[i], weights[i]);
    }

    Arrays.sort(items, (a, b) -> Double.compare(b.ratio, a.ratio));

    double totalValue = 0;
    int remaining = capacity;

    for (Item item : items) {
        if (item.weight <= remaining) {
            totalValue += item.value;
            remaining -= item.weight;
        } else {
            totalValue += item.ratio * remaining;
            break;
        }
    }

    return totalValue;
}
```

## Key Insight

> Fractional knapsack is greedy (unlike 0/1 knapsack which is DP) because we can take fractions. The optimal strategy is always to take the highest value-per-weight item.
