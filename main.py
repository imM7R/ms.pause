import os
import discord
import json
from keep_alive import keep_alive
import datetime
import pytz
import csv
import requests
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get



#Bot Envoirment
BToken = os.environ['Token']
client = discord.Client()

## Get Random Quote 
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "***" + json_data[0]['q'] + "  -- *** **" + json_data[0]['a']+"**"
  return(quote)

## PAUSE LIST - 10 mins
Pauselist = [635, 640, 650, 700, 710, 720, 730, 740, 750, 800, 810, 820, 830, 840, 850, 900, 910, 920, 930, 940, 950, 1000, 1010, 1020, 1030, 1040, 1050, 1100, 1110, 1120, 1130, 1140, 1150, 1200, 1210, 1220, 1230, 1240, 1250, 1300, 1310, 1320, 1330, 1340, 1350, 1400, 1410, 1420, 1430, 1440, 1450, 1500, 1510, 1520, 1530, 1540, 1550, 1600, 1610]


#Bot interaction in Group
@client.event 
async def on_ready():
  print('Ready')

## CSV File


@client.event 
async def on_message(message):
  ## Self Retun
  if message.author == client.user:
    return
  
  ## Output Random Quote
  if message.content.startswith('!q'):
    quote = get_quote()
    await message.channel.send(quote)
    return

  ## Channel Filtering // General Chat
  if message.channel.id == 838353565558243332:
    if message.content.startswith('-pau') or message.content.startswith('-Pau') or  message.content.startswith('Pau') or message.content.startswith('paus') or message.content.startswith('PAUSE'):
      await message.reply ("Please use **#pause** channel for requesting pauses.")
      return

  if message.channel.id == 839652258404237323: 
    if message.content.startswith('!ahod'):
      guild = client.get_guild(838353565558243329)
      channel = client.get_channel(839652258404237323)
      role_id = 855906834836488232
      role = get(guild.roles, id=role_id)
      permissions = discord.Permissions()
      permissions.update(send_messages=False)
      await role.edit(permissions=permissions)
      await channel.edit(name='AHOD-Test-Freezed')
      await message.reply ("**All Hands on Deck - Pauses FREEZED for the next 15 mins. Please do NOT pause the app or request pauses.**")
      ##await message.channel.set_Permissions(role, send_messages=False)
      return

    if message.content.startswith('!uf'):
     channel = client.get_channel(839652258404237323)
     role = 855906834836488232
     await channel.edit(name='Test')
     await message.reply ("**Pauses are avialable now.**")
     await message.channel.set_Permissions(role, send_messages=True)
     return

  ## Time and Date Update
  utcnow = datetime.datetime.now(tz=pytz.UTC)
  intime = utcnow.astimezone(pytz.timezone('Asia/Calcutta'))
  hnow = intime.hour
  mnow = intime.minute
  tnow = (hnow*100)+mnow
  
  ## Shift time 
  if tnow >= 405 and tnow < 1800:
    if message.content.startswith('-p') or message.content.startswith('pau') or message.content.startswith('Pau') or      message.content.startswith('PAUSE'):
      await message.reply("No pauses at this time.")
      return

  ## Add 1200 hrs
  if tnow <= 500:
    tnow = tnow + 1200
  elif tnow > 500:
    tnow = tnow - 1200


  for x in Pauselist:
    if x > tnow:
      break
    x +=1


  if x > 1259:
    z = x - 1200
    string = str(x)
    stringt = str(z)
    tt1 = stringt[2]
    finalslot = stringt[0] + ":" + stringt[1] + tt1
    finaltime = stringt[0] + ":" + stringt[1] + tt1

  elif x > 959 and x < 1259:
    string = str(x)
    finalslot = string[0] + string[1] + ":" + string[2] + string[3]
    finaltime = string[0] + string[1] +":" + string[2] + string[3]
    
  elif x <= 959:
    z = x + 1200
    string = str(x)
    stringt = str(z)
    finalslot = string[0] + ":" + string[1] + string[2]
    finaltime = stringt[0] + ":" + stringt[1] + stringt[2]
  
    

  if message.content.startswith('-t'):
    await message.reply("The time is " + finaltime)

  if message.content.startswith('-pau'):
    await message.reply(f'```{message.author.name}' + " =>> " + finalslot + "```") 
    
  if message.content.startswith('pause'):
    await message.reply(f'```{message.author.name}' + " =>> " + finalslot + "```")
    
  if message.content.startswith('Paus') or message.content.startswith('-Pa') or message.content.startswith('PAUS'):
    await message.reply(f'```{message.author.name}' + " =>> " + finalslot + "```")
    
  


# Run BOT
keep_alive()
client.run(BToken) 

