import requests
import re
import tldextract


def get_urls_from_tweets(tweets):
    for tweet in tweets:
        urls = parse_urls(tweet.get('text'))

        for url in urls:
            try:
                resolved_url = resolve_url(url)

                # some urls might be shortened before sharing to twitter
                if resolved_url.find('bit.ly') != -1:
                    resolved_url = resolve_url(resolved_url)

                domain = get_domain_from_url(resolved_url)
                print(domain)

            except Exception:
                print('welp...')


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

    return f'{ext.domain}.{ext.suffix}'
