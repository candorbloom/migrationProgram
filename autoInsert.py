import os
from flask import jsonify
import psycopg2
import requests
import json
import time

from faker import Faker
fake = Faker('ko_KR');

MAIN_DB = "postgres"
MAIN_DB_USER = "cntech"
MAIN_DB_HOST = "smms-v4-db-instance.cy3ime2ikct9.ap-northeast-2.rds.amazonaws.com"
MAIN_DB_PORT = "5432"
MAIN_DB_PASSWORD = "cntechdb!23"

# postgredb에 쿼리날리기
def sql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MAIN_DB, MAIN_DB_USER, MAIN_DB_HOST, MAIN_DB_PORT, MAIN_DB_PASSWORD))
        cur = conn.cursor()
        
        cur.execute(query)
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


# # tb_device에 데이터 insert하는 함수
# def insertDeviceTable(euid):
#     query = "INSERT INTO public.tb_device (euid, created_at, is_power_on, is_detached, battery, operation_ratio, lux, lbs_lat, lbs_lng, lng_installed, lat_installed, acc_threshold, mag_threshold, transmit_period, firmware_ver, sensing_period, serial_code, update_active, model_type, status_code, is_excluded) values('20B4334', now(), true, true, 90, 50, 10, '35.928245544433594', '128.9438018798828', '35.928245544433594', '128.9438018798828', 10, 13, 60, '1.0', 60, 1234, true, 1234, 100, false);"
#     query = query.format(euid);
#     result = sql(query);
#     print(query);

# insertDeviceTable()


