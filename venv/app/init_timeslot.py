from app import db
from app.model import Timeslot

def create_week():
    slot = Timeslot.query.all()
    if not slot:
        for index in range(4):
            for week in range(7):
                for time in range(24):
                    timeslot = Timeslot(index=index, time=time,
                                        week=week, open=False)
                    db.session.add(timeslot)
                    db.session.commit()
