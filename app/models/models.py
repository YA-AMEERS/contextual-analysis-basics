from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from app import db

class UptodateNews(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    postId = db.Column("post_id", db.String(500))
    headLine = db.Column("head_line", db.String(5000))
    story = db.Column("story", db.String(5000))
    source = db.Column("source", db.String(5000))
    grade = db.Column("grade", db.Integer())
    state = db.Column("state", db.String(100))
    country = db.Column("country", db.String(100))
    section = db.Column("section", db.String(500))
    channel = db.Column("channel", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, postId, headLine, story, source, grade, state, country, section, channel):
        self.postId = postId
        self.headLine = headLine
        self.story = story
        self.source = source
        self.grade = grade
        self.state = state
        self.country = country
        self.channel = channel
        self.section = section
       


class AllNews(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    postId = db.Column("post_id", db.String(500))
    headLine = db.Column("head_line", db.String(5000))
    story = db.Column("story", db.String(5000))
    source = db.Column("source", db.String(5000))
    grade = db.Column("grade", db.Integer())
    state = db.Column("state", db.String(100))
    country = db.Column("country", db.String(100))
    section = db.Column("section", db.String(500))
    channel = db.Column("channel", db.String(500))
    Created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, postId, headLine, story, source, grade, state, country, section, channel):
        self.postId = postId
        self.headLine = headLine
        self.story = story
        self.source = source
        self.grade = grade
        self.state = state
        self.country = country
        self.channel = channel
        self.section = section
