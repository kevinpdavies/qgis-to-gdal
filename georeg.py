#!/usr/bin/env python
from __future__ import print_function
import glob
import os
from os.path import basename, exists
import subprocess
from qgisgcp2gdal import parse

''' Georegister images in ../pdf, using ../gcp, and output to ../tif'''
''' Optional extent for output specified in ../ext '''
''' Optional polygon shapefile of areas to "white out" in ../shp '''
if __name__ == "__main__":

    # Get a list of PDF files based on the working folder
    pdfs = glob.glob(os.getcwd() + "/../pdf/*.pdf")
    pdfs.sort()

    for pdf in pdfs:

        gcp = os.getcwd() + "/../gcp/" + basename(pdf) + ".points"
        if not exists(gcp):
            # print("GCP file not found for PDF:", basename(pdf))
            continue

        with open(gcp) as f:

            gcp = parse(f)
            tmp =  "/tmp/" + basename(pdf) + ".tif"
            cmd = "/usr/bin/gdal_translate " + gcp
            cmd += " -of GTiff -a_srs EPSG:4283 "
            cmd += pdf + " " + tmp
            subprocess.check_call(cmd, shell=True)

            tif = os.getcwd() + "/../tif/" + \
                basename(pdf).replace(".pdf", ".tif")
            cmd = "/usr/bin/gdalwarp -r near -order 1 -co COMPRESS=NONE "
            cmd += "-overwrite "
            ext = os.getcwd() + "/../ext/" + basename(pdf) + ".ext"
            if os.path.exists(ext):
	    	with open(ext) as ext_f:
                    cmd += "-te " + ext_f.read().rstrip("\n")
            cmd += " " + tmp + " " + tif
            subprocess.check_call(cmd, shell=True)
            os.remove(tmp)

            shp = os.getcwd() + "/../shp/" + \
                basename(pdf).replace(".pdf", ".shp")
            if os.path.exists(shp):
                cmd = "gdal_rasterize -b 1 -b 2 -b 3 "
                cmd += "-burn 255 -burn 255 -burn 255 "
                cmd += "-l " + basename(shp)[:-4] + " " + shp + " "
                cmd += tif
                subprocess.check_call(cmd, shell=True)
