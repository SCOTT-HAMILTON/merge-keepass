# merge-keepass

Keepass Databases 1.x/2.x Merging module and command line utility

![Travis CI build status](https://travis-ci.org/SCOTT-HAMILTON/merge-keepass.svg?branch=master)

## Building
This project is configured for setuptools

## What it does
This updates/adds new groups, new entries and new fields.
Unfortunatly, due to a bug in pykeepass, it cannot merge attachments.

## Usage :

### Command Line Utility
```
Usage: merge_keepass [OPTIONS] [INPUT_DATABASES]... OUTPUT_DATABASE

Options:
  -p, --password TEXT
  -d, --debug
  -c, --continue-on-error
  --help                   Show this message and exit.
```

### KeepassMerger
If you want to directly use this in your python code,
you can use the python module keepassmerge as so :

 > merging multiple databases
```python
from MergeKeepass.keepassmerge import KeepassMerger
from getpass import getpass

input_databases = [
	'../db1.kdbx',
	'db2.kdbx',
	'local/mydb.kdbx',
]
output_database = 'out.kdbx'

password = getpass()

merger = KeepassMerger()
got_errors = merger.merge_databases(input_databases,
			     output_database,
			     password,
			     debug=False,
			     continue_on_error=False)
if got_errors:
	# Errors occurred
	pass
else:
	# No erros, merging succeeded
	pass
```
 > merging two databases
```python
from MergeKeepass.keepassmerge import KeepassMerger
from getpass import getpass

database1  = '../db1.kdbx'
database2 = 'local/mydb.kdbx'
output_database = 'out.kdbx'

password = getpass()

merger = KeepassMerger()
try:
	merger.merge_two_databases(database1,
				database2,
				output_database,
				password,
				debug=False)
except  DB1WrongPasswordError:
	pass
	# Password of database1 is wrong
except  DB2WrongPasswordError:
	pass
	# Password of database2 is wrong
```

### Requirements
 - [pykeepass](https://github.com/libkeepass/pykeepass) >= 3
 - [click](https://github.com/pallets/click)

### Help

This is just a little project, but feel free to fork, change, extend or correct the code.

## Development

When testing, it's convenient to use this nix command to run all the tests while
avoiding to build the whole nix derivation : 
```shell_session
$ cd /path/to/merge-keepass
$ nix-shell --command "run_test"
```

## License
merge-keepass is delivered as it is under the well known MIT License.

**References that helped**
 - [pykeepass repos] : <https://github.com/libkeepass/pykeepass>
 - [click documentation] : <https://click.palletsprojects.com/en/7.x/#documentation>

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [pykeepass repos]: <https://github.com/libkeepass/pykeepass>
   [click documentation]: <https://click.palletsprojects.com/en/7.x/#documentation>
