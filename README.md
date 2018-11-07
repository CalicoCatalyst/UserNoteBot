# UserNoteBot

Python bot using [PRAW](https://github.com/praw-dev/praw) to interact with [toolbox for reddit's](https://www.reddit.com/r/toolbox/) UserNote system, and more specifically, to allow saving of usernotes with custom reports

### Usage

As a moderator of a sub, report a submission/comment for "!flag <warning> <note>"  
  
  Warnings: "abusewarn","none","botban",null,"ban","gooduser","spamwatch","permban","spamwarn","shadow_ban","toxic","piracy"
  
  If the text isn't one of these the bot will get mad at you. 
  
This bot will only work if the user submitting a note has already submit one in the past. Make sure you do that. 

### Configuration

1. Open config.ini in a text editor
Open https://old.reddit.com/prefs/apps

2. Create an app if you haven't already

3. In config.ini, fill in the username, password, and public and private keys

4. In config.ini, enter the subreddit you would like the bot to monitor

5. Run jbbot.py

### PYTBUN.py

This class is a custom library I've coded specifically for handling UserNote modifications. It can be used seperately from jbbot.py in any project.
