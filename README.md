<h1 align="center">
  <a href="https://github.com/CreatureOX/Mysql2Markdown">
    Mysql2Markdown
  </a>
</h1>
<p align="center">
  Generate markdown documents for MySQL~
</p>

## Dependency  
1. PyMySql

``` sh
pip install -r requirements.txt
```

## Usage
``` sh
$ python mysql2MarkdownUtil.py -h

usage: mysql2MarkdownUtil.py [-h] [-H HOST] [-P PORT] [-u USERNAME]
                             [-p PASSWORD] [-d DATABASE] [-c CHARSET]
                             [-t TABLES [TABLES ...]]

mysql to markdown util

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST
  -P PORT, --port PORT
  -u USERNAME, --username USERNAME
  -p PASSWORD, --password PASSWORD
  -d DATABASE, --database DATABASE
  -c CHARSET, --charset CHARSET
  -t TABLES [TABLES ...], --tables TABLES [TABLES ...]
                        default all tables,support ',' separator and regexp
```

# Effect
![slow_log.png](https://i.loli.net/2020/10/20/9EnIoRgPCjk1htU.png)