# checks submission items for reports, downloads usernotes from /wiki/usernotes
# decompresses the ugly blob from there, modifies it with whatever the report
# was for the user, and saves it back.

# we'll need zlib, b64, and praw for this.
import praw
import zlib
import base64
import json
import time
import sys
from prawcore.exceptions import *
from pytbun import *
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

r = praw.Reddit(client_id=config['UserNoteBot']['publicKey'],
    client_secret=config['UserNoteBot']['privateKey'],
    username=config['UserNoteBot']['username'],
    password=config['UserNoteBot']['password'],
    user_agent=config['UserNoteBot']['userAgent'])
print(config['UserNoteBot']['username'])

sub = config['UserNoteBot']['subreddit']

# This is not direly important. Automod will trigger this bot only if a mod tells it to. 
ignore_automod = (config['UserNoteBot']['ignoreAutoMod'].lower() in ['true','t','yes','y'])

def parseint(string):
    return int(''.join([x for x in string if x.isdigit()]))    
        

watch_time = parseint(config['UserNoteBot']['defaultLoopTime'])
   

def saveNewNote(user, note, mod, warn):
    return CompileandZipUsernotes(
        r,
        PullandUnzipUsernotes(r, sub)[0],
            makeNewNote(PullandUnzipUsernotes(r, sub)[1],user,note,getModeratorIndex(r,sub,mod),'',getWarningIndex(r,sub,warn)),
        sub)

# Workaround for streaming EVERYTHING from the sub
def submissions_and_comments(subreddit, **kwargs):
    results = []
    results.extend(subreddit.new(**kwargs))
    results.extend(subreddit.comments(**kwargs))
    results.sort(key=lambda post: post.created_utc, reverse=True)
    return results

def check_reports_for_flags():
    subreddit = r.subreddit(sub)
    print(sub)
    try:
        print(r.user.me())
    except ResponseException:
        command_line_error_message("Basic Auth Failed with 401. Check Credentials",True,3)
    
    for item in subreddit.mod.reports():
        # If there are mod reports && if ignore reports isn't set
        if (len(item.mod_reports)!=0 and item.ignore_reports==False):
            for report in item.mod_reports:
                reporter = report[1]
                message  = report[0]
                if (not ignore_automod or reporter!='AutoModerator'):
                    # If reporter is not automod, or if automod is allowed

                    # Mod Reports: [['!flag gooduser Good Contributor', 'Insxnity']]

                    if "!flag" in message:

                        reportCMD = message.split(' ', 2)
                        
                        user = item.author.name
                        usernote = reportCMD[2]
                        warning = reportCMD[1]
                        
                        reportInfo = [user,usernote,reporter,warning]
                        # Lets not add 1000 of the same usernote
                        item.mod.ignore_reports()
                        saveNewNote(reportInfo[0],reportInfo[1],reportInfo[2],reportInfo[3])

def watch(t=watch_time):
    while True:
        check_reports_for_flags()
        time.sleep(t)
        

# This does not use python's option handler. We're working with two optional args, so why not make it verbose.  
def cla_handler(args):
    if (len(args)>=4):
        command_line_error_message("Correct Syntax: 'bot.py --watch [seconds]'",True,2)
    al = ['','single_job','default_watch','custom_watch']
    j = al[len(args)]
    
    if j == 'single_job':
        check_reports_for_flags()
        
    if j == 'default_watch':
        if args[1] == '--watch':
            watch()
        else:
            command_line_error_message("Correct Syntax: 'bot.py --watch [seconds]'",True,2)
    
    if j == 'custom_watch':
        if args[1] == '--watch':
            pass
        else:
            command_line_error_message("Correct Syntax: 'bot.py --watch [seconds]'",True,2)
        if args[2].isdigit():
             t = parseint(args[2])
             if t <= 3:
                command_line_error_message("Set looping time is smaller than the amount of time needed to process, which would create an infinite backlog. Use a time larger than at least 3, optimally 60 seconds or more",True,4)
             watch(t)
        else:
            command_line_error_message("Value [Seconds] Must be a whole, positive number.'",True,2)
        
    

def command_line_error_message(string, exit=True, ev=1):
    print("######################################################")
    print("Error encountered during exectuion of program:")
    print(string)
    print("######################################################")
    if exit:
        # 0 - successful exit
        # 1 - bad exit
        # 2 - syntax error on command line arguments
        # 3 - OAUTH initial attempt failed (if initial is successful, program will retry)
        # 4 - Loop time too small
        sys.exit(ev)
    
if __name__ == "__main__":
    cla_handler(sys.argv)
                            
