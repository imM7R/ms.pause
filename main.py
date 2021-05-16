import os
import discord
import json
from keep_alive import keep_alive
import datetime
import pytz
from discord.ext import commands
import csv

global slot 
#time and date calulcation on every event

#Bot Envoirment
BToken = os.environ['Token']
client = discord.Client()

## PAUSE LIST
Pauselist = [631, 632, 633, 634, 639, 640, 641, 642, 643, 648, 649, 650, 655, 656, 657, 685, 703, 704, 705, 706, 711, 712, 713, 714, 719, 720, 721, 722, 727, 728, 729, 730, 735, 736, 737, 738, 743, 744, 745, 746, 751, 752, 753, 754, 759, 800, 801, 802, 807, 808, 809, 810, 815, 816, 817, 818, 823, 824, 825, 826, 831, 832, 833, 834, 839, 840, 841, 842, 847, 848, 849, 850, 855, 856, 857, 858, 903, 904, 905, 906, 911, 912, 913, 914, 919, 920, 921, 922, 927, 928, 929, 930, 935, 936, 937, 938, 943, 944, 945, 946, 951, 952, 953, 954, 959, 1000, 1001, 1002, 1007, 1008, 1009, 1010, 1015, 1016, 1017, 1018, 1023, 1024, 1025, 1026, 1031, 1032, 1033, 1034, 1039, 1040, 1041, 1042, 1047, 1048, 1049, 1050, 1055, 1056, 1057, 1058, 1103, 1104, 1105, 1106, 1111, 1112, 1113, 1114, 1119, 1120, 1121, 1122, 1127, 1128, 1129, 1130, 1135, 1136, 1137, 1138, 1143, 1144, 1145, 1146, 1151, 1152, 1153, 1154, 1159, 1200, 1201, 1202, 1207, 1208, 1209, 1210, 1215, 1216, 1217, 1218, 1223, 1224, 1225, 1226, 1231, 1232, 1233, 1234, 1239, 1240, 1241, 1242, 1247, 1248, 1249, 1250, 1255, 1256, 1257, 1258, 1303, 1304, 1305, 1306, 1311, 1312, 1313, 1314, 1319, 1320, 1321, 1322, 1327, 1328, 1329, 1330, 1335, 1336, 1337, 1338, 1343, 1344, 1345, 1346, 1351, 1352, 1353, 1354, 1359, 1400, 1401, 1402, 1407, 1408, 1409, 1410, 1415, 1416, 1417, 1418, 1423, 1424, 1425, 1426, 1431, 1432, 1433, 1434, 1439, 1440, 1441, 1442, 1447, 1448, 1449, 1450, 1455, 1456, 1457, 1458, 1503, 1504, 1505, 1506, 1511, 1512, 1513, 1514, 1519, 1520, 1521, 1522, 1527, 1528, 1529, 1530, 1535, 1536, 1537, 1538, 1543, 1544, 1545, 1546, 1551, 1552, 1553, 1554, 1559]

global slot 
slot = 0
#Bot interaction in Group
@client.event 
async def on_ready():
  print('Ready')


@client.event 
async def on_message(message):
  if message.author == client.user:
    return

  ## Time and Date Update
  utcnow = datetime.datetime.now(tz=pytz.UTC)
  intime = utcnow.astimezone(pytz.timezone('Asia/Calcutta'))
  hnow = intime.hour
  mnow = intime.minute
  tnow = (hnow*100)+mnow
  
  pausetime = Pauselist[slot]

  ## Add 1200 hrs
  if tnow < 500:
    tnow = tnow + 1200


  for x in Pauselist:
    if x > tnow:
      pausetime = x
      break

  if x > 1259:
    z = x - 1200
    string = str(x)
    stringt = str(x)
    finalslot = stringt[0] + " : " + stringt[1] + string[2]
    finaltime = stringt[0] + " : " + stringt[1] + string[2]

  if x > 959 and x < 1259:
    string = str(x)
    stringt = str(tnow)
    finalslot = string[0] + string[1] + " : " + string[2] + string[3]
    finaltime = stringt[0] + string[1] +" : " + stringt[2] + stringt[3]
    
  if x < 1000:
    string = str(x)
    stringt = str(tnow)
    finalslot = string[0] + " : " + string[1] + string[2]
    finaltime = stringt[0] + " : " + stringt[1] + stringt[2]
  
  pausetime1 = intime.strftime('%I:%M %p')
  
  if message.content.startswith('-t'):
    await message.reply("The time is " + finaltime)

  if message.content.startswith('-p'):
    await message.reply(f'{message.author.name}'+ " =>> " + finalslot) 
  



# Run BOT
keep_alive()
client.run(BToken) 

