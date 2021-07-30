from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
import sqlalchemy as db
from app.db.base_class import Base
from datetime import datetime

import enum


class BanTypeEnum(enum.Enum):
    EMAIL = 1
    PHONE_NUMBER = 2


class SocialAccount(Base):
    """Define the SocialAccount model"""

    __tablename__ = 'social_account'

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(30))
    uid = db.Column(db.String(200))
    last_login = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    extra_data = db.Column(db.String(500))
    user_id = db.Column(db.Integer, index=True)


class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(
        db.Unicode(255),
        unique=True,
        nullable=False,
        index=True
    )  # , default='')
    phone_number = db.Column(db.String(255), unique=True, nullable=True)
    verification_sms_time = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.Unicode(255))  # (128), default='')
    middle_name = db.Column(db.Unicode(255))  # (128), default='')
    last_name = db.Column(db.Unicode(255))  # (128), default='')
    gender = db.Column(db.String(255))  # (10), default='')
    age = db.Column(db.String(255))  # (3), default='')
    birthday = db.Column(db.DateTime)
    about_me = db.Column(db.Text, default='')
    email = db.Column(db.String(255))  # (255), unique=True)
    password_hash = db.Column(db.String(255))  # (128), default='')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    email_confirmed_at = db.Column(db.DateTime, nullable=True)
    profile_pic_url = db.Column(db.String(255))  # (255), default='')
    cover_pic_url = db.Column(db.String(255))  # (255), default='')
    document_pic_url = db.Column(db.String(255))
    last_message_read_time = db.Column(db.DateTime, default=datetime.utcnow)
    reputation = db.Column(db.Integer, server_default='0', nullable=False)
    profile_views = db.Column(db.Integer, server_default='0', nullable=False)

    show_nsfw = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    is_deactivated = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    is_private = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    is_first_log_in = db.Column(
        db.Boolean, server_default=expression.true(), nullable=False)
    confirmed = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    is_birthday_hidden = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    admin = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    verified_document = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    show_fullname_instead_of_display_name = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)
    joined_collaboration = db.Column(
        db.Boolean, server_default=expression.false(), nullable=False)

    question_share_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    question_shared_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    question_report_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    question_reported_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    question_upvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    question_upvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    question_downvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    question_downvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)

    answer_share_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    answer_shared_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    answer_upvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    answer_upvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    answer_downvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    answer_downvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    answer_report_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    answer_reported_count = db.Column(
        db.Integer, server_default='0', nullable=False)

    article_share_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    article_shared_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    article_upvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    article_upvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    article_downvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    article_downvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    article_report_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    article_reported_count = db.Column(
        db.Integer, server_default='0', nullable=False)

    poll_share_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    poll_shared_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    poll_upvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    poll_upvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    poll_downvote_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    poll_downvoted_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    poll_report_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    poll_reported_count = db.Column(
        db.Integer, server_default='0', nullable=False)

    posts = db.relationship(
        "Post", cascade='all,delete-orphan', lazy='dynamic')

    post_share_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    post_shared_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    post_favorite_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    post_favorited_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    post_report_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    post_reported_count = db.Column(
        db.Integer, server_default='0', nullable=False)

    comment_count = db.Column(db.Integer, server_default='0', nullable=False)
    comment_favorite_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    comment_favorited_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    comment_report_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    comment_reported_count = db.Column(
        db.Integer, server_default='0', nullable=False)

    followed_topics = db.relationship(
        'Topic', secondary='topic_bookmark', lazy='dynamic')
    user_report_count = db.Column(
        db.Integer, server_default='0', nullable=False)
    user_reported_count = db.Column(
        db.Integer, server_default='0', nullable=False)


class UserBan(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    ban_by = db.Column(db.String(255))
    ban_type = db.Column(
        db.Enum(BanTypeEnum, validate_strings=True),
        nullable=False,
        server_default="EMAIL"
    )
    expiry_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete='CASCADE'))
    # one-to-many relationship with table User
    user = db.relationship('User', lazy=True)
