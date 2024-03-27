# Project Title

A short description about the project and/or client.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The things you need before installing the software.

* You need this
* And you need this
* Oh, and don't forget this

### Installation

A step by step guide that will tell you how to get the development environment up and running.

Windows:
```
$ git clone https://github.com/Nad-py/OwOBot
```
Edit the .env file using the template provided.

DISCORD_TOKEN - Discord token you use to run the bot.

BOT_OWNER_ID - Your discord ID, used to allow only you to use !sync.

GUILD_ID - ID of your discord server.

CUTE_ROLE_ID - ID of a role that is allowed to distribute points.

CUTE_CHANNEL - Channel to log point changes made by the cute role.

Set up and activate your virtual environment if you are using one:
```
$ cd OwOBot
$ python -m venv venv
$ venv\Scripts\activate
```
Note: Python version used is 3.9.16, i installed and used a separate Python interpreter, so I create my virtual environment like this:
```
D:\Python-3.9.16\PCbuild\amd64\python.exe -m venv venv
```

Install the required packages using the requirements.txt
```
$ pip install -r requirements.txt
```

And now it's ready to run! 
```
python bot.py
```

## Usage

A few examples of useful commands and/or tasks.

```
$ First example
$ Second example
$ And keep this in mind
```

## Deployment

Additional notes on how to deploy this on a live or release system. Explaining the most important branches, what pipelines they trigger and how to update the database (if anything special).

### Server

* Live:
* Release:
* Development:

### Branches

* Master:
* Feature:
* Bugfix:
* etc...

## Additional Documentation and Acknowledgments

* Project folder on server:
* Confluence link:
* Asana board:
* etc...
