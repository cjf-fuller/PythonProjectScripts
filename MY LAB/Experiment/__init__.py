# -*- coding: utf-8 -*-
"""
Init file
"""

import os

#---------------------------------------------------------------------
#  Add main directory to python path.
#   traverses up the directory tree until it finds it;s in the target named directory
#---------------------------------------------------------------------

targetdir = "MY LAB"
dirimax = 10

# Check if the dir is already there....
path0 = os.sys.path[0]
if os.path.split(path0)[1] != targetdir :

    # Gets current directory
    APP_ROOTDIR = os.path.dirname(os.path.abspath(__file__))

    diri = 1
    while (not (os.path.split(APP_ROOTDIR)[1] == targetdir)) :

        APP_ROOTDIR = os.path.dirname(APP_ROOTDIR)
        diri = diri + 1

        if diri >dirimax :
            print "Warning: Cannot find MY LAB Directory."
            break

    os.sys.path.insert(1,APP_ROOTDIR)
