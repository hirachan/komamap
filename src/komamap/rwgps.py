from typing import Optional
import requests


def download_gpx(filename: str, route_id: str, format: str, privacy_code: Optional[str] = None):
    url = f"https://ridewithgps.com/routes/{route_id}.gpx?sub_format={format}"

    if privacy_code:
        url += f"&privacy_code={privacy_code}"

    res = requests.get(url)
    with open(filename, "wb") as fw:
        fw.write(res.content)
