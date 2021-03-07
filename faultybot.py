import discord
from discord.ext import commands
from configparser import ConfigParser
import uuid
import ftplib
import ftpdata
import os
import json
import requests
import datetime


parser = ConfigParser()
parser.read("Parameter.ini")
configObject = parser["PARAMS"]
token = configObject["token"]
#
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)
#
global id_ref
id_ref = []


@bot.event
async def on_ready():
    print("I am online!")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def faulty(ctx, arg):
    team = arg.lower()
    file_id = str(uuid.uuid4().hex)[0:8]
    handle = await datahandle(team, file_id)
    # handle = [now, team, file_id, status]
    if id_ref[handle][3] == 1:  # team neu
        text = "Die Daten des Teams **" + arg + "** werden heruntergeladen und überprüft! Dies kann je nach Größe " \
                "des Teams mehrere Minuten dauern. Pro 1000 Mitglieder ca. 1 Minute!"
        await ctx.send(text)
        await faultyhandle(ctx, team, arg, handle)
    elif id_ref[handle][3] == 2:  # Team mit faulty user
        link = "http://www.zeyecx.com/Donbotti/?token=" + id_ref[handle][2]
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDie Abfrage des Teams " + arg + \
               " wurde in den letzten 4 Stunden bereits getätigt. Du findest die Liste über diesen Link:\n---> " \
               + link + " <---\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
    elif id_ref[handle][3] == 3:  # Team ohne faulty user
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDie Abfrage des Teams " + arg + \
               " wurde in den letzten 4 Stunden bereits getätigt. Dabei wurden keine geflaggten user gefunden!" \
               "\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
    elif id_ref[handle][3] == 4:  # Team existierte bei letzter Abfrage nicht
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + \
               "** existiert offenbar nicht! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)


async def faultyhandle(ctx, team, arg, handle):
    data = getdata(team)
    if data:
        data = findfaulty(data)
        if data:
            filename = id_ref[handle][2] + ".flag"
            file = open(filename, 'w')
            file.write("In dem Team " + arg + " wurden folgende User von Lichess geflaggt:\n\n")
            file.write(data)
            file.close()
            await upload(id_ref[handle][2])
            link = "http://www.zeyecx.com/Donbotti/?token=" + id_ref[handle][2]
            text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIn dem Team **" + arg + \
                   "** wurden User von Lichess markiert, dass sie gegen die Nutzungsbedingungen verstoßen haben. " \
                   "Du findest die Liste über diesen Link:\n---> " + link + \
                   " <---\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
            await ctx.send(text)
            if os.path.isfile(filename):
                os.remove(filename)
            id_ref[handle][3] = 2
        else:
            text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + \
                   "** beinhaltet keine geflaggten User!\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
            await ctx.send(text)
            id_ref[handle][3] = 3
    else:
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + \
               "** existiert offenbar nicht! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
        id_ref[handle][3] = 4


async def upload(file_id):
    ftp = ftplib.FTP()
    host = "zeyecx.lima-ftp.de"
    port = 21
    ftp.connect(host, port)
    print(ftp.getwelcome())
    try:
        print("Logging in...")
        ftpuser = ftpdata.user
        ftppwd = ftpdata.pwd
        ftp.login(ftpuser, ftppwd)
        filename = file_id + ".flag"
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
    except BaseException:
        print("Kein Logging möglich!")
    ftp.quit()


def getdata(id_team):
    url = "https://lichess.org/api/team/" + id_team + "/users"
    param = dict()
    resp = requests.get(url=url, params=param)
    list_resp = resp.text.splitlines()
    data = list(map(lambda x: json.loads(x), list_resp))
    return data


def findfaulty(data):
    fault_users = []
    for i in data:
        is_faulti = i.get("tosViolation")
        if is_faulti:
            user = i.get("username")
            fault_users.append(user)
    fault_users.sort(key=str.lower)
    if fault_users:
        trennzeichen = "\n"
        userlist = trennzeichen.join(fault_users)
        return userlist
    else:
        userlist = ""
        return userlist


async def datahandle(team, file_id):
    now = datetime.datetime.utcnow()
    for i in id_ref:
        delta = now - i[0]
        if delta.seconds > 14400:
            id_ref.remove(i)
    for i in id_ref:
        print(i)
        if i[1] == team:
            return id_ref.index(i)
    now = datetime.datetime.utcnow()
    status = 1
    newline = [now, team, file_id, status]
    id_ref.append(newline)
    return id_ref.index(newline)


bot.run(token)
