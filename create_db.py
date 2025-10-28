from WordleRoyale import app, db, models
from instance.word_list import WORDS
from config import salt

with app.app_context():
    db.create_all()

    with db.session.begin():
        db.session.query(models.User).delete()
        db.session.query(models.Word).delete()
        db.session.query(models.Session).delete()
        db.session.commit()

    for word in WORDS:
        new_word = models.Word(word = word)
        db.session.add(new_word)
        db.session.commit()