from django.db import models

class DailySums(models.Model):
    date = models.DateField(auto_now_add=True, null=False)
    number_of_tweets = models.IntegerField(default=0, null=False)
    seconds_online = models.IntegerField(default=0, null=False)
    original_tweets = models.IntegerField(default=0, null=False)
    retweets = models.IntegerField(default=0, null=False)
    retweets_with_comment = models.IntegerField(default=0, null=False)
