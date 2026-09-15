# Repository, Unit of Work and Service Patterns — 100 Interview Q&A

## Q1: What is the Repository pattern?

**A:** The Repository pattern mediates between the domain and data mapping layers, acting as an in-memory collection of domain objects. It provides an abstraction that decouples the business logic from the persistence mechanism, allowing the service layer to retrieve and persist domain objects without knowing whether they reside in a relational database, NoSQL store, or file system.

Repositories typically expose methods like `find_by_id()`, `find_all()`, `save()`, and `delete()`. They encapsulate query logic, connection management, and ORM interactions. The service layer interacts with repositories through interfaces, enabling easy substitution of persistence implementations and simplified unit testing through mocking.

The pattern was formalized by Eric Evans in Domain-Driven Design as one of the strategic patterns for managing data access. It creates a clean boundary between the domain model and the infrastructure layer, ensuring that business logic remains independent of persistence concerns.

**Example:**
```python
from abc import ABC, abstractmethod
from typing import List, Optional


class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def find_all(self) -> List[User]: ...

    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def delete(self, user_id: int) -> None: ...


class PostgresUserRepository(UserRepository):
    def __init__(self, db_connection):
        self.db = db_connection

    def find_by_id(self, user_id):
        row = self.db.execute(
            "SELECT * FROM users WHERE id = %s", (user_id,)
        )
        return User(row["id"], row["name"], row["email"]) if row else None

    def find_all(self):
        rows = self.db.execute("SELECT * FROM users")
        return [User(r["id"], r["name"], r["email"]) for r in rows]

    def save(self, user):
        self.db.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (user.name, user.email),
        )
        return user

    def delete(self, user_id):
        self.db.execute("DELETE FROM users WHERE id = %s", (user_id,))
```

## Q2: What is the Unit of Work pattern?

**A:** The Unit of Work pattern maintains a list of objects affected by a business transaction and coordinates the writing of changes and the resolution of concurrency problems. It ensures that all changes to objects within a transaction are committed as a single atomic unit.

Without Unit of Work, each repository method might independently commit changes, leading to partial updates if an error occurs midway through a transaction. The Unit of Work collects all changes (inserts, updates, deletes) during a business operation and flushes them to the database in a single transaction when the operation completes.

The Unit of Work also tracks the state of objects — new, modified, unchanged, or deleted. When `commit()` is called, it only persists objects that have actually changed, optimizing database operations. This tracking eliminates redundant database writes and ensures data consistency.

## Q3: What is the difference between Repository and Data Access Object (DAO)?

**A:** A Repository works with domain objects and provides collection-like semantics — `find()`, `save()`, `delete()` operations that mirror working with an in-memory collection. A DAO works with database tables and provides CRUD operations on individual records, often working with data structures rather than domain objects.

Repositories are domain-centric: they understand aggregate roots, enforce business invariants, and return rich domain objects. DAOs are persistence-centric: they execute SQL queries, manage connections, and return flat data structures. A Repository may internally use one or more DAOs to access the database.

The Repository pattern is preferred when working with Domain-Driven Design because it maintains a clean boundary between the domain and persistence layers. DAOs are simpler and more appropriate for applications that do not use a rich domain model.

## Q4: What is an Aggregate Root?

**A:** An Aggregate Root is the primary entity of a domain Aggregate — a cluster of associated objects treated as a single unit for data changes. All external access to the Aggregate goes through the Root, which ensures that all invariants and business rules within the Aggregate are maintained.

For example, an Order Aggregate might contain the Order (Root), OrderItems, and ShippingAddress. You cannot modify an OrderItem directly — you must go through the Order. The Order ensures that the total is recalculated when items are added, that the item count does not exceed limits, and that the shipping address is valid.

Repository interfaces are defined per Aggregate Root. The `OrderRepository` saves and retrieves entire Order Aggregates, including all contained OrderItems and the ShippingAddress. This ensures that the Aggregate is always in a consistent state when loaded from the database.

**Example:**
```python
class OrderItem:
    def __init__(self, product_id, quantity, price):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    @property
    def subtotal(self):
        return self.quantity * self.price


class Order:
    def __init__(self, order_id, customer_id):
        self.id = order_id
        self.customer_id = customer_id
        self._items = []
        self._status = "draft"

    def add_item(self, product_id, quantity, price):
        if self._status != "draft":
            raise ValueError("Cannot modify a confirmed order")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._items.append(OrderItem(product_id, quantity, price))

    def confirm(self):
        if not self._items:
            raise ValueError("Cannot confirm empty order")
        self._status = "confirmed"

    @property
    def total(self):
        return sum(item.subtotal for item in self._items)

    @property
    def items(self):
        return list(self._items)


class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id) -> Order: ...

    @abstractmethod
    def save(self, order: Order) -> None: ...
```

## Q5: What is the difference between Repository and Service?

**A:** A Repository is responsible for data access — retrieving and persisting domain objects. A Service contains business logic and orchestrates operations that may involve multiple Repositories or domain objects.

A Repository answers "how do I get and save data?" while a Service answers "what business operation should I perform?" The Service calls the Repository to load domain objects, performs business operations on them, and then calls the Repository to save the results.

For example, a `TransferService` might load two `Account` objects from the `AccountRepository`, call `Account.debit()` and `Account.credit()` methods, and then save both accounts through the Repository. The Service orchestrates the business operation while the Repository handles persistence.

## Q6: What is the difference between Active Record and Repository pattern?

**A:** In Active Record, the domain object itself contains persistence logic — methods like `save()`, `find()`, and `delete()` are defined on the domain class. The domain object knows how to persist itself, typically mapping to a single database table.

In the Repository pattern, persistence logic is separated from the domain object into dedicated Repository classes. Domain objects are pure domain concepts with no persistence awareness. Repository classes handle all data access concerns.

Active Record is simpler to implement and works well for straightforward CRUD applications. The Repository pattern is more suitable for complex domains because it separates concerns more cleanly. Active Record can lead to domain objects that are tightly coupled to the database schema, while the Repository pattern allows the domain model to evolve independently.

## Q7: What is the Repository pattern's support for CQRS?

**A:** CQRS (Command Query Responsibility Segregation) separates read and write operations. Repositories naturally support this by having separate read repositories (query side) and write repositories (command side). The write repository handles persistence through the Unit of Work, while the read repository returns optimized read models.

The write repository works with rich domain objects and enforces business invariants. The read repository returns flat DTOs or projection objects that are optimized for display, avoiding the overhead of loading entire aggregate graphs.

This separation allows independent optimization of read and write paths. Read repositories can use denormalized views, caching, and optimized queries. Write repositories focus on transactional consistency and business rule enforcement.

## Q8: What is the difference between Repository and Gateway?

**A:** A Repository abstracts data access for a specific domain aggregate, providing a collection-like interface for domain objects. A Gateway abstracts access to an external system or service, providing a simplified interface for complex external APIs.

Repositories are domain-centric and work with domain objects. Gateways are system-centric and work with external system data formats. A Repository abstracts the persistence mechanism, while a Gateway abstracts the communication protocol and API of an external service.

For example, a `PaymentGateway` might abstract the Stripe API, providing a simple `charge()` method that handles HTTP communication, authentication, error handling, and response parsing. A `PaymentRepository` might persist payment records to a database. Both abstract external concerns but at different levels.

## Q9: How does the Repository pattern support testing?

**A:** The Repository pattern is ideal for testing because it provides an interface that can be easily mocked. Service classes that depend on Repository interfaces can be tested by creating mock repositories that return predefined test data. This eliminates the need for a real database during unit testing.

In test setup, a mock repository is created and configured to return specific data. The service under test receives this mock through dependency injection, and the test verifies that the service correctly processes the data without any database interaction.

This approach makes unit tests fast (no database queries), deterministic (same input produces same output), and isolated (no external dependencies). Integration tests can verify the actual Repository implementation against a real database.

**Example:**
```python
from unittest.mock import Mock, spec


class TestOrderService:
    def setup_method(self):
        self.order_repo = Mock(spec=OrderRepository)
        self.service = OrderService(self.order_repo)

    def test_confirm_order(self):
        order = Order(1, 100)
        order.add_item(1, 2, 29.99)
        self.order_repo.find_by_id.return_value = order

        self.service.confirm_order(1)

        self.order_repo.save.assert_called_once_with(order)
        assert order._status == "confirmed"

    def test_confirm_empty_order_fails(self):
        order = Order(1, 100)
        self.order_repo.find_by_id.return_value = order

        with pytest.raises(ValueError, match="empty order"):
            self.service.confirm_order(1)
```

## Q10: What is the difference between optimistic and pessimistic locking in Repositories?

**A:** Pessimistic locking acquires a database lock when reading data and holds it until the transaction completes. Other transactions must wait for the lock to be released before they can read or modify the same data. This prevents conflicts but reduces concurrency.

Optimistic locking does not acquire locks during reads. Instead, it checks for conflicts at commit time using a version number or timestamp. If another transaction has modified the same data since it was read, the current transaction is rolled back and can be retried.

Optimistic locking is preferred when conflicts are rare and read performance is important. Pessimistic locking is necessary when conflicts are frequent or when the cost of retrying is high. Most ORM frameworks (Hibernate, Entity Framework) support both approaches through version columns or row-level locking.

## Q11: What is the specification pattern's relationship with Repositories?

**A:** The Specification pattern encapsulates business rules as composable objects that can be combined using logical operators. In the context of Repositories, Specifications define query criteria in a domain-friendly way without leaking persistence-specific syntax.

Instead of repository methods like `find_active_premium_users_created_after(date)`, you create Specifications: `IsActiveSpecification`, `IsPremiumSpecification`, `CreatedAfterSpecification`. These can be combined: `IsActive AND IsPremium AND CreatedAfter(date)`.

This approach keeps the Repository interface clean and the query logic reusable. Specifications can be used across different Repositories and composed dynamically based on user input. They eliminate the "query method explosion" problem where Repositories accumulate increasingly specific query methods.

## Q12: What is the Repository pattern's limitation with complex queries?

**A:** Repositories struggle with complex queries that span multiple aggregates or require database-specific features like window functions, CTEs, or full-text search. The Repository abstraction can become bloated with query methods that are specific to certain use cases, violating the interface segregation principle.

When queries become too complex for the Repository abstraction, developers face a choice: add more methods to the Repository interface (making it a "leaky abstraction") or bypass the Repository and access the database directly (breaking the abstraction).

The solution is often to use a Query Service or Query Object pattern for complex reads, while keeping the Repository for simple CRUD operations on aggregates. This aligns with CQRS, where complex reads are handled by specialized query services.

## Q13: What is the difference between Repository and Collection pattern?

**A:** The Collection pattern (as described by Eric Evans) provides collection-like semantics for accessing domain objects: `add()`, `remove()`, `find()`. It is essentially the same as the Repository pattern but emphasizes the collection metaphor more strongly.

The Repository pattern is a specialization of the Collection pattern that works across persistence boundaries. A local collection lives in memory; a Repository might query a remote database. The Repository's `find()` method might execute SQL, call an API, or read from a file, while a collection's `find()` searches in-memory data.

In practice, the terms are often used interchangeably. The Repository pattern is more commonly used in enterprise applications with database persistence, while the Collection pattern is more commonly used in domain-driven design literature.

## Q14: What is the Unit of Work's dirty checking mechanism?

**A:** Dirty checking is the mechanism by which the Unit of Work detects which objects have been modified since they were loaded from the database. When an object is loaded, the Unit of Work stores a snapshot of its state. When `commit()` is called, the Unit of Work compares the current state with the snapshot to determine what has changed.

Dirty checking can be implemented through snapshot comparison (storing a copy of the original state), property-level tracking (each property tracks whether it has changed), or ORM-managed change detection (the ORM framework tracks changes automatically).

NHibernate and Hibernate use snapshot-based dirty checking. Entity Framework uses property-level tracking through `ChangeTracker`. ActiveRecord frameworks typically use explicit change detection where the developer marks objects as dirty.

## Q15: What is the difference between Repository and Query Object?

**A:** A Repository provides generic CRUD operations and simple queries for a specific aggregate. A Query Object encapsulates complex query logic as a first-class object that can be constructed, combined, and executed against the database.

The Query Object pattern is useful when queries are complex, dynamic, or need to be composed at runtime. Instead of adding query methods to the Repository, you create Query Objects that encapsulate the query logic. The Repository or a Query Service executes the Query Object against the database.

Query Objects are particularly useful in CQRS architectures where the read side needs complex, optimized queries. They can be composed using a fluent API, combined with Specifications, and executed against the read database.

## Q16: How does the Repository pattern handle soft deletes?

**A:** Soft delete marks records as deleted without physically removing them from the database. The Repository implements soft delete by setting a `deleted_at` timestamp or `is_deleted` flag instead of executing a `DELETE` statement. Subsequent queries filter out soft-deleted records.

The Repository interface provides a `delete()` method that internally performs an update (setting the flag) rather than a physical delete. All query methods (`find_by_id()`, `find_all()`) include a filter to exclude soft-deleted records.

This approach preserves data for audit trails, allows recovery of accidentally deleted records, and maintains referential integrity when foreign keys reference the deleted record. The Repository abstracts this behavior so the service layer does not need to know whether records are physically or logically deleted.

**Example:**
```python
from datetime import datetime
from typing import List, Optional


class SoftDeleteUserRepository(UserRepository):
    def __init__(self, db):
        self.db = db

    def find_by_id(self, user_id: int) -> Optional[User]:
        row = self.db.execute(
            "SELECT * FROM users WHERE id = %s AND deleted_at IS NULL",
            (user_id,),
        )
        return User(row["id"], row["name"], row["email"]) if row else None

    def find_all(self) -> List[User]:
        rows = self.db.execute(
            "SELECT * FROM users WHERE deleted_at IS NULL"
        )
        return [User(r["id"], r["name"], r["email"]) for r in rows]

    def delete(self, user_id: int) -> None:
        self.db.execute(
            "UPDATE users SET deleted_at = %s WHERE id = %s",
            (datetime.now(), user_id),
        )

    def restore(self, user_id: int) -> None:
        self.db.execute(
            "UPDATE users SET deleted_at = NULL WHERE id = %s",
            (user_id,),
        )
```

## Q17: What is the difference between Repository and Data Mapper?

**A:** The Data Mapper is a layer of software that transfers data between objects and the database while keeping them independent. It maps between in-memory objects and database rows, handling type conversions, relationship management, and query translation.

The Repository pattern uses Data Mappers internally. The Repository provides the domain-level interface (`find_by_id()`, `save()`), while the Data Mapper handles the actual translation between domain objects and database rows.

In ORM frameworks like Hibernate or Entity Framework, the Data Mapper is the ORM itself. The Repository wraps the ORM and provides a cleaner interface for the domain layer. The Repository is a domain-level abstraction; the Data Mapper is a persistence-level mechanism.

## Q18: What is the Unit of Work's role in transaction management?

**A:** The Unit of Work defines the scope of a database transaction. When `commit()` is called, the Unit of Work begins a transaction, flushes all pending changes to the database, and commits the transaction. If any operation fails, the transaction is rolled back, ensuring atomicity.

This ensures that all changes within a business operation are committed atomically. If an Order and its OrderItems are being saved, both must succeed or both must be rolled back. Without Unit of Work, each save operation might commit independently, leading to inconsistent state.

The Unit of Work also manages nested transactions and savepoints in complex scenarios. It tracks the transaction hierarchy and ensures correct commit and rollback behavior across nested operations.

## Q19: What is the difference between Repository and Query Builder?

**A:** A Repository provides domain-level operations for a specific aggregate. A Query Builder provides a fluent API for constructing database queries without being tied to a specific domain concept.

Query Builders are persistence-focused and work with table and column names. Repositories are domain-focused and work with entity and property names. A Repository might use a Query Builder internally to construct complex queries.

For example, Laravel's Eloquent provides both — the Repository provides `find()`, `save()`, and `delete()` for domain objects, while the Query Builder provides `select()`, `where()`, `join()` for constructing raw queries. The Repository is preferred for simple operations; the Query Builder is used for complex queries.

## Q20: What is the Mediator pattern's relationship with the Repository pattern?

**A:** The Mediator pattern centralizes complex business operations that involve multiple Repositories. Instead of a Service directly depending on multiple Repositories, the Mediator receives requests and dispatches them to the appropriate handlers, each of which may use specific Repositories.

In CQRS architectures, the Mediator (like MediatR in .NET) dispatches Commands and Queries to their handlers. Command Handlers use write Repositories to persist data, and Query Handlers use read Repositories to retrieve data. The Mediator decouples the Controller from the specific handlers and Repositories.

This reduces coupling between the Controller and the business logic layer. The Controller only depends on the Mediator, not on specific services or Repositories. Each handler is independently testable and replaceable.

## Q21: What is the Generic Repository pattern?

**A:** A Generic Repository provides a base implementation with common CRUD operations for any entity type. Specific repositories inherit from the Generic Repository and add type-specific query methods. This eliminates code duplication across multiple repository implementations.

The Generic Repository defines `find_by_id()`, `find_all()`, `save()`, `delete()`, and other common operations using generics or templates. Specific repositories like `UserRepository` or `OrderRepository` inherit these operations and add custom methods like `find_by_email()` or `find_pending_orders()`.

While convenient, the Generic Repository can become an anti-pattern if overused. It can force a one-size-fits-all approach on repositories that have fundamentally different persistence needs. Some entities may need specialized query logic that does not fit the generic interface.

## Q22: What is the difference between Repository and Unit of Work in terms of scope?

**A:** A Repository operates on individual aggregates or entities — it retrieves and persists one type of domain object. The Unit of Work operates across multiple Repositories, coordinating changes across several aggregates within a single transaction.

A Repository answers "where is my data?" while a Unit of Work answers "how do I commit all my changes atomically?" A single business operation might use multiple Repositories (OrderRepository, InventoryRepository) coordinated by a single Unit of Work that ensures all changes are committed together.

In practice, the Unit of Work is often implemented at the service layer or as a separate infrastructure component. The Repository is implemented per aggregate root and does not manage transaction scope.

## Q23: What is the difference between Repository and Gateway in terms of data format?

**A:** Repositories work with domain objects — the internal representation of business entities. Gateways work with external data formats — the APIs and data structures used by external systems.

A Repository translates between domain objects and database rows using a Data Mapper. A Gateway translates between domain concepts and external API formats using adapters. Both provide abstraction, but at different boundaries.

For example, a `PaymentGateway` might translate between a domain `Payment` object and the Stripe API's JSON format. A `PaymentRepository` might translate between the `Payment` object and a database row. The Gateway handles external communication; the Repository handles internal persistence.

## Q24: What is the Repository pattern's approach to pagination?

**A:** Pagination in the Repository is typically implemented through methods that accept page number and page size parameters. The Repository translates these into database-specific pagination (LIMIT/OFFSET in SQL, skip/limit in MongoDB).

The Repository should return a page of results along with metadata about the total count, current page, and available pages. This metadata is important for the UI to display pagination controls.

Pagination should be handled at the Repository level, not in the service or presentation layers. The service layer should not load all records and then paginate in memory — this defeats the purpose of pagination and wastes resources. The Repository should push pagination down to the database level.

**Example:**
```python
from dataclasses import dataclass
from typing import List, Generic, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: List[T]
    total_count: int
    page_number: int
    page_size: int

    @property
    def total_pages(self):
        return (self.total_count + self.page_size - 1) // self.page_size

    @property
    def has_next(self):
        return self.page_number < self.total_pages

    @property
    def has_previous(self):
        return self.page_number > 1


class PaginatedUserRepository(UserRepository):
    def find_page(self, page: int, size: int) -> Page[User]:
        offset = (page - 1) * size
        total = self.db.execute("SELECT COUNT(*) FROM users")[0]["count"]
        rows = self.db.execute(
            "SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s",
            (size, offset),
        )
        users = [User(r["id"], r["name"], r["email"]) for r in rows]
        return Page(users, total, page, size)
```

## Q25: What is the difference between Repository and Query Service?

**A:** A Repository provides collection-like operations (CRUD) for a specific aggregate. A Query Service provides complex read operations that may span multiple aggregates or return optimized projections.

The Repository is designed for transactional operations — loading aggregates, modifying them, and saving them back. The Query Service is designed for read-heavy operations — complex queries, aggregations, reporting, and search.

In CQRS, the Repository handles the command side (writes), and the Query Service handles the query side (reads). The Query Service can use optimized read models, denormalized views, and caching strategies that are not appropriate for the write side.

The key difference is that the Repository works with domain objects and maintains consistency, while the Query Service works with read models and prioritizes query performance.

## Q26: What is the Service Layer pattern?

**A:** The Service Layer pattern defines an application boundary with a set of available operations and coordinates the application's response to each operation. It encapsulates business logic, transaction management, and orchestration of domain objects and repositories.

A Service Layer provides a uniform interface to the Presentation Layer, hiding the complexity of the business logic. It ensures that business rules are applied consistently, transactions are managed correctly, and security is enforced. Services are typically stateless and receive dependencies through constructor injection.

Services should be distinguished from domain services. Application Services orchestrate use cases (like "place order" or "transfer funds"), while Domain Services contain business logic that does not naturally belong to a single entity (like "calculate shipping cost" based on multiple entities).

## Q27: What is the difference between Application Service and Domain Service?

**A:** Application Services orchestrate use cases — they receive a request, load domain objects through Repositories, invoke domain logic, and persist the results. They are the entry point for business operations from the Presentation Layer.

Domain Services contain business logic that does not naturally belong to any single entity. For example, a `TransferService` that moves money between accounts contains logic that spans multiple Account entities. The transfer rules (overdraft limits, daily limits) are domain logic that does not fit in either Account.

Application Services are infrastructure-aware — they use Repositories, Unit of Work, and may call external services. Domain Services are pure business logic with no infrastructure dependencies. The Application Service delegates to Domain Services for complex business operations.

## Q28: How does the Unit of Work handle concurrency conflicts?

**A:** The Unit of Work detects concurrency conflicts during commit by checking if the data has been modified by another transaction since it was loaded. This is typically done through optimistic concurrency using version numbers or timestamps.

When a conflict is detected, the Unit of Work throws a `ConcurrencyException`. The application can handle this by retrying the operation (reloading data and reapplying changes), informing the user of the conflict, or merging changes manually.

Pessimistic locking prevents conflicts by acquiring locks during data loading. The Unit of Work acquires a lock when loading aggregate data and holds it until the transaction completes. This prevents other transactions from modifying the same data but reduces concurrency.

## Q29: What is the Repository pattern's relationship with ORM frameworks?

**A:** ORM frameworks like Hibernate, Entity Framework, and SQLAlchemy provide built-in Repository-like functionality through their Session/DbContext classes. These classes handle object persistence, change tracking, and query execution. The Repository pattern wraps this ORM functionality to provide a cleaner domain-level interface.

Without the Repository pattern, the Service Layer would depend directly on the ORM's API (Session, DbContext), coupling the business logic to a specific persistence technology. The Repository abstracts the ORM behind an interface, allowing the ORM to be replaced without changing the Service Layer.

In practice, many applications use the ORM's built-in capabilities directly rather than wrapping them in a Repository. This is appropriate for simple applications but becomes problematic in complex domains where the ORM's API leaks into the Service Layer.

## Q30: What is the difference between Repository and Active Record in terms of testability?

**A:** Active Record objects contain persistence logic, making them harder to test in isolation. Unit testing an Active Record object requires a database connection, which makes tests slow and non-deterministic. Integration testing is necessary for most Active Record operations.

Repository-based objects are pure domain objects with no persistence awareness. They can be unit tested without any database connection. Repositories themselves can be tested with integration tests against a real database, while the services that use Repositories can be unit tested with mocks.

The Repository pattern provides a cleaner separation for testing. Service tests are fast unit tests, Repository tests are integration tests, and the domain objects are testable without any infrastructure dependencies.

## Q31: What is the difference between Repository and Data Access Layer?

**A:** The Data Access Layer is a broader architectural concept that encompasses all data access code — connection management, query execution, ORM configuration, and transaction management. The Repository pattern is a specific pattern within the Data Access Layer that provides a domain-level interface.

The Data Access Layer might contain multiple Repositories, Data Mappers, connection factories, query builders, and other data access components. The Repository is the public interface that the Service Layer uses; the Data Access Layer contains the implementation details.

In many applications, the terms are used interchangeably. However, the Data Access Layer is an architectural layer, while the Repository is a design pattern within that layer. A well-designed Data Access Layer exposes its functionality through Repository interfaces.

## Q32: What is the difference between Repository and Gateway in terms of direction?

**A:** A Repository mediates between the domain and the persistence layer — it is an internal abstraction for accessing internal data. A Gateway mediates between the domain and an external system — it is an external-facing abstraction for communicating with external services.

Repositories are part of the application's infrastructure layer and are used by the Service Layer to access internal data. Gateways are adapters that integrate with external APIs, services, or systems. The domain layer depends on Gateway interfaces, not implementations.

The direction of dependency is different: the Service Layer depends on Repository interfaces (dependency inversion), while the domain layer depends on Gateway interfaces (also dependency inversion but at a different layer). Both use interfaces to decouple the domain from infrastructure.

## Q33: What is the Repository pattern's approach to caching?

**A:** Repositories can implement caching at multiple levels. The Repository might maintain an in-memory cache of recently accessed objects, a distributed cache for frequently read data, or a query cache for complex queries.

The caching strategy depends on the data's characteristics. Read-heavy data with infrequent updates benefits from aggressive caching. Write-heavy data with real-time consistency requirements benefits from no caching or write-through caching.

The Repository abstracts the caching behavior from the Service Layer. The Service Layer calls `find_by_id()` without knowing whether the data comes from the database or a cache. The Repository handles cache invalidation, cache warming, and cache consistency internally.

## Q34: What is the difference between Repository and Query Object in terms of complexity?

**A:** A Repository provides simple, pre-defined query methods for common operations. As query requirements become more complex, the Repository accumulates increasingly specific methods, leading to a bloated interface.

A Query Object encapsulates complex query logic as a first-class object. It can be constructed dynamically, combined with other Query Objects, and executed against the database. This keeps the Repository interface clean and the query logic reusable.

For example, instead of adding `find_active_premium_users_created_after_country()` to the Repository, you create a Query Object that combines `IsActive`, `IsPremium`, `CreatedAfter`, and `CountryIs` specifications. This is more flexible and composable.

## Q35: What is the Repository pattern's role in Domain-Driven Design?

**A:** In DDD, the Repository is the mechanism for accessing domain objects from persistent storage. Each Aggregate Root has a corresponding Repository that provides collection-like operations for that Aggregate. The Repository ensures that Aggregates are loaded and saved as complete, consistent units.

Repositories are defined as interfaces in the domain layer and implemented in the infrastructure layer. This follows the Dependency Inversion Principle — the domain depends on abstractions, not implementations. The infrastructure layer provides concrete Repository implementations.

Repositories are one of the building blocks in DDD's tactical patterns. They work alongside Aggregates, Value Objects, Domain Events, and Services to create a rich, behavior-driven domain model that is independent of persistence concerns.

## Q36: What is the difference between Repository and Service Locator?

**A:** A Repository is a domain-level abstraction for data access with a well-defined interface. A Service Locator is an infrastructure mechanism for obtaining dependencies from a central registry. They serve fundamentally different purposes.

The Repository provides collection-like operations for domain objects. The Service Locator provides a global lookup mechanism for services. The Repository is used by the Service Layer for data access; the Service Locator is used by any component that needs to resolve dependencies.

Using a Service Locator to obtain Repository instances is an anti-pattern because it hides dependencies and makes the code harder to test. Constructor injection is preferred, where the Service receives its Repository dependencies through the constructor.

## Q37: What is the Unit of Work's relationship with the Identity Map pattern?

**A:** The Identity Map ensures that each database row is loaded into memory only once within a Unit of Work. When an object is loaded, the Identity Map stores it in a dictionary keyed by its identity. Subsequent loads of the same identity return the cached instance rather than creating a new one.

This prevents inconsistent state within a transaction. Without an Identity Map, loading the same Order twice might return two different in-memory objects with potentially different state. The Identity Map ensures that all code within the Unit of Work works with the same object instance.

The Unit of Work and Identity Map work together: the Unit of Work tracks changes, and the Identity Map ensures object identity. Both are typically implemented by ORM frameworks like Hibernate and Entity Framework.

## Q38: What is the difference between Repository and DAO in terms of abstraction level?

**A:** DAO operates at the database level — it works with tables, rows, and SQL queries. It provides CRUD operations for specific database tables and may return raw data structures or simple data transfer objects.

Repository operates at the domain level — it works with aggregates and entities. It provides collection-like operations for domain objects and may enforce business rules (like ensuring an Aggregate is loaded completely before modification).

DAO is persistence-focused: it abstracts the database technology but does not abstract the persistence model. Repository is domain-focused: it abstracts both the persistence technology and the persistence model, providing a domain-centric view of data access.

## Q39: What is the Repository pattern's approach to batch operations?

**A:** Batch operations are a challenge for the Repository pattern because the standard CRUD interface is designed for individual aggregate operations. Batch inserts, updates, or deletes require either multiple individual Repository calls (which is inefficient) or batch-specific methods on the Repository.

The Repository can provide batch methods like `save_all()`, `delete_all()`, or `bulk_update()`. These methods bypass the standard Unit of Work flow and execute batch operations directly against the database for performance.

The challenge is maintaining consistency between the batch operations and the Unit of Work's change tracking. Batch operations may not trigger Unit of Work events or update the Identity Map. The Repository must handle this consistency carefully.

## Q40: What is the difference between Repository and Data Mapper in terms of responsibility?

**A:** The Data Mapper is responsible for mapping between domain objects and database rows. It handles type conversions, relationship management, and query translation. It is a persistence-level concern.

The Repository is responsible for providing a domain-level interface for data access. It uses the Data Mapper internally but exposes collection-like operations for domain objects. It is a domain-level concern.

The Data Mapper is an implementation detail within the Repository. The Repository uses the Data Mapper to translate between domain objects and database rows, but the Service Layer never interacts with the Data Mapper directly. The Repository abstracts the Data Mapper behind its interface.

## Q41: What is the Repository pattern's handling of relationships?

**A:** Repositories should load complete Aggregates, including all related objects within the Aggregate boundary. For example, an `OrderRepository` should load the Order with all its OrderItems and the associated ShippingAddress.

Relationships outside the Aggregate boundary are loaded lazily or through separate Repository calls. For example, the Order might reference a Customer, but the Customer is a separate Aggregate. The OrderRepository loads the Order, and if the Service needs the Customer, it calls the `CustomerRepository` separately.

This approach ensures that Aggregates are loaded as consistent, complete units while avoiding the N+1 query problem of loading entire object graphs. The Repository boundary aligns with the Aggregate boundary.

## Q42: What is the difference between Repository and Collection in terms of persistence?

**A:** A Collection stores objects in memory with no persistence mechanism. Adding an object to a Collection keeps it in memory until the application terminates. There is no automatic persistence, synchronization, or durability.

A Repository provides the same collection-like interface but persists objects to a durable storage mechanism. Adding an object to a Repository (via `save()`) writes it to the database. Retrieving an object (via `find()`) reads from the database.

The Repository extends the Collection concept across persistence boundaries. The Service Layer works with a Repository as if it were a collection, but the Repository handles the complexity of database access, connection management, and transaction coordination.

## Q43: What is the Unit of Work's role in distributed transactions?

**A:** Distributed transactions span multiple resource managers (databases, message queues, external systems) and require coordination to ensure atomicity across all participants. The Unit of Work can coordinate distributed transactions using protocols like Two-Phase Commit (2PC).

In practice, distributed transactions are expensive and complex. Many modern systems avoid them by using eventual consistency patterns like Sagas instead. The Unit of Work manages local transactions, and coordination across services is handled at a higher level.

When distributed transactions are necessary, the Unit of Work integrates with transaction coordinators (like JTA in Java or System.Transactions in .NET) to ensure that all participants either commit or roll back together.

## Q44: What is the difference between Repository and Specification in terms of scope?

**A:** A Repository provides CRUD operations and basic queries for a specific aggregate. A Specification encapsulates a single business rule or query criterion that can be combined with other Specifications.

The Repository is an infrastructure component that handles data access. The Specification is a domain concept that encapsulates business rules. The Repository might accept Specifications as parameters to filter results, but the Specifications themselves are domain-level objects.

Specifications are composable and reusable across different Repositories. A `IsActiveSpecification` can be used with the `UserRepository`, `OrderRepository`, and `ProductRepository`. The Repository provides the mechanism for executing queries; the Specifications provide the criteria.

## Q45: What is the Repository pattern's handling of inheritance?

**A:** Inheritance in Repositories depends on the inheritance strategy used for domain objects. If domain objects use Single Table Inheritance (STI), a single Repository can handle all subtypes. The Repository queries the discriminator column to determine the subtype and instantiate the correct class.

If domain objects use Table Per Type (TPT) or Table Per Concrete Class (TPC), separate Repositories may be needed for each subtype, or the Repository must perform joins across multiple tables. This complexity is a significant consideration when choosing an inheritance strategy.

The Repository should hide the inheritance implementation details from the Service Layer. The Service Layer calls `find_by_id()` without knowing whether the data comes from one table or multiple tables. The Repository handles the inheritance mapping internally.

## Q46: What is the difference between Repository and DAO in terms of testing impact?

**A:** DAO testing typically requires a database connection because DAOs work directly with database tables. Unit testing a DAO involves setting up an in-memory database, executing SQL, and verifying the results. This is slower and more complex than pure unit testing.

Repository testing can be split into two levels: unit testing services with mocked Repositories (fast, no database) and integration testing Repository implementations against a real database. This separation provides better test coverage with faster test execution.

The Repository pattern's interface-based design makes mocking straightforward. Services that depend on Repository interfaces can be tested with mock implementations, providing fast feedback during development.

## Q47: What is the difference between Repository and CQRS Read Model?

**A:** A Repository provides CRUD operations and works with domain objects. A CQRS Read Model provides optimized read operations and works with projection objects or DTOs designed specifically for display.

The Repository loads complete domain objects with all their relationships and business methods. The Read Model loads minimal data needed for the specific view, avoiding unnecessary joins and data transfer. The Read Model might use denormalized views, materialized views, or pre-computed aggregates.

In CQRS, the write side uses Repositories to load and save domain objects, while the read side uses Read Models to provide optimized queries. The Read Model is updated asynchronously from the write side, potentially with eventual consistency.

## Q48: What is the Repository pattern's approach to soft deletes versus hard deletes?

**A:** Soft deletes mark records as deleted without physically removing them, while hard deletes permanently remove records from the database. The Repository abstracts this choice from the Service Layer — the Service calls `delete()` without knowing whether the record is physically or logically deleted.

Soft deletes preserve data for audit trails, allow recovery, and maintain referential integrity. The Repository implements soft deletes by setting a flag or timestamp and filtering out soft-deleted records in all queries.

Hard deletes are used when data must be permanently removed (regulatory requirements, privacy compliance). The Repository may implement hard deletes for specific entities or provide both options based on configuration. The choice depends on the business requirements and data retention policies.

## Q49: What is the Repository pattern's role in event sourcing?

**A:** In event sourcing, the state of an entity is determined by replaying its event history. The Repository loads events from an event store, replays them to reconstruct the current state, and persists new events when the state changes.

This is a fundamentally different approach from traditional CRUD Repositories that load and save current state. The event-sourced Repository works with events, not entities. It loads events, builds the entity, applies new events, and stores the new events.

Event sourcing Repositories provide additional capabilities like event replay, snapshot management, and event versioning. They are essential for implementing event-sourced architectures and work well with CQRS for separating the read and write sides.

## Q50: What is the difference between Repository and Unit of Work in terms of lifecycle?

**A:** A Repository is typically a long-lived, stateless component registered in the dependency injection container. It is created once and reused across multiple requests. The Repository does not maintain state between operations.

A Unit of Work is typically a short-lived, scoped component that lives for the duration of a single business transaction. It is created when a business operation starts and disposed when the operation completes (commit or rollback).

The lifecycle difference is important for resource management. The Repository can be reused safely because it is stateless. The Unit of Work must be scoped to a transaction to ensure that changes are committed or rolled back correctly. Mixing up the lifecycles can lead to data corruption or resource leaks.

## Q51: What is the Repository pattern's approach to database sharding?

**A:** Database sharding splits data across multiple database instances based on a shard key. The Repository must be aware of the sharding strategy to route queries to the correct shard. This is typically implemented through a ShardedRepository that determines the target shard based on the entity's identity or a shard key.

The sharding logic can be implemented at the Repository level (the Repository selects the correct database connection), at the connection level (a middleware routes queries), or at the ORM level (the ORM handles shard routing transparently).

The challenge is that queries that span multiple shards require scatter-gather operations, which are expensive and complex. The Repository should minimize cross-shard queries by designing shard keys that align with access patterns.

## Q52: What is the difference between Repository and Unit of Work in terms of error handling?

**A:** The Repository handles data access errors — connection failures, query errors, constraint violations. It translates database-specific exceptions into domain-level exceptions that the Service Layer can handle.

The Unit of Work handles transaction errors — commit failures, rollback failures, concurrency conflicts. It ensures that failed transactions are properly cleaned up and that the application state remains consistent.

Both work together in error handling: when a Repository operation fails, the Unit of Work rolls back the entire transaction. When a Unit of Work commit fails, all Repository operations within that Unit of Work are rolled back. This ensures atomicity and consistency.

## Q53: What is the Repository pattern's role in microservices communication?

**A:** In microservices, each service has its own Repository for its data store. Services cannot directly access other services' Repositories — they communicate through APIs. The Repository within each service provides local data access, while inter-service communication uses APIs or message queues.

The Repository pattern helps enforce data ownership in microservices. Each service owns its data and exposes it only through APIs. The Repository abstracts the data store (which might be different for each service) and provides a consistent interface for data access within the service.

When data from multiple services is needed, the service either calls the other service's API or maintains a denormalized copy of the data in its own Repository. The Repository pattern supports both approaches by providing a clean interface for data access.

## Q54: What is the difference between Repository and Read Model in terms of consistency?

**A:** A Repository typically provides strong consistency — when `save()` returns, the data is durably stored and subsequent reads will see the updated data (assuming appropriate transaction isolation).

A Read Model may provide eventual consistency — the data might be slightly stale if it has not been updated from the write side. This is a deliberate trade-off for better read performance and scalability.

The Repository works with the write side of CQRS, where strong consistency is important for business operations. The Read Model works with the read side, where eventual consistency is acceptable for display purposes.

## Q55: What is the Repository pattern's approach to cross-aggregate queries?

**A:** Cross-aggregate queries are a challenge for the Repository pattern because each Repository is scoped to a single aggregate. Queries that span multiple aggregates cannot be handled by a single Repository and require either multiple Repository calls or a dedicated Query Service.

The Service Layer can orchestrate multiple Repository calls to gather data from different aggregates and combine the results. This is appropriate when the aggregation logic is simple and does not require complex joins or aggregations.

For complex cross-aggregate queries, a Query Service or Report Repository is more appropriate. These specialized components can execute queries across multiple aggregates and return optimized results without the overhead of loading complete aggregate objects.

## Q56: What is the difference between Repository and Value Object persistence?

**A:** Value Objects are immutable and defined by their attributes rather than identity. They do not have a Repository of their own — they are persisted as part of their owning Entity's Repository. For example, an `Address` Value Object is persisted as columns in the `users` table.

The Entity's Repository handles the serialization and deserialization of Value Objects. When loading an Entity, the Repository reconstructs its Value Objects from the database columns. When saving, it serializes the Value Objects back to columns.

This approach ensures that Value Objects are always loaded and saved with their owning Entity, maintaining consistency. The Service Layer does not need to know whether a Value Object is stored inline, as a separate table, or as a serialized column.

## Q57: What is the Repository pattern's role in event-driven architectures?

**A:** In event-driven architectures, the Repository can publish domain events when entities are saved or deleted. This allows other components to react to state changes without direct coupling to the Repository or Service.

The Repository can integrate with an Event Bus or Message Broker to publish events asynchronously. For example, when an Order is saved, the Repository publishes an `OrderCreated` event that triggers inventory updates, email notifications, and analytics processing.

This integration must be handled carefully to ensure that events are published only after the transaction is committed. Publishing events before commit can lead to inconsistencies if the transaction fails.

## Q58: What is the difference between Repository and Data Access Object in terms of reuse?

**A:** DAOs are typically specific to a particular database table or entity type. Each table has its own DAO with methods specific to that table's structure and access patterns. DAOs are reused within a single application.

Repository interfaces can be reused across applications because they are defined in the domain layer and work with domain concepts rather than database-specific structures. The same `UserRepository` interface can be implemented differently for different persistence technologies.

The Repository's domain-level abstraction makes it more reusable than the DAO's persistence-level abstraction. However, the DAO's simplicity makes it more appropriate for applications that do not need the Repository's level of abstraction.

## Q59: What is the Unit of Work's approach to nested transactions?

**A:** Nested transactions allow a transaction to be subdivided into smaller transactions, each with its own savepoint. If a nested transaction fails, only the changes since the last savepoint are rolled back, not the entire outer transaction.

The Unit of Work manages nested transactions by maintaining a transaction stack. Each `begin()` pushes a new transaction onto the stack, and each `commit()` or `rollback()` pops it. Savepoints allow partial rollbacks within a nested transaction.

Most databases support savepoints but not true nested transactions. The Unit of Work simulates nested transactions using savepoints, providing the illusion of nested transaction support without database-level nested transaction capabilities.

## Q60: What is the Repository pattern's handling of database-specific features?

**A:** Database-specific features like full-text search, geospatial queries, or JSON operations are difficult to abstract through a generic Repository interface. The Repository must either avoid these features or provide extension methods for database-specific operations.

The solution is to keep the Repository interface clean for common operations and provide database-specific extensions through specialized Repository implementations or Query Services. The service layer uses the generic interface for common operations and the specialized interface for database-specific features.

This approach maintains portability for common operations while allowing access to database-specific optimizations when needed. The trade-off is increased complexity in the Repository layer.

## Q61: What is the difference between Repository and Data Transfer Object (DTO)?

**A:** A Repository works with domain objects — rich entities with behavior and business logic. A DTO is a simple data structure used for transferring data between layers or services, with no behavior or business logic.

The Repository loads domain objects from the database and returns them to the Service Layer. The Service Layer may transform domain objects into DTOs for transfer to the Presentation Layer. DTOs prevent the Presentation Layer from being coupled to the domain model.

In CQRS, the Read Model uses DTOs or projection objects instead of domain objects. The Read Repository returns these lightweight objects directly, avoiding the overhead of constructing full domain objects for read-only operations.

## Q62: What is the Repository pattern's approach to database connection management?

**A:** The Repository should not manage database connections directly. Connection management is an infrastructure concern that should be handled by a Connection Factory or the ORM framework. The Repository receives an injected connection or session and uses it for data access.

The Unit of Work or transaction manager typically manages the connection lifecycle — creating the connection at the start of a transaction and releasing it at the end. The Repository uses the connection provided by the current Unit of Work.

This separation ensures that connection pooling, timeout management, and retry logic are handled consistently across all Repositories. Each Repository does not need to implement its own connection management.

## Q63: What is the Repository pattern's impact on database schema design?

**A:** The Repository pattern does not directly influence schema design, but the domain model it serves does. A well-designed domain model (with Aggregates, Entities, and Value Objects) may require a different schema design than a traditional normalized database schema.

Aggregate boundaries often align with transaction boundaries, which may require denormalization for performance. The Repository must load complete Aggregates, which may require joins across multiple tables or denormalized views.

The schema should support the access patterns required by the Repository. If the Repository frequently loads an Order with its Items, the schema should be designed to support efficient joins between the orders and order_items tables.

## Q64: What is the difference between Repository and Unit of Work in terms of API surface?

**A:** The Repository API is collection-like: `find_by_id()`, `find_all()`, `save()`, `delete()`. These operations work with individual aggregates or collections of aggregates. The API is domain-focused and uses entity-specific terminology.

The Unit of Work API is transaction-focused: `begin()`, `commit()`, `rollback()`, `register_dirty()`, `register_new()`. These operations manage the transaction lifecycle and track changes. The API is infrastructure-focused and uses persistence terminology.

The Repository is the primary interface used by the Service Layer. The Unit of Work is typically managed behind the scenes by the framework or a transaction manager. The Service Layer may interact with the Unit of Work to flush changes or register entities for persistence.

## Q65: What is the Repository pattern's role in domain event publishing?

**A:** Domain Events are significant occurrences in the domain that other parts of the system may want to react to. The Repository can collect events from aggregate roots during save operations and publish them after the transaction commits.

When `save()` is called on the Repository, the aggregate root may have raised domain events (like `OrderPlaced`, `PaymentReceived`). The Repository collects these events and makes them available for publishing. After the Unit of Work commits, the event publisher dispatches the events to subscribers.

This integration ensures that domain events are published reliably and consistently with the database changes. Events are only published after the transaction commits, preventing inconsistency if the transaction fails.

## Q66: What is the difference between Repository and Cache-Aside pattern?

**A:** The Cache-Aside pattern (also known as "lazy loading") caches data outside the Repository. The application checks the cache before calling the Repository. If the data is in the cache, it is returned directly. If not, the Repository loads it from the database and the application stores it in the cache.

The Repository is unaware of the cache — the caching logic is in the calling code. This separates concerns but requires the calling code to implement caching logic, which can be duplicated across multiple callers.

Alternatively, the Repository can implement caching internally, combining the Repository and Cache-Aside patterns. This centralizes caching logic but couples the Repository with the caching mechanism. The choice depends on whether caching is a domain concern or an infrastructure concern.

## Q67: What is the Repository pattern's handling of auditing?

**A:** Auditing tracks who created, modified, or deleted data and when. The Repository can integrate with the auditing system by recording audit information during save and delete operations.

When `save()` is called, the Repository records the current user, timestamp, and operation type. This information is stored in audit columns (created_at, updated_at, created_by, updated_by) or in a separate audit table.

The Unit of Work can also contribute to auditing by tracking all changes made during a transaction and recording them in a single audit entry. This provides a complete picture of all changes within a business operation.

## Q68: What is the difference between Repository and DAO in terms of architectural placement?

**A:** The Data Access Layer is an architectural layer that contains all data access code. It sits between the Business Logic Layer and the Database Layer. The Repository is a pattern that provides the public interface for the Data Access Layer.

The Data Access Layer contains Repositories, Data Mappers, connection factories, query builders, and other data access components. The Repository is the entry point that the Business Logic Layer uses; the rest of the Data Access Layer is implementation detail.

In clean architecture, the Repository interface is defined in the Application or Domain layer, and the implementation is in the Infrastructure layer. The Data Access Layer is entirely within the Infrastructure layer.

## Q69: What is the Repository pattern's handling of validation?

**A:** The Repository should enforce persistence-level validation — ensuring that required fields are present, data types are correct, and unique constraints are satisfied. Business-level validation should be handled by the domain objects or the Service Layer.

The Repository validates data before persisting it. If validation fails, the Repository throws a domain-level exception that the Service Layer can handle. The Repository does not enforce business rules — it enforces data integrity constraints.

For example, the Repository ensures that an Order has at least one OrderItem before saving (data integrity). The domain object ensures that the Order total does not exceed the customer's credit limit (business rule).

## Q70: What is the Repository pattern's role in data migration?

**A:** Repositories can be used for data migration by providing a consistent interface for reading and writing data regardless of the source or target format. A MigrationRepository can read from the old system and write to the new system using the same domain objects.

The Repository abstraction allows the migration code to work with domain objects without knowing the specifics of either the source or target database. The migration logic loads data through one Repository and saves it through another.

This approach simplifies migration code and makes it more maintainable. The same domain objects and business logic are used in both the old and new systems, ensuring consistency during migration.

## Q71: What is the difference between Repository and Query Object in terms of reusability?

**A:** Repository methods are specific to a single aggregate type. A `find_active_users()` method on the `UserRepository` cannot be reused for finding active orders.

Query Objects encapsulate reusable query criteria that can be applied across different Repositories. An `IsActive` Query Object can be used with the `UserRepository`, `OrderRepository`, or any other Repository that supports active/inactive state.

Query Objects are more reusable than Repository methods because they are not tied to a specific entity type. They can be composed with other Query Objects to create complex, reusable query logic.

## Q72: What is the Repository pattern's approach to lazy loading?

**A:** Lazy loading defers the loading of related objects until they are accessed. In ORM frameworks, lazy loading is implemented through Proxy objects that load data on first access. The Repository loads the aggregate root and the ORM handles lazy loading of related objects within the aggregate.

However, lazy loading across aggregate boundaries is problematic because it creates hidden database queries that can lead to N+1 query problems and unexpected performance degradation. The Repository should eagerly load all objects within an aggregate boundary and load related aggregates explicitly.

The Repository should control the loading strategy — eager loading for objects within the aggregate, explicit loading for related aggregates. This ensures predictable query patterns and prevents the lazy loading anti-pattern.

## Q73: What is the Repository pattern's handling of database-specific queries?

**A:** Database-specific queries (like full-text search in PostgreSQL, geospatial queries in MongoDB, or window functions in SQL) cannot be expressed through a generic Repository interface. The Repository must provide extension points for database-specific operations.

The approach is to define the generic Repository interface for common operations and provide database-specific implementations or extension methods for specialized queries. The Service Layer uses the generic interface for common operations and the database-specific interface when needed.

This maintains portability for common operations while allowing access to database-specific optimizations. The trade-off is increased complexity and the risk of leaking persistence details into the domain layer.

## Q74: What is the Unit of Work's role in distributed systems?

**A:** In distributed systems, the Unit of Work manages local transactions within a single service. Cross-service transactions are handled through patterns like Sagas, which coordinate multiple local transactions to achieve eventual consistency.

The Unit of Work ensures that all changes within a single service are committed atomically. If the service interacts with other services, the coordination is handled at a higher level — through message queues, event choreography, or orchestration.

Sagas extend the Unit of Work concept across services. Each service has its own Unit of Work for local transactions, and the Saga coordinates the overall transaction across services. If any service fails, the Saga triggers compensating transactions to undo the changes.

## Q75: What is the Repository pattern's impact on API design?

**A:** The Repository pattern influences API design by providing a consistent interface for data operations. The API endpoints map to Repository operations — a GET endpoint maps to `find_by_id()`, a POST to `save()`, a DELETE to `delete()`.

The Repository's interface should align with the API's needs. If the API requires pagination, the Repository should support paginated queries. If the API requires filtering, the Repository should support filter-based queries.

The Repository abstraction allows the API to evolve independently of the database schema. Changes to the database can be absorbed by the Repository implementation without affecting the API contract.

## Q76: How would you design a Repository for an event-sourced aggregate?

**A:** An event-sourced Repository stores events rather than the current state of an aggregate. When saving, the Repository persists new events to the event store. When loading, the Repository retrieves all events for the aggregate and replays them to reconstruct the current state.

The Repository must handle event versioning — as the aggregate evolves, events from older versions must be upcasted to the current version. It should also support snapshots to avoid replaying thousands of events for long-lived aggregates.

The event store can be implemented as an append-only log (EventStoreDB, Kafka) or as a relational table. The Repository's interface remains the same — `find_by_id()` and `save()` — but the internal implementation stores events instead of state.

**Example:**
```python
from typing import List


class EventSourcedOrderRepository:
    def __init__(self, event_store):
        self.event_store = event_store

    def find_by_id(self, order_id: int) -> Order:
        events = self.event_store.get_events(order_id)
        if not events:
            raise ValueError(f"Order {order_id} not found")
        order = Order(order_id, customer_id=0)
        for event in events:
            order.apply(event)
        return order

    def save(self, order: Order):
        new_events = order.get_uncommitted_events()
        self.event_store.append(order.id, new_events)
        order.clear_uncommitted_events()

    def get_events(self, order_id: int) -> List[dict]:
        return self.event_store.get_events(order_id)
```

## Q77: What is the Repository pattern's handling of database transactions across multiple Repositories?

**A:** When multiple Repositories participate in a single business transaction, the Unit of Work coordinates their changes. The Unit of Work ensures that all changes across all Repositories are committed atomically.

The Service Layer creates a Unit of Work, uses multiple Repositories to load and modify domain objects, and then commits the Unit of Work. The Unit of Work flushes all changes to the database in a single transaction.

This coordination requires that the Unit of Work manages the database connection and transaction. Each Repository uses the connection provided by the Unit of Work, ensuring that all operations participate in the same transaction.

## Q78: What is the difference between Repository and Data Mapper in terms of granularity?

**A:** Data Mapper operates at the individual property level — it maps each domain object property to a database column. The Data Mapper handles type conversions, null handling, and relationship mapping at the property level.

Repository operates at the aggregate level — it loads and saves entire aggregates, including all their contained entities and value objects. The Repository ensures that the aggregate is loaded completely and saved atomically.

The Data Mapper is a lower-level concern that the Repository uses internally. The Repository composes multiple Data Mapper operations to load and save complete aggregates.

## Q79: What is the Repository pattern's approach to database connection pooling?

**A:** Connection pooling is an infrastructure concern that should be handled by the database driver or a connection pool library, not by the Repository. The Repository receives an already-established connection from the connection pool and uses it for data access.

The Unit of Work or transaction manager typically obtains a connection from the pool at the start of a transaction and releases it back to the pool at the end. The Repository uses the connection provided by the current Unit of Work.

This separation ensures that connection pooling is handled consistently across all Repositories. The Repository does not need to implement its own connection pooling logic.

## Q80: What is the difference between Repository and Active Record in terms of domain purity?

**A:** Active Record objects contain both domain logic and persistence logic. The domain model is impure — it mixes business concerns with infrastructure concerns. This makes the domain model harder to test and reuse.

Repository-based domain objects are pure — they contain only domain logic and no persistence awareness. The persistence logic is in the Repository, which is an infrastructure component. This keeps the domain model clean and testable.

The Repository pattern promotes a "rich domain model" where entities contain business behavior. Active Record promotes an "anemic domain model" where entities are data containers and persistence objects.

## Q81: What is the Repository pattern's role in the CQRS write side?

**A:** On the CQRS write side, the Repository loads aggregates, the command handler applies business logic, and the Repository saves the updated aggregates. The Repository ensures that the aggregate is loaded completely and saved atomically within a transaction.

The write Repository works with rich domain objects and enforces business invariants. It loads the aggregate, the command handler processes the command, and the Repository persists the result. Domain events raised during processing are stored alongside the aggregate state.

The write Repository is designed for consistency, not performance. It loads complete aggregates, enforces business rules, and saves changes atomically. Read operations on the write side are minimal and typically only used for command validation.

## Q82: What is the Repository pattern's handling of database-specific data types?

**A:** Database-specific data types (JSON columns, spatial data, arrays) require mapping between domain objects and database representations. The Repository or Data Mapper handles this translation, converting between domain-friendly types and database-specific types.

For example, a JSON column in PostgreSQL might store a domain object's complex attribute. The Repository serializes the domain object to JSON when saving and deserializes it when loading. This translation is hidden behind the Repository's interface.

The challenge is that different databases handle these types differently. A Repository designed for PostgreSQL might not work with MySQL. This is an argument for keeping the Repository interface generic and the implementation database-specific.

## Q83: What is the Repository pattern's impact on performance?

**A:** The Repository pattern can impact performance by abstracting away database-specific optimizations. Generic Repository interfaces may not support efficient bulk operations, database-specific query hints, or connection-level optimizations.

However, the Repository can be optimized internally. A well-designed Repository uses batch operations, eager loading within aggregates, and caching strategies to minimize performance overhead. The key is that these optimizations are implementation details hidden behind the interface.

The Repository pattern's primary performance impact is the overhead of abstraction. Loading a complete aggregate when only a few fields are needed adds unnecessary data transfer. The trade-off is cleaner code and better maintainability for complex domains.

## Q84: What is the difference between Repository and Unit of Work in terms of error recovery?

**A:** When a Repository operation fails (connection loss, constraint violation), the Unit of Work rolls back the entire transaction, undoing all changes made by all Repositories within that Unit of Work.

The Repository translates database-specific errors into domain-level exceptions. The Unit of Work catches these exceptions, rolls back the transaction, and rethrows the exception to the Service Layer.

Error recovery strategies include retrying the transaction (for transient errors), notifying the user of the conflict (for concurrency errors), or compensating for partial failures (in distributed scenarios).

## Q85: What is the Repository pattern's role in data synchronization?

**A:** The Repository can support data synchronization between multiple data stores. For example, synchronizing data between a primary database and a read replica, or between an on-premises database and a cloud cache.

The Repository handles the synchronization logic internally. When `save()` is called, the Repository writes to the primary store and asynchronously updates the read stores. The synchronization can be synchronous (strong consistency) or asynchronous (eventual consistency).

The Repository abstraction allows the synchronization strategy to be changed without affecting the Service Layer. The Service Layer calls `save()` without knowing whether the data is synchronized to multiple stores.

## Q86: What is the Repository pattern's approach to database migration?

**A:** The Repository pattern facilitates database migration by providing a clean abstraction between the application and the database. During migration, the Repository implementation can be swapped to point to the new database without changing the Service Layer.

The migration strategy can use the Strangler Fig pattern — gradually replacing the old Repository implementation with a new one. Features can be migrated one at a time, with each feature using the new Repository implementation.

The Repository interface serves as a contract that both the old and new implementations must fulfill. This ensures that the migration does not break existing functionality.

## Q87: What is the Unit of Work's approach to idempotency?

**A:** Idempotency ensures that repeating an operation produces the same result. The Unit of Work can support idempotency by tracking completed operations and skipping duplicates. This is important for retry scenarios where the same business operation might be attempted multiple times.

The Unit of Work can use a unique operation identifier to detect duplicate operations. If the same operation is submitted twice, the second attempt is either skipped or returns the result of the first attempt.

This is particularly important in distributed systems where network failures can cause retries. The Unit of Work ensures that retries do not create duplicate data or inconsistent state.

## Q88: What is the Repository pattern's role in offline-first applications?

**A:** Offline-first applications need to work without network connectivity and synchronize data when connectivity is restored. The Repository pattern can abstract this by providing a local data store (like SQLite or IndexedDB) that works offline.

The Repository stores data locally and synchronizes with the server when connectivity is available. Conflict resolution strategies (last-write-wins, merge, manual resolution) are handled during synchronization.

The Service Layer uses the Repository without knowing whether the data is stored locally or on the server. The Repository handles the synchronization logic internally, providing a consistent interface regardless of connectivity.

## Q89: What is the difference between Repository and Unit of Work in terms of thread safety?

**A:** The Repository is typically stateless and thread-safe. Multiple threads can use the same Repository instance concurrently without conflicts. The Repository does not maintain mutable state between operations.

The Unit of Work is typically scoped to a single thread or request. It maintains mutable state (tracked entities, pending changes) that should not be accessed concurrently. The Unit of Work is created per-request and disposed when the request completes.

Thread safety is critical in web applications where multiple requests are processed concurrently. The Repository can be registered as a singleton, while the Unit of Work must be registered as scoped or transient to prevent cross-request contamination.

## Q90: What is the Repository pattern's handling of database constraints?

**A:** The Repository should not enforce business-level constraints (like "order total must be positive") — those belong in the domain objects or the Service Layer. The Repository enforces persistence-level constraints (like unique columns, foreign keys, not-null columns).

When a constraint violation occurs, the Repository catches the database exception and translates it into a domain-level exception. For example, a unique constraint violation on the email column becomes a `DuplicateEmailException` that the Service Layer can handle.

The Repository should not duplicate business logic. It should trust the domain objects and Service Layer to enforce business rules and only handle persistence-level concerns.

## Q91: What is the Repository pattern's role in API versioning?

**A:** API versioning can be supported by having different Repository implementations for different API versions. Version 1 of the API might use a `V1UserRepository` that returns a subset of user data, while version 2 uses a `V2UserRepository` that includes additional fields.

The Repository abstraction allows different API versions to coexist without changing the domain model. Each version has its own Repository implementation that maps the domain model to the version-specific data format.

This approach avoids duplicating business logic across API versions. The domain model and business rules are shared, and only the data mapping differs between versions.

## Q92: What is the difference between Repository and Gateway in terms of reliability?

**A:** Repositories deal with local data stores that are typically highly reliable (databases with replication and backup). The Repository can assume that data operations will succeed in most cases and handle failures through retries and transactions.

Gateways deal with external systems that may be unreliable (third-party APIs, external services). The Gateway must implement retry logic, circuit breakers, and fallback mechanisms to handle external system failures.

The reliability requirements for Gateways are typically higher than for Repositories. The Gateway must handle network failures, timeouts, and external system outages gracefully, while the Repository can rely on the database's reliability features.

## Q93: What is the Repository pattern's approach to read replicas?

**A:** Read replicas are copies of the primary database used for read operations. The Repository can abstract this by routing read operations to replicas and write operations to the primary database.

The Repository can detect the operation type (read or write) and select the appropriate database connection. Read operations use the replica connection, and write operations use the primary connection. This is transparent to the Service Layer.

The challenge is handling replication lag — data written to the primary may not yet be available on the replica. The Repository can mitigate this by using the primary for reads immediately after a write, or by implementing a cache for recently written data.

## Q94: What is the Repository pattern's role in data archival?

**A:** Data archival moves old or inactive data to long-term storage. The Repository can abstract this by transparently loading data from either the active store or the archive store.

When the Service Layer calls `find_by_id()`, the Repository checks the active store first. If the data is not found, it checks the archive store. When `save()` is called, the data is written to the active store.

The archival logic is hidden behind the Repository's interface. The Service Layer does not know whether data is in the active store or the archive. The Repository handles the storage strategy internally.

## Q95: What is the Unit of Work's handling of compensation logic?

**A:** Compensation logic is used to undo the effects of a completed operation when a later operation fails. In distributed scenarios, the Unit of Work can record compensation actions that can be executed if the transaction needs to be rolled back.

The Unit of Work tracks not only the forward actions (insert, update, delete) but also the corresponding compensation actions (delete, restore original, re-insert). If the transaction fails, the Unit of Work executes the compensation actions to restore the original state.

This is the basis of the Saga pattern for distributed transactions. Each step in the Saga has a forward action and a compensation action. If any step fails, the preceding steps are compensated.

## Q96: What is the Repository pattern's handling of database-specific features in CQRS?

**A:** On the CQRS read side, the Repository can use database-specific features freely because the read model is not constrained by domain purity requirements. The read Repository can use denormalized views, materialized views, and database-specific query optimizations.

On the write side, the Repository maintains domain purity and uses standard persistence operations. The write Repository focuses on consistency and business rule enforcement.

The separation of read and write sides allows each to use the most appropriate database features. The read side can use Elasticsearch for full-text search, Redis for caching, and PostgreSQL for complex queries. The write side uses the primary database for transactional consistency.

## Q97: What is the Repository pattern's role in domain-driven design anti-corruption layers?

**A:** An anti-corruption layer (ACL) translates between the domain model and an external system's model. The Repository can serve as an ACL by wrapping external data sources behind a domain-level interface.

When integrating with a legacy system, the Repository translates between the domain objects and the legacy system's data format. The Service Layer works with domain objects, and the Repository handles the translation.

This prevents the legacy system's model from leaking into the domain. The Repository acts as a translation layer, preserving the domain model's purity while integrating with external systems.

## Q98: What is the Repository pattern's impact on code organization?

**A:** The Repository pattern promotes a clean code organization where data access code is centralized in the Infrastructure layer. Domain objects live in the Domain layer, Services in the Application layer, and Repositories in the Infrastructure layer.

This organization follows the Dependency Inversion Principle — the Application and Domain layers depend on Repository interfaces defined in the Domain layer, and the Infrastructure layer provides the implementations.

The code organization makes it easy to find data access code, replace persistence implementations, and test components in isolation. Each layer has a clear responsibility and well-defined boundaries.

## Q99: What are the common pitfalls of implementing the Repository pattern?

**A:** Common pitfalls include: creating Repositories that are too granular (one per entity instead of per aggregate root), leaking persistence concerns into the domain layer (exposing SQL or ORM-specific types), and creating bloated interfaces with too many query methods.

Another pitfall is using the Repository pattern where it is not needed — simple CRUD applications may benefit more from Active Record. Over-engineering with Repositories adds unnecessary abstraction overhead.

The Repository should be designed around aggregate roots, not entities. The interface should be minimal and domain-focused. Persistence-specific details should be hidden behind the interface. And the pattern should be used when the complexity justifies the abstraction.

## Q100: What is your recommended architecture for a greenfield project using Repository and Unit of Work patterns?

**A:** For a new project, I recommend a layered architecture with clear boundaries: Domain Layer (entities, value objects, domain events, repository interfaces), Application Layer (services, use cases, DTOs, Unit of Work interface), and Infrastructure Layer (repository implementations, ORM configuration, database migrations).

Use package-by-feature for the Domain and Application layers, organizing code around business capabilities. Use package-by-layer for the Infrastructure layer, grouping repository implementations by persistence technology.

Implement the Repository pattern per aggregate root, the Unit of Work per request or business operation, and CQRS if the read and write models diverge significantly. Start with a monolith using clear layer boundaries, and extract microservices when scaling requirements demand it.

Use dependency injection throughout with constructor injection as the default. Define interfaces in the inner layers and implementations in the outer layers. This ensures that the architecture remains flexible and testable as the project grows.
