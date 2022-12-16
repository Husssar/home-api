import random

import cred
import pymysql
import json


def get_temperature(meter_id, medium_type):
    qry = []

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry.append('SELECT temp_latest.updated, temp_latest.value, unit.name  FROM temp_latest')
        qry.append('inner join temp_linker on temp_linker.link_id = temp_latest.name_id')
        qry.append('inner join temp_linker as unit on unit.link_id = temp_latest.unit')
        qry.append(f'where temp_latest.name_id = (select link_id from temp_linker where name = "{meter_id}")')
        qry.append(f'and temp_latest.unit = (select link_id from temp_linker where name = "{medium_type}")')

        q = " ".join(qry)
        print(q)
        cur = cnx.cursor()
        cur.execute(q)
        cnx.commit()
        response = cur.fetchall()

        return response[0][1]
    except Exception as e:
        print(e)


def get_electricity_price():
    qry = []

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry.append(f'SELECT temp.created, value/100000 from temp')
        qry.append(f'where name = (select link_id from temp_linker where name = "price of electricity")')
        qry.append(f'and mbus= (select link_id from temp_linker where name = "öre/kWh")')
        qry.append(f'order by created desc limit 1')
        q = " ".join(qry)
        print(q)
        cur = cnx.cursor()
        cur.execute(q)
        cnx.commit()
        response = cur.fetchall()

        return f'{round(response[0][1],2)}'
    except Exception as e:
        print(e)

def get_electricity_consuming():
    consuming = random.uniform(300.00, 5000.00)
    print(f"consuming {consuming}")
    return round(consuming, 2)

def get_electricity_added_power():
    qry = []

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry.append(f'SELECT temp.created, value/100 from temp')
        qry.append(f'where name = (select link_id from temp_linker where name = "electrical addition power")')
        qry.append(f'and mbus= (select link_id from temp_linker where name = "kW")')
        qry.append(f'order by created desc limit 1')
        q = " ".join(qry)
        print(q)
        cur = cnx.cursor()
        cur.execute(q)
        cnx.commit()
        response = cur.fetchall()

        return f'{round(response[0][1], 2)} kW'
    except Exception as e:
        print(e)

def get_radiator(in_value):
    qry = []

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry.append(f'SELECT temp.created, value, u.name from temp')
        qry.append(f'inner join temp_linker as u on u.link_id = mbus')
        qry.append(f'where temp.name = (select link_id from temp_linker where name = "{in_value}")')
        qry.append(f'order by temp.created desc limit 1')
        q = " ".join(qry)
        print(q)
        cur = cnx.cursor()
        cur.execute(q)
        cnx.commit()
        response = cur.fetchall()

        return f"{response[0][1]}"
    except Exception as e:
        print(e)

def get_citat():
    qry = []

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry.append(f'SELECT citatet from citat order by RAND() limit 1')
        q = " ".join(qry)
        print(q)
        cur = cnx.cursor()
        cur.execute(q)
        cnx.commit()
        response = cur.fetchall()
        print(response[0][0])
        return f"{response[0][0]}"
    except Exception as e:
        print(e)

