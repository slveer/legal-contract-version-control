import io
from zipfile import Path
import zipfile

import requests
import sys
import exceptions


def get_entered_url():
    return sys.argv[2] if len(sys.argv) > 2 else None

def resolve_entered_url(url=get_entered_url()):
    if url is None:
        print("No URL entered.")
        raise exceptions.InvalidArgumentError("No URL entered.")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    if not url.endswith("/clone"):
        url += "/clone"

    return url


response = requests.get(resolve_entered_url())

buffer = io.BytesIO(response.content)

zipfile.ZipFile(buffer, "r").extractall(resolve_entered_url().split("/")[-2])

print(response.status_code)