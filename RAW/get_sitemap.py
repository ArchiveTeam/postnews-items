import os
import re

import requests


def get_url(url: str) -> bytes:
    print('Getting', url)
    response = requests.get(url, timeout=10)
    assert response.status_code == 200
    with open(os.path.join('sitemap', url.split('/')[-1]), 'wb') as f:
        f.write(response.content)
    return response.content


def main():
    if not os.path.isdir('sitemap'):
        os.makedirs('sitemap')
    for url in re.findall(
        rb'<loc>\s*(https?://[^<]+?)\s*</loc>',
        get_url('https://post.news/sitemap-index.xml')
    ):
        get_url(str(url, 'utf8'))

if __name__ == '__main__':
    main()

