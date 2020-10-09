from Giveaways.GiveawayManager import GivawayManager

import requests
import discord


class DiscordBot:
    def __init__(self):
        self.token = 'NzM5NTY5MDEwMjI3NTQ0MTU1.XycXUA.jgCnQERZ9_7o0drJmrlKHqEBiGw'
        self.giveawayManager = GivawayManager()
        self.giveawayChannel = "giveaways"

    def Start(self):
        client = discord.Client()
        @client.event
        async def on_message(message):
            if message.content.startswith('!register'):
                channel = message.channel
                if str(channel) == self.giveawayChannel:
                    text = str(message.content)
                    if len(text.split(" ")) < 3:
                        await channel.send("Usage: '!register URL DrawDate'")
                    else:
                        url = text.split(" ")[1]
                        try:
                            response = requests.get(url)
                        except:
                            response = None
                        if response is None or "The page you were looking for doesn't exist." in response.text:
                            await channel.send("Giveaway not found.")
                        else:
                            product = url.split("/gewinnspiel-")[1].replace("-", " ")
                            drawDate = " ".join([text.split(" ")[2], text.split(" ")[3]])
                            if drawDate.count("-") != 2 or drawDate.count(":") != 2:
                                await channel.send("Format for DrawDate is 'YY-MM-DD hh:mm:ss'. \nExample: '2020-08-05 22:13:14'")
                            else:
                                self.giveawayManager.RegisterGiveaway(product, url, drawDate)
                                await channel.send("Giveaway saved.")
        @client.event
        async def on_ready():
            print('Logged in as')
            print(client.user.name)
            print(client.user.id)
            print('------')

        client.run(self.token)


if __name__ == "__main__":
    bot = DiscordBot()
    bot.Start()