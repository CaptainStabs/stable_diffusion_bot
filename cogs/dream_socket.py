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
class Dream(commands.Cog, name="dream"):
    def __init__(self, bot):
        self.bot = bot

        # Load cog-specific configs
        self.img_base_folder = bot.config["img_base_folder"]
        self.server_url = bot.config["server_url"]

        # Create socket client and connect to server
        self.sio = socketio.Client()
        self.sio.connect(self.server_url)

        # Queues
        # Workaround to get data from  get_generation_result (which is called by socketio.on)
        self.result_queue = queue.Queue()
        self.job_queue = queue.Queue()

    def generate_image(self, generation_params):
        self.sio.emit("generateImage", (generation_params, False, False))

        t_end = time.time() + 60
        while time.time() < t_end:
            # wait for the server to generate the image
            self.sio.on("generationResult", self.get_generation_result)
            # Have to get the result from get_generation_result from a queue
            # because sio.on does not have a return value
            response = self.result_queue.get(block=True, timeout=60)
            return response

    def get_generation_result(self, socket_event):
        if socket_event:
            self.result_queue.put(socket_event)

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(
        name="dream",
        description="Generate image from prompt",
    )

    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()

    # This will only allow owners of the bot to execute the command -> config.json
    # @checks.is_owner()


    @app_commands.describe(
        prompt="Prompt for image generation",
        seed="Seed for image, default is current epoch time",
        strength="Amount of noise that is added to input image",
        cfgscale="Adjust how much the image looks like the prompt and/or initimg",
        initimg="Initial image to use",
        steps="Number of steps to take to generate, must be < 50 (default 50)",
        sampler="Which sampler to use for image generation, default is kmls",
        width="Width of generated image, default 512",
        height="Height of generated image, default 512",
    )

    # @app_commands.command(name="dream", description="Generate image from prompt")
    @app_commands.choices(sampler=[
        app_commands.Choice(name="DDIM", value="ddim"),
        app_commands.Choice(name="PLMS", value="plms"),
        app_commands.Choice(name="KDPM_2", value="k_dpm_2"),
        app_commands.Choice(name="KDPM_2A", value="k_dpm_2_a"),
        app_commands.Choice(name="KEULER", value="k_euler"),
        app_commands.Choice(name="KEULER_A", value="k_euler_a"),
        app_commands.Choice(name="KHEUN", value="k_heun"),
        app_commands.Choice(name="DPMPP_2", value="dpmpp_2"),
        app_commands.Choice(name="K_DPMPP_2", value="k_dpmpp_2"),
    ])

    @app_commands.choices(width=[
        app_commands.Choice(name="64", value=64),
        app_commands.Choice(name="128", value=128),
        app_commands.Choice(name="192", value=192),
        app_commands.Choice(name="256", value=256),
        app_commands.Choice(name="320", value=320),
        app_commands.Choice(name="384", value=384),
        app_commands.Choice(name="448", value=448),
        app_commands.Choice(name="512", value=512),
        app_commands.Choice(name="576", value=576),
        app_commands.Choice(name="640", value=640),
        app_commands.Choice(name="704", value=704),
        app_commands.Choice(name="768", value=768),
        app_commands.Choice(name="832", value=832),
    ])

    @app_commands.choices(height=[
        app_commands.Choice(name="64", value=64),
        app_commands.Choice(name="128", value=128),
        app_commands.Choice(name="192", value=192),
        app_commands.Choice(name="256", value=256),
        app_commands.Choice(name="320", value=320),
        app_commands.Choice(name="384", value=384),
        app_commands.Choice(name="448", value=448),
        app_commands.Choice(name="512", value=512),
        app_commands.Choice(name="576", value=576),
        app_commands.Choice(name="640", value=640),
        app_commands.Choice(name="704", value=704),
        app_commands.Choice(name="768", value=768),
        app_commands.Choice(name="832", value=832),
    ])

    async def dream_command(self, context: Context, prompt: str, seed: int =-1, strength: float=0.75, cfgscale: float=7.5, initimg: str=None, steps: int=50, sampler: app_commands.Choice[str]=None, width: app_commands.Choice[int]=512, height: app_commands.Choice[int]=512):
        await context.defer()
        job_queue = queue.Queue()
        if context.channel.is_nsfw():
            """
            Dream up an image

            :param context: The application command context.
            :param prompt: User input
            :param seed: generator seed
            :param strength: make stronk
            :param initimg: Either a file from the message, or a previously generated img
            """
            if initimg and strength > 1:
                await context.reply("**ERROR:** Strength must be between 0.0 and 1.0")

            # if steps > 50 or steps < 1:
            if steps > 500 or steps < 1:
                await context.reply("**ERROR:** Steps must be between 1 and 50")

            try:
                await context.reply(f"{context.author.mention} requested an image of: `{prompt}`")
            except:
                # Sometimes the above fails, causing the bot to reply with an error, this fixes that
                await context.channel.send(f"{context.author.mention} requested an image of: `{prompt}`")

            if initimg:
                # Previously generated image
                initimg = initimg.strip()
                # Not really sure how to replace this with regex, the middle part of the string is a base64 encoded string
                # the first 8 characters of a UUID4
                if len(initimg) == 29:
                    img = open(self.img_base_folder + initimg, "rb").read()

                # Prevent non-images from being downloaded, stupid implementation, but I mostly trust the people using the bot
                elif ".png" or ".jpg" in initimg:
                    try:
                        img = requests.get(initimg).content
                    except:
                        await context.channel.send("The URL you provided did not return an image")
                        raise


                img_type = initimg[-3:]
                if img_type == "peg":
                    img_type = "jpeg"

                initimg = f"data:image/{img_type};base64,{str(base64.b64encode(img).decode('utf-8'))}"

            if not sampler:
                sampler = "k_lms"
            else:
                sampler = sampler.value

            generation_parameters = {
             'prompt': f"{prompt}",
             'iterations': 1,
             'steps': steps,
             'cfg_scale': cfgscale,
             'threshold': 0,
             'perlin': 0,
             'height': height.value if not type(height) is int else height,
             'width': width.value if not type(width) is int else width,
             'sampler_name': f"{sampler}",
             'seed': seed,
             'progress_images': False,
             'progress_latents': False,
             'save_intermediates': 5,
             'generation_mode': 'txt2img',
             'init_mask': '',
             'seamless': False,
             'hires_fix': True,
             'strength': strength,
             'variation_amount': 0
             }

            job_queue.put(self.generate_image(generation_parameters))

            r = job_queue.get(block=True, timeout=60)
            # print(r)
            if r:
                img_name = r["url"].split("/")[-1]
                seed_name = r["metadata"]["image"]["seed"]
                img_path = self.img_base_folder + img_name
                print(img_path)
                # await context.channel.send(f"Prompt: `{prompt}`    Seed: `{seed_name}`   Strength: `{strength}`   cfgscale: `{cfgscale}`   Filename: `{img_name}`", file=discord.File(img_path))
                await context.reply(f"Prompt: `{prompt}`    Seed: `{seed_name}`   Strength: `{strength}`   cfgscale: `{cfgscale}`   Steps: `{steps}`   Sampler: `{sampler}`   Filename: `{img_name}`", file=discord.File(img_path))

            else:
                await context.reply("SD backend is offline, please try again later")

        else:
            await context.reply("This command must be used in an NSFW channel.")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Dream(bot))
