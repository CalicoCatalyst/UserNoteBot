# UserNoteBot

Python bot using [PRAW](https://github.com/praw-dev/praw) to interact with [toolbox for reddit's](https://www.reddit.com/r/toolbox/) UserNote system, and more specifically, to allow saving of usernotes with custom reports

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

**Notice**: The submitting moderator must have previously created a toolbox usernote through the desktop extension before the bot will work. 

### Bot Configuration

1. Open config.ini in a text editor
Open https://old.reddit.com/prefs/apps

2. Create an app if you haven't already

3. In config.ini, fill in the username, password, and public and private keys

4. In config.ini, enter the subreddit you would like the bot to monitor

5. Run jbbot.py

### PYTBUN.py

This class is a custom library I've coded specifically for handling UserNote modifications. It can be used indepenently from jbbot.py in any project.
