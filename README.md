# UserNoteBot

Python bot using [PRAW](https://github.com/praw-dev/praw) to interact with [toolbox for reddit's](https://www.reddit.com/r/toolbox/) UserNote system, and more specifically, to allow saving of usernotes with custom reports

### Requirements

* PRAW Version 6.0.0  
* Program is python 2/3 compatible. 

### Running the bot

If you want the bot to run continuously, pass a loop time via `[-w <time>]`

Running `python bot.py -h` yields:

    usage: bot.py [-h] [-w WATCH] [-d]
                  [-c CREDENTIALS CREDENTIALS CREDENTIALS CREDENTIALS]

    Bot to check reports for mod initiated commands and create usernotes
    
    optional arguments:
      -h, --help            show this help message and exit
      -w WATCH, --watch WATCH
                            Specify a time for the bot to loop in seconds
      -d, --debug           Enable Debug Logging
      -c CREDENTIALS CREDENTIALS CREDENTIALS CREDENTIALS, --credentials CREDENTIALS CREDENTIALS CREDENTIALS CREDENTIALS
                            Specify oauth credentials on command line

##### -C flag

`-c` flag should only be used for testing/debug. Specify your oauth credentials in `oauth.ini`

if you insist on using -c to specify credentials via CLI, syntax is `-c public_key private_key username password`

If the program throws an IndexError, try wrapping these arguemnts in quotes like so:
`-c 'public_key' 'private_key' 'username' 'password'`

I would only reccomend using this flag if you know what you're doing
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
1. Open `oauth.ini` in a text editor
Open https://old.reddit.com/prefs/apps

2. Create an app if you haven't already

3. In config.ini, fill in the username, password, and public and private keys

4. In config.ini, enter the subreddit you would like the bot to monitor

5. Run `bot.py`
