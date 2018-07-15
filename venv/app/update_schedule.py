from app.model import Timeslot
from app import db

def update_week(open_dict):
    for key, value in open_dict.items():
        hour, index = key.split('/')
        slot = Timeslot.query.filter_by(index=index, time=hour).first()
        if slot.open and value:
            pass
        else:
            slot.open = value
            db.session.commit()
