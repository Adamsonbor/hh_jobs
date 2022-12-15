import os
import art
import psycopg2 as pg
from dotenv import load_dotenv

def get_connect():
    load_dotenv("../.env")
    DBNAME = os.getenv("DBNAME")
    DBUSER = os.getenv("DBUSER")
    DBPASSWORD = os.getenv("DBPASSWORD")
    DBHOST = os.getenv("DBHOST")
    DBPORT = os.getenv("DBPORT")
    conn = pg.connect(dbname=DBNAME, user=DBUSER, password=DBPASSWORD, host=DBHOST, port=DBPORT)
    cursor = conn.cursor()
    return conn, cursor

def create_tables(conn, cursor):
    """
    create all tables for database
    """

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employment (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experience (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employer (
        id BIGINT NOT NULL PRIMARY KEY,
        name TEXT NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS department (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS area (
        id BIGINT NOT NULL PRIMARY KEY,
        name TEXT NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skill (
        id SERIAL PRIMARY KEY,
        name text NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profarea (
        id BIGINT NOT NULL PRIMARY KEY,
        name text NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS specialization (
        id BIGINT NOT NULL PRIMARY KEY,
        profarea_id BIGINT NOT NULL REFERENCES profarea (id) ON UPDATE CASCADE,
        name text NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_role (
        id BIGINT NOT NULL PRIMARY KEY,
        name text NOT NULL
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy (
        id BIGINT UNIQUE NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        salary_from INT,
        salary_to INT,
        type VARCHAR(50),
        address TEXT,
        contacts TEXT,
        description TEXT,
        created_at TIMESTAMP,
        area_id BIGINT REFERENCES area (id) ON UPDATE CASCADE,
        department_id BIGINT REFERENCES department (id) ON UPDATE CASCADE,
        employer_id BIGINT REFERENCES employer (id) ON UPDATE CASCADE,
        employment_id BIGINT REFERENCES employment (id) ON UPDATE CASCADE,
        schedule_id BIGINT REFERENCES schedule (id) ON UPDATE CASCADE,
        experience_id BIGINT REFERENCES experience (id) ON UPDATE CASCADE
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy_specialization (
        vacancy_id BIGINT REFERENCES vacancy (id) ON UPDATE CASCADE ON DELETE CASCADE, 
        specialization_id BIGINT REFERENCES specialization (id) ON UPDATE CASCADE
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy_skill (
        vacancy_id BIGINT REFERENCES vacancy (id) ON UPDATE CASCADE ON DELETE CASCADE, 
        skill_id BIGINT REFERENCES skill (id) ON UPDATE CASCADE
        )
                   """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacancy_professional_role (
        vacancy_id BIGINT REFERENCES vacancy (id) ON UPDATE CASCADE ON DELETE CASCADE, 
        professional_role_id BIGINT REFERENCES professional_role (id) ON UPDATE CASCADE
        )
                   """)

    conn.commit()

def main():
    try:
        conn, cursor = get_connect()
        create_tables(conn, cursor)
        Art = art.text2art('''HH_DATABASE_CREATED''')
        print(Art)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

