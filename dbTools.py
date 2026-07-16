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
    INSERT INTO {tableNamestr} (
        fetching_date,
        id_input,
        rata_mensile,
        TS00,
        TS01,
        TS02,
        TS03,
        TS04,
        TS05,
        TS06,
        TS07,
        TS08,
        TS09,
        TS10,
        TS11,
        TS12,
        TS13,
        TS14,
        TS15,
        TS16,
        TS17,
        TS18,
        TS19,
        TS20,
        TS21,
        TS22,
        TS23,
        TS24,
        TS25,
        TS26,
        TS27,
        TS28,
        TS29,
        TS30,
        TS31,
        TS32,
        TS33,
        TS34,
        TS35,
        TS36,
        TS37
    )
    select * from {memTableNamestr}{tNr}
    """

    queryList.append(query)
    query = f"DROP TABLE {memTableNamestr}{tNr}"
    queryList.append(query)
    state = _exctuteSQLList(queryList)
    addLogFile("inputTb querylist", queryList)
    return state


def readPersonalData():
    query = """
    SELECT nome,cognome, email, telefono_celullare FROM finser_banks_db.generalita;
    """
    addLogFile("inputTb query", query)
    return _getDfFromSQL(query)


def readInputFromMysql(dateString: str, ON_OFF: str,bankName: str):
    ''' 
    if bankName.lower() in 'compass':
        inputTb = globals_and_constants.dbTable["inputCompass"]
    if bankName.lower() in 'agos':
        inputTb = globals_and_constants.dbTable["inputAgos"]
    if bankName.lower() in 'santander':
        inputTb = globals_and_constants.dbTable["inputSantander"]
    if bankName.lower() in 'unicredit':
        inputTb = globals_and_constants.dbTable['inputUnicredit']
    '''
    inputTb = globals_and_constants.dbTable['inputTb']
    outputTb = globals_and_constants.dbTable["outputTb"]
    query = f"""
        select zinput.* from  {inputTb} as zinput
            where zinput.ON_OFF = {ON_OFF}
            and zinput.ENTITY = '{bankName.upper()}'
            and zinput.id not in (
                select id_input 
                from {outputTb} as zoutput 
                where zoutput.fetching_date>='{dateString}'
                and zoutput.TS00 = '{bankName.upper()}'
        )
    """
    addLogFile("inputTb query", query)
    return _getDfFromSQL(query)
