#-*- coding: utf-8 -*-
import pymysql
import argparse
import re

config = {
          'host':'',
          'port':None,
          'user':'',
          'password':'',
          'database':'',
          'charset':'',
          'cursorclass':pymysql.cursors.Cursor,
          }


HEADERS = [
    "| position | name  | type | key  |  is nullable  | extra | description | default |",
    "| :--: | :--:  | :--: | :--: | :--: | :--: | :--: |  :--:  |"
]
COLUMN_FORMAT = "|  '{ORDINAL_POSITION}'  |  '{COLUMN_NAME}'  |  '{COLUMN_TYPE}'  |  '{COLUMN_KEY}'  |  '{IS_NULLABLE}'  |  '{EXTRA}'  |  '{COLUMN_COMMENT}'  |   '{COLUMN_DEFAULT}'   |"

TABLE_INFO_SQL = "SELECT `table_name`,`table_comment` FROM `information_schema`.`tables` WHERE `table_schema`='{TABLE_SCHEMA}'"
COLUMN_INFO_SQL = "SELECT `ORDINAL_POSITION`,`COLUMN_NAME`,`COLUMN_TYPE`,`COLUMN_KEY`,`IS_NULLABLE`,`EXTRA`,`COLUMN_COMMENT`,`COLUMN_DEFAULT` FROM `information_schema`.`columns` WHERE `table_schema`='{TABLE_SCHEMA}' AND `table_name`='{TABLE_NAME}' ORDER BY `ORDINAL_POSITION` ASC"

TARGET_TABLES = []

def init():
    parser = argparse.ArgumentParser(description="mysql to markdown util")
    parser.add_argument('-H','--host',default='127.0.0.1')
    parser.add_argument('-P','--port',type=int,default=3306)
    parser.add_argument('-u','--username',default='root')
    parser.add_argument('-p','--password',default='root')
    parser.add_argument('-d', '--database',default='mysql')
    parser.add_argument('-c', '--charset',default='utf8mb4')
    parser.add_argument('-t', '--tables', nargs='+',default=None,help="default all tables,support ',' separator and regexp")
    args = parser.parse_args()
    config['host'] = args.host
    config['port'] = args.port
    config['user'] = args.username
    config['password'] = args.password
    config['database'] = args.database
    config['charset'] = args.charset
    global TARGET_TABLES
    TARGET_TABLES = args.tables

def execute_sql(sqlStr):
    conn = pymysql.connect(**config)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sqlStr)
        conn.commit()
        result = cursor.fetchall()
    finally:
        conn.close()
    return result        

def to_markdown():
    content = ""
    table_names = [table_info[0] for table_info in execute_sql(TABLE_INFO_SQL.format(TABLE_SCHEMA = config["database"]))]
    if TARGET_TABLES:
        new_table_names = []
        for table_name in table_names:
            for target_table in TARGET_TABLES:
                if re.search(target_table, table_name):
                    new_table_names.append(table_name)
        table_names = list(set(new_table_names))          
    for table_name in table_names:
        content += "# " + table_name + "\n"
        content += "\n".join(HEADERS)
        content += "\n"
        table_columns = execute_sql(COLUMN_INFO_SQL.format(TABLE_SCHEMA = config["database"], TABLE_NAME = table_name))
        for table_column in table_columns:
            content += COLUMN_FORMAT.format(ORDINAL_POSITION=table_column[0],COLUMN_NAME=table_column[1],COLUMN_TYPE=table_column[2],COLUMN_KEY=table_column[3],IS_NULLABLE=table_column[4],EXTRA=table_column[5],COLUMN_COMMENT=table_column[6],COLUMN_DEFAULT=table_column[7])
            content += "\n"
    
    with open(config["database"] + ".md", "w", encoding="utf-8") as mdFile:
        mdFile.write(content)        
    return content

if __name__ == "__main__":
    init()
    to_markdown()    