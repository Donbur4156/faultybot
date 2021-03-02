import discord
from discord.ext import commands
import members
from configparser import ConfigParser
import uuid
import ftplib
import ftpdata
import os
import csv
import datahandler

if __name__ == "__main__":
    parser = ConfigParser()
    parser.read("Parameter.ini")
    configObject = parser["PARAMS"]
    token = configObject["token"]
    #
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='>', intents=intents)
    #
    datahandler.newbase()


@bot.event
async def on_ready():
    print("I am online!")


@bot.event
async def on_reaction_add(reaction, user):
    pass


# Ab here Commands

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command(name='rm')
async def returnmsg(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def faulty(ctx, arg):
    team = arg.lower()
    user = ctx.message.author
    id = await getid()
    handle = await datahandler.datahandle(team, id)
    print(handle)
    if handle:
        link = "http://www.zeyecx.com/Donbotti/?token=" + handle
        await ctx.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDie Abfrage des Teams " + team + " wurde in den letzten 4 Stunden bereits getätigt. Du findest die Liste über diesen Link:\n---> " + link + " <---\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    else:
        text = "Die Daten des Teams **" + team + "** werden heruntergeladen und überprüft! Dies kann je nach Größe des Teams mehrere Minuten dauern. Pro 1000 Mitglieder ca. 1 Minute!"
        await ctx.send(text)
        await faultyhandle(ctx, team, user, id)


async def faultyhandle(ctx, arg, user, id):
    data = members.getfaulty(arg)
    if data == 1:
        await ctx.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + "** existiert offenbar nicht! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    elif data:
        filename = id + ".flag"
        file = open(filename, 'w')
        file.write("In dem Team " + arg + " wurden folgende User von Lichess geflaggt:\n\n")
        file.write(data)
        file.close()
        await upload(id)
        link = "http://www.zeyecx.com/Donbotti/?token=" + id
        await ctx.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIn dem Team **" + arg + "** wurden User von Lichess markiert, dass sie gegen die Nutzungsbedingungen verstoßen haben. Du findest die Liste über diesen Link:\n---> " + link + " <---\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        if os.path.isfile(filename):
            os.remove(filename)
    else:
        await ctx.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + "** beinhaltet keine geflaggten User!\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


async def getid():
    return str(uuid.uuid4().hex)[0:8]


async def upload(id):
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
        filename = id + ".flag"
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
    except:
        print("kein Logging möglich!")
    ftp.quit()



bot.run(token)
