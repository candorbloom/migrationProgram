import os
from flask import jsonify
import psycopg2
import requests
import json
import time

MAIN_DB = "postgres"
MAIN_DB_USER = "cntech"
MAIN_DB_HOST = "smms-v4-db-instance.cy3ime2ikct9.ap-northeast-2.rds.amazonaws.com"
MAIN_DB_PORT = "5432"
MAIN_DB_PASSWORD = "cntech!23"

def sql_select(query):
    ret = []
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MAIN_DB, MAIN_DB_USER, MAIN_DB_HOST, MAIN_DB_PORT, MAIN_DB_PASSWORD))
        cur = conn.cursor()
        
        cur.execute(query)
        rows = cur.fetchall()
        
        for row in rows:
            tmp = dict()
            for i in range(len(row)):
                tmp[cur.description[i].name] = row[i]
            ret.append(tmp)
        
        conn.close()
    except Exception as e:
        print(e)
    
    return ret

def sql(query):
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port={} password='{}'".format(MAIN_DB, MAIN_DB_USER, MAIN_DB_HOST, MAIN_DB_PORT, MAIN_DB_PASSWORD))
        cur = conn.cursor()
        
        cur.execute(query)
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)




def insertGnssPacket(idx, euid):
    query = "INSERT INTO public.tb_gnss_packet (idx, euid, time_at, lat, lon, temp, als, firmware_ver, batt_voltage, location_category, address_city, address_load) values('{}', '{}', '2020-12-23 09:00:00+0900', '35.9291074', '128.9447484', '10', '0', '1', '100', 'GPS', '경북 영천시', '봉동 646');"
    query = query.format(idx, euid)
    result = sql(query)
    print(query)



start()

