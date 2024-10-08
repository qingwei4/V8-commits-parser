import discord
from discord.ext import commands
import asyncio
import sys
import os
import subprocess

# Add the parser directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'parser'))

class CommitNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.subscriptions = {}
        self.valid_keywords = [
            'maglev', 'wasm', 'source-phase-imports', 'interpreter', 'parser',
            'sandbox', 'ICs', 'turboshaft', 'base', 'Reland', 'Security',
            'promise', 'regexp'
        ]

    @commands.command(name='subscribe')
    async def subscribe_command(self, ctx, *args):
        user_id = ctx.author.id
        if user_id not in self.subscriptions:
            self.subscriptions[user_id] = set()

        if not args:
            self.subscriptions[user_id] = set()  # Empty set means all commits
            await ctx.send("You have subscribed to all new commits.")
            return

        keyword = args[0].lower()
        if keyword not in self.valid_keywords:
            await self.send_help_message(ctx)
            return

        self.subscriptions[user_id].add(keyword)
        await ctx.send(f"You have subscribed to commits containing '{keyword}'.")

    @commands.command(name='unsubscribe')
    async def unsubscribe_command(self, ctx):
        user_id = ctx.author.id
        if user_id in self.subscriptions:
            del self.subscriptions[user_id]
            await ctx.send("You have been unsubscribed from all commit notifications.")
        else:
            await ctx.send("You were not subscribed to any commit notifications.")

    async def send_help_message(self, ctx):
        help_message = (
            "Usage: !> subscribe [keyword]\n"
            "Valid keywords: " + ", ".join(self.valid_keywords) + "\n"
            "Example: !> subscribe maglev\n"
            "To receive all commits, use: !> subscribe\n"
            "To unsubscribe from all notifications, use: !> unsubscribe"
        )
        await ctx.send(help_message)

    @commands.command(name='add_keyword')
    @commands.has_permissions(administrator=True)
    async def add_keyword(self, ctx, keyword):
        keyword = keyword.lower()
        if keyword not in self.valid_keywords:
            self.valid_keywords.append(keyword)
            await ctx.send(f"Added '{keyword}' to the list of valid keywords.")
        else:
            await ctx.send(f"'{keyword}' is already in the list of valid keywords.")

    async def check_commits(self):
        while True:
            process = subprocess.Popen(
                ["python", "parser/main.py", "--no-log"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    if "New commit found" in output:
                        commit_info = process.stdout.readline().strip()
                        await self.notify_subscribers(commit_info)
            
            await asyncio.sleep(60)  # Wait for 60 seconds before checking again

    async def notify_subscribers(self, commit_info):
        for user_id, keywords in self.subscriptions.items():
            if not keywords or any(keyword.lower() in commit_info.lower() for keyword in keywords):
                user = await self.bot.fetch_user(user_id)
                if user:
                    await user.send(f"New commit: {commit_info}")

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!> ', intents=intents)

    async def setup_hook(self):
        await self.add_cog(CommitNotifier(self))
        self.loop.create_task(self.get_cog('CommitNotifier').check_commits())

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f"Valid keywords: {', '.join(self.get_cog('CommitNotifier').valid_keywords)}")

def run_bot():
    bot = MyBot()
    with open('discord_token', 'r') as token_file:
        token = token_file.read().strip()
    bot.run(token)

if __name__ == '__main__':
    run_bot()