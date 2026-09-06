---
title: Physical Plan in Databases Query Processing
date: 2024-04-14 18:00:00 UTC
categories: [ (CS) Learning Note, Database ]
tags: [ computer science, Database ]
pin: false
---

---
<center><font size='5'> Contents </font></center>

---

<!-- TOC -->
  * [Physical Plan Operators](#physical-plan-operators)
    * [Computation Model](#computation-model)
    * [Scan](#scan)
      * [Table Scan](#table-scan)
      * [Index Scan](#index-scan)
  * [One-Pass Algorithms](#one-pass-algorithms)
    * [Unary, Tuple at a Time](#unary-tuple-at-a-time)
    * [Unary, Full-Relation](#unary-full-relation)
      * [Duplicate Elimination](#duplicate-elimination)
      * [Grouping](#grouping)
    * [Binary, Full-Relation](#binary-full-relation)
      * [Join](#join)
  * [Example of Binary Operators: Join (in One-Pass Algorithms)](#example-of-binary-operators-join-in-one-pass-algorithms)
    * [Attempt 1: Tuple-Based Nested Loop Join](#attempt-1-tuple-based-nested-loop-join)
      * [Attempt 2: Block-Based Nested Loop Join](#attempt-2-block-based-nested-loop-join)
    * [Attempt 3: Join Reordering](#attempt-3-join-reordering)
    * [Attempt 4: Contiguous Relations (Clustered)](#attempt-4-contiguous-relations-clustered)
    * [Attempt 5: Merge Join](#attempt-5-merge-join)
  * [Two-Pass Algorithms](#two-pass-algorithms)
    * [Merge Sort](#merge-sort)
    * [Attempt 6: Merge Join (with Sort)](#attempt-6-merge-join-with-sort)
      * [Which is better, Merge Join (with Sort) or Nested Loop (Clustered)?](#which-is-better-merge-join-with-sort-or-nested-loop-clustered)
    * [Attempt 7: Improved Merge Join (using Hashing and Bucket Sort)](#attempt-7-improved-merge-join-using-hashing-and-bucket-sort)
  * [Index-based Algorithms](#index-based-algorithms)
    * [Attempt 8: Index join](#attempt-8-index-join)
<!-- TOC -->

---


## Physical Plan Operators

- **Algorithm** that implements one of the basic relational operations that are used in query plans
  - For example, relational algebra has join operator. How that join is carried out depends on:
    - structure of relations
    - size of relations
    - presence of indexes and hashes
    - ...

### Computation Model

- Need to choose good physical-plan operators
  - Estimate the “cost” of each operator
  - Key measure of cost is the number of disk accesses (far more costly than the main memory accesses)
- Assumption: arguments of operator are on disk, the result is in the main memory

---

- **Cost Parameters**
  - `M` Main memory available for buffers
  - `S(R)` Size of a tuple of relation `R` (in blocks)
  - `B(R)` Blocks used to store relation `R`
  - `T(R)` Number of tuples in relation `R` (cardinality of `R`)
  - `V(R, A)` Number of distinct values for attribute `a` in relation `R`

- **Clustered File**
  - Tuples from different relations that can be joined (on particular attribute values) stored in blocks together

- **Clustered Relation**
  - Tuples from relation are stored together in blocks, but not necessarily sorted

- **Clustering Index**
  - Index that allows tuples to be read in an order that corresponds to physical order

### Scan

- Read all of the tuples of a relation `R`
- Read only those tuples of a relation `R` that satisfy some predicate

#### Table Scan

- Tuples arranged in blocks
  - All blocks known to the system
  - Possible to get blocks one at a time
- I/O Cost
  - `B(R)` disk accesses, if `R` is clustered (assumed that per disk access can read at most one block)
  - `T(R)` disk accesses, if `R` is not clustered


#### Index Scan

- An index exists on **some** attribute of `R`
  - Use index to find all blocks holding `R`
  - Retrieve blocks for `R`
- I/O Cost
  - `B(R) + B(Ir)` disk accesses if clustered
    - `B(R) >> B(Ir)` so treat as only `B(R)`
  - `T(R)` disk accesses if not clustered

## One-Pass Algorithms

- **One-Pass Algorithms** 
  - This type of algorithm has only one phase and reads data from disk only once
  - They are typically used in situations where the amount of data is small (all the necessary data can be loaded into memory at once)
- Typically, it requires that at least one argument fits in the main memory
- Three broad categories:
  - Unary, tuple at a time (i.e. `select`, `project`) (non-blocking)
  - Unary, full-relation (i.e. `duplicate elimination`, `grouping`) (may be blocking)
  - Binary, full-relation (i.e. `join`) (typically blocking)

### Unary, Tuple at a Time

``` 
foreach, block of `R`:
    copy block to input buffer
    perform operation (`select`, `project`) on each tuple in block
    move `selected`/`projected` tuples to output buffer
```

![](https://i.postimg.cc/tCQJsHsb/em2.png){: .w-10 .shadow .rounded-10 }

- Cost
  - In general, `B(R)` or `T(R)` disk accesses depending on clustering
  - If operator is a select that compares an attribute to a constant and index exists for attributes used in select, ≪ `B(R)` disk accesses
  - Requires `M ≥ 1`

### Unary, Full-Relation

``` 
foreach, block of `R`:
    copy block to input buffer
    update accumulator
    move tuples to output buffer
```

![](https://i.postimg.cc/Y9jZg3rF/em3.png){: .w-10 .shadow .rounded-10 }

#### Duplicate Elimination

``` 
foreach block of R:
    copy block to input buffer
    foreach tuple in block
        if tuple is not in accumulator
            copy to accumulator
            copy to output buffer
```

Requires `M ≥ B(δ(R))+1` blocks of the main memory
- 1 block for input buffer
- `B(δ(R))` blocks for accumulator (records each tuple seen so far)
- Accumulator implemented as in-memory data structure (tree, hash)
- If fewer than `B(δ(R))` blocks of memory available, thrashing likely
- Cost is `B(R)` disk accesses

#### Grouping

Grouping operators: `min, max, sum, count, avg`

- Accumulator contains per-group values
- Output only when all blocks of `R` have been consumed
- Cost is `B(R)` disk accesses

### Binary, Full-Relation

Binary operators: `union, intersection, difference, product, join`

- In general, cost is `B(R) + B(S)`
  - `R, S` are operand relations
- Requirement for one pass operation: `min(B(R), B(S)) ≤ M − 1`

#### Join

- Two relations, `R(X,Y)` and `S(Y,Z)`,` B(S) < B(R)`
  - `R, S` are operand relations
  - `X, Y, Z` are attributes in the relations
- Uses the main memory search structure keyed on `Y`

``` 
foreach block of S:
    read block
    add tuples to search structure
foreach block of R:
    copy block to input buffer
    foreach tuple in block
        find matching tuples in search structure
        construct new tuples and copy to output
```

- Nested-loop join
  - Also known as iteration join
  - Assuming that we’re joining relations `R, S` on attribute `a`

``` 
foreach r ∈ R
    foreach s ∈ R
        if r.a = s.a then output <r, s>
```


## Example of Binary Operators: Join (in One-Pass Algorithms)

Consider a join between relations `R1, R2` on attribute `a`:

```
T(R1)= 10,000
T(R2)= 5,000
S(R1) = S(R2) = 0.1
M=101
```

### Attempt 1: Tuple-Based Nested Loop Join

- Relations are not contiguous: one disk access per tuple (Not Clustered)
 
---

- `R1` is outer relation (An outer relation is usually the driving table, meaning that it is the table that the algorithm starts scanning). 
- `R2` is inner relation (An inner relation is the driven table, it is scanned once for each tuple in the outer relation)
- Cost for each tuple in `R1` = `cost to read tuple + cost to read R2 (to join)` = `1 + T(R2)`

**Total Cost** = `T(R1) ∗ (1 + T(R2))` = `10,000 ∗ (1 + 5,000)` = `50,010,000` disk accesses

#### Attempt 2: Block-Based Nested Loop Join

- We can do better by:
  - Use all available main memory `(M = 101)`
  - Read outer relation `R1` in chunks of 100 blocks
    - The purpose of this is to r**educe the number of accesses to the disk**, since multiple rows of data can be read from the disk into memory at one time.
  - Read all of inner relation R2 (using 1 block) + join
    - A **block** usually corresponds to a page of data on a disk, which **is the smallest unit of data read or written**. Every time a disk is read or written, at least one complete block is involved.
- This approach is actually a simplified **Block Nested-Loop Join** that attempts to improve performance by **reducing I/O operations**. 
  - When main memory is large enough to store one or more large blocks of outer relations

---

- Tuples of `R1` stored in a 100-block chunk = `100 * 1/S(R1)` = 1,000 tuples
  - Since `S(R1)` is the size, here it is `0.1`, so per 100-block chunk contains `100 * 1/0.1` = 1000 tuples.
- Number of 100-block chunks to store R1 = `T(R1) / 1,000` = 10
  - `T(R1)` divided by the number of tuples per chunk, which is 10,000 / 1,000 = 10. This means the whole `R1` can be divided into 10 chunks.
- Cost to process each chunk = `1000 + T(R2)` = 6,000 disk accesses
  - Processing a chunk means reading all the tuples in it and matching each one with every tuple in `R2`.
  - Cost to read per chunk of `R1` = 1,000 disk accesses (per chunk contains 1000 tuples)
  - Thus, the cost is `1,000 + T(R2)` disk accesses.

**Total Cost** = `T(R1) / 1,000 ∗ (1000 + T(R2))` = `10 ∗ 6000` = `60,000` disk accesses

- Compared to the tuple-based nested loop join, which had a total cost of 50,010,000 disk accesses, the block-based nested loop join **significantly reduces the number of disk accesses, improving the efficiency of the query**. 

### Attempt 3: Join Reordering

- We can do better by:
  - `R1` becomes the inner relation
  - `R2` becomes the outer relation
- **The choice of outer and inner relations** has a significant impact on the performance of the query, as it **determines the frequency of the inner circular scan**.
  - It is usually more efficient to **select a table with fewer rows as an outer relation**, as this means that the inner relation will be scanned less often.

---

- Tuples of `R2` stored in a 100-block chunk = `100 * 1/S(R1)` = 1,000 tuples
- Number of 100-block chunks to store R1 = `T(R1) / 1,000` = 5
  - This means the whole `R2` can be divided into 5 chunks.
- Cost to process each chunk = `1000 + T(R1)` = 11,000 disk accesses
  - Cost to read per chunk of `R2` = 1,000 disk accesses (per chunk contains 1000 tuples)
  - Thus, the cost is `1,000 + T(R1)` disk accesses.

**Total Cost** = `T(R2) / 1,000 ∗ (1000 + T(R1))` = `5 ∗ 11,000` = `55,000` disk accesses

### Attempt 4: Contiguous Relations (Clustered)

- We can do better by:
  - if the tuples in each relation are contiguous (i.e. clustered)

---

- `B(R1) = T(R1)/S(R1)` = 1,000 blocks
  - the total number of blocks needed for relation `R1`
- `B(R2) = T(R2)/S(R2)` = 500 blocks
  - the total number of blocks needed for relation `R2`
- Cost to read one 100-block chunk of `R2` = 100 disk accesses
  - Here, it is **assumed that per disk access can read at most one block** (in practice, multiple blocks can be read in single disk access).
  - So, here, each 100-block chunk requires 100 disk accesses.
- Cost to process each chunk = `100 + B(R1)` = 1,100

**Total Cost** = `(B(R2) / 100) * 1,100` = `5 ∗ 1,100` = `5,500` disk accesses

### Attempt 5: Merge Join

- We can do better by:
  - if both relations are contiguous and sorted by the join attribute
    - **Merge join** is an efficient joining method that **requires both relations to be pre-sorted on the joining attributes.** When this condition is met, the merge join just needs to sequentially traverse through both relations once.

---

- Read each block of R1 and R2 once only

**Total cost** = `B(R1) + B(R2)` = `1,000 + 500` = 1,500 disk accesses

(It is still assumed that per disk access can read at most one block)

## Two-Pass Algorithms

- **One-Pass Algorithms**: Read data from disk only once

---

- What if `R1` and `R2` aren’t sorted by the join attribute?
  - need to sort `R1` and` R2` first

### Merge Sort

- Cost of Merge Sort **requires 4 disk accesses for each data**. Because it is an **external sorting** algorithm, it requires multiple moves of data between disk and memory.
- **External sorting** algorithm is typically used to handle datasets **too large to fit into memory all at once.** Therefore, it involves **breaking down the data into manageable chunks**, sorting each chunk in memory, and then **merging these sorted chunks into a final ordered dataset.** Typically, **4 disk accesses are required for each piece of data.**
  - **First Read**: Data is read from the disk into memory for processing.
  - **First Write**: The sorted chunks of data in memory are written back to disk as temporary sorted blocks.
  - **Second Read**: During the merge phase, these sorted blocks are read back into memory to be merged.
  - **Second Write**: The final sorted result, after merging, is written back to the disk. This could be the final output of the sort operation or used as input for other database operations, such as a join.

---

**For example:**

- For each 100-block chunk of R:
  - **Read** chunk
  - Sort in memory
  - **Write** to disk

![](https://i.postimg.cc/j2Wxv6dG/ad.png){: .w-10 .shadow .rounded-10 }
_Contain one read and one write_

- **Read** a part of each sorted 100-block chunk of R (Main memory size needs to be able to hold these parts)
- Merge them in the main memory
- **Write** to the final sorted result (in disk)

![](https://i.postimg.cc/tC3Tc5zj/ad2.png){: .w-10 .shadow .rounded-10 }
_Contain one read and one write_

---

So, Cost of Merge Sort for `R1` and `R2`

- Each tuple is read, written, read, written
  - Sort cost `R1`: 4 x 1,000 = 4,000 disk accesses
  - Sort cost `R2`: 4 x 500 = 2,000 disk accesses

### Attempt 6: Merge Join (with Sort)

- R1, R2 contiguous, but unordered

---

**Total cost** (Merge join with sort) = sort cost + join cost = `(4,000 + 2,000) + 1,500` = 7,500 disk accesses

#### Which is better, Merge Join (with Sort) or Nested Loop (Clustered)?

**It depends on the number of relations.**

---

- If: 
  - R1 = 1,000 blocks (contiguous)
  - R2 = 500 blocks (not ordered)


- Total cost (Nested loop cost) = `(500/100) * (100 + 1,000)` = **5,500** disk accesses
  - Same as: [Attempt 4: Contiguous Relations](#attempt-4-contiguous-relations-clustered)
- Total cost (Merge join cost with sort) = sort cost + join cost =`4 * (1,000+500)` + `(1,000+500)` = **7,500** disk accesses
- In this case, Nested Loop is better

---

- But, if:
  - R1 = 10,000  blocks (contiguous)
  - R2 = 5,000 blocks (not ordered)
- Total cost (Nested loop cost) = `(5,000/100) * (100 + 10,000)` = **505,000** disk accesses
  - `R2` is divided into 100-block chunks, so 50 cycles are needed.
  - For each chunk of `R2 `processed (100 blocks in size), the total cost is `100` (to read this chunk of R2) + `10,000` (to traverse all the blocks of R1),
- Total cost (Merge join cost with sort) = sort cost + join cost =`4 * (10,000+5,000)` + `(10,000+5,000)` = **75,000** disk accesses
- In this case, merge join (with sort) is better

### Attempt 7: Improved Merge Join (using Hashing and Bucket Sort)

- Partition relation into M-1 buckets
- In general:
  - Read relation a tuple at a time
  - Hash tuple to a bucket
  - When the bucket is full, move to disk and reinitialise bucket
- Cost of Bucket Sort **requires 2 disk accesses for each data**. 

Total cost = sort cost + join cost = `2 * (B(R1) + B(R2))` + `(B(R1) + B(R2))` = `3 * (B(R1) + B(R2))` = `3 * (1,000 + 500)` = 4,500 disk accesses

## Index-based Algorithms

- What if we have an index on the join attribute?
  - Assume `R2.a`index exists and fits in memory (`a` is the joining attributes)
  - Assume `R1` contiguous, unordered

### Attempt 8: Index join

- Assume that Cost of Reads `R1` is 500 disk accesses
- Assume that `R1` has 5000 tuples
  - foreach `R1` tuple:
    - probe index: free (free: no disk access is required, as it is assumed that the indexes are all in memory)
    - if matched, read `R2` tuple: 1 disk access (because of Index)

— How many matching tuples?
  - If `R2.a` is key, `R1.a` is foreign key
    - expected number of matching tuples = 1
    - Cost = 500 + 5000 * 1 * 1 = **5,500** disk accesses
  - If `V(R2,C)` = 5000, `T(R2)` = 10,000 and uniform assumption,
    - expected number of matching tuples = 10,000/5,000 = 2
    - Cost = 500 + 5000 * 2 * 1 = **10,500** disk accesses
  - Assume `domain(R2, C)`=1,000,000, `T(R2)` = 10,000 with an alternate assumption
    - expected number of matching tuples = 10,000 /1,000,000 = 1/100
    - Cost = 500 + 5000 * 1/100 * 1 = **550** disk accesses
  
More about Index: [Is the Index a Panacea?](/posts/Database-Index/)
