import pytest
import pykeepass

from MergeKeepass.keepassmerge import merge_databases

def test_merge_databases():
    assert not merge_databases([ 'testing/DB1.kdbx', 'testing/DB2.kdbx' ], 'testing/DB-out.kdbx', 'test')

