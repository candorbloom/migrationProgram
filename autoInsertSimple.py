import os
from flask import jsonify
import psycopg2
from faker import Faker
fake = Faker('ko_KR');

# db와 연결
MAIN_DB = "postgres";
MAIN_DB_USER = "cntech";
MAIN_DB_HOST = "smms-v4-db-instance.cy3ime2ikct9.ap-northeast-2.rds.amazonaws.com";
MAIN_DB_PORT = "5432";
MAIN_DB_PASSWORD = "cntechdb!23";
conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MAIN_DB, MAIN_DB_USER, MAIN_DB_HOST, MAIN_DB_PORT, MAIN_DB_PASSWORD));
cur = conn.cursor();

cur.execute("INSERT INTO public.tb_device (created_at, is_power_on, is_detached, battery, operation_ratio, lux, lbs_lat, lbs_lng, lng_installed, lat_installed, euid, acc_threshold, mag_threshold, transmit_period, firmware_ver, sensing_period, serial_code, update_active, model_type, status_code, is_excluded) values(now(), true, true, 90, 50, 10, '35.928245544433594', '128.9438018798828', '35.928245544433594', '128.9438018798828', '20B4330', 10, 13, 60, '1.0', 60, 1234, true, 1234, 100, false);");
conn.commit();
conn.close();