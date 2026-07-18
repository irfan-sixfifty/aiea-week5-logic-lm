% Week 4 Knowledge Base
% Topic: AIEA Lab interns, skills, and project readiness

% Facts about interns
intern(irfan).
intern(maya).
intern(alex).
intern(sophia).

% Facts about skills
knows(irfan, python).
knows(irfan, git).
knows(irfan, prolog).
knows(maya, python).
knows(maya, machine_learning).
knows(alex, git).
knows(alex, logic).
knows(sophia, python).
knows(sophia, prolog).
knows(sophia, logic).

% Facts about projects
project(llm_logic).
project(neuro_symbolic_reasoning).
project(website_onboarding).

% Facts about project requirements
requires(llm_logic, python).
requires(llm_logic, prolog).
requires(neuro_symbolic_reasoning, logic).
requires(neuro_symbolic_reasoning, python).
requires(website_onboarding, git).

% Rule 1:
% An intern is ready for a project if they know a skill required by that project.
ready_for(Intern, Project) :-
    intern(Intern),
    project(Project),
    requires(Project, Skill),
    knows(Intern, Skill).

% Rule 2:
% An intern is a strong LLM logic candidate if they know both Python and Prolog.
strong_llm_logic_candidate(Intern) :-
    intern(Intern),
    knows(Intern, python),
    knows(Intern, prolog).

% Rule 3:
% Two interns can collaborate if they share at least one skill.
can_collaborate(Intern1, Intern2) :-
    intern(Intern1),
    intern(Intern2),
    Intern1 \= Intern2,
    knows(Intern1, Skill),
    knows(Intern2, Skill).