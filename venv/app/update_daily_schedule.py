from app.model import Timeslot, User, DateTimeSlot
from app.update_schedule import get_email_to_name
from app import db
import datetime


def convert_from_date(date):
    return str(date.month) + '-' + str(date.day) + '-' + str(date.year)


def convert_to_date(date, version):
    if version == 0:
        month, day, year = date.split('-')
        return datetime.date(year=int(year), month=int(month), day=int(day))
    if version == 1:
        year, month, day = date.split('-')
        return datetime.date(year=int(year), month=int(month), day=int(day))


def get_update_list(old_start_day, old_end_day, new_start_day, new_end_day):
    delete_list = []
    add_list = []
    all_date = DateTimeSlot.query.all()
    for single_date in all_date:
        single_day = convert_to_date(single_date.date, 1)
        if single_day > new_end_day or single_day < new_start_day:
            if single_day not in delete_list:
                print('Delete: ' + str(single_day))
                delete_list.append(single_day)
    position = new_start_day # position serves simliar like single_day above
    while position <= new_end_day:
        if position > old_end_day or position < old_start_day:
            print('Add: ' + str(position))
            add_list.append(position)
        try:
            position = position.replace(day=position.day+1)
        except ValueError:
            try:
                position = position.replace(month=position.month+1, day=1)
            except ValueError:
                position = position.replace(year=position.year+1, month=1, day=1)
    return [add_list, delete_list]


def update_daily(old_start, old_end, new_start, new_end):
    hours = range(24)
    orders = range(5)
    temp_list = get_update_list(old_start, old_end, new_start, new_end)
    add_list = temp_list[0]
    delete_list = temp_list[1]
    for old_entry in delete_list:
        old_dates = DateTimeSlot.query.filter_by(date=old_entry)
        for old_date in old_dates:
            db.session.delete(old_date)
    db.session.commit()
    for new_entry in add_list:
        week = new_entry.weekday()
        for hour in hours:
            for order in orders:
                slot = Timeslot.query.filter_by(week=week, time=hour, index=order).first()
                date_slot = DateTimeSlot(index=order, time=hour, open=slot.open,
                                        date=new_entry, user_id=slot.user_id)
                db.session.add(date_slot)
        db.session.commit()


def get_date(date):
    slots = DateTimeSlot.query.filter_by(date=date)
    print(date)
    slots_dic = {}
    email_dic = get_email_to_name()
    for slot in slots:
        key = str(slot.time) + '/' + str(slot.index)
        if slot.user_id is not None:
            name = email_dic[slot.user_id]
            slots_dic[key] = [slot.open, name]
        else:
            slots_dic[key] = [slot.open, slot.user_id]
    print(slots_dic)
    return slots_dic
