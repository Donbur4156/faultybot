import discord
from discord.ext import commands
import members
from configparser import ConfigParser
import uuid
import ftplib
import ftpdata
import os

parser = ConfigParser()
parser.read("Parameter.ini")
configObject = parser["PARAMS"]
token = configObject["token"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)


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
    user = ctx.message.author
    print(user)
    print(arg)
    text = "Lade die Daten des Teams **" + arg + "** herunter! Die Liste, mit den von Lichess geflaggten Usern, wird im Anschluss erstellt und dir per PN zur Verfügung gestellt! Dies kann je nach Größe des Teams mehrere Minuten dauern. Als Beispiel benötigt ein Team mit 10.000 Mitglieder ca. 10 Minuten!"
    await ctx.send(text)
    await faultyhandle(ctx, arg, user)
    await ctx.send("Vorgang für das Team **" + arg + "** abgeschlossen!")


async def faultyhandle(ctx, arg, user):
    data = members.getfaulty(arg)
    if data == 1:
        await user.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + "** existiert offenbar nicht!\nEnde der Mitteilung! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    elif data:
        uuidID = await getID()
        filename = uuidID + ".flag"
        file = open(filename, 'w')
        file.write("In dem Team " + arg + " wurden folgende User von Lichess geflaggt:\n")
        file.write(data)
        file.close()
        await upload(uuidID)
        link = "http://www.zeyecx.com/Donbotti/?token=" + uuidID
        await user.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIn dem Team **" + arg + "** wurden User von Lichess markiert, dass sie gegen die Nutzungsbedingungen verstoßen haben. Du findest die Liste als Text Datei über diesen Link:\n" + link + "\nEnde der Mitteilung! \n - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        if os.path.isfile(filename):
            os.remove(filename)
    else:
        await user.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + "** beinhaltet keine geflaggten User!\nEnde der Mitteilung! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


async def getID():
    return str(uuid.uuid4().hex)[0:8]


async def upload(uuid_id):
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
        filename = uuid_id + ".txt"
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
    except:
        "failed to login"
    ftp.quit()



bot.run(token)
