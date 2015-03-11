#!/usr/bin/env python
from __future__ import print_function
import glob
import os
from os.path import basename, exists
import subprocess
from qgisgcp2gdal import parse

''' Georegister images in ../pdf, using ../gcp, and output to ../tif'''
if __name__ == "__main__":

    # Get a list of PDF files based on the working folder
    pdfs = glob.glob(os.getcwd() + "/../pdf/*.pdf")
    for pdf in pdfs:

        gcp = os.getcwd() + "/../gcp/" + basename(pdf) + ".points"
        if not exists(gcp):
            # print("GCP file not found for PDF:", basename(pdf))
            continue

        with open(gcp) as f:
            gdal_gcp = parse(f)
            tmp_tif =  "/tmp/" + basename(pdf) + ".tif"
            cmd = "/usr/bin/gdal_translate " + gdal_gcp + " -of GTiff -a_srs EPSG:4283 "
            cmd += pdf + " " + tmp_tif
            subprocess.check_call(cmd, shell=True)
            out_tif = os.getcwd() + "/../tif/" + basename(pdf).replace(".pdf", ".tif")
            cmd = "/usr/bin/gdalwarp -r near -order 1 -co COMPRESS=NONE "
            cmd += tmp_tif + " " + out_tif
            subprocess.check_call(cmd, shell=True)
            os.remove(tmp_tif)
