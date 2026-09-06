---
title: SAT Problem and DPLL
date: 2023-11-20 19:37:00 UTC
categories: [ (CS) Learning Note, Automated Software Verification ]
tags: [computer science, software verification, Model Checking]
pin: false
---

---
<center><font size='5'> Contents </font></center>

---

<!-- TOC -->
  * [What is SAT Problem?](#what-is-sat-problem)
    * [Conjunctive Normal Form of SAT Problem](#conjunctive-normal-form-of-sat-problem)
  * [What is DPLL?](#what-is-dpll)
    * [DPLL Simplification Rules](#dpll-simplification-rules)
    * [DPLL Splitting](#dpll-splitting)
    * [Example of a SAT Problem](#example-of-a-sat-problem)
  * [Current State of SAT Solving](#current-state-of-sat-solving)
<!-- TOC -->

---

## What is SAT Problem?

The Boolean satisfiability problem (also SAT problem) asks whether a given Boolean formula is satisfiable.

**E.g.**: Is the following Boolean (propositional) formula satisfiable?

`(x1 ∧ x2 ∨ x3) ∧ (x4 ∧ x1 ∨ x3) ∧ ¬(x4 ∨ x1)`

- That is, does there exist an assignment of truth values to the Boolean variables x1, x2, x3, x4 that makes the formula True?
  - Yes! `x1 = False, x2 = True, x3 = True, x4 = False`

- The SAT problem was the first example of an NP-Complete problem (Cook-Levin theorem, 1971).
- We can encode many interesting problems in terms of Boolean satisfiability (SAT).
- In particular, many problems in circuit design can often be cast as SAT problems.

### Conjunctive Normal Form of SAT Problem

- A **literal** is a atomic formula or its negation (e.g. a propositional variable `x1`, or `¬x1`).
- A **clause** is a disjunction of literals (e.g. `x1 ∨ ¬x3 ∨ x2`)
- A propositional formula is in Conjunctive Normal Form (CNF) if it is a conjunction of one or more clauses, e.g. `(x1 ∨ ¬x3 ∨ x2) ∧ (¬x4 ∨ ¬x1 ∨ x3) ∧ (¬x5)`
- Any given propositional formula can be converted into CNF by applying transformations
  - eliminating double negations (i.e. `¬¬ϕ` becomes `ϕ`)
  - applying De Morgan’s laws
  - applying the distributive law

## What is DPLL?

**DPLL (Davis–Putnam–Logemann–Loveland) Algorithm** is a fundamental algorithm for solving the Boolean satisfiability problem (SAT problem), which is a key problem in computer science, particularly in fields such as artificial intelligence, computational complexity theory, and algorithm design.

- DPLL can take an exponential amount of time, however it can often find solutions to SAT relatively quickly.
- The DPLL algorithm works by
  - Converting the Boolean formula into CNF (Conjunctive Normal Form)
  - Applying simplification rules
  - Splitting

### DPLL Simplification Rules

There are two main rules. Both simplification rules preserve satisfiability:
- Unit propagation (one literal rule): when there is a unit clause (a clause with just one element `p`), remove `¬p` from all the other clauses.
  - Intuitively: if `p` has to be true, then `¬p` does not add anything to the other disjunctive clauses.]
- Affirmative-negative rule: if `p` occurs either only negated, or only unnegated, then remove all clauses containing `p`.
  - one can make all clauses containing `p` True by setting `p` to True if it is always unnegated, or by setting `p` to False if it only appears negated.

### DPLL Splitting

The simplification rules by themselves do not generally allow us to check satisfiability. To make further progress, we must consider case **splits**:

- For a set of clauses Γ, choose a propositional variable x and consider two cases:
  1. `Γ ∪ {x}` (set `x` to True)
  2. `Γ ∪ {¬x}` (set `x` to False).
- Then apply the simplification rules (unit propagation and affirmative-negative rule) as before.
- Applying these steps recursively one obtains a backtracking strategy for solving the SAT problem.
  - If an empty set of clauses is found, the formula is satisfiable.

### Example of a SAT Problem

Suppose we have the following Boolean formula, which is a conjunction of several clauses (each clause is a disjunction of literals): 

```
(A ∨ ¬B) ∧ (¬A ∨ C) ∧ (B ∨ ¬C)
```

Here, `A`, `B`, and `C` are Boolean variables that can take the values True (T) or False (F). The goal is to find an assignment of values to these variables such that the entire formula evaluates to True, or determine that no such assignment exists (in which case the formula is unsatisfiable).

**Step-by-Step Solution Using a Simplified DPLL Approach:**

- **Start with the first clause** `A ∨ ¬B`:
  - We don't have any unit clause or pure literal yet, so we make a choice. Let's assume `A = True`.
- **Move to the next clause** `¬A ∨ C`:
  - Since we have `A = True`, this clause simplifies to `C`.
  - We must make `C = True` for this clause to be satisfied.
- **Now consider the last clause** `B ∨ ¬C`:
  - Since `C = True`, `¬C` is False. This clause simplifies to `B`.
  - We must make `B = True` for this clause to be satisfied.
- **Check the entire formula with `A = True, B = True, C = True`**:
  - `(A ∨ ¬B) = (True ∨ False) = True`
  - `(¬A ∨ C) = (False ∨ True) = True`
  - `(B ∨ ¬C) = (True ∨ False) = True`

Since all clauses are satisfied, this assignment `(A = True, B = True, C = True)` is a solution to the SAT problem. Therefore, the formula is satisfiable.

## Current State of SAT Solving

- DPLL is the basis for many modern SAT solvers. These solvers have enhanced DPLL with various heuristics and optimization techniques to efficiently handle large and complex SAT instances.
- SAT solvers are capable of solving practical SAT problems with millions of propositional variables
- Enormous progress has been made in SAT solving technology over the past 20 years, spurred on by the [SAT competition](https://www.satcompetition.org/)
