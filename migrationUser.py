
import os
import psycopg2
import time

TARGET_DB = "smms_iot"
TARGET_DB_HOST = "15.165.80.49"
TARGET_DB_PORT = "5432"
TARGET_DB_USER = "smms_main"
TARGET_DB_PASSWORD = "!!##Cntech#@201217!smms"

MIGRATION_DB = "smms"
MIGRATION_DB_HOST = "smms-v3-db.cy3ime2ikct9.ap-northeast-2.rds.amazonaws.com"
MIGRATION_DB_PORT = "5432"
MIGRATION_DB_USER = "smms"
MIGRATION_DB_PASSWORD = "cntech00##"


# 조회 함수
def selectSql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(TARGET_DB, TARGET_DB_USER, TARGET_DB_HOST, TARGET_DB_PORT, TARGET_DB_PASSWORD))
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(e)

# 입력 함수
def insertSql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MIGRATION_DB, MIGRATION_DB_USER, MIGRATION_DB_HOST, MIGRATION_DB_PORT, MIGRATION_DB_PASSWORD))
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)



## targetDB에서 tb_bnak 데이터 가져오기 
def selectTbAccount():
    query = "select * from tb_account"
    result = selectSql(query)
    parsingTbAccount(result)


def parsingTbAccount(result):
    param = {}
    for data in result:
        param['uid'] = data[0]
        param['name'] = data[1]

        param['phone'] = ''
        if (data[7] == None) or (data[7] == ''):
            print('pass_phone')
        else:
            param['phone'] = data[7]
        
        param['client_idx'] =''
        if (data[6] == None) or (data[6] == ''):
            print('pass_client_idx')
        else :
            param['client_idx'] = data[6]
        
        param['email'] = ''
        if (data[8] == None) or (data[8] == ''):
            print('pass_email')
        else:
            param['email'] = data[8]
        
        param['created_at'] = data[12]
        param['password'] = data[2]
        insertAccountToUser(param)

def insertAccountToUser(param):
    query = "INSERT INTO tb_user (uid, name, phone, client_idx, email, created_at, password) values ('{}', '{}', '{}', {}, '{}', '{}', '{}')"
    query = query.format( param['uid'],
                        param['name'],
                        param['phone'],
                        param['client_idx'],
                        param['email'],
                        param['created_at'],
                        param['password'])
    insertSql(query)
    print(query)



selectTbAccount()

