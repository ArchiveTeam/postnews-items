import os
import re
import urllib.parse


def main(filename_prefix: str, item_type: str, url_part: str):
    items = set()
    for filename in os.listdir('sitemap'):
        if filename.startswith(filename_prefix):
            print('Processing', filename)
            with open(os.path.join('sitemap', filename), 'r') as f:
                items |= {
                    item_type+':'+urllib.parse.quote(s, safe='')
                    for s in re.findall(r'<loc>\s*https?://[^/]+/'+url_part+r'/([^\s<]+)', f.read())
                }
            print('Total found', len(items))
    chars = set()
    for item in items:
        if '/' in item:
            print(item)
        chars |= set(item.split(':', 1)[1])
    print('Characters', sorted(chars))
    size = 100000
    items = sorted(items)
    for i in range(0, len(items), size):
        with open('{}_{}-{}.txt'.format(item_type, i, min(i+size-1, len(items))), 'w') as f:
            print('Writing', f.name)
            f.write('\n'.join(items[i:i+size])+'\n')

if __name__ == '__main__':
    main('sitemap-profiles-', 'profile', '@')
    main('sitemap-topics-', 'topic', 'topics')

