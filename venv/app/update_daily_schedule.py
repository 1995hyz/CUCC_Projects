from app.model import Timeslot, User, DateTimeSlot
from app import db
import datetime


def convert_date_integer(date):
    month, day, year = date.split('-')
    return int(year)*1000 + int(month)*100 + int(day)


def update_daily(old_start, old_end, new_start, new_end):
    new_start_num = convert_date_integer(new_start)
    new_end_num = convert_date_integer(new_end)
    old_boundary_num = new_start_num
    all_date = DateTimeSlot.query.all()
    for single_date in all_date:
        single_date_num = convert_date_integer(single_date.date)
        if single_date_num > new_end_num or single_date_num < new_start_num:
            db.session.delete(single_date)
        else:
            old_boundary_num = single_date_num
    db.session.commit()
    new_start_day = datetime.date(year=int(old_boundary_num/10000),
                                    month=int(int(old_boundary_num%10000)/100),
                                    day=int(old_boundary_num%100))
