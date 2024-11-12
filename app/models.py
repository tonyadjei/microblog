from datetime import datetime, timezone
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

# from sqlalchemy.dialects.postgresql import ARRAY
from flask_login import UserMixin
from app import db, login


followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    followed = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        joined_table = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)
        return joined_table.union(self.posts).order_by(Post.timestamp.desc())  # type: ignore


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)


class HomePageWhoWeAre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_title = db.Column(db.String(20))
    section_body = db.Column(db.String(400))
    section_image_path = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "section_title": self.section_title,
            "section_body": self.section_body,
            "section_image_path": self.section_image_path,
        }

    def __repr__(self):
        return "<HomePageWhoWeAre {}>".format(self.section_body)


class FeaturedArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_title = db.Column(db.String(150))
    section_body = db.Column(db.String(400))
    section_image_path = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "section_title": self.section_title,
            "section_body": self.section_body,
            "section_image_path": self.section_image_path,
        }

    def __repr__(self):
        return "<FeaturedArticle {}>".format(self.section_body)


class Carousel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_title = db.Column(db.String(200))
    section_image_path = db.Column(db.String(255))

    def __repr__(self):
        return "<Carousel {}>".format(self.section_title)


class OurImpact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_count = db.Column(db.Integer)
    section_title = db.Column(db.String(150))
    section_suffix = db.Column(db.String(10))
    section_body = db.Column(db.String(400))

    def to_dict(self):
        return {
            "id": self.id,
            "section_count": self.section_count,
            "section_title": self.section_title,
            "section_suffix": self.section_suffix,
            "section_body": self.section_body,
        }

    def __repr__(self):
        return "<OurImpact {}>".format(self.section_body)


class AboutUsSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_about_us_title = db.Column(db.String(150))
    section_about_us_body = db.Column(db.String(400))
    section_about_us_image_path = db.Column(db.String(255))
    section_mission_title = db.Column(db.String(150))
    section_mission_image_path = db.Column(db.String(255))
    section_our_vision_title = db.Column(db.String(150))
    section_our_vision_body = db.Column(db.String(400))
    section_vision_image = db.Column(db.String(255))
    section_our_values_title = db.Column(db.String(150))

    def to_dict(self):
        return {
            "id": self.id,
            "section_about_us_title": self.section_about_us_title,
            "section_about_us_body": self.section_about_us_body,
            "section_about_us_image_path": self.section_about_us_image_path,
            "section_mission_title": self.section_mission_title,
            "section_mission_image_path": self.section_mission_image_path,
            "section_our_vision_title": self.section_our_vision_title,
            "section_our_vision_body": self.section_our_vision_body,
            "section_vision_image": self.section_vision_image,
            "section_our_values_title": self.section_our_values_title,
        }

    def __repr__(self):
        return "<AboutUsSection {}>".format(self.section_about_us_body)


class MissionItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_mission_icon = db.Column(db.String(150))
    section_mission_body = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "section_mission_icon": self.section_mission_icon,
            "section_mission_body": self.section_mission_body,
        }

    def __repr__(self):
        return "<MissionItems {}>".format(self.section_mission_body)


class ValuesItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_our_values_icon = db.Column(db.String(150))
    section_our_values_body = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "section_our_values_icon": self.section_our_values_icon,
            "section_our_values_body": self.section_our_values_body,
        }

    def __repr__(self):
        return "<ValuesItems {}>".format(self.section_our_values_body)


class Leadership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leadership_name = db.Column(db.String(150))
    leadership_titles = db.Column(db.String(150))
    leadership_logo = db.Column(db.String(255))
    leadership_position = db.Column(db.String(150))
    leadership_body = db.Column(db.String(600))
    is_management = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "leadership_name": self.leadership_name,
            "leadership_titles": self.leadership_titles,
            "leadership_logo": self.leadership_logo,
            "leadership_position": self.leadership_position,
            "leadership_body": self.leadership_body,
            "is_management": self.is_management,
        }

    def __repr__(self):
        return "<Leadership {}>".format(self.leadership_name)


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_name = db.Column(db.String(150))
    partner_description = db.Column(db.String(200))
    partner_logo = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "partner_name": self.partner_name,
            "partner_description": self.partner_description,
            "partner_logo": self.partner_logo,
        }

    def __repr__(self):
        return "<Partner {}>".format(self.partner_name)


class LatestNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latest_news_title = db.Column(db.String(200))
    latest_news_body = db.Column(db.String(1000))
    latest_news_image = db.Column(db.String(255))
    created_date = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    last_modified = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "latest_news_title": self.latest_news_title,
            "latest_news_body": self.latest_news_body,
            "latest_news_image": self.latest_news_image,
            "created_date": self.created_date,
            "last_modified": self.last_modified,
        }

    def __repr__(self):
        return "<LatestNews {}>".format(self.latest_news_title)


class LatestVideos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latest_videos_title = db.Column(db.String(200))
    latest_videos_link = db.Column(db.String(255))
    created_date = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    last_modified = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "latest_videos_title": self.latest_videos_title,
            "latest_videos_link": self.latest_videos_link,
            "created_date": self.created_date,
            "last_modified": self.last_modified,
        }

    def __repr__(self):
        return "<LatestVideos {}>".format(self.latest_videos_title)


class IndustryUpdates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_updates_title = db.Column(db.String(200))
    industry_updates_image = db.Column(db.String(255))
    industry_updates_link = db.Column(db.String(255))
    created_date = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    last_modified = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "industry_updates_title": self.industry_updates_title,
            "industry_updates_image": self.industry_updates_image,
            "industry_updates_link": self.industry_updates_link,
            "created_date": self.created_date,
            "last_modified": self.last_modified,
        }

    def __repr__(self):
        return "<IndustryUpdates {}>".format(self.industry_updates_title)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(200))
    event_image = db.Column(db.String(255))
    event_body = db.Column(db.String(1000))
    upcoming_event = db.Column(db.Boolean, default=False)
    created_date = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    last_modified = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "event_title": self.event_title,
            "event_image": self.event_image,
            "event_body": self.event_body,
            "upcoming_event": self.upcoming_event,
            "created_date": self.created_date,
            "last_modified": self.last_modified,
        }

    def __repr__(self):
        return "<Event {}>".format(self.event_title)
