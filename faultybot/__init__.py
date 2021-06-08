import asyncio
import datetime
import ftplib
import os
import os.path
import sys
import uuid
import json
from concurrent.futures import ThreadPoolExecutor
import aiocron
import discord
import lichesspy.api
from discord.ext import commands
import config
import function

# Build the bot according to the Discord syntax
bot_token = config.bot_token
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

id_ref = []
TEAM_FILE = os.path.join(sys.path[0], "teams_to_check.json")

# Test function to see if the bot is online.
@bot.event
async def on_ready():
    print_log("I am online!")


@bot.event
async def on_message(ctx):
    if ctx.content.startswith('>'):
        user = "<@" + str(ctx.author.id) + ">"
        await ctx.channel.send(f'{user}, the Prefix of the bot was changed to "!"')
    await bot.process_commands(ctx)


@bot.command(aliases=['Kickfaulty'])
async def kickfaulty(ctx, *args):
    channel = ctx.guild
    if channel:
        text = "This command is only available via private message.. " \
               "The Lichess Token should never be used publicly!"
        await ctx.send(text)
        await ctx.message.delete()
        return False
    if len(args) != 2:
        text = "The command ``>kickfaulty`` requires 2 arguments: " \
               "1. ``team name``; 2. ``OAuth token``"
        await ctx.send(text)
        return False
    team = function.check_team_name(args[0].lower())
    lichess_token = args[1]
    handle = await datahandle(team)
    text = f"The data of the team **{team}** is downloaded and checked! This can take several " \
           f"minutes depending on the size of the team. Per 1000 members approx 1 minute!"
    await ctx.send(text)
    cheaters, handle = await faultyhandle(ctx, team, handle)
    if cheaters:
        await run_kick(ctx, team, handle, cheaters, lichess_token)


@bot.command(aliases=['Faulty'])
async def faulty(ctx, *args):
    if len(args) <1 or len(args) >2:
        text = "The command ``>faulty`` requires at least 1 argument: " \
               "1. ``team name``; 2. ``optional: new [if you want a new request]``"
        await ctx.send(text)
        return False
    new = False
    team = function.check_team_name(args[0].lower())
    if len(args) > 1 and args[1] == "new":
        new = True
    handle = await datahandle(team, new)
    # handle = [now, team, file_id, status]
    if id_ref[handle][3] == 1:  # team neu
        text = f"The data of the team **{team}** is downloaded and checked! " \
               "This can take several minutes depending on the size of the team. " \
               "Per 1000 members approx 1 minute!"
        await ctx.send(text)
        await faultyhandle(ctx, team, handle)
    elif id_ref[handle][3] == 2:  # Team mit faulty user
        link = "http://www.donbotti.de/?token=" + id_ref[handle][2]
        text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nThe query of the team " \
               f"{team} has already been made in the last 4 hours. You can find the list via this" \
               f" link:\n--->{link}<---\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
    elif id_ref[handle][3] == 3:  # Team ohne faulty user
        text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nThe query of the team " \
               f"{team} has already been made in the last 4 hours. No flagged users were found!" \
               "\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
    elif id_ref[handle][3] == 4:  # Team existierte bei letzter Abfrage nicht
        text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
               f"The query of the team **{team}**  apparently does not exist! \n" \
               f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)


@bot.command()
@commands.has_role(802626303958188122)
async def add(ctx, teamname, userid):
    print_log(f'Team {teamname} for User {userid}')
    with open(TEAM_FILE, 'r') as json_file:
        json_data = json.load(json_file)
    teamnew = True
    for team in json_data['teams']:
        if team['teamname'] == teamname:
            if userid not in team['user']:
                team['user'].append(userid)
            teamnew = False
            break
    if teamnew:
        json_data['teams'].append({
            'teamname': teamname,
            'user': [userid]
        })
    with open(TEAM_FILE, 'w') as json_file:
        json.dump(json_data, json_file)
    mention = "<@" + str(userid) + "> "
    text = f"das Team {teamname} ist nun mit dem User mit dem User {mention} " \
            f"(ID:{userid}) verknüpft."
    await ctx.send(text)


@bot.command()
async def get(ctx):
    with open(TEAM_FILE, 'r') as json_file:
        json_data = json.load(json_file)
    for team in json_data['teams']:
        teamname = team['teamname']
        userlist = team['user']
        text = f'Das Team {teamname} ist mit diesen Usern verknüpft:\n'
        for user in userlist:
            text += f"<@{str(user)}>; "
        await ctx.send(text)


@add.error
async def add_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRole):
        await ctx.send("Du hast nicht die benötigten Rechte um diesen Command auszuführen!")


async def faultyhandle(ctx, team, handle):
    try:
        loop = asyncio.get_event_loop()
        cheaters = await loop.run_in_executor(ThreadPoolExecutor(), function.analyse_team, team)
    except lichesspy.api.ApiHttpError:
        text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
               f"The queried team **{team}** apparently does not exist! \n" \
               f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
        id_ref[handle][3] = 4
        return False
    if not cheaters:
        text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
               f"The queried team **{team}** does not include flagged users!\n" \
               f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
        id_ref[handle][3] = 3
        return False
    marker = "\n"
    data = marker.join(cheaters)
    filename = id_ref[handle][2] + ".flag"
    with open(filename, 'w') as file:
        file.write(f"{id_ref[handle][2]}\n{id_ref[handle][1]}\n")
        file.write(data)
    upload(id_ref[handle][2])
    link = f"http://www.donbotti.de/?token={id_ref[handle][2]}"
    text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIn the team **{team}**, " \
           f"users were marked by Lichess as having violated the terms of use. " \
           f"You can find the list via this link:\n--->{link}<---\n" \
           f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    await ctx.send(text)
    if os.path.isfile(filename):
        os.remove(filename)
    id_ref[handle][3] = 2
    return cheaters, handle


async def run_kick(ctx, team, handle, cheaters, token):
    print_log(f"found {str(len(cheaters))} Cheater in Team {str(team)}")
    count_cheater = 0
    for cheater in cheaters:
        request = function.kick(team.lower(), cheater, token)
        print_log("Request for Cheater " + str(count_cheater +
                    1) + " '" + cheater + "' returns " + str(request))
        if not function.check(request):
            status = function.status(request)
            text = f"The kick process was cancelled due to the following error:\n" \
                    f"**{status}**\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
            print_log(f"Request failed with {status}")
            await ctx.send(text)
            return False
        print_log("with success")
        count_cheater += 1
    if count_cheater == 1:
        text = "There was 1 flagged user kicked\n" \
                " - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    else:
        text = f"There were {str(count_cheater)} flagged users kicked\n" \
                f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    await ctx.send(text)
    id_ref.__delitem__(handle)
    return False


# Uploads the files to the FTP server.
def upload(file_id):
    # Lima City hosts the server for us. But you can also use another provider.
    ftp = ftplib.FTP()
    host = config.url
    port = config.port
    try:
        ftp.connect(host, port)
        ftpuser = config.user
        ftp_pw = config.pwd
        ftp.login(ftpuser, ftp_pw)
        filename = f"{file_id}.flag"
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
            print_log(f"Upload of the file {filename} is successfully completed.")
        ftp.quit()
    except ftplib.all_errors:
        print_log("No logging possible!")


def write_file(handle, cheaters):
    marker = "\n"
    data = marker.join(cheaters)
    filename = id_ref[handle][2] + ".flag"
    with open(filename, 'w') as file:
        file.write(f"{id_ref[handle][2]}\n{id_ref[handle][1]}\n")
        file.write(data)
    return filename


async def datahandle(team, new=True):
    file_id = str(uuid.uuid4().hex)
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


# Creates a logger and works with it.
def print_log(text):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    print(str(now) + ": " + str(text))


# Cronjob every day at 02:00 for every team in database
@aiocron.crontab('0 2 * * *')
async def crown_faulty():
    print_log("start Crown")
    with open(TEAM_FILE, 'r') as json_file:
        json_data = json.load(json_file)
    for team in json_data['teams']:
        teamname = team['teamname']
        print_log(teamname)
        userlist = team['user']
        print_log(userlist)
        handle = await datahandle(teamname)
        try:
            loop = asyncio.get_event_loop()
            cheaters = await loop.run_in_executor(ThreadPoolExecutor(),
            function.analyse_team, teamname)
        except lichesspy.api.ApiHttpError:
            id_ref[handle][3] = 4
            return False
        if cheaters:
            print_log(f'{str(len(cheaters))}cheater found: in team {teamname}')
            print_log(cheaters)
            filename = write_file(handle, cheaters)
            upload(id_ref[handle][2])
            user_mention = ""
            for user in userlist:
                user_mention += "<@" + str(user) + "> "
            link = f"http://www.donbotti.de/?token={id_ref[handle][2]}"
            text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
                f"{user_mention}\nIn the team **{teamname}**, " \
                f"users were marked by Lichess as having violated the terms of use. " \
                f"You can find the list via this link:\n--->{link}<---\n" \
                f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
            request_channel = bot.get_channel(814566650345947177)
            await request_channel.send(text)
            if os.path.isfile(filename):
                os.remove(filename)
            id_ref[handle][3] = 2
    print_log("end Crown")


def create_teamlist():
    if not os.path.isfile(TEAM_FILE):
        with open(TEAM_FILE, 'w') as jsonfile:
            data = {'teams': []}
            json.dump(data, jsonfile)


# Starting from the Await Client
if __name__ == "__main__":
    create_teamlist()
    bot.run(bot_token)
