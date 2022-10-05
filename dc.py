import discord
import os
import random
from scrapey import Search

# from scrapey import Fic
random.seed()

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Yahoo!')

    if message.content.startswith('$rec'):
        # add a message saying it might take a while

        tag = message.content
        tag = tag.strip('$rec ')
        print(tag)
        try:
            x = Search(tag)
            await message.channel.send('give me a moment <3')
            x.eat_fics()
            Fics = x.print_best()

            # PRINT RANDOM

            # fic = Fics[random.randint(0,len(Fics)-1)] # tu chyba jest problem
            # embed = discord.Embed(
            # url = fic["link"],
            # title = fic["title"]
            # )

            # embed.add_field(name="Author", value=fic["author"])
            # await message.channel.send(embed = embed)

            # PRINT ALL 10
            for i in Fics:
                # format it nicely

                embed = discord.Embed(
                    url=i["link"],
                    title=i["title"]
                )
                # embed.set_author(name) - eat author url

                embed.add_field(name="Author", value=i["author"])

                # embed.add_field(name="Summary", value=i["summary"])
                await message.channel.send(embed=embed)

        except:
            await message.channel.send('error')

        Fics *= 0


client.run(os.environ['token'])
