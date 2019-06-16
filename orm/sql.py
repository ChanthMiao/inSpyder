# encoding="utf-8"
from sqlalchemy import Integer, String
from sqlalchemy import Column, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String(length=12), primary_key=True)
    username = Column(String(length=30))
    posts = Column(Integer, default=0)
    following = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    biography = Column(String(length=300))
    r_post = relationship("Post", backref="users")


class Post(Base):
    __tablename__ = "posts"
    id = Column(String(length=24), primary_key=True)
    timestamp = Column(Integer, default=0)
    stars = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    url = Column(String(length=300))
    uid = Column(String(length=12), ForeignKey("users.id"))


class manager(object):
    def __init__(self, con_string: str):
        self._engine = create_engine(con_string)
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()

    def close(self):
        self._session.close()

    def insert_or_update_user(self,
                              uid: str,
                              name: str,
                              posts_n: int,
                              following_n: int,
                              followers_n: int,
                              bio: str,
                              commit=True):
        line = self._session.query(User)\
            .filter(User.id == uid)\
            .one_or_none()
        if line is None:
            user = User(id=uid,
                        username=name,
                        posts=posts_n,
                        following=followers_n,
                        followers=followers_n,
                        biography=bio)
            self._session.add(user)
        else:
            line.username = name
            line.posts = posts_n
            line.following = followers_n
            line.followers = followers_n
            line.biography = bio
        if commit:
            self._session.commit()

    def insert_or_update_post(self,
                              pic_id: str,
                              pic_timestamp: int,
                              pic_stars: int,
                              pic_comments: int,
                              pic_url: str,
                              pic_uid: str,
                              commit=True):
        line = self._session.query(Post)\
            .filter(Post.id == pic_id)\
            .one_or_none()
        if line is None:
            post = Post(id=pic_id,
                        timestamp=pic_timestamp,
                        stars=pic_stars,
                        comments=pic_comments,
                        url=pic_url,
                        uid=pic_uid)
            self._session.add(post)
        else:
            line.timestamp = pic_timestamp
            line.stars = pic_stars
            line.comments = pic_comments
            line.url = pic_url
            line.uid = pic_uid
        if commit:
            self._session.commit()

    def get_uid_list(self) -> list:
        sqlRT = self._session.query(User.id).all()
        rt = []
        for line in sqlRT:
            rt.append(line[0])
        return rt

    def get_user_list(self) -> list:
        sqlRT = self._session.query(User.id, User.username).all()
        rt = []
        for line in sqlRT:
            rt.append({"uid": line[0], "username": line[1]})
        return rt

    def get_pic_id_list(self) -> list:
        sqlRT = self._session.query(Post.id).all()
        rt = []
        for line in sqlRT:
            rt.append(line[0])
        return rt

    def get_pic_list(self) -> list:
        sqlRT = self._session.query(Post.id, Post.url).all()
        return sqlRT

    def check_uid_exist(self, Uid: str) -> bool:
        sqlRT = self._session\
                .query(User.id)\
                .filter(User.id == Uid)\
                .one_or_none()
        return (sqlRT is not None)

    def update_one_user_data(self, data: dict):
        self.insert_or_update_user(data["uid"], data["username"],
                                   data["posts"], data["following"],
                                   data["followers"], data["biography"])
        posts_list = []
        posts_list = data["blogs"]
        for blog in posts_list:
            self.insert_or_update_post(blog["pic_id"], blog["pic_time_stamp"],
                                       blog["pic_stars"], blog["pic_comments"],
                                       blog["pic_url"], data["uid"])
        # self._session.commit()

    def get_one_user_data(self, uid) -> dict:
        rt = {}
        if self.check_uid_exist(uid):
            sqlRT0 = self._session.query(User)\
                .filter(User.id == uid).one()
            rt["uid"] = sqlRT0.id
            rt["username"] = sqlRT0.username
            rt["biography"] = sqlRT0.biography
            rt["posts"] = sqlRT0.posts
            rt["following"] = sqlRT0.following
            rt["followers"] = sqlRT0.followers
            sqlRT1 = self._session.query(Post)\
                .filter(Post.uid == uid)\
                .all()
            blogs = []
            for line in sqlRT1:
                blog = {}
                blog["pic_id"] = line.id
                blog["pic_time_stamp"] = line.timestamp
                blog["pic_stars"] = line.stars
                blog["pic_comments"] = line.comments
                blog["pic_url"] = line.url
                blogs.append(blog)
            rt["blogs"] = blogs
            return rt
        else:
            return None

    def get_userless_data(self) -> list:
        sqlRT = self._session\
            .query(User.posts, User.following, User.followers, User.biography)\
            .all()
        return sqlRT

    def get_idless_data(self) -> list:
        sqlRT = self._session\
            .query(Post.timestamp, Post.comments, Post.stars)\
            .all()
        return sqlRT
