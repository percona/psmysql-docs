| Benefit                   | Description                                                                                       |
|---------------------------|---------------------------------------------------------------------------------------------------|
| Generates Sequences       | Acts as an inline table-valued function that generates a sequence of numbers.                     |
| Table-Valued Function     | Unlike traditional scalar functions, the function returns a virtual table with a single column named `value` containing the generated sequence. |
| Simpler Syntax            | Simplifies queries that need to generate predictable sequences of numbers.                        |
| Flexibility               | Allows dynamic definition of sequences within queries, offering more control compared to pre-defined tables for sequences. |
| Predefined Sequence       | Does not manage sequences like Oracle or PostgreSQL; instead, it allows definition and generation of sequences within a `SELECT` statement. |
| Customization             | Enables customization of starting value, increment/decrement amount, and number of values to generate. |
