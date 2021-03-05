
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


## targetDB에서 tb_bank 데이터 가져오기 
def selectTbBank():
    query = "select bank_srl, bank_nm, manager, phone, email, addr, addr_detail, zipcode, created_at, ci_image_path, admin_id from tb_bank order by bank_srl"
    result = selectSql(query)
    parsingTbBank(result)

## targetDB에서 tb_branch 데이터 가져오기
def selectTbBranch():
    query = "select branch_srl, bank_srl, branch_nm, manager, phone, email, addr, addr_detail, zipcode, created_at, admin_id from tb_branch order by branch_srl;"
    result = selectSql(query)
    parsingTbBranch(result)


## targetDB에서 가져온 tb_bank 데이터 파싱하기
def parsingTbBank(result) :
    param = {}
    for data in result:
        param['idx'] = data[0]
        param['name'] = data[1]
        param['manager_name'] = data[2]
        param['phone'] = data[3]
        param['email'] = data[4]
        
        #빈주소처리
        param['address_1'] = ''
        param['address_2'] = ''
        param['address_3'] = ''
        if (data[5] == None) or (data[5] == ''):
            print('pass')
        else : 
            address_0 = data[5].split(' ')
            param['address_1'] = address_0[0]
            param['address_2'] = address_0[1]
            address3=''
            for address in data[5].split(' ')[2:] :
                address3 += address if address == None else (address+" ")
                param['address_3'] = address3 + " " + data[6]
        param['zipcode'] = data[7]
        
        # 빈 데이터 처리
        param['created_at'] = ''
        if (data[8] == None) or (data[8] == ''):
            param['created_at'] = '1000-10-10'
        else :
            param['created_at'] = data[8]

        param['ci_image_path'] = data[9]       
        param['manager_uid'] = data[10]
        insertBankToClient(param)     

def insertBankToClient(param):
    query = "INSERT INTO new_client (idx, name, manager_name, phone, email, address_1, address_2, address_3, zipcode, created_at, ci_image_path, manager_uid) values ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
    query = query.format(param['idx'],
                        param['name'],
                        param['manager_name'],
                        param['phone'],
                        param['email'],
                        param['address_1'],
                        param['address_2'],   
                        param['address_3'],
                        param['zipcode'],
                        param['created_at'],
                        param['ci_image_path'],
                        param['manager_uid'])
    # insertSql(query)
    print(query)


################################################################################
def parsingTbBranch(result):
    param = {}
    for data in result:

        param['idx'] = data[0]
        param['parent_idx'] = data[1]
        param['name'] = data[2]
        param['manager_name'] = data[3]
        param['phone'] = data[4]
        param['email'] = data[5]
    
        #빈주소처리
        param['address_1'] = ''
        param['address_2'] = ''
        param['address_3'] = ''
        if (data[6] == None) or (data[6] == ''):
            print('pass_address')
        else:
            address3 = ""
            address_0 = data[6].split(" ")
            param['address_1'] = address_0[0]
            param['address_2'] = address_0[1]
            for address in data[6].split(" ")[2:] :
                address3 += (address + " ")
            param['address_3'] = address3 if data[7] == None else address3 + str(data[7])

        param['zipcode'] = data[8]

        # 빈 데이터 처리
        param['created_at'] = ''
        if (data[9] == None) or (data[9] == ''):
            param['created_at'] = '1000-10-10'
        else :
            param['created_at'] = data[9]
        
        param['manager_uid'] = data[10]
        insertBranchToClient(param)

def insertBranchToClient(param):
    query = "INSERT INTO new_client (idx, parent_idx, name, manager_name, phone, email, address_1, address_2, address_3, zipcode, created_at, manager_uid) values ({}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    query = query.format(param['idx'],
                        param['parent_idx'],
                        param['name'],
                        param['manager_name'],
                        param['phone'],
                        param['email'],
                        param['address_1'],
                        param['address_2'],
                        param['address_3'],
                        param['zipcode'],
                        param['created_at'],
                        param['manager_uid'])
    insertSql(query)
    print(query)



selectTbBranch()

# selectTbBank()

