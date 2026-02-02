import discord
from discord import app_commands
from discord.ext import commands

from storage.sqlite import SQLiteStore
from markov.trainer import MarkovTrainer
from markov.generator import MarkovGenerator
from markov.filters import should_learn, sanitize_output


class MarkovCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Storage
        self.store = SQLiteStore()
        self.store.init_schema()

        # Markov components
        self.trainer = MarkovTrainer(self.store)
        self.generator = MarkovGenerator(self.store)

    # -----------------------------
    # Learning from messages
    # -----------------------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if not message.content:
            return

        if not should_learn(message.content):
            return

        self.trainer.train(message.content)

    # -----------------------------
    # Slash command: /markov
    # -----------------------------
    @app_commands.command(name="markov", description="Generate a Markov sentence")
    async def markov(self, interaction: discord.Interaction):
        text = self.generator.generate()

        if not text:
            await interaction.response.send_message(
                "I don’t know enough yet",
                ephemeral=True
            )
            return

        text = sanitize_output(text)
        if not text:
            await interaction.response.send_message(
                "That came out cursed, try again",
                ephemeral=True
            )
            return

        await interaction.response.send_message(text)


async def setup(bot: commands.Bot):
    await bot.add_cog(MarkovCog(bot))