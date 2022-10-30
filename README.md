# CS457 PA1: DBMS
(DATABASE MANAGEMENT SYSTEM)

## How to run the code
You can start the dbms by running dbms.py file in the /src/ directory. Once you have the dependencies installed (see here), run the program like so:

    python src/dbms.py

Additionally, the dbms has been tested using the PA2 test script. The test script can be run through the dmbs either using a filename argument or using the standard input (on Linux):

    python src/dbms.py tests/pa2_test.txt

    python src/dbms.py < tests/pa2_test.txt

## Dependencies
This program is built using Python 3.10.4 and requires Ubuntu version 18 or above. It uses the following standard library modules:
- csv - for file creation/deletion/manipulation
- re - for parsing SQL statements
- os - for directory creation/deletion as well as file/directory existance checking
- sys - for command line argument parsing

## How are databases structured and managed? 
Under the hood, databases are represented by simple folders/directories. A simple Database class is implemented which allows the user to interact with the folder. Multiple databases are represented by multiple folders, making it easy to switch between databases by simply changing the current working directory. All tables for a given database are stored within their database's folder, so there is no risk of access or modification of a table in a database which is not currently selected or in use.

## How are tables structured and managed?
Tables are stored as comma-separated files, where the first row in the file represents the headers or fields for the table, and each subsequent row represents a tuple or record of data in that table.

## How are tuples stored?
Tuples, or table records, are stored as comma-separated rows in the file that represents a table. When loaded into memory, a Record class is created for each tuple. The Record class contains the values as well as metadata of records (field names and types), so that manipulation ofthe tuple can be handled correctly.

## Functionality implemented (at a high level)
At this time, the following SQL statements (and syntax) are supported:

### ALTER TABLE
Allows the user to add a new field or column of table to an already existing table. The table must exist. Note that there is no checking to ensure that field names are unique presently. Under the hood, the program is reading in the existing `<table>` into memory, appending a new field, `<field>`, to each row, and then writing that data back out to a new file of the same name.

    ALTER TABLE <table> ADD <field> <datatype>; 

### CREATE DATABASE
Allows the user to initiate a new, empty database of name `<database>`. Under the hood, the program is using os.mkdir to create a new folder to represent the database.

    CREATE DATABASE <database>; 
    
### CREATE TABLE
Allows the user to initiate a new, empty table of name `<table>`, with n number of fields as listed out in the comma-separated parenthetical group. Under the hood, the program is writing a csv with the first row consistent with the `<field>` list provided.

    CREATE TABLE <table> (<field> <datatype>, <field> <datatype>, ...);

## DELETE
Removes records from a `<table>` according to the condition(s) specified. Under the hood, it opens the table's file and loops through each row checking to see if the condition is satisfied. If it is met, the row is not written back to the file. Thus, only rows that do not meet the criteria are retained.

    DELETE FROM <table> WHERE <condition>;

### DROP DATABASE
Removes the database `<database>` and any tables within. Under the hood, it is using os.remove and os.rmdir to achieve this.

    DROP DATABASE <database>;

### DROP TABLE
Removes a specific `<table>` from the active database. Under the hood, it is using os.remove.

    DROP TABLE <table>;

## INSERT INTO
Adds a record to `<table>`. Under the hood, it opens up the file in append mode and adds the values supplied in the `VALUES` clause as a new row. Simple checking to ensure the correctly number of values is provided.

    INSERT INTO <table> VALUES(<value1>, <value2>, ...);

### SELECT
Queries and returns contents of `<table>`, as specified by the `SELECT` and `WHERE` clauses. Under the hood, it loads the table into memory using csv.reader, then loops through each row as a Record to see if `<condition>` is satisfied. Finally, if the condition is satisfied, it returns the values for the `<columns>` specified in the `SELECT` clause (or all values if the special character `*` is provided). All values are printed to th eterminal using a | separator.

    SELECT <columns> FROM <table> WHERE <condition>;

## UPDATE
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