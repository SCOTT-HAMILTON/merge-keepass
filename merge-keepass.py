#! /usr/bin/env python3

import getpass
import argparse
from keepassmerge import merge_two_databases

parser = argparse.ArgumentParser()
parser.add_argument('infilenames', nargs=2)
parser.add_argument('outfilename')
parser.add_argument('-p', '--password')
args = parser.parse_args()

filename = args.infilenames[0]
filename_other = args.infilenames[1]
filename_output = args.outfilename

if args.password:
    master_password = args.password
else:
    master_password = getpass.getpass()

verbose = 0

merge_two_databases(filename,
                filename_other,
                filename_output,
                master_password)
