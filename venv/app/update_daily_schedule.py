from app.model import Timeslot, User, DateTimeSlot
from app import db
import datetime


def convert_date_integer(date):
    month, day, year = date.split('-')
    return int(year)*1000 + int(month)*100 + int(day)


def convert_from_date(date):
    return str(date.month) + '-' + str(date.day) + '-' + str(date.year)


def convert_to_date(date):
        month, day, year = date.split('-')
        return datetime.date(year=year, month=month, day=day)


def get_update_list(old_start, old_end, new_start, new_end):
    new_start_day = convert_to_date(new_start)
    new_end_day = convert_to_date(new_end)
    old_start_day = convert_to_date(old_start)
    old_end_day = convert_to_date(old_end)
    delete_list = []
    add_list = []
    all_date = DateTimeSlot.query.all()
    for single_date in all_date:
        single_day = convert_to_date(single_date.date)
        if single_day > new_end_day or single_day < new_start_day:
            delete_list.append(single_day)
    position = new_start_day # position serves simliar like single_day above
    while position <= new_end_day:
        if position > old_end_day or position < old_start_day:
            add_list.append(position)
    return [add_list, delete_list]


def update_daily(old_start, old_end, new_start, new_end):
    hours = range(24)
    orders = range(5)
    temp_list = get_update_list(old_start, old_end, new_start, new_end)
    add_list = temp_list[0]
    delete_list = temp_list[1]
    for old_entry in delete_list:
        old_date = DateTimeSlot.query.filter_by(date=old_entry)
        db.session.delete(old_date)
    db.session.commit()
    for new_entry in add_list:
        week = convert_to_date(new_entry).weekday()
        for hour in hours:
            for order in orders:
                slot = Timeslot.query.filter_by(week=week, time=hour, index=order).first()
                date_slot = DateTimeSlot(index=order, time=hour
                                        , date=new_entry, user_id=slot.user_id)
                db.session.add(date_slot)
        db.session.commit()
