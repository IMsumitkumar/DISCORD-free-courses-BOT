import discord
from discord.ext import tasks
import pandas as pd
import configration 
import time
import os
from selenium import webdriver
from discord.ext import commands
from datetime import date, datetime, timedelta
from scrapper import scrap_free_course, recent_data


TOKEN = os.environ.get('TOKEN')

client = discord.Client()

# @client.event
# async def on_ready(): 
#     print("Bot is ready!")

@tasks.loop(hours=24)
async def free_course():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    DRIVER=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d") 

    DATA = recent_data(configration.DATAFRAME)
    # DRIVER = webdriver.Chrome("drivers/chromedriver.exe")

    data = scrap_free_course(wd=DRIVER, url_dict=configration.URL_DICT, df=DATA)
    data = data.sort_values('date_time', ascending=False).drop_duplicates(['title'], keep='last').reset_index(drop=True)
    data.to_csv("database/free_courses.csv", index=False)

    new_data = pd.read_csv("database/free_courses.csv")
    data = new_data[new_data['date_time'] == date_time].reset_index(drop=True)
    data = data[(data['title']!="Not Available") & (data['duration'] != "Expired")].reset_index(drop=True)
    channel = client.get_channel(817013087324209162)

    for i in range(data.shape[0]):
        embed=discord.Embed(title=data['title'][i], description=data['desc'][i], 
                            url=data['link'][i], color=0xFF5733)
        embed.set_author(name=data['name'][i])
        embed.set_thumbnail(url="https://i.imgur.com/NPvfO4I.jpg")
        embed.add_field(name="FREE", value=data['duration'][i], inline=False)
        embed.add_field(name="category", value=data['category'][i], inline=True)
        embed.add_field(name="Rating", value=data['rating'][i],  inline=True)
        embed.set_image(url=data['image'][i])
        embed.set_footer(text="Click on the title to enroll.")
        await channel.send(embed=embed)

@client.event
async def on_ready():
    free_course.start()

client.run(TOKEN)


