from WordleRoyale import db


class User(db.Model):
    username: db.Mapped[str] = db.mapped_column(primary_key=True)
    password: db.Mapped[str]

class Word(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    word: db.Mapped[str]

class Session(db.Model):
    session_id: db.Mapped[str] = db.mapped_column(primary_key=True)
    solution: db.Mapped[str]
    attempt1: db.Mapped[str]
    attempt2: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt3: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt4: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt5: db.Mapped[str | None] = db.mapped_column(nullable=True)
    attempt6: db.Mapped[str | None]= db.mapped_column(nullable=True)
