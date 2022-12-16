import asyncio
from time import sleep
from aiohttp import ClientSession
from requests import get, Session
from tqdm import tqdm


class Parser:

    def __init__(self, headers):
        super().__init__()
        self.www = "https://api.hh.ru/"
        self.vacancies = []
        self.idxs = []
        self.pages = []
        self.headers = headers
        self.timeout = 100


    # def get_json(self, www=""):
    #     data = get(self.www + www, headers=self.headers)
    #     if data.status_code == 200:
    #         return data.json()
    #     else:
    #         print(data.status_code)
    

    # def get_vacancies(self, params={}):
    #     request = "vacancies?" + "&".join([key + '=' + str(value) for key, value in params.items()])
    #     json_data = self.get_json(request)
    #     if json_data:
    #         for i in tqdm(range(json_data["pages"])):
    #             list_data = self.get_json(f"{request}&page={i}")["items"]
    #             if list_data:
    #                 self.vacancies.extend(list_data)
    #             else:
    #                 print(f"[ELOG] {i} page...")
    #     else:
    #         print("[ELOG] pages...")


    # def get_vacancy(self, idx):
    #     return self.get_json(f"vacancies/{idx}")


    # def get_idxs(self):
    #     if len(self.vacancies) > 0:
    #         return [item["id"] for item in self.vacancies]


    # def full_vacancies(self, idxs=[]):
    #     self.vacancies = []
    #     if len(idxs) > 0:
    #         for i in tqdm(idxs):
    #             json_data = self.get_vacancy(i)
    #             if json_data:
    #                 self.vacancies.append(json_data)
    #             else:
    #                 print("[ELOG] full vacancies...")
    #     else:
    #         print("[LOG] 0 vacancies")


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
            print(f"[ELOG] status log {status}")
            return False

    
    async def async_get_page_idxs(self, sess, params=[], page=0):
        request = self.url(params)
        async with sess.get(f"{request}&page={page}", timeout=self.timeout) as res:
            if self.status_200(res.status):
                json_data = await res.json()
                self.idxs.extend([str(item["id"]) for item in json_data["items"]])
                print(f"{len(self.idxs):04} / {self.pages * 20} \r", end="")


    async def async_get_vacancy(self, session, idx):
        async with session.get(f"{self.www}vacancies/{idx}", timeout=self.timeout) as res:
            if self.status_200(res.status):
                self.vacancies.append(await res.json())
                print(f"{len(self.vacancies):04} / {len(self.idxs)} \r", end="")


    async def async_full_vacancies(self, idxs=[]):
        self.vacancies = []
        self.idxs = idxs
        idxs = list(idxs)
        p = len(idxs) // 10
        async with ClientSession(headers=self.headers) as sess:
            for i in range(0, len(idxs), p):
                tasks = []
                for idx in idxs[i:i + p]:
                    tasks.append(self.async_get_vacancy(sess, idx))
                await asyncio.gather(*tasks)


    async def async_get_idxs(self, pages, params={}):
        self.idxs = []
        async with ClientSession(headers=self.headers) as sess:
            tasks = []
            for page in range(pages//2):
                tasks.append(self.async_get_page_idxs(sess, params, page))
            await asyncio.gather(*tasks)
            tasks = []
            for page in range(pages//2, page):
                tasks.append(self.async_get_page_idxs(sess, params, page))
            await asyncio.gather(*tasks)


    async def main(self, params={}):
        pages = self.get_pages(params)
        await self.async_get_idxs(pages, params)
        sleep(10)
        await self.async_full_vacancies(self.idxs)


    def get_vacancies(self, idxs):
        asyncio.run(self.async_full_vacancies(idxs))
        return self.vacancies


    def get_idxs(self, pages, params={}):
        asyncio.run(self.async_get_idxs(pages, params))
        return self.idxs

    
    def __call__(self, params):
        self.run(params)
        return self.vacancies

