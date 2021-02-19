
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


## targetDB에서 tb_warranty 데이터 가져오기 
def selectTbWarranty():
    query = "select * from tb_warranty where warranty_srl=13665 order by warranty_srl"
    result = selectSql(query)
    parsingTbWarranty(result)


def parsingTbWarranty(result):
    param = {}
    for data in result :

        # 빈 데이터 처리
        param['company_idx'] = ''
        if (data[2] == None) or (data[2] == ''):
            param['company_idx'] = -1
        else :
            param['company_idx'] = data[2]

        param['created_at'] = data[8]
        param['stock_fg'] = data[9]
    
        # 빈 데이터 처리
        param['client_idx'] = ''
        if (data[15] == None) or (data[15] == ''):
            param['client_idx'] = -1
        else :
            param['client_idx'] = data[15]
        
        # 빈 데이터 처리
        param['model_name'] = ''
        if (data[16] == None) or (data[16] == ''):
            param['model_name'] = ''
        else :
            param['model_name'] = data[16]
        
        param['expired'] = data[17]

        # 빈 데이터 처리
        param['expired_at'] = ''
        if (data[18] == None) or (data[18] == ''):
            param['expired_at'] = '1000-10-10'
        else :
            param['expired_at'] = data[18]
        
        # 빈 데이터 처리
        param['started_at'] = ''
        if (data[19] == None) or (data[19] == ''):
            param['started_at'] = '1000-10-10'
        else :
            param['started_at'] = data[19]

        # 빈 데이터 처리
        param['deleted_at'] = ''
        if (data[20] == None) or (data[20] == ''):
            param['deleted_at'] = '1000-10-10'
        else :
            param['deleted_at'] = data[20]
        
        # 빈 데이터 처리
        param['move_grade'] = ''
        if (data[21] == None) or (data[21] == ''):
            param['move_grade'] = ''
        else :
            param['move_grade'] = data[21]

        # 빈 데이터 처리
        param['operation_grade'] = ''
        if (data[22] == None) or (data[22] == ''):
            param['operation_grade'] = ''
        else :
            param['operation_grade'] = data[22]
        
        # 빈 데이터 처리
        param['confidence_grade'] = ''
        if (data[23] == None) or (data[23] == ''):
            param['confidence_grade'] = ''
        else :
            param['confidence_grade'] = data[23]
        
        # 빈 데이터 처리
        param['report_send_at'] = ''
        if (data[24] == None) or (data[24] == ''):
            param['report_send_at'] = '1000-10-10'
        else :
            param['report_send_at'] = data[24]

        # 빈 데이터 처리
        param['name'] = ''
        if (data[1] == None) or (data[1] == ''):
            param['name'] = ''
        else :
            param['name'] = data[1]
        
        # 빈 데이터 처리
        param['class_code'] = ''
        if (data[5] == None) or (data[5] == ''):
            param['class_code'] = ''
        else :
            param['class_code'] = data[5]
        
        # 빈 데이터 처리
        param['warranty_img_path'] = ''
        if (data[6] == None) or (data[6] == ''):
            param['warranty_img_path'] = ''
        else :
            param['warranty_img_path'] = data[6]
        
        # euid 데이터 가공 
        param['device_euid'] = ''
        device_euid = ''
        if (data[7] == None) or (data[7] == ''):
            param['device_euid'] = ''
        else :
            param['device_euid'] = device_euid = data[7].lstrip()
        
        # 빈 데이터 처리
        param['serial_code'] = ''
        if (data[13] == None) or (data[13] == ''):
            param['serial_code'] = ''
        else :
            param['serial_code'] = data[13]
        
        param['idx'] = data[0]
        insertToWarranty(param)

def insertToWarranty(param):
    query = "INSERT INTO tb_warranty (company_idx, created_at, stock_fg, client_idx, model_name, expired, expired_at, started_at, deleted_at, move_grade, operation_grade, confidence_grade, report_send_at, name, class_code, warranty_img_path, device_euid, serial_code, idx) values ({}, '{}', {}, {}, '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {})"
    query = query.format(param['company_idx'], 
                        param['created_at'], 
                        param['stock_fg'], 
                        param['client_idx'], 
                        param['model_name'], 
                        param['expired'], 
                        param['expired_at'], 
                        param['started_at'], 
                        param['deleted_at'], 
                        param['move_grade'], 
                        param['operation_grade'], 
                        param['confidence_grade'], 
                        param['report_send_at'], 
                        param['name'],
                        param['class_code'], 
                        param['warranty_img_path'], 
                        param['device_euid'], 
                        param['serial_code'], 
                        param['idx'])
    insertSql(query)
    print(query)


selectTbWarranty()

