import asyncio
import os
import psycopg2 as pg
from dotenv import load_dotenv
from aiohttp import ClientSession
from datetime import datetime, timedelta
from json import dump, load
from parser import Parser
from processor import Processor
from SQLeha import SQLeha

load_dotenv("../.env")
DBNAME = os.getenv("DBNAME")
DBUSER = os.getenv("DBUSER")
DBPASSWORD = os.getenv("DBPASSWORD")
DBHOST = os.getenv("DBHOST")
DBPORT = os.getenv("DBPORT")

headers = {
    "User-Agent":"Mozilla/5.0"
    }

conn = pg.connect(dbname=DBNAME,
                  user=DBUSER,
                  password=DBPASSWORD,
                  host=DBHOST,
                  port=DBPORT)


def save_json(json_data, filename):
    with open(filename, "w") as json_file:
        dump(json_data, json_file, indent=4, ensure_ascii=False)


def main():

    date_from = datetime.now().date() - timedelta(days=1)
    params = {"industry":7, "date_from":str(date_from)}

    parser = Parser(headers)
    processor = Processor()
    db = SQLeha(conn)
    pages = parser.get_pages(params)
    idxs = parser.get_idxs(pages, params)
    old_idxs = db.vacancy.get("id")
    idxs = idxs - set(str(item) for item in old_idxs)
    vacancies = parser.vacancies(idxs)
    db(vacancies)
    db.commit()


    


if __name__ == "__main__":
    main()
