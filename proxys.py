import requests


class GetProxy:
    def __init__(self):
        pass

    def Fetch_Proxys(self):
        r = requests.get(
            "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=200&country=all&ssl=all&anonymity=all").text
        proxylist = []
        for x in r.splitlines():
            proxylist.append(x)
        print(proxylist)


if __name__ == "__main__":
    i = GetProxy()
    i.Fetch_Proxys()
    input()
