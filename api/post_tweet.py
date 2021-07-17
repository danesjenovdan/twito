from datetime import date
import os
import io

import django
from django.utils import translation
from django.utils import formats

from TwitterAPI import TwitterAPI
import requests


def post_tweet_with_image(api, content, image_data):
    """Post tweeet and image using TwitterAPI.
    """
    response = api.request("media/upload", None, {"media": image_data})
    if response.status_code != 200:
        raise RuntimeError(
            "Upload media failure", response.status_code, response.response.content
        )

    response = api.request(
        "statuses/update", {"status": content, "media_ids": response.json()["media_id"]}
    )
    if response.status_code != 200:
        raise RuntimeError(
            "Update status failure", response.status_code, response.content
        )


def load_image_from_url(url):
    """Returns image data loaded from URL.
    """
    response = requests.get(url)
    return io.BytesIO(response.content)


def today_string_in_language(language, format=None):
    """Returns today date formated in language with using Django.
    """
    django.setup()
    with translation.override(language):
        return formats.date_format(date.today(), format)


def main():
    api = TwitterAPI(
        os.getenv("TWITTER_CONSUMER_KEY"),
        os.getenv("TWITTER_CONSUMER_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN_KEY"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )
    image_data = load_image_from_url("https://twito.si/twito.png")
    content = today_string_in_language("sl")
    post_tweet_with_image(api, content, image_data)


if __name__ == "__main__":
    main()
