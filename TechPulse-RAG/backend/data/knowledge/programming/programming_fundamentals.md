# Programming Fundamentals

Programming is the process of expressing algorithms and data transformations in a language a computer can execute.

## Arrays
An array stores elements in contiguous memory and supports constant-time indexed access. Inserting or deleting in the middle can require shifting elements.

## Linked Lists
A linked list stores nodes connected by references. A singly linked list node usually contains data and a pointer to the next node. Traversal is O(n). Insertion at a known node can be O(1).

## Stack
A stack follows LIFO: last in, first out. Common operations are push and pop.

## Queue
A queue follows FIFO: first in, first out. Common operations are enqueue and dequeue.

## Hash Tables
A hash table maps keys to values using a hash function. Average-case lookup, insertion and deletion are commonly O(1), although collisions can degrade performance.

## Binary Search
Binary search works on sorted data. It repeatedly compares the target with the middle element and discards half of the search space. Time complexity is O(log n).

## Big O
Big O describes how resource usage grows with input size. Common complexities include O(1), O(log n), O(n), O(n log n), and O(n²).
