from __future__ import print_function
import os
from configparser import ConfigParser

from appdirs import user_config_dir
from cloudomate.util.settings import Settings
from twython import Twython


def tweet_arrival():
    options = Settings()
    options.read_settings()
    name = options.get('user', 'firstname') + ' ' + options.get('user', 'lastname')

    path = os.path.join(user_config_dir(), 'twitter.cfg')
    if not os.path.exists(path):
        print("Can't Tweet: {0} doesn't exist".format(path))
        return False
    cp = ConfigParser()
    cp.read(path)

    try:
        twitter = Twython(cp.get('twitter', 'app_key'),
                          cp.get('twitter', 'app_secret'),
                          cp.get('twitter', 'oauth_token'),
                          cp.get('twitter', 'oauth_token_secret'))
        twitter.update_status(
            status='Pleb %s has joined the botnet for good. #PlebNet #Cloudomate #Tribler #Bitcoin' % name)
        print("Tweeted arrival")
    except Exception as e:
        print(e)
        return False
    return True
