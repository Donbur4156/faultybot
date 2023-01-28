import asyncio
import os
import os.path
import sys
import json
from concurrent.futures import ThreadPoolExecutor
import aiocron
import lichesspy.api
import interactions as di
from interactions.api.models.flags import Intents
import config as c
import function
import logging

# Build the bot according to the Discord syntax
bot = di.Client(token=c.bot_token, intents=Intents.ALL, disable_sync=False)
logging.basicConfig(filename=c.logdir + c.logfilename, level=c.logginglevel, format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')


TEAM_FILE = os.path.join(sys.path[0], "teams_to_check.json")

# Test function to see if the bot is online.
@bot.event
async def on_start():
    logging.info("Bot started!")


@bot.command(description="kick faulty user of a team. Authentification needed!")
@di.option(description="teamname to check")
@di.option(description="OAuth Code")
async def kickfaulty(ctx: di.CommandContext, teamname: str, oauth: str):
    team = function.check_team_name(teamname.lower())
    text = f"The data of the team **{team}** is downloaded and checked! This can take several " \
           f"minutes depending on the size of the team. Per 1000 members approx 1 minute!"
    await ctx.send(text, ephemeral=True)
    text, cheaters = await faultyhandle(ctx, team)
    await ctx.send(text, ephemeral=True, suppress_embeds=True)
    if cheaters:
        await run_kick(ctx, team, cheaters, oauth)


@bot.command(description="return a list with faulty user of a team")
@di.option(description="teamname to check")
async def faulty(ctx: di.CommandContext, team: str):
    text = f"The data of the team **{team}** is downloaded and checked! " \
            "This can take several minutes depending on the size of the team. " \
            "Per 1000 members approx 1 minute!"
    await ctx.send(text)
    text, cheaters = await faultyhandle(ctx, team)
    await ctx.send(text, suppress_embeds=True)
    

@bot.command(name="cron", description="Commands für den CronJob")
async def cron(ctx: di.CommandContext):
    pass

@cron.subcommand(name="add", description="add a team to cron list")
@di.option(description="team which should be checked daily")
@di.option(description="user who will be pinged")
async def crone_add(ctx: di.CommandContext, teamname: str, user: di.Member):
    logging.info(f'Team {teamname} for User {user.id}')
    with open(TEAM_FILE, 'r', encoding='utf-8') as json_file:
        json_data: dict[str, list[dict[str, list[str]]]] = json.load(json_file)
    teamnew = True
    for team in json_data['teams']:
        if team['teamname'] == teamname:
            if str(user.id) not in team['user']:
                team['user'].append(str(user.id))
            teamnew = False
            break
    if teamnew:
        json_data['teams'].append({
            'teamname': teamname,
            'user': [str(user.id)]
        })
    with open(TEAM_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file)
    text = f"Das Team {teamname} ist nun mit dem User mit dem User {user.mention} verknüpft."
    await ctx.send(text)


@cron.subcommand(name="get_cron_teams", description="get all teams which are checked daily")
async def cron_get(ctx: di.CommandContext):
    with open(TEAM_FILE, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for team in json_data['teams']:
        teamname = team['teamname']
        userlist = team['user']
        text = f'Das Team {teamname} ist mit diesen Usern verknüpft:\n'
        for user in userlist:
            text += f"<@{str(user)}>; "
        await ctx.send(text, allowed_mentions=None)


async def faultyhandle(ctx: di.CommandContext, team: str):
    try:
        loop = asyncio.get_event_loop()
        cheaters = await loop.run_in_executor(ThreadPoolExecutor(), function.analyse_team, team, c.ignore_user)
    except lichesspy.api.ApiHttpError:
        text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
               f"The queried team **{team}** apparently does not exist! \n" \
               f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
        return text, None
    if not cheaters:
        text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
               f"The queried team **{team}** does not include flagged users!\n" \
               f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - "
        await ctx.send(text)
        return text, None
    data = "\n".join([f"[{cheater}](https://lichess.org/@/{cheater})" for cheater in cheaters])
    text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\nIn the team **{team}**, " \
           f"following users were marked by Lichess as having violated the terms of use:\n" \
           f"{data}\n" \
           f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    return text, cheaters


async def run_kick(ctx: di.CommandContext, team: str, cheaters: list, token: str):
    logging.info(f"found {str(len(cheaters))} Cheater in Team {str(team)}")
    count_cheater = 0
    for cheater in cheaters:
        request = function.kick(team.lower(), cheater, token)
        logging.info(f"Request for Cheater {count_cheater + 1}. {cheater}: returns {request.text}")
        if not function.check(request):
            status = function.status(request)
            text = f"The kick process was cancelled due to the following error:\n**{status}**" \
                    "\nFor further information, please contact donbur#4156 on discord!" \
                    "\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
            logging.info(f"Request failed with {status}: ({request})")
            await ctx.send(text, ephemeral=True)
            break
        logging.info("with success")
        count_cheater += 1
    if count_cheater == 1:
        text = f"There was 1 of {str(len(cheaters))} flagged user kicked\n" \
                " - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    else:
        text = f"There were {count_cheater} of {len(cheaters)} flagged users kicked" \
                f"\n - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
    await ctx.send(text, ephemeral=True)


# Cronjob every day at 02:00 for every team in database
@aiocron.crontab('0 2 * * *')
async def cron_faulty():
    logging.info("start Crown")
    request_channel: di.Channel = await di.get(client=bot, obj=di.Channel, object_id=c.cron_channel)
    with open(TEAM_FILE, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for team in json_data['teams']:
        teamname = team['teamname']
        userlist = team['user']
        logging.info(f'Team "{teamname}" for {userlist}')
        try:
            loop = asyncio.get_event_loop()
            cheaters = await loop.run_in_executor(
                ThreadPoolExecutor(), function.analyse_team, 
                teamname, c.ignore_user)
        except lichesspy.api.ApiHttpError:
            logging.warn(f"Cron Request for Team {teamname} failed.")
            return False
        if cheaters:
            data = "\n".join([f"{cheater} https://lichess.org/@/{cheater}" for cheater in cheaters])
            logging.info(f'{str(len(cheaters))} cheater found in team "{teamname}": {cheaters}')
            user_mentions = ", ".join([f'<@{user}>' for user in userlist])
            text = f"- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
                f"{user_mentions}\nIn the team **{teamname}**, " \
                f"following users were marked by Lichess as having violated the terms of use:\n{data}\n" \
                f" - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
            msg = await request_channel.send(text)
            await msg.edit(suppress_embeds=True)
    logging.info("end Crown")


def create_teamlist():
    if not os.path.isfile(TEAM_FILE):
        with open(TEAM_FILE, 'w', encoding='utf-8') as jsonfile:
            data = {'teams': []}
            json.dump(data, jsonfile)


# Starting from the Await Client
if __name__ == "__main__":
    create_teamlist()
    bot.start()
