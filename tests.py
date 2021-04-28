import pytest
import pykeepass

from MergeKeepass.keepassmerge import KeepassMerger

def test_merge_databases():
    merger = KeepassMerger()
    assert not merger.merge_databases(
            [ 'testing/DB1.kdbx', 'testing/DB2.kdbx' ],
            'testing/DB-out.kdbx', 'test')

