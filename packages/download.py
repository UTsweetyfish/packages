import gzip
from pathlib import Path
import requests

from debian.deb822 import Sources
from debian.debian_support import version_compare


data_source = {
    'beige': {
        'sources': 'https://ci.deepin.com/repo/deepin/deepin-community/stable/dists/beige/main/source/Sources.gz',
    },
    'sid': {
        'sources': 'https://ftp.debian.org/debian/dists/sid/main/source/Sources.gz',
    },
}

TARGET_DIR = 'data'

def sync_data():

    for repo, data in data_source.items():
            
        Path(TARGET_DIR + '/' + repo).mkdir(parents=True, exist_ok=True)

        for file, url in data.items():
            r = requests.get(url, timeout=60)
            assert r.url.endswith('.gz')
            decompressed = gzip.decompress(r.content)
            match file.split('-'):
                case ['sources']:
                    with open(TARGET_DIR + '/' + repo + '/' + 'Sources', 'wb') as f:
                        f.write(decompressed)
                case ['packages', arch]:
                    with open(TARGET_DIR + '/' + repo + '/' + 'Packages-' + arch, 'wb') as f:
                        f.write(decompressed)

def prepare():
    sync_data()
    # Stable + Testing
    packages = {}
    for repo in ['beige', 'sid']:
        with open(TARGET_DIR + '/' + repo + '/' + 'Sources') as f:
            for item in Sources.iter_paragraphs(f):
                package: str = item['package']
                version: str = item['version']
                if package not in packages:
                    packages[package] = {}
                if repo not in packages[package]:
                    packages[package][repo] = version
                elif version_compare(version, packages[package][repo]) >= 0:
                    packages[package][repo] = version
    return packages
