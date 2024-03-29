---
title: Is the Index a Panacea?
date: 2024-02-18 18:22:00 UTC
categories: [ (CS) Learning Note, Database ]
tags: [ software engineering, Database ]
pin: false
---

**Indexes play a big part in SQL optimisation.** Used properly, indexes can increase the efficiency of a SQL query by a factor of 10 or more. But is the index a panacea? If indexes can improve efficiency, wouldn't it be better to just create them? In fact, in some cases, creating an index can reduce efficiency.

---
<center><font size='5'> Contents </font></center>

---

<!-- TOC -->
  * [Introduction to Indexing](#introduction-to-indexing)
    * [Why Use Indexing?](#why-use-indexing)
  * [Is the Index a Panacea?](#is-the-index-a-panacea)
    * [When is an Index Created and When is it Not Needed?](#when-is-an-index-created-and-when-is-it-not-needed)
  * [Types of Indexes](#types-of-indexes)
<!-- TOC -->

---

## Introduction to Indexing

Indexing in databases is akin to the index in a book. It is a data structure that improves the speed of data retrieval operations on a database table at the cost of additional writes and storage space to maintain the index data structure. Indexes are used to quickly locate data without having to search every row in a database table every time a database table is accessed.

### Why Use Indexing?

The primary reason to use indexing is to **enhance the performance and efficiency of database queries**. Without indexing, the database server must perform a **full table scan** to retrieve the desired data, which can be time-consuming, especially for large tables. Indexes allow databases to locate the data without scanning each row of the table, significantly reducing the amount of time and resources required for query processing.

## Is the Index a Panacea?

While indexing can dramatically improve query performance, it is not a panacea. Indexes come with their own set of trade-offs:

- **Storage Overhead**: Each index created consumes additional disk space.
- **Maintenance Cost**: Indexes need to be updated whenever the data in the indexed columns is modified, which can slow down write operations such as `INSERT`, `UPDATE`, and `DELETE`.
- **Optimization Complexity**: Over-indexing can lead to unnecessary complexity in query optimization and execution.

### When is an Index Created and When is it Not Needed?

- When to Create an Index:
  - **Frequent Queries**: For columns that are frequently used in WHERE clauses or as join predicates.
  - **High Selectivity**: Columns with a high number of unique values (high selectivity) are good candidates for indexing.
  - **Sorting and Grouping**: Columns that are often used for sorting (`ORDER BY`) and grouping (`GROUP BY`).

- When an Index is Not Needed:
  - **Small Tables**: Tables with few rows might not benefit significantly from indexing, as a full table scan can be efficient enough.
  - **Frequent Modifications**: Tables that undergo heavy INSERT, UPDATE, DELETE operations might suffer from the overhead of maintaining indexes.
  - **Low Selectivity**: Columns with a small range of values (low selectivity), where most queries would retrieve a large percentage of rows.

## Types of Indexes

In terms of **functional logic**, there are 4 main types of indexes:

- **Secondary Index (Ordinary Index)**: Any index that is not a primary index, used to improve the performance of queries not covered by the primary index. 
- **Unique Index**: Ensures that all values in the index are unique, useful for enforcing uniqueness on columns other than the primary key. It is an index that adds a data **uniqueness constraint** to a normal index, which is `UNIQUE`.
- **Primary Index**: Unique index on the primary key of a table, automatically created when the primary key is defined. It adds the **not null constraint** to the unique index, which is `NOT NULL + UNIQUE`. 
- **Full-Text Index**: Designed for text-based columns to facilitate full-text searches. Full-text indexing is not used much. We can usually use specialised full-text search engines such as ES (ElasticSearch) and Solr.

In terms of **physical implementation**, indexes can be classified into 2 types:

- **Clustered Index**: **A clustered index determines the physical order of data in a table.** It sorts and stores the data rows in the table or view based on the key values in the index. Because of this, **a table can have only one clustered index**. 
- **Non-Clustered Index**: A non-clustered index has a structure separate from the data rows. It contains the non-clustered index key values and each key value entry has a pointer to the data row containing the key value. **You can have multiple non-clustered indexes on a table because they do not affect the physical order of the data.** They can be stored anywhere in the database, and the table data is not affected even if a non-clustered index is created or modified. 

In terms of **the number of fields**, indexes can be divided into 2 types:

- **Single Index**: A single index is an index on a single column of a table.
- **Composite Index**: Indexes that are defined on more than one column, useful for queries that involve multiple columns in their predicates. There is a leftmost matching principle for Composite Index, which means that indexes are matched according to the leftmost priority. For example, for (x, y, z), if the query condition is `WHERE x=1 AND y=2 AND z=3` or `WHERE x=1 AND y=2`, you can match the union index; if the query condition is `WHERE y=2`, you cannot match the composite index.


<br>

---

**Reference:**

- Chen, Yang (2019) _What you must know about SQL_. Geek Time.
