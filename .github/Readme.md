# Faultybot
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=ffffff) 

![VS Code](https://img.shields.io/badge/VSCode-%23007ACC?logo=Visual-studio-code) ![Pycharm](https://img.shields.io/badge/PyCharm-green?logo=PyCharm) 

![Git](https://img.shields.io/badge/-Git-%23F05032?logo=git&logoColor=%23ffffff)


## Technical fundamentals
To use the bot, you need a Discord bot and a Lichess account. We recommend creating a new account specifically for this purpose. The account is only essential if you want to kick people; otherwise, you don't need a Lichess account. Python is a required dependency.


### Create a Discord bot
Lichess bots can be created on the [Discord Developer](https://discord.com/developers/) page. For details on creating Discord bots, you can refer to the video linked at the end of this part. Inviting the bot to your server and granting necessary permissions are your responsibilities. [YouTube Video about Discord Bots](https://youtu.be/SPTfmiYiuok?t=3)

### Lichess Bot
If you choose to use a Lichess bot, you'll need to generate an OAuth2 token or an API token. The specific permissions required for the project are as follows:

```bash
team:write
```

## Installing the bot

### Clone git
Download the repository using the git clone command. Make sure to use the master branch.

```bash
git clone https://github.com/Donbur4156/faultybot.git
```

### Install Dependencies with Pip

Pip should already be installed. If not, follow the instructions:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Install the required dependencies with:

```bash
pip install -r requirements.txt

```

### Creating the Config File
Create a file named ``ftpdata.py`` in the subfolder client and enter your values following the syntax below. FTP data is needed to transfer cheater lists to the server.



```Python
# FTP 
user = "DATA"
pwd = "DATA"
port = "DATA"
url = "DATA"

# Lichess
bot_token = "DATA"
```

## Usage
To view all players who have violated the Terms of Service (TOS), type the following in the chat with the bot. The bot only searches for new cheaters every 4 hours after the last call. The "new" flag can be used to circumvent this.

```bash
/faulty >>TEAM-ID<< 
```

To kick players, use the following:

```bash
/kickfaulty >>TEAM-ID<< >>TOKEN<< 
```

Note that only one token can be assigned to a bot at a time. The bot must also be a Team Leader in the desired team to kick players.
