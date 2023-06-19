import discord
from discord.ext import commands, tasks
import asyncio
import datetime


from settings import TOKEN
from discord.ext import commands

from data import get_job_listings
from filter import get_relevant_listings
from alert import write_to_csv, process_csv_and_get_jobs


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("The secret TOKEN is correct!")
    print(f"We have logged in as {client.user}")
    job_check.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
       instructions = """
       Hello! Here are the commands you can use:
          
       `$findjob [your interest] [job level]`: The bot fetches job listings based on your interest and job level. Example: `$findjob programming executive`.
       `$alert [your interest]`: The bot sets the interest that will be queried for your notification of new job listings. Example: `$alert programming`.
          
       Remember to replace the brackets and the words within them with your own input!
       """
       await message.reply(instructions, mention_author=True)


    if message.content.startswith("$findjob "):
        content = message.content.split()
        if len(content) == 3:
            interest = content[1]
            job_level = content[2]
            get_listings = get_job_listings()
            listings = get_relevant_listings(get_listings, interest, job_level)

            await message.reply(
                f"Here are your job listings for interest '{interest}' and job level '{job_level}'",
                mention_author=True,
            )

            for listing in listings:
                await message.channel.send("Position: " + listing["position"])
                await message.channel.send(
                    "Link: " + "https://jobs.sunway.com.my/#" + str(listing["id"])
                )
        else:
            await message.reply(
                "Please provide an interest and a job level.", mention_author=True
            )

    if message.content.startswith("$alert "):
        content = message.content.split()
        if len(content) == 3:
            interest = content[1]
            duration = content[2]
            current_time = datetime.datetime.now()

            write_to_csv(
                [
                    interest,
                ],
                current_time,
                duration,
            )
            await message.reply(
                f"Alert for job listings for interest '{interest}' is set.'",
                mention_author=True,
            )
        else:
            await message.reply(
                "Please provide an interest and a job level.", mention_author=True
            )


@tasks.loop(seconds=60)
async def job_check():
    process_csv_and_get_jobs()


@job_check.before_loop
async def before():
    await client.wait_until_ready()


client.run(TOKEN)
