#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Local import
import globals_and_constants
from addLogtoFile import addLogFile, createNewFile
from dbTools import (
    readInputFromMysql,
    loadCSVtoDB,
    readPersonalData,
)
import getListDataCompass
# import getListDataAgos
import getListDataUnicredit


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

csvFolderPath = "csvdata"
errfilePath = "errfile"
logPath = "logz"

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
    return workGroup, refreshFromDate

def beginCompasswork(workGroup, refreshFromDate):
    readState, inputDf = readInputFromMysql(refreshFromDate,workGroup,'compass')
    addLogFile("input_dataFrame", inputDf)
    if inputDf is None:
        addLogFile("info", "compass inputDf is None", True)
        return
    
    
    inputDicOriList = inputDf.to_dict("records")
    if len(inputDicOriList) == 0:
        addLogFile("info", "compass inputDf is None 2", True)
        return
    

    allZData = []
    inputCount = len(inputDicOriList)
    for i in tqdm(range(inputCount), desc="compass input Progress:"):
        time.sleep(1)

        addLogFile("workGroup", workGroup)
        try:
            stateOutput, errcode, detailsDic, csvFileName = getListDataCompass.getList(
                inputDicOriList[i]
            )

            addLogFile("DetailsDic", detailsDic)
        except:
            addLogFile("getData fail", "input ID: %d" % inputDicOriList[i]["id"], True)
            addLogFile("Error", traceback.format_exc(), True)
            continue
        state = False
        for n in range(5):
            state = loadCSVtoDB(
                csvFileName,
                globals_and_constants.dbTable["outputTbRam"],
                globals_and_constants.dbTable["outputTb"]
            )

            csvFileName1 = csvFileName.replace("csvdata/","")
            if state:
                break
            if not state:
                shutil.move(f"csvdata/{csvFileName1}", f"errfile/{csvFileName1}")
                addLogFile(
                    f"load csv to table fail {csvFileName}",
                    traceback.format_exc(),
                    True,
                )
                addLogFile(f"load csv to table fail", traceback.format_exc(), True)

def beginUnicrediwork(workGroup, refreshFromDate):
    readState, inputDf = readInputFromMysql(refreshFromDate,workGroup,'unicredit')
    addLogFile("input_dataFrame", inputDf)
    if inputDf is None:
        addLogFile("info", "unicredit inputDf is None", True)
        return
    
    
    inputDicOriList = inputDf.to_dict("records")
    if len(inputDicOriList) == 0:
        addLogFile("info", "unicredit inputDf is None 2", True)
        return
    
    # return
    allZData = []
    inputCount = len(inputDicOriList)
    for i in tqdm(range(inputCount), desc="unicredit input Progress:"):
        time.sleep(1)

        addLogFile("workGroup", workGroup)
        try:
            stateOutput, errcode, detailsDic, csvFileName = getListDataUnicredit.getList(
                inputDicOriList[i]
            )

            addLogFile("DetailsDic", detailsDic)
        except:
            addLogFile("getData fail", "input ID: %d" % inputDicOriList[i]["id"], True)
            addLogFile("Error", traceback.format_exc(), True)
            continue
        state = False
        for n in range(5):
            state = loadCSVtoDB(
                csvFileName,
                globals_and_constants.dbTable["outputTbRam"],
                globals_and_constants.dbTable["outputTb"]
            )

            csvFileName1 = csvFileName.replace("csvdata/","")
            if state:
                break
            if not state:
                shutil.move(f"csvdata/{csvFileName1}", f"errfile/{csvFileName1}")
                addLogFile(
                    f"load csv to table fail {csvFileName}",
                    traceback.format_exc(),
                    True,
                )
                addLogFile(f"load csv to table fail", traceback.format_exc(), True)


'''
def beginAgoswork(workGroup, refreshFromDate):
    
    nowtime = datetime.now().strftime("%Y%m%d%H%M%S")
    csvFileName = f"{csvFolderPath}/outputAgos{nowtime}.csv"
    readState, inputDf = readInputFromMysql(refreshFromDate,workGroup,'agos')
    addLogFile("input_dataFrame", inputDf)
    if inputDf is None:
        addLogFile("info", "agos inputDf is None", True)
        return
    
    
    inputDicOriList = inputDf.to_dict("records")
    if len(inputDicOriList) == 0:
        addLogFile("info", "agos inputDf is None 2", True)
        return
    
    
    # time.sleep(10000)
    allZData = []
    inputCount = len(inputDicOriList)
    for i in tqdm(range(inputCount), desc="agos input Progress:"):
        time.sleep(1)

        addLogFile("workGroup", workGroup)
        try:
            state, errcode, detailsDic = getListDataAgos.getList(
                inputDicOriList[i]
            )

            addLogFile("DetailsDic", detailsDic)
            get_csv(detailsDic,csvFileName) 
        except:
            addLogFile("getData fail", "input ID: %d" % inputDicOriList[i]["id"], True)
            addLogFile("Error", traceback.format_exc(), True)
            continue
    state = False
    for n in range(5):
        state = loadCSVtoDB(
            csvFileName,
            globals_and_constants.dbTable["outputTbRam"],
            globals_and_constants.dbTable["outputTb"]
        )
        if state:
            break
        if not state:
            shutil.move(f"csvdata/{csvFileName}", f"errfile/{csvFileName}")
            addLogFile(
                f"load csv to table fail {csvFileName}",
                traceback.format_exc(),
                True,
            )
            addLogFile(f"load csv to table fail", traceback.format_exc(), True)
'''


def split_list(lst, m):
    n = int(len(lst) / m)
    if n == 0:
        n = 1
    return [lst[i : i + n] for i in range(0, len(lst), n)]



def main():
    workGroup, refreshFromDate = mainInit()

    beginCompasswork(workGroup,refreshFromDate)
    # beginAgoswork(workGroup, refreshFromDate) 
    beginUnicrediwork(workGroup,refreshFromDate)
if __name__ == "__main__":
    main()

