from datetime import datetime, timedelta
from json import dump, load
from parser import Parser
from processor import Processor

def save_json(json_data, filename):
    with open(filename, "w") as json_file:
        dump(json_data, json_file, indent=4, ensure_ascii=False)


def main():
    date_from = datetime.now().date() - timedelta(days=1)
    params = {"industry":7, "date_from":str(date_from)}

    parser = Parser()
    processor = Processor()
    print(parser.url(params))
    # vacancies = parser(params)
    # vacancies = processor(vacancies)
    # save_json(vacancies, "new_vacancies.json")


if __name__ == "__main__":
    main()
