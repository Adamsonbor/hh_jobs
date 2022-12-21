import os
import psycopg2 as pg
from dotenv import load_dotenv
from json import dump, load


load_dotenv("../.env")
DBNAME = os.getenv("DBNAME")
DBUSER = os.getenv("DBUSER")
DBPASSWORD = os.getenv("DBPASSWORD")
DBHOST = os.getenv("DBHOST")
DBPORT = os.getenv("DBPORT")

conn = pg.connect(dbname=DBNAME,
                  user=DBUSER,
                  password=DBPASSWORD,
                  host=DBHOST,
                  port=DBPORT)


def save_json(json_data:dict, filename:str):
    with open(filename, "w") as json_file:
        dump(json_data, json_file, indent=4, ensure_ascii=False)



class Collector:
    __table_names = ("vacancy",
                    "vacancy_skill",
                    "vacancy_specialization",
                    "vacancy_professional_role",
                    "skill",
                    "employer",
                    "employment",
                    "schedule",
                    "experience",
                    "department",
                    "area",
                    "profarea",
                    "professional_role",
                    "specialization")

    def __init__(self, conn):
        self.cursor = conn.cursor()
        self.conn = conn


    @property
    def tables(self):
        return self.__table_names


    def collect_data_from_table(self, table_name:str):
        self.cursor.execute(f"""SELECT * FROM {table_name}""")
        data = self.cursor.fetchall()
        names = self.column_names(table_name)
        out = []
        for item in data:
            out.append({names[i]:item[i] if names[i] != "created_at" else item[i].timestamp() for i in range(len(names))})
        return out


    
    def column_names(self, table_name:str):
        self.cursor.execute(f"""SELECT column_name 
                                FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE table_name LIKE '{table_name}'""")
        return tuple(item[0] for item in self.cursor.fetchall())



def main():
    coll = Collector(conn)

    for table in coll.tables:
        save_json(coll.collect_data_from_table(table), f"../json/{table}.json")


if __name__ == "__name__":
    main()

# with open("../json/vacancy.json") as file:
#     data = load(file)
#     print(len(data))



