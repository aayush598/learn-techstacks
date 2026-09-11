# Oop — Solid Principles Interview Questions and Answers

## Q1: What are the SOLID principles?
**A:** Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion — five principles for maintainable OO design.

## Q2: Explain Single Responsibility Principle.
**A:** A class should have one reason to change — one responsibility. Splitting concerns keeps classes focused and testable (e.g., separate data access, business logic, presentation).

## Q3: Explain Open-Closed Principle.
**A:** Software should be open for extension but closed for modification — add new behaviour via inheritance/strategies rather than editing existing class code.

## Q4: Explain Liskov Substitution Principle.
**A:** Subtypes must be substitutable for their base types without breaking behaviour — a derived class must not weaken the base's contract (override that throws exceptions is a classic violation).

## Q5: Explain Interface Segregation Principle.
**A:** Clients should not be forced to depend on methods they don't use — prefer several specific interfaces over one fat interface.

## Q6: Explain Dependency Inversion Principle.
**A:** High-level modules should not depend on low-level modules; both should depend on abstractions. Inject dependencies rather than hard-coding implementations (e.g., pass an LLM client, don't import one).

## Q7: How do the SOLID principles apply to a FastAPI service?
**A:** Separate routers/controllers, service (business) layer, repository (data) layer; abstract external clients behind interfaces so they can be swapped or mocked.

## Q8: Give an example of LSP used properly.
**A:** If Rectangle has area(); Square extended from it would break expectations — the famous design smell. Use a Shape abstraction instead — each provides area() consistently.

## Q9: What is 'favour composition over inheritance'?
**A:** Build behaviour by composing objects (has-a) instead of deep inheritance — more flexible at runtime and avoids fragile base-class coupling.

## Q10: How would you refactor a god class with SRP/OCP?
**A:** Extract each responsibility into its own class (SRP), expose them through an interface (ISP), and enable extension via strategy/injection (OCP/DIP).

## Q11: Define 05 solid principles in one line and then expand with a real-world example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q12: Why is 05 solid principles important in real production systems?
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q13: What are the advantages and disadvantages of 05 solid principles?
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q14: Compare 05 solid principles with alternatives and state when to prefer which.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q15: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q16: What common misconceptions exist about 05 solid principles?
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q17: How would you test correctness of a system that relies on 05 solid principles?
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q18: Describe 05 solid principles as if explaining to a new hire.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q19: How does 05 solid principles interact with performance (time/space trade-off)?
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q20: What would you change about how 05 solid principles is taught, based on your experience?
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q21: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q22: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q23: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q24: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q25: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q26: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q27: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q28: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q29: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q30: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q31: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q32: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q33: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q34: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q35: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q36: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q37: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q38: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q39: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q40: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q41: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q42: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q43: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q44: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q45: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q46: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q47: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q48: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q49: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q50: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q51: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q52: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q53: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q54: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q55: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q56: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q57: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q58: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q59: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q60: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q61: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q62: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q63: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q64: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q65: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q66: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q67: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q68: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q69: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q70: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q71: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q72: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q73: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q74: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q75: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q76: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q77: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q78: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q79: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q80: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q81: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q82: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q83: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q84: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q85: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q86: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q87: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q88: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q89: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q90: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q91: Define 05 solid principles in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 05 solid principles is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q92: Why is 05 solid principles important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q93: What are the advantages and disadvantages of 05 solid principles? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q94: Compare 05 solid principles with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q95: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 05 solid principles knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q96: What common misconceptions exist about 05 solid principles? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q97: How would you test correctness of a system that relies on 05 solid principles? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q98: Describe 05 solid principles as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q99: How does 05 solid principles interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q100: What would you change about how 05 solid principles is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.
