# -*- coding: utf-8 -*-
import os

from appdirs import user_config_dir
from cloudomate import wallet as wallet_util
from cloudomate.cmdline import execute, _merge_random_user_data
from cloudomate.hoster.vps.vps_hoster import VpsHoster
from cloudomate.util.settings import Settings


def _user_settings():
    settings = Settings()
    settings.read_settings()
    return settings


def status(provider):
    settings = _user_settings()
    return provider(settings).get_status()


def get_ip(provider):
    return get_configuration(provider).ip


def setrootpw(provider, password):
    return execute(["vps", "setrootpw", provider, password])


def get_options(provider):
    return provider.get_options()


def get_configuration(provider):
    settings = _user_settings()
    return provider(settings).get_configuration()


def get_network_fee():
    return wallet_util.get_network_fee()


def purchase(provider, option, wallet):
    settings = _user_settings()
    option = get_options(provider)[option]
    try:
        provider(settings).purchase(wallet, option)
        provider_type = "VPS" if issubclass(provider, VpsHoster) else "VPN"
        print("Successfully: bought {0} at {1}".format(provider_type, provider.get_metadata()[0]))
        return True
    except SystemExit as e:
        print("SystemExit caught at cloudomatecontroller purchase")
        print(e)
        return False


def generate_config():
    config = Settings()
    filename = os.path.join(user_config_dir(), 'cloudomate.cfg')
    if os.path.exists(filename):
        print("cloudomate.cfg already present at %s" % filename)
        config.read_settings(filename=filename)
        return config
    _merge_random_user_data(config)
    config.save_settings(filename)
    return config
