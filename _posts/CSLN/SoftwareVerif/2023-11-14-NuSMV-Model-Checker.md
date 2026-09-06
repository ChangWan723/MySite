---
title: NuSMV Model Checker
date: 2023-11-14 19:51:00 UTC
categories: [ (CS) Learning Note, Automated Software Verification ]
tags: [computer science, software verification, Model Checking]
pin: false
---

---
<center><font size='5'> Contents </font></center>

---

<!-- TOC -->
  * [What is NuSMV?](#what-is-nusmv)
    * [Key Features of NuSMV](#key-features-of-nusmv)
    * [Applications of NuSMV](#applications-of-nusmv)
      * [Hardware Verification](#hardware-verification)
      * [Software Verification](#software-verification)
      * [Protocol Verification](#protocol-verification)
  * [Getting Started with NuSMV](#getting-started-with-nusmv)
  * [NuSMV's modeling language](#nusmvs-modeling-language)
    * [Declaring State Variables](#declaring-state-variables)
    * [Assignments](#assignments)
    * [Expressions](#expressions)
    * [LTL specifications](#ltl-specifications)
  * [Examples of NuSMV Model Checker](#examples-of-nusmv-model-checker)
    * [Example 1](#example-1)
    * [Example 2](#example-2)
    * [Example 3](#example-3)
    * [Example 4](#example-4)
  * [Module Composition](#module-composition)
    * [Synchronous Composition](#synchronous-composition)
    * [Asynchronous Composition](#asynchronous-composition)
  * [Modelling Programs in NuSMV](#modelling-programs-in-nusmv)
    * [Example: Mutual Exclusion Protocol](#example-mutual-exclusion-protocol)
      * [Mutual Exclusion Protocol in NuSMV](#mutual-exclusion-protocol-in-nusmv)
      * [Running NUSMV (interactive mode)](#running-nusmv-interactive-mode)
      * [NuSMV output](#nusmv-output)
      * [Fairness Constraints](#fairness-constraints)
<!-- TOC -->

---

## What is NuSMV?

[NuSMV](https://nusmv.fbk.eu/) is a software tool(model checker) used for the formal verification of finite state systems. It is based on symbolic model checking techniques, which allow for the efficient verification of systems with a large number of states. Developed as an extension of the original SMV (Symbolic Model Verifier) system, NuSMV integrates new algorithms and analysis techniques.

- NuSMV is a symbolic model checker developed by ITC-IRST and Univ. Trento with the collaboration of CMU and Univ.  Genova.
- it supports the modelling of both **synchronous** and **asynchronous** systems
  - allows for modular construction of models
- it supports the verification of properties expressed in LTL (Linear Temporal Logic) and CTL (Computation Tree Logic)
- it also supports bounded model checking

### Key Features of NuSMV

1. **Symbolic Model Checking**: NuSMV employs Binary Decision Diagrams (BDDs) and SAT solvers to handle large state spaces effectively.
2. **Rich Modeling Language**: It supports a high-level modeling language that allows for the description of complex system behaviors and properties.
3. **Temporal Logic Specifications**: NuSMV can check specifications written in temporal logics such as CTL (Computation Tree Logic) and LTL (Linear Temporal Logic).
4. **Modular Structure**: The system is designed in a modular way, allowing for extensions and integration with other tools.
5. **Counterexample Generation**: When a property is violated, NuSMV provides a counterexample, which is crucial for diagnosing and fixing issues.

### Applications of NuSMV

#### Hardware Verification

NuSMV is widely used in the semiconductor and hardware design industry to verify digital circuits. By checking the correctness of hardware at the design stage, engineers can avoid costly errors and revisions later in the production process.

#### Software Verification

In software engineering, NuSMV can verify properties of software models, ensuring they adhere to specified behaviors. This is particularly important in safety-critical systems like aviation or medical software.

#### Protocol Verification

NuSMV is also used in verifying communication and security protocols. It ensures that protocols behave as expected under various conditions and do not have vulnerabilities.

## Getting Started with NuSMV

To start using NuSMV, one typically goes through the following steps:

1. **Modeling the System**: Define the system's behavior using NuSMV's modeling language. This includes specifying the states, transitions, and variables.
2. **Specifying Properties**: Specify the properties to be verified, usually in temporal logics like CTL or LTL.
3. **Running the Model Checker**: Execute NuSMV with the model and properties. NuSMV then checks whether the properties hold for the given model.
4. **Analyzing Results**: Analyze the output provided by NuSMV. If any property is not satisfied, examine the counterexample provided to understand the issue.

## NuSMV's modeling language

### Declaring State Variables

SMV data types include:
- **boolean**:

```
VAR
  x : boolean;
```

- **enumeration**:

```
VAR
  st : {ready, busy, waiting, stopped};
```

- **bounded integer (interval)**:

```
VAR
  n : 1..8;
```

- **array**:

```
VAR
  a : array 1..10 of {red, green, blue};
```

### Assignments

- **initialisation**:

```
ASSIGN
  init(x) := expression ;
```
If no `init()` assignment is specified for a variable, then it is initialised non-deterministically.

- **progression**:

```
ASSIGN
  next(x) := expression ;
```

- If no `next()` assignment is specified for a variable, then it evolves nondeterministically, i.e. it is unconstrained.
- Unconstrained variables can be used to model nondeterministic inputs to the system.

- **immediate**:

```
ASSIGN
  y := expression ;
```

or

```
DEFINE
  y := expression ;
```
- Immediate assignments constrain the current value of a variable in terms of the current values of other variables.
- Immediate assignments can be used to model outputs of the system.

### Expressions

- **arithmetic operators**:
  - `+ − ∗ / mod (unary)`
- **comparison operators**:
  - `= != > < <= >=`
- **logic operators**:
  - `& | xor ! (not) -> <->`
- **set operators**: {v1,v2,...,vn}
  - `in` : tests a value for membership in a set (set inclusion)
  - `union` : takes the union of 2 sets (set union)
- **count operator**: counts number of true boolean expressions
  - `count(b1 + b2 + ... + bn)`

- **case expression**:
  - guards are evaluated sequentially,
  - first true guard determines the resulting value.

```
case
  c1 : e1;
  c2 : e2;
  ...
  TRUE : default;
esac
```

- **if-then-else expression**:
  - `cond_expr ? basic_expr 1 : basic_expr2`

> Expressions in SMV do not necessarily evaluate to one value
> 
> In general, they can represent a set of possible values.
> - `init(var) := {a,b,c} union {x,y,z};`
>   - destination (`init(var)`) can take any value in the set represented by the set expression (`{a,b,c} union {x,y,z}`)
>   - constant `c` is a syntactic abbreviation for singleton `{c}`
{: .prompt-tip }


### LTL specifications

- LTL properties are specified with the keyword `LTLSPEC`:
  - `LTLSPEC <ltl expression>`
  - `<ltl expression>` can contain the temporal operators: `X_` `F_` `G_` `_U_`
  - e.g. condition `out = 0` holds until `reset` becomes false: `LTLSPEC (out = 0) U (!reset)`

## Examples of NuSMV Model Checker

### Example 1
![](https://i.postimg.cc/Kcptt2d8/nus1.png){: .w-55 .shadow .rounded-10 }

```
MODULE main
VAR
  b0 : boolean
ASSIGN
  init(b0) := 0;
  next(b0) := !b0;
```

An SMV model consists of:
- declarations of state variables (b0 in the example); these determine the state space of the model.
- assignments that constrain the valid initial states
  - (init(b0) := 0)
- assignments that constrain the transition relation
  - (next(b0) := !b0)

### Example 2

![](https://i.postimg.cc/nhxcdnwJ/nus2.png){: .w-55 .shadow .rounded-10 }

Here's how to understand the different parts of the model:

- `MODULE main`: 
  - This declares the main module of the NuSMV model, which is the starting point for the verification process.
- `VAR` section:
  - `request : boolean;` - This declares a Boolean variable `request` which can be true or false, but as noted, it does not receive an assignment in this model, which means its value is non-deterministic and can be considered as an input.
  - `state : {ready, busy};` - This declares a state variable that can have two possible values: 'ready' or 'busy'.
- `ASSIGN` section:
  - `init(state) := ready;` - This initialises the `state` variable to 'ready' at the start.
  - `next(state) := case` - This is a case statement that defines the next value of `state` based on certain conditions.
    - `request : busy;` - If `request` is true, then the next state will be 'busy'.
    - `TRUE : {ready, busy}` - If none of the above conditions are true (which acts as a default case), then `state` can non-deterministically transition to either 'ready' or 'busy'.
- `LTLSPEC` section:
  - `G (request -> F state = busy)` - This is a Linear Temporal Logic (LTL) specification that states globally (`G`), whenever `request` is true, it is eventually (`F`) followed by the `state` being 'busy'. The NuSMV tool would use this LTL specification to check that the model always satisfies this condition.

In the above picture, **the NuSMV code** and **the diagram** are meant to **represent the same model**:

- If the `request` is `true` (req), the diagram shows that the system must go to the `busy` state, which corresponds to the NuSMV `case` code `request : busy;`.
- If the `request` is `false` (¬req), the system can stay in the `ready` state or transition to the `busy` state. This is the default, which corresponds to the NuSMV `case` code `TRUE : {ready, busy}`.

### Example 3

An SMV program can consist of one or more module declarations.

![](https://i.postimg.cc/bwD81mYp/nus3.png){: .w-55 .shadow .rounded-10 }

- Modules are instantiated in other modules. The instantiation is performed inside the VAR declaration of the parent module.
- In each SMV program, there must be a module `main` (top-most one).
- All variables declared in a module instance are visible in the module in which it has been instantiated via the dot notation (e.g. `m1.out`).

### Example 4
Module declarations may be parametric.

![](https://i.postimg.cc/YqfkRvYy/nus4.png){: .w-55 .shadow .rounded-10 }

- Formal parameters (`in`) are substituted with the actual parameters(`m2.out`, `m1.out`) when the module is instantiated.
- Actual parameters can be any legal expression.
- Actual parameters are passed by reference.

## Module Composition

- **synchronous composition**
  - all assignments are executed in parallel and synchronously
  - a single step of the resulting model corresponds to a step in each of the components

- **asynchronous composition**
  - a step of the composition is a step by exactly one process
  - variables not assigned in that process are left unchanged

### Synchronous Composition

By default, the composition of modules is synchronous:
- all modules move at each step

![](https://i.postimg.cc/76yHNdmS/nus5.png){: .w-55 .shadow .rounded-10 }

![](https://i.postimg.cc/Xq16tzcH/nus6.png){: .w-55 .shadow .rounded-10 }
_a possible execution (Bolded text indicates a change)_

### Asynchronous Composition

- Asynchronous composition can be specified using the keyword `process`
- In asynchronous composition, one process moves at each step.

``` 
MODULE cell(input) VAR
  val : {red, green, blue};
  ASSIGN
    next(val) := {val, input};
MODULE main
  VAR
    c1 : process cell(c3.val);
    c2 : process cell(c1.val);
    c3 : process cell(c2.val);
```

![](https://i.postimg.cc/zvcFsCLS/nus7.png){: .w-55 .shadow .rounded-10 }
_a possible execution_

The execution of Asynchronous Composition is more unstable.

## Modelling Programs in NuSMV

Given the following piece of code, computing the GCD of a and b, how do we model and verify it with NuSMV?

```c++
void main() {
// initialization of a and b
  while (a!=b) {
    if (a>b)
      a=a-b;
    else
      b=b-a;
  }
// GCD=a=b
}
```

---

**Step 1:**

label pc (program counter)

![](https://i.postimg.cc/G2LyQXLg/nus8.png){: .w-55 .shadow .rounded-10 }

---

**Step 2:**

encode the transition system using `ASSIGN`

![](https://i.postimg.cc/G2xZ0m1h/nus9.png){: .w-55 .shadow .rounded-10 }

---

### Example: Mutual Exclusion Protocol

![](https://i.postimg.cc/6pGWknbW/nus10.png){: .w-55 .shadow .rounded-10 }

####  Mutual Exclusion Protocol in NuSMV

```
MODULE process1(a,b,turn)
VAR
  pc: {out, wait, cs};
ASSIGN
  init(pc) := out;
  next(pc) := case
    pc=out : wait;
    pc=wait & (!b | !turn) : cs;
    pc=cs : out;
    TRUE : pc;
  esac;
  
  next(turn) := case
    pc=out : TRUE;
    TRUE : turn;
  esac;
  
  next(a) := case
    pc=out : TRUE;
    pc=cs : FALSE;
    TRUE : a;
  esac;
  
  next(b) := b;
  
MODULE process2(a,b,turn)
VAR
  pc: {out, wait, cs};
ASSIGN
  init(pc) := out;
  next(pc) := case
    pc=out : wait;
    pc=wait & (!a | turn) : cs;
    pc=cs : out;
    TRUE : pc;
  esac;
  
  next(turn) := case
    pc=out : FALSE;
    TRUE : turn;
  esac;
  
  next(b) := case
    pc=out : TRUE;
    pc=cs : FALSE;
    TRUE : b;
  esac;
  
  next(a) := a;

MODULE main
VAR
  a : boolean;
  b : boolean;
  turn : boolean;
  p1 : process process1(a,b,turn);
  p2 : process process2(a,b,turn);
ASSIGN
  init(a) := FALSE;
  init(b) := FALSE;
LTLSPEC
  G(!(p1.pc=cs & p2.pc=cs))
LTLSPEC
  G(a -> F(p1.pc=cs)) & G(b -> F(p2.pc=cs))
```

> The `LTLSPEC` is used to verify:
> 1. **Mutual Exclusion**: The critical section(cs) is not entered by more than one process at the same time.
> 2. **Fairness**: If a process is waiting to enter the critical section(cs), it will eventually be allowed to enter.
{: .prompt-tip }

#### Running NUSMV (interactive mode)

``` 
% NuSMV -int add.smv
NuSMV > go
NuSMV > check_ltlspec
NuSMV > quit
```

- `go` abbreviates the sequence of commands `read_model`, `flatten_hierarchy`, `encode_variables`, `build_model`
- for command options, use -h or look in the NuSMV User Manual


#### NuSMV output

![](https://i.postimg.cc/0NW5GdVP/nus11.png){: .w-55 .shadow .rounded-10 }

#### Fairness Constraints

If we add the following declaration to `process1`:

``` 
COMPASSION
  (pc=wait & (!b | !turn), pc=cs);
```

And we also add the following declaration to `process2`:

``` 
COMPASSION
  (pc=wait & (!a | turn), pc=cs);
```

then: `( G (a -> F p1.pc = cs) & G (b -> F p2.pc = cs))` is true!

---

> `COMPASSION (expr1, expr2)`: restricts attention to executions where if `expr1` is true infinitely often, then `expr2` is true infinitely often.
> 
> In essence, the `COMPASSION` is to **ensure that a process is not infinitely prevented** from entering the critical section **due to the system's unfairness**. However, access to the critical region still requires that **the process must satisfy the conditions for entry**.
{: .prompt-tip }
