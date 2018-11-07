# r/jailbreak bot
# checks submission items for reports, downloads usernotes from /wiki/usernotes
# decompresses the ugly blob from there, modifies it with whatever the report
# was for the user, and saves it back.

# we'll need zlib, b64, and praw for this.
import praw
import zlib
import base64
import json
import time
from pytbun import *
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

r = praw.Reddit(client_id=config['UserNoteBot']['publicKey'],
    client_secret=config['UserNoteBot']['privateKey'],
    username=config['UserNoteBot']['username'],
    password=config['UserNoteBot']['password'],
    user_agent=config['UserNoteBot']['userAgent'])

sub = config['UserNoteBot']['subreddit']

processed = ""
              

def saveNewNote(user, note, mod, warn):
    return CompileandZipUsernotes(
        r,
        PullandUnzipUsernotes(r, sub)[0],
            makeNewNote(PullandUnzipUsernotes(r, sub)[1],user,note,getModeratorIndex(r,sub,mod),'',getWarningIndex(r,sub,warn)),
        "Monstercat")

# Workaround for streaming EVERYTHING from the sub
def submissions_and_comments(subreddit, **kwargs):
    results = []
    results.extend(subreddit.new(**kwargs))
    results.extend(subreddit.comments(**kwargs))
    results.sort(key=lambda post: post.created_utc, reverse=True)
    return results


if __name__ == "__main__":
    subreddit = r.subreddit(sub)
	# Suboptimal method of maintaining a "Stream"
    while True:
		# Checks items in 'reported' section of mod stuff
        for item in subreddit.mod.reports():
			# If there are mod reports && if ignore reports isn't set
            if (len(item.mod_reports)!=0 and item.ignore_reports==False):
                for report in item.mod_reports:
                    if (report[1]!='AutoModerator'):
                        # ignore automod reports for general sub modularity
                        # replace the above condition with true to not ignore AutoMod
                        print('just work pls')
                        print("Poster: {}".format(item.author.name))

                        # Mod Reports: [['!flag gooduser Good Contributor', 'Insxnity']]

                        if "!flag" in report[0]:
                            # the first two words are args, the rest is the usernote. this will seperate the args while maintaining the usernote
                            # 0 - !flag
                            # 1 - warning
                            # 2 - usernote
                            reportCMD = report[0].split(' ', 2)
                            reportInfo = [item.author.name,reportCMD[2],report[1],reportCMD[1]]
							# Lets not add 1000 of the same usernote
                            item.mod.ignore_reports()
                            print(saveNewNote(reportInfo[0],reportInfo[1],reportInfo[2],reportInfo[3]))
        time.sleep(30)
                            

