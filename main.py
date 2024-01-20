import os
import asyncio
import configparser
import acc
from asmr import ASMR
import handle

async def main(codes):
    config = configparser.ConfigParser()
    config.read('./config.ini')

    asmr = ASMR(config.get('account', 'name'), config.get('account', 'password'))
    await asmr.get_token()

    for code in codes:
        try:
            info, tracks = await asyncio.gather(asmr.get_voice_info(code), asmr.get_voice_tracks(code))

            handle.info(info).print_info()
            handle.download(code, tracks, asmr.headers).search(tracks, os.path.join('.', 'RJ{}'.format(code)))
        except Exception as e:
            continue

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./config.ini')
    
    if config.has_option('account', 'name') and config.has_option('account', 'password'):
        if not acc.auth(config.get('account', 'name'), config.get('account', 'password')):
            acc.check()
    else:
        acc.check()

    code = input('Please input RJ code (Split with space): ')

    codes = [item.split('RJ')[-1] if 'RJ' in item else item.split('/')[-1] for item in code.split(' ')]
    if [item for item in codes if item]:
        asyncio.run(main(codes))
