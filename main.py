import discord
from discord.ext import commands, tasks
import random
import asyncio
import os
from dotenv import load_dotenv

# Snatch env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Wrestle Intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# Wake up the ghost
class PeekabooBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='p!', intents=intents, help_command=None)
        self.peekaboo_running = False

bot = PeekabooBot()

# Track scores
scores = {}

# Track Messages
current_channel_id = None
current_message_id = None

# Take a Selfie
GHOST_IMAGE_URL = "https://files.catbox.moe/3d56fj.jpg"

@bot.event
async def on_ready():
    print(f'{bot.user} is back from the dead!')

@tasks.loop(minutes=2)
async def peekaboo_loop():
    global current_channel_id, current_message_id

    # Delete the previous message if it exists
    if current_channel_id and current_message_id:
        try:
            channel = bot.get_channel(current_channel_id)
            if channel:
                try:
                    message = await channel.fetch_message(current_message_id)
                    await message.delete()
                    print(f"Deleted message: {current_message_id}")
                except discord.NotFound:
                    print(f"Message {current_message_id} was already deleted.")
                except discord.Forbidden:
                    print(f"No permission to delete message {current_message_id}")
                except discord.HTTPException as e:
                    print(f"Failed to delete message {current_message_id}: {e}")
            else:
                print(f"Channel {current_channel_id} no longer exists.")
        except Exception as e:
            print(f"Error handling previous message: {e}")

    # Snoop channels
    suitable_channels = [
        channel for channel in bot.get_all_channels()
        if isinstance(channel, discord.TextChannel)
        and channel.permissions_for(channel.guild.me).send_messages
        and channel.permissions_for(channel.guild.me).read_messages
        and not channel.is_nsfw()
    ]

    if not suitable_channels:
        print("No suitable channels found to send Peekaboo message.")
        return

    # Pick a random one
    channel = random.choice(suitable_channels)

    # Peekaboo
    embed = discord.Embed(title="Peekaboo!", color=0x2F3136)
    embed.set_thumbnail(url=GHOST_IMAGE_URL)
    embed.description = "React with any emoji to earn a point!"
    embed.set_footer(text="p!leaderboard for scores")

    new_message = await channel.send(embed=embed)
    current_channel_id = channel.id
    current_message_id = new_message.id
    print(f"Sent new message: {current_message_id} in channel: {channel.name}")

    # Sit back and chill
    await asyncio.sleep(115)  # Wait for 1 minute and 55 seconds

    # Check for reactions
    try:
        message = await channel.fetch_message(current_message_id)

        # Update score (only 1 point per user)
        reacted_users = set()
        for reaction in message.reactions:
            async for user in reaction.users():
                if user != bot.user and user.id not in reacted_users:
                    scores[user.id] = scores.get(user.id, 0) + 1
                    reacted_users.add(user.id)
    except discord.NotFound:
        print(f"Message {current_message_id} was deleted before processing reactions.")
    except discord.Forbidden:
        print(f"No permission to fetch or modify message {current_message_id}")
    except discord.HTTPException as e:
        print(f"Failed to process message {current_message_id}: {e}")

@bot.command(name="start", description="Start the Peekaboo game")
@commands.has_permissions(administrator=True)
async def start_peekaboo(ctx):
    if not bot.peekaboo_running:
        peekaboo_loop.start()
        bot.peekaboo_running = True
        await ctx.send("Peekaboo game has begun")
    else:
        await ctx.send("Peekaboo game is already running.")

@bot.command(name="stop", description="End the Peekaboo game")
@commands.has_permissions(administrator=True)
async def stop_peekaboo(ctx):
    if bot.peekaboo_running:
        peekaboo_loop.stop()
        bot.peekaboo_running = False
        await ctx.send("Peekaboo game has been stopped.")
    else:
        await ctx.send("Peekaboo game is not currently running.")

@bot.command(name="leaderboard", description="Show the Peekaboo leaderboard")
async def show_leaderboard(ctx):
    await send_leaderboard(ctx)

@bot.command(name="adminboard", description="Show detailed Peekaboo leaderboard (Admin only)")
@commands.has_permissions(administrator=True)
async def admin_leaderboard(ctx):
    await send_leaderboard(ctx, is_admin=True)

@bot.command(name="reset", description="Reset the Peekaboo leaderboard (Admin only)")
@commands.has_permissions(administrator=True)
async def reset_leaderboard(ctx):
    scores.clear()
    await ctx.send("Leaderboard has been reset by an administrator.")

async def send_leaderboard(ctx, is_admin=False):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(title="🏆 Peekaboo Leaderboard 🏆", color=0x2F3136)
    embed.set_thumbnail(url=bot.user.avatar.url)

    leaderboard_text = ""
    for i, (user_id, score) in enumerate(sorted_scores[:10], start=1):
        user = await bot.fetch_user(user_id)
        leaderboard_text += f"{i}. {user.name}: {score} points\n"

    embed.add_field(name="Top Players", value=leaderboard_text if leaderboard_text else "No scores yet!", inline=False)

    if is_admin:
        embed.add_field(name="Total Players", value=str(len(scores)), inline=True)
        embed.add_field(name="Total Points", value=str(sum(scores.values())), inline=True)

    embed.set_footer(text="React to Peekaboo messages to earn points!")

    await ctx.send(embed=embed)

@bot.command(name="help", description="Show the help menu")
async def help_command(ctx):
    embed = discord.Embed(title="Peekaboo Bot Help Menu", color=0x2F3136)
    embed.set_thumbnail(url=bot.user.avatar.url)

    commands_list = [
        ("p!start", "Start the Peekaboo game (Admin only)"),
        ("p!stop", "Stop the Peekaboo game (Admin only)"),
        ("p!leaderboard", "Show the Peekaboo leaderboard"),
        ("p!adminboard", "Show detailed Peekaboo leaderboard (Admin only)"),
        ("p!reset", "Reset the Peekaboo leaderboard (Admin only)"),
        ("p!help", "Show this help menu")
    ]

    for command, description in commands_list:
        embed.add_field(name=command, value=description, inline=False)

    embed.set_footer(text="The Peekaboo game sends ghost images to random channels. React to these messages with any emoji to earn points!")

    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)