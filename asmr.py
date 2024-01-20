import requests

from typing import Any, Dict

class ASMR:
    def __init__(self, name, password) -> None:
        self.requests = requests
        self.name = name
        self.password = password
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
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            print(f"RJ{voice_id} 不存在， 自動跳過下載")

    async def get_voice_tracks(self, voice_id: str) -> Dict[str, Any]:
        resp = self.requests.get(
            f"https://api.asmr.one/api/tracks/{voice_id}",
            headers=self.headers,
            timeout=120
        )
        return resp.json()
