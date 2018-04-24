import sys
import psycopg2
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_table():
    create_table_command = (
        """
        CREATE TABLE cities (
            id TEXT PRIMARY KEY,
            name VARCHAR(200),
            ascii VARCHAR(200),
            alt_name VARCHAR(5000),
            lat FLOAT,
            long FLOAT,
            feature_class VARCHAR(1),
            feature_code VARCHAR(10),
            country_code VARCHAR(2),
            alt_country_code VARCHAR(60),
            admin_1_code VARCHAR(20),
            admin_2_code VARCHAR(20),
            admin_3_code VARCHAR(20),
            admin_4_code VARCHAR(20),
            population BIGINT,
            elevation INTEGER,
            dem INTEGER,
            timezone VARCHAR(40),
            modification_date VARCHAR(10)
        )
        """
    )

    con = None
    con = connect(database= 'coveo_cities', user='postgres', host = 'localhost', password='password')
    try:
        cur = con.cursor()
        cur.execute(create_table_command)
        cur.close()
        con.commit()
        print('Successfully created table')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        con.close()

def populate_table():
    con = None
    con = connect(database='coveo_cities', user='postgres', host = 'localhost', password='password')
    cur = con.cursor()
    counter = 0
    with open('cities_canada-usa.tsv','r', encoding='UTF-8') as tsvin:
        next(tsvin)
        print(counter)
        counter += 1
        cur.copy_from(tsvin, 'cities', sep='\t', null='')
        
    con.commit()
    cur.close()
    con.close()

create_table()
populate_table()