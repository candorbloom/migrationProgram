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
def selectTbBank():
    query = "select * from tb_bank"
    result = selectSql(query)
    parsingTbBank(result)

## targetDB에서 가져온 tb_bank 데이터 파싱하기
def parsingTbBank(result) :
    migrationParam = {}
    for data in result:
        migrationParam['idx'] = data[0]
        migrationParam['name'] = data[1]
        migrationParam['manager'] = data[2]
        migrationParam['phone'] = data[3]
        migrationParam['email'] = data[4]
        migrationParam['zipcode'] = data[5]
        #빈주소처리
        if data[6] is not None :
            count=0
            migrationParam['address_2'] = ""
            migrationParam['address_3'] = ""
            for address in data[6].split(" ") :
                if count == 0 :
                    migrationParam['address_1'] = address
                elif count == 1 : 
                    migrationParam['address_2'] = address
                else :
                    migrationParam['address_3'] += (" " + address)    
                count+=1
        migrationParam['ci_image_path'] = data[8]
        migrationParam['created_at'] = data[9]
        migrationParam['is_used'] = data[10]
        migrationParam['admin_id'] = data[11]
        
        insertBankToClient(migrationParam)     

def insertBankToClient(migrationParam):
    query = "INSERT INTO tb_client (updated_at, idx, name ,manager, phone, email, zipcode, address_1, address_2, address_3, ci_image_path, created_at, is_used, admin_id) values (now(), {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}');"
    query = query.format(migrationParam['idx'],
                        migrationParam['name'],
                        migrationParam['manager'],
                        migrationParam['phone'],
                        migrationParam['email'],
                        migrationParam['zipcode'],
                        migrationParam['address_1'],
                        migrationParam['address_2'],   
                        migrationParam['address_3'],
                        migrationParam['ci_image_path'],
                        migrationParam['created_at'],
                        migrationParam['is_used'],
                        migrationParam['admin_id'])
    insertSql(query)
    print(query)

    
selectTbBank()





