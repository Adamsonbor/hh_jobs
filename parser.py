import asyncio
from aiohttp import ClientSession
from requests import get, Session
from tqdm import tqdm


class Parser:

    def __init__(self):
        super().__init__()
        self.www = "https://api.hh.ru/"
        self.vacancies = []
        self.idxs = []
        self.pages = []
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
            }


    def get_json(self, www=""):
        data = self.get(self.www + www)
        if data.status_code == 200:
            return data.json()
    

    def get_vacancies(self, params={}):
        request = "vacancies?" + "&".join([key + '=' + str(value) for key, value in params.items()])
        json_data = self.get_json(request)
        if json_data:
            for i in tqdm(range(json_data["pages"])):
                list_data = self.get_json(f"{request}&page={i}")["items"]
                if list_data:
                    self.vacancies.extend(list_data)
                else:
                    print(f"[ELOG] {i} page...")
        else:
            print("[ELOG] pages...")


    def get_vacancy(self, idx):
        return self.get_json(f"vacancies/{idx}")


    def get_idxs(self):
        if len(self.vacancies) > 0:
            return [item["id"] for item in self.vacancies]


    def full_vacancies(self, idxs=[]):
        self.vacancies = []
        if len(idxs) > 0:
            for i in tqdm(idxs):
                json_data = self.get_vacancy(i)
                if json_data:
                    self.vacancies.append(json_data)
                else:
                    print("[ELOG] full vacancies...")
        else:
            print("[LOG] 0 vacancies")


    def get_pages(self, params={}):
        request = self.url(params)
        res = get(request, headers=self.headers)
        if res.status_code == 200:
            self.pages = res.json()["pages"]
            return self.pages
        else:
            print(f"[ELOG] status log {res.status_code}")


    def url(self, params):
        return f"{self.www}vacancies?{'&'.join([key + '=' + str(value) for key, value in params.items()])}"


    def status_200(self, status):
        if status == 200:
            return True
        else:
            print(f"[ELOG] status log {res.status}")
            return False

    
    async def async_get_page_idxs(self, sess, params=[], page=0):
        request = self.url(params)
        async with sess.get(f"{request}&page={page}") as res:
            if self.status_200(res.status):
                json_data = await res.json()
                self.idxs.extend([item["id"] for item in json_data["items"]])
                print(f"{len(self.idxs):04} / {self.pages} \r", end="")


    async def async_get_vacancy(self, session, idx):
        async with session.get(f"{self.www}vacancies/{idx}") as res:
            if self.status_200(res.status):
                self.vacancies.append(await res.json())
                print(f"{len(self.vacancies):04} / {self.pages} \r", end="")


    async def async_full_vacancies(self, sess, idxs=[]):
        tasks = []
        for idx in idxs:
            tasks.append(self.async_get_vacancy(sess, idx))
        await asyncio.gather(*tasks)


    async def get_idxs(self, pages=[], params={}):
        tasks = []
        async with ClientSession(headers=self.headers) as sess:
            for page in range(pages):
                tasks.append(self.async_get_page_idxs(sess, params, page))
            await asyncio.gather(*tasks)


    async def main(self, params={}):
        pages = self.get_pages(params)
        async with ClientSession(headers=self.headers) as sess:
            await self.get_idxs(pages, params)
            await self.async_full_vacancies(sess, self.idxs)


    def run(self, params):
        asyncio.run(self.main(params))

    
    def __call__(self, params):
        self.run(params)
        return self.vacancies

