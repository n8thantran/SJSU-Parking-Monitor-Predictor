import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
import time

import discord
from discord.ext import commands
import asyncio

import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

parking_data = {
    "South Garage": 1505,
    "West Garage": 1144,
    "North Garage": 1445,
    "South Campus Garage": 1480
}

# Suppress only the single InsecureRequestWarning from urllib3 needed for requests  
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getParkingPercentage():
    url = 'https://sjsuparkingstatus.sjsu.edu/GarageStatusPlain'
    response = requests.get(url, verify=False)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    garages = soup.find_all('h2', class_='garage__name')
    fullness = soup.find_all('span', class_='garage__fullness')

    data = {
        'Garage': [garage.text.strip() for garage in garages],
        'Fullness (%)': [100 if full.text.strip().lower() == 'full' else int(full.text.strip().split()[0]) for full in fullness],
        'Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(garages) 
    }

    df = pd.DataFrame(data)
    return df

def saveDataToCsvFile(filePath):
    df = getParkingPercentage()
    csv_file_path = filePath
    df.to_csv(csv_file_path, mode='a', header=not pd.io.common.file_exists(csv_file_path), index=False)
    return df

def getCurrentParkingStatus():
    df = getParkingPercentage()
    
    embed = discord.Embed(
        title="Current Parking Status",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    for index, row in df.iterrows():
        garage_name = row['Garage']
        fullness = row['Fullness (%)']
        
        if garage_name in parking_data:
            total_spaces = parking_data[garage_name]
            available_spaces = total_spaces - int(total_spaces * fullness / 100)
            
            if fullness < 50:
                color = "🟢"
            elif fullness < 80:
                color = "🟡"
            else:
                color = "🔴"
            
            status = f"{color} {available_spaces} out of {total_spaces} spaces ({fullness}%)"
            
            embed.add_field(
                name=garage_name,
                value=status,
                inline=False
            )
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed.set_footer(text=f"{current_time} | Spaces are only an estimation")
    
    return embed

@bot.command()
async def parking(ctx):
    embed = getCurrentParkingStatus()
    await ctx.send(embed=embed)

@bot.command()
async def sendcsv(ctx):
    csv_file_path = "parkingData.csv"
    
    if os.path.exists(csv_file_path):
        try:
            file = discord.File(csv_file_path, filename="parkingData.csv")
            
            embed = discord.Embed(
                title="Parking Data CSV",
                description="Here's the CSV file containing the parking data.",
                color=discord.Color.green()
            )
            
            await ctx.send(embed=embed, file=file)
            
        except Exception as e:
            await ctx.send(f"An error occurred while sending the file: {str(e)}")
    else:
        await ctx.send("The CSV file does not exist.")

@bot.command(name='botinfo', aliases=['info'])
async def bot_info(ctx):
    bot = ctx.bot

    server_count = len(bot.guilds)

    member_count = sum(guild.member_count for guild in bot.guilds)
    embed = discord.Embed(title=f"{bot.user.name} Information", color=discord.Color.blue())
    
    embed.add_field(name="Servers", value=f"{server_count:,}", inline=True)
    embed.add_field(name="Members Served", value=f"{member_count:,}", inline=True)
    
    embed.add_field(name="Bot Version", value="1.0.0", inline=False)
    
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the SJSU Parking Lots"))

    # put ur channel here
    channel = bot.get_channel()

    while True:
        df = saveDataToCsvFile("parkingData.csv")
        
        # Create and send embed
        embed = discord.Embed(title="Parking Status Update", color=0x00ff00)
        embed.timestamp = datetime.now()
        
        for index, row in df.iterrows():
            status = f"{row['Fullness (%)']}% full"
            embed.add_field(name=row['Garage'], value=status, inline=False)
        
        await channel.send(embed=embed)
        
        # Wait for 30 minutes
        await asyncio.sleep(300)

bot.run('')
