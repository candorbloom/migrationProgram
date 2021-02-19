
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


## targetDB에서 tb_device 데이터 가져오기 
def selectTbDevice():
    query = "select euid, installed_lat, installed_lng, created_at, model, lux , asis_acc_threshold, asis_mag_threshold tb_detector from tb_detector order by euid;"
    result = selectSql(query)
    parsingTbDevice(result)


def parsingTbDevice(result):
    param = {}
    for data in result :
        print(data)
        param['euid'] = data[0]
        param['installed_lat'] = data[1]
        param['installed_lng'] = data[2]

        # 빈 데이터 처리
        param['created_at'] = ''
        if (data[3] == None) or (data[3] == ''):
            param['created_at'] = '1000-10-10'
        else :
            param['created_at'] = data[3]
        
        param['type'] = data[4]
        param['default_lux'] = data[5]
        param['threshold_acc'] = data[6]
        param['threshold_mag'] = data[7]
        param['firmware'] = 9999
        param['status_code'] = 3

        insertToDevice(param)


def insertToDevice(param):
    query = "INSERT INTO tb_device (euid, installed_lat, installed_lng, created_at, type, default_lux, threshold_acc, threshold_mag, firmware, status_code) values ('{}', '{}', '{}', '{}', '{}', {}, {}, {}, '{}', {})"
    query = query.format(param['euid'],
            param['installed_lat'],
            param['installed_lng'],
            param['created_at'],
            param['type'],
            param['default_lux'],
            param['threshold_acc'],
            param['threshold_mag'],
            param['firmware'],
            param['status_code'])
    print(query)
    
    insertSql(query)


selectTbDevice()
