from app.model import Timeslot, User, DateTimeSlot, ScheduleRange
from app.update_schedule import get_email_to_name, get_name_to_email
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
    """ This function returns a list of dates that should be deleted from the
    database and a list of dates that should be added to the database. """
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
    """ This function add or delete dates accroding to the old and new
    date range. """
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
    """ This function retrieves the data from DateTimeSlot database. """
    slots = DateTimeSlot.query.filter_by(date=date)
    #print(date)
    slots_dic = {}
    email_dic = get_email_to_name()
    for slot in slots:
        key = str(slot.time) + '/' + str(slot.index)
        if slot.user_id is not None:
            name = email_dic[slot.user_id]
            slots_dic[key] = [slot.open, name]
        else:
            week = convert_to_date(date, 1).weekday()
            slot_week = Timeslot.query.filter_by(week=week, time=slot.time, index=slot.index).first()
            if slot_week.user_id:
                slots_dic[key] = [slot.open, None, True]
            else:
                slots_dic[key] = [slot.open, None, False]
            """ The True and False above indicate if this slot is permanently
            or temporarily open. """
    #print(slots_dic)
    return slots_dic


def update_date_schedule(slots_dic, date):
    email_dic = get_name_to_email()
    for key, value in slots_dic.items():
        time, index = key.split('/')
        slot = DateTimeSlot.query.filter_by(date=date, time=time, index=index).first()
        if value:
            slot.user_id = email_dic[value]
        else:
            slot.user_id = None
    db.session.commit()


def update_from_current(week, slot_dic, parameter):
    """ This function expects a week index (0-6) to update DateTimeSlot
    database from current date to the end of schedule period. """
    date = datetime.date.today() + datetime.timedelta(days=1)
    # Any permanet change takes effects start from the next week
    schedule_range = ScheduleRange.query.all()[0]
    end_date = convert_to_date(schedule_range.end_date, 0)
    for key, value in slot_dic.items():
        time, index = key.split('/')
        change_parameter = value
    while True:
        if date.weekday() == week:
            break
        else:
            date = date + datetime.timedelta(days=1)
    while True:
        if date <= end_date:
            slot = DateTimeSlot.query.filter_by(date=date.strftime('%Y-%m-%d'),
                                                time=time, index=index).first()
            if parameter == 'user_id':
                slot.user_id = change_parameter
            elif parameter == 'open':
                slot.open = change_parameter
            else:
                raise ValueError('Timeslot database doesn\'t have column called ' + str(parameter))
            date = date + datetime.timedelta(weeks=1)
            continue
        db.session.commit()
        break
    slot = DateTimeSlot.query.filter_by()
