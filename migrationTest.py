import os
import psycopg2
import time


MAIN_DB = "smms_v4"
MAIN_DB_USER = "sama"
MAIN_DB_HOST = "52.79.111.170"
MAIN_DB_PORT = "5432"
MAIN_DB_PASSWORD = "sama"



# 조회 함수

def selectSql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MAIN_DB, MAIN_DB_USER, MAIN_DB_HOST, MAIN_DB_PORT, MAIN_DB_PASSWORD))
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(e)

def selectTable():
    query = "select * from tb_code; "
    result = selectSql(query)
    parsing = parsingResult(result)
    # return parsing

def parsingResult(result) :
    for data in result:
        insertWarrant(data)

def insertWarray(data):
    query = "INSERT INTO TB_WARRANTY (WARRANTY_SRL, ..., ..., ..., ...) VALUES ({}, {}, '{}', {})"
    query.format(data[0], data[1], data[2])




# 입력 함수
def insertSql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MAIN_DB, MAIN_DB_USER, MAIN_DB_HOST, MAIN_DB_PORT, MAIN_DB_PASSWORD))
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)