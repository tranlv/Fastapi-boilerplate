-- question -> user related data

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

-- answer -> user related data

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

-- article -> user related data


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

-- poll -> user related data
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

-- posts -> user related data
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

-- comment and misc
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