#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import globals_and_constants
from datetime import datetime
from Update_heartbeat import update_heartbeat


def createNewFile():
    lineString = f"\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"

    current_date_and_time = datetime.now().strftime("%Y%m%d%H%M%S")

    logkey = "Log Begin"
    logStringLine = ""
    logTimeString = "%s%s\n%s\n%s" % (
        lineString,
        current_date_and_time,
        logkey,
        logStringLine,
    )

    if False:
        print(logTimeString, flush=True)
    # """
    fileNameZ = f"logz/logZhang_{current_date_and_time}.txt"
    logFile = open(fileNameZ, "w", encoding="utf-8")
    logFile.write(logTimeString)
    logFile.close()
    globals_and_constants.set_value("fileNameZ", fileNameZ)
    # """


def addLogFile(logkey, logStringLine, isPrint=False):

    lineString = f"\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"
    update_heartbeat()
    current_date_and_time = datetime.now()
    logTimeString = "--%s-- --%s-- --%s--\n" % (
        current_date_and_time,
        logkey,
        logStringLine,
    )

    if isPrint:
        print(logTimeString, flush=True)
    # """
    filePathz = globals_and_constants.get_value("fileNameZ")
    if filePathz is not None:
        logFile = open(filePathz, "a", encoding="utf-8")
        logFile.write(logTimeString)
        logFile.close()
    else:
        raise Exception("filePathz is null")
    # """
