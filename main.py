import requests
import asyncio
import os
from dotenv import load_dotenv
from typing import Any, Dict


class ASMR:
    def __init__(self) -> None:
        self.name = os.getenv('name')
        self.password = os.getenv('password')
        self.requests = requests
        self.name = []
        self.track = []
        self.headers = {
            "Referer": 'https://www.asmr.one/',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }

    async def get_token(self) -> None:
        req = self.requests.post(
            url='https://api.asmr.one/api/auth/me',
            json={
                "name": self.name,
                "password": self.password
            },
            headers={
                "Referer": 'https://www.asmr.one/',
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            },
            timeout=120
        )
        self.headers |= {
            "Authorization": f"Bearer {(req.json())['token']}",
        }

    async def get_voice_info(self, voice_id: str) -> Dict[str, Any]:
        resp = self.requests.get(
            f"https://api.asmr.one/api/work/{voice_id}",
            headers=self.headers,
            timeout=120
        )
        return resp.json()

    async def get_voice_tracks(self, voice_id):
        resp = self.requests.get(
            f"https://api.asmr.one/api/tracks/{voice_id}",
            headers=self.headers,
            timeout=120
        )
        return resp.json()

async def main(code):
    def search(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                search(value)
        elif isinstance(obj, list):
            for item in obj:
                search(item)
        else:
            if (str(obj).endswith('.mp3')) and 'download' not in obj: # or str(obj).endswith('.wav')
                if obj.startswith('https://'):
                    asmr.track.append(obj)
                else:
                    asmr.name.append(obj)
    asmr = ASMR()
    await asmr.get_token()
    RJ = code.split('RJ')[-1]
    search(await asmr.get_voice_tracks(RJ))
    if not os.path.exists('RJ'+RJ):
        os.mkdir('RJ'+RJ)
    for i in range(len(asmr.name)):
        with open('RJ'+RJ+'/'+asmr.name[i], 'wb') as f:
            f.write(requests.get(asmr.track[i], headers=asmr.headers).content)

if __name__ == '__main__':
    load_dotenv()
    code = input('please input RJ code: ')
    asyncio.run(main(code))
