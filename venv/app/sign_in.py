from app.model import SignInSlot, DateTimeSlot
from app import db
from app.update_schedule import get_email_to_name
import datetime


def get_min_sec():
    now = datetime.datetime.now()
    return now.minute * 100 + now.second


def generate_sign_in(date, hour):
    """"""
    slots = DateTimeSlot.query.filter_by(date=date, time=hour).all()
    min_sec = get_min_sec()
    if len(slots) == 0:     # No open slots at that hour
        return False
    else:
        for slot in slots:
            if slot.open:
                new_sign_in = SignInSlot(index=slot.index, time=hour,
                                        date=date, user_id=slot.user_id,
                                        signed=None, approved=None,
                                        replace=None, min_sec=min_sec)
                db.session.add(new_sign_in)
        db.session.commit()
        return True


def delete_sign_in(start_date, end_date):
    """ This function searches any SignInSlot slot that is more than
    six month previous than the end_date, and delete such slot. The searching
    process startes at the date "start_date". """
    pass


def get_sign_in(date, hour):
    slots = SignInSlot.query.filter_by(date=date, time=hour).all()
    name_dic = get_email_to_name()
    name_dic[None] = None
    slot_list = []
    if len(slots) == 0:
        if not generate_sign_in(date, hour):
            print('No available slot in current hour.')
            return None
        else:
            slots = SignInSlot.query.filter_by(date=date, time=hour).all()
    for slot in slots:
        temp = {}
        temp['index'] = slot.index
        temp['name'] = name_dic[slot.user_id]
        temp['signed'] = slot.signed
        temp['replace'] = slot.replace
        temp['approved'] = slot.approved
        slot_list.append(temp)
    return slot_list
