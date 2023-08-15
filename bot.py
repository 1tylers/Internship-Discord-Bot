import discord
from discord.ext import tasks
import responses

from selenium import webdriver
from selenium.webdriver.common.by import By

internship_list_1 = []

# async functions can be paused and resumed, making it dynamic for discord
# this function handles the response to user commands
async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'your token here'
    intents=discord.Intents.default()

    # stop unncescesary event notifications
    intents.typing = False
    intents.presences = False

    # enable bot to see messages
    intents.message_content = True
    client = discord.Client(intents=intents)

    # this function activates on bot start up
    @client.event
    async def on_ready():
        global internship_list_1

        print(f'{client.user} is now running!')

        # get list of internships on start up
        internship_list_1 = list(responses.get_internship_list())

        # start the get list function
        get_list.start()


    # function for whenever a message is sent
    @client.event
    async def on_message(message):
        # prevents endless loops, making sure the bot doesnt respond to itself
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{user_message}")
        print(f"{username} said: '{user_message}' ({channel})")

        # code for bot to respond to messages
        response = responses.handle_response(user_message)
        print(f"Generated response: {response}")
        await send_message(message, user_message)

    # function that loops every 6 hours for the announcements
    @tasks.loop(seconds=21600)
    async def get_list():
        global internship_list_1

        # get the new internship list
        internship_list_2 = list(responses.get_internship_list())

        announcement = "New listings for Summer Internships have been posted to levels.fyi/internships:\n"

        differences_exist = False

        # find listings that internship 1 has that internship 2 doesn't, that means theres new listings.
        for internship in internship_list_1:
            if internship not in internship_list_2:
                differences_exist = True
                add_to_announcement = f"Company: {internship_list_1['name']}, Location: {internship_list_1['location']}\n"
                announcement += add_to_announcement

        # if there are no differences, there are no new listings
        if not differences_exist:
            announcement = "No new listings for Summer Internships have been posted to levels.fyi/internships"

        # sets the new list as the old list so its ready to compare for the next update
        internship_list_1 = list(internship_list_2)

        print(internship_list_1)

        # send the message
        message_channel = client.get_channel(your channel id here)
        print(f"Got channel id ({message_channel})")
        if message_channel:
            await message_channel.send(announcement)

    
    client.run(TOKEN)
