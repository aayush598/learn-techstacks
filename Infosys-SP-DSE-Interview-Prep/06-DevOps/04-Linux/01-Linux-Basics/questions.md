# 01 Linux Basics — Linux

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What is Linux and its architecture?**
   - An open-source OS with a kernel managing hardware, scheduling, and system calls; user-space tools (GNU coreutils) sit on top — the server OS of choice.

2. **What are the most common Linux commands?**
   - ls, cd, pwd, cp, mv, rm, mkdir, grep, find, chmod, ps, top, ssh — the everyday toolbox everyone must rattle off.

3. **What is the difference between absolute and relative paths?**
   - Absolute: /home/user/file, from root. Relative: ../file, from cwd — the path semantics of navigation.

4. **What is the directory structure (/bin, /etc, /var)?**
   - /bin binaries, /etc config, /var variable logs/data, /home users, /tmp temp, /proc virtual-kernel files — the FHS layout maps.

5. **What are file permissions and how do you change them?**
   - r/w/x per owner/group/other as octal (755); chmod sets them, chown changes ownership — the access-control basics.

6. **What is the difference between a hard link and symlink in Linux?**
   - Hard link: additional name for the same inode. Symlink: a shortcut path (may break). ln file hard, ln -s target sym — reuses the OS concepts.

7. **What is stdout, stdin, stderr?**
   - Standard streams: input (0), output (1), error (2); redirect with >, >>, 2>, and pipe with | — the shell plumbing.

8. **What does grep find?**
   - Text search in files/streams: grep pattern file, -i ignore case, -r recursive — the pattern-matching reviewer.

9. **What is the difference between find and grep?**
   - find locates files by name/type/time; grep searches content of files — two different axes of the filesystem.

10. **How do you check disk space, memory, CPU?**
   - df -h (disks), free -h (RAM), top/htop (live processes), uptime (load) — the health-check command quartet.

11. **What is a package manager?**
   - apt/yum/dnf install, update, and remove software from repos — the dependency management of the OS itself.

12. **How do you edit/search history in the shell?**
   - history, !! (last), ctrl-r reverse search — shell productivity, the fastest editing shortcuts.

13. **Define 01 linux basics in one line and then expand with a real-world example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

14. **Why is 01 linux basics important in real production systems?**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

15. **What are the advantages and disadvantages of 01 linux basics?**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

16. **Compare 01 linux basics with alternatives and state when to prefer which.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

17. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

18. **What common misconceptions exist about 01 linux basics?**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

19. **How would you test correctness of a system that relies on 01 linux basics?**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

20. **Describe 01 linux basics as if explaining to a new hire.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

21. **How does 01 linux basics interact with performance (time/space trade-off)?**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

22. **What would you change about how 01 linux basics is taught, based on your experience?**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

23. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

24. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

25. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

26. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

27. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

28. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

29. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

30. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

31. **How does 01 linux basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

32. **What would you change about how 01 linux basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

33. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

34. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

35. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

36. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

37. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

38. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

39. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

40. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

41. **How does 01 linux basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

42. **What would you change about how 01 linux basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

43. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

44. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

45. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

46. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

47. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

48. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

49. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

50. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

51. **How does 01 linux basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

52. **What would you change about how 01 linux basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

53. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

54. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

55. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

56. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

57. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

58. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

59. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

60. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

61. **How does 01 linux basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

62. **What would you change about how 01 linux basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

63. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

64. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

65. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

66. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

67. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

68. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

69. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

70. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

71. **How does 01 linux basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

72. **What would you change about how 01 linux basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

73. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

74. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

75. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

76. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

77. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

78. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

79. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

80. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

81. **How does 01 linux basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

82. **What would you change about how 01 linux basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

83. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

84. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

85. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

86. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

87. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

88. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

89. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

90. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

91. **How does 01 linux basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

92. **What would you change about how 01 linux basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

93. **Define 01 linux basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 linux basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

94. **Why is 01 linux basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

95. **What are the advantages and disadvantages of 01 linux basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

96. **Compare 01 linux basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

97. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 linux basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

98. **What common misconceptions exist about 01 linux basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

99. **How would you test correctness of a system that relies on 01 linux basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

100. **Describe 01 linux basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

</details>