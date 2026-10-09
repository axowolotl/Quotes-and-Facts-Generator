import os
import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

# Setup bot with default intents
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync slash commands with Discord global API
        await self.tree.sync()
        print("Slash commands synced globally.")

bot = Bot()

# Helper function to get random data from SQLite
def get_random_entry(table_name: str):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    # ORDER BY RANDOM() LIMIT 1 efficiently fetches a random row
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")

# /fact Command
@bot.tree.command(name="fact", description="Get a random interesting fact!")
async def fact(interaction: discord.Interaction):
    row = get_random_entry("facts")
    if row:
        fact_text = row[1]
        embed = discord.Embed(
            title="💡 Random Fact",
            description=fact_text,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("The facts database is currently empty!", ephemeral=True)

# /quote Command
@bot.tree.command(name="quote", description="Get a random inspirational quote!")
async def quote(interaction: discord.Interaction):
    row = get_random_entry("quotes")
    if row:
        quote_text, author = row[1], row[2]
        embed = discord.Embed(
            title="💬 Random Quote",
            description=f'"{quote_text}"',
            color=discord.Color.green()
        )
        embed.set_footer(text=f"— {author}")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("The quotes database is currently empty!", ephemeral=True)

# /add_quote Command (Allows users to submit custom quotes)
@bot.tree.command(name="add_quote", description="Add a new quote to the database.")
@app_commands.describe(text="The quote itself", author="Who said it")
async def add_quote(interaction: discord.Interaction, text: str, author: str):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quotes (content, author) VALUES (?, ?)", (text, author))
    conn.commit()
    conn.close()

    embed = discord.Embed(
        title="✅ Quote Added!",
        description=f'Successfully saved: "{text}" - {author}',
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

# /add_fact Command (Allows users to submit custom facts)
@bot.tree.command(name="add_fact", description="Add a new fact to the database.")
@app_commands.describe(text="The fact itself")
async def add_fact(interaction: discord.Interaction, text: str):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO facts (content) VALUES (?)", (text,))
    conn.commit()
    conn.close()

    embed = discord.Embed(
        title="✅ Fact Added!",
        description=f'Successfully saved: "{text}"',
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

# /remove_quote Command (Allows users to remove a quote by ID)
@bot.tree.command(name="remove_quote", description="Remove a quote from the database by its ID.")
@app_commands.describe(quote_id="The ID of the quote to remove")
async def remove_quote(interaction: discord.Interaction, quote_id: int):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    if cursor.rowcount > 0:
        conn.commit()
        response = f"✅ Quote with ID {quote_id} has been removed."
    else:
        response = f"❌ No quote found with ID {quote_id}."
    conn.close()
    await interaction.response.send_message(response)

# /remove_fact Command (Allows users to remove a fact by ID)
@bot.tree.command(name="remove_fact", description="Remove a fact from the database by its ID.")
@app_commands.describe(fact_id="The ID of the fact to remove")
async def remove_fact(interaction: discord.Interaction, fact_id: int):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM facts WHERE id = ?", (fact_id,))
    if cursor.rowcount > 0:
        conn.commit()
        response = f"✅ Fact with ID {fact_id} has been removed."
    else:
        response = f"❌ No fact found with ID {fact_id}."
    conn.close()
    await interaction.response.send_message(response)

# /help Command (Provides a list of available commands)
@bot.tree.command(name="help", description="List all available commands.")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Available Commands",
        description="Here are the commands you can use:",
        color=discord.Color.blue()
    )
    embed.add_field(name="/add_quote", value="Add a new quote to the database.", inline=False)
    embed.add_field(name="/add_fact", value="Add a new fact to the database.", inline=False)
    embed.add_field(name="/remove_quote", value="Remove a quote from the database by its ID.", inline=False)
    embed.add_field(name="/remove_fact", value="Remove a fact from the database by its ID.", inline=False)
    embed.add_field(name="/help", value="Show this help message.", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run("your_discord_bot_token_here")  # Replace with your actual bot token