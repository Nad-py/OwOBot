# OwOBot

OwOBot is a Discord bot with a primary focus on managing "cute points", with additional features such as "professions" that allow users to post and delete tasks.

### Prerequisites

The things you need before installing the software.

* Python 3.9.16
* Git

### Installation


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

### /cute_give
![/cute_give](https://github.com/Nad-py/OwOBot/assets/84136430/ef5c7345-9073-4094-a104-37b025ba8b72)

![/cute_give output](https://github.com/Nad-py/OwOBot/assets/84136430/227964ad-0370-4662-96d7-40e671f6630b)

### /cute_leaderboard
![/cute_leaderboard](https://github.com/Nad-py/OwOBot/assets/84136430/65d5e436-ad4c-4284-8e99-f40cea8b5612)

### /cute_points
![/cute_points](https://github.com/Nad-py/OwOBot/assets/84136430/a01b1b30-baf4-409f-aac7-1b2dc27730fa)

### /profession
![/profession](https://github.com/Nad-py/OwOBot/assets/84136430/9ec515a9-bf0b-4e3a-8a32-6bc28a55f06c)

![/profession output](https://github.com/Nad-py/OwOBot/assets/84136430/e740a7c1-489b-4b0e-aebe-2a654dd3a336)

### Logging for /cute_give
![/cute_give logging](https://github.com/Nad-py/OwOBot/assets/84136430/14e6f7f1-76ca-4781-b28c-2a9b15343aa4)
