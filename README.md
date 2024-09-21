# stenographer

A discord bot to export channel messages into a CSV for backups.

## Setup

Follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) on creating a Discord bot application on the dev portal.

## Local development

Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer):

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

Then clone this repository:

```shell
git clone git@github.com:bitjockey42/stenographer.git
```

Create a `.env` file and set these values:

```
DISCORD_BOT_TOKEN=
DISCORD_BOT_ID=
``` 

You can find the value of `DISCORD_BOT_TOKEN` from the Discord dev portal page for your bot application under "Bot". 

`DISCORD_BOT_ID` can be found under OAuth2 -> Client information -> CLIENT ID.

Then install the dependencies:

```shell
poetry install
```

To start the bot:

```shell
poetry run stenographer start
```

Invite the bot to your Discord server using the link that's displayed in the server log, something like:

https://discordapp.com/oauth2/authorize?client_id=DISCORD_CLIENT_ID&scope=bot

## Dokku deploy

On the dokku host:

```shell
dokku apps:create stenographer
dokku config:set stenographer DISCORD_BOT_TOKEN=<bot token from Discord dev portal>
dokku config:set stenographer DISCORD_BOT_ID=<bot client id>
```

On your computer, where `example.test` is the hostname of your dokku host (e.g. `dokku.me`):

```shell
git remote add dokku dokku@example.test:stenographer
```

This will deploy the bot to your dokku instance.
