# Intro to SQL Part 4 - INSERT, UPDATE, and DELETE

## INSERT & UPDATE: Writing to a database

### SQL: insert a row into a table

```sql
INSERT INTO table_1
    (column_1, column_2)
VALUES
    (value_1, value_2)
```

* You should match data types for columns - you can explicitly cast data types but results can be
unpredictable with some DBMS
* You must specify a value for any column that doesn't allow NULL values or has a default defined

### SQL: update table rows

```sql
UPDATE table_1
SET
    column_1=value_1,
    column_2=value_2
WHERE…
```

### SQL: Delete table rows

```sql
DELETE
FROM table_1
WHERE…
```
