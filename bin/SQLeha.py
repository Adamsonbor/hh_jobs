import os
import psycopg2 as pg
from dotenv import load_dotenv

load_dotenv("../.env")
DBNAME = os.getenv("DBNAME")
DBUSER = os.getenv("DBUSER")
DBPASSWORD = os.getenv("DBPASSWORD")
DBHOST = os.getenv("DBHOST")
DBPORT = os.getenv("DBPORT")



class Base:
    _columns = ("id", "name")


    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()


    def commit(self):
        self.conn.commit()

    
    def idxs(self):
        self.cursor.execute(f"""
        SELECT id FROM {self}
                            """)
        return self.cursor.fetchall()


    def save(self, *args):
        if len(args) != len(self._columns):
            print(len(args), len(self._columns), self._columns)
            raise AttributeError("[ELOG] too few args")
        self.cursor.execute(f"""
        INSERT INTO {self} ({" ,".join(self._columns)}) VALUES
        ({", ".join(['%s' for _ in range(len(self._columns))])})
                            """, tuple(args))
    

    def __repr__(self):
        return self.__class__.__name__.lower()


    def __del__(self):
        self.cursor.close()
        self.conn.close()


class Employer(Base): pass
class Employment(Base): pass
class Schedule(Base): pass
class Experience(Base): pass
class Department(Base): pass
class Area(Base): pass
class Profarea(Base): pass
class Proffesional_role(Base): pass

class Skill(Base):
    _columns = ("name",)
    def name(self):
        print(self.__name__)

class Specialization(Base):
    _columns = ("id", "profarea_id", "name")

class Vacancy(Base):
    _columns = ["idx",
                 "name",
                 "salary_from",
                 "salary_to",
                 "opened",
                 "address",
                 "contacts",
                 "description",
                 "employer_name",
                 "created_at",
                 "area_id",
                 "department_id",
                 "employer_id",
                 "proffesional_role_id",
                 "employment_id",
                 "schedule_id",
                 "experience_id"]


conn = pg.connect(dbname=DBNAME,
                  user=DBUSER,
                  password=DBPASSWORD,
                  host=DBHOST,
                  port=DBPORT)

skill = Skill(conn)
skill.save("hard_worker")
print(skill.idxs())
