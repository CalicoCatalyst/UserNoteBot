# UserNoteBot

Python bot using [PRAW](https://github.com/praw-dev/praw) to interact with [toolbox for reddit's](https://www.reddit.com/r/toolbox/) UserNote system, and more specifically, to allow saving of usernotes with custom reports

### Requirements

* PRAW Version 6.0.0  
* Program is python 2/3 compatible. 

### Running the bot

The bot has two "modes" it can run in. It can be told to run once and exit, or to run indefinitely with a default loop, or "check" time. This can also be set

The command line syntax is:

    python bot.py --watch [seconds]
    
    # To run once
    python bot.py
    
    # To run in a loop with default time of 30 seconds
    python bot.py --watch
    
    # To run in a loop, checking every two minutes instead
    python bot.py --watch 120

### Usage

As a moderator of a sub, report a submission/comment with the custom text:

    !flag <warning> <note>
  
Warnings:

Keyword | Usernote category
--- | ---
gooduser | Good Contributor
spamwatch | Spam Watch
spamwarn | Spam Warning
toxic | Warning	Toxic
piracy | Piracy
ban | Ban
permban | Permanent Ban
shadow_ban | Shadow Ban
null | No category

If the warning doesn't match one of the above, the bot will not work.

##### Note: The submitting moderator must have previously created a toolbox usernote through the desktop extension before the bot will work. 

### Bot Configuration

##### Note: Do not use quotation marks in config.ini. The program will not run properly if this is done.
1. Open config.ini in a text editor
Open https://old.reddit.com/prefs/apps

2. Create an app if you haven't already

3. In config.ini, fill in the username, password, and public and private keys

4. In config.ini, enter the subreddit you would like the bot to monitor

5. Run jbbot.py

### PYTBUN.py

This class is a custom library I've coded specifically for handling UserNote modifications. It can be used indepenently from jbbot.py in any project.
