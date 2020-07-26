import asyncio
from proxybroker import Broker


class ProxyGenerator:
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