from WordleRoyale import db
import datetime



class Word(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    word: db.Mapped[str]

class SessionBase(db.Model):
    __abstract__ = True
    solution: db.Mapped[str]
    status: db.Mapped[str]
    attempt1: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt2: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt3: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt4: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt5: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt6: db.Mapped[str | None]= db.mapped_column(nullable=True)

class DailySession(SessionBase):
    session_id: db.Mapped[str] = db.mapped_column(primary_key=True)

class RankedSession(SessionBase):
    user_id: db.Mapped[str] = db.mapped_column(primary_key=True)

class Streak(db.Model):
    user_id: db.Mapped[str] = db.mapped_column(primary_key=True)
    count: db.Mapped[int]
    last_update: db.Mapped[datetime.datetime]

class Score(db.Model):
    user_id: db.Mapped[str] = db.mapped_column(primary_key=True)
    username: db.Mapped[str]
    score: db.Mapped[int]


def get_word(index):
    return Word.query.get(index)

def get_daily_session(session_id):
    return DailySession.query.get(session_id)

def get_ranked_session(session_id):
    return RankedSession.query.get(session_id)

def get_streak(session_id):
    return Streak.query.get(session_id)
