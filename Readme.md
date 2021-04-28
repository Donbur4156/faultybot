# Faultybot

## Technical fundamentals
To use the bot you need a Discord bot and a Lichess account.
We recommend creating another new account for this purpose. The account is only important if you want to kick people. Otherwise you don't need a Lichess account.  The presence of Python is required.

### Create a Discord bot
Lichess bots can be created on the [Discord Developer](https://discord.com/developers/) page. Since this is a different topic, we recommend the video from freeCodeCamp. It is linked at the end of this text. Of course, the bot must also be invited to their server and be able to write there. But this is your responsibility.  [YouTube Video about Discord Bots](https://youtu.be/SPTfmiYiuok?t=3)

### Lichess Bot
If you decide to use a Lichess bot, you will need to generate an OAuth2 token or an API token. Actually it doesn't matter what rights it has. However, for the project at hand, it must have the right to act in the team.
```Lichess
team:write
```

## Installing the bot

### Pip install 
Actually, pip should already be there. If this is not the case, I will give a short instruction here. Simply copy the following commands into a shell or CMD. The instructions are only for Windows users. Linux and Mac users know everything better and therefore don't need them. 

```PowerShell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### 