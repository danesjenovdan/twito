from sqlalchemy import Column, DateTime
from sqla_wrapper import SQLAlchemy
from config import DB_URL


db = SQLAlchemy(url=DB_URL)


class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    twitter_id = db.Column(db.String, nullable=False, unique=True)
    favorite_count = db.Column(db.Integer, nullable=True)
    filter_level = db.Column(db.String, nullable=True)
    from_user_created_at = Column(DateTime, nullable=True)
    from_user_description = Column(db.String, nullable=True)
    from_user_favourites_count = Column(db.Integer, nullable=True)
    from_user_followercount = Column(db.Integer, nullable=True)
    from_user_friendcount = Column(db.Integer, nullable=True)
    from_user_id = Column(db.String, nullable=True)
    from_user_lang = Column(db.String, nullable=True)
    from_user_listed = Column(db.String, nullable=True)
    from_user_name = Column(db.String, nullable=True)
    from_user_profile_image_url = Column(db.String, nullable=True)
    from_user_timezone = Column(db.String, nullable=True)
    from_user_tweetcount = Column(db.Integer, nullable=True)
    from_user_url = Column(db.String, nullable=True)
    from_user_utcoffset = Column(db.String, nullable=True)
    from_user_verified = Column(db.Integer, nullable=True)
    from_user_withheld_scope = Column(db.String, nullable=True)
    from_user_realname = Column(db.String, nullable=True)
    in_reply_to_status_id = Column(db.String, nullable=True)
    lang = Column(db.String, nullable=True)
    lat = Column(db.String, nullable=True)
    lng = Column(db.String, nullable=True)
    location = Column(db.String, nullable=True)
    possibly_sensitive = Column(db.Integer, nullable=True)
    quoted_status_id = Column(db.String, nullable=True)
    retweet_count = Column(db.Integer, nullable=True)
    source = Column(db.String, nullable=True)
    text = Column(db.String, nullable=True)
    time = Column(db.Integer, nullable=True)
    to_user_name = Column(db.String, nullable=True)
    truncated = Column(db.String, nullable=True)
    withheld_copyright = Column(db.String, nullable=True)
    withheld_scope = Column(db.String, nullable=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.utcnow)
    # updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow)


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    short_url = Column(db.String, nullable=False)
    resolved_url = Column(db.String, nullable=True)
    domain = Column(db.String, nullable=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.utcnow)
    # updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow)


class TweetUrl(db.Model):
    __tablename__ = 'tweets_urls'

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'), primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), primary_key=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.utcnow)
    # updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow)
