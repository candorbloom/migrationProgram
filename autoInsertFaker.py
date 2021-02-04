import os
from flask import jsonify
import psycopg2
import requests
import json
import time
from random import uniform
import random

from faker import Faker
fake = Faker('ko_KR');

MAIN_DB = "smms"
MAIN_DB_USER = "smms"
MAIN_DB_HOST = "52.79.111.170"
MAIN_DB_PORT = "5432"
MAIN_DB_PASSWORD = "smms##201216##cntech"

## postgreDB 쿼리 실행
def exeSql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MAIN_DB, MAIN_DB_USER, MAIN_DB_HOST, MAIN_DB_PORT, MAIN_DB_PASSWORD))
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

## tb_device에 들어갈 데이터
def makeTbDeviceParam():
    tbDeviceParam = {}
    tbDeviceParam['euid'] = fake.random_int(min=1000000, max=9999999)
    tbDeviceParam['is_power_on'] = fake.random_element(elements=('true', 'false'))
    tbDeviceParam['is_detached'] = fake.random_element(elements=('true', 'false'))
    tbDeviceParam['battery'] = fake.random_int(min=0, max=100)
    tbDeviceParam['operation_ratio'] = fake.random_int(min=0, max=100)
    tbDeviceParam['lux'] = fake.random_int(min=0, max=100)
    tbDeviceParam['lbs_lat'] = round(uniform(35,38),10)
    tbDeviceParam['lbs_lng'] = round(uniform(127,128.3),10)
    tbDeviceParam['lng_installed'] = round(uniform(35,38),10)
    tbDeviceParam['lat_installed'] = round(uniform(127,128.3),10)
    tbDeviceParam['acc_threshold'] = fake.random_int(min=0, max=100)
    tbDeviceParam['mag_threshold'] = fake.random_int(min=10, max=100)
    tbDeviceParam['transmit_period'] = 60
    tbDeviceParam['firmware_ver'] = '1.0'
    tbDeviceParam['sensing_period'] = 60
    tbDeviceParam['serial_code'] = str(random.choice(range(1000000000,9999999999)))
    tbDeviceParam['update_active'] = fake.random_element(elements=('true', 'false'))
    tbDeviceParam['model_type'] = 1
    tbDeviceParam['status_code'] = 1
    tbDeviceParam['is_excluded'] = fake.random_element(elements=('true', 'false'))

    return tbDeviceParam

##tb_device에 insert하는 함수
def insertTbDevice(tbDeviceParam):
    query = "INSERT INTO tb_device (euid, created_at, is_power_on, is_detached, battery, operation_ratio, lux, lbs_lat, lbs_lng, lng_installed, lat_installed, acc_threshold, mag_threshold, transmit_period, firmware_ver, sensing_period, serial_code, update_active, model_type, status_code, is_excluded) values({}, now(), {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});"
    query = query.format(tbDeviceParam['euid'], 
                        tbDeviceParam['is_power_on'], 
                        tbDeviceParam['is_detached'],
                        tbDeviceParam['battery'], 
                        tbDeviceParam['operation_ratio'], 
                        tbDeviceParam['lux'], 
                        tbDeviceParam['lbs_lat'], 
                        tbDeviceParam['lbs_lng'], 
                        tbDeviceParam['lng_installed'], 
                        tbDeviceParam['lat_installed'], 
                        tbDeviceParam['acc_threshold'], 
                        tbDeviceParam['mag_threshold'], 
                        tbDeviceParam['transmit_period'], 
                        tbDeviceParam['firmware_ver'], 
                        tbDeviceParam['sensing_period'], 
                        tbDeviceParam['serial_code'], 
                        tbDeviceParam['update_active'], 
                        tbDeviceParam['model_type'], 
                        tbDeviceParam['status_code'], 
                        tbDeviceParam['is_excluded'])
    exeSql(query)


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
    query = "INSERT INTO tb_client (updated_at, created_at, phone, email, address_1, address_2, address_3, is_used, parent_idx, zipcode, name) values (now(), now(), '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', '{}');"
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


## tb_warranty에 들어갈 데이터
def makeTbWarrantyParam():
    tbWarrantyParam = {}
    tbWarrantyParam['company_idx'] = fake.random_int(min=1, max=101)
    tbWarrantyParam['is_stock'] = fake.random_element(elements=('true', 'false'))
    tbWarrantyParam['client_idx'] = fake.random_element(elements=('11', '12', '13','14','15'))
    tbWarrantyParam['model_name'] = fake.lexify(text="?????", letters="abcdefghijklmnopqrstuvwxyz")
    tbWarrantyParam['is_expired'] = fake.random_element(elements=('true', 'false'))
    tbWarrantyParam['move_grade'] = fake.lexify(text="?", letters="ABCD")
    tbWarrantyParam['operation_grade'] = fake.lexify(text="?", letters="ABCD")
    tbWarrantyParam['confidence_grade'] = fake.lexify(text="?", letters="ABCD")
    tbWarrantyParam['name'] = fake.lexify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    tbWarrantyParam['class_code'] = fake.random_int(min=1000, max=9999)
    tbWarrantyParam['device_euid'] = fake.random_int(min=1000000, max=9999999)
    tbWarrantyParam['serial_code'] = fake.random_int(min=1000, max=9999)
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

##########################################
def makeLogTaskParam():
    address = fake.address()
    address_3 = address.split(' ')[2]
    address_3 = address_3+'지점'
    logTaskParam={}
    logTaskParam['task_idx'] = fake.random_int(min=1, max=100)
    logTaskParam['comment'] = fake.lexify(text="???????????????????", letters="abcdefghijklmnopqrstuvwxyz")
    logTaskParam['event_code'] = fake.random_int(min=100, max=999)
    logTaskParam['event_type'] = fake.random_int(min=100, max=999)
    logTaskParam['manager'] = fake.name();
    logTaskParam['client_root'] = fake.random_element(elements=('기업은행', '하나은행', '카카오뱅크','국민은행'))
    logTaskParam['client_branch'] = address_3
    logTaskParam['company'] = fake.lexify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    logTaskParam['status_code'] = fake.lexify(text="?????", letters="abcdefghijklmnopqrstuvwxyz")
    logTaskParam['running_time'] = fake.random_element(elements=('26시간25분', '55시간27분', '56시간19분'))
    return logTaskParam


def insertLogTask(logTaskParam):
    query = "INSERT INTO log_task (task_idx, created_at, comment , event_code, manager, client_root, client_branch, company, status_code, running_time) values ({}, now(), '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}');"
    query = query.format(
                        logTaskParam['task_idx'], 
                        logTaskParam['comment'], 
                        logTaskParam['event_code'], 
                        logTaskParam['manager'], 
                        logTaskParam['client_root'], 
                        logTaskParam['client_branch'], 
                        logTaskParam['company'], 
                        logTaskParam['status_code'], 
                        logTaskParam['running_time'])
    exeSql(query)
    print(query)



## log_task에 들어갈 데이터

def makeTbTaskParam():
    tbTaskParam={}
    tbTaskParam['type_code'] = fake.random_int(min=100, max=999)
    tbTaskParam['progress_code'] = fake.random_int(min=1, max=10)
    tbTaskParam['user_uid'] = fake.random_element(elements=('admin', 'manager', 'user'))
    tbTaskParam['log_device_idx'] = fake.random_int(min=1, max=100)
    tbTaskParam['company_idx'] = fake.random_int(min=1, max=100)
    tbTaskParam['warranty_idx'] = fake.random_int(min=1, max=100)
    tbTaskParam['device_idx'] = fake.random_int(min=1, max=100)
    tbTaskParam['code_idx'] = fake.random_int(min=1, max=6)

    return tbTaskParam

## log_task에 insert하는 함수
def insertTbTask(tbTaskParam):
    query = "INSERT INTO tb_task (updated_at, created_at, type_code, progress_code, user_uid, log_device_idx, company_idx, warranty_idx, device_idx, code_idx) values(now(), now(), {}, {}, '{}', {}, {}, {}, {}, {});"
    query = query.format(tbTaskParam['type_code'],
                        tbTaskParam['progress_code'],
                        tbTaskParam['user_uid'], 
                        tbTaskParam['log_device_idx'], 
                        tbTaskParam['company_idx'], 
                        tbTaskParam['warranty_idx'], 
                        tbTaskParam['device_idx'], 
                        tbTaskParam['code_idx'])
    exeSql(query)

# init = 0
# while(init <= 100) :
#     init += 1
#     insertTbTask(makeTbTaskParam())
#     time.sleep(0.5)


# ## 반복문


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


