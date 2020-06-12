#!/usr/bin/env python3

from __future__ import print_function
import sys
import libkeepass
import libkeepass.utils.merge
import itertools
from shutil import copyfile

def merge_two_databases(file_database1,
                   file_database2,
                   file_output_database,
                   master_password,
                   verbose=0):
    try:
        with libkeepass.open(file_database1, password=master_password) as kdb, \
             libkeepass.open(file_database2, password=master_password) as kdb_other:
            found = {}

            kdbm = kdb.merge(kdb_other, metadata=True, debug=(verbose>0),
                             mode=libkeepass.utils.merge.KDB4Merge.MM_OVERWRITE_IF_NEWER)
            with open(file_output_database, 'wb') as output:
                kdb.write_to(output)

            if verbose > 0:
                if verbose > 1:
                    print(kdb.pretty_print().decode('utf-8'))
                    print(kdb_other.pretty_print().decode('utf-8'))

                # Print merge operations to see what occurred during the merge
                print(kdbm.mm_ops)
    except Exception as e:
        import traceback
        print('Could not merge KeePass Databases:\n  %s\n  %s\n%s' % (file_database1, file_database2, str(e)), file=sys.stderr)
        traceback.print_exc()
        sys.exit(2)

def merge_databases(file_input_databases,
                    file_output_database,
                    master_password,
                    verbose=0):
    if len(file_input_databases) == 1:
        copyfile(file_input_databases[0],file_output_database)
        return
    previous_file_db = file_input_databases[0]
    for file_db in itertools.islice(file_input_databases, 1, None):
        merge_two_databases(previous_file_db,
                            file_db,
                            file_output_database,
                            master_password)
        previous_file_db = file_output_database

