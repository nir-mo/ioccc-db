# IOCCC Winners Database

This repository contains a database of all the winners in the International Obfuscated C Code Contest (IOCCC). 
The database includes information about each winner, including their source code, spoiler, hint (if available), and the
year of their participation.

The information in this database was gathered from the official IOCCC repository available at
[https://github.com/ioccc-src/winner](https://github.com/ioccc-src/winner). We are grateful to the IOCCC community for
providing this valuable collection of obfuscated C code entries.

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

## Explore the IOCCC winners DB


```python
import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('ioccc_winners.sqlite')

# Query to select 10 rows of data from the "winners" table
query = "SELECT * FROM winners WHERE year < 1998 LIMIT 10"

# Read the table into a pandas DataFrame
df = pd.read_sql_query(query, conn)

conn.close()
```


```python
df
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>year</th>
      <th>spoiler</th>
      <th>prog</th>
      <th>hint</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>litmaath</td>
      <td>1988</td>
      <td>sorts each arg using only argc, argv, and 'whi...</td>
      <td>b'main(argc, argv)\nint\targc;\nchar\t**argv;\...</td>
      <td>Best small program:\n\n\tMaarten Litmaath\n\tF...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>phillipps</td>
      <td>1988</td>
      <td>'first day of christmas', tables, heavily main...</td>
      <td>b'main(t,_,a )\nchar\n*\na;\n{\n\t\t\t\treturn...</td>
      <td>Least likely to compile successfully:\n\n\tIan...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>reddy</td>
      <td>1988</td>
      <td>prints name of 'char *(*(foo[16])();', compressed</td>
      <td>b'#include&lt;stdio.h&gt;\n#include&lt;ctype.h&gt;\n#defin...</td>
      <td>Most useful Obfuscated C program:\n\n\tAmperif...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>westley</td>
      <td>1988</td>
      <td>prints '3.141', circle made of '_-_-_-_' in la...</td>
      <td>b'#define _ -F&lt;00||--F-OO--;\nint F=00,OO=00;m...</td>
      <td>Best layout:\n\n    \tMerlyn LeRoy (Brian West...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>applin</td>
      <td>1988</td>
      <td>massive #define stuff, includes itself; prints...</td>
      <td>b'I a\nU a\nI b\nU b\nI c\nU c\nI d\nU d\nI e\...</td>
      <td>Best of show:\n\n    \tJack Applin\n\tHewlett-...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>spinellis</td>
      <td>1988</td>
      <td>#include "/dev/tty"</td>
      <td>b'#include "/dev/tty"\n'</td>
      <td>Best abuse of the rules:\n\n    \tDiomidis Spi...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>robison</td>
      <td>1988</td>
      <td>print e in any base, uses only --, &gt;=, and whi...</td>
      <td>b'#include &lt;stdio.h&gt;\nunsigned char w,h,i,l,e,...</td>
      <td>Best abuse of C constructs:\n\n    \tArch D. R...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>dale</td>
      <td>1988</td>
      <td>prints command line, using lots of system calls</td>
      <td>b'#define _ define\n#_ P char\n#_ p int\n#_ O ...</td>
      <td>Best abuse of system calls:\n\n    \tPaul Dale...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>isaak</td>
      <td>1988</td>
      <td>table driven table of the elements; cpp, self-...</td>
      <td>b'main(){}\x0c\n#define P define\n#P U ifdef\n...</td>
      <td>Best visuals:\n\n    \tMark Isaak\n\tImagen Co...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>bright</td>
      <td>1986</td>
      <td>hex dump, cpp compressed, uses lost of &lt;&lt; for ...</td>
      <td>b'#include &lt;stdio.h&gt;\n#define O1O printf\n#def...</td>
      <td># Most useful obfuscation \n\nWalter Bright\n\...</td>
    </tr>
  </tbody>
</table>
</div>



### print the obfuscated program


```python
westley = df[df.name == "westley"]
prog = westley.prog.values[0]

import codecs
print(codecs.decode(prog))
```

    #define _ -F<00||--F-OO--;
    int F=00,OO=00;main(){F_OO();printf("%1.3f\n",4.*-F/OO/OO);}F_OO()
    {
                _-_-_-_
           _-_-_-_-_-_-_-_-_
        _-_-_-_-_-_-_-_-_-_-_-_
      _-_-_-_-_-_-_-_-_-_-_-_-_-_
     _-_-_-_-_-_-_-_-_-_-_-_-_-_-_
     _-_-_-_-_-_-_-_-_-_-_-_-_-_-_
    _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
    _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
    _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
    _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
     _-_-_-_-_-_-_-_-_-_-_-_-_-_-_
     _-_-_-_-_-_-_-_-_-_-_-_-_-_-_
      _-_-_-_-_-_-_-_-_-_-_-_-_-_
        _-_-_-_-_-_-_-_-_-_-_-_
            _-_-_-_-_-_-_-_
                _-_-_-_
    }
    



## How to Generate the Database

To generate the IOCCC Winners Database, follow these steps:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Fetch the submodule from the IOCCC winners repository:
   ```
   git submodule update --init
   ```
   
   __OR__, If you encounter any issues with the submodule, you can clone the IOCCC winners repository manually into the
   `winners` directory:
   ```
   git clone https://github.com/ioccc-src/winner winners
   ```

3. Run the `ioccc_db/cli.py` script, specifying the directory containing the IOCCC winner entries:
   ```
   python ioccc_db/cli.py --verbose --force --output_file=../ioccc_winners.sqlite --ioccc_winners_directory=ioccc/winners.directory
   ```

4. The script will generate the `ioccc_winners.sqlite` file, which contains the SQLite database with all the winners 
   information.

## Technical Debts

The following are the known technical debts and areas for improvement in this repository:

- Add unit tests to ensure the correctness of the database generation process.
- Add support for hints with the encoding of Latin-1 to handle special characters and non-ASCII characters in the hint 
  field.


## License

This project is licensed under the MIT License. For more information, please refer to the [LICENSE](LICENSE) file.
