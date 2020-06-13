from pykeepass import PyKeePass
from datetime import datetime
from dateutil import tz
import itertools

addedAndModifiedEntries = []

class NoGroupException(Exception):
    pass

class NoEntryException(Exception):
    pass

def copy_group(group1, group2, debug=False):
    if group1.name:
        group2.username=group1.username
    if group1.icon:
        group2.icon=group1.icon
    if group1.notes:
        group2.notes=group1.notes
    group2.touch(modify=True)
    if debug:
        print("Updated group ",group2)

def add_group(group, db, debug=False):
    parentgroup = db.find_groups(path=group.parentgroup.path)
    if not parentgroup:
        add_group(group.parentgroup, db)
    parentgroup = db.find_groups(path=group.parentgroup.path)
    if not parentgroup:
        raise NoGroupException
    args = {'destination_group':parentgroup}
    if group.name:
        args['group_name'] = group.name
    if group.icon:
        args['icon'] = group.icon
    if group.notes:
        args['notes'] = group.notes
    print(args)
    new_group = db.add_group(**args)
    if debug:
        print("Added group ",args)

def sync_groups(db1, db2, debug=False):
    for group in db1.groups:
        if group.name == 'Recycle Bin' or 'Recycle Bin' in group.path:
            continue
        other_group = db2.find_groups(path=group.path)
        if not other_group:
            add_group(group, db2)
        elif group.mtime > other_group.mtime:
            copy_group(group, db2, debug)


def copy_entry(entry1, entry2, debug=False):
    if entry1.title:
        entry2.title=entry1.title
    if entry1.username:
        entry2.username=entry1.username
    if entry1.password:
        entry2.password=entry1.password
    if entry1.url:
        entry2.url=entry1.url
    if entry1.notes:
        entry2.notes=entry1.notes
    if entry1.expiry_time:
        entry2.expiry_time=entry1.expiry_time
    if entry1.tags:
        entry2.tags=entry1.tags
    if entry1.icon:
        entry2.icon=entry1.icon
    entry2.touch(modify=True)

def add_entry(entry, db, debug=False):
    parentgroup = db.find_groups(path=entry.parentgroup.path)
    if not parentgroup:
        raise NoGroupException
    args = {'destination_group':parentgroup}
    if entry.title:
        args['title'] = entry.title
    if entry.username:
        args['username'] = entry.username
    if entry.password:
        args['password'] = entry.password
    if entry.url:
        args['url'] = entry.url
    if entry.notes:
        args['notes'] = entry.notes
    if entry.expires and entry.expiry_time:
        args['expiry_time'] = entry.expiry_time
    if entry.tags:
        args['tags'] = entry.tags
    if entry.icon:
        args['icon'] = entry.icon

    new_entry = db.add_entry(**args)
    if debug:
        print("Added entry",args)
    addedAndModifiedEntries.append(parentgroup.path+new_entry.title)
    print(addedAndModifiedEntries)

def sync_entries(db1, db2, debug=False):
    for entry in db1.entries:
        other_entry = db2.find_entries(path=entry.path)
        if entry.parentgroup.name == 'Recycle Bin':
            continue
        if other_entry == None:
            add_entry(entry, db2)
        elif not entry.title in addedAndModifiedEntries:
            if entry.mtime > other_entry.mtime:
                addedAndModifiedEntries.append(entry.title)
                if debug:
                    print("Updated entry : ", other_entry)
                other_entry.save_history()
                copy_entry(other_entry, entry)
            elif entry.mtime < other_entry.mtime:
                addedAndModifiedEntries.append(entry.title)
                if debug:
                    print("Updated entry : ", entry)
                entry.save_history()
                copy_entry(entry, other_entry)


def sync_custom_properties(db1, db2, debug=False):
    for entry in db1.entries:
        if entry.parentgroup.name == 'Recycle Bin':
            continue
        other_entry = db2.find_entries(path=entry.path)
        if other_entry == None:
            raise NoEntryException
        for property_key,property_value in entry.custom_properties.items():
            other_property = other_entry.get_custom_property(property_key)
            if not other_property:
                new_property = other_entry.set_custom_property(property_key,property_value)
                if debug:
                    print('Added property : {',property_key,' : `'+property_value+'`}')

def merge_two_databases(file_database1,
                   file_database2,
                   file_output_database,
                   master_password,
                   debug=False):
    kp1 = PyKeePass(file_database1, password=master_password)
    kp2 = PyKeePass(file_database2, password=master_password)
    sync_groups(kp2,kp1, debug=debug)
    sync_entries(kp2,kp1, debug=debug)
    sync_custom_properties(kp2,kp1, debug=debug)

    kp1.save(filename=file_output_database)


def merge_databases(file_input_databases,
                    file_output_database,
                    master_password,
                    debug=False):
    if len(file_input_databases) == 1:
        copyfile(file_input_databases[0],file_output_database)
        return
    previous_file_db = file_input_databases[0]
    for file_db in itertools.islice(file_input_databases, 1, None):
        merge_two_databases(previous_file_db,
                            file_db,
                            file_output_database,
                            master_password,
                            debug)
        previous_file_db = file_output_database