""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.0
"""

from mimetypes import init
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

import discord

from helpers import checks
import json
import re
import requests
import urllib3
import aiohttp
import base64
import asyncio
from typing import List


import socketio
import time
import queue


# Here we name the cog and create a new class for the cog.
class Models(commands.Cog, name="models"):
    def __init__(self, bot):
        self.bot = bot

        self.server_url = bot.config["server_url"]

        # Create socket client and connect to server
        self.sio = socketio.Client()
        self.sio.connect(self.server_url)

        self.models = queue.Queue()

    def get_models(self, socket_event):
        if socket_event:
            self.models.put(socket_event)


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(
        name="models",
        description="List available models",
    )

    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()

    async def models_command(self, context: Context):
        await context.defer()
        self.sio.emit("requestSystemConfig")
        self.sio.on("systemConfig", self.get_models)
        models = self.models.get()
        print(models)
        if models:
            models = models["model_list"]
            sorted_models = sorted(models.items(), key=lambda x: (x[1]["status"] != "active", x[1]["status"] != "cached"))
            new_msg = '**{} models available**\n:green_circle: = Active :orange_circle: = Previously loaded (Cached) :red_circle: = unloaded\n'.format(len(models))

            for m in sorted_models:
                if m[1]["status"] == "not loaded":
                    new_msg += ":red_circle:"
                elif m[1]["status"] == "cached":
                    new_msg += ":orange_circle:"
                elif m[1]["status"] == "active":
                    new_msg += ":green_circle:"
                new_msg += "`{}`".format(m[0])
                new_msg += m[1]["description"] + "\n"


            await context.reply(new_msg)



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Models(bot))
