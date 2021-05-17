import os
import discord
import json
from keep_alive import keep_alive
import datetime
import pytz
from discord.ext import commands
import csv
import requests
import random

global slot 
#time and date calulcation on every event

#Bot Envoirment
BToken = os.environ['Token']
client = discord.Client()

## Get Random Quote 
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "***" + json_data[0]['q'] + "  -- *** **" + json_data[0]['a']+"**"
  return(quote)

## PAUSE LIST - 1st HALF
Pauselist = [631, 633, 639, 641, 674, 649, 655, 657, 703, 705, 711, 713, 719, 721, 727, 729, 735, 737, 743, 745, 751, 753, 759, 801, 807, 809, 815, 817, 823, 825, 831, 833, 839, 841, 847, 849, 855, 857, 903, 905, 911, 913, 919, 921, 927, 929, 935, 937, 943, 945, 951, 953, 959, 1001, 1007, 1009, 1015, 1017, 1023, 1025, 1031, 1033, 1039, 1041, 1047, 1049, 1055, 1057, 1103, 1105, 1111, 1113, 1119, 1121, 1127, 1129, 1135, 1137, 1143, 1145, 1151, 1153, 1159, 1201, 1207, 1209, 1215, 1217, 1223, 1225, 1231, 1233, 1239, 1241, 1247, 1249, 1255, 1257, 1303, 1305, 1311, 1313, 1319, 1321, 1327, 1329, 1335, 1337, 1343, 1345, 1351, 1353, 1359, 1401, 1407, 1409, 1415, 1417, 1423, 1425, 1431, 1433, 1439, 1441, 1447, 1449, 1455, 1457, 1503, 1505, 1511, 1513, 1519, 1521, 1527, 1529, 1535, 1537, 1543, 1545, 1551, 1553, 1559]

global slot 
slot = 0
#Bot interaction in Group
@client.event 
async def on_ready():
  print('Ready')


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
    if message.content.startswith('-pause'):
      await message.reply ("Please use **#pause** channel for requesting pauses.")
      return

  ## Time and Date Update
  utcnow = datetime.datetime.now(tz=pytz.UTC)
  intime = utcnow.astimezone(pytz.timezone('Asia/Calcutta'))
  hnow = intime.hour
  mnow = intime.minute
  tnow = (hnow*100)+mnow
  
  ## Shift time 
  if tnow > 359 and tnow < 1800:
    if message.content.startswith('-p'):
      await message.reply(" No pauses at this time.")
      return

  pausetime = Pauselist[slot]

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
    await message.reply(f'```css .{message.author.name}' + " =>> " + finalslot + "```")
  


# Run BOT
keep_alive()
client.run(BToken) 

