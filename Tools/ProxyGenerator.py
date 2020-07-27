import asyncio
from proxybroker import Broker


class ProxyBroker:
    def __init__(self):
        self.proxies = []

    @staticmethod
    def GetSpeed(proxy):
        return str(proxy).split(" ")[2]

    async def TestProxies(self, proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            self.proxies.append(proxy)

    def GetProxies(self, ammount):
        self.proxies = []
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(
            broker.find(types=['HTTPS'], limit=ammount),
            self.TestProxies(proxies)
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)

        self.proxies.sort(key=self.GetSpeed)
        return list(map(lambda proxy: ":".join([proxy.host, str(proxy.port)]), self.proxies))


import requests


class SpyScraper:
    def __init__(self):
        pass

    def GetProxies(self, ammount):
        if ammount > 300:
            step = "5"
        elif ammount > 200:
            step = "4"
        elif ammount > 100:
            step = "3"
        elif ammount > 50:
            step = "2"
        elif ammount > 30:
            step = "1"
        else:
            step = "0"
        response = requests.post("http://spys.one/en/free-proxy-list/", data={
            "xx0": "92b8b4b43dd7133df3cf54d9a403fa05",
            "xpp": step,
            "xf1": "0",
            "xf2": "0",
            "xf4": "0",
            "xf5": "1"
        })
        print(response)
