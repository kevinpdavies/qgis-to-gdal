#!/usr/bin/env python
from __future__ import print_function
import csv
from operator import itemgetter
import sys

""" Parse a file-like object containg QGIS GCP data"""
def parse(f):
    
    reader = csv.reader(f)
    next(reader, None)  # Skip headers
    out = ""
    for row in reader:
        if int(row[4]): # Whether GCP is 'enabled'
            # Image coords come before map coords in gdal
            # QGIS incorrectly outputs negative image y coords - fix this too
            out += " -gcp {:} {:} {:} {:}".format(row[2], abs(float(row[3])), row[0], row[1])
    return out

if __name__ == "__main__":
    
    parse(sys.stdin)
