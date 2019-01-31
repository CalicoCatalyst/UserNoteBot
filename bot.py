# checks submission items for reports, downloads usernotes from /wiki/usernotes
# decompresses the ugly blob from there, modifies it with whatever the report
# was for the user, and saves it back.

import argparse
import base64
import configparser
import json
import logging
import socket
import time
import zlib

# we'll need zlib, b64, and praw for this.
import praw
from prawcore.exceptions import *

config_file = 'oauth.ini'

config = configparser.ConfigParser()
config.read(config_file)

r = praw.Reddit(client_id=config['RedditAuth']['publicKey'],
                client_secret=config['RedditAuth']['privateKey'],
                username=config['RedditAuth']['username'],
                password=config['RedditAuth']['password'],
                user_agent='Mod Toolbox Usernote Modification Bot')
print(config['RedditAuth']['username'])

sub = "jailbreak"


def save_new_note(user, note, mod, warn):
    return UserNoteHandler.compile_and_zip_usernotes(
        r,
        UserNoteHandler.pull_and_unzip_usernotes(r, sub)[0],
        UserNoteHandler.make_new_note(UserNoteHandler.pull_and_unzip_usernotes(r, sub)[1], user, note,
                                      UserNoteHandler.get_moderator_index(r, sub, mod), '',
                                      UserNoteHandler.get_warning_index(r, sub, warn)),
        sub)


def check_reports_for_flags():
    subreddit = r.subreddit(sub)
    logging.debug('Subreddit program is configured to scan: %s' % sub)
    logging.debug('Value returned by r.user.me(): %s' % r.user.me())

    if r.user.me() is None:
        # test internet connection first
        try:
            logging.debug("Username is None. Checking whether internet works by pinging google DNS servers")
            socket.setdefaulttimeout(10)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
            logging.debug("Looks like we can access google DNS servers. Either reddit is down or oauth credentials "
                          "are bad / nonexistent")
        except OSError:
            logging.critical("It appears that you dont have internet connection. Please check your netowrk settings. "
                             "Exiting. ")
            exit(1)

        logging.critical("Authentication Failed. Please verifiy contents of %s. Exiting" % config_file)
        exit(1)
    try:
        # We have to simulate the later function as praw will not check if the list contains anything until it needs to
        for _ in subreddit.mod.reports():
            pass
    except ResponseException:
        logging.critical("Authenticated Account does not have permission to view reports in /r/%s. Exiting" % sub)
        exit(1)

    for item in subreddit.mod.reports():
        # If there are mod reports && if ignore reports isn't set
        if len(item.mod_reports) != 0 and item.ignore_reports is False:
            for report in item.mod_reports:
                reporter = report[1]
                message = report[0]
                if "!flag" in message:
                    # Mod Reports: [['!flag gooduser Good Contributor', 'Insxnity']]

                    if "!flag" in message:

                        report_cmd = message.split(' ', 2)

                        user = item.author.name
                        usernote = report_cmd[2]
                        warning = report_cmd[1]

                        # No warning handling
                        null_location = 3

                        if UserNoteHandler.get_warning_index(r, sub, warning) == null_location:
                            report_cmd = message.split(' ', 1)

                            usernote = report_cmd[1]
                            warning = "nullwarning"

                        report_info = [user, usernote, reporter, warning]
                        # Lets not add 1000 of the same usernote
                        item.mod.ignore_reports()
                        save_new_note(report_info[0], report_info[1], report_info[2], report_info[3])


def watch(t=30):
    while True:
        check_reports_for_flags()
        time.sleep(t)


class UserNoteHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def get_moderator_index(reddit, subreddit, mod):
        try:
            x = UserNoteHandler.pull_and_unzip_usernotes(reddit, subreddit)[0]['constants']['users'].index(mod)
            return x
        except ValueError:
            all_usernotes = UserNoteHandler.pull_and_unzip_usernotes(reddit, subreddit)
            # If there are no mods, place the mod into the list
            all_usernotes[0]['constants']['users'][0] = mod
            # Write that to the usernote file before we do anything else in the program
            UserNoteHandler.compile_and_zip_usernotes(reddit, all_usernotes, all_usernotes[1], subreddit)
            # Since the mod will be the first in the list, we can return 0 instead of
            #     Calling the function again, which could create a memory leak if something went very wrong.
            return 0

    @staticmethod
    def get_warning_index(reddit, subreddit, warning):
        """

        :param reddit:
        :param subreddit:
        :param warning:
        :return:
        """
        # Not conditioned to deal with a warning bla bla bla ^^^
        thing_list = UserNoteHandler.pull_and_unzip_usernotes(reddit, subreddit)[0]['constants']['warnings']
        val = thing_list.index(warning) if warning in thing_list else 3
        return val

    # Huge thanks to /u/sjrsimac for the below code

    @staticmethod
    def make_new_note(blob, redditor, notetext, moderatornumber, link, warning_number):
        newnote = {
            'n': notetext,  # The displayed note.
            't': int(time.time()),  # The time the note is made.
            'm': moderatornumber,  # The moderator number that made the note.
            'l': link,  # The attached link, which will be blank for now.
            'w': warning_number  # The warning number.
        }
        # noinspection PyBroadException
        try:
            blob[redditor]['ns'] = [newnote] + blob[redditor]['ns']
        except Exception as ex:
            logging.debug("Exception was hit when making new note:" + str(ex))
            blob[redditor] = {'ns': list()}
            blob[redditor]['ns'] = [newnote]
        return blob

    @staticmethod
    def pull_and_unzip_usernotes(reddit, our_subreddit):
        # Extract the whole usernotes page and turns it into a dictionary.
        allusernotes = json.loads(reddit.subreddit(our_subreddit).wiki['usernotes'].content_md)
        # Get the blob in the usernotes and convert the base64 number into a binary (base2) number.
        blob = base64.b64decode(allusernotes['blob'])
        # Convert the blob binary number into a string.
        blob = zlib.decompress(blob).decode()
        # Convert blob string into a dictionary.
        blob = json.loads(blob)

        # Print the blob in a user readable form.
        # print(blob)

        return [allusernotes, blob]

    @staticmethod
    def compile_and_zip_usernotes(reddit, allusernotes, blob, our_subreddit):
        # This is the debugging code. Disable or delete this when you're done debugging.
        # print(allusernotes)
        # print(blob)

        blob = json.dumps(blob)
        blob = blob.encode()
        blob = zlib.compress(blob)
        rewrittenblob = base64.b64encode(blob).decode()
        allusernotes['blob'] = str(rewrittenblob)
        allusernotes = json.dumps(allusernotes)
        # noinspection PyBroadException
        try:
            reddit.subreddit(our_subreddit).wiki['usernotes'].edit(allusernotes)
        except Forbidden:
            logging.critical("Authenticated Account does not have permission to edit wiki for /r/%s. Exiting." % sub)
            exit(1)
        except Exception as ex:
            logging.critical("Exception encountered while uploading usernotes: %s" % str(ex))
            exit(1)


def main():
    parser = argparse.ArgumentParser(description="Bot to check reports for mod initiated commands and create usernotes")
    parser.add_argument('-w', '--watch', help="Specify a time for the bot to loop", nargs=1)
    parser.add_argument('-d', '--debug', help='Enable Debug Logging', action='store_true')
    parser.add_argument('-c', '--credentials', help='Specify oauth credentials on command line', nargs=4)

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    if args.credentials is not None:
        # We're modifying the global variable r, make sure this is specified
        global r
        logging.debug("CLI Credentials Specified! Format is client_id, client_secret, username, password!")
        try:
            r = praw.Reddit(client_id=args.credentials[0],
                            client_secret=args.credentials[1],
                            username=args.credentials[2],
                            password=args.credentials[3],
                            user_agent='Mod Toolbox Usernote Modification Bot')
        except IndexError:
            logging.critical('Not enough credentials provided. If they are all present, try wrapping them in quotes')
            exit(1)

    logging.debug('Value recieved from --watch argument: %s' % args.watch[0])
    if args.watch is not None:
        loop_time = args.watch[0]
        logging.info("Initializing Bot, Checking reports every %s seconds" % loop_time)
        logging.debug("!! Debug mode enabled")
        watch(loop_time)
    else:
        logging.info("Initializing Bot, Checking reports once and then exiting")

    # watch(time) will loop the bot
    # to not loop the bot, just call check_reports_for_flags()


if __name__ == "__main__":
    main()
