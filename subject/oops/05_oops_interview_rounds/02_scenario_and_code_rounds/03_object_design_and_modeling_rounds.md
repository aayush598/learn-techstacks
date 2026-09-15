# Object Design and Modeling Rounds — 100 Interview Q&A

## Q1: Design a basic `User` class with authentication capabilities.

**A:** A `User` class should encapsulate identity, credentials, and authentication behavior. Key fields include a unique identifier, username, email, hashed password, and status (active, locked, banned). The class must enforce invariants: emails must be valid, passwords must be hashed (never stored in plain text), and a locked user cannot authenticate. Methods include `authenticate(password)`, `lock()`/`unlock()`, and `changePassword(old, new)`.

The design follows encapsulation by making the password hash private with no getter. Authentication logic belongs in the User entity because it operates on User-owned data (the password hash). A separate `AuthService` handles session management, token generation, and external provider integration, but core credential verification stays in the domain object. This is a rich domain model approach.

Security considerations include using bcrypt or Argon2 for password hashing (never MD5/SHA1), rate limiting login attempts, and ensuring the `authenticate` method is timing-attack resistant. The User class should be immutable where possible — changes to profile data create new copies rather than modifying in place, making concurrent access safer.

**Example:**
```java
class User {
    private final String id;
    private final String email;
    private final String passwordHash;
    private UserStatus status;

    boolean authenticate(String password) {
        if (status != UserStatus.ACTIVE) return false;
        return BCrypt.checkpw(password, this.passwordHash);
    }
}
```

## Q2: Design a `Library` system that manages books and borrowers.

**A:** A Library system requires three core entities: `Book` (title, author, ISBN, copies available), `Borrower` (name, ID, borrowed books), and `Loan` (association between borrower and book with issue/due dates). The `Library` class coordinates these entities, providing operations like `borrowBook(borrowerId, isbn)`, `returnBook(loanId)`, and `searchBooks(query)`.

The key design decisions involve the relationships. A Book can have multiple Loans over time but only one active Loan per copy. A Borrower can have multiple active Loans. The Library class acts as a facade, coordinating between Book, Borrower, and Loan repositories. Business rules include: borrowers cannot exceed their loan limit, overdue books trigger fines, and books must be available (copies > 0) to be borrowed.

Use the Repository pattern for persistence and the Unit of Work pattern to ensure atomicity of borrow/return operations. A `Loan` value object encapsulates the issue date, due date, and fine calculation logic. The `Library` facade keeps the API simple while the internal complexity is managed by well-designed domain objects.

**Example:**
```python
class Book:
    def __init__(self, isbn, title, author, total_copies):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.borrowed_count = 0

    @property
    def available_copies(self):
        return self.total_copies - self.borrowed_count
```

## Q3: Design a `ParkingLot` system with capacity management.

**A:** A ParkingLot should manage parking spots, vehicles, and the parking/unparking workflow. Core entities: `ParkingSpot` (type: compact/standard/large/motorcycle, status: available/occupied), `Vehicle` (plate number, type), `Ticket` (issue time, spot assignment, vehicle). The `ParkingLot` is a singleton that orchestrates spot allocation, fee calculation, and capacity tracking.

The key operations are `parkVehicle(vehicle)` which finds an available spot of the right type, assigns it, and issues a ticket; `unparkVehicle(ticketId)` which calculates the fee, frees the spot, and processes payment; and `getAvailableSpots()` for capacity queries. The fee calculation strategy should be encapsulated in a `FeeStrategy` interface, following the Strategy pattern for flexibility.

Design considerations include thread safety (multiple attendants can park/unpark simultaneously), scalability (multiple levels/floors, each a `ParkingFloor`), and the Singleton pattern for the ParkingLot instance. Display boards showing available spots per floor should be updated reactively using the Observer pattern.

**Example:**
```java
class ParkingLot {
    private static ParkingLot instance;
    private List<ParkingFloor> floors;

    ParkingTicket parkVehicle(Vehicle v) {
        for (ParkingFloor floor : floors) {
            ParkingSpot spot = floor.findSpot(v.getType());
            if (spot != null) {
                spot.assign(v);
                return new ParkingTicket(v, spot, LocalDateTime.now());
            }
        }
        throw new LotFullException();
    }
}
```

## Q4: Design an `Elevator` system for a multi-floor building.

**A:** An Elevator system manages elevator cars, floor requests, and scheduling. Core entities: `Elevator` (current floor, direction, state: idle/moving/door-open), `Floor` (number, buttons up/down), `ElevatorController` (receives requests, dispatches elevators), and `Request` (origin floor, destination floor). The design requires efficient scheduling algorithms (SCAN, LOOK) and state management for each elevator.

Each `Elevator` has an internal state machine (IdleState, MovingUpState, MovingDownState, DoorOpenState) implemented via the State pattern. The controller maintains a queue of pending requests and assigns them to elevators using a scheduler. The SCAN algorithm moves the elevator in one direction, servicing all requests in that direction before reversing.

The Observer pattern is used for real-time updates: floor buttons and elevator displays subscribe to the controller's events. Thread safety is critical — multiple passengers can request elevators simultaneously. Use `ConcurrentLinkedQueue` for request queues and atomic operations for elevator state transitions.

**Example:**
```python
class Elevator:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.direction = None
        self.state = IdleState()
        self.queue = []

    def add_request(self, floor):
        self.queue.append(floor)
        self.state.handle(self)
```

## Q5: Design a `Hotel` reservation system.

**A:** A Hotel reservation system involves Room, Guest, Reservation, and Hotel entities. `Room` has a number, type (single/double/suite), status (available/occupied/maintenance), and rate. `Reservation` links a Guest to a Room for a date range with a status (pending, confirmed, checked-in, checked-out, cancelled). The `Hotel` class coordinates room availability, reservation management, and check-in/check-out workflows.

The core challenge is date-based availability. Checking room availability requires searching for reservations that overlap with the requested date range. A `RoomInventory` class maintains a date-indexed view of room availability for fast lookup. Reservation creation must be atomic — two guests cannot book the same room for overlapping dates simultaneously.

Pricing strategy should be flexible: different rates for weekdays/weekends, seasonal pricing, corporate rates, and early-bird discounts. A `PricingStrategy` interface with multiple implementations handles this. The Observer pattern notifies the cleaning service, billing system, and front desk of status changes.

**Example:**
```java
class Reservation {
    private String roomId;
    private String guestId;
    private LocalDate checkIn;
    private LocalDate checkOut;
    private ReservationStatus status;

    boolean overlaps(LocalDate start, LocalDate end) {
        return this.checkIn.isBefore(end) && this.checkOut.isAfter(start);
    }
}
```

## Q6: Design a `File System` with directories and files.

**A:** A file system is a classic Composite pattern application. The base abstraction is `FileSystemNode` with `getName()`, `getSize()`, `getFullPath()`, and `list()` methods. Two concrete types: `File` (leaf — has content, size) and `Directory` (composite — contains child nodes). A directory's size is the sum of all children's sizes (recursive).

Operations include `createFile(path, content)`, `createDirectory(path)`, `delete(path)`, `move(path, newPath)`, `copy(path, newPath)`, and `search(pattern)`. The `FileSystem` class acts as a facade over the root directory, parsing paths and delegating to the appropriate nodes. Path resolution handles absolute paths, relative paths, and symbolic links.

Design considerations include permission management (each node has an owner, group, and permission bits), efficient searching (index files by name for O(1) lookup), and lazy loading for large directory trees.

**Example:**
```python
class FileSystemNode:
    def __init__(self, name):
        self.name = name
        self.parent = None

class File(FileSystemNode):
    def __init__(self, name, content=""):
        super().__init__(name)
        self.content = content
    def get_size(self):
        return len(self.content)

class Directory(FileSystemNode):
    def __init__(self, name):
        super().__init__(name)
        self.children = []
    def get_size(self):
        return sum(c.get_size() for c in self.children)
```

## Q7: Design a `Chess` game with piece movement and validation.

**A:** A Chess game requires a `Board` (8x8 grid), `Piece` subclasses (King, Queen, Rook, Bishop, Knight, Pawn), `Player`, `Move`, and `Game` classes. Each piece defines its valid movement pattern. The `Board` manages piece placement and provides methods for piece lookup and move execution.

The key design insight is using polymorphism for piece movement: each piece subclass overrides a `getValidMoves(board, position)` method that returns only legal moves. The `Board` handles the mechanics of move execution, while each `Piece` knows its own movement rules.

Advanced features include: move validation that checks for self-check, checkmate detection (no valid moves exist and the king is in check), stalemate detection, and move history for undo. The Command pattern is ideal for moves — each `Move` object captures the piece, origin, destination, and captured piece, enabling clean undo.

**Example:**
```java
abstract class Piece {
    abstract List<Position> getValidMoves(Board board, Position pos);
}

class Knight extends Piece {
    List<Position> getValidMoves(Board board, Position pos) {
        int[][] offsets = {{2,1},{2,-1},{-2,1},{-2,-1},{1,2},{1,-2},{-1,2},{-1,-2}};
        // filter valid positions
    }
}
```

## Q8: Design a `Traffic Light` control system.

**A:** A TrafficLight system manages signal states, timing, and coordination across intersections. Core entities: `TrafficLight` (current state: red/yellow/green, duration per state), `Intersection` (collection of traffic lights), `SignalController` (manages timing and synchronization). Each `TrafficLight` follows a strict state cycle: Green → Yellow → Red → Green, enforced by a state machine.

The State pattern is ideal: `GreenState`, `YellowState`, `RedState` each implement a `next()` method that transitions to the appropriate next state. The `SignalController` manages the global timing — coordinating lights at an intersection to prevent conflicting green signals.

Pedestrian crossing adds complexity: a pedestrian button request should interrupt the current cycle. Emergency vehicle preemption is another event that forces all lights to red except the emergency direction. The Observer pattern notifies all lights of controller decisions.

**Example:**
```python
class TrafficLight:
    def __init__(self):
        self.state = RedState()
        self.duration = {"green": 30, "yellow": 5, "red": 25}

    def tick(self):
        self.state.next(self)

class GreenState:
    def next(self, light):
        light.state = YellowState()
```

## Q9: Design a `Vending Machine` with product dispensing and inventory.

**A:** A VendingMachine manages product inventory, accepts payment, and dispenses products. Core entities: `Product` (name, price, quantity), `Slot` (product reference, quantity), `Coin` (denomination), and `VendingMachine` (state, slots, inserted coins). The machine has states: Idle, HasMoney, Dispensing, and ReturnChange, managed via the State pattern.

The State pattern handles the workflow: in Idle state, the machine only accepts product selection. In HasMoney state, it accepts coins and product selection. In Dispensing state, it releases the product. In ReturnChange state, it returns excess coins. Each state object implements the valid operations for that state.

The `selectProduct(slotId)` method checks that the slot has inventory and that the inserted amount covers the price. The change calculation should use a greedy algorithm for simplicity, or dynamic programming for optimal coin usage.

**Example:**
```java
interface VendingState {
    void insertCoin(VendingMachine machine, Coin coin);
    void selectProduct(VendingMachine machine, int slotId);
}

class IdleState implements VendingState {
    public void insertCoin(VendingMachine m, Coin c) {
        m.addCoin(c);
        m.setState(new HasMoneyState());
    }
}
```

## Q10: Design a `Chat Application` with messaging and user management.

**A:** A ChatApplication manages users, conversations, and messages. Core entities: `User` (id, name, status), `Conversation` (participants, messages), `Message` (sender, content, timestamp, read status), and `ChatService` (orchestrates operations). Conversations can be one-on-one or group. The system supports real-time message delivery, read receipts, and message history.

The key design challenge is message delivery. The Observer pattern is central: when a user sends a message, the conversation notifies all online participants. For offline users, messages are queued and delivered on reconnect. The `ChatService` manages user sessions, mapping user IDs to active connections.

Design considerations include: message ordering (use timestamps or sequence numbers), eventual consistency for read receipts, support for different message types (text, image, file), and conversation management (creating/leaving groups, admin permissions). For scalability, conversations are partitioned by ID.

**Example:**
```python
class ChatRoom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.participants = set()
        self.messages = []

    def send(self, message):
        self.messages.append(message)
        for p in self.participants:
            if p.is_online:
                p.notify(message)
```

## Q11: Design an `Online Shopping Cart` with pricing rules.

**A:** A ShoppingCart manages items, quantities, and pricing calculations. Core entities: `CartItem` (product, quantity), `ShoppingCart` (items, customer), `Product` (name, base price, category), and `PricingRule` (discount strategy). The cart calculates totals by applying base prices, quantity discounts, category discounts, coupon codes, and tax.

Pricing should use the Strategy pattern: `PricingRule` is an interface with `calculate(items)` method. Implementations include `FlatDiscount`, `PercentageDiscount`, `BuyXGetYFree`, and `CategoryDiscount`. The cart applies rules in a defined order using a chain of responsibility. Each rule can modify the running total.

The `addItem(product, quantity)` method checks inventory, adds to the item list, and triggers price recalculation. The cart should support both authenticated users (persistent cart) and anonymous users (session-based cart). Cart merging happens when an anonymous user logs in. Thread safety is essential for concurrent cart modifications.

**Example:**
```java
interface PricingRule {
    Money apply(List<CartItem> items, Money subtotal);
}

class PercentageDiscount implements PricingRule {
    private double percentage;
    public Money apply(List<CartItem> items, Money subtotal) {
        return subtotal.multiply(1 - percentage);
    }
}
```

## Q12: Design a `Weather Station` system with data collection and display.

**A:** A WeatherStation collects weather data from sensors and displays it on multiple output devices. Core entities: `Sensor` (temperature, humidity, pressure), `WeatherData` (readings with timestamps), `Display` (shows data in a format), and `WeatherStation` (coordinates sensors and displays). The Observer pattern is the backbone: sensors are subjects, displays are observers.

When a sensor reading changes, the `WeatherStation` notifies all registered displays. Each display implements an `update(data)` method with its own rendering logic. A `CurrentConditionsDisplay` shows the latest readings, a `StatisticsDisplay` shows min/max/average, and a `ForecastDisplay` shows predictions.

Design considerations include: data persistence in a time-series database, alerting (register alert observers that trigger when thresholds are exceeded), and data aggregation. The station should support hot-swapping sensors through the Adapter pattern for different sensor protocols.

**Example:**
```python
class WeatherStation:
    def __init__(self):
        self.observers = []
        self.readings = {}

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self):
        for obs in self.observers:
            obs.update(self.readings)
```

## Q13: Design a `Document Editor` with formatting capabilities.

**A:** A DocumentEditor manages document content with formatting, supporting operations like typing, bold/italic, font changes, and undo/redo. Core entities: `Document` (list of elements), `TextElement` (text + formatting attributes), `FormattingRun` (font, size, bold, italic, color), and `Editor` (handles user input). The Composite pattern models the document structure.

Formatting is modeled as `FormattingRun` value objects attached to text ranges. When the user selects text and applies bold, the affected runs are split and the selected portion gets a bold run. The `Document` maintains a list of runs that, combined with the text, fully describe the document.

The Command pattern handles user operations: `TypeCommand`, `BoldCommand`, `UndoCommand`, `RedoCommand`. Each command is a reversible operation stored in a history stack. The `Clipboard` manages cut/copy/paste using the Memento pattern.

**Example:**
```java
class TextElement {
    private String text;
    private FormattingRun format;
    TextElement(String text, FormattingRun format) {
        this.text = text;
        this.format = format;
    }
}

class FormattingRun {
    String font; int size; boolean bold, italic;
}
```

## Q14: Design an `ATM` machine with account management.

**A:** An ATM system manages user authentication, account operations, and cash dispensing. Core entities: `ATM` (state, cash inventory), `Card` (card number, PIN, linked accounts), `Account` (number, balance, type: checking/savings), `Transaction` (type, amount, timestamp, balance after). The ATM follows a strict state machine: Welcome → PIN Entry → Account Selection → Transaction Type → Dispensing Cash → Eject Card.

Each ATM state is a State pattern implementation. The `WelcomeState` accepts card insertion. The `PinEntryState` validates the PIN. The `AccountSelectionState` presents linked accounts. The `TransactionState` handles withdrawal, deposit, and balance inquiry. Cash dispensing must be atomic.

Security considerations include: PIN validation must be timing-attack resistant, cards are locked after 3 failed PIN attempts, and transaction limits apply per card and per account. The `CashDispenser` manages the physical note inventory.

**Example:**
```java
interface ATMState {
    void insertCard(ATM atm, Card card);
    void enterPin(ATM atm, int pin);
    void selectAccount(ATM atm, Account account);
}

class WelcomeState implements ATMState {
    public void insertCard(ATM atm, Card card) {
        atm.setCard(card);
        atm.setState(new PinEntryState());
    }
}
```

## Q15: Design a `Stock Trading` platform with order matching.

**A:** A StockTrading platform manages orders, matches buyers and sellers, and executes trades. Core entities: `Order` (type: buy/sell, symbol, quantity, price, timestamp), `OrderBook` (collection of pending orders for a symbol), `Trade` (matched buy and sell orders, execution price), and `Trader` (account balance, portfolio). The order book maintains sorted buy orders (highest price first) and sell orders (lowest price first).

Order matching uses the price-time priority algorithm: the best buy order (highest price, earliest time) is matched against the best sell order (lowest price, earliest time). If the buy price >= sell price, a trade is executed. Partial fills are supported.

Design considerations include: limit orders vs. market orders, order cancellation, trade settlement, and market data streaming via WebSocket/Observer pattern. The `OrderBook` should use a `PriorityQueue` for efficient best-price lookup.

**Example:**
```java
class OrderBook {
    private PriorityQueue<Order> buyOrders;  // max heap by price
    private PriorityQueue<Order> sellOrders; // min heap by price

    List<Trade> match(Order newOrder) {
        List<Trade> trades = new ArrayList<>();
        while (canMatch(newOrder)) {
            Order best = getBestOpposite(newOrder.getType());
            Trade trade = execute(newOrder, best);
            trades.add(trade);
        }
        return trades;
    }
}
```

## Q16: Design a `Movie Ticket Booking` system like BookMyShow.

**A:** A MovieTicketBooking system manages movies, theaters, shows, seats, and user bookings. Core entities: `Movie` (title, duration, rating), `Theater` (name, location, screens), `Screen` (seat layout, show times), `Show` (movie, screen, time, available seats), `Seat` (number, type: regular/premium/royal, status), and `Booking` (user, show, seats, payment status).

The critical design challenge is seat locking during booking. When a user selects seats, they must be temporarily locked (held for 5-10 minutes) to prevent double-booking. This requires a distributed lock mechanism — use Redis-based locks or optimistic locking with version numbers. If the user completes payment, the lock becomes a confirmed booking. If timeout occurs, the seats are released.

The `Show` class manages seat availability using a 2D matrix (or a `SeatMap` object). `getAvailableSeats()` returns unbooked seats. `reserveSeats(seatIds)` atomically marks seats as held. The booking flow is: select show → select seats → hold seats (with timer) → make payment → confirm booking → release lock. The Observer pattern notifies users of show announcements and booking confirmations.

**Example:**
```python
class SeatMap:
    def __init__(self, rows, cols):
        self.seats = [[Seat(r, c) for c in range(cols)] for r in range(rows)]

    def available_seats(self):
        return [s for row in self.seats for s in row if s.is_available()]

    def hold(self, seat_ids, timeout=300):
        for sid in seat_ids:
            s = self.get(seat_ids)
            if not s.is_available():
                raise SeatUnavailableException()
            s.hold(timeout)
```

## Q17: Design a `Ride Sharing` system like Uber/lyft.

**A:** A RideSharing system manages riders, drivers, ride requests, and trip matching. Core entities: `Rider` (profile, payment), `Driver` (profile, vehicle, location, status), `Ride` (rider, driver, pickup, dropoff, fare, status), `Location` (latitude, longitude), and `TripMatcher` (finds optimal driver). The system must handle real-time location tracking, ETA calculation, and dynamic pricing.

The key algorithm is driver matching: when a rider requests a ride, the system finds the nearest available driver within a radius. This requires a spatial index — use a geospatial hash grid (like S2 cells or H3) for O(1) lookup of nearby drivers. The matching criteria include distance, driver rating, vehicle type, and surge pricing eligibility.

The ride lifecycle follows a state machine: Requested → Matching → Accepted → Arriving → InProgress → Completed → Rated. Each state transition triggers notifications (Observer pattern): rider gets driver ETA, driver gets rider location, both get trip updates. Dynamic pricing (surge) adjusts fares based on supply/demand ratio in a geographic zone. The `FareCalculator` uses the Strategy pattern to support different pricing models (flat, metered, surge, shared).

**Example:**
```python
class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def distance_to(self, other):
        return haversine(self.lat, self.lng, other.lat, other.lng)

class TripMatcher:
    def find_driver(self, pickup, vehicle_type, radius=5.0):
        nearby = self.spatial_index.query(pickup, radius)
        available = [d for d in nearby if d.is_available()]
        return min(available, key=lambda d: d.location.distance_to(pickup))
```

## Q18: Design a `Restaurant Reservation` system.

**A:** A RestaurantReservation system manages restaurants, tables, time slots, and reservations. Core entities: `Restaurant` (name, capacity, table layout), `Table` (number, capacity, status), `TimeSlot` (date, time, duration), `Reservation` (restaurant, table, party size, time slot, customer), and `ReservationSystem` (orchestrates bookings).

The core challenge is table allocation. A reservation for 4 people needs a table that seats at least 4 but not much more (waste of capacity). The allocation algorithm finds the best-fit table: smallest available table that fits the party size. Overlapping reservations on the same table must be prevented using date-time range checks.

The system should support: walk-in management (mark tables as occupied in real-time), waitlist management (when full, add to queue and notify when table opens), and cancellation policies (free cancellation up to 2 hours before). The Observer pattern notifies restaurant staff of new reservations and cancellations. The `AvailabilityChecker` handles complex queries: "What times are available for 6 people on Saturday?" requires scanning all tables and finding time slots where a suitable table is free.

**Example:**
```java
class Table {
    int number;
    int capacity;
    List<Reservation> reservations;

    boolean isAvailable(LocalDateTime start, LocalDateTime end) {
        return reservations.stream()
            .noneMatch(r -> r.overlaps(start, end));
    }
}
```

## Q19: Design a `Social Media Feed` like Twitter/Instagram.

**A:** A SocialMediaFeed manages users, posts, followers, and feed generation. Core entities: `User` (id, name, followers, following), `Post` (author, content, timestamp, likes, comments), `Feed` (timeline of posts), and `FeedService` (generates personalized feeds). The key operations are: `createPost()`, `follow/unfollow()`, `like/comment()`, and `getFeed()`.

Feed generation is the critical design challenge. Two main approaches: push model (fan-out on write — when a user posts, immediately push to all followers' feeds) and pull model (fan-out on read — when a user requests their feed, pull posts from all followed users and sort). Push is better for read-heavy systems (celebrity problem: a celebrity's post reaches millions instantly). Pull is better for write-heavy systems with many followers per user.

Most systems use a hybrid: regular users use push (pre-computed feeds stored in Redis), celebrities use pull (their posts are fetched on-demand when the feed is loaded). The `FeedService` merges pre-computed feeds with on-demand celebrity posts. The Observer pattern handles real-time updates (new posts appear in feed without refresh). The `NewsFeed` uses a priority queue sorted by timestamp and relevance score.

**Example:**
```python
class FeedService:
    def get_feed(self, user_id, limit=20):
        precomputed = self.redis.get(f"feed:{user_id}") or []
        celebrity_posts = self.fetch_celebrity_posts(user_id)
        merged = heapq.merge(precomputed, celebrity_posts, key=lambda p: p.timestamp, reverse=True)
        return list(merged)[:limit]

    def on_post_created(self, post):
        for follower_id in post.author.followers:
            self.redis.lpush(f"feed:{follower_id}", post)
```

## Q20: Design a `URL Shortener` like bit.ly.

**A:** A URLShortener converts long URLs to short, unique URLs and redirects short URLs back to the original. Core entities: `ShortURL` (short code, original URL, creation time, expiration, click count), `User` (optional, for custom aliases and analytics), and `URLService` (handles shortening and lookup). The core operation: `shorten(url)` returns a short code; `expand(code)` returns the original URL.

The short code generation has several strategies: hash-based (SHA256 of URL, take first 7 chars — collision possible), counter-based (auto-increment ID, base62 encode — deterministic), or random (generate random 7-char alphanumeric — collision checked). The counter-based approach is simplest and most efficient: maintain an atomic counter, convert to base62 for a short, URL-safe code. The counter can be distributed using a database sequence or a Snowflake-like ID generator.

The redirect operation must be extremely fast (billions of redirects per day). Use a cache (Redis) for hot URLs and a database (DynamoDB, Cassandra) for the full mapping. Analytics track: click count, referrer, geographic location, timestamp. The `ClickEvent` is published to an analytics pipeline (Kafka) asynchronously so it doesn't slow down the redirect. The `URLService` handles expiration cleanup and custom aliases.

**Example:**
```python
import hashlib

class URLShortener:
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def shorten(self, url):
        url_hash = hashlib.md5(url.encode()).hexdigest()
        short_code = self._to_base62(int(url_hash[:8], 16))[:7]
        self.store.save(short_code, url)
        return short_code

    def expand(self, code):
        return self.store.get(code)

    def _to_base62(self, num):
        result = []
        while num > 0:
            result.append(self.ALPHABET[num % 62])
            num //= 62
        return ''.join(reversed(result))
```

## Q21: Design a `Payment Processing` system.

**A:** A PaymentProcessing system handles transactions between buyers, sellers, and payment providers. Core entities: `Payment` (amount, currency, status, timestamps), `PaymentMethod` (credit card, debit card, bank transfer — Strategy pattern), `Transaction` (record of money movement), `Wallet` (balance, holds), and `PaymentGateway` (interface to external providers like Stripe/PayPal).

The payment flow must be idempotent and atomic: create payment → authorize with provider → capture funds → update wallet balances → notify parties. The `PaymentService` orchestrates this flow using the Saga pattern for distributed transactions. If any step fails, compensating transactions undo previous steps (e.g., if wallet update fails after authorization, reverse the authorization).

Design considerations include: double-entry bookkeeping (every transfer debits one wallet and credits another — no money is created or destroyed), idempotency keys (prevent duplicate charges from retries), currency conversion (use real-time exchange rates with a `CurrencyConverter`), and compliance (PCI DSS for card data, audit logs for all transactions). The `Payment` object follows a strict state machine: Pending → Authorized → Captured → Settled → (or Failed/Refunded at any point).

**Example:**
```java
class PaymentService {
    PaymentResult process(PaymentRequest req) {
        Payment payment = Payment.create(req);
        try {
            payment.authorize(gateway);
            payment.capture(gateway);
            walletService.transfer(payment);
            payment.complete();
            return PaymentResult.success(payment);
        } catch (Exception e) {
            payment.fail(e);
            compensate(payment);
            return PaymentResult.failure(e);
        }
    }
}
```

## Q22: Design a `Email System` with folders and filtering.

**A:** An EmailSystem manages mailboxes, emails, folders, and rules. Core entities: `Mailbox` (user, folders, emails), `Email` (from, to, subject, body, timestamp, read status, labels), `Folder` (name, filter rules), and `EmailService` (sends, receives, organizes). The `RuleEngine` applies user-defined rules to incoming emails (e.g., "from:boss → move to Priority").

The Folder pattern uses Composite: folders can contain emails and subfolders. A special "All Mail" virtual folder shows everything; "Trash" and "Spam" are system folders. Emails can exist in multiple folders simultaneously (labeled, not moved) — this is a many-to-many relationship. The `Rule` class defines conditions (sender, subject pattern, date range) and actions (move, label, mark read, delete).

The system must handle high throughput: incoming emails are processed by a pipeline (receive → spam filter → virus scan → rule engine → deliver to mailbox). The Observer pattern notifies clients of new mail. The `EmailService` supports IMAP-like operations: sync, fetch headers, fetch body, search. Concurrency is handled at the mailbox level — multiple operations on the same mailbox must be serialized.

**Example:**
```python
class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def apply(self, email):
        if self.condition.matches(email):
            self.action.execute(email)

class InboxRule:
    def __init__(self):
        self.rules = []

    def process(self, email):
        for rule in self.rules:
            rule.apply(email)
```

## Q23: Design a `Notification System` supporting multiple channels.

**A:** A NotificationSystem sends notifications via email, SMS, push, and in-app channels. Core entities: `Notification` (title, body, priority, channels, recipient), `Channel` (interface for send — email, SMS, push, in-app), `Template` (parameterized message format), and `NotificationService` (orchestrates delivery). The Strategy pattern is fundamental: each channel is a strategy.

The `NotificationService` accepts a notification request, selects channels based on user preferences and notification priority, and dispatches to each channel. For high-priority notifications (security alerts), use all channels. For low-priority (marketing), use only the user's preferred channel. Each channel handles its own retry logic, rate limiting, and delivery confirmation.

Design considerations include: template rendering (use Handlebars/Mustache templates with variable substitution), batching (group multiple notifications to the same user into a digest), deduplication (prevent sending the same notification twice), and delivery tracking (mark as delivered, read, clicked). The Observer pattern notifies analytics when notifications are sent, delivered, and interacted with.

**Example:**
```java
interface NotificationChannel {
    void send(Notification notification);
}

class EmailChannel implements NotificationChannel {
    public void send(Notification n) {
        // SMTP/API call
    }
}

class PushChannel implements NotificationChannel {
    public void send(Notification n) {
        // FCM/APNs call
    }
}
```

## Q24: Design a `Inventory Management` system for a warehouse.

**A:** An InventorySystem tracks products, stock levels, orders, and warehouse operations. Core entities: `Product` (SKU, name, category, weight), `InventoryItem` (product, quantity, location, batch), `Warehouse` (zones, shelves), `StockMovement` (inbound/outbound, quantity, timestamp), and `InventoryService` (manages stock operations).

The core operations are: `receiveStock(product, qty, location)` (inbound), `pickStock(product, qty)` (outbound for orders), `transferStock(product, from, to)` (internal moves), and `cycleCount(location)` (audit). Stock movements are immutable event records — every change creates a `StockMovement` entry. This provides a complete audit trail and enables stock reconciliation.

Concurrency is critical: multiple pickers might try to pick the last unit simultaneously. Use optimistic locking (version numbers on inventory items) or pessimistic locking (lock the item row during pick). The `InventoryService` supports ABC analysis (categorize items by value), reorder point calculation (auto-reorder when stock hits minimum), and batch/lot tracking for perishable goods.

**Example:**
```python
class InventoryItem:
    def __init__(self, product, location, quantity=0):
        self.product = product
        self.location = location
        self.quantity = quantity
        self.version = 0

    def pick(self, qty):
        if self.quantity < qty:
            raise InsufficientStockException()
        self.quantity -= qty
        self.version += 1
        return StockMovement(self.product, self.location, -qty)
```

## Q25: Design a `Calendar` system like Google Calendar.

**A:** A CalendarSystem manages users, events, reminders, and scheduling. Core entities: `Calendar` (owner, events), `Event` (title, description, start/end time, location, attendees, recurrence), `Reminder` (time before event, notification method), and `CalendarService` (manages CRUD and conflict detection). The critical operation is conflict detection: when creating or moving an event, check if the time slot overlaps with existing events.

Recurrence rules follow the iCalendar RFC 5545 standard: `RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR` means every Monday, Wednesday, Friday. The `RecurrenceRule` class parses and generates recurrence patterns, expanding a single event definition into concrete occurrences for a date range.

The system must handle time zones correctly — every event stores its time zone, and display converts to the user's local time. Shared calendars allow others to view or edit events. The `AvailabilityService` answers queries like "When am I free next week?" by computing the complement of busy intervals across all calendars. The Observer pattern notifies attendees of event creation, updates, and cancellations.

**Example:**
```java
class Event {
    private String id;
    private String title;
    private ZonedDateTime start;
    private ZonedDateTime end;
    private List<String> attendeeIds;
    private RecurrenceRule recurrence;

    boolean conflictsWith(Event other) {
        return this.start.isBefore(other.end) && this.end.isAfter(other.start);
    }
}
```

## Q26: Design a `News Aggregation` system with categorization.

**A:** A NewsAggregation system collects articles from multiple sources, categorizes them, and presents a personalized feed. Core entities: `Article` (title, content, source, publishedAt, category, tags), `Source` (name, RSS/API endpoint, credibility score), `Category` (politics, tech, sports, etc.), and `FeedService` (aggregates and ranks articles). The system ingests articles from RSS feeds, news APIs, and web scrapers.

The ingestion pipeline: fetch source → parse content → deduplicate (compare titles/content hashes) → classify (ML model assigns categories) → store → index. Deduplication is critical — the same story appears on multiple sources. Use MinHash or SimHash for near-duplicate detection. The `Classifier` uses a trained model (Naive Bayes, BERT) to assign categories and extract entities.

Personalization uses collaborative filtering: "users who liked articles X also liked article Y." The `RecommendationEngine` maintains user preference profiles based on reading history and builds a personalized ranking. The Observer pattern pushes new articles to subscribed users in real-time. The `TrendingService` identifies articles with high engagement velocity (rapid like/share growth).

**Example:**
```python
class ArticleClassifier:
    def __init__(self, model):
        self.model = model

    def classify(self, article):
        text = f"{article.title} {article.content}"
        prediction = self.model.predict([text])
        return Category(prediction)
```

## Q27: Design a `File Upload` service with processing pipeline.

**A:** A FileUploadService handles file uploads, storage, virus scanning, thumbnail generation, and CDN distribution. Core entities: `UploadedFile` (id, originalName, mimeType, size, storagePath, status), `UploadPolicy` (max size, allowed types, quota), and `ProcessingPipeline` (chain of post-upload processors). The system must handle large files (multipart upload), concurrent uploads, and resumable uploads.

The upload flow: validate policy (size, type, user quota) → generate presigned URL (for direct S3 upload) → client uploads directly to storage → trigger processing pipeline. The pipeline uses the Chain of Responsibility: VirusScanner → ThumbnailGenerator → MetadataExtractor → CDNInvalidator. Each processor runs asynchronously (using a message queue) so the upload response returns immediately.

Design considerations include: chunked upload for large files (split into 5MB chunks, upload in parallel, reassemble), resumable uploads (track uploaded chunks, allow resume from last successful chunk), virus scanning (ClamAV integration, reject infected files), and metadata extraction (EXIF for images, duration for videos, text extraction for PDFs). The `FileService` maintains a status machine: Uploaded → Processing → Ready → (or Failed).

**Example:**
```java
interface ProcessingStep {
    void process(UploadedFile file);
}

class VirusScanStep implements ProcessingStep {
    public void process(UploadedFile file) {
        if (clamav.scan(file.getStoragePath()).isInfected()) {
            file.setStatus(FileStatus.REJECTED);
            throw new VirusDetectedException();
        }
    }
}
```

## Q28: Design a `Blog Platform` like Medium/WordPress.

**A:** A BlogPlatform manages authors, posts, comments, tags, and publishing. Core entities: `Author` (profile, followers), `Post` (title, content, author, publishedAt, tags, claps/responses), `Comment` (post, author, content, parent for threading), `Tag` (name, post count), and `BlogService` (manages CRUD and publishing). The content is stored as rich text (Markdown or HTML with embedded media).

The publishing workflow: Draft → Review → Published → (optionally Archived). The `Post` object tracks revisions — each save creates a new revision, enabling version history and rollback. The `DraftService` auto-saves drafts periodically (every 30 seconds) to prevent data loss. The `PublishService` handles SEO optimization (meta tags, canonical URLs) and social media sharing.

The feed algorithm ranks posts by: recency, engagement (claps, responses, read time), author authority (follower count, past engagement), and tag relevance. The `FeedService` uses a scoring function combining these signals. The Observer pattern notifies followers when a new post is published. The `Comment` class supports threading (parent-child relationships) and moderation (flag, hide, delete).

**Example:**
```python
class Post:
    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content
        self.status = PostStatus.DRAFT
        self.revisions = [PostRevision(title, content, datetime.now())]

    def publish(self):
        if not self.title or not self.content:
            raise ValueError("Title and content required")
        self.status = PostStatus.PUBLISHED
        self.published_at = datetime.now()
```

## Q29: Design a `Food Delivery` system like DoorDash/UberEats.

**A:** A FoodDelivery system manages restaurants, menus, orders, delivery drivers, and real-time tracking. Core entities: `Restaurant` (name, location, menu, rating, open hours), `MenuItem` (name, price, description, category), `Order` (customer, restaurant, items, status, delivery address), `DeliveryDriver` (location, status, current order), and `DeliveryService` (orchestrates the workflow).

The order lifecycle: Browse → Add to Cart → Place Order → Restaurant Accepts → Restaurant Prepares → Driver Picks Up → In Transit → Delivered. Each transition notifies the customer and restaurant. The `OrderService` handles payment processing before sending to the restaurant. The `MatchingService` assigns available drivers based on proximity, direction (toward the restaurant), and current load.

Real-time tracking uses WebSocket connections: the driver's app sends location updates every few seconds, which are broadcast to the customer's app. The `LocationService` maintains a spatial index of driver locations for fast nearest-driver queries. ETA calculation combines real-time traffic data with historical patterns. The `PricingService` calculates delivery fees based on distance, demand, and driver availability (dynamic pricing).

**Example:**
```python
class DeliveryMatcher:
    def find_driver(self, restaurant_location, radius=3.0):
        nearby = self.location_index.nearby(restaurant_location, radius)
        available = [d for d in nearby if d.status == DriverStatus.AVAILABLE]
        if not available:
            raise NoDriverAvailableException()
        return min(available, key=lambda d: d.distance_to(restaurant_location))
```

## Q30: Design a `Survey/Quiz` platform like Google Forms.

**A:** A SurveyPlatform manages surveys, questions, responses, and analytics. Core entities: `Survey` (title, description, questions, settings), `Question` (text, type: multiple-choice, text, rating, checkbox), `Response` (survey, answers, respondent, timestamp), and `SurveyAnalytics` (aggregates results). The `QuestionType` is an abstract class with concrete implementations for each question type.

The key design challenge is the polymorphic question handling. Each question type validates answers differently: multiple-choice validates against allowed options, rating validates numeric range, text validates max length. The `Question` interface defines `validate(answer)` and `display()` methods. The `SurveyRenderer` generates the form dynamically based on question types.

The `ResponseService` collects answers, validates each against its question's rules, and stores responses. Analytics aggregate results: pie charts for multiple-choice, histograms for ratings, word clouds for text responses. The `SurveyAccessService` manages permissions (public, private, link-only, email-invite) and prevents duplicate responses. The Observer pattern notifies the survey creator when new responses arrive.

**Example:**
```java
interface Question {
    boolean validate(Object answer);
    String display();
}

class MultipleChoiceQuestion implements Question {
    private String text;
    private List<String> options;

    public boolean validate(Object answer) {
        return options.contains(answer);
    }
}

class RatingQuestion implements Question {
    private int min = 1, max = 5;
    public boolean validate(Object answer) {
        int val = (int) answer;
        return val >= min && val <= max;
    }
}
```

## Q31: Design a `Real-time Collaborative Editor` like Google Docs.

**A:** A CollaborativeEditor allows multiple users to edit the same document simultaneously, with changes reflected in real-time. Core entities: `Document` (content, version), `EditOperation` (type: insert/delete, position, character), `Collaborator` (user, cursor position, selection), and `SyncService` (manages conflict resolution). The critical challenge is concurrent edit resolution — two users editing the same position simultaneously must not corrupt the document.

The two primary approaches are Operational Transformation (OT) and Conflict-free Replicated Data Types (CRDTs). OT transforms operations against concurrent operations to maintain consistency — if user A inserts "X" at position 5 and user B inserts "Y" at position 5 simultaneously, OT ensures both insertions are applied correctly (e.g., A's insertion happens first, B's insertion is transformed to position 6). CRDTs use data structures that are mathematically guaranteed to converge regardless of operation order.

The system uses WebSocket for real-time communication: each client sends operations to the server, which broadcasts transformed operations to all other clients. The `SyncService` maintains a version vector for causal ordering. The `Document` supports undo/redo per user (each user's undo only affects their own operations). Cursor positions are broadcast so collaborators can see each other's cursors (like Google Docs' colored cursors).

**Example:**
```python
class EditOperation:
    def __init__(self, op_type, position, char, user_id):
        self.op_type = op_type  # 'insert' or 'delete'
        self.position = position
        self.char = char
        self.user_id = user_id
        self.version = 0

    def transform(self, other):
        if self.position >= other.position:
            if other.op_type == 'insert':
                self.position += 1
            elif other.op_type == 'delete':
                self.position -= 1
```

## Q32: Design a `Web Crawler` system.

**A:** A WebCrawler system discovers and downloads web pages, extracts links, and builds a web graph. Core entities: `Crawler` (manages crawl queue), `Page` (URL, content, links, timestamp), `CrawlPolicy` (robots.txt, rate limiting, scope), and `UrlParser` (extracts links from HTML). The system must handle billions of URLs efficiently while respecting website policies.

The architecture uses a distributed crawl queue: URLs are added to a priority queue (by domain authority, freshness, or importance). Worker threads fetch URLs, extract links, filter new URLs, and enqueue them. The `URLFrontier` manages politeness — one request per domain at a time, respecting crawl-delay from robots.txt. Use a per-domain queue with a scheduler that respects the robots.txt crawl-delay directive.

Design considerations include: deduplication (use a Bloom filter for URL seen-check with 1% false positive rate — much more memory-efficient than a hash set), content fingerprinting (detect duplicate content at different URLs using SimHash), politeness (respect robots.txt, rate-limit per domain), and distributed coordination (partition URLs by domain across crawler nodes). The `ContentParser` extracts text, metadata, and links. The `StorageService` saves raw HTML and parsed content.

**Example:**
```python
class WebCrawler:
    def __init__(self):
        self.frontier = URLFrontier()
        self.seen = BloomFilter(capacity=1_000_000_000, error_rate=0.01)
        self.robots_parser = RobotsParser()

    def crawl(self, seed_urls):
        for url in seed_urls:
            self.frontier.enqueue(url)

        while not self.frontier.empty():
            url = self.frontier.dequeue()
            if self.seen.contains(url):
                continue
            if not self.robots_parser.is_allowed(url):
                continue
            page = self.fetch(url)
            self.seen.add(url)
            for link in page.extract_links():
                if not self.seen.contains(link):
                    self.frontier.enqueue(link)
```

## Q33: Design a `Rate Limiter` that can be used across services.

**A:** A RateLimiter controls how many requests a client can make within a time window, preventing abuse and ensuring fair resource allocation. Core entities: `RateLimitRule` (window size, max requests, key strategy), `RateLimiter` (checks and enforces limits), and `Client` (identified by IP, API key, or user ID). The limiter must be distributed — working correctly across multiple server instances.

The four main algorithms are: Fixed Window (simple counter per time window — suffers from burst at window boundaries), Sliding Window Log (timestamp-based, exact but memory-heavy), Sliding Window Counter (combines current and previous window counts — good balance), and Token Bucket (tokens added at fixed rate, each request consumes a token — allows controlled bursts). Token Bucket is the most widely used because it's simple, efficient, and allows bursts up to the bucket capacity.

The implementation uses Redis for distributed counting: `INCR key` with `EXPIRE key window_size` for atomic increment-and-set-TTL. The `RateLimitMiddleware` intercepts requests, extracts the client key (API key or IP), checks the limit, and either passes the request through or returns HTTP 429 (Too Many Requests) with a `Retry-After` header. The `RateLimitRule` supports different limits per endpoint, per user tier (free vs. paid), and per time granularity (per second, minute, hour).

**Example:**
```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def allow(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

## Q34: Design a `Distributed Cache` system.

**A:** A DistributedCache stores key-value pairs across multiple nodes for fast access. Core entities: `CacheNode` (stores a subset of keys), `CacheManager` (manages node membership), `CacheClient` (client interface), and `ConsistentHashRing` (determines which node owns a key). The cache must handle node failures, cache eviction, and replication.

The consistent hash ring maps keys to nodes: each node occupies a position on a ring (0 to 2^32), and a key hashes to a position and is assigned to the next node clockwise. This minimizes key redistribution when nodes are added or removed (only adjacent keys move). Virtual nodes (multiple positions per physical node) ensure even distribution.

Design considerations include: eviction policies (LRU, LFU, TTL-based — use a `CacheEntry` with access timestamps), replication (write to N nodes for fault tolerance), consistency (eventual consistency is acceptable for caches — stale data is acceptable), and cache warming (pre-populate cache on startup or deployment). The `CacheClient` implements a local cache + distributed cache hierarchy: check local cache first (fast), then distributed cache, then database (slowest).

**Example:**
```python
import hashlib

class ConsistentHashRing:
    def __init__(self, nodes, virtual_nodes=150):
        self.ring = {}
        self.sorted_keys = []
        for node in nodes:
            for i in range(virtual_nodes):
                key = self._hash(f"{node}:{i}")
                self.ring[key] = node
                self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def get_node(self, key):
        h = self._hash(key)
        for ring_key in self.sorted_keys:
            if h <= ring_key:
                return self.ring[ring_key]
        return self.ring[self.sorted_keys[0]]
```

## Q35: Design a `Task Scheduler` like Cron or Airflow.

**A:** A TaskScheduler manages recurring and one-time tasks, executing them at specified times. Core entities: `Task` (name, schedule, handler, retry policy), `JobExecution` (task, start time, end time, status, output), `Scheduler` (determines which tasks to run), and `WorkerPool` (executes tasks). The scheduler must handle distributed execution, retries, and dependencies.

The scheduler uses a priority queue sorted by next execution time. Every tick, it checks the queue for due tasks and dispatches them to available workers. For distributed scheduling, use a database-backed approach: each task row has a `next_run_at` column. Workers compete to claim tasks using `SELECT ... FOR UPDATE` or optimistic locking with version numbers (only one worker succeeds).

Task dependencies are modeled as a DAG (Directed Acyclic Graph). A task can only run after all its dependencies complete. The `DagScheduler` topologically sorts the DAG and executes tasks in order, skipping tasks whose dependencies failed. Retry policies use exponential backoff. The `DeadLetterQueue` stores tasks that exhausted all retries. The Observer pattern notifies on task completion, failure, and SLA violations.

**Example:**
```python
from datetime import datetime, timedelta

class Task:
    def __init__(self, name, schedule, handler):
        self.name = name
        self.schedule = schedule  # cron expression
        self.handler = handler
        self.next_run = None

    def should_run(self, now):
        return self.next_run is not None and self.next_run <= now

class Scheduler:
    def __init__(self):
        self.tasks = []

    def tick(self):
        now = datetime.now()
        for task in self.tasks:
            if task.should_run(now):
                self.execute(task)
                task.next_run = self._next_run(task.schedule)
```

## Q36: Design a `Content Delivery Network` (CDN) cache system.

**A:** A CDN caches static and dynamic content at edge locations worldwide to reduce latency. Core entities: `EdgeNode` (geographic location, cached content), `Origin` (original content source), `CachePolicy` (TTL, invalidation rules), and `CDNService` (routes requests to optimal edge). The CDN must minimize cache misses and handle content invalidation efficiently.

The request flow: user requests a URL → DNS resolves to nearest edge node → edge node checks its cache → if hit, returns cached content; if miss, fetches from origin (or a parent edge), caches it, and returns. The `CacheKey` is typically the URL + relevant headers (Accept-Encoding, Vary headers). Cache invalidation is the hardest problem — use TTL-based expiry for most content, and explicit purge API for urgent invalidation.

Design considerations include: cache hierarchy (edge → regional → origin), content hashing (append content hash to URL for cache-busting on update), range requests (partial content for large files), and HTTPS (TLS termination at edge). The `OriginShield` reduces origin load by having a mid-tier cache between edges and origin. Cache warming pre-populates edges with popular content during deployment.

**Example:**
```python
class EdgeNode:
    def __init__(self, location):
        self.location = location
        self.cache = {}
        self.parent = None  # parent edge or origin

    def get(self, url):
        if url in self.cache:
            entry = self.cache[url]
            if not entry.is_expired():
                return entry.content
        content = self.parent.get(url) if self.parent else self.fetch_origin(url)
        self.cache[url] = CacheEntry(content, ttl=3600)
        return content
```

## Q37: Design a `Metrics and Monitoring` system like Prometheus/Datadog.

**A:** A MetricsSystem collects, stores, and visualizes time-series data from applications and infrastructure. Core entities: `Metric` (name, labels, type: counter/gauge/histogram/summary), `TimeSeries` (metric + label values + data points), `Collector` (pulls or receives metrics), and `QueryEngine` (aggregation, filtering, alerting). The system must handle millions of data points per second.

The data model follows Prometheus conventions: metrics have a name and label set (key-value pairs). A counter `http_requests_total{method="GET", status="200"}` is a monotonically increasing number. A gauge `cpu_usage_percent` can go up and down. A histogram `request_duration_seconds` tracks value distributions. Each unique label combination is a separate time series.

The architecture uses a pull model (agent scrapes metrics from endpoints) or push model (agents send metrics to a collector). Storage uses a time-series database (InfluxDB, Prometheus TSDB, or TimescaleDB) optimized for append-only writes and range queries. The `AlertManager` evaluates rules against metrics and fires alerts (email, Slack, PagerDuty). The `QueryEngine` supports PromQL-like queries: `rate(http_requests_total[5m])` computes requests per second over 5-minute windows.

**Example:**
```python
import time

class MetricsCollector:
    def __init__(self):
        self.counters = {}
        self.gauges = {}

    def increment(self, name, labels=None, value=1):
        key = (name, tuple(sorted(labels.items())) if labels else ())
        self.counters[key] = self.counters.get(key, 0) + value

    def gauge_set(self, name, value, labels=None):
        key = (name, tuple(sorted(labels.items())) if labels else ())
        self.gauges[key] = value
```

## Q38: Design a `Feature Flag` system for gradual rollouts.

**A:** A FeatureFlagSystem allows developers to enable/disable features without deploying code. Core entities: `FeatureFlag` (name, enabled, targeting rules, variants), `TargetingRule` (conditions: user attributes, percentage, segments), `Variant` (for A/B tests: control, treatment), and `FlagService` (evaluates flags for users). Flags support gradual rollouts, A/B testing, and kill switches.

The flag evaluation flow: check flag → evaluate targeting rules (percentage rollout, user segments, attribute matching) → return variant. The `TargetingRule` supports operators (equals, contains, in, greater than) on user attributes (country, plan, signup_date). A percentage rollout randomly assigns users to variants based on a hash of their user ID (deterministic — same user always gets the same variant).

Design considerations include: real-time updates (use a polling or streaming mechanism so flag changes propagate instantly), audit logging (track who changed which flag when), SDK integration (client-side and server-side SDKs for evaluating flags), and fallback values (if the flag service is unavailable, use a sensible default). The `FlagService` uses a local cache with short TTL to avoid network calls on every evaluation.

**Example:**
```python
import hashlib

class FeatureFlag:
    def __init__(self, name, enabled=False, percentage=0):
        self.name = name
        self.enabled = enabled
        self.percentage = percentage

    def is_enabled(self, user_id):
        if not self.enabled:
            return False
        hash_val = int(hashlib.md5(f"{self.name}:{user_id}".encode()).hexdigest(), 16)
        return (hash_val % 100) < self.percentage
```

## Q39: Design a `Config Management` system for microservices.

**A:** A ConfigManagement system centralizes configuration for distributed microservices. Core entities: `ConfigKey` (service, environment, key), `ConfigValue` (value, version, encrypted), `ConfigChange` (key, old value, new value, who changed, when), and `ConfigService` (stores, distributes, and caches config). The system must support dynamic config changes without service restarts.

The architecture: a central Config Store (database or distributed KV like ZooKeeper/etcd) holds all configuration. A Config Server provides a REST API for CRUD operations. Services subscribe to config changes via long-polling or WebSocket. When a config changes, the Config Server pushes the update to subscribed services, which update their local cache.

Design considerations include: encryption for secrets (AES-256 encryption at rest, decryption only by authorized services), versioning (each change creates a new version, enabling rollback), audit trail (log all changes with who/what/when), environment isolation (dev/staging/prod have separate config namespaces), and feature-specific config (each feature flag can have its own config). The `ConfigClient` in each service maintains a local cache and refreshes on changes, ensuring zero-downtime config updates.

**Example:**
```python
class ConfigClient:
    def __init__(self, service_name, environment):
        self.service = service_name
        self.env = environment
        self.cache = {}

    def get(self, key, default=None):
        if key in self.cache:
            return self.cache[key]
        value = self.fetch_from_server(key)
        self.cache[key] = value
        return value or default

    def on_config_change(self, key, new_value):
        self.cache[key] = new_value
        self.apply(key, new_value)
```

## Q40: Design a `Logging` infrastructure for distributed systems.

**A:** A DistributedLogging system collects, aggregates, and queries logs from multiple services. Core entities: `LogEntry` (timestamp, level, service, message, traceId, metadata), `LogCollector` (receives logs from services), `LogStorage` (time-series store), and `LogQuery` (search, filter, aggregate). The system must handle high throughput (millions of entries per second) and provide fast search.

The architecture uses a push model: services emit structured JSON logs to a local agent (Fluentd/FluentBit), which forwards to a log aggregator (Kafka), which writes to a storage backend (Elasticsearch, Loki, or CloudWatch). Structured logging is critical — each log entry is a JSON object with consistent fields, enabling efficient indexing and querying.

Distributed tracing integrates with logging: each request gets a `traceId` that appears in all log entries across services, enabling end-to-end request tracing. The `LogEntry` includes: timestamp, level (INFO/WARN/ERROR), service name, trace ID, span ID, and arbitrary metadata. The `LogQuery` interface supports time-range queries, level filtering, service filtering, full-text search, and aggregation (error rate per service). Alerting rules fire when error rates exceed thresholds.

**Example:**
```python
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, service_name):
        self.service = service_name
        self.trace_id = None

    def log(self, level, message, **kwargs):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "service": self.service,
            "message": message,
            "trace_id": self.trace_id,
            **kwargs
        }
        self.transport.send(json.dumps(entry))
```

## Q41: Design a `Service Discovery` system for microservices.

**A:** A ServiceDiscovery system allows microservices to find and communicate with each other dynamically. Core entities: `ServiceInstance` (name, host, port, health, metadata), `ServiceRegistry` (stores instance information), and `DiscoveryClient` (queries the registry). Services register on startup and deregister on shutdown. Clients query the registry to find available instances.

Two main approaches: client-side discovery (client queries the registry and load-balances) and server-side discovery (a load balancer/proxy queries the registry and routes traffic). Client-side (Netflix Eureka, Consul) gives clients more control. Server-side (Kubernetes Services, AWS ALB) is simpler for clients.

Health checking is critical: the registry must detect failed instances and remove them. Approaches include heartbeat (instances send periodic pings), active checking (registry probes instances), and passive checking (clients report failures). The registry uses eventual consistency — a few seconds of stale data is acceptable and preferable to the complexity of strong consistency. The `DiscoveryClient` caches registry data locally and refreshes periodically.

**Example:**
```python
class ServiceRegistry:
    def __init__(self):
        self.instances = {}  # service_name -> list of instances

    def register(self, instance):
        name = instance.service_name
        if name not in self.instances:
            self.instances[name] = []
        self.instances[name].append(instance)

    def deregister(self, instance):
        self.instances[instance.service_name].remove(instance)

    def discover(self, service_name):
        return [i for i in self.instances.get(service_name, [])
                if i.is_healthy()]
```

## Q42: Design an `Event Sourcing` system for audit trails.

**A:** EventSourcing stores all changes as a sequence of immutable events rather than overwriting current state. Core entities: `Event` (type, payload, timestamp, aggregateId, version), `Aggregate` (reconstructed from events), `EventStore` (append-only log of events), and `EventBus` (publishes events to subscribers). The current state is derived by replaying events from the beginning (or from a snapshot).

The event store is the source of truth. To get the current state of an Order aggregate, replay all Order events: OrderCreated → ItemAdded → ItemRemoved → PaymentReceived → Shipped. Each event is immutable and ordered. Snapshots (periodic state captures) optimize replay — instead of replaying 10,000 events, replay from the most recent snapshot plus the 50 events since.

Design considerations include: event schema evolution (version events, use upcasters to handle old versions), projection (build read models from events — e.g., a `OrderSummary` projection aggregates events into a queryable table), eventual consistency (projections update asynchronously), and idempotency (events must be processed idempotently since delivery may be at-least-once). The Event Bus (Kafka, RabbitMQ) distributes events to consumers.

**Example:**
```python
class OrderAggregate:
    def __init__(self):
        self.id = None
        self.items = []
        self.status = None
        self.version = 0

    def apply(self, event):
        if event.type == "OrderCreated":
            self.id = event.payload["order_id"]
            self.status = "created"
        elif event.type == "ItemAdded":
            self.items.append(event.payload["item"])
        self.version += 1

    @classmethod
    def from_events(cls, events):
        agg = cls()
        for event in events:
            agg.apply(event)
        return agg
```

## Q43: Design a `Message Queue` system like Kafka/RabbitMQ.

**A:** A MessageQueue system provides asynchronous communication between services. Core entities: `Topic/Queue` (named channel for messages), `Message` (payload, key, headers, timestamp), `Producer` (sends messages), `Consumer` (receives messages), and `Broker` (stores and delivers messages). The system must guarantee ordering (per partition), durability, and at-least-once delivery.

Kafka-style architecture: topics are split into partitions (for parallelism), each partition is an append-only log. Consumers in a group each consume different partitions (load balancing). Offsets track how far each consumer group has progressed. Partitioning by message key ensures all messages with the same key go to the same partition (preserving ordering per key).

RabbitMQ-style architecture: queues with routing exchanges (direct, topic, fanout). Messages are pushed to consumers or pulled. Acknowledgments ensure reliable delivery — messages are only removed after consumer acknowledgment. Dead letter queues capture failed messages.

Design considerations include: message retention (Kafka retains messages for a configured time regardless of consumption), backpressure (slow consumers shouldn't block fast producers), exactly-once semantics (idempotent producers + transactional consumers), and consumer groups (parallel processing with partition assignment). The `Broker` handles replication (multiple replicas per partition for fault tolerance) and leader election.

**Example:**
```python
class Topic:
    def __init__(self, name, partitions=3):
        self.name = name
        self.partitions = [Partition(i) for i in range(partitions)]

    def produce(self, key, value):
        partition = hash(key) % len(self.partitions)
        self.partitions[partition].append(Message(key, value))

    def consume(self, group, partition=None):
        p = self.partitions[partition or 0]
        return p.read_offset(group)
```

## Q44: Design a `Search Engine` with indexing and ranking.

**A:** A SearchEngine indexes documents and returns ranked results for queries. Core entities: `Document` (id, title, content, metadata), `Index` (inverted index: term → document IDs), `Query` (parsed search terms, operators), `SearchResult` (document, score, snippets), and `Ranker` (scores results by relevance). The inverted index is the core data structure.

The indexing pipeline: tokenize document → normalize (lowercase, stem, remove stopwords) → build inverted index (term → list of document IDs with positions and frequencies) → compute TF-IDF scores. The inverted index maps each unique term to a posting list (sorted list of document IDs with term frequency and position data).

Query processing: parse query into terms → look up each term in the inverted index → intersect posting lists (AND) or union (OR) → compute relevance scores → rank and return top K. The BM25 scoring function (used by Elasticsearch) considers term frequency, inverse document frequency, and document length. The `SnippetGenerator` extracts the most relevant passage from the document for display.

**Example:**
```python
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)  # term -> [(doc_id, tf)]

    def add_document(self, doc_id, tokens):
        tf = defaultdict(int)
        for token in tokens:
            tf[token] += 1
        for term, count in tf.items():
            self.index[term].append((doc_id, count))

    def search(self, query_terms):
        results = set()
        for term in query_terms:
            if term in self.index:
                results.update(doc_id for doc_id, _ in self.index[term])
        return results
```

## Q45: Design a `Load Balancer` with health checking.

**A:** A LoadBalancer distributes incoming requests across multiple backend servers. Core entities: `BackendServer` (host, port, weight, health status), `LoadBalancer` (algorithm, server list, health checker), and `HealthCheck` (probes servers periodically). The load balancer must handle server failures gracefully and distribute load evenly.

The four main algorithms are: Round Robin (cycle through servers — simple, even distribution), Weighted Round Robin (servers with higher weight get more requests), Least Connections (route to server with fewest active connections — good for long-lived connections), and Consistent Hash (same client always hits same server — good for caching). IP hash is a variant that uses client IP for consistent routing.

Health checking uses active probes: the load balancer sends periodic HTTP requests (e.g., `GET /health`) to each backend. If a server fails N consecutive checks, it's marked unhealthy and removed from the rotation. Once it passes M consecutive checks, it's re-added. The `LoadBalancer` maintains a thread-safe server list and uses lock-free data structures for high throughput. The health check interval and failure thresholds are configurable.

**Example:**
```python
import itertools

class RoundRobinBalancer:
    def __init__(self, servers):
        self.servers = [s for s in servers if s.is_healthy]
        self.iterator = itertools.cycle(self.servers)

    def next_server(self):
        server = next(self.iterator)
        while not server.is_healthy:
            server = next(self.iterator)
        return server

class LeastConnectionsBalancer:
    def next_server(self):
        return min(self.servers, key=lambda s: s.active_connections)
```

## Q46: Design a `Session Management` system for web applications.

**A:** A SessionManagement system maintains user state across HTTP requests. Core entities: `Session` (id, userId, attributes, createdAt, lastAccessed, maxInactiveInterval), `SessionStore` (persists sessions), and `SessionManager` (creates, retrieves, invalidates sessions). Sessions must be scalable across multiple application servers.

The session flow: user logs in → server creates session → session ID sent as cookie → subsequent requests include cookie → server looks up session → application accesses session data. The session ID must be cryptographically random (128+ bits) to prevent guessing. Sessions expire after inactivity (typically 30 minutes).

For distributed systems, use a shared session store: Redis (fast, in-memory, TTL support) is the most common choice. The `SessionStore` interface has `create()`, `get()`, `update()`, `delete()` methods, with Redis implementing them. Sticky sessions (routing same user to same server) are an alternative but less scalable. The `SessionManager` handles session fixation attacks (regenerate ID on login), concurrent session limits (max N sessions per user), and session invalidation on password change.

**Example:**
```python
import uuid
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, store, timeout_minutes=30):
        self.store = store
        self.timeout = timedelta(minutes=timeout_minutes)

    def create(self, user_id):
        session_id = str(uuid.uuid4())
        session = Session(session_id, user_id, self.timeout)
        self.store.save(session)
        return session_id

    def get(self, session_id):
        session = self.store.get(session_id)
        if session and not session.is_expired():
            session.touch()
            self.store.save(session)
            return session
        return None
```

## Q47: Design a `File Storage` system like Google Drive/Dropbox.

**A:** A FileStorage system manages file uploads, downloads, versioning, sharing, and synchronization. Core entities: `File` (id, name, mimeType, size, owner, versions), `FileVersion` (content hash, storage path, timestamp, size), `Folder` (id, name, parent, children), `Share` (file, user, permission: view/edit), and `SyncService` (detects changes and syncs).

The storage architecture separates metadata (file names, permissions, versions) from content (actual file bytes). Metadata goes in a relational database (PostgreSQL). Content goes in object storage (S3, GCS) organized by content hash — identical files are stored once (deduplication). A `FileVersion` references a content hash, enabling efficient versioning without duplicating unchanged files.

File sync uses a polling or WebSocket-based approach: the client reports its latest version for each file, the server compares with its version, and returns a diff (new files, updated files, deleted files). The `FileVersionManager` handles conflict resolution: if two users edit the same file offline, both versions are kept and the user must choose. The `ShareService` manages permissions with inheritance (folder permissions apply to children).

**Example:**
```python
class FileVersionManager:
    def upload(self, file_id, content):
        content_hash = sha256(content)
        storage_path = self.store_content(content_hash, content)
        version = FileVersion(
            file_id=file_id,
            content_hash=content_hash,
            storage_path=storage_path,
            timestamp=datetime.now()
        )
        self.db.add_version(version)
        return version
```

## Q48: Design an `Authentication and Authorization` system (OAuth2/OIDC).

**A:** An AuthSystem handles user authentication (who are you?) and authorization (what can you do?). Core entities: `User` (credentials, profile), `Role` (name, permissions), `Permission` (resource, action), `Token` (type: access/refresh, claims, expiry), and `AuthServer` (validates credentials, issues tokens). The system implements OAuth2 flows and OpenID Connect.

The OAuth2 Authorization Code flow: client redirects to auth server → user authenticates → auth server issues authorization code → client exchanges code for tokens → client uses access token for API calls. The access token (JWT) contains claims (user ID, roles, permissions, expiry) and is self-contained — APIs validate it without calling the auth server.

Design considerations include: token refresh (access tokens expire in 15 minutes, refresh tokens in 7 days), token revocation (blacklist revoked tokens), PKCE (Proof Key for Code Exchange for public clients), and multi-factor authentication (TOTP, SMS, push). The `AuthorizationService` evaluates permissions: `hasPermission(user, "read", "document:123")` checks roles and fine-grained permissions. RBAC (role-based) for simple cases, ABAC (attribute-based) for complex policy needs.

**Example:**
```python
import jwt
from datetime import datetime, timedelta

class TokenService:
    def __init__(self, secret_key):
        self.secret = secret_key

    def create_access_token(self, user_id, roles):
        payload = {
            "sub": user_id,
            "roles": roles,
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_token(self, token):
        return jwt.decode(token, self.secret, algorithms=["HS256"])
```

## Q49: Design a `Payment Subscription` system like Stripe Subscriptions.

**A:** A SubscriptionSystem manages recurring billing, plan changes, and payment cycles. Core entities: `Customer` (payment methods, subscriptions), `Plan` (name, price, interval: monthly/yearly), `Subscription` (customer, plan, status, currentPeriodStart/End), `Invoice` (amount, due date, paid status), and `PaymentMethod` (card, bank — tokenized). The system must handle proration, upgrades, downgrades, and cancellations.

The subscription lifecycle: create subscription → charge immediately (or at period start) → auto-renew at period end → handle payment failures (retry with exponential backoff → retry limit → pause subscription). The `BillingService` generates invoices at each billing cycle. Proration is calculated when a customer changes plans mid-cycle: credit unused time on old plan, charge for remaining time on new plan.

Design considerations include: dunning (automated retry and notification for failed payments), trial periods (free trial that converts to paid), metered billing (charge based on usage — e.g., API calls), and tax calculation (integrate with tax APIs for different jurisdictions). The `WebhookService` notifies the application of subscription events (created, updated, payment_failed, canceled). The `SubscriptionScheduler` runs daily to check for renewals, expirations, and dunning.

**Example:**
```python
class SubscriptionService:
    def change_plan(self, subscription, new_plan):
        old_plan = subscription.plan
        proration = self.calculate_proration(subscription, new_plan)
        subscription.plan = new_plan
        invoice = Invoice(
            customer=subscription.customer,
            amount=proration,
            description=f"Plan change: {old_plan.name} → {new_plan.name}"
        )
        self.charge(invoice)
```

## Q50: Design a `Distributed Lock` system like Redis Redlock.

**A:** A DistributedLock ensures that only one process can access a shared resource at a time across multiple machines. Core entities: `Lock` (resource, owner, expiry, acquiredAt), `LockManager` (acquires and releases locks), and `LockProvider` (Redis, ZooKeeper, etcd). The lock must be safe against process crashes, network partitions, and clock drift.

The Redlock algorithm: client sends lock requests to N independent Redis instances (typically 5). If a majority (N/2+1) grant the lock within the timeout, the lock is acquired. The lock has a TTL (auto-expiry) to prevent deadlocks from crashed holders. The client must perform the acquisition in a single atomic operation (all or nothing — actually Redlock requires sequential requests with total time less than the TTL).

Design considerations include: lock renewal (extend TTL while holding the lock — use a background thread), fencing tokens (monotonically increasing tokens prevent stale lock holders from interfering), and lock fairness (waiting processes should eventually acquire the lock — use a queue-based approach). The `LockManager` interface: `tryLock(resource, ttl) → Optional<Lock>`, `unlock(lock)`, `isLocked(resource)`. The `RenewableLock` wrapper auto-renews the lock while the operation is in progress.

**Example:**
```python
import redis
import uuid

class RedisLock:
    def __init__(self, client, resource, ttl_seconds=30):
        self.client = client
        self.resource = resource
        self.ttl = ttl_seconds
        self.owner = str(uuid.uuid4())

    def acquire(self):
        return self.client.set(
            f"lock:{self.resource}",
            self.owner,
            nx=True,  # only set if not exists
            ex=self.ttl
        )

    def release(self):
        # Lua script for atomic check-and-delete
        script = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        end
        return 0
        """
        self.client.eval(script, 1, f"lock:{self.resource}", self.owner)
```

## Q51: Design a `Circuit Breaker` pattern for fault tolerance.

**A:** A CircuitBreaker prevents cascading failures by detecting when a downstream service is failing and short-circuiting calls to it. Core entities: `CircuitBreaker` (state: closed/open/half-open, failure count, success count), `FailureDetector` (tracks error rates), and `FallbackStrategy` (alternative behavior when circuit is open). The three states: Normal (closed — requests pass through), Failed (open — requests rejected immediately), Testing (half-open — one request probes if service recovered).

The closed state tracks consecutive failures. When failures exceed a threshold (e.g., 5 consecutive failures or 50% error rate in a window), the circuit opens. In the open state, all requests immediately return a fallback value (cached data, default response, or error). After a timeout (e.g., 30 seconds), the circuit moves to half-open state. In half-open, one probe request is allowed through. If it succeeds, the circuit closes; if it fails, it opens again.

Implementation uses the State pattern: `ClosedState`, `OpenState`, `HalfOpenState` each handle requests differently. The `FailureDetector` uses a sliding window to track error rates (not just consecutive failures). The `FallbackStrategy` can be: return cached data, call a degraded service, return default values, or propagate an error. Integration is via a decorator/proxy that wraps service calls with circuit breaker logic.

**Example:**
```python
import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.state = "CLOSED"
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenException()
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
```

## Q52: Design a `Retry` mechanism with exponential backoff.

**A:** A Retry mechanism automatically retries failed operations with increasing delays. Core entities: `RetryPolicy` (max retries, delay strategy, retryable exceptions), `BackoffStrategy` (fixed, linear, exponential with jitter), and `RetryExecutor` (wraps operations with retry logic). The goal is to handle transient failures (network blips, temporary overloads) without overwhelming the failing service.

Exponential backoff: delay doubles with each retry (1s, 2s, 4s, 8s, 16s). Adding jitter (random variation) prevents thundering herd — when many clients retry simultaneously, they all retry at the same time without jitter. Jitter adds random delay: `delay = base * 2^retry + random(0, base)`. This spreads retries across time.

The `RetryPolicy` defines which exceptions are retryable (network errors: yes; validation errors: no) and maximum retry count. The `CircuitBreaker` integrates with retry — if the circuit is open, don't retry (it will fail immediately). The `RetryExecutor` wraps any operation: `retryExecutor.execute(() -> service.call())`. Dead letter queues capture operations that exhausted all retries. The `RetryTelemetry` logs retry attempts for debugging and monitoring.

**Example:**
```python
import time
import random

class ExponentialBackoff:
    def __init__(self, base_delay=1, max_delay=60, max_retries=5):
        self.base = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries

    def execute(self, func):
        for attempt in range(self.max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                delay = min(self.base * (2 ** attempt), self.max_delay)
                jitter = random.uniform(0, delay * 0.1)
                time.sleep(delay + jitter)
```

## Q53: Design a `Saga` pattern for distributed transactions.

**A:** A Saga manages a sequence of local transactions across multiple services, ensuring eventual consistency without distributed locks. Each step in the saga has a compensating transaction that undoes its effect if a later step fails. Two orchestration styles: choreography (each service publishes events that trigger the next step) and orchestration (a central coordinator directs the flow).

The order saga example: CreateOrder → ReserveInventory → ProcessPayment → ShipOrder. If ShipOrder fails, the saga executes compensating transactions: RefundPayment → ReleaseInventory → CancelOrder. Each service must be idempotent — compensating transactions may be called multiple times. The `SagaOrchestrator` manages the state machine: each step transitions to the next or triggers compensation.

The choreography approach: OrderService creates order and publishes OrderCreated → InventoryService reserves stock and publishes InventoryReserved → PaymentService charges and publishes PaymentProcessed → ShippingService ships and publishes OrderShipped. If PaymentService fails, it publishes PaymentFailed → OrderService compensates (cancels order) and InventoryService compensates (releases stock). Choreography is simpler but harder to debug. Orchestration is more explicit but adds a central coordinator.

**Example:**
```python
class OrderSaga:
    def __init__(self):
        self.steps = [
            SagaStep("create_order", "cancel_order"),
            SagaStep("reserve_inventory", "release_inventory"),
            SagaStep("process_payment", "refund_payment"),
            SagaStep("ship_order", "cancel_shipment"),
        ]

    def execute(self, context):
        completed = []
        for step in self.steps:
            try:
                step.execute(context)
                completed.append(step)
            except Exception:
                for s in reversed(completed):
                    s.compensate(context)
                raise
```

## Q54: Design a `CQRS` (Command Query Responsibility Segregation) system.

**A:** CQRS separates read and write models: commands (create, update, delete) modify the write model, and queries read from a separate read model optimized for display. Core entities: `Command` (intent to change state), `Query` (request for data), `WriteModel` (normalized, normalized database), `ReadModel` (denormalized, optimized for specific queries), and `Projection` (synchronizes write model to read model).

The write model uses a normalized relational database optimized for transactions and consistency. The read model uses a denormalized store (Elasticsearch, Redis, materialized views) optimized for fast reads. Events published by the write model trigger projections that update the read model. The read model can be rebuilt from events at any time.

Design considerations include: eventual consistency (read model may lag behind write model by milliseconds to seconds), projection rebuild (replay all events to reconstruct the read model), and read model design (each query can have its own specialized read model). CQRS pairs naturally with Event Sourcing — the write model is the event store, and projections build read models from events. The separation allows independent scaling: read-heavy systems scale read replicas; write-heavy systems scale write throughput.

**Example:**
```python
class OrderCommandHandler:
    def handle_create_order(self, cmd):
        order = Order(cmd.customer_id, cmd.items)
        self.db.save(order)
        self.event_store.append(OrderCreated(order.id, cmd.customer_id, cmd.items))

class OrderQueryService:
    def get_order_summary(self, order_id):
        return self.read_db.query("SELECT * FROM order_summary WHERE id = %s", order_id)
```

## Q55: Design a `Leader Election` system for coordination.

**A:** A LeaderElection system selects one node from a cluster to coordinate shared tasks (scheduling, cleanup, configuration updates). Core entities: `Candidate` (node, term number), `Election` (term, votes), `Leader` (node, lease), and `Heartbeat` (proof of liveness). The leader must be unique and step down if it becomes unavailable.

The Bully algorithm: when a node detects no leader, it starts an election by sending election messages to all nodes with higher IDs. If no higher node responds, it becomes leader. Higher nodes respond with their own election, and the highest node wins. The Raft consensus algorithm is more robust: nodes elect a leader for a term, the leader sends heartbeats, and if heartbeats stop, followers start a new election.

Design considerations include: split-brain prevention (two nodes both think they're leader — use quorum-based election), leader lease (leader's authority expires if it doesn't renew within a timeout), and graceful leadership transfer (leader tells a specific follower to take over, avoiding election). The `LeaderLatch` (Curator) or `RedLock` (Redis) implementations provide distributed leader election. The leader performs exclusive tasks; if it fails, the new leader picks up where it left off.

**Example:**
```python
class LeaderElection:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.current_term = 0
        self.voted_for = None

    def start_election(self):
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1
        for peer in self.peers:
            if peer.request_vote(self.current_term, self.node_id):
                votes += 1
        if votes > (len(self.peers) + 1) / 2:
            self.become_leader()
```

## Q56: Design a `Consensus` system like Raft/Paxos.

**A:** A Consensus system ensures distributed nodes agree on a single value or sequence of values despite failures. Raft is the most understood consensus algorithm: nodes are in one of three states — Follower, Candidate, or Leader. The Leader handles all client requests and replicates log entries to Followers. A majority (quorum) must agree for a value to be committed.

Raft operation: Followers time out and become Candidates, starting elections. Candidates request votes from peers. A Candidate with a majority becomes Leader. The Leader sends AppendEntries heartbeats. If the Leader fails, Followers time out and elect a new Leader. Log entries are committed when replicated to a majority. The algorithm guarantees safety (committed entries are never lost) and liveness (eventually a Leader is elected).

Design considerations include: leader election safety (at most one leader per term), log matching (if two entries have the same index and term, all preceding entries are identical), and membership changes (adding/removing nodes while maintaining consensus). The implementation requires careful handling of edge cases: network partitions, split votes, stale leaders, and disk persistence. Use existing libraries (etcd's Raft, Apache ZooKeeper's ZAB) rather than implementing from scratch.

**Example:**
```python
class RaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = "follower"
        self.current_term = 0
        self.log = []
        self.commit_index = -1

    def request_vote(self, term, candidate_id):
        if term > self.current_term:
            self.current_term = term
            self.state = "follower"
            return True
        return False
```

## Q57: Design a `Pluggable Architecture` for extensibility.

**A:** A PluggableArchitecture allows new functionality to be added via plugins without modifying the core system. Core entities: `Plugin` (interface with lifecycle methods: init, start, stop), `PluginManager` (discovers, loads, and manages plugins), `ExtensionPoint` (hooks where plugins can add behavior), and `PluginRegistry` (tracks active plugins). Plugins can be loaded from JARs, npm packages, or dynamic libraries.

The PluginManager scans plugin directories, loads plugin manifests (name, version, dependencies, extension points), and initializes plugins in dependency order. The `ExtensionPoint` interface defines where plugins can hook in: `preProcess()`, `postProcess()`, `onEvent()`. The core system calls extension points at appropriate times, and registered plugins execute their logic.

Design considerations include: plugin isolation (plugins should not crash the core — use classloader isolation or sandboxing), dependency management (plugins can depend on other plugins or specific core versions), lifecycle management (graceful start, stop, and hot-reload without restarting the core), and plugin discovery (service loader pattern in Java, entry points in npm). The `PluginConfig` provides each plugin with its own configuration namespace. The `EventBus` lets plugins communicate with each other without direct dependencies.

**Example:**
```python
class PluginManager:
    def __init__(self):
        self.plugins = []
        self.extension_points = {}

    def register_extension_point(self, name, interface):
        self.extension_points[name] = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
        for hook in plugin.get_hooks():
            if hook.point in self.extension_points:
                self.extension_points[hook.point].append(hook.handler)

    def execute_extension(self, point_name, context):
        for handler in self.extension_points.get(point_name, []):
            handler(context)
```

## Q58: Design a `Multi-tenant` SaaS architecture.

**A:** A MultiTenant system serves multiple customers (tenants) from a single application instance. Core entities: `Tenant` (id, name, plan, config), `TenantContext` (current tenant for request), `TenantIsolation` (data separation strategy), and `TenantService` (manages tenant lifecycle). Three isolation models: shared database/shared schema, shared database/separate schemas, and separate databases.

Shared database with row-level isolation: all tenants' data in the same tables, differentiated by a `tenant_id` column. Every query includes `WHERE tenant_id = ?`. Use database Row-Level Security (PostgreSQL RLS) or application-level filtering. Separate schema: each tenant gets their own database schema. Separate database: each tenant has their own database (maximum isolation, highest cost).

The `TenantContext` propagates through the request: middleware extracts tenant ID from the request (subdomain, header, JWT claim) and sets a thread-local/context variable. Every data access layer reads the tenant context and filters accordingly. The `TenantResolver` handles tenant identification: `acme.myapp.com` → tenant "acme". The `PlanManager` enforces feature limits per plan (free tier: 1000 API calls/day, enterprise: unlimited).

**Example:**
```python
class TenantMiddleware:
    def __call__(self, request):
        tenant_id = self.resolve_tenant(request)
        TenantContext.set_current(tenant_id)
        response = self.app(request)
        TenantContext.clear()
        return response

class TenantRepository:
    def find_by_id(self, id):
        tenant_id = TenantContext.get_current()
        return self.db.query(
            "SELECT * FROM resources WHERE id = %s AND tenant_id = %s",
            id, tenant_id
        )
```

## Q59: Design a `Webhook` delivery system.

**A:** A WebhookSystem delivers HTTP callbacks to external URLs when events occur. Core entities: `Webhook` (url, events, secret, active), `WebhookDelivery` (webhook, event, payload, status, attempts), `Event` (type, data, timestamp), and `DeliveryService` (queues and delivers webhooks). The system must handle retries, delivery verification, and payload signing.

The delivery flow: event occurs → find matching webhooks → queue delivery jobs → send HTTP POST with JSON payload → verify response (2xx = success) → retry on failure. Retry policy: exponential backoff (1s, 5s, 25s, 125s) with maximum 5 attempts. The `DeliveryService` uses a message queue (SQS, Redis) for reliable delivery.

Security is critical: sign each payload with HMAC-SHA256 using the webhook's secret key. The recipient verifies the signature to ensure authenticity. Use a `X-Webhook-Signature` header. The `WebhookRegistry` manages webhook CRUD and event filtering (subscribe to specific event types). The `DeliveryTracker` records delivery status, response codes, and timing for debugging. Dead letter queue captures permanently failed deliveries for manual inspection.

**Example:**
```python
import hmac
import hashlib
import requests

class WebhookDelivery:
    def send(self, webhook, event):
        payload = json.dumps(event.to_dict())
        signature = hmac.new(
            webhook.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        response = requests.post(
            webhook.url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Webhook-Signature": f"sha256={signature}"
            },
            timeout=10
        )
        return response.status_code < 300
```

## Q60: Design a `Read-Through Cache` with write-behind.

**A:** A Read-Through Cache transparently loads data from the database when a cache miss occurs, and a Write-Behind Cache asynchronously writes cache changes to the database. Core entities: `Cache` (in-memory store with TTL), `CacheLoader` (loads from DB on miss), `WriteBehindQueue` (buffers writes for async flush), and `CachePolicy` (TTL, eviction, invalidation).

Read-through flow: application reads key → cache checks for key → if miss, CacheLoader loads from DB, stores in cache, returns to application → subsequent reads hit cache. The application doesn't know about the cache — it's transparent. This is different from a read-ahead cache which pre-populates based on predicted access patterns.

Write-behind flow: application writes to cache → cache stores locally → async worker flushes to DB in batches. This reduces DB load by batching writes and absorbs write spikes. The `WriteBehindQueue` uses a buffer with configurable flush intervals (e.g., every 5 seconds or when buffer reaches 1000 entries). If the cache node crashes before flushing, data is lost — use a write-ahead log (WAL) for durability. The `CacheInvalidationService` handles explicit invalidation: when a write happens in the DB directly (bypassing cache), invalidate the cache key.

**Example:**
```python
class ReadThroughCache:
    def __init__(self, db, loader, default_ttl=300):
        self.db = db
        self.loader = loader
        self.ttl = default_ttl
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                return entry.value
        value = self.loader.load(self.db, key)
        self.cache[key] = CacheEntry(value, self.ttl)
        return value

class WriteBehindCache:
    def __init__(self, db, flush_interval=5):
        self.db = db
        self.buffer = []
        self.flush_interval = flush_interval

    def put(self, key, value):
        self.cache[key] = value
        self.buffer.append(("put", key, value))
        if len(self.buffer) >= 1000:
            self.flush()

    def flush(self):
        for op, key, value in self.buffer:
            self.db.save(key, value)
        self.buffer.clear()
```

## Q61: Design a `Monitoring Dashboard` for system health.

**A:** A MonitoringDashboard aggregates metrics, logs, and alerts into a unified view for operators. Core entities: `Dashboard` (panels, refresh interval), `Panel` (query, visualization type: graph/table/heatmap), `AlertRule` (condition, threshold, notification channel), and `DataSource` (Prometheus, Elasticsearch, etc.). The dashboard must display real-time data with configurable time ranges.

The architecture: a frontend (React/Vue) queries a backend API, which queries multiple data sources. The `DashboardService` stores dashboard definitions (JSON/YAML). The `QueryService` translates panel queries into data-source-specific queries (PromQL for Prometheus, Lucene for Elasticsearch). The `VisualizationService` formats query results for different chart types.

Design considerations include: real-time updates (WebSocket or SSE for live data), drill-down (click a metric to see detailed view), correlation (overlay metrics and logs for the same time range), and template variables (dynamic dashboards where users select service, environment, etc.). Alert rules evaluate in the backend and push notifications (Slack, PagerDuty, email). The `DashboardSharing` service manages permissions (view-only, edit, admin).

**Example:**
```python
class DashboardPanel:
    def __init__(self, title, query, viz_type="graph"):
        self.title = title
        self.query = query
        self.viz_type = viz_type

    def execute(self, data_source, time_range):
        results = data_source.query(self.query, time_range)
        return self.format(results)

class AlertEvaluator:
    def evaluate(self, rule, data_source):
        value = data_source.query_single(rule.query, rule.time_range)
        if rule.condition == "above" and value > rule.threshold:
            self.notify(rule, value)
```

## Q62: Design a `Workflow Engine` for business processes.

**A:** A WorkflowEngine executes multi-step business processes with conditional logic, parallel execution, and error handling. Core entities: `Workflow` (name, steps, transitions), `Step` (action, type: task/gateway/subprocess), `Transition` (condition, target step), `WorkflowInstance` (running execution, current state, variables), and `WorkflowEngine` (executes and manages instances).

The workflow is modeled as a directed graph: steps are nodes, transitions are edges. Gateways (exclusive, parallel) handle branching: exclusive gateway picks one path based on conditions; parallel gateway splits into concurrent branches that must all complete (join). The engine tracks the current step and evaluates transitions to determine the next step.

Design considerations include: persistence (workflow instances must survive restarts — store state in a database), compensation (if a step fails, execute compensating steps for completed steps — saga pattern), timeout (steps that take too long trigger timeout events and alternative paths), and versioning (new workflow versions must not break running instances). The `WorkflowScheduler` handles timer-based steps (wait 3 days, then send reminder). Integration with external systems uses the Adapter pattern.

**Example:**
```python
class WorkflowEngine:
    def __init__(self, workflow):
        self.workflow = workflow

    def execute(self, instance):
        while not instance.is_complete():
            current = instance.current_step()
            result = current.execute(instance.context)
            instance.context.set_result(current.id, result)
            next_step = self.workflow.next_step(current, instance.context)
            instance.move_to(next_step)
        return instance
```

## Q63: Design a `Graph Database` query system.

**A:** A GraphDatabase stores entities as nodes and relationships as edges, enabling efficient traversal queries. Core entities: `Node` (id, labels, properties), `Edge` (source, target, type, properties), `Graph` (nodes, edges), and `CypherQuery` (declarative graph query language). The key advantage over relational databases: relationship traversal is O(1) per hop, not O(N) join operations.

The storage engine uses an adjacency list: each node stores references to its edges. For undirected graphs, edges are stored in both directions. Indexes on node labels and properties enable fast lookup of starting nodes. The query engine compiles declarative queries (like Cypher: `MATCH (p:Person)-[:FRIEND]->(f:Person) WHERE p.name = 'Alice' RETURN f`) into an execution plan that traverses the graph efficiently.

Design considerations include: index-free adjacency (each node directly references its neighbors — no index lookups during traversal), variable-length paths (`MATCH (a)-[:KNOWS*1..5]->(b)` finds paths of 1-5 hops), graph algorithms (shortest path, PageRank, community detection — often implemented as stored procedures), and caching (hot subgraphs cached in memory for fast traversal). The `QueryPlanner` optimizes query execution order, and the `TraversalEngine` implements breadth-first, depth-first, or weighted shortest-path traversal.

**Example:**
```python
class Graph:
    def __init__(self):
        self.nodes = {}
        self.adjacency = defaultdict(list)

    def add_edge(self, source, target, edge_type):
        self.adjacency[source].append((target, edge_type))

    def bfs(self, start, edge_type=None, max_depth=float('inf')):
        visited = set()
        queue = [(start, 0)]
        while queue:
            node, depth = queue.pop(0)
            if depth > max_depth or node in visited:
                continue
            visited.add(node)
            yield node
            for neighbor, etype in self.adjacency[node]:
                if edge_type is None or etype == edge_type:
                    queue.append((neighbor, depth + 1))
```

## Q64: Design a `Key-Value Store` like DynamoDB/Redis.

**A:** A KeyValueStore provides fast read/write access to data identified by keys. Core entities: `KVStore` (get, put, delete operations), `Partition` (hash-range of keys), `ReplicationGroup` (copies of a partition), and `ConsistentHashRing` (routes keys to partitions). The store must be distributed, highly available, and partition-tolerant (AP in CAP theorem).

The data model is simple: `put(key, value)`, `get(key) → value`, `delete(key)`. Values are byte arrays (serialized as needed). Keys are strings (or byte arrays). The store is organized into partitions using consistent hashing. Each partition has N replicas across different failure domains. Writes go to the coordinator node, which replicates to W nodes; reads query R nodes and return the most recent version (using vector clocks or timestamps for conflict detection).

Design considerations include: quorum consistency (W + R > N ensures read-your-writes consistency), anti-entropy (periodic full synchronization between replicas using Merkle trees to detect differences), read repair (when a read returns stale data from one replica, send the latest to the stale replica), and hinted handoff (when a replica is temporarily unavailable, another node stores a hint and forwards the write when the replica recovers). The `CompactionService` merges old SSTables to reclaim space and improve read performance.

**Example:**
```python
class KVStore:
    def __init__(self):
        self.data = {}
        self.version = {}

    def put(self, key, value):
        self.data[key] = value
        self.version[key] = self.version.get(key, 0) + 1

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.version[key] = self.version.get(key, 0) + 1
```

## Q65: Design a `Blob Storage` system like S3.

**A:** A BlobStorage system stores and retrieves large binary objects (files, images, videos). Core entities: `Bucket` (namespace for objects), `Object` (key, size, content hash, metadata, storage class), `StorageNode` (physical storage), and `BlobService` (API gateway). The system must handle petabyte-scale storage with high durability (11 nines).

The architecture: the API gateway handles authentication, rate limiting, and request routing. Metadata service stores object metadata (key, size, hash, storage class) in a distributed database. Data nodes store the actual bytes in object storage (each object stored as a sequence of chunks). A placement service determines which data nodes store each object based on storage class, geographic region, and load balancing.

Design considerations include: multipart upload (for objects > 100MB, split into parts uploaded in parallel and assembled), replication (store 3 copies across different failure domains), lifecycle policies (move objects to cheaper storage after N days: Standard → IA → Glacier), and presigned URLs (generate time-limited URLs for direct client upload/download). The `ObjectService` supports conditional operations (If-Match for optimistic concurrency) and range reads (for partial downloads).

**Example:**
```python
class BlobService:
    def put_object(self, bucket, key, data):
        content_hash = sha256(data)
        storage_node = self.placement.get_node(bucket, key)
        storage_node.write(bucket, key, data)
        self.metadata.save(ObjectMetadata(bucket, key, len(data), content_hash))

    def get_object(self, bucket, key, range_start=None, range_end=None):
        meta = self.metadata.get(bucket, key)
        storage_node = self.placement.get_node(bucket, key)
        return storage_node.read(bucket, key, range_start, range_end)
```

## Q66: Design a `Sharded Counter` for high-throughput metrics.

**A:** A ShardedCounter distributes a single logical counter across multiple shards to handle high-concurrency increments without contention. A single counter with atomic operations becomes a bottleneck under heavy load (millions of increments per second). Sharding splits the counter into N shards, each updated independently, with the final value being the sum of all shards.

The design: N shards (e.g., 16), each independently incremented. `increment()` randomly selects a shard and increments it. `get()` sums all shard values. The random shard selection distributes writes evenly and eliminates contention. Each shard can use a local variable (single-server) or a separate Redis key (distributed).

For distributed sharding, each shard is a Redis key: `counter:shard:0` through `counter:shard:15`. `INCR` on a random shard is O(1). `GET` sums all 16 keys. The count is approximate (non-transactional sum of shards), but the error is small and acceptable for metrics. For exact counts, use a single atomic counter (slower). The `ShardedCounter` class encapsulates this logic. The shard count is configurable — more shards reduce contention but increase read cost.

**Example:**
```python
import random

class ShardedCounter:
    def __init__(self, num_shards=16):
        self.shards = [0] * num_shards
        self.num_shards = num_shards

    def increment(self, shard=None):
        if shard is None:
            shard = random.randint(0, self.num_shards - 1)
        self.shards[shard] += 1

    def get(self):
        return sum(self.shards)
```

## Q67: Design a `Bloom Filter` for membership testing.

**A:** A BloomFilter is a probabilistic data structure that tests whether an element is in a set. False positives are possible (says an element is in the set when it's not), but false negatives are impossible (if it says an element is not in the set, it definitely isn't). It's extremely memory-efficient compared to hash sets.

The Bloom filter is a bit array of M bits, initialized to 0. Adding an element: hash it with K different hash functions, set the corresponding K bits to 1. Checking an element: hash it with the same K functions, check if all K bits are set. If any bit is 0, the element is definitely not in the set. If all bits are 1, the element is probably in the set (false positive rate depends on M, K, and the number of elements).

The false positive rate is approximately `(1 - e^(-kn/m))^k` where n is the number of elements, m is the bit array size, and k is the number of hash functions. For 1% false positive rate with 1 billion elements, the Bloom filter needs about 1.2 GB (vs. 40+ GB for a hash set). Applications: web crawlers (URL deduplication), databases (check if key exists before expensive disk lookup), caches (avoid caching items that don't exist in the database).

**Example:**
```python
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item):
        for i in range(self.num_hashes):
            idx = mmh3.hash(item, i) % self.size
            self.bit_array[idx] = 1

    def contains(self, item):
        for i in range(self.num_hashes):
            idx = mmh3.hash(item, i) % self.size
            if not self.bit_array[idx]:
                return False
        return True  # may be false positive
```

## Q68: Design a `Proximity Service` for location-based queries.

**A:** A ProximityService finds nearby places, users, or objects based on geographic coordinates. Core entities: `Location` (lat, lng), `Place` (id, name, location, type), `GeoIndex` (spatial data structure for fast proximity queries), and `ProximityService` (finds nearby places within radius). The challenge is efficiently querying millions of locations by proximity.

The two main data structures are: Geohash (encodes lat/lng into a string prefix — nearby places share prefixes) and Quadtree (recursive subdivision of 2D space). Geohash is simpler: index places by their geohash prefix. Query: find all places with matching prefix + scan neighbors. Quadtree is more flexible: each node splits into 4 quadrants; query traverses relevant quadrants.

The geohash approach: divide the world into a grid using geohash strings. A geohash of precision 6 covers a 0.6km x 0.6km area. To find nearby places, look up the geohash of the query point and neighboring geohashes (8 neighbors). This reduces the search space from millions to thousands. The `GeoIndex` stores places indexed by geohash prefix. For more precision, use a KD-tree for exact distance calculations after the geohash narrows the search.

**Example:**
```python
import geohash2

class GeoIndex:
    def __init__(self):
        self.index = defaultdict(list)

    def add_place(self, place):
        gh = geohash2.encode(place.lat, place.lng, precision=6)
        self.index[gh].append(place)

    def find_nearby(self, lat, lng, radius_km=1.0):
        center_gh = geohash2.encode(lat, lng, precision=6)
        candidates = []
        for neighbor in geohash2.neighbors(center_gh).values():
            candidates.extend(self.index.get(neighbor, []))
        candidates.extend(self.index.get(center_gh, []))
        return [p for p in candidates if p.distance_to(lat, lng) <= radius_km]
```

## Q69: Design a `Recommendation Engine` like Netflix/Amazon.

**A:** A RecommendationEngine suggests items (movies, products, content) based on user behavior. Core entities: `User` (id, preferences, history), `Item` (id, features, category), `Interaction` (user, item, rating, timestamp), and `RecommendationService` (generates recommendations). Three main approaches: collaborative filtering, content-based filtering, and hybrid.

Collaborative filtering finds users with similar tastes (user-based) or items liked by similar users (item-based). User-based: find K users who rated similar items as the target user, aggregate their ratings for unseen items. Item-based: for each item the user liked, find similar items. The similarity metric is typically cosine similarity or Pearson correlation. Matrix factorization (SVD, ALS) decomposes the user-item interaction matrix into latent factors.

Content-based filtering recommends items similar to what the user has liked before, based on item features (genre, director, keywords). The user profile is a vector of preferred features. The `RecommendationService` combines both approaches: collaborative filtering for discovery (find new categories), content-based for consistency (similar to past likes). The `Ranker` re-scores candidates based on freshness, diversity, and business rules (promote new content).

**Example:**
```python
import numpy as np

class CollaborativeFilter:
    def __init__(self, interactions):
        self.user_item_matrix = self.build_matrix(interactions)

    def recommend(self, user_id, top_k=10):
        user_vector = self.user_item_matrix[user_id]
        similarities = self.user_item_matrix.dot(user_vector)
        scores = self.user_item_matrix.T.dot(similarities)
        scores[user_vector > 0] = 0  # exclude already rated
        top_items = np.argsort(scores)[-top_k:][::-1]
        return top_items
```

## Q70: Design a `Version Control` system like Git (simplified).

**A:** A VersionControlSystem tracks file changes over time, enabling branching, merging, and history navigation. Core entities: `Repository` (collection of commits), `Commit` (snapshot of files, parent commit(s), message, timestamp), `Tree` (directory structure), `Blob` (file content), `Branch` (pointer to a commit), and `Index` (staging area).

Git's object model: every object (commit, tree, blob) is identified by a SHA-1 hash of its content. A commit points to a tree (root directory) and a parent commit. A tree points to blobs (files) and sub-trees (subdirectories). Branches are just pointers to commits. The HEAD pointer indicates the current branch. The staging area (index) tracks changes that will be included in the next commit.

The key operations: `commit` (create a new commit from staged changes), `branch` (create a new pointer), `checkout` (switch branches), `merge` (combine two branches — fast-forward or three-way merge), and `diff` (compare commits). The `MergeStrategy` handles conflicts: three-way merge compares the two branches and their common ancestor. Conflicting changes require manual resolution. The `CommitGraph` (DAG) enables history traversal, blame, and rebase.

**Example:**
```python
import hashlib
from datetime import datetime

class Commit:
    def __init__(self, tree, parent, message):
        self.tree = tree
        self.parent = parent
        self.message = message
        self.timestamp = datetime.now()
        self.id = self._hash()

    def _hash(self):
        content = f"{self.tree}{self.parent}{self.message}{self.timestamp}"
        return hashlib.sha1(content.encode()).hexdigest()

class Repository:
    def __init__(self):
        self.commits = {}
        self.branches = {"main": None}
        self.head = "main"

    def commit(self, tree, message):
        parent = self.branches[self.head]
        c = Commit(tree, parent, message)
        self.commits[c.id] = c
        self.branches[self.head] = c.id
        return c
```

## Q71: Design a `Notification Preferences` system for user settings.

**A:** A NotificationPreferences system allows users to control which notifications they receive and through which channels. Core entities: `User` (id, preferences), `NotificationPreference` (event type, channel, enabled, schedule), `NotificationType` (order_update, marketing, security, social), and `PreferenceService` (evaluates preferences). Users can configure per-type, per-channel preferences.

The preference model: each notification type has a default configuration (e.g., security alerts: all channels enabled, no opt-out). Users can override defaults per type and channel. A preference entry: `{type: "order_update", channel: "email", enabled: true, schedule: "daily_digest"}`. The `PreferenceService` checks: is this notification type enabled for this user? Is this channel enabled? Is it within the user's quiet hours?

Design considerations include: quiet hours (no notifications between 10 PM and 7 AM), digest mode (batch notifications into daily/weekly summaries), channel preferences (push for urgent, email for non-urgent), and opt-out management (CAN-SPAM compliance for marketing emails). The `NotificationRouter` consults preferences before sending each notification. The `DigestService` collects notifications for digest-mode users and sends batched summaries on schedule.

**Example:**
```python
class PreferenceService:
    def should_notify(self, user, notification_type, channel):
        pref = self.get_preference(user.id, notification_type, channel)
        if pref is None:
            return self.get_default(notification_type, channel)
        if not pref.enabled:
            return False
        if self.is_quiet_hours(user):
            return pref.urgent_only and notification_type.is_urgent
        return True
```

## Q72: Design a `License Key` validation system.

**A:** A LicenseKeySystem validates software licenses, manages activation, and enforces usage limits. Core entities: `License` (key, product, type: trial/standard/enterprise, expiry, maxActivations), `Activation` (license, machineId, activatedAt), and `LicenseService` (validates, activates, deactivates). The system must work offline (periodic online validation) and resist tampering.

The license key encodes: product ID, license type, expiry date, and a digital signature. The key is typically base32-encoded for human readability. Validation: parse the key → verify the digital signature (using RSA or Ed25519) → check expiry → check activation count. The signature prevents forgery — only the server can generate valid keys.

The activation flow: client sends license key + machine fingerprint → server verifies key → checks activation count < max → stores activation → returns validation token (JWT with expiry). Offline validation: client caches the validation token and verifies locally. Periodic online check (every 30 days) ensures continued validity. The `LicenseService` handles deactivation (free an activation slot), upgrades (change license type), and grace periods (allow short-term usage after expiry for renewal).

**Example:**
```python
import jwt
from cryptography.hazmat.primitives.asymmetric import ed25519

class LicenseValidator:
    def __init__(self, public_key):
        self.public_key = public_key

    def validate(self, license_key):
        try:
            payload = jwt.decode(license_key, self.public_key, algorithms=["EdDSA"])
            if payload["expiry"] < time.time():
                return False
            return True
        except jwt.InvalidSignatureError:
            return False
```

## Q73: Design a `Debounce/Throttle` mechanism for event handling.

**A:** Debounce and Throttle control the rate of event processing. Debounce delays processing until a pause in events (e.g., wait 300ms after the last keystroke before searching). Throttle limits processing to at most once per interval (e.g., scroll events processed at most once every 100ms). Both prevent excessive function calls during rapid events.

Debounce implementation: when an event arrives, start/reset a timer. Only execute the function when the timer expires without being reset. This is ideal for search-as-you-type (wait until the user stops typing) and window resize handling. The timer is typically managed with `setTimeout` (JavaScript) or `threading.Timer` (Python).

Throttle implementation: when an event arrives, check if enough time has passed since the last execution. If yes, execute and record the timestamp. If no, skip the event. This is ideal for scroll handlers, mouse move handlers, and API rate limiting. Leading throttle executes on the first event in the interval; trailing throttle executes on the last event. Both can be combined.

**Example:**
```python
import time
import threading

def debounce(wait):
    def decorator(func):
        timer = None
        def wrapper(*args, **kwargs):
            nonlocal timer
            if timer:
                timer.cancel()
            timer = threading.Timer(wait, func, args, kwargs)
            timer.start()
        return wrapper
    return decorator

def throttle(interval):
    def decorator(func):
        last_called = [0]
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] >= interval:
                last_called[0] = now
                return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Q74: Design a `Dependency Injection Container`.

**A:** A DI Container manages object creation, dependency resolution, and lifecycle. Core entities: `Container` (registers and resolves types), `Registration` (type mapping, lifetime: transient/singleton/scoped), `Scope` (manages scoped lifetimes), and `Resolver` (creates instances with resolved dependencies). The container eliminates manual object construction and enables loose coupling.

Registration: `container.register(Interface, ConcreteClass, lifetime=Singleton)`. Resolution: `container.resolve(Interface) → ConcreteClass instance`. The container walks the dependency graph: if `UserService` depends on `UserRepository` and `EmailService`, it resolves each dependency recursively. Circular dependencies are detected and reported. Lifetime management: transient (new instance per resolve), singleton (one instance forever), scoped (one instance per request/scope).

Design considerations include: auto-registration (scan assemblies for interface-implementation pairs), interceptors (AOP — add logging, caching, or validation around resolved objects), and module system (group related registrations into modules). The `Container.build()` finalizes registrations and optimizes resolution paths. The `ServiceProvider` is the runtime interface for resolving dependencies. Frameworks like Spring (Java), Dagger (Java/Android), and Autofac (C#) implement this pattern.

**Example:**
```python
class Container:
    def __init__(self):
        self.registrations = {}
        self.singletons = {}

    def register(self, interface, impl, singleton=False):
        self.registrations[interface] = (impl, singleton)

    def resolve(self, interface):
        if interface in self.singletons:
            return self.singletons[interface]
        impl, is_singleton = self.registrations[interface]
        deps = [self.resolve(param) for param in get_type_hints(impl.__init__).values()]
        instance = impl(*deps)
        if is_singleton:
            self.singletons[interface] = instance
        return instance
```

## Q75: Design an `Audit Trail` system for compliance.

**A:** An AuditTrail records all significant actions for compliance and forensics. Core entities: `AuditEvent` (timestamp, actor, action, resource, before/after state, IP address), `AuditLog` (append-only store of events), and `AuditService` (records and queries events). The log must be tamper-evident — entries cannot be modified or deleted.

The `AuditEvent` captures: who (user ID, IP, user agent), what (action type), when (timestamp), where (resource type + ID), and what changed (before/after state as JSON diffs). Events are written to an append-only store (write-once storage, immutable database, or blockchain-style hash chain). Each event includes a hash of the previous event, creating a tamper-evident chain.

Design considerations include: immutability (write-once storage — never update or delete audit entries), performance (audit writes should not block the main operation — use async/event-driven writing), retention (compliance regulations require specific retention periods — GDPR right to be forgotten may require redaction), and queryability (search by actor, action, time range, resource). The `AuditQueryService` provides rich search across the audit log. Integration is via AOP (aspect around service methods) or event listeners.

**Example:**
```python
import hashlib
import json
from datetime import datetime

class AuditService:
    def __init__(self, store):
        self.store = store
        self.last_hash = "0" * 64

    def record(self, actor, action, resource, before=None, after=None):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "actor": actor,
            "action": action,
            "resource": resource,
            "before": before,
            "after": after,
            "prev_hash": self.last_hash
        }
        event_str = json.dumps(event, sort_keys=True)
        event["hash"] = hashlib.sha256(event_str.encode()).hexdigest()
        self.last_hash = event["hash"]
        self.store.append(event)
```

## Q76: Design a `Caching Strategy` for a news feed application.

**A:** A news feed caching strategy must balance freshness with performance. The feed changes constantly (new posts, likes, comments) but must load in < 100ms. The strategy uses a multi-tier cache: L1 (in-process memory, < 1ms), L2 (Redis, ~5ms), L3 (database, ~50ms). Hot feeds (celebrity accounts) are cached aggressively; cold feeds (inactive users) are computed on demand.

The feed cache uses a write-through strategy for user timelines: when a user posts, immediately update the cached feeds of their followers. This is the push model. For reads, check L1 first, then L2, then L3. The cache key pattern is `feed:{user_id}` with a TTL of 5 minutes. Stale data is acceptable — a few seconds of delay in showing a new post is fine.

Cache invalidation follows these rules: explicit invalidation on post deletion (remove from all follower feeds), time-based expiration (TTL), and event-driven invalidation (new comment triggers a partial update). The `FeedCacheService` implements a hybrid approach: push for regular users (pre-computed feeds), pull for celebrities (their posts are fetched on-demand to avoid massive fan-out). Cache warming pre-populates feeds for active users during deployment.

**Example:**
```python
class FeedCache:
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db

    def get_feed(self, user_id, limit=20):
        cached = self.redis.lrange(f"feed:{user_id}", 0, limit - 1)
        if cached:
            return [json.loads(p) for p in cached]
        posts = self.db.get_feed(user_id, limit)
        self.redis.rpush(f"feed:{user_id}", *[json.dumps(p) for p in posts])
        self.redis.expire(f"feed:{user_id}", 300)
        return posts

    def on_new_post(self, post):
        for follower_id in post.author.followers:
            self.redis.lpush(f"feed:{follower_id}", json.dumps(post))
            self.redis.ltrim(f"feed:{follower_id}", 0, 499)
```

## Q77: Design a `Database Sharding` strategy for horizontal scaling.

**A:** Database sharding splits a single database across multiple servers. Core entities: `Shard` (database partition), `ShardKey` (column used for routing), `ShardRouter` (maps keys to shards), and `CrossShardQuery` (joins across shards). The key decision is shard key selection — it determines data distribution and query efficiency.

The two main sharding strategies: hash-based (hash the shard key to distribute evenly — `shard = hash(user_id) % num_shards`) and range-based (assign contiguous ranges to shards — shard 0 gets user_id 1-1M, shard 1 gets 1M-2M). Hash-based provides even distribution but makes range queries expensive. Range-based supports range queries but risks hotspots (all new users go to the latest shard).

Design considerations include: cross-shard joins (expensive — denormalize to avoid), rebalancing (adding shards requires data migration — use consistent hashing to minimize redistribution), shard key selection (choose a key that distributes evenly and is used in most queries — user_id for user tables, order_id for orders), and global tables (small reference tables replicated to all shards). The `ShardManager` handles connection routing, query rewriting, and result aggregation across shards.

**Example:**
```python
class ShardRouter:
    def __init__(self, shards):
        self.shards = shards
        self.num_shards = len(shards)

    def get_shard(self, shard_key):
        idx = hash(shard_key) % self.num_shards
        return self.shards[idx]

    def execute_on_shards(self, query, shard_keys):
        results = {}
        for key in shard_keys:
            shard = self.get_shard(key)
            results[key] = shard.execute(query, key)
        return results
```

## Q78: Design a `Data Pipeline` for ETL processing.

**A:** A DataPipeline extracts data from sources, transforms it, and loads it into a target system. Core entities: `Source` (database, API, file), `Transform` (clean, aggregate, enrich), `Sink` (data warehouse, search index, cache), `Pipeline` (orchestrates source → transform → sink), and `PipelineRun` (execution instance with status and metrics).

The architecture follows the medallion pattern: Bronze (raw data ingested as-is), Silver (cleaned, deduplicated, standardized), Gold (aggregated, business-ready). Each layer is a pipeline stage. The `PipelineOrchestrator` manages dependencies — Silver can't run until Bronze completes successfully. DAG-based scheduling (like Airflow) handles complex dependency graphs.

Design considerations include: exactly-once semantics (use idempotent writes and deduplication), schema evolution (handle source schema changes gracefully), backfill (reprocess historical data), and monitoring (track data freshness, quality metrics, pipeline duration). The `DataQuality` layer validates data at each stage (null checks, range validation, referential integrity). The `PipelineScheduler` triggers runs on schedule (hourly, daily) or event (new file arrived). Error handling routes failed records to a dead letter queue for investigation.

**Example:**
```python
class Pipeline:
    def __init__(self, name):
        self.name = name
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def run(self):
        data = None
        for stage in self.stages:
            data = stage.execute(data)
            self.log_metrics(stage, data)
        return data

class TransformStage:
    def execute(self, data):
        return data.dropna().drop_duplicates().reset_index(drop=True)
```

## Q79: Design a `Service Mesh` for microservice communication.

**A:** A ServiceMesh handles cross-cutting concerns (security, observability, traffic management) at the infrastructure layer rather than in application code. Core entities: `SidecarProxy` (intercepts all network traffic for a service), `ControlPlane` (configures proxies), `DataPlane` (proxy-to-proxy communication), and `Policy` (routing rules, security policies, rate limits).

The sidecar pattern: each service instance has a proxy (Envoy, Linkerd-proxy) running alongside it. All inbound and outbound traffic goes through the proxy. The proxy handles: mutual TLS (mTLS — encrypts all service-to-service communication), load balancing (retry-aware, circuit-breaking), observability (logs, metrics, distributed traces), and traffic management (canary deployments, traffic splitting, timeouts).

Design considerations include: zero-config security (mTLS enabled by default — no application code changes), observability without instrumentation (proxies capture all traffic metadata), gradual rollout (introduce the mesh incrementally — one service at a time), and performance overhead (sidecar adds ~1ms latency per hop). The `ControlPlane` (Istio's istiod, Linkerd's control plane) distributes configuration to proxies. The `PolicyEngine` enforces RBAC (which service can call which), rate limits, and circuit breaker settings.

**Example:**
```yaml
# Istio VirtualService for canary deployment
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
spec:
  hosts:
    - my-service
  http:
    - route:
        - destination:
            host: my-service
            subset: v1
          weight: 90
        - destination:
            host: my-service
            subset: v2
          weight: 10
```

## Q80: Design an `A/B Testing` framework for feature experiments.

**A:** An ABTestingFramework assigns users to experiment variants, tracks metrics, and determines statistical significance. Core entities: `Experiment` (name, variants, targeting rules, primary metric), `Variant` (name, traffic percentage, configuration), `Assignment` (user, experiment, variant), and `ExperimentResult` (statistical analysis, confidence interval). The framework must ensure consistent variant assignment and accurate metrics collection.

The assignment flow: user enters an experiment → the `AssignmentService` hashes `user_id + experiment_id` to deterministically assign a variant → the variant configuration is returned to the application → the user experiences the variant. Deterministic assignment ensures the same user always gets the same variant (consistency) and that traffic percentages are respected across the experiment.

The `MetricsCollector` tracks the primary metric (conversion rate, revenue, engagement) for each variant. The `StatisticalAnalyzer` runs significance tests (t-test, chi-squared, Bayesian analysis) to determine if the variant's performance is significantly different from the control. The experiment is concluded when enough data is collected (power analysis determines sample size). The framework handles: multi-variate testing (multiple independent experiments), interference prevention (users in overlapping experiments are excluded), and novelty effects (users behave differently initially).

**Example:**
```python
import hashlib

class ABTest:
    def __init__(self, experiment_id, variants):
        self.experiment_id = experiment_id
        self.variants = variants  # {"control": 50, "treatment": 50}

    def assign_variant(self, user_id):
        hash_val = int(hashlib.md5(
            f"{self.experiment_id}:{user_id}".encode()
        ).hexdigest(), 16)
        bucket = hash_val % 100
        cumulative = 0
        for variant, percentage in self.variants.items():
            cumulative += percentage
            if bucket < cumulative:
                return variant
```

## Q81: Design a `Canary Deployment` system for safe releases.

**A:** A CanaryDeployment gradually routes traffic from the old version to the new version, monitoring for errors before fully rolling out. Core entities: `Deployment` (service, current version, target version), `TrafficSplit` (percentage routing: 95% old / 5% canary), `HealthMonitor` (tracks error rates, latency, custom metrics), and `RollbackPolicy` (automatic rollback on degradation).

The deployment flow: deploy canary to a subset of instances → route 5% of traffic to canary → monitor metrics for N minutes → if healthy, increase traffic (5% → 25% → 50% → 100%) → if unhealthy, rollback and alert. Each traffic increment has a "bake time" to collect enough data for statistical comparison.

The `TrafficRouter` (Istio VirtualService, nginx, or application-level) splits traffic by weight. The `HealthMonitor` compares canary metrics against baseline: error rate must be within threshold, latency p99 must not increase by more than X%, and custom business metrics (conversion rate) must not degrade. The `AutoRollback` triggers if any threshold is violated. The system supports blue-green (instant switch), canary (gradual), and ring-based (internal → beta → GA) deployment strategies.

**Example:**
```python
class CanaryDeployer:
    def __init__(self, traffic_router, health_monitor):
        self.router = traffic_router
        self.monitor = health_monitor

    def deploy(self, service, new_version, steps=[5, 25, 50, 100]):
        for percentage in steps:
            self.router.split(service, old=100 - percentage, canary=percentage)
            time.sleep(self.bake_time)
            if self.monitor.is_unhealthy(service):
                self.router.rollback(service)
                raise DeploymentFailedException()
        self.router.promote(service, new_version)
```

## Q82: Design a `Dead Letter Queue` handling system.

**A:** A DeadLetterQueue (DLQ) captures messages that failed processing after maximum retries. Core entities: `MessageQueue` (primary queue), `DeadLetterQueue` (failed messages), `DLQHandler` (processes failed messages), and `RetryPolicy` (max retries, backoff). The DLQ prevents poison messages from blocking the queue and provides a mechanism for investigation and reprocessing.

The flow: message fails → retry with backoff → max retries exceeded → move to DLQ with metadata (failure reason, retry count, original timestamp, stack trace). The `DLQHandler` provides: inspection (view failed messages with full context), reprocessing (replay messages back to the main queue), manual intervention (fix the underlying issue, then reprocess), and alerting (notify when DLQ depth exceeds threshold).

Design considerations include: message metadata (capture everything needed for debugging — the original payload, error details, retry history, timestamps), TTL (old DLQ messages are archived or deleted), batch reprocessing (replay a group of related messages), and root cause analysis (aggregate DLQ messages by error type to identify systemic issues). The `DLQAnalyzer` groups failures by error pattern and recommends fixes. The `CircuitBreaker` integration prevents processing messages that will always fail.

**Example:**
```python
class DLQHandler:
    def __init__(self, main_queue, dlq):
        self.main_queue = main_queue
        self.dlq = dlq

    def handle_failure(self, message, error, max_retries=3):
        message.metadata["retry_count"] = message.metadata.get("retry_count", 0) + 1
        message.metadata["last_error"] = str(error)
        if message.metadata["retry_count"] >= max_retries:
            self.dlq.enqueue(message)
            self.alert_if_threshold_exceeded()
        else:
            delay = 2 ** message.metadata["retry_count"]
            self.main_queue.enqueue_with_delay(message, delay)

    def reprocess(self, dlq_message):
        self.main_queue.enqueue(dlq_message)
        self.dlq.remove(dlq_message)
```

## Q83: Design a `Write-Ahead Log` for durability.

**A:** A WriteAheadLog (WAL) ensures durability by writing changes to a log before applying them to the actual data store. Core entities: `LogEntry` (sequence number, operation type, data, checksum), `WALManager` (writes, reads, checkpoints), and `RecoveryManager` (replays log on startup). The WAL guarantees that committed data is never lost, even after crashes.

The write flow: application prepares a change → WAL appends the entry to the log file (sequential write — fast) → returns to application (acknowledged) → asynchronously apply the change to the actual data store. On crash recovery: replay the WAL from the last checkpoint, re-applying all committed entries. This is the foundation of most database systems (PostgreSQL, MySQL InnoDB) and message brokers (Kafka).

Design considerations include: log rotation (periodically create new log files, delete old ones after checkpointing), checksumming (detect corruption), fsync (force writes to disk for true durability — expensive but necessary for critical data), and compaction (merge small log entries to reclaim space). The `WALManager` handles concurrent writes (append-only, naturally thread-safe), log segment management, and checkpoint creation (snapshot the data store state + log position).

**Example:**
```python
class WriteAheadLog:
    def __init__(self, log_path):
        self.log_path = log_path
        self.sequence = 0

    def append(self, operation, data):
        self.sequence += 1
        entry = LogEntry(self.sequence, operation, data)
        entry.checksum = self.compute_checksum(entry)
        with open(self.log_path, 'ab') as f:
            f.write(entry.serialize())
        return self.sequence

    def recover(self, data_store):
        with open(self.log_path, 'rb') as f:
            for entry in LogEntry.read_all(f):
                if entry.operation == "PUT":
                    data_store.put(entry.key, entry.value)
                elif entry.operation == "DELETE":
                    data_store.delete(entry.key)
```

## Q84: Design a `Event-Driven Architecture` for decoupled services.

**A:** An Event-Driven Architecture (EDA) uses events as the primary communication mechanism between services. Core entities: `Event` (type, payload, metadata, timestamp), `EventBus` (delivers events to subscribers), `EventHandler` (processes events), and `EventStore` (persists events for replay). Services publish events when something significant happens; other services subscribe and react.

The two main patterns: event notification (lightweight events that say "something happened" — subscribers fetch details) and event-carried state transfer (events contain full data — no follow-up fetch needed). Event notification is simpler but causes extra API calls. Event-carried state transfer is more data-heavy but eliminates coupling to the producer's API.

Design considerations include: event schema evolution (version events, backward compatibility), ordering (partition events by entity ID to guarantee per-entity ordering), exactly-once delivery (idempotent handlers + transactional outbox), and dead letter queues (capture events that fail processing). The `EventBus` implementation choices: Kafka (ordered, durable, high-throughput), RabbitMQ (flexible routing, at-most-once/at-least-once), or cloud-native (SNS/SQS, EventBridge). The `OutboxPattern` ensures events are published atomically with database changes.

**Example:**
```python
class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def publish(self, event):
        for handler in self.subscribers[event.type]:
            handler.handle(event)

    def subscribe(self, event_type, handler):
        self.subscribers[event_type].append(handler)

class OrderEventHandler:
    def handle(self, event):
        if event.type == "OrderCreated":
            self.inventory.reserve(event.payload["items"])
        elif event.type == "OrderCancelled":
            self.inventory.release(event.payload["items"])
```

## Q85: Design a `Cell-Based Architecture` for scalability.

**A:** A Cell-Based Architecture partitions users into independent cells, each with its own complete stack (compute, database, cache, queue). Core entities: `Cell` (isolated deployment unit), `CellRouter` (routes users to cells), `CellConfig` (per-cell configuration), and `GlobalServices` (shared cross-cell services). Each cell handles a subset of users independently.

Cells provide: blast radius reduction (a failure in Cell A doesn't affect Cell B), independent scaling (Cell A handles 10M users, Cell B handles 5M), and simplified testing (test one cell instead of the entire system). The `CellRouter` maps users to cells using consistent hashing on user_id. Cell boundaries are typically at the infrastructure level — each cell is a complete, isolated deployment.

Design considerations include: cross-cell queries (some operations need data from multiple cells — keep these rare and use async replication), cell rebalancing (moving users between cells), and global data (reference data shared across cells — replicate to each cell). Cell-based architecture is used by AWS (each AZ is a cell), Netflix (cells for user segments), and Stripe (cells for API key prefixes). The `CellMigrationService` handles moving users between cells with minimal downtime.

**Example:**
```python
class CellRouter:
    def __init__(self, cells):
        self.cells = cells
        self.ring = ConsistentHashRing(cells)

    def route(self, user_id):
        cell = self.ring.get_node(user_id)
        return cell.endpoint

class Cell:
    def __init__(self, name, db, cache, queue):
        self.name = name
        self.db = db
        self.cache = cache
        self.queue = queue
```

## Q86: Design a `Chaos Engineering` framework for resilience testing.

**A:** A ChaosEngineering framework intentionally introduces failures to test system resilience. Core entities: `Experiment` (hypothesis, fault to inject, steady state definition), `Fault` (type: latency, kill, CPU stress, network partition), `SteadyState` (expected behavior under normal conditions), and `ChaosRun` (execution with metrics and pass/fail). The goal is to find weaknesses before they cause real outages.

The experiment flow: define steady state (e.g., "API response time < 200ms, error rate < 0.1%") → inject fault (add 500ms latency to payment service) → observe if steady state is maintained → if steady state breaks, the system has a weakness → fix it. The `ChaosOrchestrator` manages experiment lifecycle: plan → execute → observe → analyze → report.

Design considerations include: blast radius control (start small — one instance, then one AZ, then cross-AZ), automated rollback (stop the experiment if critical systems degrade), safety mechanisms (only run in production if you've validated in staging first), and observability (comprehensive monitoring during experiments). Tools like Chaos Monkey (random instance termination), Litmus (Kubernetes chaos), and Gremlin (commercial chaos platform) implement these patterns. The `GameDay` orchestrates coordinated chaos experiments across teams.

**Example:**
```python
class ChaosExperiment:
    def __init__(self, name, hypothesis, fault, steady_state):
        self.name = name
        self.hypothesis = hypothesis
        self.fault = fault
        self.steady_state = steady_state

    def run(self, orchestrator):
        baseline = self.steady_state.measure()
        orchestrator.inject(self.fault)
        time.sleep(self.duration)
        result = self.steady_state.measure()
        orchestrator.recover(self.fault)
        return ExperimentResult(
            baseline=baseline,
            during=result,
            passed=self.steady_state.is_met(result)
        )
```

## Q87: Design a `Feature Toggling` system with complex targeting.

**A:** A FeatureToggling system enables runtime feature control with sophisticated user targeting. Core entities: `FeatureFlag` (name, enabled, targeting rules, variants, prerequisites), `TargetingRule` (conditions with operators: equals, starts_with, in, percentage), `Prerequisite` (flag A must be on before flag B evaluates), and `User` (attributes for targeting).

The targeting rule engine evaluates conditions in order: percentage rollout → user segments → attribute matching → prerequisite flags. A rule: `if user.plan == "enterprise" AND user.country IN ["US", "UK"] AND percentage(user_id, 10) → variant "enhanced"`. Rules are evaluated top-down; the first matching rule determines the variant.

Design considerations include: flag dependencies (flag B depends on flag A — if A is off, B returns default), environment-specific overrides (different targeting per dev/staging/prod), audit logging (track who changed targeting when), and SDK caching (evaluate flags locally with a short polling interval to avoid network calls). The `FlagEvaluator` is deterministic — given the same user and flag, it always returns the same variant. The `FlagDashboard` provides a UI for managing flags, viewing metrics per variant, and scheduling rollouts.

**Example:**
```python
class FeatureFlagEvaluator:
    def evaluate(self, flag, user):
        if not flag.enabled:
            return flag.default_variant
        for rule in flag.targeting_rules:
            if self.matches(rule, user):
                return rule.variant
        return flag.default_variant

    def matches(self, rule, user):
        for condition in rule.conditions:
            user_val = getattr(user, condition.attribute, None)
            if not condition.operator.evaluate(user_val, condition.value):
                return False
        return True
```

## Q88: Design a `Multi-Region` deployment with data replication.

**A:** A MultiRegion system deploys application instances in multiple geographic regions for low latency and disaster recovery. Core entities: `Region` (name, endpoint, data replica), `DataReplication` (async or sync cross-region replication), `RoutingPolicy` (direct users to nearest region), and `FailoverPolicy` (redirect traffic if a region fails).

Data replication strategies: active-active (both regions accept writes, replicate bidirectionally — eventual consistency), active-passive (one region handles all writes, replicates to standby), and global tables (DynamoDB Global Tables — multi-region, multi-active). Active-active requires conflict resolution (last-writer-wins, or application-level merge).

Design considerations include: data residency (some data must stay in specific regions for GDPR), conflict resolution (two users in different regions edit the same record simultaneously), and failover (detect region failure, reroute traffic, promote replica to primary). The `RegionHealthChecker` monitors each region's health (latency, error rate, connectivity). The `GlobalLoadBalancer` routes users based on latency, geographic proximity, and health. The `DataSynchronizer` handles cross-region replication with conflict detection.

**Example:**
```python
class MultiRegionRouter:
    def __init__(self, regions):
        self.regions = regions

    def route(self, user_location):
        nearest = min(self.regions,
            key=lambda r: r.distance_to(user_location))
        if nearest.is_healthy():
            return nearest.endpoint
        fallback = self.failover(nearest)
        return fallback.endpoint

    def failover(self, failed_region):
        return min(self.regions,
            key=lambda r: r.distance_to(failed_region.location)
        )
```

## Q89: Design a `GraphQL` API gateway for client efficiency.

**A:** A GraphQL gateway provides a single endpoint that clients query with a schema-defined query language, fetching exactly the data they need. Core entities: `Schema` (types, queries, mutations, subscriptions), `Resolver` (resolves field data from backend services), `DataLoader` (batches and caches database queries), and `Gateway` (routes queries to backend services).

The gateway composes a unified schema from multiple backend services. Each service contributes its types and resolvers. The `SchemaStitcher` or `Federation` (Apollo Federation) merges schemas. A query like `{ user(id: 1) { name, orders { total } } }` resolves the user from the User service and orders from the Order service, executing them in parallel.

Design considerations include: N+1 query problem (the DataLoader pattern batches database calls — if 10 users are queried, batch into one SQL query), query complexity analysis (prevent expensive queries by scoring field depth and cost), persisted queries (pre-registered queries to prevent arbitrary query injection), and response caching (cache at the field level based on arguments). The `GraphQLGateway` handles authentication, rate limiting (per-query complexity), and schema validation.

**Example:**
```python
import graphene

class User(graphene.ObjectType):
    name = graphene.String()
    orders = graphene.List(lambda: Order)

    def resolve_orders(self, info):
        return info.context["order_loader"].load(self.id)

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())

    def resolve_user(self, info, id):
        return info.context["user_loader"].load(id)
```

## Q90: Design a `Real-time Analytics` pipeline for clickstream data.

**A:** A RealTimeAnalytics pipeline processes user clickstream events in real-time for dashboards, recommendations, and alerting. Core entities: `ClickEvent` (userId, sessionId, page, action, timestamp, metadata), `StreamProcessor` (windowed aggregations, joins), `MaterializedView` (pre-aggregated results), and `AnalyticsAPI` (serves queries against materialized views).

The pipeline: browser/app sends click events → Kafka receives events → Flink/Spark Streaming processes events (windowed aggregations: active users per minute, page views per session) → materialized views updated in real-time → dashboard queries materialized views. The `StreamProcessor` handles: session windowing (group events by session with 30-minute inactivity gap), tumbling windows (count events per 5-minute window), and sliding windows (average over last 10 minutes).

Design considerations include: event ordering (events may arrive out of order — use watermarks to handle late events), exactly-once processing (Flink's checkpointing), late data handling (allowed lateness window), and backpressure (when processing can't keep up with ingestion). The `MaterializedView` stores pre-computed aggregations for fast queries: `active_users_last_hour`, `top_pages_last_day`, `conversion_funnel`. The `AlertService` evaluates rules against real-time metrics.

**Example:**
```python
class StreamProcessor:
    def __init__(self, kafka_consumer):
        self.consumer = kafka_consumer
        self.windows = defaultdict(list)

    def process(self, event):
        window_key = self.get_window_key(event)
        self.windows[window_key].append(event)
        if self.is_window_complete(window_key):
            self.emit_aggregation(window_key)

    def emit_aggregation(self, window_key):
        events = self.windows.pop(window_key)
        unique_users = len(set(e.user_id for e in events))
        self.materialized_view.update(window_key, unique_users)
```

## Q91: Design a `Service Catalog` for organizational service management.

**A:** A ServiceCatalog is a centralized registry of all microservices, their owners, dependencies, and documentation. Core entities: `ServiceEntry` (name, description, owner, team, tier, dependencies, APIs), `APIspec` (OpenAPI schema, version, endpoints), `Owner` (team, Slack channel, on-call rotation), and `Dependency` (upstream/downstream services, SLA). The catalog enables teams to discover, understand, and operate services.

The catalog provides: service discovery (find services by name, capability, team), dependency visualization (see which services depend on which), API documentation (auto-generated from OpenAPI specs), and operational metadata (runbooks, dashboards, alerts linked to each service). The `CatalogService` aggregates data from multiple sources: source code repos (language, framework), CI/CD (build status, deployment frequency), monitoring (SLO dashbooks, alert definitions), and documentation (README, API specs).

Design considerations include: self-service registration (teams register their own services via UI or YAML config), freshness (auto-detect new services from deployment pipelines), integration with other tools (PagerDuty for on-call, Datadog for monitoring, GitHub for source), and quality gates (services must have documentation, API spec, and on-call to be marked "certified"). The `ServiceScorecard` rates services on operational maturity (documentation, testing, monitoring, incident response).

**Example:**
```python
class ServiceCatalog:
    def __init__(self):
        self.services = {}

    def register(self, service):
        self.services[service.name] = service
        self.validate_requirements(service)

    def find_by_capability(self, capability):
        return [s for s in self.services.values()
                if capability in s.tags]

    def get_dependency_graph(self, service_name):
        visited = set()
        graph = {}
        self._dfs(service_name, graph, visited)
        return graph
```

## Q92: Design an `Incident Management` system.

**A:** An IncidentManagement system tracks incidents from detection through resolution. Core entities: `Incident` (severity, status, affected services, timeline, responders), `IncidentCommander` (person leading response), `Timeline` (events, actions, status changes), `Runbook` (step-by-step resolution procedures), and `PostMortem` (root cause analysis, action items).

The incident lifecycle: Detection (alert fires or user reports) → Triage (assess severity, assign commander) → Mitigation (restore service — work around the problem) → Resolution (fix the root cause) → Post-mortem (analyze and prevent recurrence). The `IncidentService` manages state transitions and notifications. Severity levels: SEV1 (critical, customer-facing, all hands), SEV2 (degraded experience), SEV3 (minor, non-urgent).

Design considerations include: automated runbooks (playbooks that execute automatically — restart service, scale up, failover), status page updates (public-facing status page updated by the incident system), communication channels (dedicated Slack/Teams channel per incident), and metrics (MTTD — mean time to detect, MTTA — mean time to acknowledge, MTTR — mean time to resolve). The `PostMortemTemplate` ensures consistent blameless post-mortems. The `ActionItemTracker` follows up on prevention measures.

**Example:**
```python
class Incident:
    def __init__(self, title, severity, affected_services):
        self.title = title
        self.severity = severity
        self.status = "open"
        self.timeline = []
        self.commander = None
        self.created_at = datetime.now()

    def acknowledge(self, commander):
        self.commander = commander
        self.status = "acknowledged"
        self.timeline.append(Event("acknowledged", commander))

    def mitigate(self, action):
        self.timeline.append(Event("mitigated", action))
        self.status = "mitigated"

    def resolve(self, root_cause):
        self.timeline.append(Event("resolved", root_cause))
        self.status = "resolved"
```

## Q93: Design a `Billing Metering` system for usage-based pricing.

**A:** A BillingMetering system tracks resource usage and generates bills based on consumption. Core entities: `MeterEvent` (tenantId, metric, quantity, timestamp), `AggregationWindow` (hourly/daily rollups), `RatePlan` (metric → price mapping), `Invoice` (line items, total, status), and `MeteringService` (collects, aggregates, and bills).

The metering pipeline: services emit meter events (API calls, storage GB, compute hours) → Kafka receives events → Flink aggregates by tenant and metric (hourly rollups) → billing service applies rates from the rate plan → generates invoices. The `RatePlan` supports tiered pricing (first 1000 calls free, $0.01 per call after), volume discounts, and flat-rate tiers.

Design considerations include: high-throughput ingestion (millions of events per minute — use Kafka + Flink), idempotent event processing (exactly-once semantics for accurate billing), backfill (reprocess historical meter data for corrections), and grace periods (allow a buffer before finalizing invoices). The `UsageDashboard` shows real-time consumption so customers can monitor their spending. The `InvoiceService` generates PDF invoices and handles payment collection.

**Example:**
```python
class MeteringService:
    def __init__(self, kafka_producer, aggregation_store):
        self.producer = kafka_producer
        self.store = aggregation_store

    def record_usage(self, tenant_id, metric, quantity):
        event = MeterEvent(tenant_id, metric, quantity, datetime.utcnow())
        self.producer.send("meter-events", event)

    def aggregate_hourly(self, tenant_id, metric, hour):
        total = self.store.sum(tenant_id, metric, hour, hour + timedelta(hours=1))
        rate = self.rate_plan.get_rate(metric, total)
        return total * rate
```

## Q94: Design a `Data Masking` system for PII protection.

**A:** A DataMasking system protects sensitive data (PII) by replacing or obfuscating sensitive fields. Core entities: `MaskingRule` (field pattern, masking strategy), `MaskingStrategy` (hash, redact, tokenize, partial mask), `SensitiveField` (PII classification: name, email, SSN, credit card), and `MaskingService` (applies rules to data). The system ensures PII is not exposed in logs, test environments, or unauthorized views.

Masking strategies: full redact (`***`), partial mask (show last 4 digits of SSN: `***-**-1234`), tokenization (replace with a non-reversible token that can be mapped back via a secure vault), hashing (SHA-256 with salt — consistent but non-reversible), and shuffling (randomize characters while maintaining format). The strategy depends on the use case: test environments use tokenization (can be detokenized), logs use redaction (irreversible), analytics use hashing (consistent for grouping).

The `DataClassifier` automatically detects PII fields using patterns (regex for email, SSN, credit card), NLP models (detect names in free text), and metadata (column names like `email`, `phone`). The `MaskingPipeline` applies rules as data flows through the system: database → ETL → data warehouse. The `MaskingPolicy` is configurable per environment (production: no masking, staging: tokenization, development: full redact).

**Example:**
```python
import hashlib
import re

class DataMasker:
    def __init__(self):
        self.strategies = {
            "email": self.mask_email,
            "ssn": self.mask_ssn,
            "credit_card": self.mask_credit_card,
        }

    def mask(self, field_type, value):
        return self.strategies[field_type](value)

    def mask_email(self, email):
        name, domain = email.split("@")
        return f"{name[0]}***@{domain}"

    def mask_ssn(self, ssn):
        return f"***-**-{ssn[-4:]}"
```

## Q95: Design a `Service Level Agreement` (SLA) monitoring system.

**A:** An SLAMonitoring system tracks service availability and performance against defined SLAs. Core entities: `SLA` (target: 99.9% availability, p99 latency < 200ms), `SLABudget` (allowed downtime per period: 99.9% = 8.76 hours/year), `ErrorBudget` (remaining tolerance for failures), and `SLAReport` (current status, historical trends). The system alerts when error budgets are being consumed too quickly.

The SLA calculation: availability = (total time - downtime) / total time. Downtime is detected by health checks, synthetic monitoring, or user-reported errors. The `SLACalculator` computes rolling availability windows (daily, weekly, monthly, yearly). The `ErrorBudgetBurnRate` tracks how fast the error budget is being consumed — if the burn rate exceeds 2x, the team must prioritize reliability over features.

Design considerations include: composite SLAs (overall availability = product of component availabilities), multi-signal SLAs (combine availability, latency, and error rate into a single SLI), and historical tracking (SLA compliance over time for executive reporting). The `SLADashboard` shows real-time SLA status with burn-down charts. The `PagerDuty` integration alerts when the error budget is critically low. The `SLAReport` is generated monthly for customer-facing SLA compliance.

**Example:**
```python
class SLAMonitor:
    def __init__(self, target_availability=0.999):
        self.target = target_availability
        self.total_time = 0
        self.downtime = 0

    def record_outage(self, duration_seconds):
        self.downtime += duration_seconds

    def record_healthy(self, duration_seconds):
        self.total_time += duration_seconds

    def current_availability(self):
        if self.total_time == 0:
            return 1.0
        return 1 - (self.downtime / self.total_time)

    def error_budget_remaining(self):
        allowed_downtime = self.total_time * (1 - self.target)
        return max(0, allowed_downtime - self.downtime)
```

## Q96: Design a `Configuration as Code` pipeline for infrastructure.

**A:** A ConfigurationAsCode pipeline manages infrastructure through version-controlled configuration files. Core entities: `ConfigFile` (Terraform/CloudFormation/Kubernetes YAML), `Pipeline` (validate → plan → apply), `StateStore` (tracks current infrastructure state), and `DriftDetector` (detects manual changes). The pipeline ensures infrastructure changes are reviewed, tested, and auditable.

The workflow: developer commits config change → PR triggers validation (syntax check, linting, security scanning) → plan phase shows what will change → PR approved → merge triggers apply phase → infrastructure updated → state updated. The `StateStore` (Terraform state in S3, Kubernetes etcd) tracks the current state to calculate diffs. The `DriftDetector` periodically compares actual infrastructure with declared config and alerts on drift.

Design considerations include: state locking (prevent concurrent applies — use DynamoDB locks), import (bring existing resources under management), destroy (safely remove resources), and policy enforcement (OPA/Conftest validates configs against organizational policies). The `ConfigValidator` checks for security issues (public S3 buckets, overly permissive IAM), cost estimation (Infracost shows cost impact before applying), and compliance (HIPAA, SOC2 checks).

**Example:**
```hcl
# Terraform example
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  tags = {
    Name = "web-server"
    Environment = "production"
  }
}

# Drift detection
data "aws_instances" "current" {
  filter {
    name   = "tag:ManagedBy"
    values = ["terraform"]
  }
}
```

## Q97: Design a `Tech Debt Tracking` system for engineering teams.

**A:** A TechDebtTracking system identifies, categorizes, and prioritizes technical debt. Core entities: `TechDebtItem` (description, category, impact, effort, age, owner), `Category` (code quality, architecture, dependencies, testing, documentation), `Impact` (developer productivity, reliability, security risk), and `DebtScore` (composite priority score). The system makes invisible debt visible and tracks progress.

The `DebtDiscovery` identifies debt through: static analysis (code smells, complexity metrics), dependency scanning (outdated packages with known vulnerabilities), test coverage analysis (uncovered code paths), and manual tagging (developers flag debt during code review). Each item gets a `DebtScore` = impact × age / effort (high impact + old + easy to fix = highest priority).

Design considerations include: integration with existing tools (SonarQube for code quality, Snyk for dependencies, GitHub Issues for tracking), automated detection (CI pipeline flags new debt), and reporting (engineering leaders see debt trends, teams see their debt backlog). The `DebtPaydown` plan allocates sprint capacity to debt reduction (e.g., 20% of sprint capacity). The `DebtDashboard` visualizes total debt, category distribution, and trend over time.

**Example:**
```python
class TechDebtItem:
    def __init__(self, description, category, impact, effort_estimate):
        self.description = description
        self.category = category
        self.impact = impact
        self.effort = effort_estimate
        self.created_at = datetime.now()
        self.status = "open"

    @property
    def debt_score(self):
        age_days = (datetime.now() - self.created_at).days
        return (self.impact * age_days) / self.effort

class DebtTracker:
    def prioritize(self):
        return sorted(self.items, key=lambda i: i.debt_score, reverse=True)
```

## Q98: Design a `Chaos Monkey`-style resilience testing tool.

**A:** A ChaosMonkey randomly terminates instances, introduces latency, and injects failures to ensure services are resilient. Core entities: `ChaosGroup` (group of instances to target), `FaultType` (terminate, latency, CPU stress, disk fill), `Schedule` (when to run: business hours, maintenance window), and `SafetyCheck` (ensure minimum capacity is maintained).

The ChaosMonkey runs on a schedule: select a random instance from the target group → verify safety (at least N healthy instances remain) → inject fault → observe recovery → report results. The `SafetyCheck` is critical: never take down the last healthy instance in a region, never take down more than X% of instances simultaneously, and respect minimum capacity guarantees.

Design considerations include: configurable blast radius (percentage of instances to target), opt-out for critical services, automated rollback (if recovery fails, restore the instance), and comprehensive logging (every fault injection is logged for post-mortem analysis). The `ChaosDashboard` shows active experiments, historical results, and resilience scores per service. The `GameDay` feature allows coordinated chaos experiments across multiple services.

**Example:**
```python
import random

class ChaosMonkey:
    def __init__(self, instance_group, safety_checker):
        self.group = instance_group
        self.safety = safety_checker

    def run(self, config):
        instances = self.group.get_healthy_instances()
        target_count = max(1, len(instances) * config.percentage // 100)
        targets = random.sample(instances, target_count)

        for instance in targets:
            if not self.safety.can_terminate(instance):
                continue
            self.inject_fault(instance, config.fault_type)
            self.observe_recovery(instance)

    def inject_fault(self, instance, fault_type):
        if fault_type == "terminate":
            instance.terminate()
        elif fault_type == "latency":
            instance.add_network_latency(config.latency_ms)
```

## Q99: Design a `Service Dependency Graph` visualization system.

**A:** A ServiceDependencyGraph maps and visualizes relationships between microservices. Core entities: `Node` (service, version, health, metrics), `Edge` (caller → callee, call frequency, latency, error rate), `Graph` (nodes + edges), and `GraphService` (builds, queries, and visualizes the graph). The graph is built from telemetry data (distributed traces, service mesh metrics).

The graph construction: distributed traces record service-to-service calls. The `TraceAnalyzer` extracts caller-callee pairs and aggregates metrics: call count, error rate, latency percentiles. The `GraphBuilder` constructs the dependency graph from aggregated traces. Alternatively, service mesh (Istio) provides real-time traffic data without instrumentation.

The visualization shows: service nodes (colored by health — green/yellow/red), dependency edges (thickness proportional to traffic volume), and drill-down (click a service to see its details, metrics, and runbooks). The `GraphService` supports: dependency impact analysis (if service X fails, which downstream services are affected?), blast radius calculation (how many users are impacted?), and path finding (shortest path between two services for debugging latency). The `AnomalyDetector` highlights unusual patterns (sudden increase in error rate on a specific edge).

**Example:**
```python
class DependencyGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(lambda: {"count": 0, "errors": 0, "latency_sum": 0})

    def record_call(self, caller, callee, latency_ms, is_error):
        self.edges[(caller, callee)]["count"] += 1
        self.edges[(caller, callee)]["latency_sum"] += latency_ms
        if is_error:
            self.edges[(caller, callee)]["errors"] += 1

    def get_impact(self, service):
        affected = set()
        queue = [service]
        while queue:
            current = queue.pop(0)
            for (caller, callee) in self.edges:
                if caller == current and callee not in affected:
                    affected.add(callee)
                    queue.append(callee)
        return affected
```

## Q100: Design a `Production Readiness Review` checklist system.

**A:** A ProductionReadinessReview (PRR) system ensures services meet operational standards before deployment. Core entities: `Checklist` (categories and items), `CheckItem` (question, owner, automated: yes/no, evidence), `Review` (service, reviewer, results, approval), and `ReadinessScore` (percentage of checks passing). The system enforces standards for monitoring, alerting, documentation, security, and disaster recovery.

The PRR checklist covers: Observability (logs, metrics, dashboards configured), Alerting (critical alerts with runbooks), Documentation (API docs, architecture diagram, runbook), Security (authentication, authorization, encryption, secrets management), Reliability (backup/restore tested, failover tested, SLA defined), and Capacity (load tested, auto-scaling configured, cost estimated). Each item has a definition of done and evidence requirements.

Design considerations include: automation (automated checks for metrics coverage, alert existence, test coverage), progressive enforcement (new services must pass PRR before going to production, existing services get a grace period), and integration (PRR gate in CI/CD pipeline — deployment blocked if PRR fails). The `PRRDashboard` shows readiness scores per service, highlights gaps, and tracks improvement over time. The `PRRReviewer` workflow: service owner fills evidence → reviewer verifies → approval required for deployment.

**Example:**
```python
class PRRChecklist:
    def __init__(self):
        self.categories = {
            "observability": [
                CheckItem("Metrics endpoint exposed", automated=True),
                CheckItem("Dashboard created in Grafana", automated=False),
                CheckItem("Structured logging enabled", automated=True),
            ],
            "alerting": [
                CheckItem("Critical alerts configured", automated=True),
                CheckItem("Alert has runbook link", automated=False),
                CheckItem("PagerDuty service created", automated=True),
            ],
            "security": [
                CheckItem("Authentication enabled", automated=True),
                CheckItem("Secrets not in code", automated=True),
                CheckItem("HTTPS enforced", automated=True),
            ],
        }

    def evaluate(self, service):
        results = {}
        for category, items in self.categories.items():
            results[category] = [item.check(service) for item in items]
        return ReadinessScore(results)
```
