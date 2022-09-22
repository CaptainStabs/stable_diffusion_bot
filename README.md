# Stable Diffusion Discord Bot

<p align="center">
  <a href="//github.com/kkrypt0nn/Python-Discord-Bot-Template/releases"><img src="https://img.shields.io/github/v/release/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/kkrypt0nn/Python-Discord-Bot-Template/commits/main"><img src="https://img.shields.io/github/last-commit/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/kkrypt0nn/Python-Discord-Bot-Template/releases"><img src="https://img.shields.io/github/downloads/kkrypt0nn/Python-Discord-Bot-Template/total"></a>
  <a href="//github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/kkrypt0nn/Python-Discord-Bot-Template"><img src="https://img.shields.io/github/languages/code-size/kkrypt0nn/Python-Discord-Bot-Template"></a>
  <a href="//github.com/kkrypt0nn/Python-Discord-Bot-Template/issues"><img src="https://img.shields.io/github/issues-raw/kkrypt0nn/Python-Discord-Bot-Template"></a>
</p>


## How to set up

Requires https://github.com/invoke-ai/InvokeAI.

Copy the `ldm` [folder](ldm) from this repo to your stable diffusion (InvokeAI) main folder and overwrite `server.py` with my version.

You must setup the [config.json](config.json) file.

Here is an explanation of what everything is:

| Variable                  | What it is                                                            |
| ------------------------- | ----------------------------------------------------------------------|
| YOUR_BOT_PREFIX_HERE      | The prefix you want to use for normal commands                        |
| YOUR_BOT_TOKEN_HERE       | The token of your bot                                                 |
| YOUR_BOT_PERMISSIONS_HERE | The permissions integer your bot needs when it gets invited           |
| YOUR_APPLICATION_ID_HERE  | The application ID of your bot                                        |
| OWNERS                    | The user ID of all the bot owners                                     |


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
