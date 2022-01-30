from click import echo
from datetime import datetime
from dateutil import tz
import itertools
from pykeepass import PyKeePass

from pkg_resources import parse_version, get_distribution

pykeepass_version = get_distribution("pykeepass").version

if parse_version(pykeepass_version) < parse_version("3.2.1"):
    from pykeepass.exceptions import CredentialsIntegrityError

    CredentialsError = CredentialsIntegrityError
else:
    from pykeepass.exceptions import CredentialsError

from shutil import copyfile


class NoGroupException(Exception):
    pass


class NoEntryException(Exception):
    pass


class NoTitleException(Exception):
    pass


class DB1WrongPasswordError(Exception):
    pass


class DB2WrongPasswordError(Exception):
    pass


class WrongPasswordError(Exception):
    pass


class KeepassMerger:
    def __init__(self):
        self.addedAndModifiedEntries = []

    def copy_group(self, group1, group2, debug=False):
        if group1.name:
            group2.name = group1.name
        if group1.icon:
            group2.icon = group1.icon
        if group1.notes:
            group2.notes = group1.notes
        group2.mtime = group1.mtime
        if debug:
            echo("Updated group ", group2)

    def add_group(self, group, db, debug=False):
        parentgroup = db.find_groups(path=group.parentgroup.path)
        if not parentgroup:
            self.add_group(group.parentgroup, db)
        parentgroup = db.find_groups(path=group.parentgroup.path)
        if not parentgroup:
            raise NoGroupException
        args = {"destination_group": parentgroup}
        if group.name:
            args["group_name"] = group.name
        if group.icon:
            args["icon"] = group.icon
        if group.notes:
            args["notes"] = group.notes
        echo(args)
        new_group = db.self.add_group(**args)
        if debug:
            echo("Added group ", args)

    def sync_groups(self, db1, db2, debug=False):
        for group in db1.groups:
            if group.name == "Recycle Bin" or "Recycle Bin" in group.path:
                continue
            other_group = db2.find_groups(path=group.path)
            if not other_group:
                self.add_group(group, db2)
            elif group.mtime > other_group.mtime:
                self.copy_group(group, db2, debug)

    def copy_entry(self, entry1, entry2, debug=False):
        if entry1.title:
            entry2.title = entry1.title
        if entry1.username:
            entry2.username = entry1.username
        if entry1.password:
            entry2.password = entry1.password
        if entry1.url:
            entry2.url = entry1.url
        if entry1.notes:
            entry2.notes = entry1.notes
        if entry1.expiry_time:
            entry2.expiry_time = entry1.expiry_time
        if entry1.tags:
            entry2.tags = entry1.tags
        if entry1.icon:
            entry2.icon = entry1.icon
        entry2.touch(modify=True)

    def add_entry(self, entry, db, debug=False):
        parentgroup = db.find_groups(path=entry.parentgroup.path)
        if not parentgroup:
            raise NoGroupException
        args = {"destination_group": parentgroup}
        parentgroup._element.append(entry._element)
        if debug:
            echo("Added entry", args)
        print("Pykeepass Version : ", pykeepass_version)
        if parse_version(pykeepass_version) < parse_version("3.2.1"):
            self.addedAndModifiedEntries.append(new_entry.uuid)
        echo(self.addedAndModifiedEntries)

    def move_entry(self, db, entry, other_entry):
        db.move_entry(entry, other_entry.parentgroup)

    def sync_entries(self, db1, db2, debug=False):
        for entry in db1.entries:
            other_entry = db2.find_entries(uuid=entry.uuid)
            if not other_entry:
                self.add_entry(entry, db2)
            assert len(other_entry) == 1
            other_entry = other_entry[0]
            moved = False
            if entry.path != other_entry.path:
                moved = True
            if (
                entry.parentgroup.name == "Recycle Bin"
                or other_entry.parentgroup.name == "Recycle Bin"
            ):
                continue
            elif not entry.uuid in self.addedAndModifiedEntries:
                if entry.mtime > other_entry.mtime:
                    self.addedAndModifiedEntries.append(entry.uuid)
                    if debug:
                        echo("Updated entry : ", other_entry)
                    other_entry.save_history()
                    self.copy_entry(other_entry, entry)
                    if moved:
                        self.move_entry(db2, other_entry, entry)
                elif entry.mtime < other_entry.mtime:
                    self.addedAndModifiedEntries.append(entry.uuid)
                    if debug:
                        echo("Updated entry : ", entry)
                    entry.save_history()
                    self.copy_entry(entry, other_entry)
                    if moved:
                        self.move_entry(db1, other_entry, entry)

    def sync_custom_properties(self, db1, db2, debug=False):
        for entry in db1.entries:
            other_entry = db2.find_entries(uuid=entry.uuid)
            if other_entry == None:
                raise NoEntryException
            assert len(other_entry) == 1
            other_entry = other_entry[0]
            if (
                entry.parentgroup.name == "Recycle Bin"
                or other_entry.parentgroup.name == "Recycle Bin"
            ):
                continue
            for property_key, property_value in entry.custom_properties.items():
                other_property = other_entry.get_custom_property(property_key)
                if not other_property:
                    new_property = other_entry.set_custom_property(
                        property_key, property_value
                    )
                    if debug:
                        echo(
                            "Added property : {",
                            property_key,
                            " : `" + property_value + "`}",
                        )

    def merge_two_databases(
        self,
        file_database1,
        file_database2,
        file_output_database,
        master_password,
        debug=False,
    ):
        try:
            kp1 = PyKeePass(file_database1, password=master_password)
        except CredentialsError:
            raise DB1WrongPasswordError
        try:
            kp2 = PyKeePass(file_database2, password=master_password)
        except CredentialsError:
            raise DB2WrongPasswordError

        self.sync_groups(kp2, kp1, debug=debug)
        self.sync_entries(kp2, kp1, debug=debug)
        self.sync_custom_properties(kp2, kp1, debug=debug)

        kp1.save(filename=file_output_database)

    def merge_databases(
        self,
        file_input_databases,
        file_output_database,
        master_password,
        continue_on_error=False,
        debug=False,
    ):
        if len(file_input_databases) == 1:
            copyfile(file_input_databases[0], file_output_database)
            return
        previous_file_db = file_input_databases[0]
        got_errors = False
        for file_db in itertools.islice(file_input_databases, 1, None):
            try:
                self.merge_two_databases(
                    previous_file_db,
                    file_db,
                    file_output_database,
                    master_password,
                    debug,
                )
            except DB1WrongPasswordError:
                got_errors = True
                if continue_on_error:
                    previous_file_db = file_db
                    continue
                raise WrongPasswordError
            except DB2WrongPasswordError:
                got_errors = True
                if continue_on_error:
                    continue
                raise WrongPasswordError
            previous_file_db = file_output_database
        if continue_on_error:
            return got_errors
