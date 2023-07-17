# IOCCC Winners Database

This repository contains a database of all the winners in the International Obfuscated C Code Contest (IOCCC). 
The database includes information about each winner, including their source code, spoiler, hint (if available), and the
year of their participation.

## Introduction

The International Obfuscated C Code Contest is a renowned competition that celebrates the art of writing creative, 
puzzling, and obfuscated C code. This database aims to provide a comprehensive collection of IOCCC winners, making it
easier for enthusiasts and researchers to explore and analyze the contest's historical entries.

## How to Access the Database

The IOCCC Winners Database is available in SQLite format, allowing for easy integration with various applications and 
programming languages. To access the database, follow these steps:

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/nir-mo/ioccc-db.git
   ```

2. Navigate to the repository directory:
   ```
   cd ioccc-db
   ```

3. The SQLite database file is located at `ioccc_winners.sqlite`. You can use your preferred SQLite client or library 
   to connect to the database and perform queries.

4. Explore the database schema to understand the available tables and columns. The `winners` table contains the 
   following columns:
   - `name` (TEXT): The name of the IOCCC winner.
   - `year` (INTEGER): The year of participation.
   - `spoiler` (TEXT): The spoiler associated with the entry.
   - `prog` (BLOB): The program source code as a binary large object.
   - `hint` (TEXT): A hint related to the entry (if available).

## How to Generate the Database

The `build_sqllite_db.py` script in this repository can be used to generate the SQLite database from IOCCC winner 
entries. To generate the database, follow these steps:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the `ioccc_db/cli.py` script, specifying the directory containing the IOCCC winner entries:
   ```
   python ioccc_db/cli.py --verbose --force --output_file=../ioccc_winners.sqlite
   ```

3. The script will generate the `ioccc_winners.sqlite` file, which contains the SQLite database with all the winners 
   information.

## Technical Debts

The following are the known technical debts and areas for improvement in this repository:

- Add unit tests to ensure the correctness of the database generation process.
- Add support for hints with the encoding of Latin-1 to handle special characters and non-ASCII characters in the hint 
  field.


## License

This project is licensed under the MIT License. For more information, please refer to the [LICENSE](LICENSE) file.
