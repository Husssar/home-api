
import cred
import pymysql
from datetime import datetime, timedelta



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
    now = datetime.now()
    time_now = (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    tomorrow = (now + timedelta(1)).strftime("%Y-%m-%d 23:59:59")

    print(time_now)
    print(tomorrow)

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry = f"SELECT when_price, totalprice FROM `grid_cost` " \
              f"where when_price > \"{time_now}\" and when_price < \"{tomorrow}\""

        cur = cnx.cursor()
        cur.execute(qry)
        cnx.commit()
        response = cur.fetchall()
        print(response)
        resp = {}
        i = 0
        for d in response:
            resp[i] = {"time": str(d[0]), "price": d[1]}
            i += 1


        return resp
    except Exception as e:
        print(e)


def get_electricity_price_now():
    qry = []
    now = datetime.now()
    time_now = now.strftime("%Y-%m-%d %H:%M:%S")
    time_then = (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry = f"SELECT when_price, totalprice FROM `grid_cost` " \
              f"where when_price >= \"{time_then}\" and when_price <= \"{time_now}\""

        cur = cnx.cursor()
        cur.execute(qry)
        cnx.commit()
        response = cur.fetchall()

        resp = {"time": str(response[0][0]), "price": response[0][1]}

        return resp
    except Exception as e:
        print(e)

def get_electricity_consuming():
    qry = []

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)

        qry.append(f'SELECT value, effiency, obis.obis_str FROM grid_data_latest')
        qry.append(f'inner join obis on obis.obis_id = grid_data_latest.obis_id')

        q = " ".join(qry)
        print(q)
        cur = cnx.cursor()
        cur.execute(q)
        cnx.commit()
        response = cur.fetchall()

        l1_effekt = ''
        l2_effekt = ''
        l3_effekt = ''
        total_effekt = ''
        l1 = 0
        l2 = 0
        l3 = 0
        total = 0
        l1_value = 0
        l2_value = 0
        l3_value = 0
        total_value = 0

        if response[0][2] == 'L1 Aktiv Effekt Uttag Momentan effekt':
            l1_value = response[0][0]
            l1_effekt = response[0][1]
            l1 = f'{response[0][0]} {response[0][1]}'

        if response[1][2] == 'L2 Aktiv Effekt Uttag Momentan effekt':
            l2_value = response[1][0]
            l2_effekt = response[1][1]
            l2 = f'{response[0][0]} {response[0][1]}'

        if response[2][2] == 'L3 Aktiv Effekt Uttag Momentan effekt':
            l3_value = response[2][0]
            l3_effekt = response[2][1]
            l3 = f'{response[2][0]} {response[2][1]}'

        if response[3][2] == 'Aktiv Effekt Uttag\tMomentan trefaseffekt':
            total_value = response[3][0]
            total_effekt = response[3][1]
            total = f'{response[3][0]} {response[3][1]}'

        _str = {
            "l1_value": l1_value,
            "l1_effekt": l1_effekt,
            "l1": l1,
            "l2_value": l2_value,
            "l2_effekt": l2_effekt,
            "l2": l2,
            "l3_value": l3_value,
            "l3_effekt": l3_effekt,
            "l3": l3,
            "total_value": total_value,
            "total_effekt": total_effekt,
            "total_out": total,
               }
        print(_str)
        return _str
    except Exception as e:
        print(e)

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

