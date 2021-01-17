import requests
import re
import tldextract
from tweets.utilities import is_retweet, get_tweet_id
import logging
logger = logging.getLogger(__name__)

url_shortener_domains = ['bit.ly']


def get_urls_from_tweet(tweet, resolve_retweet=False):
    if should_resolve_tweet(tweet, resolve_retweet):
        urls = parse_urls(tweet.get('text'))

        resolved_urls = []
        for url in urls:
            resolved_url = resolve_url(url)

            if any(x in url for x in url_shortener_domains):
                logger.info(f'<{url}> has been shortened before sharing, resolving again')
                resolved_url = resolve_url(resolved_url)

            if should_process_url(resolved_url):
                domain = get_domain_from_url(resolved_url)
                resolved_urls.append({'url': resolved_url, 'domain': domain})

        return resolved_urls


def should_resolve_tweet(tweet, resolve_retweet):
    if is_retweet(tweet) and not resolve_retweet:
        logger.info(f'tweet <{get_tweet_id(tweet)}> is retweet, skipping')
        return False

    return True


def should_process_url(url):
    # skip photos
    return url.find('JJansaSDS') == -1


def parse_urls(string):
    return re.findall(r'(https?://\S+)', string)


def resolve_url(url):
    logger.info(f'getting <{url}>')
    r = requests.get(url, allow_redirects=False)

    if r.status_code not in [301, 302]:
        message = f'short url resolution for <{url}> went wrong, got response with status code: {r.status_code}'
        logger.error(message)
        raise Exception(message)

    resolved_url = r.headers['Location']

    logger.info(f'<{url}> resolves to <{resolved_url}>')

    return resolved_url


def get_domain_from_url(url):
    ext = tldextract.extract(url)
    domain = f'{ext.domain}.{ext.suffix}'
    logger.info(f'domain <{domain}> extracted for <{url}>')

    return domain
