from app.model import Timeslot
from app import db

def update_week(open_dict, week):
    for key, value in open_dict.items():
        hour, index = key.split('/')
        slot = Timeslot.query.filter_by(week=week, index=index, time=hour).first()
        if slot.open and value:
            pass
        else:
            slot.open = value
            db.session.commit()


def get_week(week):
    slots = Timeslot.query.filter_by(week=week)
    slots_dic = {}
    for slot in slots:
        key = str(slot.time) + '/' + str(slot.index)
        slots_dic[key] = [slot.open, slot.user_id]
    return slots_dic
