#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import MySQLdb as mysql
from MySQLdb._exceptions import OperationalError, DataError

import globals_and_constants
from addLogtoFile import addLogFile

import traceback
import random


def _getDfFromSQL(query: str):
    try:
        mydb = mysql.connect(**globals_and_constants.MYSQL)
        inputDf = pd.read_sql(query, con=mydb, coerce_float=False)
        mydb.close()
        return True, inputDf
    except Exception as e:
        addLogFile("Error", traceback.format_exc())
        return False, None


def _exctuteSQLList(queryList: list, md=False):
    try:
        mydb = mysql.connect(**globals_and_constants.MYSQL)
        if md:
            mydb = mysql.connect(**globals_and_constants.MYSQL1)
        cursor = mydb.cursor()
        for query in queryList:
            cursor.execute(query)
            mydb.commit()
        mydb.close()

        return True
    except Exception as e:
        addLogFile("Error", traceback.format_exc())
        return False


def loadCSVtoDB1(filePathStr, memTableNamestr, tableNamestr):
    tNr = random.randint(1, 5)
    queryList = []
    query = f"CREATE TEMPORARY TABLE IF NOT EXISTS {memTableNamestr}{tNr} AS (SELECT * FROM {memTableNamestr} LIMIT 0)"
    queryList.append(query)
    query = f"""LOAD DATA LOCAL INFILE '{filePathStr}'
    INTO TABLE {memTableNamestr}{tNr}
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\\r\\n'
    IGNORE 1 LINES;"""
    queryList.append(query)

    query = f"""
    INSERT INTO {tableNamestr} select * from {memTableNamestr}{tNr}
    """

    queryList.append(query)
    query = f"DROP TABLE {memTableNamestr}{tNr}"
    queryList.append(query)
    state = _exctuteSQLList(queryList, True)
    addLogFile("inputTb querylist", queryList)
    return state


def loadCSVtoDB(filePathStr, memTableNamestr, tableNamestr):
    tNr = random.randint(1, 5)
    queryList = []
    query = f"CREATE TEMPORARY TABLE IF NOT EXISTS {memTableNamestr}{tNr} AS (SELECT * FROM {memTableNamestr} LIMIT 0)"
    queryList.append(query)
    query = f"""LOAD DATA LOCAL INFILE '{filePathStr}'
    INTO TABLE {memTableNamestr}{tNr}
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\\r\\n'
    IGNORE 1 LINES;"""
    queryList.append(query)

    query = f"""
    INSERT INTO {tableNamestr} select * from {memTableNamestr}{tNr}
    """

    queryList.append(query)
    query = f"DROP TABLE {memTableNamestr}{tNr}"
    queryList.append(query)
    state = _exctuteSQLList(queryList)
    addLogFile("inputTb querylist", queryList)
    return state


def checkBusinessDataToday(datecheck):
    query = f"SELECT * FROM finser_utilities_mb_db.output_luce_info_segugio where fetching_date >= '{datecheck}'"

    addLogFile("inputTb query", query)
    return _getDfFromSQL(query)


def readPersonalData():
    query = """
    SELECT nome,cognome, email, telefono_celullare FROM finser_banks_db.generalita;
    """
    addLogFile("inputTb query", query)
    return _getDfFromSQL(query)


def readInputFromMysql(dateString: str, ON_OFF: str, isLuce):
    if isLuce:
        inputTb = globals_and_constants.dbTable["inputTb1"]
        outputTb = globals_and_constants.dbTable["outputTb1"]
    else:
        inputTb = globals_and_constants.dbTable["inputTb2"]
        outputTb = globals_and_constants.dbTable["outputTb2"]
    query = f"""
        select zinput.* from  {inputTb} as zinput
            where zinput.ON_OFF = {ON_OFF}
            and zinput.id not in (
                select input_id 
                from {outputTb} as zoutput 
                where zoutput.fetching_date>='{dateString}'
        )
    """
    addLogFile("inputTb query", query)
    return _getDfFromSQL(query)
