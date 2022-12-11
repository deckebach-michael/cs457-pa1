# CS457 PA1: DBMS
(DATABASE MANAGEMENT SYSTEM)

## How to run the code
You can start the dbms by running dbms.py file in the /src/ directory. Once you have the dependencies installed (below), run the program like so:

    python src/dbms.py

Additionally, the dbms has been tested using the PA5 test script. You can pass the script via command line argument or standard input (on Linux) like so:

    python src/dbms.py tests/pa5_test.txt

    python src/dbms.py < tests/pa5_test.txt

## Dependencies
This program is built using Python 3.10.4 and requires Ubuntu version 18 or above. It uses the following standard library modules:
- csv - for file creation/deletion/manipulation
- re - for parsing SQL statements
- os - for directory creation/deletion as well as file/directory existance checking
- shutil - for creating separate copies of tables (for transactions)
- sys - for command line argument parsing

## How are databases structured and managed? 
Under the hood, databases are represented by simple folders/directories. A simple Database class is implemented which allows the user to interact with the folder. Multiple databases are represented by multiple folders, making it easy to switch between databases by simply changing the current working directory. All tables for a given database are stored within their database's folder, so there is no risk of access or modification of a table in a database which is not currently selected or in use.

## How are tables structured and managed?
Tables are stored as comma-separated files, where the first row in the file represents the headers or fields for the table, and each subsequent row represents a tuple or record of data in that table.

## How are tuples stored?
Tuples, or table records, are stored as comma-separated rows in the file that represents a table. When loaded into memory, a Record class is created for each tuple. The Record class contains the values as well as metadata of records (field names and types), so that manipulation ofthe tuple can be handled correctly.

## How are transactions implemented?
Transactions are implemented by created separate `<table>_lock` versions of the table files. This means locking is done at the table level. If a `_lock` table file is present, any user knows that the table is locked in a transaction. This also allows for concurrent users to read from the original disk version of a table if a transaction is mid-process but has not yet been committed. Once committed, the contents of the `_lock` file overwrite the original copy, thus "writing to disk."

## How are aggregations performed?
Only single aggregations on complete tables are supported at this time. At a high level, the field to be aggregated and the type of aggregation to be performed are extracted using regex. The table is then read into memory, and the specific field is added to a list. The following aggregation functions are supported:

    COUNT() - returns the number of rows in the table
    AVG(<field>) - returns the average value for the specified field, as a decimal
    MAX(<field>) - returns the greatest value for the specified field, as an integer

## Functionality implemented (at a high level)
At this time, the following SQL statements (and syntax) are supported:

### ALTER TABLE
Allows the user to add a new field or column of table to an already existing table. The table must exist. Note that there is no checking to ensure that field names are unique presently. Under the hood, the program is reading in the existing `<table>` into memory, appending a new field, `<field>`, to each row, and then writing that data back out to a new file of the same name.

    ALTER TABLE <table> ADD <field> <datatype>; 

### BEGIN TRANSACTION
Beings a transaction event. It flips the session variable `is_transaction` to True, which is then used by subsequent commands to track what tables have been locked and modified.

    BEGIN TRANSACTION;

### COMMIT
Completes a transaction event. It goes through every table locked by the transaction and commits their changes to disk. If no changes have been made, a transaction abort message is displayed.

### CREATE DATABASE
Allows the user to initiate a new, empty database of name `<database>`. Under the hood, the program is using os.mkdir to create a new folder to represent the database.

    CREATE DATABASE <database>; 
    
### CREATE TABLE
Allows the user to initiate a new, empty table of name `<table>`, with n number of fields as listed out in the comma-separated parenthetical group. Under the hood, the program is writing a csv with the first row consistent with the `<field>` list provided.

    CREATE TABLE <table> (<field> <datatype>, <field> <datatype>, ...);

### DELETE
Removes records from a `<table>` according to the condition(s) specified. Under the hood, it opens the table's file and loops through each row checking to see if the condition is satisfied. If it is met, the row is not written back to the file. Thus, only rows that do not meet the criteria are retained.

    DELETE FROM <table> WHERE <condition>;

### DROP DATABASE
Removes the database `<database>` and any tables within. Under the hood, it is using os.remove and os.rmdir to achieve this.

    DROP DATABASE <database>;

### DROP TABLE
Removes a specific `<table>` from the active database. Under the hood, it is using os.remove.

    DROP TABLE <table>;

### INSERT INTO
Adds a record to `<table>`. Under the hood, it opens up the file in append mode and adds the values supplied in the `VALUES` clause as a new row. Simple checking to ensure the correctly number of values is provided.

    INSERT INTO <table> VALUES(<value1>, <value2>, ...);

### SELECT
Queries and returns contents of `<table>`, as specified by the `SELECT` and `WHERE` clauses. Under the hood, it loads the table into memory using csv.reader, then loops through each row as a Record to see if `<condition>` is satisfied. Finally, if the condition is satisfied, it returns the values for the `<columns>` specified in the `SELECT` clause (or all values if the special character `*` is provided). All values are printed to the terminal using a | separator.

    SELECT <columns> FROM <table> WHERE <condition>;

#### INNER JOIN
The basic SELECT syntax above is expanded to support INNER JOINs in the following format:

    SELECT <columns> FROM <table1>, <table2> WHERE <condition>;
    SELECT <columns> FROM <table1> INNER JOIN <table2> ON <condition>;

Under the hood, both files for the corresponding tables are opened and iterated through in a nested loop, with `<table1>` records comprising the outer loop and `<table2>` records making up the inner loop. For each combination of records between the two tables, the `<condition>` is evaluated. Only combinations that satisfy the `<condition>` are returned.

#### LEFT OUTER JOIN
The basic SELECT syntax above is expanded to support LEFT OUTER JOINs in the following format:

    SELECT <columns> FROM <table1> LEFT OUTER JOIN <table2> ON <condition>;

This implementation is near-identical to the INNER JOIN implementation. The only difference being that a special `is_printed` boolean flag tracks whether `<table1>`'s record has had at least one match with a record from `<table2>` that satisfies `<condition>` and thus has been returned to the console.

If at the end of the inner loop through `<table2>`'s records, no match has been found (i.e., `is_printed` is still `False`), a special record consisting of the values of the record in `<table1>` with `None` values for the missing `<table2>` fields is constructed and returned to the console.

### UPDATE
Changes values in records from a `<table>` when the row satsifies a given `<condition>`. Under the hood, it opens the table using csv.reader, then loops through each row as a Record to test if it satisfies `<condition>`. If so, it sets the `<target_field>` to `<new_value>` in the Record before writing that record back to disk using csv.writer.

    UPDATE <table> SET <target_field> = <new_value> WHERE <condtion>;

### USE
Changes the active database to `<database>`. This command must be used before any of the `<table>` commands listed above. Under the hood, it is using os.chdir.

    USE <database>;

### EXIT
Finally, while not a SQL command, the special keyword 'EXIT' is supported to terminate the program. Case-sensitive.

    EXIT - terminates the program

Note that for all SQL commands (i.e., excluding EXIT), semicolons (;) are strictly required. The program will return an error message if you attempt to pass it a SQL command that does not end in a semicolon.

## Contact
You can find the repository at https://github.com/deckebach-michael/dbms

To request access or for any questions, email Michael Deckebach at michael.deckebach@gmail.com