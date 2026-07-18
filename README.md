\# AIEA Lab Week 5: Logic-LM Reimplementation



\## Overview



This project is a simplified reimplementation of ideas from the paper:



\*\*Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning\*\*



The goal of this project was to understand how large language models can be combined with symbolic reasoning systems. The implementation demonstrates how natural-language reasoning questions can be paired with symbolic Prolog queries and evaluated using SWI-Prolog through Python.



\## Logic-LM Concept



Logic-LM separates natural-language understanding from formal reasoning.



The general framework is:



```text

Natural-language problem

&#x20;       ↓

LLM-generated symbolic formulation

&#x20;       ↓

Symbolic solver

&#x20;       ↓

Final answer

```



The language model interprets the problem and translates it into symbolic logic. A deterministic symbolic solver then performs the actual inference. Logic-LM can also use solver error messages to help an LLM revise an invalid symbolic program.



\## My Simplified Pipeline



My implementation uses manually defined Prolog queries instead of automatically generating them with an LLM.



```text

Natural-language question

&#x20;       ↓

Predefined Prolog query

&#x20;       ↓

SWI-Prolog knowledge base

&#x20;       ↓

True, false/not derivable, or solver error

&#x20;       ↓

Markdown test report

```



\## Tools Used



\- Python

\- SWI-Prolog

\- PySwip

\- JSON

\- Markdown

\- Git and GitHub



\## Project Structure



```text

Week 5/

├── implementation/

│   ├── knowledge\_base.pl

│   ├── logic\_lm\_pipeline.py

│   └── test\_cases.json

├── results/

│   └── test\_results.md

├── slides/

├── deliverable/

├── paper\_notes.md

├── README.md

└── .gitignore

```



\## Knowledge Base



The Prolog knowledge base was reused from the Week 4 onboarding task. It contains facts and rules about:



\- Sample AIEA Lab interns

\- Programming and reasoning skills

\- Research projects

\- Project skill requirements

\- Project readiness

\- Possible collaboration between interns



Example facts:



```prolog

intern(irfan).

knows(irfan, python).

knows(irfan, prolog).

project(llm\_logic).

requires(llm\_logic, python).

```



Example rules:



```prolog

ready\_for(Person, Project) :-

&#x20;   knows(Person, Skill),

&#x20;   requires(Project, Skill).



strong\_llm\_logic\_candidate(Person) :-

&#x20;   knows(Person, python),

&#x20;   knows(Person, prolog).

```



\## Program Description



The main program is:



```text

implementation/logic\_lm\_pipeline.py

```



The program:



1\. Loads the Prolog knowledge base using PySwip.

2\. Reads test cases from `test\_cases.json`.

3\. Sends each symbolic query to SWI-Prolog.

4\. Classifies the result as `true`, `false`, or `error`.

5\. Compares the actual result with the expected result.

6\. Marks each test as `PASS` or `FAIL`.

7\. Creates a Markdown report containing the results and solver feedback.



\## Test Cases



The implementation includes seven test cases covering:



\- Direct fact retrieval

\- Rule-based inference

\- Multi-condition inference

\- Unsupported claims

\- Malformed symbolic queries

\- Solver-error reporting



Example standard query:



```prolog

ready\_for(irfan, llm\_logic)

```



This query returns `true` because the knowledge base contains the facts and rules needed to determine that Irfan knows a skill required by the LLM logic project.



Example malformed query:



```prolog

ready\_for(irfan, llm\_logic

```



This query is missing a closing parenthesis. SWI-Prolog detects the invalid syntax, and the Python program catches and records the solver error.



\## Results



All seven test cases produced their expected results.



The automatically generated report is located at:



```text

results/test\_results.md

```



The report contains:



\- Test identification number

\- Test category

\- Natural-language question

\- Prolog query

\- Expected result

\- Actual result

\- Pass-or-fail status

\- Returned variable bindings

\- Solver feedback



\## Running the Program



\### Requirements



\- Python

\- SWI-Prolog

\- PySwip



Create and activate a Python virtual environment, then install PySwip:



```powershell

py -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip

.\\.venv\\Scripts\\python.exe -m pip install pyswip==0.3.3

```



Confirm that SWI-Prolog and PySwip are available:



```powershell

swipl --version

.\\.venv\\Scripts\\python.exe -c "from pyswip import Prolog; print('PySwip imported successfully')"

```



Run the program from the project directory:



```powershell

.\\.venv\\Scripts\\python.exe .\\implementation\\logic\_lm\_pipeline.py

```



Expected runtime is approximately 1–5 seconds.



\## Limitations



This implementation is intentionally smaller than the complete Logic-LM framework.



The main limitations are:



\- Natural-language questions are paired with manually written Prolog queries.

\- An LLM does not automatically generate the symbolic programs.

\- Solver errors are recorded but are not automatically sent back to an LLM for correction.

\- Results depend on the accuracy and completeness of the knowledge base.

\- A Prolog result of `false` means the statement could not be derived from the available facts and rules. It does not necessarily prove that the statement is false in the real world.



\## What I Learned



This project helped me understand how large language models and symbolic reasoning systems can complement each other.



LLMs are useful for interpreting flexible natural language, while symbolic solvers provide deterministic, transparent, and reproducible logical inference. I also gained more experience with:



\- Connecting Python and SWI-Prolog through PySwip

\- Writing and testing Prolog facts and rules

\- Organizing test cases in JSON

\- Handling solver errors

\- Generating automated Markdown reports

\- Examining the structure of a research-code repository



\## Paper Reference



Pan, Liangming, Alon Albalak, Xinyi Wang, and William Yang Wang.



\*Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning.\*



Findings of the Association for Computational Linguistics: EMNLP 2023.

