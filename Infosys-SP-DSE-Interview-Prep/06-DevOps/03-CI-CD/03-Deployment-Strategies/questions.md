# 03 Deployment Strategies — Ci / Cd

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What are the deployment strategies?**
   - Recreate, rolling, blue/green, canary, and feature-flag/shadow — each trades deploy risk against speed and infrastructure cost.

2. **What is a rolling deploy?**
   - Instances upgrade one-by-one while the service stays up — simple, no extra capacity, but partial-incompatibility window during the roll.

3. **What is blue/green deployment?**
   - Two full environments; switch traffic atomically on the new (green) set — instant rollback to blue, at the cost of doubled capacity.

4. **What is a canary deployment?**
   - Sending ~5-10% of traffic to the new version, watching metrics, then ramping to 100% — incremental trust with real-world verification.

5. **What is the rollback strategy and how does it work?**
   - Every deploy should roll back: previous image is one command away; automated rollback triggers on error-rate/health degradation.

6. **What is a zero-downtime deploy?**
   - Combining readiness probes/before-registration with rolling or blue-green so users never see 503s — the availability standard for production paths.

7. **What is database migration's special deploy risk?**
   - Schema changes must be additive/backwards-compatible (expand-contract); deploys and migrations sequence separately to avoid breaking running versions.

8. **What is immutable infrastructure?**
   - Servers/containers are never patched in place — deployments replace them wholesale with new images; drift is impossible by construction.

9. **What is a feature flag and why does it decouple deploys?**
   - Code ships dormant behind flags, toggled at runtime — releasing features without redeploying and enabling instant kill-switches.

10. **What is a shadow deploy?**
   - Writing the new version side-by-side, mirroring traffic without acting on it — comparing behaviour before exposing users (an advanced technique).

11. **What metrics gate a deploy?**
   - Error rate, latency percentiles, CPU, and business metrics — auto-rollback thresholds are set before, not after, the deploy.

12. **Define 03 deployment strategies in one line and then expand with a real-world example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

13. **Why is 03 deployment strategies important in real production systems?**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

14. **What are the advantages and disadvantages of 03 deployment strategies?**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

15. **Compare 03 deployment strategies with alternatives and state when to prefer which.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

16. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

17. **What common misconceptions exist about 03 deployment strategies?**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

18. **How would you test correctness of a system that relies on 03 deployment strategies?**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

19. **Describe 03 deployment strategies as if explaining to a new hire.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

20. **How does 03 deployment strategies interact with performance (time/space trade-off)?**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

21. **What would you change about how 03 deployment strategies is taught, based on your experience?**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

22. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

23. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

24. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

25. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

26. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

27. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

28. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

29. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

30. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

31. **What would you change about how 03 deployment strategies is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

32. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

33. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

34. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

35. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

36. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

37. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

38. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

39. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

40. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

41. **What would you change about how 03 deployment strategies is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

42. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

43. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

44. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

45. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

46. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

47. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

48. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

49. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

50. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

51. **What would you change about how 03 deployment strategies is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

52. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

53. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

54. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

55. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

56. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

57. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

58. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

59. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

60. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

61. **What would you change about how 03 deployment strategies is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

62. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

63. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

64. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

65. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

66. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

67. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

68. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

69. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

70. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

71. **What would you change about how 03 deployment strategies is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

72. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

73. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

74. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

75. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

76. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

77. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

78. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

79. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

80. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

81. **What would you change about how 03 deployment strategies is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

82. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

83. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

84. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

85. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

86. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

87. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

88. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

89. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

90. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

91. **What would you change about how 03 deployment strategies is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

92. **Define 03 deployment strategies in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 03 deployment strategies is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

93. **Why is 03 deployment strategies important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

94. **What are the advantages and disadvantages of 03 deployment strategies? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

95. **Compare 03 deployment strategies with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

96. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 03 deployment strategies knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

97. **What common misconceptions exist about 03 deployment strategies? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

98. **How would you test correctness of a system that relies on 03 deployment strategies? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

99. **Describe 03 deployment strategies as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

100. **How does 03 deployment strategies interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

</details>