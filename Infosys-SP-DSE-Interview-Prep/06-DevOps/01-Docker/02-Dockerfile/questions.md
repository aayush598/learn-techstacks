# 02 Dockerfile — Docker

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What is a Dockerfile and its key instructions?**
   - The build recipe: FROM (base), WORKDIR, COPY, RUN (build-time), ENV, EXPOSE, CMD/ENTRYPOINT — a declarative image definition.

2. **What is the difference between CMD and ENTRYPOINT?**
   - ENTRYPOINT is the fixed process (can't be overridden casually); CMD supplies default args — combine (ENTRYPOINT + CMD) for a default-and-overridable command.

3. **How do you build and tag an image?**
   - docker build -t myapp:1.0 . — the build context (.) is sent to the daemon; tag format repo:tag for registry push.

4. **How do you pass build-time vs runtime config?**
   - ARG for build-time (FROM versions, build args), ENV for runtime; different use cases and caching implications.

5. **What is a multi-stage build and why use it?**
   - Chaining FROM statements: one stage compiles (huge toolchains), the final stage copies only artifacts into a slim runtime image — dramatically smaller, safer images.

6. **Why is the order of instructions important for layer caching?**
   - Docker caches layers; COPY requirements.txt before the rest, then RUN pip install — so dependency installs cache unless requirements change; frequent-changers last.

7. **What makes an image slim?**
   - Slim base (python:slim/distroless/scratch), multi-stage builds, removing caches (pip --no-cache-dir apt lists), and non-root users — the size-optimisation checklist.

8. **What is the best practice of running as non-root?**
   - USER appuser in the Dockerfile — containers running as root escalate host risk; security best practice shouted at interviews.

9. **How do you handle secrets at build vs runtime?**
   - Never bake secrets into images — build args/COPY embed them, leaking in layers; inject via env/compose/K8s secrets at runtime.

10. **What is a healthcheck instruction?**
   - HEALTHCHECK CMD tells Docker to probe the app (curl/health endpoint) — orchestrators/LB decide readiness from the result.

11. **What is .dockerignore and why is it critical?**
   - Excluding .git, venv, __pycache__, caches from the build context — faster builds, smaller contexts, and no accidental secret copying.

12. **What is the difference between RUN vs CMD in building the app?**
   - RUN executes during build (results become layers); CMD runs at container start — confusion here is a classic Docker interview trap.

13. **Define 02 dockerfile in one line and then expand with a real-world example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

14. **Why is 02 dockerfile important in real production systems?**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

15. **What are the advantages and disadvantages of 02 dockerfile?**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

16. **Compare 02 dockerfile with alternatives and state when to prefer which.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

17. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

18. **What common misconceptions exist about 02 dockerfile?**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

19. **How would you test correctness of a system that relies on 02 dockerfile?**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

20. **Describe 02 dockerfile as if explaining to a new hire.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

21. **How does 02 dockerfile interact with performance (time/space trade-off)?**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

22. **What would you change about how 02 dockerfile is taught, based on your experience?**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

23. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

24. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

25. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

26. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

27. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

28. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

29. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

30. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

31. **How does 02 dockerfile interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

32. **What would you change about how 02 dockerfile is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

33. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

34. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

35. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

36. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

37. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

38. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

39. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

40. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

41. **How does 02 dockerfile interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

42. **What would you change about how 02 dockerfile is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

43. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

44. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

45. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

46. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

47. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

48. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

49. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

50. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

51. **How does 02 dockerfile interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

52. **What would you change about how 02 dockerfile is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

53. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

54. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

55. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

56. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

57. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

58. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

59. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

60. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

61. **How does 02 dockerfile interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

62. **What would you change about how 02 dockerfile is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

63. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

64. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

65. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

66. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

67. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

68. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

69. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

70. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

71. **How does 02 dockerfile interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

72. **What would you change about how 02 dockerfile is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

73. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

74. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

75. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

76. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

77. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

78. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

79. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

80. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

81. **How does 02 dockerfile interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

82. **What would you change about how 02 dockerfile is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

83. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

84. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

85. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

86. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

87. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

88. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

89. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

90. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

91. **How does 02 dockerfile interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

92. **What would you change about how 02 dockerfile is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

93. **Define 02 dockerfile in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 02 dockerfile is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

94. **Why is 02 dockerfile important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

95. **What are the advantages and disadvantages of 02 dockerfile? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

96. **Compare 02 dockerfile with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

97. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 02 dockerfile knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

98. **What common misconceptions exist about 02 dockerfile? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

99. **How would you test correctness of a system that relies on 02 dockerfile? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

100. **Describe 02 dockerfile as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

</details>