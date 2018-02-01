# -*- coding: utf-8 -*-
import codecs
import os
import random
import unicodedata
from ConfigParser import ConfigParser

from appdirs import user_config_dir
from cloudomate import wallet as wallet_util
from cloudomate.cmdline import providers, change_root_password_ssh
from cloudomate.util.settings import Settings
from faker.factory import Factory


def _user_settings():
    settings = Settings()
    settings.read_settings()
    return settings


def status(provider):
    settings = _user_settings()
    return provider.get_status(settings)


def get_ip(provider):
    settings = _user_settings()
    return provider.get_ip(settings)


def setrootpw(password):
    return change_root_password_ssh({'root_password': password})


def get_vps_options(provider):
    return providers['vps'][provider.get_metadata()[0]].get_options()


def get_network_fee():
    return wallet_util.get_network_fee()


def purchase(provider, vps_option, wallet):
    settings = _user_settings()
    option = get_vps_options(provider)[vps_option]
    try:
        transaction_hash = provider.purchase(wallet, option)
        print("Transaction hash of purchase: {0}".format(transaction_hash))
        return transaction_hash
    except SystemExit as e:
        print("SystemExit catched at cloudomatecontroller purchase")
        print(e)
        return False


def generate_config():
    config = Settings()
    filename = os.path.join(user_config_dir(), 'cloudomate.cfg')
    if os.path.exists(filename):
        print("cloudomate.cfg already present at %s" % filename)
        config.read_settings(filename=filename)
        return config
    locale = random.choice(['cs_CZ', 'de_DE', 'dk_DK', 'es_ES', 'et_EE', 'hr_HR', 'it_IT'])
    fake = Factory().create(locale)
    cp = ConfigParser()
    _generate_address(cp, fake)
    _generate_server(cp, fake)
    _generate_user(cp, fake)
    _remove_unicode(cp)
    with codecs.open(filename, 'w', 'utf8') as config_file:
        cp.write(config_file)
    return cp


def _remove_unicode(cp):
    for section in cp.sections():
        for option in cp.options(section):
            item = cp.get(section, option)
            if isinstance(item, unicode):
                cp.set(section, option, unicodedata.normalize('NFKD', item).encode('ascii', 'ignore'))

#
# [User]
# email =
# firstName =
# lastName =
# companyName =
# phoneNumber =
# password =
#
# [Address]
# address =
# city =
# state =
# countryCode =
# zipcode =
#
# [payment]
# walletpath =
#
# [Server]
# root_password =
# ns1 =
# ns2 =
# hostname =


def _generate_user(cp, fake):
    cp.add_section('user')
    firstname = fake.first_name()
    lastname = fake.last_name()
    full_name = firstname + '_' + lastname
    full_name = full_name.replace(' ', '_')
    cp.set('user', 'username', fake.user_name())
    cp.set('user', 'email', full_name + '@erackron.com')
    cp.set('user', 'firstname', firstname)
    cp.set('user', 'lastname', lastname)
    cp.set('user', 'companyname', fake.company())
    cp.set('user', 'phonenumber', fake.numerify('##########'))
    cp.set('user', 'password', fake.password(length=10, special_chars=False))


def _generate_address(cp, fake):
    cp.add_section('address')
    cp.set('address', 'address', fake.street_address())
    cp.set('address', 'city', fake.city())
    cp.set('address', 'state', fake.state())
    cp.set('address', 'countryCode', fake.country_code())
    cp.set('address', 'zipcode', fake.postcode())


def _generate_server(cp, fake):
    cp.add_section('server')
    cp.set('server', 'root_password', fake.password(length=10, special_chars=False))
    cp.set('server', 'ns1', 'ns1')
    cp.set('server', 'ns2', 'ns2')
    cp.set('server', 'hostname', fake.word())
