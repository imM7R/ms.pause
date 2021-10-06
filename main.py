import os
import discord
import json
import datetime
import pytz
import requests
from discord import Member
from discord.utils import get

# Bot Envoirment
##BToken = os.environ['token']
client = discord.Client()

# view_channel=True,add_reaction=True,read_message_history=True,use_external_emojis=False,send_tts_message=False,use_slash_commands=False,mention_everyone=False,attach_files=False,embed_links=False,manage_webhooks=False,manage_channels=False,manage_roles=False,create_instant_invite=False

#Concurrency
MAX_PAUSE_SHIFT_COUNT = 4

# Dictionary to store count of slot of individual user
USER_SLOT_COUNT = {}

# Maximum Pause, an individual can take
MAX_PAUSE_USER = 2

LOG_FILE = "logs.txt"

shift_start = 1800
shift_end = 411


## Get Random Inspirational Quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random", verify=False)
    json_data = json.loads(response.text)
    quote = "***" + json_data[0]['q'] + " -- *** **" + json_data[0]['a'] + "**"
    return (quote)


def reset_pauseList():
    global Pauselist, PauselistDupl
    Pauselist = PauselistDupl[::]


def clear_log_file():
    open(LOG_FILE, 'w').close()


def write_log(ids, username, shift_pause):
    global USER_SLOT_COUNT
    count = 0
    try:
        count = USER_SLOT_COUNT[ids]
    except:
        pass
    timedate = datetime.datetime.utcnow().strftime("%H:%M-%d/%m/%y")

    with open(LOG_FILE, 'a+') as file:
        file.write('{},{},{},{},{}\n'.format(ids, username, shift_pause, timedate, count))
    return 0


    def get_log_data():
        data = []
        with open(LOG_FILE, 'r') as file:
            data = file.readlines()
        return ''.join(data).strip()


## PAUSE LIST - 10 mins

Pauselist = [630, 640, 650, 700, 710, 720, 730, 740, 750, 800, 810, 820, 830, 840, 850, 900, 910, 920, 930, 940, 950,
             1000, 1010, 1020, 1030, 1040, 1050, 1100, 1110, 1120, 1130, 1140, 1150, 1200, 1210, 1220, 1230, 1240, 1250,
             1300, 1310, 1320, 1330, 1340, 1350, 1400, 1410, 1420, 1430, 1440, 1450, 1500, 1510, 1520, 1530, 1540, 1550,
             1600, 1610, 1620]
PauselistDupl = Pauselist[::]

countDict = {}

# Bot interaction in Group
@client.event
async def on_ready():
    print('Ready!')


@client.event
async def on_message(message):
    ## Self Retun
    global shift_end, shift_start, MAX_PAUSE_SHIFT_COUNT, countDict, Pauselist, PauselistDupl, USER_SLOT_COUNT, MAX_PAUSE_USER
    if message.author == client.user:
        return

    ## Output Random Quote
    if message.content.startswith('!q'):
        quote = get_quote()
        await message.channel.send(quote)
        return

    ## Channel Filtering // General Chat
    if message.channel.id == 838353565558243332:
        if message.content.startswith('-pau') or message.content.startswith('-Pau') or message.content.startswith(
                'Pau') or message.content.startswith('pau') or message.content.startswith('PAUSE'):
            await message.reply("Hey! Please use the **#pause** channel for requesting pauses.")
            return

    ## Function for changing shift_start and shift_end
    if message.channel.id == 857277054341218347:
        if (message.content.startswith('!shiftstart')):
            value = float(message.content.split(' ')[1])
            shift_start = value
            await message.reply("Shift START time changed.")

        if (message.content.startswith('!shiftend')):
            value = float(message.content.split(' ')[1])
            shift_end = value
            await message.reply("Shift START time changed.")

        if (message.content.startswith('!help')):
            await message.reply(
                "****BOT COMMANDS**** \n **!q** - Random inspirational quote \n **!ahod** - All Hands on Deck. \n **!uf** - Unfreeze Pauses. \n **!conc** - Changes max pause limit (!conc 3) \n **!reset** - Bot reset \n **!clearlog** - Clear LOG file. \n **!log** - Outputs log file \n **!help** - Commands. \n **!shiftstart** - Change shift start time (Do not use) \n **!shiftend** - Change shift end time. (Do not use)")

        if message.content.startswith('!ahod'):
            guild = client.get_guild(838353565558243329)
            channel = client.get_channel(838369470803738625)
            role_id = 838356141112557568
            role = get(guild.roles, id=role_id)
            permissions = discord.Permissions()
            permissions.update(manage_messages=False, send_messages=False, view_channel=True, add_reactions=True,
                               read_message_history=True, use_external_emojis=False, send_tts_messages=False,
                               use_slash_commands=False, mention_everyone=False, attach_files=False, embed_links=False,
                               manage_webhooks=False, manage_channels=False, manage_roles=False,
                               create_instant_invite=False)
            await role.edit(permissions=permissions)
            await channel.edit(name='ahod-pause-freezed')
            await channel.send(
                "**All Hands on Deck - Pauses are FREEZED for the next 15 mins. Please do NOT pause the app.**")
            await message.reply("**All Hands on Deck - Pauses FREEZED.**")
            await channel.set_permissions(role, manage_messages=False, send_messages=False, view_channel=True,
                                          add_reactions=True, read_message_history=True, use_external_emojis=False,
                                          send_tts_messages=False, use_slash_commands=False, mention_everyone=False,
                                          attach_files=False, embed_links=False, manage_webhooks=False,
                                          manage_channels=False, manage_roles=False, create_instant_invite=False)
            return

        if message.content.startswith('!uf'):
            guild = client.get_guild(838353565558243329)
            channel = client.get_channel(838369470803738625)
            role_id = 838356141112557568
            role = get(guild.roles, id=role_id)
            permissions = discord.Permissions()
            permissions.update(send_messages=True, view_channel=True, add_reactions=True, read_message_history=True,
                               use_external_emojis=False, send_tts_messages=False, use_slash_commands=False,
                               mention_everyone=False, attach_files=False, embed_links=False, manage_webhooks=False,
                               manage_channels=False, manage_roles=False, create_instant_invite=False)
            await role.edit(permissions=permissions)
            await channel.edit(name='pause')
            await channel.send("**Pauses are available now.**")
            await message.reply("**Pauses are available now.**")
            await channel.set_permissions(role, manage_messages=False, send_messages=True, view_channel=True,
                                          add_reactions=True, read_message_history=True, use_external_emojis=False,
                                          send_tts_messages=False, use_slash_commands=False, mention_everyone=False,
                                          attach_files=False, embed_links=False, manage_webhooks=False,
                                          manage_channels=False, manage_roles=False, create_instant_invite=False)
            return

        if message.content.startswith("!conc"):
            value = float(message.content.split(' ')[1])
            MAX_PAUSE_SHIFT_COUNT = value
            await message.reply("**Pause concurrency changed**")

        # Clear LOGS command
        if message.content.startswith('!clearlog'):
            clear_log_file()
            await message.reply("**LOG file cleared.**")

        if message.content.startswith("!reset"):
            clear_log_file()
            Pauselist = PauselistDupl[::]
            MAX_PAUSE_SHIFT_COUNT = 3
            MAX_PAUSE_USER = 2
            await  message.reply("**BOT Resetting...**")
            with open(LOG_FILE, "rb") as file:
                await message.reply("**Log File**", file=discord.File(file, "logs.csv"))
            await  message.reply("**LOG file cleared**")
            await  message.reply("**MAX Pause/User = 2 || Concurrency = 3**")
        if message.content.startswith("!maxpause"):
            value = float(message.content.split(' ')[1])
            MAX_PAUSE_USER = value
            await message.reply("**Max Pause is set to {}**".format(MAX_PAUSE_USER))

        if message.content.startswith("!log"):
          with open(LOG_FILE,"rb") as file:
            await message.reply("**Log File**",file=discord.File(file,"logs.csv"))
            
    if message.channel.id == 838369470803738625:
        ## Time and Date Update
        utcnow = datetime.datetime.now(tz=pytz.UTC)
        intime = utcnow.astimezone(pytz.timezone('Asia/Calcutta'))
        hnow = intime.hour
        mnow = intime.minute
        tnow = (hnow * 100) + mnow

        ## Shift time
        if tnow < shift_start and tnow >= shift_end:
            if message.content.startswith('-p') or message.content.startswith('pau') or message.content.startswith(
                    'Pau') or message.content.startswith('PAUSE'):
                await message.reply("**No pauses at this time.**")
                return

        ## Add 1200 hrs
        if tnow <= 500:
            tnow = tnow + 1200
        elif tnow > 500:
            tnow = tnow - 1200

        for x in Pauselist:
            if x > tnow:
                break
            x += 1

        try:
            if (USER_SLOT_COUNT[message.author.id] >= MAX_PAUSE_USER):
                await message.reply("**{} pauses already alloted today.**".format(MAX_PAUSE_USER))
                return
            else:
                USER_SLOT_COUNT[message.author.id] += 1
        except:
            USER_SLOT_COUNT[message.author.id] = 1

        if (not x):
            await message.reply("No more pauses available.")
        try:
            countDict[x] += 1
        except:
            countDict[x] = 1

        print(countDict[x])
        if (countDict[x] == MAX_PAUSE_SHIFT_COUNT):
            print(intime, " - Count exceeded for slot - ", x)
            Pauselist.remove(x)

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
            finaltime = string[0] + string[1] + ":" + string[2] + string[3]

        elif x <= 959:
            z = x + 1200
            string = str(x)
            stringt = str(z)
            finalslot = string[0] + ":" + string[1] + string[2]
            finaltime = stringt[0] + ":" + stringt[1] + stringt[2]

        write_log(message.author.id, message.author.display_name, x)
        if message.content.startswith('-t'):
            await message.reply("The time is " + finaltime)

        if message.content.startswith('-pau'):
            await message.reply(f'```{message.author.display_name}' + " =>> " + finalslot + "```")

        if message.content.startswith('pause'):
            await message.reply(f'```{message.author.display_name}' + " =>> " + finalslot + "```")

        if message.content.startswith('Paus') or message.content.startswith('-Pa') or message.content.startswith(
                'PAUS'):
            await message.reply(f'```{message.author.display_name}' + " =>> " + finalslot + "```")

# Run BOT
client.run('ODQzMDMxMjE3ODUwNTQ4MjI1.YJ98AQ.pwxNLx6AyIKnzuiEyrluPsLqH3k')
