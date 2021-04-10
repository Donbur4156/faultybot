import discord
from discord.ext import commands
import uuid
import ftplib
import ftpdata
import os
import datetime
from lichess import api
from system import function

#  build bot
bot_token = ftpdata.bot_token
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)

id_ref = []


@bot.event
async def on_ready():
    print("I am online!")


@bot.command()
async def kickfaulty(ctx, *args):
    channel = ctx.guild
    if channel:
        text = "Dieser Command steht nur per Privater Nachricht zur Verfügung. " \
               "Der Lichess Token sollte niemals öffentlich benutzt werden!"
        await ctx.send(text)
        await ctx.message.delete()
        return False
    if len(args) != 2:
        await ctx.send("Der Command >kickfaulty benötigt 2 Argumente: 1. Teamname; 2. OAuth Token")
        return False
    team = args[0].lower()
    lichess_token = args[1]
    file_id = str(uuid.uuid4().hex)[0:8]
    new = True
    handle = await datahandle(team, file_id, new)
    text = "Die Daten des Teams **" + args[0] + "** werden heruntergeladen und überprüft! Dies kann je nach " \
           "Größe des Teams mehrere Minuten dauern. Pro 1000 Mitglieder ca. 1 Minute!"
    await ctx.send(text)
    await faultyhandle(ctx, team, args[0], handle, lichess_token)


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
        token = False
        await faultyhandle(ctx, team, args[0], handle, token)
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


async def faultyhandle(ctx, team, arg, handle, token):
    try:
        cheater = function.analyse_team(team)
    except api.ApiHttpError:
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + \
               "** existiert offenbar nicht! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
        id_ref[handle][3] = 4
        return False
    if not cheater:
        text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + \
               "** beinhaltet keine geflaggten User!\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
        id_ref[handle][3] = 3
        return False
    marker = "\n"
    data = marker.join(cheater)
    filename = id_ref[handle][2] + ".flag"
    file = open(filename, 'w')
    file.write(id_ref[handle][2] + "\n" + id_ref[handle][1] + "\n")
    file.write(data)
    file.close()
    await upload(id_ref[handle][2])
    link = "http://www.donbotti.de/?token=" + id_ref[handle][2]
    text = "- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIn dem Team **" + arg + \
           "** wurden User von Lichess markiert, dass sie gegen die Nutzungsbedingungen verstoßen haben. " \
           "Du findest die Liste über diesen Link:\n---> " + link + \
           " <---\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    await ctx.send(text)
    if os.path.isfile(filename):
        os.remove(filename)
    if token:
        count_cheater = 0
        for c in cheater:
            if function.kick(team.lower(), c, token) != "<Response [200]>":
                await ctx.send("Der Token funktioniert nicht!")
                return False
            count_cheater += 1
        if count_cheater == 1:
            text = "Es wurde 1 geflaggter User gekickt"
        else:
            text = "Es wurden " + str(count_cheater) + " geflaggte User gekickt"
        await ctx.send(text)
        id_ref.__delitem__(handle)
        return False
    id_ref[handle][3] = 2


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


bot.run(bot_token)
