import discord
from discord.ext import commands

from BotCore import BOT_CONFIG
from WolfBot.WolfEmbed import Colors
import logging

import git

LOG = logging.getLogger("DiyBot/Plugin/" + __name__)

class BotAdmin:
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    async def on_ready(self):
        LOG.info("Enabled plugin!")
        
    
    @commands.command(name="version")
    async def version_cmd(self, ctx: discord.ext.commands.Context):
        repo = git.Repo(search_parent_directories = True)
        sha = repo.head.object.hexsha
    
        await ctx.send(embed=discord.Embed(
                title="DiyBot",
                description="This is DIYBot, a fork of the WolfBot core Discord bot platform. It is responsible for managing"
                + " and assisting the moderators on the DIY Tech subreddit.",
                color = Colors.INFO
            )
            .add_field(name="Authors", value="KazWolfe, Clover", inline=False)
            .add_field(name="Bot Version", value=sha[-8:], inline=True)
            .add_field(name="Library Version", value=discord.__version__, inline=True)
        )

    @commands.group(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def admin(self, ctx: discord.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(
                title="Bot Manager",
                description="The command you have requested is not available.",
                color = Colors.DANGER
            ))
            return

    @admin.command(name="reloadConfig")
    async def reloadConfig(self, ctx: discord.ext.commands.Context):
        BOT_CONFIG.load()
        LOG.info("Bot configuration reloaded.")
        await ctx.send(embed=discord.Embed(
            title="Bot Manager",
            description="The bot configuration has been reloaded.",
            color = Colors.INFO
        ))

    @admin.command(name="load")
    async def load(self, ctx: discord.ext.commands.Context, plugin_name: str):
        try:
            self.bot.load_extension(plugin_name)
        except (AttributeError, ImportError) as e:
            await ctx.send(embed=discord.Embed(
                title="Plugin Manager",
                description="The plugin `" + plugin_name + "` has failed to load. The following error is available:\n ```{}: {}```".format(type(e).__name__, str(e)),
                color = Colors.DANGER
            ))
            return
        LOG.info("Loaded plugin %s", plugin_name)
        await ctx.send(embed=discord.Embed(
            title="Plugin Manager",
            description="The plugin `" + plugin_name + "` has been loaded.",
            color = Colors.INFO
        ))

    @admin.command(name="unload")
    async def unload(self, ctx: discord.ext.commands.Context, plugin_name: str):
        if plugin_name == "BotAdmin":
            await ctx.send("ERROR: Can not unload BotAdmin! It is marked as a critical module.")
            return

        """Unloads an extension."""
        self.bot.unload_extension(plugin_name)
        LOG.info("Unloaded plugin %s", plugin_name)
        await ctx.send(embed=discord.Embed(
            title="Plugin Manager",
            description="The plugin `" + plugin_name + "` has been unloaded.",
            color = Colors.INFO
        ))

    @admin.command(name="reload")
    async def reload(self, ctx: discord.ext.commands.Context, plugin_name: str):
        self.bot.unload_extension(plugin_name)
        LOG.info("Unloaded plugin %s for reload.", plugin_name)
        try:
            self.bot.load_extension(plugin_name)
        except (AttributeError, ImportError) as e:
            await ctx.send(embed=discord.Embed(
                title="Plugin Manager",
                description="The plugin `" + plugin_name + "` has failed to reload. The following error is available:\n ```{}: {}```".format(type(e).__name__, str(e)),
                color = Colors.DANGER
            ))
            return
        LOG.info("Reloaded plugin %s", plugin_name)
        await ctx.send(embed=discord.Embed(
            title="Plugin Manager",
            description="The plugin `" + plugin_name + "` has been reloaded.",
            color = Colors.INFO
        ))

    @admin.command(name="enable")
    async def enable(self, ctx: discord.ext.commands.Context, plugin_name: str):
        config = BOT_CONFIG.get('plugins', [])

        if plugin_name in config:
            await ctx.send("Plugin {} is already enabled.".format(plugin_name))
            return

        try:
            self.bot.load_extension(plugin_name)
        except (AttributeError, ImportError) as e:
            await ctx.send(embed=discord.Embed(
                title="Plugin Manager",
                description="The plugin `" + plugin_name + "` has failed to enable. The following error is available:\n ```{}: {}```".format(type(e).__name__, str(e)),
                color = Colors.DANGER
            ))
            return
        LOG.info("Loaded plugin %s for enable", plugin_name)

        config.append(plugin_name)
        BOT_CONFIG.set('plugins', config)
        LOG.info("Enabled plugin %s", plugin_name)
        await ctx.send(embed=discord.Embed(
            title="Plugin Manager",
            description="The plugin `" + plugin_name + "` has been enabled and will run automatically.",
            color = Colors.SUCCESS
        ))

    @admin.command(name="disable")
    async def disable(self, ctx: discord.ext.commands.Context, plugin_name: str):
        if plugin_name == "BotAdmin":
            await ctx.send("ERROR: Can not disable BotAdmin! It is marked as a critical module.")
            return

        config = BOT_CONFIG.get('plugins', [])

        if plugin_name not in config:
            await ctx.send("Plugin {} is already disabled.".format(plugin_name))
            return

        self.bot.unload_extension(plugin_name)
        LOG.info("Unloaded plugin %s for disable", plugin_name)

        config.remove(plugin_name)
        BOT_CONFIG.set('plugins', config)
        LOG.info("Disabled plugin %s", plugin_name)
        await ctx.send(embed=discord.Embed(
            title="Plugin Manager",
            description="The plugin `" + plugin_name + "` has been disabled and will no longer run automatically.",
            color = Colors.WARNING
        ))


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(BotAdmin(bot))
