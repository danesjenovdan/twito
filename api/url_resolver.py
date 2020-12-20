import requests
import re
import tldextract

url_shortener_domains = ['bit.ly']


def get_urls_from_tweet(tweet):
    urls = parse_urls(tweet.get('text'))

    resolved_urls = []
    for url in urls:
        resolved_url = resolve_url(url)

        if any(x in url for x in url_shortener_domains):
            print(f'{url} has been shortened before sharing, resolving again')
            resolved_url = resolve_url(resolved_url)

        domain = get_domain_from_url(resolved_url)
        resolved_urls.append({'url': resolved_url, 'domain': domain})

    return resolved_urls


def parse_urls(string):
    return re.findall(r'(https?://\S+)', string)


def resolve_url(url):
    print(f'getting {url}')
    r = requests.get(url, allow_redirects=False)

    if r.status_code not in [301, 302]:
        raise Exception(f'short url resolution went wrong, got response with status code: {r.status_code}')

    resolved_url = r.headers['Location']

    print(f'{url} resolves to {resolved_url}')

    return resolved_url


def get_domain_from_url(url):
    ext = tldextract.extract(url)
    domain = f'{ext.domain}.{ext.suffix}'
    print(f'domain {domain} extracted for {url}')

    return domain
