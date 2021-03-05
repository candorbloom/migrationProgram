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

# 업데이트 함수
def updateSql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MIGRATION_DB, MIGRATION_DB_USER, MIGRATION_DB_HOST, MIGRATION_DB_PORT, MIGRATION_DB_PASSWORD))
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


## targetDB에서 tb_detector 데이터 가져오기 
def selectTbDetector():
    query = "SELECT euid, warranty_srl FROM tb_detector ORDER BY warranty_srl;"
    result = selectSql(query)
    parsingTbDetector(result)

## targetDB에서 가져온 데이터 파싱
def parsingTbDetector(result):
    param = {}
    for data in result :
        # 데이터 처리
        param['device_euid']=''
        if (data[0] == None) or (data[0] == ''):
            param['device_euid'] = ''
        else :
            param['device_euid'] = data[0]        
        param['idx'] = data[1]
        insertToWarranty(param)

def insertToWarranty(param):
    query = "UPDATE new_warranty SET device_euid='{}' where idx ='{}'"
    query = query.format(param['device_euid'],
                        param['idx'])
    updateSql(query)
    print(query)


selectTbDetector()
