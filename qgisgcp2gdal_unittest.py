#!/usr/bin/env python
from __future__ import print_function
import qgisgcp2gdal
import unittest
import StringIO
import sys

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        
        self.str = StringIO.StringIO()
        sys.stdout = self.str
        print("mapX,mapY,pixelX,pixelY,enable")
        print("146.8617631025457797,-24.58564294366027525,", end="")
        print("1273.98092031425358073,-71.32435465768789129,1")
        print("147.77097875827593043,-24.72826500730421628,", end="")
        print("1339.56453423120092339,81.58810325476979131,0")
        print("148.39588858976847519,-25.43386890112162035,", end="")
        print("1386.36026936026928524,-132.38496071829399625,0")
        print("148.24576010172222595,-26.05877873261416511,", end="")
        print("1375.05274971941639706,178.48484848484844179,1")
        print("150.21431990122874822,-26.13571958273787033,", end="")
        print("1517.70145903479260596,-183.87766554433224542,1")
        print("151.22018077113867207,-26.37967837581303954,", end="")
        print("1590.93939393939422189,201.62177328844001067,1")
        sys.stdout = sys.__stdout__

        # Test output sould look like this
        self.gcp =" -gcp 1273.98092031425358073 71.3243546577 146.8617631025457797 -24.58564294366027525 -gcp 1375.05274971941639706 178.484848485 148.24576010172222595 -26.05877873261416511 -gcp 1517.70145903479260596 183.877665544 150.21431990122874822 -26.13571958273787033 -gcp 1590.93939393939422189 201.621773288 151.22018077113867207 -26.37967837581303954"

    def test_parse(self):

        self.str.seek(0)
        self.assertEqual(self.gcp, qgisgcp2gdal.parse(self.str))


if __name__ == '__main__':
    unittest.main()


