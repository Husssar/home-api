
import cred
import pymysql



def get_temperature(meter_id, medium_type):
    qry = []

    try:
        cnx = pymysql.connect(user=cred.SQLUW, password=cred.USERPW, host=cred.HOST, database=cred.DATABASE)
        qry.append(f'SELECT temp.created, value from temp')
        qry.append(f'where name = (select link_id from temp_linker where name = "{meter_id}")')
        qry.append(f'and mbus= (select link_id from temp_linker where name = "{medium_type}")')
        qry.append(f'order by created desc limit 1')
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

