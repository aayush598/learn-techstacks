# Chain of Responsibility, Mediator and Interpreter — 100 Interview Q&A

## Q1: What is the Chain of Responsibility pattern and when would you use it?

**A:** The Chain of Responsibility pattern passes a request along a chain of handlers. Each handler decides either to process the request or to pass it to the next handler in the chain. It decouples the sender of a request from its receivers, giving multiple objects a chance to handle the request.

You would use this pattern when you have multiple objects that may handle a request, but the handler is not known in advance. Examples include middleware in web frameworks (authentication, logging, rate limiting), UI event handling (event bubbling in the DOM), approval workflows (manager, director, VP approval chains), and exception handling (try-catch chain).

The key benefit is that the sender does not need to know which handler will process the request. Handlers can be added, removed, or reordered dynamically at runtime. The sender only needs to know the first handler in the chain, not the entire chain structure.

**Example:**
```python
class Handler:
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def handle(self, request):
        if self._next:
            return self._next.handle(request)
        return None

class AuthHandler(Handler):
    def handle(self, request):
        if not request.get("token"):
            return "Unauthorized"
        return super().handle(request)

class LoggingHandler(Handler):
    def handle(self, request):
        print(f"Request: {request}")
        return super().handle(request)
```

---

## Q2: What is the difference between the Chain of Responsibility and a simple if-else chain?

**A:** A simple if-else chain hardcodes all the handling logic in one place. The condition and the handling code are tightly coupled, and adding a new handler requires modifying the existing code. The Chain of Responsibility distributes handling logic across multiple, independent handler objects.

The Chain of Responsibility provides several advantages: each handler is self-contained (Single Responsibility Principle), handlers can be reordered or replaced at runtime without modifying other handlers, and new handlers can be added without changing existing code (Open/Closed Principle).

The if-else chain is simpler for a small, fixed number of conditions. The Chain of Responsibility is better when handlers may change, when the same chain needs to be used in different configurations, or when handlers need to maintain their own state. The pattern also naturally supports the concept of "stopping" the chain when a handler processes the request.

---

## Q3: What is the difference between a handler chain and middleware?

**A:** Middleware is a specific application of the Chain of Responsibility pattern, typically used in web frameworks and application servers. Middleware sits between the request and the core application logic, performing cross-cutting concerns like authentication, logging, CORS, and request transformation.

A handler chain is more general: handlers can process, transform, reject, or pass along requests. Middleware typically has a specific contract: it receives a request and a `next` function, performs its logic, and optionally calls `next()` to pass to the next middleware. Middleware is usually configured centrally and applies to all requests (or specific routes).

The key difference is that middleware follows a convention (request/response cycle with `next()`), while handler chains are more flexible (handlers may modify, reject, or pass along any type of object). Middleware is typically unidirectional (request flows forward, response flows back), while handler chains may be bidirectional.

**Example:**
```java
interface Middleware {
    void handle(Request request, Runnable next);
}

class AuthMiddleware implements Middleware {
    public void handle(Request request, Runnable next) {
        if (request.getHeader("Authorization") == null) {
            throw new UnauthorizedException();
        }
        next.run();
    }
}

// Express.js style
app.use((req, res, next) => {
    if (!req.headers.authorization) return res.status(401).send();
    next();
});
```

---

## Q4: What is the Mediator pattern and what problem does it solve?

**A:** The Mediator pattern defines an object that encapsulates how a set of objects interact. It promotes loose coupling by preventing objects from referring to each other explicitly and lets you vary their interaction independently. The Mediator centralizes complex communications between objects.

The problem it solves is the "spaghetti references" problem: in a system with many interacting objects, each object may need to communicate with many others, creating a web of dependencies. The Mediator replaces these pairwise dependencies with a single dependency on the mediator.

Common examples include: air traffic control (planes communicate through the tower, not directly with each other), chat rooms (users communicate through the server), UI dialog boxes (components interact through the dialog controller), and workflow engines (activities coordinate through the workflow engine).

---

## Q5: What is the difference between the Mediator pattern and the Observer pattern?

**A:** Both patterns reduce coupling, but they serve different purposes. The Observer pattern creates a one-to-many dependency where the subject notifies observers of state changes. Observers are independent of each other and do not know about other observers.

The Mediator pattern centralizes complex many-to-many interactions between objects. Colleagues (the objects managed by the mediator) communicate exclusively through the mediator, which contains the interaction logic. Colleagues may know about the mediator but not about each other.

The key distinction: Observer is for broadcasting (one producer, many consumers), while Mediator is for coordination (many objects interacting in complex ways). Observer is push-based (subject pushes to observers), while Mediator can be pull-based (colleagues query the mediator). Observer creates a hierarchy; Mediator creates a hub-and-spoke topology.

---

## Q6: How does the Mediator pattern reduce coupling between components?

**A:** Without a Mediator, components communicate directly with each other. If there are N components, there can be up to N*(N-1)/2 pairwise connections. Each component knows about and depends on many others, creating tight coupling that makes changes risky and testing difficult.

With a Mediator, each component depends only on the mediator. The mediator knows about all components and routes messages between them. This reduces the dependencies from O(N²) to O(N). Components can be modified, added, or removed without affecting other components, only the mediator needs to be updated.

The mediator also centralizes interaction logic, making it easier to understand, modify, and test. Complex conditional logic (if component A is in state X, notify component B but not component C) is in the mediator rather than distributed across components. This makes the system's behavior more predictable and maintainable.

---

## Q7: What is the Interpreter pattern and when would you use it?

**A:** The Interpreter pattern defines a grammatical representation for a language and an interpreter that uses this representation to evaluate sentences in the language. It is used to evaluate expressions, formulas, commands, or rules written in a formal language.

You would use the Interpreter pattern when you have a simple language to evaluate, the grammar is simple and fixed, efficiency is not critical, and the language is used repeatedly. Examples include: mathematical expression evaluators, SQL query parsers, regular expression engines, template languages, configuration file parsers, and domain-specific languages (DSLs).

The pattern involves defining a class for each grammar rule (Terminal and Non-terminal expressions), a context that holds global information, and an interpreter that evaluates the expression tree. Each grammar rule class implements an `interpret()` method that evaluates itself in the given context.

---

## Q8: What is an Abstract Syntax Tree (AST) and how does it relate to the Interpreter pattern?

**A:** An Abstract Syntax Tree (AST) is a tree representation of the syntactic structure of source code or expressions. Each node in the tree represents a construct in the language (operator, operand, statement, expression). The AST is an intermediate representation between the raw text and the executed result.

In the Interpreter pattern, the AST is the primary data structure. The grammar is parsed into an AST, and each node in the tree is an interpreter object. Evaluating the expression means traversing the AST and computing the result at each node.

The AST is built by the parser (typically generated by parser generators like ANTLR, Yacc, or hand-written recursive descent parsers). Each node type corresponds to a grammar rule. Terminal nodes represent literals or identifiers; non-terminal nodes represent operations or compositions.

**Example:**
```python
class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def interpret(self):
        return self.value

class AddNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def interpret(self):
        return self.left.interpret() + self.right.interpret()

# 3 + 5 → AddNode(NumberNode(3), NumberNode(5))
```

---

## Q9: What is the difference between a terminal and non-terminal expression in the Interpreter pattern?

**A:** A terminal expression represents an atomic element of the grammar (a literal, a variable, or a simple symbol). It does not contain other expressions and cannot be decomposed further. Terminal expressions are the leaves of the AST.

A non-terminal expression represents a compound construct that contains one or more sub-expressions (which may be terminal or non-terminal). Non-terminal expressions are the internal nodes of the AST. They decompose the problem and combine the results of their sub-expressions.

For example, in the expression `3 + 5 * 2`, `3`, `5`, and `2` are terminal expressions (numbers). `5 * 2` is a non-terminal expression (multiplication), and `(3 + 5) * 2` or `3 + (5 * 2)` are higher-level non-terminal expressions (addition wrapping multiplication). The grammar rules define which combinations are valid.

---

## Q10: How do you handle operator precedence in the Interpreter pattern?

**A:** Operator precedence determines the order in which operations are evaluated. In the Interpreter pattern, precedence is handled during parsing, not interpretation. The parser builds an AST that reflects the correct precedence by nesting sub-expressions appropriately.

Higher-precedence operators are placed deeper in the AST (evaluated first), while lower-precedence operators are placed higher (evaluated last). For example, `3 + 5 * 2` is parsed as `Add(Number(3), Multiply(Number(5), Number(2)))`, ensuring multiplication happens before addition.

The grammar definition explicitly encodes precedence through its structure. A common technique is to define separate grammar rules for each precedence level, from lowest to highest: expression → term → factor → primary. This ensures the parser naturally produces the correct tree structure.

---

## Q11: What are the limitations of the Interpreter pattern?

**A:** The Interpreter pattern has several limitations. For complex grammars, the number of classes grows proportionally to the grammar size, leading to class explosion. Each grammar rule requires a separate class, which can become unwieldy for large, complex languages.

Performance can be poor for frequently evaluated expressions because the AST traversal is slower than compiled code. There is no optimization phase (unlike compilers that optimize the AST). The pattern is also not suitable for languages with complex scoping, type systems, or side effects.

The pattern works best for simple, domain-specific languages where the grammar is small, the language is used repeatedly, and performance is acceptable. For complex languages (general-purpose programming languages, SQL), a full parser and compiler are more appropriate. The Interpreter pattern is often used in conjunction with other patterns (Composite for the AST, Flyweight for shared symbols).

---

## Q12: How does the Chain of Responsibility pattern support the Open/Closed Principle?

**A:** The Chain of Responsibility pattern supports the Open/Closed Principle because new handlers can be added to the chain without modifying existing code. The chain's behavior is extended by adding new handler classes, not by changing existing ones.

Adding a new handler requires: creating a new class that implements the handler interface, and inserting it into the chain at the appropriate position. No existing handler needs to be modified, and the sender does not need to change. This is the essence of the Open/Closed Principle: open for extension, closed for modification.

For example, adding a new validation step to a form processing chain requires creating a new validator class and inserting it into the chain. The existing validators, the form processor, and the form submission logic remain unchanged.

---

## Q13: What is the role of a context object in the Chain of Responsibility pattern?

**A:** The context object carries information about the request through the chain. It is a container for all data that handlers need to process the request, including the request itself, metadata, authentication information, and any state that handlers need to share.

The context object decouples handlers from each other. Instead of passing the raw request and having each handler extract what it needs, the context provides a structured interface for accessing request data. Handlers may also add information to the context for downstream handlers (e.g., an authentication handler adds the authenticated user to the context).

Using a context object avoids "parameter explosion" where the handler signature grows with each new piece of data. It also provides a natural extension point: new data can be added to the context without changing handler signatures.

---

## Q14: How do you implement a filter chain in Java Servlets?

**A:** The Java Servlet API defines a `Filter` interface with `init()`, `doFilter()`, and `destroy()` methods. The `doFilter()` method receives a `ServletRequest`, `ServletResponse`, and `FilterChain`. The filter performs its logic and optionally calls `chain.doFilter()` to pass the request to the next filter.

Filters are configured in `web.xml` or via annotations (`@WebFilter`). They are applied in the order specified in the configuration. Each filter wraps the next, creating a Russian-doll structure. The innermost filter calls the servlet, and the response flows back through the filters in reverse order.

Filters are used for authentication, logging, compression, CORS, content-type checking, and request/response transformation. The chain can short-circuit by not calling `chain.doFilter()`, which is useful for authentication failures or request rejections.

**Example:**
```java
@WebFilter("/*")
public class AuthFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpReq = (HttpServletRequest) req;
        if (httpReq.getHeader("Authorization") == null) {
            ((HttpServletResponse) res).setStatus(401);
            return;
        }
        chain.doFilter(req, res);
    }
}
```

---

## Q15: What is the difference between the Mediator pattern and event-driven architecture?

**A:** The Mediator pattern is an object-oriented design pattern for structuring interactions within a single application. It centralizes communication logic in a single mediator object. Event-driven architecture (EDA) is a system-level architectural pattern where components communicate through events via a message broker.

The Mediator is synchronous and in-process: colleagues call the mediator directly. EDA is typically asynchronous and distributed: components publish events to a broker, and subscribers receive events independently. The Mediator knows about all colleagues; in EDA, producers and subscribers are typically unaware of each other.

In practice, a mediator may be implemented using EDA within a service, and EDA may use mediators to coordinate within a single component. The Mediator pattern is the in-process building block of event-driven architectures.

---

## Q16: How do you handle circular dependencies in the Mediator pattern?

**A:** Circular dependencies in the Mediator pattern occur when colleague A triggers an action in the mediator that notifies colleague B, which triggers an action that notifies colleague A, creating an infinite loop. This is a design flaw that must be addressed.

Solutions include: tracking the source of notifications (the mediator knows which colleague initiated the action and does not re-notify it), implementing reentrancy guards (a flag that prevents recursive notification from the same source), using a message queue (notifications are queued and processed after the current notification completes), and designing the interaction graph to be acyclic.

The mediator should detect and log potential infinite loops during development. In production, a recursion depth limit or timeout prevents infinite loops from crashing the system. The root cause is usually a circular dependency in the domain model, which should be resolved by restructuring the interaction logic.

---

## Q17: What is the difference between a pull and push mediator?

**A:** In a pull mediator, colleagues actively query the mediator for information or state changes. The mediator acts as a registry or information broker. Colleagues pull data when they need it, and the mediator responds to queries.

In a push mediator, the mediator actively notifies colleagues when relevant state changes occur. The mediator maintains subscription information and pushes updates to interested colleagues. This is similar to the Observer pattern but with a central mediator.

The pull model is better when colleagues need different views of the data, when data changes infrequently, or when polling is acceptable. The push model is better for real-time updates, when colleagues need immediate notification, and when data changes frequently. A hybrid approach uses push for critical updates and pull for on-demand data.

---

## Q18: How does the Chain of Responsibility pattern apply to middleware in Express.js?

**A:** Express.js middleware follows the Chain of Responsibility pattern: each middleware function receives the request, response, and a `next` function. The middleware performs its logic and calls `next()` to pass control to the next middleware. If `next()` is not called, the chain stops.

Middleware is registered with `app.use()` or `app.METHOD()`. They execute in the order of registration. The chain flows forward through middleware, reaches the route handler, and then flows back through the middleware in reverse order (for response modification).

This architecture enables composable, modular request processing. Authentication, logging, body parsing, CORS, and error handling are all implemented as middleware. Each middleware is independent and can be added, removed, or reordered without affecting other middleware.

---

## Q19: What is the Visitor pattern and how does it differ from the Interpreter pattern?

**A:** The Visitor pattern adds operations to an object structure without modifying the classes of the elements. The Interpreter pattern defines a grammar and evaluates sentences in that language. They both traverse object structures but for different purposes.

The Visitor pattern is used when you have a fixed set of element types and want to add new operations without modifying those types. The Interpreter pattern is used when you have a language (grammar) and want to evaluate expressions in that language. The Interpreter uses the Composite pattern for its AST; the Visitor may also use Composite.

The key distinction: the Interpreter pattern's primary purpose is evaluating a language, while the Visitor pattern's primary purpose is performing operations on a structure. In practice, the Interpreter pattern often uses the Visitor to traverse the AST for operations like type-checking, optimization, or code generation.

---

## Q20: What is a grammar and how does it relate to the Interpreter pattern?

**A:** A grammar is a formal specification of the syntax of a language. It defines the rules for constructing valid sentences (expressions, statements, programs) in the language. In the Interpreter pattern, the grammar is the foundation: the interpreter evaluates sentences that conform to the grammar.

A grammar consists of: terminal symbols (the basic tokens of the language), non-terminal symbols (intermediate constructs), production rules (how non-terminals are composed from terminals and other non-terminals), and a start symbol (the root of the grammar).

In the Interpreter pattern, each grammar rule maps to a class. Terminal rules map to terminal expression classes; non-terminal rules map to non-terminal expression classes. The grammar's structure determines the AST's structure, which determines the interpreter's evaluation logic.

---

## Q21: How do you handle error recovery in the Interpreter pattern?

**A:** Error recovery in the Interpreter pattern involves detecting syntax errors during parsing and semantic errors during interpretation. During parsing, the parser collects syntax errors and may attempt recovery (skipping tokens, inserting missing tokens) to report multiple errors at once.

During interpretation, semantic errors (type mismatches, undefined variables, division by zero) are detected by the interpreter. The interpreter should report the error with context (line number, column, the expression being evaluated) and continue evaluating other parts of the program if possible.

The error handling strategy depends on the use case: a calculator may throw an exception for invalid expressions; a DSL may report all errors and continue; a compiler may abort after too many errors. The Interpreter pattern supports error handling through the context object (which can carry error information) and exception handling (each interpreter method can throw exceptions).

---

## Q22: What is the difference between a handler chain and a pipeline?

**A:** A handler chain (Chain of Responsibility) passes a request through a sequence of handlers, where each handler may process the request or pass it along. A pipeline is a more general concept where data flows through a sequence of processing stages, with each stage transforming the data.

The key difference is in the data flow: in a handler chain, the request may be consumed (stopping the chain) or passed along. In a pipeline, data always flows through all stages, with each stage producing output for the next. A pipeline is typically unidirectional; a handler chain may be bidirectional (request flows forward, response flows back).

In practice, many systems combine both: a middleware pipeline where each stage transforms the request/response, and within each stage, a handler chain processes the transformed data. The pipeline provides the overall flow; the handler chain provides the internal processing logic.

---

## Q23: How do you implement a dynamic handler chain that can be modified at runtime?

**A:** A dynamic handler chain allows handlers to be added, removed, or reordered at runtime without restarting the application. The implementation maintains a list of handlers and provides methods for modification (add, remove, insert, sort).

The chain is typically managed by a chain builder or chain manager that holds the handler list and the current execution pointer. When a request arrives, the chain manager starts at the first handler and passes the request through each handler in order. Handlers can modify the chain (e.g., a handler can remove itself after processing a certain number of requests).

Thread safety is critical: concurrent modification of the chain while it is being executed can cause undefined behavior. Solutions include copy-on-write (create a new chain when modifications occur), read-write locks, or using a concurrent data structure for the handler list.

**Example:**
```python
class DynamicChain:
    def __init__(self):
        self.handlers = []
        self.lock = threading.Lock()

    def add_handler(self, handler):
        with self.lock:
            self.handlers.append(handler)

    def remove_handler(self, handler):
        with self.lock:
            self.handlers.remove(handler)

    def execute(self, request):
        with self.lock:
            chain = list(self.handlers)
        for handler in chain:
            if handler.can_handle(request):
                return handler.handle(request)
        return None
```

---

## Q24: What is the difference between the Mediator pattern and the Facade pattern?

**A:** The Mediator encapsulates complex interactions between a set of objects. Colleagues communicate through the mediator, and the mediator contains the interaction logic. The Facade provides a simplified interface to a complex subsystem. The facade does not contain interaction logic; it delegates to subsystem components.

The key difference: the Mediator handles many-to-many communication between objects that are aware of the mediator. The Facade provides a one-way simplified interface to a subsystem that is not aware of the facade. The Mediator's colleagues may call the mediator; the Facade's subsystem components do not know about the facade.

In practice, the Mediator pattern often emerges within a Facade: the facade coordinates complex interactions between subsystem components, acting as a mediator. However, the Facade's primary purpose is simplification, while the Mediator's primary purpose is coordination.

---

## Q25: How does the Interpreter pattern handle variable substitution?

**A:** Variable substitution in the Interpreter pattern is handled through the context object. The context contains a mapping of variable names to values. When the interpreter encounters a variable reference (a terminal expression), it looks up the variable's value in the context.

The variable reference expression implements `interpret()` by calling `context.getVariable(name)`. If the variable is not defined, the expression may throw an exception, return a default value, or treat it as an error. The context may also support assignment, allowing expressions to modify variable values.

For more complex scenarios (scoped variables, closures, lazy evaluation), the context may implement a stack of scopes, where inner scopes shadow outer scopes. The interpreter pushes a new scope when entering a block and pops it when exiting. This supports nested variable scoping as in programming languages.

**Example:**
```python
class Context:
    def __init__(self):
        self.variables = {}

    def get(self, name):
        if name not in self.variables:
            raise NameError(f"Undefined variable: {name}")
        return self.variables[name]

    def set(self, name, value):
        self.variables[name] = value

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def interpret(self, context):
        return context.get(self.name)
```


## Q26: What is the difference between a non-deterministic and deterministic handler chain?

**A:** A deterministic handler chain processes requests in a fixed, predictable order. Every request of the same type follows the same path through the chain. The outcome depends only on the request and the chain configuration.

A non-deterministic handler chain may process requests in different orders or through different paths. The handler selection may depend on runtime conditions (load balancing, random selection, priority-based routing). The same request may be processed by different handlers on different invocations.

Deterministic chains are easier to test and reason about. Non-deterministic chains are more flexible but harder to debug. In production systems, a common approach is to use deterministic chains with randomized elements for load balancing, where the randomization is controlled and reproducible (seeded random).

---

## Q27: How do you implement a handler chain with short-circuit evaluation?

**A:** Short-circuit evaluation means the chain stops processing as soon as a handler fully handles the request. This is useful for optimization (avoid unnecessary processing), security (stop after authentication failure), and error handling (stop after finding the first error).

The implementation uses a return value or flag to indicate whether the request was handled. Each handler checks this flag before processing. If the request is already handled, the handler passes it along without processing. Alternatively, the chain executor checks the flag after each handler and stops if the request is marked as handled.

In some designs, handlers return a result object that indicates whether the chain should continue. In others, the handler itself calls a method to stop the chain. The key is that the chain does not continue processing after a handler has fully handled the request.

---

## Q28: What is the Mediator's impact on testability?

**A:** The Mediator pattern has a mixed impact on testability. On one hand, it centralizes interaction logic, making it easier to test the mediator in isolation by mocking colleagues. On the other hand, it can create a large, complex mediator that is difficult to test thoroughly.

Testing the mediator involves: verifying that the mediator correctly routes messages between colleagues, verifying that the mediator handles edge cases (missing colleagues, circular dependencies, error conditions), and verifying that the mediator's state changes correctly in response to colleague events.

Testing colleagues in isolation is straightforward because they only depend on the mediator interface, which can be mocked. The mediator can be tested with mock colleagues that verify the mediator's behavior. The key is to keep the mediator interface small and focused to make mocking practical.

---

## Q29: How do you handle a handler chain where handlers have different priorities?

**A:** Handler priorities determine the order in which handlers are executed. Higher-priority handlers execute first. The implementation uses a priority queue or sorted list for the handler chain. Each handler has an associated priority value.

The chain manager sorts handlers by priority before execution. When handlers are added or removed, the chain is re-sorted. For handlers with equal priority, FIFO order is used as a tiebreaker.

Priority-based chains are useful in security systems (audit observers run before business observers), UI frameworks (layout observers before paint observers), and middleware (authentication before authorization). The priority can be static (defined at registration time) or dynamic (changed at runtime based on conditions).

---

## Q30: What is the difference between a recursive and iterative interpreter?

**A:** A recursive interpreter evaluates the AST by recursively calling `interpret()` on child nodes. Each non-terminal expression calls `interpret()` on its sub-expressions, which in turn call `interpret()` on their sub-expressions, until terminal nodes are reached. This mirrors the recursive structure of the AST.

An iterative interpreter uses an explicit stack or worklist to traverse the AST. It pushes nodes onto a stack and processes them in a loop, avoiding the overhead of recursive function calls. This is more efficient for deep ASTs (avoids stack overflow) and enables more flexible traversal strategies.

Recursive interpreters are simpler and more natural to write. Iterative interpreters are more efficient and can handle deeper ASTs. For most DSL interpreters, the recursive approach is sufficient. For production compilers and interpreters, the iterative approach is preferred for performance and stack safety.

**Example:**
```python
class IterativeInterpreter:
    def evaluate(self, root):
        stack = [(root, False)]
        results = {}
        while stack:
            node, processed = stack.pop()
            if isinstance(node, NumberNode):
                results[id(node)] = node.value
            elif isinstance(node, AddNode):
                if processed:
                    results[id(node)] = results[id(node.left)] + results[id(node.right)]
                else:
                    stack.append((node, True))
                    stack.append((node.right, False))
                    stack.append((node.left, False))
        return results[id(root)]
```

---

## Q31: How does the Chain of Responsibility pattern support the Single Responsibility Principle?

**A:** Each handler in the chain has a single responsibility: processing one specific aspect of the request. An authentication handler only handles authentication; a logging handler only handles logging; a validation handler only handles validation. No handler is responsible for multiple concerns.

This separation makes each handler simple, focused, and easy to test. Changes to one concern (e.g., updating the authentication logic) do not affect other handlers. New concerns are added as new handlers without modifying existing ones.

The chain itself has the responsibility of routing requests to handlers, which is a single concern. The sender has the responsibility of initiating the request. This clean separation of responsibilities makes the system easier to understand, modify, and maintain.

---

## Q32: What is the Mediator's role in a GUI application?

**A:** In a GUI application, the Mediator pattern coordinates interactions between UI components. A dialog box, for example, may contain text fields, buttons, checkboxes, and dropdown lists. The mediator (often called the dialog controller) manages how changes in one component affect others.

For example, when a checkbox is toggled, the mediator may enable or disable related text fields. When a text field changes, the mediator may update a preview panel. When a button is clicked, the mediator validates all fields and submits the form. Without the mediator, each component would need to know about and communicate with every other component.

The mediator reduces the code complexity in each UI component and centralizes the interaction logic. It also makes the dialog easier to test: the mediator can be tested with mock components, and the components can be tested independently with mock mediators.

---

## Q33: How do you implement a recursive descent parser for the Interpreter pattern?

**A:** A recursive descent parser is a top-down parser that uses a set of recursive functions, one for each grammar rule. Each function parses the corresponding grammar construct and returns an AST node. The parser consumes tokens from the input and builds the AST.

The parser starts with the start symbol's function and calls other functions based on the grammar rules. Terminal symbols are matched by consuming tokens; non-terminal symbols are matched by calling the corresponding function. The parser handles errors by throwing exceptions or collecting error messages.

Recursive descent parsers are simple to write and understand, making them ideal for the Interpreter pattern. They naturally produce ASTs and can handle left-recursive grammars with minor modifications (left recursion elimination). Parser generators (ANTLR, Yacc) can generate recursive descent parsers from grammar definitions.

---

## Q34: What is the difference between a handler chain and an interceptor chain?

**A:** A handler chain passes a request through a sequence of handlers, where each handler may process the request or pass it along. The request flows in one direction, and each handler is independent.

An interceptor chain wraps the request and response in a nested structure. Each interceptor has "before" and "after" logic. The request flows forward through the "before" logic, reaches the target, and then flows backward through the "after" logic. This is a Russian-doll structure.

The key difference is in the response handling: handlers typically do not see the response (they process the request and let the chain continue), while interceptors have access to both the request and the response. Interceptors are better for cross-cutting concerns that affect both request and response (logging, timing, transformation).

---

## Q35: What is the Abstract Factory pattern's relationship to the Interpreter pattern?

**A:** The Abstract Factory pattern may be used in the Interpreter pattern to create AST nodes. Instead of directly instantiating concrete expression classes, the interpreter uses a factory that creates the appropriate node type based on the grammar rule or token type.

This decouples the parser from the concrete expression classes. The parser calls factory methods to create nodes; the factory decides which concrete class to instantiate. This makes it easy to change the expression classes (e.g., to use optimized implementations) without modifying the parser.

The factory may also create different types of nodes for different evaluation strategies (e.g., lazy evaluation vs. eager evaluation). This allows the interpreter to be configured with different evaluation strategies without changing the parsing logic.

---

## Q36: How do you implement a handler chain with conditional routing?

**A:** Conditional routing means the chain's path depends on the request content or context. Different requests follow different paths through the chain. This is implemented using conditional logic in the chain manager or within handlers.

The chain manager may maintain multiple chains (one per condition) and select the appropriate chain based on the request. Alternatively, each handler may decide whether to pass the request to the next handler or to a different handler based on conditions.

In middleware systems, conditional routing is implemented using route matching (URL patterns, HTTP methods, headers). The Express.js router and Spring MVC's handler mapping are examples of conditional routing in middleware chains. The routing logic determines which chain of handlers processes the request.

---

## Q37: What is the difference between an eager and lazy interpreter?

**A:** An eager interpreter evaluates the entire AST immediately when `interpret()` is called. All sub-expressions are evaluated, even if their results are not needed. This is the default behavior in most simple interpreters.

A lazy interpreter evaluates sub-expressions only when their results are needed. This is useful for conditional expressions (short-circuit evaluation), infinite data structures (generators), and performance optimization (avoid unnecessary computation).

Lazy evaluation is implemented using thunks (delayed computation objects) or generators. Each node in the AST may wrap its computation in a thunk, which is evaluated only when the value is accessed. This adds complexity but can significantly improve performance for conditional or selective evaluation.

---

## Q38: How does the Mediator pattern handle asymmetric relationships between colleagues?

**A:** In many systems, colleagues have asymmetric relationships: some colleagues are more important, some produce data while others consume it, and some are optional while others are mandatory. The mediator must handle these asymmetries.

The mediator may assign different roles to colleagues (producer, consumer, observer, validator) and route messages based on these roles. The mediator may also enforce access control (only certain colleagues can send certain types of messages) and priority (important colleagues' messages are processed first).

The mediator can also handle optional colleagues: if an optional colleague is unavailable, the mediator routes around it. For mandatory colleagues, the mediator may queue messages until the colleague is available. The key is that the mediator encapsulates the asymmetry logic, keeping colleagues unaware of their relative importance.

---

## Q39: What is the difference between a push-based and pull-based Interpreter pattern?

**A:** In a push-based interpreter, the evaluation drives the traversal: each node calls `interpret()` on its children, pushing evaluation down the tree. This is the standard recursive approach.

In a pull-based interpreter, the evaluation is driven by demand: the root node requests values from its children, which in turn request values from their children. This is the lazy evaluation approach, where values are computed only when needed.

The push model is simpler and more common. The pull model is more efficient for selective evaluation and supports lazy evaluation naturally. In reactive programming, pull-based evaluation is the norm (observables produce values only when subscribed). The choice depends on whether you need lazy evaluation and the cost of evaluating unnecessary sub-expressions.

---

## Q40: How do you implement a handler chain with timeout support?

**A:** Timeout support ensures that handlers do not execute indefinitely. The chain manager sets a timeout for the entire chain or for individual handlers. If a handler exceeds its timeout, the chain is aborted and an error is returned.

The implementation uses a timer thread or scheduled executor that monitors handler execution. If the timer fires before the handler completes, the chain manager interrupts the handler thread and returns a timeout error. In Java, `Future.cancel(true)` interrupts the handler thread.

Timeout support requires handlers to be interruptible: they must periodically check for interruption and clean up resources when interrupted. Handlers that perform blocking I/O should use interruptible I/O operations. The timeout may be per-request, per-handler, or per-chain, depending on the requirements.

---

## Q41: What is the Interpreter pattern's relationship to the Composite pattern?

**A:** The Interpreter pattern uses the Composite pattern for its AST. The AST is a tree structure where each node is either a terminal (leaf) or a non-terminal (composite). The Composite pattern provides the structure; the Interpreter pattern provides the evaluation logic.

Each node in the AST implements a common `interpret()` interface. Terminal nodes implement `interpret()` by returning a value directly. Non-terminal nodes implement `interpret()` by calling `interpret()` on their children and combining the results. This is the Composite pattern's uniform treatment of individual objects and compositions.

The relationship is so close that the Interpreter pattern is sometimes considered a specialized application of the Composite pattern. The key addition is the evaluation semantics: the Composite pattern does not specify how to process the tree, while the Interpreter pattern defines how to evaluate it.

---

## Q42: How do you handle side effects in the Interpreter pattern?

**A:** Side effects are actions that modify external state (writing to a file, modifying a global variable, making a network call). In the Interpreter pattern, side effects complicate evaluation because they make the order of evaluation important and can cause unexpected behavior.

The simplest approach is to make the interpreter pure (no side effects): `interpret()` returns a value without modifying external state. Side effects are collected as a list of actions that are executed after evaluation completes. This separates evaluation from execution.

For interpreters that must support side effects during evaluation (e.g., variable assignment), the context object manages the mutable state. Side effects are contained within the context, and the interpreter's evaluation logic is still deterministic. For distributed or concurrent interpreters, side effects must be coordinated to avoid conflicts.

---

## Q43: What is the difference between a synchronous and asynchronous mediator?

**A:** A synchronous mediator processes colleague messages in the same thread as the caller. When colleague A sends a message through the mediator, the mediator synchronously notifies colleagues B and C before returning to A. This is simpler but can block the caller during processing.

An asynchronous mediator dispatches messages to colleagues on separate threads or via a message queue. Colleague A sends a message and continues immediately. The mediator notifies B and C asynchronously. This is more responsive but requires handling message ordering, error propagation, and result collection asynchronously.

The choice depends on the use case: synchronous mediators are suitable for simple, fast interactions. Asynchronous mediators are essential for long-running operations, UI responsiveness, and distributed systems. A hybrid approach uses synchronous notification for fast operations and asynchronous for slow ones.

---

## Q44: How does the Chain of Responsibility pattern handle handler failures?

**A:** Handler failures can occur due to exceptions, timeouts, or invalid input. The chain must handle these failures gracefully without breaking the entire chain.

Strategies include: try-catch blocks around each handler (the chain continues if a handler fails), fallback handlers (a default handler that processes the request if all others fail), circuit breakers (skip a handler that has failed repeatedly), and retry logic (retry a failed handler before moving to the next).

The chain manager may also implement compensation: if a handler fails after partially processing the request, the chain may need to undo the partial processing before continuing. The error handling strategy should be configurable per handler, as different handlers have different failure modes and recovery strategies.

---

## Q45: What is the difference between a stateless and stateful mediator?

**A:** A stateless mediator does not maintain any state between colleague interactions. It simply routes messages based on the current message and the mediator's logic. Each interaction is independent of previous interactions.

A stateful mediator maintains state that accumulates over time. This state may include: colleague registration information, message history, aggregate statistics, or workflow state. Stateful mediators can make decisions based on past interactions.

Stateless mediators are simpler, more predictable, and easier to test and scale (any instance can handle any message). Stateful mediators are more powerful but require careful state management (persistence, replication, consistency). In distributed systems, stateless mediators can be horizontally scaled, while stateful mediators require state replication or partitioning.

---

## Q46: How do you implement a handler chain with retry logic?

**A:** Retry logic automatically retries a failed handler before moving to the next handler in the chain. The implementation wraps each handler with a retry decorator that catches exceptions and retries the handler a configurable number of times.

The retry decorator may implement: fixed delay (wait a constant time between retries), exponential backoff (wait an increasing time), jitter (add randomness to prevent thundering herd), and maximum retry count (give up after N failures).

The retry logic must handle: idempotency (retries should not cause duplicate side effects), timeout (retries should not extend beyond the overall request timeout), and error classification (retry only on transient errors, not on permanent errors like validation failures).

---

## Q47: What is the difference between the Interpreter pattern and a compiler?

**A:** The Interpreter pattern evaluates ASTs directly, typically in a tree-walking fashion. Each node's `interpret()` method computes the result for that node. This is simple but slow for large programs.

A compiler translates the AST (or source code) into another form (machine code, bytecode, intermediate representation) before execution. The compilation phase can perform optimizations (constant folding, dead code elimination, inlining) that the interpreter cannot.

The Interpreter pattern is suitable for simple, domain-specific languages that are evaluated frequently but are small. Compilers are suitable for complex languages where performance matters. Some interpreters use compilation internally (JIT compilation) to get the simplicity of interpretation with the performance of compilation.

---

## Q48: How does the Mediator pattern support the Dependency Inversion Principle?

**A:** The Mediator pattern supports the Dependency Inversion Principle (DIP) because both high-level and low-level components depend on the mediator abstraction. Colleagues depend on the mediator interface, not on each other.

The mediator interface defines the contract for communication. Concrete mediators implement this interface. Colleagues depend on the mediator interface, not on the concrete mediator. This allows different mediator implementations to be used without changing colleagues.

DIP is satisfied because the abstraction (mediator interface) is at the center of the dependency graph, with both high-level policies (business logic colleagues) and low-level details (infrastructure colleagues) depending on it. This inverts the natural dependency direction where low-level components would depend on high-level ones.

---

## Q49: What is the difference between a handler chain and a filter chain?

**A:** A handler chain passes a request through handlers, where each handler may process the request or pass it along. The focus is on who handles the request.

A filter chain transforms the request and/or response as it passes through. Each filter applies a transformation (adding headers, encoding content, logging). The focus is on how the request/response is modified.

In practice, the terms are often used interchangeably. However, a filter typically modifies the request or response without deciding whether to handle it, while a handler may decide to handle (consume) the request. Filters are transparent (they don't change the request's intent); handlers may change the request's intent (rejecting it, redirecting it).

---

## Q50: How do you implement a global error handler in the Chain of Responsibility pattern?

**A:** A global error handler catches exceptions from any handler in the chain and provides a uniform error response. It is typically the last handler in the chain, wrapping the entire chain in a try-catch block.

The implementation may use a decorator around the chain executor, a try-catch in the chain manager, or a dedicated error handler at the end of the chain. The error handler logs the exception, generates a user-friendly error response, and may trigger alerting or monitoring.

For more sophisticated error handling, the global handler may implement error classification (transient vs. permanent), error aggregation (collecting multiple errors from the chain), and error recovery (retrying the entire chain with different parameters). The error handler should also ensure that resources are cleaned up properly (closing connections, releasing locks) even when errors occur.


## Q51: How do you implement a typed mediator with compile-time safety?

**A:** A typed mediator ensures that colleagues communicate through type-safe channels, preventing runtime errors from invalid message types. The implementation uses generics to parameterize the mediator by the message types it handles.

In Java, this can be achieved with a `Map<Class<?>, List<Consumer<?>>>` where each message type is associated with a list of handlers. The `send()` method is generic and dispatches to handlers of the correct type. TypeScript achieves similar safety with discriminated unions and mapped types.

The typed mediator eliminates the need for message type checking at runtime and makes the API self-documenting. The compiler enforces that handlers match their message types, preventing common bugs like handling the wrong message type or sending a message that no handler understands.

**Example:**
```java
class TypedMediator {
    private final Map<Class<?>, List<Consumer<?>>> handlers = new HashMap<>();

    <T> void register(Class<T> type, Consumer<T> handler) {
        handlers.computeIfAbsent(type, k -> new ArrayList<>()).add(handler);
    }

    @SuppressWarnings("unchecked")
    <T> void send(T message) {
        for (Consumer h : handlers.getOrDefault(message.getClass(), List.of())) {
            h.accept(message);
        }
    }
}
```

---

## Q52: What is the difference between a grammar-based and pattern-matching interpreter?

**A:** A grammar-based interpreter uses a formal grammar (BNF, EBNF) to define the language and a parser to build an AST. The interpreter evaluates the AST. This approach supports complex, nested expressions and operator precedence.

A pattern-matching interpreter uses regular expressions or string matching to identify and evaluate expressions. It does not build an AST; instead, it matches patterns and evaluates them directly. This approach is simpler but limited to flat expressions without nesting.

Grammar-based interpreters are more powerful and flexible but require more code (grammar definition, parser, AST classes). Pattern-matching interpreters are simpler to implement but cannot handle complex grammars. The choice depends on the complexity of the language being interpreted.

---

## Q53: How do you optimize an interpreter for frequently evaluated expressions?

**A:** Optimization strategies for frequently evaluated expressions include: caching (memoizing the result of expressions with the same inputs), compilation (translating the AST to bytecode or machine code for faster execution), and constant folding (evaluating constant expressions at parse time).

Caching stores the result of previous evaluations and returns the cached result when the same inputs are provided. This is effective for expressions with limited input domains. Compilation translates the AST into a more efficient representation (bytecode for a virtual machine, or native code via JIT). Constant folding evaluates expressions that contain only constants during parsing, storing the result directly.

Additional optimizations include: common subexpression elimination (reusing results of identical sub-expressions), dead code elimination (removing unreachable code), and inlining (replacing function calls with the function body). These optimizations are typically performed on the AST before evaluation.

---

## Q54: What is the difference between a handler chain and a责任链 (responsibility chain) in Chinese software engineering terminology?

**A:** The terms are identical: 责任链 (zérèn liàn) is the direct Chinese translation of "Chain of Responsibility." The pattern was described by the Gang of Four in their 1994 book "Design Patterns: Elements of Reusable Object-Oriented Software," and the Chinese translation uses 责任链.

The pattern's behavior is the same regardless of language: a request is passed along a chain of handlers, and each handler decides whether to process the request or pass it to the next handler. The implementation details may vary based on language features (interfaces in Java, traits in Rust, protocols in Go), but the pattern's intent and structure are universal.

Understanding the pattern across languages is important for international teams and for reading Chinese-language design pattern resources, which are abundant given China's large software engineering community.

---

## Q55: How do you implement a mediator with event sourcing for auditability?

**A:** An event-sourced mediator logs every interaction between colleagues as an immutable event. Instead of directly routing messages, the mediator records each message as an event in an event store. Colleagues subscribe to events from the store and react accordingly.

The event store provides a complete audit trail of all mediator interactions. This is valuable for debugging (replaying the event sequence to understand behavior), compliance (proving that interactions followed business rules), and analytics (analyzing interaction patterns).

The implementation uses an append-only log for the event store. The mediator publishes events to the log, and colleagues subscribe to relevant events. The mediator may also maintain materialized views (projections) for efficient querying. For replay, events can be reprocessed from the beginning of the log.

---

## Q56: What is the difference between a chain of responsibility and a middleware pipeline in .NET?

**A:** .NET middleware follows the Chain of Responsibility pattern with a specific convention: each middleware receives the HTTP context and a `next` delegate. The middleware calls `next()` to pass the request to the next middleware. The request flows forward through middleware, and the response flows backward.

The key difference from a generic chain of responsibility is that .NET middleware has a specific contract (HttpContext, next delegate) and a specific flow model (nested, not sequential). Middleware can perform logic before and after calling `next()`, creating a Russian-doll structure.

.NET middleware is configured in `Startup.cs` using `app.Use()` or `app.UseMiddleware()`. The order of configuration determines the order of execution. This is a specific, opinionated implementation of the Chain of Responsibility pattern tailored for HTTP request processing.

---

## Q57: How do you handle concurrent modifications in a mediator's colleague registry?

**A:** Concurrent modifications to the mediator's colleague registry (adding or removing colleagues while messages are being processed) can cause race conditions, ConcurrentModificationExceptions, or incorrect message routing.

Solutions include: copy-on-write (creating a new colleague list for each modification, so message processing uses a snapshot), read-write locks (allowing concurrent reads but exclusive writes), concurrent data structures (ConcurrentHashMap for the colleague registry), and actor-model approaches (each colleague is an actor with a mailbox, and the mediator sends messages to mailboxes).

The choice depends on the frequency of modifications vs. message processing. If colleagues are rarely added or removed, copy-on-write is simplest. If modifications are frequent, a concurrent data structure is more efficient. The key guarantee is that message processing should not be affected by concurrent registry modifications.

---

## Q58: What is the difference between a top-down and bottom-up interpreter?

**A:** A top-down interpreter starts at the root of the AST (the start symbol) and recursively evaluates sub-expressions. This is the standard recursive approach used in most Interpreter pattern implementations.

A bottom-up interpreter starts at the leaves of the AST (terminal expressions) and combines results upward toward the root. This approach evaluates leaf nodes first, then uses their results to evaluate parent nodes, continuing until the root is evaluated.

Bottom-up evaluation is natural for certain grammars (e.g., arithmetic expressions where operands are evaluated before operators). It can be more efficient for some tree structures because it avoids redundant computation (each node is evaluated exactly once). However, it requires storing intermediate results, which may use more memory.

---

## Q59: How do you implement a handler chain with circuit breaker support?

**A:** Circuit breakers prevent cascading failures by detecting when a handler is failing and short-circuiting the chain to avoid further failures. The circuit breaker tracks handler failures and enters an "open" state after a threshold is exceeded.

When the circuit is open, requests are immediately failed (or routed to a fallback) without calling the handler. After a timeout, the circuit enters a "half-open" state and allows a test request through. If the test succeeds, the circuit closes; if it fails, it reopens.

The implementation wraps each handler with a circuit breaker decorator that tracks success/failure counts, manages state transitions (closed → open → half-open → closed), and provides fallback behavior. The circuit breaker pattern is essential for building resilient distributed systems where handler failures can cascade.

**Example:**
```python
class CircuitBreaker:
    def __init__(self, handler, failure_threshold=5, timeout=60):
        self.handler = handler
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "closed"
        self.last_failure_time = 0

    def handle(self, request):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError("Circuit is open")
        try:
            result = self.handler.handle(request)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

---

## Q60: What is the difference between a synchronous and asynchronous interpreter?

**A:** A synchronous interpreter evaluates the AST in the same thread as the caller. Each `interpret()` call blocks until the result is available. This is simple and predictable but can block during slow operations (I/O, network calls).

An asynchronous interpreter evaluates the AST using asynchronous operations. Each `interpret()` call returns a future or promise that resolves when the result is available. This allows the interpreter to handle I/O-bound operations without blocking.

Asynchronous interpretation is useful for interpreters that evaluate expressions involving network calls, database queries, or other I/O operations. The AST evaluation can issue multiple I/O requests in parallel and collect results as they arrive. This is the model used in reactive and event-driven systems.

---

## Q61: How do you implement a mediator with undo/redo support?

**A:** A mediator with undo/redo support records colleague interactions and can reverse them. Each interaction (message sent, state change) is recorded as a command or event. The undo operation reverses the last interaction; the redo operation re-applies it.

The implementation uses the Command pattern: each colleague interaction is encapsulated as a command object with `execute()` and `undo()` methods. The mediator maintains an undo stack and a redo stack. When a colleague sends a message, the mediator creates a command and pushes it onto the undo stack.

When the user requests undo, the mediator pops the top command from the undo stack, calls `undo()`, and pushes it onto the redo stack. Redo reverses this flow. The mediator must handle concurrent interactions and ensure that undo/redo operations are consistent with the current state.

---

## Q62: What is the difference between a grammar and a parse tree?

**A:** A grammar is a set of rules that define the valid structure of a language. A parse tree (or concrete syntax tree) is a tree representation of a specific sentence in the language, showing how the sentence is derived from the grammar rules.

The grammar is the abstract specification; the parse tree is the concrete representation of a specific input. The grammar may have many possible parse trees (for ambiguous grammars), while each input sentence has at most one parse tree (for unambiguous grammars).

An Abstract Syntax Tree (AST) is a simplified parse tree that omits syntactic details (parentheses, whitespace, delimiters) and focuses on the semantic structure. The Interpreter pattern typically uses ASTs rather than parse trees because ASTs are simpler and more efficient to evaluate.

---

## Q63: How do you implement a handler chain with rate limiting per handler?

**A:** Rate limiting per handler restricts the number of requests each handler can process within a time window. This prevents any single handler from being overwhelmed and ensures fair resource allocation.

The implementation wraps each handler with a rate limiter that tracks request counts using a token bucket or sliding window algorithm. Before calling the handler, the rate limiter checks if a token is available. If not, the request is queued, rejected, or delayed.

The rate limiter may be per-handler (each handler has its own limit), per-request-type (different limits for different request types), or per-user (different limits for different users). The configuration should be externalized to allow adjustment without code changes.

---

## Q64: What is the difference between a command pattern and a message pattern?

**A:** A command pattern encapsulates an action as an object. The command has a clear intent (what to do) and may support undo, queuing, and logging. Commands are typically processed by a single handler.

A message pattern encapsulates information as an object. The message has no inherent action; it simply carries data. Messages are typically published to a message bus and consumed by multiple subscribers.

The key distinction is in intent: commands are requests to perform actions; messages are notifications that something happened. Commands are point-to-point (sent to a specific handler); messages are pub-sub (broadcast to all subscribers). Commands may be rejected; messages are simply recorded. In event-driven architectures, commands trigger actions, and messages report results.

---

## Q65: How do you implement an interpreter with type checking?

**A:** Type checking in the Interpreter pattern verifies that operations are applied to compatible types. The interpreter evaluates the AST in two passes: the first pass (type checking) verifies type compatibility; the second pass (evaluation) computes the result.

During type checking, each node computes its type based on the types of its children. Terminal nodes have known types (integer, string, boolean). Non-terminal nodes compute their result type based on the operation and operand types (integer + integer = integer, string + string = string).

Type errors are reported during the type-checking pass, before evaluation begins. This catches errors early and provides better error messages. The type information can also be used for optimization (using integer arithmetic instead of floating-point when types are known).

---

## Q66: What is the difference between a handler chain and a decorator chain?

**A:** A handler chain passes a request through handlers, where each handler may process the request or pass it along. The focus is on handling the request.

A decorator chain wraps an object with additional behavior. Each decorator implements the same interface as the wrapped object and adds pre/post-processing. The focus is on enhancing the wrapped object's behavior.

The key difference is in the relationship between chain elements: handlers are independent (they don't wrap each other), while decorators are nested (each decorator wraps the previous one). Handlers form a flat sequence; decorators form a nested structure. In practice, many middleware chains use a decorator-like structure where each middleware wraps the next.

---

## Q67: How do you handle infinite loops in the Interpreter pattern?

**A:** Infinite loops in the Interpreter pattern occur when the AST contains cycles (a node that is its own ancestor) or when the evaluation logic has infinite recursion. Since ASTs are trees (acyclic by definition), cycles are prevented during parsing.

Infinite recursion occurs when a non-terminal expression's `interpret()` method calls itself without a base case. This is a bug in the grammar or interpreter implementation. Solutions include: tracking recursion depth (throwing an exception after a maximum depth), using iterative evaluation (explicit stack instead of recursion), and detecting cycles in the evaluation logic.

The interpreter should also handle infinite data structures (lazy generators, recursive data types) by limiting the number of elements evaluated. This prevents the interpreter from running forever when evaluating expressions that produce infinite sequences.

---

## Q68: What is the difference between a mediator and a message broker?

**A:** A mediator is an in-process design pattern that coordinates interactions between objects within a single application. It is typically synchronous, in-memory, and fast. The mediator knows about all colleagues and routes messages directly.

A message broker is a distributed infrastructure component that routes messages between processes, services, or applications. It is typically asynchronous, durable, and supports features like persistence, replication, and consumer groups. The broker does not know about producers and subscribers; it routes based on topics or queues.

The mediator is used for intra-service communication; the message broker is used for inter-service communication. Some systems bridge the two: a mediator within a service coordinates colleagues, and for cross-service communication, the mediator publishes messages to a broker.

---

## Q69: How do you implement a handler chain with priority queues?

**A:** A priority-based handler chain uses a priority queue to determine the order in which handlers are executed. Higher-priority handlers execute before lower-priority ones, regardless of registration order.

The implementation maintains a `PriorityQueue` of handlers, ordered by priority. When a request arrives, handlers are dequeued in priority order. Each handler may modify the queue (add new handlers, change priorities) before the next handler is dequeued.

Priority queues are essential in real-time systems (safety-critical handlers before routine ones), UI frameworks (input handlers before background processing), and middleware (authentication before logging). The priority may be static (defined at registration) or dynamic (changed based on request characteristics).

---

## Q70: What is the difference between a recursive and tabled interpreter?

**A:** A recursive interpreter evaluates the AST by recursive calls. Each node's `interpret()` method calls `interpret()` on its children. This can cause redundant computation when the same sub-expression appears multiple times in the AST.

A tabled interpreter (or memoizing interpreter) stores the results of previously evaluated sub-expressions in a table (hash map). When a sub-expression is encountered, the interpreter first checks the table. If the result is cached, it is returned directly. Otherwise, the sub-expression is evaluated, and the result is stored in the table.

Tabled interpretation eliminates redundant computation, making it significantly faster for ASTs with shared sub-expressions. The trade-off is memory usage for the table. This optimization is particularly valuable for expressions with common sub-expressions (e.g., `(a + b) * (a + b)` where `a + b` is evaluated twice in a recursive interpreter).

---

## Q71: How do you implement a mediator with publish-subscribe semantics?

**A:** A mediator with publish-subscribe semantics allows colleagues to publish events and subscribe to events of interest. The mediator acts as an event bus, routing events from publishers to subscribers.

The implementation maintains a map of event types to subscriber lists. When a colleague publishes an event, the mediator looks up subscribers for that event type and notifies them. Subscribers can register for specific event types or for all events.

This approach combines the Mediator's coordination role with the Observer pattern's decoupled notification. Colleagues do not know about each other; they only know the mediator. The mediator encapsulates the routing logic and can implement filtering, transformation, and aggregation of events.

---

## Q72: What is the difference between a parser and an interpreter?

**A:** A parser converts source code (text) into an AST (tree structure). It performs lexical analysis (tokenization) and syntactic analysis (building the AST). The parser's output is the AST.

An interpreter evaluates the AST to produce a result. It traverses the AST and computes the result of each node. The interpreter's input is the AST (produced by the parser).

In the Interpreter pattern, the parser and interpreter are separate concerns. The parser is typically generated by a parser generator or hand-written. The interpreter is implemented as AST node classes with `interpret()` methods. Some systems combine parsing and interpretation (eval in Python, Function in JavaScript), but the underlying process is still parse-then-interpret.

---

## Q73: How do you implement a handler chain with asynchronous processing?

**A:** A handler chain with asynchronous processing allows handlers to execute on separate threads or via a thread pool. This is essential for handlers that perform I/O operations (network calls, database queries) that would block the main thread.

The implementation uses a thread pool or executor service to run handlers asynchronously. The chain manager submits each handler to the executor and waits for the result (using `Future.get()` or callbacks). The chain may support parallel execution (all handlers run concurrently) or sequential execution (handlers run one after another, each on a separate thread).

Async handler chains must handle: thread synchronization (ensuring handlers complete before the chain continues), error propagation (capturing exceptions from handler threads), and timeout (canceling handlers that take too long). The implementation should use `CompletableFuture` (Java), `asyncio` (Python), or `Promise` (JavaScript) for clean asynchronous composition.

---

## Q74: What is the difference between a BNF grammar and an EBNF grammar?

**A:** BNF (Backus-Naur Form) is a formal notation for defining grammars. It uses the syntax `symbol ::= expression` where `expression` is a combination of terminals, non-terminals, and operators (`|` for alternatives, concatenation for sequences).

EBNF (Extended Backus-Naur Form) adds extensions to BNF: `{}` for zero or more repetitions, `[]` for optional elements, and `()` for grouping. These extensions make grammars more concise and readable.

For the Interpreter pattern, EBNF is generally preferred because it produces cleaner, more readable grammar definitions. However, BNF is more fundamental and can express everything EBNF can (with more verbose rules). Parser generators typically accept BNF or EBNF variants and produce parsers that build ASTs.

---

## Q75: How do you implement a mediator for a distributed system?

**A:** A distributed mediator coordinates interactions between services across network boundaries. Unlike an in-process mediator, a distributed mediator must handle network latency, message ordering, failure detection, and partial failures.

The implementation uses a message broker (Kafka, RabbitMQ, NATS) as the communication backbone. The mediator publishes messages to topics, and services subscribe to relevant topics. The mediator maintains distributed state (using a distributed cache or database) for coordination logic.

Key design decisions include: message ordering (partitioning by service ID for per-service ordering), exactly-once delivery (using idempotent consumers and transactional outbox), failure handling (dead letter queues, retry with backoff), and monitoring (distributed tracing, message lag monitoring). The mediator may be replicated for high availability, with leader election for coordination.


## Q76: How would you design a production-grade interpreter for a domain-specific language?

**A:** A production-grade DSL interpreter requires a robust architecture with multiple phases: lexical analysis (tokenizer), syntactic analysis (parser), semantic analysis (type checking, symbol resolution), optimization, and evaluation. Each phase is a separate compiler pass.

The architecture includes: a lexer that converts source text to tokens, a parser that builds an AST from tokens, a semantic analyzer that validates types and resolves references, an optimizer that transforms the AST for efficiency, and an evaluator that computes results.

For production use, the interpreter must handle: error recovery (reporting multiple errors without aborting), source location tracking (mapping AST nodes back to source positions for error messages), incremental evaluation (re-evaluating only changed parts), and extensibility (adding new language features without rewriting the core). The interpreter should be benchmarked against realistic workloads and profiled for performance bottlenecks.

---

## Q77: What is the difference between an interpreter and a transpiler?

**A:** An interpreter evaluates source code directly, producing results without generating an intermediate representation. A transpiler (source-to-source compiler) translates source code from one language to another language, producing equivalent code in the target language.

Interpreters are simpler (no code generation phase) but slower (re-evaluate on each execution). Transpilers are more complex (must generate correct code in the target language) but produce code that can be compiled and optimized by the target language's compiler.

Many modern tools blur the line: Babel transpiles JavaScript to backward-compatible JavaScript; TypeScript transpiles to JavaScript; Kotlin transpiles to Java bytecode. These are technically transpilers but are often called compilers. The Interpreter pattern is for evaluating expressions; transpilation is for translating between languages.

---

## Q78: How do you handle concurrency in a mediator-based system?

**A:** Concurrency in a mediator-based system arises when multiple colleagues send messages simultaneously or when the mediator processes messages on multiple threads. The mediator must handle concurrent message processing without race conditions or data corruption.

Strategies include: single-threaded mediator (all messages are processed sequentially on one thread, using a message queue), multi-threaded mediator with synchronization (using locks or atomic operations to protect shared state), and actor-based mediator (each colleague is an actor with a mailbox, and the mediator sends messages to mailboxes).

The choice depends on the throughput requirements and the nature of the colleague interactions. Single-threaded mediators are simplest and avoid concurrency issues but have limited throughput. Multi-threaded mediators provide higher throughput but require careful synchronization. Actor-based mediators are the most scalable but require the actor model's programming paradigm.

---

## Q79: What is the difference between a chain of responsibility and a decorator pattern?

**A:** Both patterns wrap objects with additional behavior, but they serve different purposes. The Chain of Responsibility passes a request through a sequence of handlers, where each handler may process the request or pass it along. The Decorator wraps an object with additional behavior, enhancing its functionality.

The key difference: in a chain, handlers are independent (they don't wrap each other); in a decorator chain, decorators are nested (each wraps the previous). Chains are for routing requests; decorators are for adding behavior. Chains may short-circuit; decorators always delegate.

In practice, the patterns overlap: middleware chains use decorator-like nesting (each middleware wraps the next), and decorator chains may implement chain-like behavior (each decorator decides whether to delegate). The distinction is in intent: Chain of Responsibility is for request routing; Decorator is for behavior enhancement.

---

## Q80: How do you implement a mediator with event-driven architecture for microservices?

**A:** An event-driven mediator for microservices uses a message broker as the communication backbone. Each microservice is a colleague that publishes events and subscribes to events of interest. The mediator (or orchestration service) coordinates complex workflows across services.

The implementation uses: an event broker (Kafka, NATS) for message delivery, an event schema registry for message format validation, saga orchestration for distributed transactions, and CQRS for separating read and write models.

The mediator publishes coordination events (e.g., "order created," "payment processed") and services subscribe to relevant events. Each service processes events independently and publishes its own events. The mediator may maintain workflow state to track the progress of multi-step operations and handle compensation (saga pattern) when steps fail.

---

## Q81: What is the difference between an AST interpreter and a bytecode interpreter?

**A:** An AST interpreter traverses the AST directly, evaluating each node as it encounters it. This is simple but slow because the tree traversal overhead is significant for large programs.

A bytecode interpreter first compiles the AST to a linear sequence of bytecode instructions (a flat list of operations). The bytecode is then executed by a virtual machine that interprets each instruction. This is faster because linear instruction sequences have better cache locality and lower traversal overhead than trees.

Bytecode interpreters add a compilation phase but gain significant performance improvements. Most production interpreters (CPython, Ruby MRI, Lua) use bytecode interpretation. The JIT (Just-In-Time) compilation approach goes further, dynamically compiling hot bytecode paths to native code for even better performance.

---

## Q82: How do you test an interpreter for correctness and completeness?

**A:** Correctness testing verifies that the interpreter produces the correct result for valid inputs. Completeness testing verifies that the interpreter handles all valid inputs (no crashes or undefined behavior) and correctly rejects invalid inputs.

Test strategies include: unit tests for individual AST nodes (testing each `interpret()` method), integration tests for complete expressions (testing parsing and evaluation together), property-based testing (generating random valid expressions and verifying properties like associativity and commutativity), and fuzz testing (feeding random or malformed input to find crashes).

The test suite should cover: all grammar rules, edge cases (empty input, very large numbers, deeply nested expressions), error handling (invalid syntax, undefined variables, type errors), and performance (ensuring the interpreter handles large inputs within acceptable time). Test coverage should be measured and tracked.

---

## Q83: What is the difference between a handler chain and an aspect-oriented programming (AOP) aspect?

**A:** A handler chain is a sequence of handlers that process a request, where each handler may process or pass along the request. An AOP aspect is a cross-cutting concern (logging, security, transaction management) that is applied to multiple points in the codebase.

The key difference: handler chains are explicit (the chain is configured and visible in the code), while AOP aspects are implicit (the aspect is applied through configuration or annotations, and its presence is not visible in the business code). Handler chains are for request processing; AOP aspects are for cross-cutting concerns.

In practice, AOP frameworks (Spring AOP, AspectJ) often implement aspects as handler chains under the aspects the application. The aspect framework intercepts method calls, applies the aspect logic, and delegates to the original method. This is essentially a handler chain where the handlers are aspects and the target method is the final handler.

---

## Q84: How do you implement a grammar with ambiguity handling in the Interpreter pattern?

**A:** Ambiguous grammars produce multiple valid parse trees for the same input. The Interpreter pattern requires unambiguous grammars because each expression must have exactly one interpretation. Ambiguity must be resolved during grammar design or parsing.

Grammar restructuring eliminates ambiguity: adding precedence rules (making multiplication bind tighter than addition), associativity rules (left-associative for subtraction, right-associative for exponentiation), and explicit grouping (parentheses). The grammar is transformed into an unambiguous equivalent.

Parser techniques handle remaining ambiguity: operator precedence climbing (for expression grammars), GLR parsing (for ambiguous grammars that cannot be made unambiguous), and conflict resolution rules (yacc/bison's shift-reduce and reduce-reduce conflict resolution). The goal is a deterministic parse that produces a unique AST for each valid input.

---

## Q85: What is the difference between a mediator and an event aggregator?

**A:** An event aggregator is a simple publish-subscribe component that receives events from publishers and distributes them to subscribers. It has no knowledge of the event semantics; it just routes messages.

A mediator is a more sophisticated component that encapsulates complex interaction logic between objects. It may route events, transform them, make decisions, and coordinate multi-step workflows. The mediator contains business logic; the event aggregator does not.

The event aggregator is a building block; the mediator is an architectural component. A mediator may use an event aggregator internally for event routing, but it adds coordination logic on top. The event aggregator is for decoupling; the mediator is for coordination.

---

## Q86: How do you handle memory management in a long-running interpreter?

**A:** Long-running interpreters must manage memory carefully to avoid leaks and excessive consumption. Strategies include: garbage collection (relying on the runtime's GC), reference counting (counting references to objects and freeing when the count reaches zero), arena allocation (allocating objects in arenas and freeing entire arenas at once), and manual memory management (explicit allocation and deallocation).

For AST-based interpreters, memory leaks occur when AST nodes are retained after evaluation (e.g., in a cache or closure). The interpreter should release AST references after evaluation unless they are needed for re-evaluation.

For interpreters that evaluate expressions repeatedly (like a calculator or template engine), object pooling reuses AST nodes and evaluation contexts instead of creating new ones. This reduces GC pressure and improves performance. Memory profiling tools (Valgrind, Java VisualVM, Python tracemalloc) are essential for identifying and fixing memory issues.

---

## Q87: What is the difference between a handler chain and a pipeline in Apache Camel?

**A:** Apache Camel implements the Enterprise Integration Patterns (EIP), including the Pipes and Filters pattern (similar to Chain of Responsibility) and the Message Router pattern. A Camel route is a pipeline of processing steps where messages flow through endpoints, processors, and transforms.

The key difference from a generic handler chain is that Camel routes are declarative (defined in DSL or XML), support multiple protocols (HTTP, JMS, File), and include built-in EIP implementations (aggregator, splitter, content-based router). Camel routes are more than handler chains; they are integration pipelines.

Camel's processing model combines Chain of Responsibility (each processor handles the message), Decorator (processors wrap the message with additional behavior), and Mediator (routes coordinate interactions between systems). Understanding these patterns helps in designing effective Camel routes.

---

## Q88: How do you implement a handler chain with dynamic composition based on request attributes?

**A:** Dynamic composition means the handler chain is assembled at runtime based on request attributes (user role, request type, content type, priority). Different requests may follow different chains even if they arrive at the same entry point.

The implementation uses a chain resolver that examines the request and selects the appropriate handlers. The resolver may use a configuration file, rules engine, or code-based logic to determine the chain composition. The selected handlers are assembled into a chain for this specific request.

This approach is common in API gateways (routing based on URL, headers, or JWT claims), workflow engines (selecting steps based on document type), and security systems (applying different validation chains based on user permissions). The chain resolver must be efficient to avoid adding latency to request processing.

---

## Q89: What is the difference between an interpreter and a query engine?

**A:** An interpreter evaluates expressions or programs in a language, producing a result. A query engine evaluates queries against a data source, returning matching data. A query engine is a specialized interpreter for query languages (SQL, GraphQL, Elasticsearch DSL).

Query engines often include optimizations that general-purpose interpreters do not: query planning (determining the most efficient execution strategy), indexing (using indexes to speed up lookups), caching (storing query results for reuse), and pushdown optimization (filtering data at the source rather than in the engine).

The Interpreter pattern can be used to implement a query engine: the grammar defines the query language, the parser builds an AST, and the interpreter evaluates the AST against a data source. The optimization phase (query planning, index selection) is an additional compiler pass that transforms the AST before evaluation.

---

## Q90: How do you handle security in a chain of responsibility pattern?

**A:** Security in a Chain of Responsibility pattern involves placing security handlers early in the chain (authentication, authorization, input validation) and ensuring that security cannot be bypassed by later handlers.

The security handler should be the first or second handler in the chain, processing the request before any business logic. It should reject unauthorized requests immediately, preventing them from reaching sensitive handlers. The chain should not be configurable in a way that allows security handlers to be removed or reordered.

Additional security considerations: input sanitization (preventing injection attacks), rate limiting (preventing abuse), output encoding (preventing XSS), and audit logging (tracking all requests for security analysis). The chain should also handle security exceptions gracefully, returning appropriate error responses without leaking sensitive information.

---

## Q91: What is the difference between a mediator and a workflow engine?

**A:** A mediator coordinates interactions between a fixed set of objects. The interaction logic is encoded in the mediator's methods. The mediator is suitable for simple, well-defined interaction patterns.

A workflow engine executes a sequence of activities (tasks, steps, actions) with branching, parallel execution, error handling, and human interaction points. The workflow is defined externally (in a DSL, XML, or visual designer) and executed by the engine.

The mediator is a design pattern for structuring code; the workflow engine is an infrastructure component for managing business processes. A mediator may be used within a workflow engine to coordinate activities, and a workflow engine may use the mediator pattern to coordinate services. The key distinction is in scope and complexity: mediators handle simple interactions; workflow engines handle complex, long-running processes.

---

## Q92: How do you implement an interpreter with support for user-defined functions?

**A:** User-defined functions in the Interpreter pattern require a function registry that maps function names to function definitions. A function definition includes the parameter names and the body (an AST node).

When the interpreter encounters a function call, it looks up the function in the registry, creates a new scope with the parameter bindings, evaluates the function body in that scope, and returns the result. This requires scope management (nested scopes for closures) and a way to represent functions as first-class values.

The implementation may use: a symbol table (mapping names to function definitions), a closure (a function body plus its enclosing scope), and higher-order functions (functions that accept or return other functions). The function registry can be pre-populated with built-in functions and extended with user-defined functions at runtime.

---

## Q93: What is the difference between a chain of responsibility and a policy-based design?

**A:** A policy-based design uses interchangeable policy objects to implement different strategies for a specific concern. Each policy is a self-contained implementation of a specific behavior. The context selects the appropriate policy at compile time or runtime.

A chain of responsibility passes a request through a sequence of handlers, where each handler may process the request or pass it along. The chain is dynamic; handlers can be added or removed at runtime.

The key difference: policies are typically static (selected once at configuration time) and mutually exclusive (only one policy is active), while chains are dynamic (handlers can be added or removed) and cumulative (multiple handlers may process the same request). Policies are for swappable behavior; chains are for sequential processing.

---

## Q94: How do you implement a mediator with conflict resolution for collaborative editing?

**A:** Collaborative editing requires handling concurrent modifications to the same document. The mediator (or collaboration server) must resolve conflicts when multiple users edit the same section simultaneously.

Strategies include: Operational Transformation (OT) which transforms concurrent operations to maintain consistency, Conflict-free Replicated Data Types (CRDTs) which use mathematically guaranteed convergence, and Last-Writer-Wins (LWW) which uses timestamps to resolve conflicts.

The mediator receives operations from clients, transforms them against concurrent operations (OT), or merges them using CRDT semantics. The mediator then broadcasts the transformed operations to all clients. The choice between OT and CRDTs depends on the requirements: OT provides strong consistency but is complex; CRDTs provide eventual consistency but are simpler and more scalable.

---

## Q95: What is the difference between a handler chain and a request pipeline in ASP.NET Core?

**A:** ASP.NET Core's request pipeline is a specific implementation of the Chain of Responsibility pattern for HTTP request processing. Each middleware component in the pipeline receives the HTTP context and a `next` delegate. The middleware performs its logic and optionally calls `next()` to pass to the next middleware.

The pipeline is configured in `Program.cs` using `app.Use()`, `app.UseMiddleware()`, or extension methods. Middleware is executed in the order of registration. The pipeline supports short-circuiting (not calling `next()`), error handling (`app.UseExceptionHandler()`), and branching (`app.Map()` for path-based routing).

The ASP.NET Core pipeline is more than a generic handler chain: it includes built-in middleware for common concerns (authentication, CORS, routing, static files), supports dependency injection, and provides a rich API for request/response manipulation. Understanding the Chain of Responsibility pattern helps in designing effective middleware.

---

## Q96: How do you implement an interpreter with lazy evaluation semantics?

**A:** Lazy evaluation in the Interpreter pattern defers the evaluation of expressions until their values are needed. This is implemented using thunks (delayed computation objects) or by modifying the AST to represent unevaluated expressions.

Each AST node wraps its computation in a thunk. When `interpret()` is called, it returns a thunk instead of a value. The thunk is evaluated only when the value is accessed (via a `force()` method). This enables short-circuit evaluation (if-then-else only evaluates the taken branch) and infinite data structures.

The implementation must handle: memoization (caching the result of a thunk after the first evaluation), sharing (ensuring that the same thunk is not evaluated multiple times), and error handling (propagating errors from thunks). Lazy evaluation adds complexity but can significantly improve performance for conditional or selective evaluation.

---

## Q97: What is the difference between a mediator and a service locator?

**A:** A service locator is a registry that provides access to services by name or type. Clients query the locator to find and use services. The locator decouples clients from service implementations.

A mediator coordinates interactions between objects, encapsulating the interaction logic. The mediator actively routes messages and makes decisions; the service locator passively provides service references.

The key distinction: the mediator contains business logic (how objects interact); the service locator contains infrastructure logic (how to find services). A mediator may use a service locator to resolve colleague references, and a service locator may use a mediator pattern internally to coordinate service initialization. The mediator is for coordination; the service locator is for discovery.

---

## Q98: How do you handle versioning in a grammar for the Interpreter pattern?

**A:** Grammar versioning ensures that old expressions can still be interpreted as the language evolves. Strategies include: versioned grammar rules (each rule has a version number), backward-compatible extensions (new rules do not break old rules), and explicit version markers in the source (comments or directives that specify the grammar version).

The interpreter maintains a version-aware parser that can parse expressions from multiple grammar versions. The parser selects the appropriate grammar rules based on the version marker. For backward-compatible changes (adding new keywords, extending existing rules), the parser can handle multiple versions without explicit markers.

For incompatible changes (removing rules, changing semantics), the interpreter provides migration tools that transform old expressions to the new format. The versioning strategy should be documented and communicated to language users to ensure a smooth transition between versions.

---

## Q99: What is the difference between a chain of responsibility and a middleware pattern in Go?

**A:** Go's middleware pattern is a specific application of the Chain of Responsibility pattern for HTTP handlers. A middleware function takes an `http.Handler` and returns a new `http.Handler` that wraps the original with additional logic. This creates a decorator-like chain.

The Go middleware pattern is function-based (using closures) rather than class-based. Middleware functions are composed using higher-order functions: `func(next http.Handler) http.Handler`. The chain is built by nesting middleware calls.

The key difference from a generic handler chain is that Go middleware uses function composition rather than object composition. This is more concise and idiomatic in Go, which favors functions over classes. The pattern is the same (Chain of Responsibility), but the implementation leverages Go's first-class functions and closures.

---

## Q100: How would you design an interpreter for a natural language processing (NLP) system?

**A:** An NLP interpreter processes natural language input, extracts meaning, and performs actions or returns information. It combines multiple patterns: the Interpreter pattern for grammar-based parsing, the Chain of Responsibility for processing stages, and the Mediator for coordinating NLP components.

The architecture includes: tokenization (splitting text into words), parsing (building a syntactic tree), semantic analysis (extracting meaning), intent recognition (determining the user's intent), entity extraction (identifying named entities), and response generation (producing output).

Modern NLP interpreters use statistical and neural approaches rather than pure grammar-based parsing. The grammar provides the structure; statistical models fill in the ambiguity. The interpreter may use pre-trained language models for intent recognition and entity extraction, combined with rule-based post-processing for domain-specific logic. The key challenge is handling the inherent ambiguity and variability of natural language while maintaining predictable, testable behavior.

