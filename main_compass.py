#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Local import
import globals_and_constants
from addLogtoFile import addLogFile, createNewFile
import getListDataLuce
import getListDataGas
import getBusinessLuce
from dbTools import (
    readInputFromMysql,
    loadCSVtoDB,
    readPersonalData,
    checkBusinessDataToday,
    loadCSVtoDB1,
)

# pip installation import
from fake_useragent import UserAgent
from python_ghost_cursor import path
import pandas as pd
import MySQLdb as mysql
from MySQLdb._exceptions import OperationalError, DataError
from tqdm import tqdm

# python import
import numpy as np
from datetime import datetime
import json
import time
import traceback
import random
import sys
import shutil
import os
import threading
from Update_heartbeat import update_heartbeat

def mainInit():
    try:
        workGroup = int(sys.argv[1])
    except:
        workGroup = 1
    try:
        refreshFromDate = sys.argv[2]
    except:

        fetching_date = datetime.now().strftime("%Y-%m-%d")
        refreshFromDate = fetching_date
    # global value init()
    csvFolderPath = "csvdata"
    errfilePath = "errfile"
    logPath = "logz"
    if not os.path.exists(csvFolderPath):
        os.makedirs(csvFolderPath)
    if not os.path.exists(errfilePath):
        os.makedirs(errfilePath)
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    globals_and_constants._init()
    globals_and_constants.set_value("workGroup", workGroup)
    update_heartbeat()

    createNewFile()

def split_list(lst, m):
    n = int(len(lst) / m)
    if n == 0:
        n = 1
    return [lst[i : i + n] for i in range(0, len(lst), n)]



def main():
    mainInit()



if __name__ == "__main__":
    main()

