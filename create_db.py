from WordleRoyale import app, db, models
import csv

with app.app_context():
    db.create_all()

    with db.session.begin():
        db.session.query(models.Word).delete()
        #db.session.query(models.RankedSession).delete()
        #db.session.query(models.DailySession).delete()
        #db.session.query(models.Streak).delete()
        db.session.query(models.Score).delete()
        db.session.commit()

    with open("./instance/words.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # skip header
        for row in reader:
            new_word = models.Word(word = row[0].upper())
            db.session.add(new_word)
        db.session.commit()