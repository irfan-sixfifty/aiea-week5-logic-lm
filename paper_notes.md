\# Logic-LM Paper Notes



\## Paper Information



\*\*Title:\*\* Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning



\*\*Authors:\*\* Liangming Pan, Alon Albalak, Xinyi Wang, and William Yang Wang



\*\*Publication:\*\* Findings of EMNLP 2023



\## Research Problem



Large language models can generate convincing step-by-step explanations, but their conclusions do not always logically follow from their reasoning. Because LLMs generate text probabilistically, they do not guarantee that every inference is valid.



Logic-LM addresses this problem by separating natural-language understanding from formal logical reasoning. The LLM translates a problem into symbolic logic, while a deterministic symbolic solver performs the actual inference.



\## Logic-LM Pipeline



The Logic-LM framework has three main stages:



1\. \*\*Problem formulation:\*\* An LLM translates a natural-language problem and question into a symbolic representation.

2\. \*\*Symbolic reasoning:\*\* A deterministic symbolic solver runs inference over the generated facts, rules, and constraints.

3\. \*\*Result interpretation:\*\* The symbolic result is converted into the final answer required by the task.



The framework also includes a self-refinement stage. When the symbolic program cannot run, the solver's error message is sent back to the LLM so that the symbolic formulation can be revised.



\## Why Symbolic Solvers Are Useful



Symbolic solvers follow explicit logical rules and produce reproducible results. Unlike a language model, a solver does not generate a conclusion based on which answer sounds most likely.



The LLM and solver therefore have complementary roles:



\- The LLM handles flexible and ambiguous natural language.

\- The symbolic solver handles exact and faithful logical inference.



\## Reasoning Tasks and Solvers



Logic-LM was evaluated on five datasets:



\- ProofWriter

\- PrOntoQA

\- FOLIO

\- LogicalDeduction

\- AR-LSAT



These datasets cover deductive reasoning, first-order logic, constraint satisfaction, and analytical reasoning.



The framework uses different symbolic tools depending on the problem type, including logic-programming, first-order-logic, constraint-satisfaction, and satisfiability solvers.



\## Main Results



The paper reports that Logic-LM improved average performance by 39.2% compared with standard LLM prompting and by 18.4% compared with chain-of-thought prompting when using GPT-3.5.



The authors also found that Logic-LM became more useful as reasoning depth increased. This suggests that symbolic solvers are especially valuable for problems requiring several connected inference steps.



\## Original Repository



The original repository separates the system into several components:



\- `logic\_program.py` generates symbolic programs from natural-language problems.

\- `logic\_inference.py` sends generated programs to the appropriate symbolic solver.

\- `self\_refinement.py` attempts to repair symbolic programs using solver feedback.

\- `symbolic\_solvers/` contains dataset-specific solver implementations.

\- `outputs/logic\_programs/` contains symbolic programs previously generated during experiments.



\## My Simplified Reimplementation



My implementation uses a Python program connected to SWI-Prolog through PySwip.



The pipeline is:



Natural-language test question  

→ predefined symbolic Prolog query  

→ SWI-Prolog knowledge base  

→ true, false/not derivable, or solver error  

→ Markdown results report



The knowledge base was reused from my earlier LLM/Prolog task and includes facts and rules involving interns, technical skills, projects, project readiness, and collaboration.



\## Tests Performed



The implementation tested:



\- Direct fact retrieval

\- Rule-based inference

\- Multi-condition inference

\- Unsupported claims

\- A malformed Prolog query

\- Solver-error reporting



The test runner compares each result against its expected result and automatically creates a Markdown test report.



\## Similarities to Logic-LM



Both systems:



\- Represent knowledge using symbolic logic

\- Delegate inference to a deterministic solver

\- Separate the problem representation from the reasoning process

\- Detect malformed symbolic input through solver errors

\- Produce reproducible reasoning results



\## Differences from the Full Logic-LM System



My implementation is intentionally smaller than the full paper system.



The most important difference is that my Prolog queries are predefined in the test-case file. An LLM does not yet automatically translate each natural-language question into symbolic logic.



My implementation also detects and records solver errors but does not send the error back to an LLM for automatic correction. Therefore, it demonstrates the symbolic reasoning and feedback portions of Logic-LM rather than reproducing the complete framework.



\## Limitations



Prolog normally uses a closed-world assumption. When a statement cannot be derived from the available facts and rules, it is treated as false or not provable. This does not necessarily mean the statement is false in the real world.



The system is also limited by the coverage and correctness of the knowledge base. Missing facts, incorrect rules, or incorrectly formulated queries can produce misleading results.



Finally, translating unrestricted natural language into correct symbolic logic remains difficult because language can be ambiguous.



\## What I Learned



This task showed me why combining LLMs with symbolic tools can improve logical reliability. LLMs are useful for interpreting natural language, while symbolic solvers provide transparent and deterministic reasoning.



I also learned how Python can communicate with SWI-Prolog through PySwip, how facts and rules are evaluated, how automated test cases can verify reasoning behavior, and how solver errors can support a future self-correction process.

