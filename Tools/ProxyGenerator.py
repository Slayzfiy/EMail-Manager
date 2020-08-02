from proxybroker import Broker
import asyncio

from bs4 import BeautifulSoup
import requests
import json


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


class SpyScraper:
    def __init__(self):
        self.dict = ""

    def PortSetup(self, script):
        self.dict = json.loads("{}")
        for number in script[:-1].split(";"):
            if "^" not in number:
                a = number.split("=")[0]
                b = number.split("=")[1]
                self.dict[a] = b
            else:
                a = number.split("=")[0]
                b = number.split("=")[1].split("^")[0]
                c = number.split("=")[1].split("^")[1]
                self.dict[a] = int(self.dict[c]) ^ int(b)

    def GetPort(self, inputString):
        output = ""
        for part in inputString.replace("(", "").replace(")", "").split("+"):
            output = output + str(int(self.dict[part.split("^")[0]]) ^ int(self.dict[part.split("^")[1]]))
        return output

    def GetThird(self, element):
        return element[2]
    def GetFourth(self, element):
        return element[3]

    def GetProxies(self, ammount):
        response = requests.post("http://spys.one/en/free-proxy-list/", data={
            "xpp": 0,
            "xf1": "0",
            "xf2": "0",
            "xf4": "0",
            "xf5": "1"
        }, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        })
        soup = BeautifulSoup(response.text, "html.parser")
        element = soup.find("input", {"name": "xx0"})
        xx0 = element["value"]

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
            "xx0": xx0,
            "xpp": step,
            "xf1": "0",
            "xf2": "1",
            "xf4": "0",
            "xf5": "1"
        }, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
        })
        soup = BeautifulSoup(response.text, "html.parser")

        self.PortSetup(str(soup.find("script", {"type": "text/javascript"})).split(">")[1].split("<")[0])

        rows = soup.find_all("tr", {"class": "spy1x"})[1:]
        rows = rows + soup.find_all("tr", {"class": "spy1xx"})
        proxies = []
        for row in rows:
            dataFields = row.find_all("td")

            ipField = dataFields[0]
            ip = ipField.text
            port = self.GetPort(str(ipField).split('/font>"+')[1].split(")</script>")[0])

            latency = dataFields[5].text

            uptime = dataFields[8].text
            if "%" in uptime:
                uptime = int(str(uptime).split("%")[0])
            else:
                uptime = 0

            proxies.append([ip, port, latency, uptime])

        proxies.sort(key=self.GetThird, reverse=True)
        return proxies[:ammount]


class ProxyScraper:
    def __init__(self):
        pass

    def GetProxies(self, count):
        r = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=200&country=all&ssl=all&anonymity=all").text
        proxylist = []
        for x in r.splitlines():
            proxylist.append(x)
        if len(proxylist) > count:
            return proxylist[:count]
        else:
            return proxylist


class OwnProxies:
    def __init__(self):
        self.proxies = json.load(open("../Files/proxies.json", "r"))

    def GetProxies(self):
        return list(map(lambda proxy: ":".join([proxy["address"], str(proxy["port"])]), self.proxies["shared_proxy"]))
