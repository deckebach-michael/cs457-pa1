# CS457 PA1: DBMS
(DATABASE MANAGEMENT SYSTEM)

## How to run the code
You can start the dbms by running dbms.py file in the /src/ directory. Once you have the dependencies installed (see here), run the program like so:

    python src/dbms.py

Additionally, the dbms has been tested using the PA1 test script. The test script can be run through the dmbs like so:

    python src/dbms.py < tests/pa1_test.txt

## Dependencies
This program is built using Python 3.10.4. It uses the following standard library modules:
- csv - for file creation/deletion/manipulation
- re - for parsing SQL statements
- os - for directory creation/deletion as well as file/directory existance checking

## How are databases structured and managed? 
Under the hood, databases are represented by simple folders/directories. A simple Database class is implemented which allows the user to interact with the folder. Multiple databases are represented by multiple folders, making it easy to switch between databases by simply changing the current working directory. All tables for a given database are stored within their database's folder, so there is no risk of access or modification of a table in a database which is not currently selected or in use.

## How are tables structured and managed?
Tables are stored as comma-separated files, where the first row in the file represents the headers or fields for the table, and each subsequent row represents a tuple or record of data in that table.

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

### DROP DATABASE
Removes the database `<database>` and any tables within. Under the hood, it is using os.remove and os.rmdir to achieve this.

    DROP DATABASE <database>;

### DROP TABLE
Removes a specific `<table>` from the active database. Under the hood, it is using os.remove.

    DROP TABLE <table>;

### SELECT
Queries and returns all values from `<table>`. Under the hood, it is using csv.reader and joining all values using a | separator before printing results to the terminal.

    SELECT * FROM <table>;

### USE
Changes the active database to `<database>`. This command must be used before any of the `<table>` commands listed above. Under the hood, it is using os.chdir.

    USE <database>;

### EXIT
Finally, while not a SQL command, the special keyword 'EXIT' is supported to terminate the program.

    EXIT - terminates the program

Note that for all SQL commands (i.e., excluding EXIT), semicolons (;) are strictly required. The program will return an error message if you attempt to pass it a SQL command that does not end in a semicolon.

## Contact
You can find the repository at https://github.com/deckebach-michael/dbms

To request access or for any questions, email Michael Deckebach at michael.deckebach@gmail.com