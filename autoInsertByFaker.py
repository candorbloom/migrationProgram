import os
import psycopg2
from random import uniform
import random
import time

from faker import Faker
fake = Faker('ko_KR');

MIGRATION_DB = "smms"
MIGRATION_DB_HOST = "smms-v3-db.cy3ime2ikct9.ap-northeast-2.rds.amazonaws.com"
MIGRATION_DB_PORT = "5432"
MIGRATION_DB_USER = "smms"
MIGRATION_DB_PASSWORD = "cntech00##"


## postgreDB 쿼리 실행 원래 네이밍이 insertSql이라고 했어야했어..
def exeSql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MIGRATION_DB, MIGRATION_DB_USER, MIGRATION_DB_HOST, MIGRATION_DB_PORT, MIGRATION_DB_PASSWORD))
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

# # 전역변수
# profile= fake.profile()
# email= profile['mail']
# address = fake.address()
# address_1 = address.split(' ')[0]
# address_2 = address.split(' ')[1]
# address_3 = address.split(' ')[2]


###################################################
## tb_device에 들어갈 데이터
def makeTbDeviceParam():
    tbDeviceParam = {}
    tbDeviceParam['euid'] = fake.random_int(min=1000000, max=1000050)
    tbDeviceParam['type'] = fake.random_element(elements=('CN102', 'CN100'))
    tbDeviceParam['firmware'] = '9999'
    tbDeviceParam['lat_installed'] = round(uniform(127,128.3),10)
    tbDeviceParam['lng_installed'] = round(uniform(35,38),10)
    tbDeviceParam['status_code'] = 3

    return tbDeviceParam

##tb_device에 insert하는 함수
def insertTbDevice(tbDeviceParam):
    query = "INSERT INTO tb_device (euid, type, firmware, lat_installed, lng_installed, status_code, created_at, updated_at) values('{}', '{}', '{}', {}, {}, {}, now(), now());"
    query = query.format(tbDeviceParam['euid'], 
                        tbDeviceParam['type'], 
                        tbDeviceParam['firmware'],
                        tbDeviceParam['lat_installed'], 
                        tbDeviceParam['lng_installed'], 
                        tbDeviceParam['status_code'])
    exeSql(query)


###################################################
## tb_client에 들어갈 데이터
def makeTbClientParam():
    profile= fake.profile()
    email= profile['mail']
    address = fake.address()
    address_1 = address.split(' ')[0]
    address_2 = address.split(' ')[1]
    address_3 = address.split(' ')[2]
    address_4 = address_3+'지점'
    tbClientParam={}
    tbClientParam['phone'] = fake.bothify(text="###?####?####", letters="-")
    tbClientParam['email'] = email
    tbClientParam['address_1'] = address_1
    tbClientParam['address_2'] = address_2
    tbClientParam['address_3'] = address_3
    tbClientParam['is_used'] = fake.random_element(elements=('true', 'false'))
    tbClientParam['parent_idx'] = fake.random_int(min=1, max=9)
    tbClientParam['zipcode'] = fake.postcode()
    tbClientParam['name'] = address_4
    return tbClientParam

## tb_client에 insert하는 함수
def insertTbClient(tbClientParam):
    query = "INSERT INTO tb_client (idx, updated_at, created_at, phone, email, address_1, address_2, address_3, is_used, parent_idx, zipcode, name) values (-1, now(), now(), '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', '{}');"
    query = query.format(tbClientParam['phone'],
                        tbClientParam['email'],
                        tbClientParam['address_1'] ,
                        tbClientParam['address_2'] , 
                        tbClientParam['address_3'] , 
                        tbClientParam['is_used'] ,
                        tbClientParam['parent_idx'] , 
                        tbClientParam['zipcode'] ,
                        tbClientParam['name'])
    print(query)
    exeSql(query)

insertTbClient(makeTbClientParam())

###################################################
## tb_user에 들어갈 데이터
def makeTbUserParam():
    tbUserParam={}
    profile= fake.profile()
    email=profile['email']
    tbUserParam['uid'] = fake.random_int(min=1000000, max=9999999)
    tbUserParam['name'] = fake.name()
    tbUserParam['phone'] = fake.bothify(text="###?####?####", letters="-")
    tbUserParam['client_idx'] = fake.random_element(elements=('1', '2', '3'))
    tbUserParam['email'] = email
    tbUserParam['status_code'] = fake.random_element(elements=('1', '2', '3'))
    return tbUserParam

## tb_user에 insert하는 함수
def insertTbUser(tbUserParam):
    query = "INSERT INTO tb_user (uid, name, phone, client_idx, email, updated_at, created_at, status_code) values ({}, {}, {}, {}, {}, now(), now(), {});"
    query = query.format(tbUserParam['uid'],
                        tbUserParam['name'],
                        tbUserParam['phone'],
                        tbUserParam['client_idx'],
                        tbUserParam['email'],
                        tbUserParam['status_code'])
    result = exeSql(query)

###################################################
## tb_company에 들어갈 데이터
profile= fake.profile()
email= profile['mail']
def makeTbCompanyParam():
    tbCompanyParam={}
    tbCompanyParam['name'] = fake.lexify(text="???", letters="가나다라마바사아자차카타파하")
    tbCompanyParam['president'] = fake.name();
    tbCompanyParam['phone'] = fake.bothify(text="###?####?####", letters="-")
    tbCompanyParam['fax'] = fake.bothify(text="###?####?####", letters="-")
    tbCompanyParam['email'] = email
    tbCompanyParam['address_1'] = fake.address().split(' ')[0]
    tbCompanyParam['address_2'] = fake.address().split(' ')[1]
    tbCompanyParam['address_3'] = fake.address().split(' ')[2]
    tbCompanyParam['zipcode'] = fake.postcode()
    tbCompanyParam['control_number'] = fake.random_int(min=1000, max=9999)
    tbCompanyParam['client_idx'] = fake.random_element(elements=('1', '2', '3'))
    tbCompanyParam['client_manager_uid'] = fake.random_element(elements=('admin', 'manager', 'user'))
    tbCompanyParam['company_manager'] = fake.lexify(text="??????", letters="abcdefghijklmnopqrstuvwxyz")
    tbCompanyParam['channel'] = fake.random_element(elements=('카카오톡', '라인', '페이스북'))
    tbCompanyParam['status_code'] = fake.random_element(elements=('1', '2', '3'))
    tbCompanyParam['class_code'] = fake.random_element(elements=('100', '200', '300'))
    return tbCompanyParam

## tb_company에 insert하는 함수
def insertTbCompany(tbCompanyParam):
    query="INSERT INTO tb_company (updated_at, created_at, name, president, phone, fax, email, address_1, address_2, address_3, zipcode, control_number, client_idx, client_manager_uid , company_manager, channel, status_code, class_code) values (now(), now(), '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}');"
    query=query.format(tbCompanyParam['name'],
                    tbCompanyParam['president'], 
                    tbCompanyParam['phone'], 
                    tbCompanyParam['fax'], 
                    tbCompanyParam['email'], 
                    tbCompanyParam['address_1'], 
                    tbCompanyParam['address_2'], 
                    tbCompanyParam['address_3'], 
                    tbCompanyParam['zipcode'], 
                    tbCompanyParam['control_number'],
                    tbCompanyParam['client_idx'],
                    tbCompanyParam['client_manager_uid'],
                    tbCompanyParam['company_manager'],
                    tbCompanyParam['channel'],
                    tbCompanyParam['status_code'],
                    tbCompanyParam['class_code'])
    exeSql(query)


###################################################
## tb_warranty에 들어갈 데이터
def makeTbWarrantyParam():
    tbWarrantyParam = {}
    tbWarrantyParam['company_idx'] = fake.random_int(min=1, max=100)
    tbWarrantyParam['is_stock'] = fake.random_element(elements=('true', 'false'))
    tbWarrantyParam['client_idx'] = fake.random_element(elements=('11', '12', '13','14','15'))
    tbWarrantyParam['model_name'] = fake.lexify(text="?????", letters="abcdefghijklmnopqrstuvwxyz")
    tbWarrantyParam['is_expired'] = fake.random_element(elements=('true', 'false'))
    tbWarrantyParam['move_grade'] = fake.lexify(text="?", letters="ABCD")
    tbWarrantyParam['operation_grade'] = fake.lexify(text="?", letters="ABCD")
    tbWarrantyParam['confidence_grade'] = fake.lexify(text="?", letters="ABCD")
    tbWarrantyParam['name'] = fake.lexify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    tbWarrantyParam['class_code'] = fake.random_int(min=1000, max=9999)
    tbWarrantyParam['device_euid'] = fake.random_int(min=1000000, max=1000100)
    tbWarrantyParam['serial_code'] = fake.random_int(min=1000, max=9999)
    print(tbWarrantyParam)
    return tbWarrantyParam

## tb_warranty에 insert하는 함수
def insertTbWarranty(tbWarrantyParam):
    query = "INSERT INTO tb_warranty (company_idx, created_at, is_stock, client_idx, model_name, is_expired, expired_at, started_at, deleted_at, move_grade, operation_grade, confidence_grade, report_send_at, name, class_code, device_euid, serial_code) values ({}, now(), {}, {}, '{}', {}, now(), now(), now(), '{}', '{}', '{}', now(), '{}', {}, '{}', {});"
    query = query.format(
                        tbWarrantyParam['company_idx'],
                        tbWarrantyParam['is_stock'],
                        tbWarrantyParam['client_idx'],
                        tbWarrantyParam['model_name'],
                        tbWarrantyParam['is_expired'],
                        tbWarrantyParam['move_grade'],
                        tbWarrantyParam['operation_grade'],
                        tbWarrantyParam['confidence_grade'],
                        tbWarrantyParam['name'],
                        tbWarrantyParam['class_code'],
                        tbWarrantyParam['device_euid'],
                        tbWarrantyParam['serial_code'])
    exeSql(query)


###################################################
def makeLogTaskParam():
    logTaskParam={}
    logTaskParam['user_uid'] = fake.random_element(elements=('admin', 'manager','user1','user2','user3'))
    logTaskParam['task_idx'] = fake.random_int(min=1, max=100)
    logTaskParam['comment'] = fake.lexify(text="???????????????????", letters="abcdefghijklmnopqrstuvwxyz")
    return logTaskParam


def insertLogTask(logTaskParam):
    query = "INSERT INTO log_task (user_uid, created_at, task_idx , comment) values ('{}', now(), {}, '{}');"
    query = query.format(
                        logTaskParam['user_uid'], 
                        logTaskParam['task_idx'], 
                        logTaskParam['comment'])
    exeSql(query)
    print(query)


###################################################
## tb_task에 들어갈 데이터
def makeTbTaskParam():
    tbTaskParam={}
    tbTaskParam['event_id'] = fake.random_int(min=1000000, max=9999999)
    tbTaskParam['type_code_idx'] = fake.random_element(elements=('120', '125', '130', '131', '132', ''))
    tbTaskParam['progress_code_idx'] = fake.random_int(min=11, max=16)
    tbTaskParam['device_euid'] = fake.random_element(elements=('31350144', '27692769'))
    tbTaskParam['warranty_idx'] = fake.random_int(min=42, max=43)
    tbTaskParam['is_completed'] = fake.random_element(elements=('true', 'false'))

    return tbTaskParam

## tb_task에 insert하는 함수
def insertTbTask(tbTaskParam):
    query = "INSERT INTO tb_task (updated_at, created_at, event_id, type_code_idx, progress_code_idx, device_euid, warranty_idx, is_completed) values(now(), now(), {}, {}, {}, '{}', {}, {});"
    query = query.format(tbTaskParam['event_id'],
                        tbTaskParam['type_code_idx'],
                        tbTaskParam['progress_code_idx'], 
                        tbTaskParam['device_euid'], 
                        tbTaskParam['warranty_idx'], 
                        tbTaskParam['is_completed'])
    exeSql(query)
    print(query)


# ## 반복문
# init = 0
# while(init <= 20) :
#     init += 1
#     insertTbTask(makeTbTaskParam())
#     time.sleep(0.5)


## 데이터 lib
# euid = fake.random_int(min=1000000, max=9999999)
# name = fake.name();
# address = fake.address();
# ip = fake.ipv4_private();
# profile = fake.profile()
# mail = fake.profile['mail'];
# latlng = fake.latlng();
# battery = fake.random_int(min=0, max=100)
# random_uppercase_letter = fake.random_uppercase_letter()
# random_element = fake.random_element(elements=('0', '80', '3'))
# random_choices = fake.random_choices(elements=('a', 'b', 'c'), length=None)
# random.choice("QWERTYUIOPASDFGHJKLZXCVBNM") for _ in range(1)
# zipcode = fake.postcode()
# random_문자 = fake.lexify(text="????", letters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
# random_숫자 = fake.numerify(text="###")
# random_문자숫자 = fake.bothify(text="##?####", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# address = fake.address()
# address_1 = fake.address().split(' ')[0]
# address_2 = fake.address().split(' ')[1]
# address_3 = fake.address().split(' ')[2]


