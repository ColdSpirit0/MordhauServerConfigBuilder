import requests
from pathlib import Path


def get_profile_url(game_id):
    url = f'https://mod.io/v1/games/@mordhau/mods?_limit=100&_offset=0&_sort=-popular&id={game_id}'
    headers = {
        'Accept': 'application/json',
        'X-Modio-Origin': 'web',
        'Alt-Used': 'mod.io'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    data = response.json()
    return data["data"][0]['profile_url']


def update_ini_files():
    key = 'Mods'
    for file_name in Path().rglob('*.ini'):
        with file_name.open('r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith(key + "="):
                if ";" not in line:
                    line = line.strip()
                    _, game_id = line.split("=")
                    profile_url = get_profile_url(game_id)
                    line = f"{key}={game_id} ; {profile_url}\n"
                    lines[i] = line

        text = "".join(lines)
        # print(text)
        # print("----------------------")
        with file_name.open("w") as f:
            f.write(text)


if __name__ == "__main__":
    update_ini_files()
