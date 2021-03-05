
import os
import psycopg2
import time

# TARGET_DB = "smms_iot"
# TARGET_DB_HOST = "15.165.80.49"
# TARGET_DB_PORT = "5432"
# TARGET_DB_USER = "smms_main"
# TARGET_DB_PASSWORD = "!!##Cntech#@201217!smms"

TARGET_DB = "smms"
TARGET_DB_HOST = "smms-v3-db.cy3ime2ikct9.ap-northeast-2.rds.amazonaws.com"
TARGET_DB_PORT = "5432"
TARGET_DB_USER = "smms"
TARGET_DB_PASSWORD = "cntech00##"
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


## targetDB에서 tb_company 데이터 가져오기 
def selectTbCompany():
    query = "select * from mg_company order by company_srl"
    result = selectSql(query)
    parsingTbCompany(result)


def parsingTbCompany(result):
    param = {}
    for data in result :
        param['idx'] = data[0]

        # 빈 데이터 처리
        param['created_at'] = ''
        if (data[11] == None) or (data[11] == ''):
            param['created_at'] = '1000-10-10'
        else :
            param['created_at'] = data[11]

        param['name'] = data[1]
        
        # 빈 데이터 처리
        param['president_name'] = ''
        if (data[2] == None) or (data[2] == ''):
            param['president_name'] =''
        else :
            param['president_name'] = data[2]
        
        # 빈 데이터 처리
        param['company_phone'] = ''
        if (data[5] == None) or (data[5] == ''):
            param['company_phone'] = ''
        else :
            param['company_phone'] = data[5]

        # 빈 데이터 처리
        param['company_fax'] = ''
        if (data[7] == None) or (data[7] == ''):
            param['company_fax'] = ''
        else :
            param['company_fax'] = data[7]
        
        # 빈 데이터 처리
        param['company_email'] = ''
        if (data[6] == None) or (data[6] == ''):
            param['company_email'] = ''
        else :
            param['company_email'] = data[6]
        
        param['address_1'] = ''
        param['address_2'] = ''
        param['address_3'] = ''
        if (data[9] == None) or (data[9] == ''):
            print('pass_address')
        else:
            address3 = ""
            address_0 = data[9].split(" ")
            param['address_1'] = address_0[0]
            param['address_2'] = address_0[1]
            for address in data[9].split(" ")[2:] :
                address3 += (address + " ")
            param['address_3'] = address3 if data[10] == None else address3 + str(data[10])
        

        # 빈 데이터 처리
        param['client_idx'] = ''
        if (data[4] == None) or (data[4] == ''):
            param['client_idx'] = -1
        else :
            param['client_idx'] = data[4]

        # 빈 데이터 처리
        param['company_manager_name'] = ''
        if (data[15] == None) or (data[15] == ''):
            param['company_manager_name'] = ''
        else :
            param['company_manager_name'] = data[15]
        
        # 빈 데이터 처리
        param['company_manager_phone'] = ''
        if (data[16] == None) or (data[16] == ''):
            param['company_manager_phone'] = ''
        else :
            param['company_manager_phone'] = data[16]

        # 빈 데이터 처리
        param['zipcode'] = ''
        if (data[8] == None) or (data[8] == ''):
            param['zipcode'] = ''
        else :
            param['zipcode'] = data[8]

        # 빈 데이터 처리
        param['memo'] = ''
        if (data[22] == None) or (data[22] == ''):
            param['memo'] = ''
        else :
            param['memo'] = data[22]
        
        insertToCompany(param)


def insertToCompany(param):
    query = "INSERT INTO new_company (idx, created_at, name, president_name, company_phone, company_fax, company_email, address_1, address_2, address_3, client_idx, company_manager_name, company_manager_phone, memo, zipcode) values ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}')"
    query = query.format(param['idx'],
                        param['created_at'],
                        param['name'],
                        param['president_name'],
                        param['company_phone'],
                        param['company_fax'],
                        param['company_email'],
                        param['address_1'],
                        param['address_2'],
                        param['address_3'],
                        param['client_idx'],
                        param['company_manager_name'],
                        param['company_manager_phone'],
                        param['memo'],
                        param['zipcode'])
    insertSql(query)
    print(query)



selectTbCompany()
