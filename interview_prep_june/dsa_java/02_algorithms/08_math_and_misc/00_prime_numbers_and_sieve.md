# Prime Numbers & Sieve

## Check if Prime (O(√n))

```java
public boolean isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}
```

## Sieve of Eratosthenes (O(n log log n))

```java
public boolean[] sieve(int n) {
    boolean[] isPrime = new boolean[n + 1];
    Arrays.fill(isPrime, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }

    return isPrime;
}
```

## Segmented Sieve

For large ranges [L, R] where R - L ≤ 10^6 but R up to 10^12.

```java
public boolean[] segmentedSieve(long L, long R) {
    int limit = (int) Math.sqrt(R);
    boolean[] sqrtPrimes = sieve(limit); // regular sieve up to sqrt(R)

    // Only the segment
    int n = (int) (R - L + 1);
    boolean[] isPrime = new boolean[n];
    Arrays.fill(isPrime, true);

    for (int i = 2; i <= limit; i++) {
        if (sqrtPrimes[i]) {
            long start = Math.max((long) i * i, (L + i - 1) / i * i);
            for (long j = start; j <= R; j += i) {
                isPrime[(int) (j - L)] = false;
            }
        }
    }

    return isPrime;
}
```

## Prime Factorization

```java
public List<Integer> primeFactors(int n) {
    List<Integer> factors = new ArrayList<>();
    while (n % 2 == 0) { factors.add(2); n /= 2; }
    for (int i = 3; i * i <= n; i += 2) {
        while (n % i == 0) { factors.add(i); n /= i; }
    }
    if (n > 1) factors.add(n);
    return factors;
}

// Using smallest prime factor (SPF) — O(log n) per query
int[] spf = new int[n + 1];
void computeSPF(int n) {
    for (int i = 0; i <= n; i++) spf[i] = i;
    for (int i = 2; i * i <= n; i++) {
        if (spf[i] == i) {
            for (int j = i * i; j <= n; j += i) {
                if (spf[j] == j) spf[j] = i;
            }
        }
    }
}

List<Integer> fastFactorize(int x) {
    List<Integer> factors = new ArrayList<>();
    while (x > 1) {
        factors.add(spf[x]);
        x /= spf[x];
    }
    return factors;
}
```
