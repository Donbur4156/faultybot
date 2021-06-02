# Faultybot
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=ffffff) ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?&logo=javascript&logoColor=000000) ![PHP](https://img.shields.io/badge/-PHP-BB4444?logo=PHP&logoColor=000000)

![VS Code](https://img.shields.io/badge/VSCode-%23007ACC?logo=Visual-studio-code) ![Pycharm](https://img.shields.io/badge/PyCharm-green?logo=PyCharm) 

![Git](https://img.shields.io/badge/-Git-%23F05032?logo=git&logoColor=%23ffffff)

<a href="https://github.com/jplight/faultybot">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username=jplight&repo=faultybot&theme=algolia" />
</a>


## Technical fundamentals
To use the bot you need a Discord bot and a Lichess account.
We recommend creating another new account for this purpose. The account is only important if you want to kick people. Otherwise you don't need a Lichess account.  The presence of Python is required.

### Create a Discord bot
Lichess bots can be created on the [Discord Developer](https://discord.com/developers/) page. Since this is a different topic, we recommend the video from freeCodeCamp. It is linked at the end of this text. Of course, the bot must also be invited to their server and be able to write there. But this is your responsibility.  [YouTube Video about Discord Bots](https://youtu.be/SPTfmiYiuok?t=3)

### Lichess Bot
If you decide to use a Lichess bot, you will need to generate an OAuth2 token or an API token. Actually it doesn't matter what rights it has. However, for the project at hand, it must have the right to act in the team.

```Log
team:write
```

## Installing the bot

### Clone git
You can download the git simply by using the command git clone. Please use the master branch

```GIT
git clone https://github.com/jplight/faultybot.git
```

### Pip install 
Actually, pip should already be there. If this is not the case, I will give a short instruction here. Simply copy the following commands into a shell or CMD. The instructions are only for Windows users. Linux and Mac users know everything better and therefore don't need them. 

```PowerShell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### Installation of the pip suspensions
This is also done with a simple console input. 
```PowerShell
pip install -r client\requirements.txt 
```
Please note that the requirements file is located in the subfolder client.

### Creating the Config File
Create a file named ftpdata.py in the subfolder client. Please use the syntax below and enter your values. You can obtain the FTP data from your website hoster. They are needed to transfer the cheater lists to the server.

```Python
# FTP 
user = "DATA"
pwd = "DATA"
port = "DATA"
url = "DATA"

# Lichess
bot_token = "DATA"
```

## Server Config
I assume at this point that you own a web server and know how to use it.

### Upload Files
Please upload the files from the Server folder to the Web Server.  PHP7 (, JavaScript and CSS as well as SCSS) are required there. However, this is by far not a special feature. I write the JS files here because there are hosters who reject these file formats. I am aware that CSS and JS are executed locally. 


### FTP scope
Create another FTP account. This should only have access to the flag folder. 
This data is important for the config file created earlier. The bot then creates a *.txt file and writes it to the server via FTP. This would otherwise be too much for the output.
That's about it. The bot automatically generates the links and then sends them to the user via a message.


## How to use the bot
To view all players who have violated the TOS, write the following in the chat with the bot.
The bot only searches for new cheaters every 4 hours after the last call. That would otherwise generate too much traffic. The flag "new" can be used to circumvent this.

```PowerShell
>faulty >>TEAM-ID<< 
```

However, if they want to kick players, write the following:

```PowerShell
>kickfaulty >>TEAM-ID<< >>TOKEN<< 
```

Please note that only one token can be uniquely assigned to a bot at a time. This bot must then also be TeamLeader in the desired team. This means that you cannot kick people all over the place. You can only do that in your teams.

## Have Fun
