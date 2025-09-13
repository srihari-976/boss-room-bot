import discord
from discord.ext import commands
import subprocess
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# --- Code Execution Command ---
@bot.command()
async def run(ctx, lang, *, code):
    """Run code in Python, C++, or JavaScript"""
    
    filename = ""
    command = []
    
    if lang.lower() == "python":
        filename = "temp.py"
        command = ["python", filename]
    elif lang.lower() in ["cpp", "c++"]:
        filename = "temp.cpp"
        command = ["g++", filename, "-o", "temp.out", "&&", "./temp.out"]
    elif lang.lower() in ["js", "javascript"]:
        filename = "temp.js"
        command = ["node", filename]
    else:
        await ctx.send("❌ Supported languages: python, cpp, js")
        return
    
    # Save code to temp file
    with open(filename, "w") as f:
        f.write(code)
    
    try:
        # Run code safely with subprocess
        result = subprocess.run(" ".join(command), shell=True, capture_output=True, text=True, timeout=5)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        output = str(e)
    
    # Send output in Discord
    await ctx.send(f"```{output}```")

# ✅ Run the bot with environment variable
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
