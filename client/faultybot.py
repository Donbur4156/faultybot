import discord
from discord.ext import commands
import uuid
import ftplib
import ftpdata
import os
import json
import requests
import datetime
from lichess import api


token = ftpdata.token

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)

id_ref = []


@bot.event
async def on_ready():
    print("I am online!")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def faulty(ctx, *args):
    new = False
    team = args[0].lower()
    if len(args) > 1 and args[1] == "new":
        new = True
    file_id = str(uuid.uuid4().hex)[0:8]
    handle = await datahandle(team, file_id, new)
    # handle = [now, team, file_id, status]
    if id_ref[handle][3] == 1:  # team neu
        text = "Die Daten des Teams **" + args[0] + "** werden heruntergeladen und überprüft! Dies kann je nach " \
                "Größe des Teams mehrere Minuten dauern. Pro 1000 Mitglieder ca. 1 Minute!"
        await ctx.send(text)
        await faultyhandle(ctx, team, args[0], handle)
    elif id_ref[handle][3] == 2:  # Team mit faulty user
        link = "http://www.donbotti.de/?token=" + id_ref[handle][2]
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDie Abfrage des Teams " + args[0] + \
               " wurde in den letzten 4 Stunden bereits getätigt. Du findest die Liste über diesen Link:\n---> " \
               + link + " <---\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
    elif id_ref[handle][3] == 3:  # Team ohne faulty user
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDie Abfrage des Teams " + args[0] + \
               " wurde in den letzten 4 Stunden bereits getätigt. Dabei wurden keine geflaggten user gefunden!" \
               "\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
    elif id_ref[handle][3] == 4:  # Team existierte bei letzter Abfrage nicht
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + args[0] + \
               "** existiert offenbar nicht! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)


async def faultyhandle(ctx, team, arg, handle):
    data = api.users_by_team(team)
    if data:
        data = findfaulty(data)
        if data:
            filename = id_ref[handle][2] + ".flag"
            file = open(filename, 'w')
            file.write(id_ref[handle][2] + "\n" + id_ref[handle][1] + "\n")
            file.write(data)
            file.close()
            await upload(id_ref[handle][2])
            link = "http://www.donbotti.de/?token=" + id_ref[handle][2]
            text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\ntemp - In dem Team **" + arg + \
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
    try:
        ftp.connect(host, port)
        print(ftp.getwelcome())
        print("Logging in...")
        ftpuser = ftpdata.user
        ftp_pw = ftpdata.pwd
        ftp.login(ftpuser, ftp_pw)
        filename = file_id + ".flag"
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
        ftp.quit()
    except ftplib.all_errors:
        print("Kein Logging möglich!")


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
        user = i.get("username")
        is_faulti = i.get("tosViolation")
        if is_faulti:
            fault_users.append(user)
    fault_users.sort(key=str.lower)
    if fault_users:
        trennzeichen = "\n"
        userlist = trennzeichen.join(fault_users)
        return userlist
    else:
        userlist = ""
        return userlist


async def datahandle(team, file_id, new):
    now = datetime.datetime.utcnow()
    for i in id_ref:
        delta = now - i[0]
        if delta.seconds > 14400 or i[1] == team and new:
            id_ref.remove(i)
        elif i[1] == team:
            return id_ref.index(i)
    now = datetime.datetime.utcnow()
    status = 1
    newline = [now, team, file_id, status]
    id_ref.append(newline)
    return id_ref.index(newline)


bot.run(token)
