import asyncio
import json
import logging
import os
import os.path
import sys
from concurrent.futures import ThreadPoolExecutor

import config as c
import function
import interactions as di
import lichesspy.api
from interactions import (
    Intents,
    SlashContext,
    Task,
    TimeTrigger,
    listen,
    slash_command,
    slash_option,
)
from util.color import Colors
from util.decorator import teamname_option
from util.logger import create_logger

di_logger = create_logger(
    file_name=c.logdir + "interactions.log", log_name="interactions_logger"
)
bot_logger = create_logger(file_name=c.logdir + c.logfilename, log_name="bot_logger")

# Build the bot according to the Discord syntax
client = di.Client(token=c.bot_token, intents=Intents.ALL, logger=di_logger)

TEAM_FILE = os.path.join(sys.path[0], "teams_to_check.json")


# Test function to see if the bot is online.
@listen()
async def on_startup():
    bot_logger.info("Bot started!")
    cron_faulty.start()


@slash_command(description="kick faulty user of a team. Authentification needed!")
@teamname_option()
@slash_option(
    name="oauth", description="OAuth Code", opt_type=di.OptionType.STRING, required=True
)
async def kickfaulty(ctx: SlashContext, teamname: str, oauth: str):
    teamname = function.check_team_name(teamname.lower())
    text = (
        f"The data of the team **{teamname}** is downloaded and checked!\nThis can take several "
        f"minutes depending on the size of the team.\nPer 1000 members approx 1 minute!"
    )
    await ctx.send(embed=_embed(text), ephemeral=True)
    embed, cheaters = await faultyhandle(teamname)
    await ctx.send(embed=embed, ephemeral=True)
    if cheaters:
        await run_kick(ctx, teamname, cheaters, oauth)


@slash_command(description="return a list with faulty user of a team")
@teamname_option()
async def faulty(ctx: SlashContext, teamname: str):
    teamname = function.check_team_name(teamname.lower())
    text = (
        f"The data of the team **{teamname}** is downloaded and checked!\n"
        "This can take several minutes depending on the size of the team.\n"
        "Per 1000 members approx 1 minute!"
    )
    await ctx.send(embed=_embed(text, Colors.YELLOW))
    embed, cheaters = await faultyhandle(teamname)
    await ctx.send(embed=embed)


cron_cmds = di.SlashCommand(name="cron", description="Commands für den Cronjob")


@cron_cmds.subcommand(sub_cmd_name="add", sub_cmd_description="add a team to cron list")
@teamname_option()
@slash_option(
    name="user",
    description="user who will be pinged",
    opt_type=di.OptionType.USER,
    required=True,
)
async def crone_add(ctx: SlashContext, teamname: str, user: di.Member):
    teamname = function.check_team_name(teamname.lower())
    bot_logger.info(f"Team {teamname} for User {user.id}")
    with open(TEAM_FILE, "r", encoding="utf-8") as json_file:
        json_data: dict[str, list[dict[str, list[str]]]] = json.load(json_file)
    teamnew = True
    for team in json_data["teams"]:
        if team["teamname"] == teamname:
            if str(user.id) not in team["user"]:
                team["user"].append(str(user.id))
            teamnew = False
            break
    if teamnew:
        json_data["teams"].append({"teamname": teamname, "user": [str(user.id)]})
    with open(TEAM_FILE, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file)
    text = f"Das Team **{teamname}** ist nun mit dem User {user.mention} verknüpft."
    await ctx.send(embed=_embed(text))


@cron_cmds.subcommand(
    sub_cmd_name="get_cron_teams",
    sub_cmd_description="get all teams which are checked daily",
)
async def cron_get(ctx: SlashContext):
    with open(TEAM_FILE, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    text = ""
    for team in json_data["teams"]:
        teamname = team["teamname"]
        userlist = team["user"]
        text += f"\nDas Team **{teamname}** ist mit diesen Usern verknüpft:\n"
        for user in userlist:
            text += f"<@{str(user)}> "
    await ctx.send(embed=_embed(text, Colors.BLUE), allowed_mentions=None)


async def faultyhandle(team: str):
    try:
        loop = asyncio.get_event_loop()
        cheaters = await loop.run_in_executor(
            ThreadPoolExecutor(), function.analyse_team, team, c.ignore_user
        )
    except lichesspy.api.ApiHttpError:
        text = f"The queried team **{team}** apparently does not exist! \n"
        embed = _embed(text, Colors.RED)
        return embed, None
    if not cheaters:
        text = f"The queried team **{team}** does not include flagged users!\n"
        embed = _embed(text)
        return embed, None
    data = "\n".join(
        [f"[{cheater}](https://lichess.org/@/{cheater})" for cheater in cheaters]
    )
    text = (
        f"In the team **{team}**, "
        f"following users were marked by Lichess as having violated the terms of use:\n"
        f"{data}\n"
    )
    embed = _embed(text, Colors.ORANGE)
    return embed, cheaters


async def run_kick(ctx: SlashContext, team: str, cheaters: list, token: str):
    bot_logger.info(f"found {str(len(cheaters))} Cheater in Team {str(team)}")
    count_cheater = 0
    for cheater in cheaters:
        request = function.kick(team.lower(), cheater, token)
        bot_logger.info(
            f"Request for Cheater {count_cheater + 1}. {cheater}: returns {request.text}"
        )
        if not function.check(request):
            status = function.status(request)
            text = (
                f"The kick process was cancelled due to the following error:\n**{status}**"
                "\nFor further information, please contact donbur#4156 on discord!"
            )
            bot_logger.info(f"Request failed with {status}: ({request})")
            await ctx.send(embed=_embed(text, Colors.RED), ephemeral=True)
            break
        bot_logger.info("with success")
        count_cheater += 1
    if count_cheater == 1:
        text = f"There was 1 of {str(len(cheaters))} flagged user kicked\n"
    else:
        text = f"There were {count_cheater} of {len(cheaters)} flagged users kicked"
    await ctx.send(embed=_embed(text), ephemeral=True)


# Cronjob every day at 02:00 for every team in database
@Task.create(TimeTrigger(hour=2, utc=False))
async def cron_faulty():
    bot_logger.info("start Crown")
    request_channel = await client.fetch_channel(channel_id=c.cron_channel)
    with open(TEAM_FILE, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    for team in json_data["teams"]:
        teamname = team["teamname"]
        userlist = team["user"]
        bot_logger.info(f'Team "{teamname}" for {userlist}')
        try:
            loop = asyncio.get_event_loop()
            cheaters = await loop.run_in_executor(
                ThreadPoolExecutor(), function.analyse_team, teamname, c.ignore_user
            )
        except lichesspy.api.ApiHttpError:
            bot_logger.warn(f"Cron Request for Team {teamname} failed.")
            return False
        if cheaters:
            data = "\n".join(
                [
                    f"[{cheater}](https://lichess.org/@/{cheater})"
                    for cheater in cheaters
                ]
            )
            bot_logger.info(
                f'{str(len(cheaters))} cheater found in team "{teamname}": {cheaters}'
            )
            user_mentions = ", ".join([f"<@{user}>" for user in userlist])
            text = (
                f"In the team **{teamname}**, "
                f"following users were marked by Lichess as having violated the terms of use:\n{data}\n"
            )
            await request_channel.send(
                content=user_mentions, embed=_embed(text, Colors.ORANGE)
            )
    bot_logger.info("end Crown")


def create_teamlist():
    if not os.path.isfile(TEAM_FILE):
        with open(TEAM_FILE, "w", encoding="utf-8") as jsonfile:
            data = {"teams": []}
            json.dump(data, jsonfile)


def _embed(text, color=Colors.GREEN):
    return di.Embed(description=text, color=color)


# Starting from the Await Client
if __name__ == "__main__":
    create_teamlist()
    client.start()
