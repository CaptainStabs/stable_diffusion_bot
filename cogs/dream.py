""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.0
"""

from mimetypes import init
from discord.ext import commands
from discord.ext.commands import Context
import discord

from helpers import checks
import json
import re
import requests
import aiohttp
import base64



# Here we name the cog and create a new class for the cog.
class Dream(commands.Cog, name="dream"):
    def __init__(self, bot):
        self.bot = bot
        self.pat = re.compile('''(?<="url": "\.\/outputs\/img-samples\/).*\.png(?=",)''')
        self.seed_pat = re.compile('''(?<="seed": )\d{10}(?=,)''')


    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(
        name="dream",
        description="Generate image from prompt",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    # @checks.is_owner()
    async def dream_command(self, context: Context, prompt: str, seed=-1, strength=0.75, cfgscale=7.5, initimg=None):
        message = prompt
        await context.defer()
        """
        Dream up an image

        :param context: The application command context.
        :param prompt: User input
        :param seed: generator seed
        :param strength: make stronk
        :param initimg: Either a file from the message, or a previously generated img
        """
        try:
            await context.reply(f"{context.author.mention} requested an image of: `{message}`")
        except:
            await context.channel.send(f"{context.author.mention} requested an image of: `{message}`")
        # await context.channel.send(f"{context.author.mention} requested an image of: `{message}`")


        # if initimg:
        #     
        # Do your stuff here

        if initimg:
            # Previously generated image
            initimg = initimg.strip()
            if len(initimg) == 20:
                img = open("F:\\stable-diffusion\\outputs\\img-samples\\bot\\" + initimg, "rb").read()
            
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

        payload = json.dumps({
        "prompt": f"{message}",
        "iterations": "1",
        "steps": "50",
        "cfgscale": f"{cfgscale}",
        "sampler": "k_lms",
        "width": "512",
        "height": "512",
        "seed": f"{seed}",
        "initimg": initimg,
        "strength": f"{strength}",
        "fit": "on",
        "gfpgan_strength": "0.8",
        "upscale_level": "",
        "upscale_strength": "0.75"
        })
        headers = {
        'host': '127.0.0.1',
        'content-type': 'application/json'
        }

        # async with aiohttp.ClientSession() as session:
        #     async with session.post("http://127.0.0.1:9090/#", data=payload, headers=headers) as r:
        #         # r = requests.request("POST", url, headers=headers, data=payload).text
        #         img_name = re.findall(self.pat, r)[0]
        #         img_path = "F:\\stable-diffusion\\outputs\\img-samples\\" + img_name
        #         print(img_path)
        #         # img_path = "F:\\stable-diffusion\\outputs\\img-samples\\000004.1291979794.png"
        #         await context.send(file=discord.File(img_path))

        url = "http://127.0.0.1:9090/#"

        r = requests.request("POST", url, headers=headers, data=payload).text
        print(r)
        r = json.loads(r)
        # img_name = re.findall(self.pat, r)[0]
        # try:
        #     seed_name = re.findall(self.seed_pat, r)[0]
        # except IndexError:
        #     seed_name = "IndexError"
        #     print(r)

        img_name = r["url"].split("/")[-1]
        seed_name = r["seed"]
        img_path = "F:\\stable-diffusion\\outputs\\img-samples\\bot\\" + img_name
        print(img_path)
        # await context.channel.send(f"Prompt: `{message}`    Seed: `{seed_name}`   Strength: `{strength}`   cfgscale: `{cfgscale}`   Filename: `{img_name}`", file=discord.File(img_path))
        await context.reply(f"Prompt: `{message}`    Seed: `{seed_name}`   Strength: `{strength}`   cfgscale: `{cfgscale}`   Filename: `{img_name}`", file=discord.File(img_path))

        # Don't forget to remove "pass", I added this just because there's no content in the method.
        # pass


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Dream(bot))
