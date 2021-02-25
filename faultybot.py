import discord
from discord.ext import commands
import members
from configparser import ConfigParser

parser = ConfigParser()
parser.read("Parameter.ini")
configObject = parser["PARAMS"]
token = configObject["token"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)
# rollenchannel_id = 813802464599605248


@bot.event
async def on_ready():
    print("I am online!")
    # rollenchannel = bot.get_channel(rollenchannel_id)


@bot.event
async def on_reaction_add(reaction, user):
    pass


# Ab hier Commands

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
    text = "Lade die Daten des Teams **" + arg + "** herunter! Die Liste, mit den von Lichess geflaggten Usern, wird im Anschluss erstellt und dir per PN zugesendet! Dies kann je nach Größe des Teams mehrere Minuten dauern. Als Beispiel benötigt ein Team mit 10.000 Mitglieder ca. 10 Minuten!"
    await ctx.send(text)
    await faultyhandle(ctx, arg, user)

async def faultyhandle(ctx, arg, user):
    data = members.getfaulty(arg)
    if data:
        await user.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIn dem Team **" + arg + "** wurden folgende User von Lichess markiert, dass sie gegen die Nutzungsbedingungen verstoßen haben:\n" + data + "\nEnde der Mitteilung! \n - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    else:
        await user.send("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nDas abgefragte Team **" + arg + "** beinhaltet keine geflaggten User!\nEnde der Mitteilung! \n- - - - - - - - - - - - - - - - - - - - - - - - - - - - ")




bot.run(token)
