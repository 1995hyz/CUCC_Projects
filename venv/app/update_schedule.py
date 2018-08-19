from app.model import Timeslot, User
from app import db


def get_name_to_id():
    name_dic = {}
    users = User.query.all()
    for user in users:
        full_name = user.first_name + ' ' + user.last_name
        name_dic[full_name] = user.id
    return name_dic


def get_id_to_name():
    id_dic = {}
    users = User.query.all()
    for user in users:
        full_name = user.first_name + ' ' + user.last_name
        id_dic[user.id] = full_name
    return id_dic


from app.update_daily_schedule import update_from_current
# Because update_daily_schedule depends on the two functions above


def update_week(open_dict, week):
    for key, value in open_dict.items():
        hour, index = key.split('/')
        slot = Timeslot.query.filter_by(week=week, index=index, time=hour).first()
        if slot.open == value:
            pass
        else:
            slot.open = value
            db.session.commit()
            update_from_current(week, {key: value}, 'open')


def update_week_schedule(slots_dic, week):
    """ This function updates the permanent shedule in Timeslot database. """
    id_dic = get_id_to_name()
    name_dic = get_name_to_id()
    name_dic[None] = None
    id_dic[None] = None
    invalid_dic = {}
    for key, value in slots_dic.items():
        hour, index = key.split('/')
        slot = Timeslot.query.filter_by(week=week, index=index, time=hour).first()
        if value == '':
            value = None
        if value != id_dic[slot.user_id]:
            if value in name_dic:
                if value is None:
                    update_from_current(week, {key: None}, 'user_id')
                    slot.user_id = name_dic[value] # None
                    db.session.commit()
                else:
                    user = User.query.filter_by(id=name_dic[value]).first()
                    if (user.privilege and index == str(0)) or (not user.privilege and index != 0):
                        # Check if the new user is supervisor or operator
                        update_from_current(week, {key: name_dic[value]}, 'user_id')
                        slot.user_id = name_dic[value]
                        db.session.commit()
                    else:
                        invalid_dic[key] = value
            else:
                if value is not None:
                    invalid_dic[key] = value
    return invalid_dic


def get_week(week):
    slots = Timeslot.query.filter_by(week=week)
    slots_dic = {}
    id_dic = get_id_to_name()
    for slot in slots:
        key = str(slot.time) + '/' + str(slot.index)
        if slot.user_id is not None:
            name = id_dic[slot.user_id]
            slots_dic[key] = [slot.open, name]
        else:
            slots_dic[key] = [slot.open, slot.user_id]
    return slots_dic


def get_open(week):
    slots = Timeslot.query.filter_by(week=week)
    slots_dic = {}
    for slot in slots:
        key = str(slot.time) + '/' +str(slot.index)
        slots_dic[key] = slot.open
    return slots_dic
