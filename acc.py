import os
import requests
import configparser

def check():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    if not config.has_section('account') or not (config.has_option('account', 'name') and config.has_option('account', 'password')):
        print("Account information error, please input your account information again")

        name = input('Please input your name: ')
        password = input('Please input your password: ')

        if auth(name, password):
            if not config.has_section('account'):
                config.add_section('account')

            config.set('account', 'name', name)
            config.set('account', 'password', password)

            with open("./config.ini", 'w') as f:
                config.write(f)
        else:
            check()
    else:
        if config.has_option('account', 'name') and config.has_option('account', 'password'):
            if auth(config['account']['name'], config['account']['password']) == False:
                config.remove_option('account', 'name')
                config.remove_option('account', 'password')
                with open("./config.ini", 'w') as f:
                    config.write(f)
                check()


def auth(name, password) -> bool:
    req = requests.post(
        url='https://api.asmr.one/api/auth/me',
        json={
            "name": name,
            "password": password
        },
        headers={
            "Referer": 'https://www.asmr.one/',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        },
        timeout=120
    )
    if str(req.status_code).startswith('2'):
        return True
    elif str(req.status_code).startswith('4'):
        return False
