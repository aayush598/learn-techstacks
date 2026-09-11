# 01 Sql Basics — Sql

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What does SQL stand for and what are its sub-languages?**
   - Structured Query Language. DDL (DEFINE structure), DML (MANIPULATE data), DQL (SELECT), DCL (control access GRANT/REVOKE), TCL (transactions COMMIT/ROLLBACK) — the classification Infosys loves.

2. **Write a basic SELECT with WHERE and ORDER BY.**
   - SELECT name, salary FROM employees WHERE department='IT' ORDER BY salary DESC; — read columns, filter rows, order results.

3. **What does DISTINCT do?**
   - Removes duplicate rows from the result (SELECT DISTINCT dept FROM emp returns each department once).

4. **What are the arithmetic and comparison operators in SQL?**
   - Arithmetic: + - * / %; comparison: =, <>, !=, <, >, <=, >=, BETWEEN, IN, LIKE, IS NULL — the SQL toolbox for expressions.

5. **What is the difference between WHERE and HAVING?**
   - WHERE filters rows before grouping; HAVING filters groups after GROUP BY. WHERE can't reference aggregates; HAVING can (HAVING COUNT(*) > 5).

6. **What is NULL and how does comparison affect it?**
   - NULL means unknown/missing. Comparisons with = are never true (result unknown) — use IS NULL / IS NOT NULL, and COALESCE/NULLIF for safe arithmetic.

7. **What is the difference between <= and <> with NULL?**
   - Neither works with NULL: any comparison with NULL yields UNKNOWN and rows are filtered out — the classic 'WHERE col <> 5' missing-NULLs bug.

8. **How do you limit the number of rows?**
   - LIMIT n in PostgreSQL/MySQL; TOP n in SQL Server; FETCH FIRST n ROWS ONLY in standard SQL. Combined with ORDER BY to get the 'top N' rows.

9. **What is an alias and why is it useful?**
   - Renaming columns/tables in the query (SELECT e.name AS employee_name FROM emp e) for readability and disambiguation in joins/subqueries.

10. **Write a query to get the second-highest salary.**
   - SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp); alternative: ORDER BY salary DESC LIMIT 1 OFFSET 1.

11. **What is COALESCE?**
   - Returns the first non-NULL argument from a list — COALESCE(middle_name, 'N/A') gives a default when a value is missing; the ISO standard 'first non-null'.

12. **What is the difference between COUNT(*) and COUNT(column)?**
   - COUNT(*) counts all rows; COUNT(column) counts non-NULL values in that column — a subtle but critical SQL distinction.

13. **What is the difference between IN and EXISTS?**
   - IN compares against a list/subquery result; EXISTS tests whether rows exist and short-circuits — EXISTS often faster on large correlated subqueries.

14. **What is LIKE and its wildcards?**
   - Pattern matching: % matches any number of chars, _ matches exactly one. 'LIKE a%' → starts with 'a'; escape %% when a literal % is needed.

15. **What is the difference between UNION and UNION ALL?**
   - UNION combines results and removes duplicates (sorting); UNION ALL keeps all rows (faster). UNION requires matching column counts/types.

16. **Define 01 sql basics in one line and then expand with a real-world example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

17. **Why is 01 sql basics important in real production systems?**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

18. **What are the advantages and disadvantages of 01 sql basics?**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

19. **Compare 01 sql basics with alternatives and state when to prefer which.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

20. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

21. **What common misconceptions exist about 01 sql basics?**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

22. **How would you test correctness of a system that relies on 01 sql basics?**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

23. **Describe 01 sql basics as if explaining to a new hire.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

24. **How does 01 sql basics interact with performance (time/space trade-off)?**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

25. **What would you change about how 01 sql basics is taught, based on your experience?**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

26. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

27. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

28. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

29. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

30. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

31. **What common misconceptions exist about 01 sql basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

32. **How would you test correctness of a system that relies on 01 sql basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

33. **Describe 01 sql basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

34. **How does 01 sql basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

35. **What would you change about how 01 sql basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

36. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

37. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

38. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

39. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

40. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

41. **What common misconceptions exist about 01 sql basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

42. **How would you test correctness of a system that relies on 01 sql basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

43. **Describe 01 sql basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

44. **How does 01 sql basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

45. **What would you change about how 01 sql basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

46. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

47. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

48. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

49. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

50. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

51. **What common misconceptions exist about 01 sql basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

52. **How would you test correctness of a system that relies on 01 sql basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

53. **Describe 01 sql basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

54. **How does 01 sql basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

55. **What would you change about how 01 sql basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

56. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

57. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

58. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

59. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

60. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

61. **What common misconceptions exist about 01 sql basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

62. **How would you test correctness of a system that relies on 01 sql basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

63. **Describe 01 sql basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

64. **How does 01 sql basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

65. **What would you change about how 01 sql basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

66. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

67. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

68. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

69. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

70. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

71. **What common misconceptions exist about 01 sql basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

72. **How would you test correctness of a system that relies on 01 sql basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

73. **Describe 01 sql basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

74. **How does 01 sql basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

75. **What would you change about how 01 sql basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

76. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

77. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

78. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

79. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

80. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

81. **What common misconceptions exist about 01 sql basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

82. **How would you test correctness of a system that relies on 01 sql basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

83. **Describe 01 sql basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

84. **How does 01 sql basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

85. **What would you change about how 01 sql basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

86. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

87. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

88. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

89. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

90. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

91. **What common misconceptions exist about 01 sql basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

92. **How would you test correctness of a system that relies on 01 sql basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

93. **Describe 01 sql basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

94. **How does 01 sql basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

95. **What would you change about how 01 sql basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

96. **Define 01 sql basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 sql basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

97. **Why is 01 sql basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

98. **What are the advantages and disadvantages of 01 sql basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

99. **Compare 01 sql basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

100. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 sql basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

</details>