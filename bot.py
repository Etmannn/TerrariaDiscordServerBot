# Terraria Discord Bot by Ethan Cleminson | 22/12/2024

# Packages used in program
import discord
from discord.ext import commands
import subprocess
import yaml
import wmi

# Open and read config file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Set discord bot intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command("help")


# Pings server to check if its online
def serverping():
    f = wmi.WMI()

    flag = 0
    for process in f.Win32_Process():
        if "TerrariaServer.exe" == process.Name:
            flag = 1
            return True

    if flag == 0:
        return False

async def startserver(interaction: discord.Interaction):
    online = serverping()
    if online is True:
        await interaction.followup.send("Server already Online")
    else:
        await interaction.followup.send("Server is starting!")
        subprocess.Popen(f"cd {config['serverdir']} && start cmd.exe /c TerrariaServer.exe -config {config['configfile']}", shell=True)
        if config['playit'] == 'true':
            subprocess.call("TASKKILL /F /IM playit.exe")
            subprocess.Popen('start cmd.exe /c playit.exe', shell=True)
        checking = True
        while checking is True:
            checkstat = serverping()
            if checkstat is True:
                await interaction.followup.send("Server Online!")
                checking = False


async def stopserver(interaction: discord.Interaction):
    online = serverping()
    if online is True:
        subprocess.call("TASKKILL /IM TerrariaServer.exe /F /T")
        if config['playit'] == 'true':
            subprocess.call("TASKKILL /F /IM playit.exe")
        await interaction.followup.send("Server Offline")
    else:
        await interaction.followup.send("Sever already Offline")


# Prints a message and sets activitiy to the help command; triggers when the bot is online
@bot.event
async def on_ready():
    print("Bot successfully logged in")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name=f"/help"))
    await bot.tree.sync()


# A command to check if the server is online
@bot.tree.command(name="ping", description="Checks if the server is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Thinking...")
    online = serverping()
    if online is True:
        await interaction.followup.send("** Server is Online! **")
    if online is False:
        await interaction.followup.send("** Server is Offline **")


# A command to start the Terraria server
# If the server is already online it will inform the user
@bot.tree.command(name="start", description="Starts the Terraria server")
async def start(interaction: discord.Interaction):
    await interaction.response.send_message("Thinking...")
    await startserver(interaction=interaction)


# A command to stop the Terraria server
@bot.tree.command(name="stop", description="Stops the Terraria server")
async def stop(interaction: discord.Interaction):
    await interaction.response.send_message("Thinking...")
    await stopserver(interaction=interaction)


# A command to restart the Terraria server
@bot.tree.command(name="restart", description="Restarts the Terraria server")
async def restart(interaction: discord.Interaction):
    await interaction.response.send_message("Thinking...")
    online = serverping()
    if online is True:
        await stopserver(interaction=interaction)
        await startserver(interaction=interaction)
    else:
        await interaction.followup.send("Server Offline")


# Displays all the commands of the bot in a discord embed
@bot.tree.command(name="help", description="Lists all avaible commands")
async def help(interaction: discord.Interaction):
    helpembed = discord.Embed(title="Commands", color=0x55FF55)

    helpembed.add_field(name=f"/ping",
                        value="Returns whether or not the server is online",
                        inline=False)
    helpembed.add_field(name=f"/start",
                        value="Starts the Terraria server",
                        inline=False)
    helpembed.add_field(name=f"/stop",
                        value="Stops the Terraria server",
                        inline=False)
    helpembed.add_field(name=f"/restart",
                        value="Restarts the Terraria server",
                        inline=False)
    helpembed.add_field(name=f"/help",
                        value="Shows this help menu",
                        inline=False)

    await interaction.response.send_message(embed=helpembed)


# Runs the bot using the bot token
bot.run(config['token'])
