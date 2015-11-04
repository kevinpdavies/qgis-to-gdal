#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
from os.path import basename
import subprocess
from qgisgcp2gdal import parse

def go(cmd): 
    out = subprocess.check_output(cmd, shell=True)
    print(out)
    if "done" not in out: # Some failures don't set the exit code so check
        raise Exception("gdal_translate failed")
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Georegister an image ' \
        'based on ground control points collected in QGIS.')
    parser.add_argument("src_image", help="source image file to be registered")
    parser.add_argument("gcp_file", help="ground control points collected in QGIS")
    parser.add_argument("EPSG", help="target coordinate system e.g. EPSG:4283")
    parser.add_argument("dst_image", help="destination GeoTIFF image file to be created")
    parser.add_argument("-p", "--poly_order", type=int, default=1, choices=[1,2,3], \
                        help="polynomial transormation order")
    parser.add_argument("-e", "--extent_file", help="text file describing output extent")
    parser.add_argument("-s", "--shapefile", \
                        help="polygon shape file where image should be whitened")
    parser.add_argument("-v", "--verbose", action="store_true", \
                        help="print detailed gdal commands")
    
    args = parser.parse_args()

    with open(args.gcp_file) as f:

        gcp = parse(f)
        tmp =  args.dst_image + ".tmp.tif"
        cmd = "gdal_translate " + gcp
        cmd += " -of GTiff -a_srs " + args.EPSG + " "
        cmd += args.src_image + " " + tmp
        if args.verbose: print(cmd)
        go(cmd)
        
        cmd = "gdalwarp -r near -order " + str(args.poly_order) + " "
        cmd += "-co COMPRESS=NONE "
        # TODO: This should be optional
        cmd += "-overwrite "
        if args.extent_file:
            with open(args.extent_file) as ext_f:
                cmd += "-te " + ext_f.read().rstrip("\n")
        cmd += " " + tmp + " " + args.dst_image
        if args.verbose: print(cmd)
        go(cmd)
        os.remove(tmp)

        if (args.shapefile):
            cmd = "gdal_rasterize -b 1 -b 2 -b 3 "
            cmd += "-burn 255 -burn 255 -burn 255 "
            cmd += "-l " + basename(args.shapefile)[:-4] + " "
            cmd += args.shapefile + " "
            cmd += args.dst_image
            if args.verbose: print(cmd)
            subprocess.check_call(cmd, shell=True)
