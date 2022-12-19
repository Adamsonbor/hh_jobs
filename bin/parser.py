import asyncio
from aiohttp import ClientSession
from requests import get, Session


class Parser:

    def __init__(self, headers):
        super().__init__()
        self.www = "https://api.hh.ru/"
        self.vacancies = []
        self.idxs = []
        self.pages = []
        self.headers = headers
        self.timeout = 100


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
                print(f"async_get_idxs >>> {len(self.idxs)} / {self.pages * 20} \t\t\r", end="")


    async def async_get_vacancy(self, session, idx):
        async with session.get(f"{self.www}vacancies/{idx}", timeout=self.timeout) as res:
            if self.status_200(res.status):
                self.vacancies.append(await res.json())
                print(f"async_get_vacancy >>> {len(self.vacancies)} / {len(self.idxs)} \t\t\r", end="")


    async def async_full_vacancies(self, idxs=[]):
        self.vacancies = []
        self.idxs = idxs
        idxs = list(idxs)
        step = len(idxs) // 10
        if step != 0:
            async with ClientSession(headers=self.headers) as sess:
                for i in range(0, len(idxs), step):
                    tasks = []
                    for idx in idxs[i:i + step]:
                        tasks.append(self.async_get_vacancy(sess, idx))
                    await asyncio.gather(*tasks)


    async def async_get_idxs(self, pages, params={}):
        self.idxs = []
        async with ClientSession(headers=self.headers) as sess:
            step = pages // 10
            for i in range(0, pages, step):
                tasks = []
                for page in range(i, i + step):
                    tasks.append(self.async_get_page_idxs(sess, params, page))
                await asyncio.gather(*tasks)


    def get_vacancies(self, idxs):
        asyncio.run(self.async_full_vacancies(idxs))
        return self.vacancies


    def get_idxs(self, pages, params={}):
        asyncio.run(self.async_get_idxs(pages, params))
        return self.idxs

    
    def __call__(self, idxs):
        self.run(self.async_full_vacancies(idxs))
        return self.vacancies

