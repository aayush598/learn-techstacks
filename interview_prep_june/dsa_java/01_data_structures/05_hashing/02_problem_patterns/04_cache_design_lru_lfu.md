# Cache Design: LRU and LFU

## LRU Cache (Least Recently Used)

Evicts the **least recently accessed** item when capacity is full.

### Approach 1: LinkedHashMap (Built-in)

```java
class LRUCache extends LinkedHashMap<Integer, Integer> {
    private int capacity;
    
    LRUCache(int capacity) {
        super(capacity, 0.75f, true);  // accessOrder = true
        this.capacity = capacity;
    }
    
    int get(int key) { return super.getOrDefault(key, -1); }
    
    void put(int key, int value) { super.put(key, value); }
    
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
        return size() > capacity;
    }
}
```

### Approach 2: HashMap + DoublyLinkedList (O(1) get/put)

```java
class LRUCache {
    class Node {
        int key, value;
        Node prev, next;
        Node(int k, int v) { key = k; value = v; }
    }
    
    private Map<Integer, Node> map;
    private Node head, tail;  // head.next = MRU, tail.prev = LRU
    private int capacity;
    
    LRUCache(int capacity) {
        this.capacity = capacity;
        map = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }
    
    int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        moveToFront(node);
        return node.value;
    }
    
    void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            moveToFront(node);
        } else {
            Node node = new Node(key, value);
            map.put(key, node);
            addToFront(node);
            if (map.size() > capacity) {
                Node removed = removeLast();
                map.remove(removed.key);
            }
        }
    }
    
    private void addToFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
    
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void moveToFront(Node node) {
        removeNode(node);
        addToFront(node);
    }
    
    private Node removeLast() {
        Node node = tail.prev;
        removeNode(node);
        return node;
    }
}
```

## LFU Cache (Least Frequently Used)

Evicts the **least frequently used** item. If tie, evict LRU among those.

```java
class LFUCache {
    private int capacity, minFreq;
    private Map<Integer, Integer> keyToVal;      // key -> value
    private Map<Integer, Integer> keyToFreq;     // key -> frequency
    private Map<Integer, LinkedHashSet<Integer>> freqToKeys;  // freq -> set of keys
    
    LFUCache(int capacity) {
        this.capacity = capacity;
        keyToVal = new HashMap<>();
        keyToFreq = new HashMap<>();
        freqToKeys = new HashMap<>();
        freqToKeys.put(1, new LinkedHashSet<>());
    }
    
    int get(int key) {
        if (!keyToVal.containsKey(key)) return -1;
        increaseFreq(key);
        return keyToVal.get(key);
    }
    
    void put(int key, int value) {
        if (capacity == 0) return;
        
        if (keyToVal.containsKey(key)) {
            keyToVal.put(key, value);
            increaseFreq(key);
            return;
        }
        
        if (keyToVal.size() >= capacity) {
            int evict = freqToKeys.get(minFreq).iterator().next();
            freqToKeys.get(minFreq).remove(evict);
            keyToVal.remove(evict);
            keyToFreq.remove(evict);
        }
        
        keyToVal.put(key, value);
        keyToFreq.put(key, 1);
        freqToKeys.computeIfAbsent(1, k -> new LinkedHashSet<>()).add(key);
        minFreq = 1;
    }
    
    private void increaseFreq(int key) {
        int freq = keyToFreq.get(key);
        keyToFreq.put(key, freq + 1);
        freqToKeys.get(freq).remove(key);
        
        if (freqToKeys.get(freq).isEmpty() && freq == minFreq) {
            minFreq++;
        }
        
        freqToKeys.computeIfAbsent(freq + 1, k -> new LinkedHashSet<>()).add(key);
    }
}
```
