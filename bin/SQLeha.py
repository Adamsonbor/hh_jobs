import psycopg2 as pg


class Base:
    _columns = ("id", "name")


    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()


    def commit(self):
        self.conn.commit()


    def get(self, arg):
        self.cursor.execute(f"""
        SELECT {arg} FROM {self}
                            """)
        return tuple(str(item[0]) for item in self.cursor.fetchall())


    def save(self, *args):
        if len(args) != len(self._columns):
            raise AttributeError("[ELOG] too few args")
        if args[0] != None:
            self.cursor.execute(f"""
                INSERT INTO {self} ({" ,".join(self._columns)}) VALUES
                ({", ".join(['%s' for _ in range(len(self._columns))])})
                                """, tuple(args))
    

    def id_by_name(self, name):
        if name is not None:
            self.cursor.execute(f"""
                SELECT id, name FROM {self}
                WHERE name LIKE '{name}'""")
            data = self.cursor.fetchall()
            return data[0][0] if len(data) != 0 else None


    def __repr__(self):
        return self.__class__.__name__.lower()


    def __del__(self):
        self.cursor.close()
        self.conn.close()


class Id_name:
    def save(self, item_id, item_name):
        if str(item_id) not in self.get("id"):
            super().save(item_id, item_name)


class Name:
    def save(self, name):
        if name and name not in self.get("name"):
            self.cursor.execute(f"""
            INSERT INTO {self} (name) VALUES (%s)
                                """, (name,))



class Employer(Id_name, Base): pass
class Area(Id_name, Base): pass
class Profarea(Id_name, Base): pass
class Professional_role(Id_name, Base): pass
class Department(Name, Base): pass
class Employment(Name, Base): pass
class Schedule(Name, Base): pass
class Experience(Name, Base): pass

class Vacancy_skill(Base):
    _columns = ("vacancy_id", "skill_id")

class Vacancy_specialization(Base):
    _columns = ("vacancy_id", "specialization_id")

class Vacancy_professional_role(Base):
    _columns = ("vacancy_id", "professional_role_id")

class Skill(Name, Base):
    _columns = ("name",)

    def __init__(self, conn):
        super().__init__(conn)
        self.vacancy_skill = Vacancy_skill(conn)


class Specialization(Base):
    _columns = ("id", "profarea_id", "name")

    def __init__(self, conn):
        super().__init__(conn)
        self.vacancy_specialization = Vacancy_specialization(conn)


    def save(self, specialization_id, profarea_id, name):
        if specialization_id and str(specialization_id) not in self.get("id"):
            super().save(specialization_id, profarea_id, name)


class Vacancy(Base):
    _columns = ["id",
                 "name",
                 "salary_from",
                 "salary_to",
                 "type",
                 "address",
                 "contacts",
                 "description",
                 "created_at",
                 "area_id",
                 "department_id",
                 "employer_id",
                 "employment_id",
                 "schedule_id",
                 "experience_id"]



class SQLeha:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.vacancy = Vacancy(conn)
        self.skill = Skill(conn)
        self.employer = Employer(conn)
        self.employment = Employment(conn)
        self.schedule = Schedule(conn)
        self.experience = Experience(conn)
        self.department = Department(conn)
        self.area = Area(conn)
        self.profarea = Profarea(conn)
        self.professional_role = Professional_role(conn)
        self.specialization = Specialization(conn)
        self.vacancy_skill = Vacancy_skill(conn)
        self.vacancy_specialization = Vacancy_specialization(conn)
        self.vacancy_professional_role = Vacancy_professional_role(conn)


    def save(self, json):
        self.area.save(json["area_id"], json["area_name"])
        self.employer.save(json["employer_id"], json["employer_name"])
        self.department.save(json["department_name"])
        self.employment.save(json["employment"])
        self.experience.save(json["experience"])
        self.schedule.save(json["schedule"])
        self.vacancy.save(
                json["id"],
                json["name"],
                json["salary_from"],
                json["salary_to"],
                json["type"],
                json["address"],
                json["contacts"],
                json["description"],
                json["created_at"],
                json["area_id"],
                self.department.id_by_name(json["department_name"]),
                json["employer_id"],
                self.employment.id_by_name(json["employment"]),
                self.schedule.id_by_name(json["schedule"]),
                self.experience.id_by_name(json["experience"])
                )
        for skill in json["key_skills"]:
            self.skill.save(skill)
            self.vacancy_skill.save(json["id"], self.skill.id_by_name(skill))
        for item in json["specializations"]:
            self.profarea.save(item["profarea_id"], item["profarea_name"])
            self.specialization.save(item["specialization_id"], item["profarea_id"], item["specialization_name"])
            self.vacancy_specialization.save(json["id"], item["specialization_id"])
        for role in json["professional_roles"]:
            self.professional_role.save(role["professional_role_id"], role["professional_role_name"])
            self.vacancy_professional_role.save(json["id"], role["professional_role_id"])


    def commit(self):
        self.conn.commit()

    
    def __call__(self, json_list):
        idxs = self.vacancy.get("id")
        json_list = [item for item in json_list if item["id"] not in idxs]
        for item in json_list:
            self.save(item)
        print(f"{len(json_list)} saved!")


    def __del__(self):
        self.cursor.close()
        self.conn.close()
