# Stable Diffusion Discord Bot

<p align="center">
  <a href="//github.com/CaptainStabs/stable_diffusion_bot/releases"><img src="https://img.shields.io/github/v/release/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/CaptainStabs/stable_diffusion_bot/commits/main"><img src="https://img.shields.io/github/last-commit/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/CaptainStabs/stable_diffusion_bot/releases"><img src="https://img.shields.io/github/downloads/CaptainStabs/stable_diffusion_bot/total"></a>
  <a href="//github.com/CaptainStabs/stable_diffusion_bot/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/CaptainStabs/stable_diffusion_bot/"><img src="https://img.shields.io/github/languages/code-size/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/CaptainStabs/stable_diffusion_bot/issues"><img src="https://img.shields.io/github/issues-raw/kkrypt0nn/Python-Discord-Bot-Template"></a>
</p>

## How to add bot to server
Invite your bot on servers using the following invite: 
https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS ( Replace YOUR_APPLICATION_ID_HERE with the application ID and replace PERMISSIONS with the required permissions your bot needs that it can be get at the bottom of a this page https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot)

## How to set up

Here is an explanation of what everything is:

| Variable                  | Description                                                           |
| ------------------------- | ----------------------------------------------------------------------|
| YOUR_BOT_PREFIX_HERE      | The prefix you want to use for normal commands                        |
| YOUR_BOT_TOKEN_HERE       | The token of your bot                                                 |
| YOUR_BOT_PERMISSIONS_HERE | The permissions integer your bot needs when it gets invited           |
| YOUR_APPLICATION_ID_HERE  | The application ID of your bot                                        |
| OWNERS                    | The user ID of all the bot owners                                     |
| img_base_folder           | The path to where stable diffusion saves the images (if on windows ensure escaped backslashes) |
| server_url                | By default stable diffusion's web server will run on the provided IP+port, only change if you changed your settings |
| wait_time                 | How long the bot should wait for an image to generate, system dependent |


## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
pip install -r requirements.txt
```

If you have multiple versions of python installed (2.x and 3.x) then you will need to use the following command:

```
python3 bot.py
```

or eventually

```
python3.x bot.py
```
Replace `x` with the version of Python you have installed.

<br>

If you have just installed python today, then you just need to use the following command:

```
python bot.py
```

To start the stable diffusion web-server that the bot uses, in a seperate terminal (in the stable diffusion working directory) run:
```
python ./scripts/dream.py --web
```

You can run it with whatever other parameters you want (such as `-F`)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details
