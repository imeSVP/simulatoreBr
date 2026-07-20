#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from logging import exception
import nodriver as uc
from sqlalchemy import except_
import globals_and_constants
import time
from addLogtoFile import createNewFile, addLogFile
import json
import urllib.parse
import random
import requests
from bs4 import BeautifulSoup as bs

# from lxml import etree
from tqdm import tqdm
import re
from datetime import datetime
import traceback
from TimeOutZhang import timeout, task_retry
import glob
import os
import shutil

from csvToolZ import get_csv

import tabula
import pandas as pd

class GetListScraper:
    main_tab: uc.Tab

    USERNAME = globals_and_constants.USERNAME
    PASSWORD = globals_and_constants.PASSWORD

    datadomecodez: str
    listUrl = "-1"

    listContent = None
    br = None
    page = None
    inputDicOri = None
    personDataOri = None
    detalailsLink = []

    isFirstGetList = True
    detailsHrefs = []
    outputList = []
    outputDic ={}
    detailsHrefs.clear()
    outputDic.clear()
    outputList.clear()
    detalailsLink.clear()
    
    minPayNr = 50
    maxPayNr = 50
    nowPayNr = 50

    csvFileName = None
    @task_retry(max_retry_count=2)
    def __init__(self, port, inputDicOri, nowPayNr):
        errString = ""
        self.datadomeCodez = "null"
        self.inputDicOri = inputDicOri
        self.nowPayNr = nowPayNr
        try:
            uc.loop().run_until_complete(self.run(port))
            if self.br is None:
                raise Exception("self.br is null")
            try:
                self.br.stop()
            except:
                pass

        except:
            if self.br is None:
                raise Exception("self.br is null")
            try:
                self.br.stop()
            except:
                pass
            errString = f"fillFormError: {traceback.format_exc()}"
            raise Exception(errString)

    def __del__(self):

        addLogFile("info_del", "__del__")
    
    async def set_range_value(self, page, target_value):
        """设置 range 滑块值"""
        try:
            await page.wait_for("input[type='range']", timeout=10)
            await asyncio.sleep(0.5)
            
            decreaseBtn = await page.find('(//button[contains(@class,"hover:text-(--green-default)")])[2]')
            increaseBtn = await page.find('(//button[contains(@class,"hover:text-(--green-default)")])[3]')
            for i in range(8):
                
                numeroRateCheck = await page.find('//span[text()="numero rate"]/following-sibling::div')
                nowRate = int(numeroRateCheck.text_all)
                if nowRate < target_value:
                    await increaseBtn.mouse_click()
                if nowRate > target_value:
                    await decreaseBtn.mouse_click()
                if nowRate == target_value:
                    break

                await asyncio.sleep(1)

            return True
            
        except Exception as e:
            print(f"失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    async def read_pdf_tables(self, pdf_path):
        """用tabula读取PDF中的所有表格"""
        
        try:
            tables = tabula.read_pdf(
                pdf_path,
                pages='all',
                multiple_tables=True,
                lattice=True,
                pandas_options={'header': None}
            )
            
            # 如果没找到，试试stream模式
            if not tables:
                tables = tabula.read_pdf(
                    pdf_path,
                    pages='all',
                    multiple_tables=True,
                    lattice=False,
                    stream=True,
                    pandas_options={'header': None}
                )
            
            # 清理空表格
            clean_tables = []
            for df in tables:
                if not df.empty:
                    df = df.dropna(how='all')
                    df = df.reset_index(drop=True)
                    clean_tables.append(df)
            
            return clean_tables
            
        except Exception as e:
            print(f"❌ 读取PDF失败: {e}")
            return []      
    
    async def df_to_dict(self, df):
        """将两列的DataFrame转为字典"""
        def clean_text(text):
            """清理所有特殊字符"""
            if not isinstance(text, str):
                return text
            
            # 1. 替换换行符
            text = text.replace('\r\n', ' ')
            text = text.replace('\r', ' ')
            text = text.replace('\n', ' ')
            
            # 2. 替换Unicode项目符号
            text = text.replace('\uf0b7', '•')
            
            # 3. 替换不换行空格
            text = text.replace('\xa0', ' ')
            
            # 4. 替换零宽空格
            text = text.replace('\u200b', '')
            text = text.replace('\u200c', '')
            text = text.replace('\u200d', '')
            
            # 5. 替换多个空格为一个
            text = ' '.join(text.split())
            
            # 6. 清理开头和结尾空格
            text = text.strip()
            
            return text
        
        result = {}
        
        for _, row in df.iterrows():
            key = clean_text(str(row[0]).strip() if pd.notna(row[0]) else '')
            try:
                value = str(row[1]).strip() if pd.notna(row[1]) else ''
            except:
                value = None
            if key:
                result[key] = clean_text(value)
        
        return result

    @task_retry(max_retry_count=5)
    async def fillForm(self):

        csvFolderPath = globals_and_constants.csvFolderPath
        nowtime = datetime.now().strftime("%Y%m%d%H%M%S")
        csvFileName = f"{csvFolderPath}/outputSantader{nowtime}.csv"



        addLogFile("inputDicOri_fillForm", self.inputDicOri)
        '''
        {'id': 281, 'ENTITY': 'BCC', 'total_amount': 1000, 
        'rate': -1, 'PURPOSE': '-1', 'duration': -1, 'ON_OFF': 1}
        '''
        page = self.page
        if page is None:
            raise Exception("page is None")

        await asyncio.sleep(2)
        
        try:
            await page.wait_for_load_state("networkidle", timeout=60)
        except:
            pass
       
        motoriBtn = await page.find('//input[@value="AUN"]/..')
        await motoriBtn.mouse_click()

        await asyncio.sleep(0.5)
        proseguiBtn = await page.find('//button[text()="Prosegui"]')
        await proseguiBtn.mouse_click()

        await asyncio.sleep(1)
        motoriBtn = await page.find('//input[@value="AUP"]/..')
        await motoriBtn.mouse_click()

        await asyncio.sleep(0.5)
        proseguiBtn = await page.find('//button[text()="Prosegui"]')
        await proseguiBtn.mouse_click()
        await asyncio.sleep(1)
        
        motoriBtn = await page.find('//span[text()="Altro Importo"]/..')
        await motoriBtn.mouse_click()

        await asyncio.sleep(0.5)
       
        inputAmountNr = self.inputDicOri['total_amount']
        inputAmountSel = await page.find('//input[@placeholder="Inserisci un importo tra 1.500 € e 30.000 €"]')
        await inputAmountSel.send_keys(str(inputAmountNr))

        await asyncio.sleep(0.5)
        proseguiBtn = await page.find('//button[text()="Prosegui"]')
        await proseguiBtn.mouse_click()
        await asyncio.sleep(2)
        rateList = [12,24,36,42,48,60,72,84 ] 
        for rateItem in  tqdm(rateList, desc="rate:", leave=False):
            rangeinput = await page.find(
                '//input[@type="range"]',
                timeout=10
            )
        
            try:
                await page.wait_for_load_state("networkidle", timeout=60)
            except:
                pass

            
            await self.set_range_value(page,rateItem)
            numeroRateCheck = await page.find('//span[text()="numero rate"]/following-sibling::div')
            nowRate = int(numeroRateCheck.text_all)
            addLogFile('nowRate', nowRate)
            
            await asyncio.sleep(1)
            proseguiBtn = await page.find('//button[text()="Prosegui"]')
            await proseguiBtn.mouse_click()
            
            await asyncio.sleep(2)
            
            rataConAssiBtn = await page.find('//span[contains(text(),"Rata con assicurazione:")]')
            await rataConAssiBtn.click()

            await asyncio.sleep(2)
            
            pdffilePath = "./downloads/BCC/YES"
            if not os.path.exists(pdffilePath):
                os.makedirs(pdffilePath)
            target_path = "./pdf/BCC/YES"
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            
            pdfBtn = await page.find('//label[contains(text(),"Modulo SECCI")]')
            await pdfBtn.click()
            
            await asyncio.sleep(2)
            tabs = self.br.tabs
            pdf_tab = tabs[-1]  # 最新打开的标签页

            await pdf_tab.set_download_path(pdffilePath)
            # print(f"📄 切换到最新标签页")
            await pdf_tab.activate()
 

            url = await pdf_tab.evaluate("window.location.href")
            input_id = self.inputDicOri['id']
            nowTimez = datetime.now().strftime("%Y%m%d%H%M%S")
            pdfName = f"BCC_INPUT_YES_{input_id}{nowTimez}.pdf"
            # await pdf_tab.download_file(url, filename=pdfName)
            #
            

            # 获取 downloads 文件夹下所有 PDF
            isFind = False
            for k in range(10):

                files = glob.glob(f'{pdffilePath}/*.pdf')
                if files:
                    # 按修改时间排序，取最新的
                    latest = max(files, key=os.path.getmtime)
                    new_path = f'{pdffilePath}/{pdfName}'
                    os.rename(latest, new_path)
                    # print(f"✅ PDF已下载并重命名: {pdfName}")
                    pdfTables = await self.read_pdf_tables(new_path)
                    pdfDic = {}
                    for n, pdftableItem in enumerate(pdfTables):
                        pdfDic[n] = await self.df_to_dict(pdftableItem) 
                    addLogFile('pdf', pdfDic)
                    await self.getDetails(pdfDic, True, csvFileName)
                                        
                    if os.path.exists(f"{target_path}/{pdfName}"):
                        os.remove(f"{target_path}/{pdfName}")
 
                    shutil.move(new_path, target_path)
                    isFind = True
                    break
                else:
                    pass

                await asyncio.sleep(2)
            if not isFind:
                print("❌ 没有找到下载的文件")
                raise Exception("❌ 没有找到下载的文件") 

            await asyncio.sleep(1)
 
            rataConAssiBtn = await page.find('//span[contains(text(),"Rata senza assicurazione:")]')
            await rataConAssiBtn.click()
            await asyncio.sleep(2)
            
            pdffilePath = "./downloads/BCC/NO"
            if not os.path.exists(pdffilePath):
                os.makedirs(pdffilePath)
            target_path = "./pdf/BCC/No"
            if not os.path.exists(target_path):
                os.makedirs(target_path)
 

            pdfBtn = await page.find('//label[contains(text(),"Modulo SECCI")]')
            await pdfBtn.click()
            
            await asyncio.sleep(2)
            tabs = self.br.tabs
            pdf_tab = tabs[-1]  # 最新打开的标签页

            await pdf_tab.set_download_path(pdffilePath)
            # print(f"📄 切换到最新标签页")
            await pdf_tab.activate()
 
            await pdf_tab.set_download_path(pdffilePath)

            url = await pdf_tab.evaluate("window.location.href")
            input_id = self.inputDicOri['id']
            nowTimez = datetime.now().strftime("%Y%m%d%H%M%S")
            pdfName = f"BCC_INPUT_NO_{input_id}{nowTimez}.pdf"
            # await pdf_tab.download_file(url, filename=pdfName)

            # 获取 downloads 文件夹下所有 PDF
            isFind = False            
            for k in range(10):

                files = glob.glob(f'{pdffilePath}/*.pdf')
                if files:
                    # 按修改时间排序，取最新的
                    latest = max(files, key=os.path.getmtime)
                    new_path = f'{pdffilePath}/{pdfName}'
                    os.rename(latest, new_path)
                    # print(f"✅ PDF已下载并重命名: {pdfName}")
                    pdfTables = await self.read_pdf_tables(new_path)
                    pdfDic = {}
                    for n, pdftableItem in enumerate(pdfTables):
                        pdfDic[n] = await self.df_to_dict(pdftableItem) 
                    addLogFile('pdf', pdfDic)
                    await self.getDetails(pdfDic,False, csvFileName)
                    
                    if os.path.exists(f"{target_path}/{pdfName}"):
                        os.remove(f"{target_path}/{pdfName}")
 
                    shutil.move(new_path, target_path)
                    isFind = True
                    break
                else:
                    pass
                await asyncio.sleep(2)
            if not isFind:
                print("❌ 没有找到下载的文件")

                raise Exception("❌ 没有找到下载的文件") 

            await asyncio.sleep(1)
            backBtn = await page.find('(//button[contains(@class,"hover:text-(--green-default)")])[1]')
            await backBtn.mouse_click()
        self.csvFileName = csvFileName 
        return


    async def getDetails(self, pdfDic, isAssicurazione, csvFileName):

        willContinue = False
        errStr = ""
        page = self.page
        if page is None:
            raise Exception("page is None")

        outputDic = {}
        errStr = ""

        TS00 = self.inputDicOri['ENTITY']
        TS01 = None
        TS02 = None
        TS03 = None
        TS04 = None
        TS05 = None
        TS06 = None
        TS07 = None
        TS08 = None
        TS09 = None
       
        TS10 = None
        TS11 = None
        TS12 = None
        TS13 = None
        TS14 = None
        TS15 = None
        TS16 = None
        TS17 = None
        TS18 = None
        TS19 = None
        
        TS20 = None 
        TS21 = None
        TS22 = None
        TS23 = None
        TS24 = None
        TS25 = None
        TS26 = None
        TS27 = None
        TS28 = None
        TS29 = None
        
        TS30 = None 
        TS31 = None
        TS32 = None
        TS33 = None
        TS34 = None
        TS35 = None
        TS36 = None
        TS37 = None
        ''' 
        TS01 = contentPText.split('prestito personale del valore di €')[1].split(",00")[0].replace('.','').strip()
        TS17 = contentPText.split(',00 da restituire in')[1].split("rate mensili ognuna")[0].replace('.','').strip()
        TS35 = contentPText.split('importo totale dovuto dal consumatore €')[1].split(". TAN")[0].replace('.','').strip()
        TS07 = contentPText.split('. TAN')[1].split("%")[0].replace('.','').strip()
        TS09 = contentPText.split('- TAEG')[1].split("%")[0].replace('.','').strip()
        TS20 = contentPText.split(', istruttoria €')[1].split(", incasso rata")[0].replace('.','').strip()
        TS26 = contentPText.split(', incasso rata €')[1].split("cad.")[0].replace('.','').strip()

        TS13 = contentPText.split('rate mensili ognuna di €')[1].split(", importo totale dovuto ")[0].replace('.','').strip()
        '''


        TS01Str = pdfDic[2]["Importo totale del credito Limite massimo o somma totale degli importi messi a disposizione del consumatore."]
        TS17Str = pdfDic[2]["Rate ed, eventualmente, loro ordine di imputazione"]
        TS3536Str = pdfDic[2]["Importo totale dovuto dal consumatore Importo del capitale preso in prestito, più gli interessi e i costi connessi al credito."]
        
        TS0708Str = pdfDic[3]["Tasso di interesse o (se applicabili) tassi di interesse diversi che si applicano al Contratto di credito (TAN)"]
        TS0910Str = pdfDic[3]["Tasso annuo effettivo globale (TAEG) Costo totale del credito espresso in percentuale, calcolata su base annua, dell’importo totale del credito. Il TAEG consente al consumatore di confrontare le varie offerte."]
        TS232021Str = pdfDic[4]["Eventuali altri costi derivanti dal Contratto di credito"]


        TS01 = TS01Str.split('di cui')[0].replace('€','').strip()
        TS17 = TS17Str.split('Numero rate:')[1].split('Periodicità Mensile')[0]\
                .replace('€','').strip()
        TS0708 = TS0708Str.split('TAN')[1].split('fisso dalla')[0]\
                .replace('%','').strip()
        TS0910 = TS0910Str.split('TAEG')[1].split('%')[0].strip()
        TS2321 = TS232021Str.split('Spesa mensile gestione pratica')[1]\
                .split('€')[0].strip()
        TS20 = TS232021Str.split('Spese istruttoria/Commissioni')[1]\
                .split('€')[0].strip()



        if isAssicurazione:
            TS37 = TS01Str.split('€ di cui')[1]\
                .split('Assicurazione')[0].replace('€','').strip()
            TS14 = TS17Str.split('Importo rata:')[1].split('Numero rate:')[0]\
                .replace('€','').strip()
            TS36 = TS3536Str.replace('€','').strip()
            TS08 = TS0708
            TS10 = TS0910
            TS23 = TS2321
            TSrataMensile = TS14
        

        else:
            TS13 = TS17Str.split('Importo rata:')[1].split('Numero rate:')[0]\
                .replace('€','').strip()
            TS35 = TS3536Str.replace('€','').strip()
            TS07 = TS0708
            TS09 = TS0910
            TS21 = TS2321
            TSrataMensile = TS13


        outputDic["fetching_date"] = datetime.now().strftime("%Y-%m-%d")
        outputDic["id_input"] = self.inputDicOri['id']
        outputDic["rata_mensile"] = TSrataMensile
        
        outputDic["TS00"] = TS00
        outputDic["TS01"] = TS01
        outputDic["TS02"] = TS02
        outputDic["TS03"] = TS03
        outputDic["TS04"] = TS04
        outputDic["TS05"] = TS05
        outputDic["TS06"] = TS06
        outputDic["TS07"] = TS07
        outputDic["TS08"] = TS08
        outputDic["TS09"] = TS09

        outputDic["TS10"] = TS10
        outputDic["TS11"] = TS11
        outputDic["TS12"] = TS12
        outputDic["TS13"] = TS13
        outputDic["TS14"] = TS14
        outputDic["TS15"] = TS15
        outputDic["TS16"] = TS16
        outputDic["TS17"] = TS17
        outputDic["TS18"] = TS18
        outputDic["TS19"] = TS19

        outputDic["TS20"] = TS20
        outputDic["TS21"] = TS21
        outputDic["TS22"] = TS22
        outputDic["TS23"] = TS23
        outputDic["TS24"] = TS24
        outputDic["TS25"] = TS25
        outputDic["TS26"] = TS26
        outputDic["TS27"] = TS27
        outputDic["TS28"] = TS28
        outputDic["TS29"] = TS29

        outputDic["TS30"] = TS30
        outputDic["TS31"] = TS31
        outputDic["TS32"] = TS32
        outputDic["TS33"] = TS33
        outputDic["TS34"] = TS34
        outputDic["TS35"] = TS35
        outputDic["TS36"] = TS36
        outputDic["TS37"] = TS37

        addLogFile('outputDic', outputDic)
        self.outputDic = outputDic
        get_csv(outputDic,csvFileName) 
        
        







    async def brInit(self, port):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        PROXY = f"{globals_and_constants.ENDPOINT}:{port}"
        browser = await uc.start(
            browser_args=[
                # f'--user-agent={user_agent}',
                f"--proxy-server={PROXY}",
                f"--accept-lang={globals_and_constants.get_value('accept-la')}",
                "--disable-blink-features=AutomationControlled",  # 隐藏自动化控制特征
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-site-isolation-trials",
                                
                '--disable-features=DownloadBubble',
                '--disable-features=DownloadLater',
                '--safebrowsing-disable-download-protection',
                '--disable-extensions',
                '--disable-features=PDFViewer',  # 禁用内置PDF查看器


            ],
        )
        self.main_tab = await browser.get("draft:,")
        self.main_tab.add_handler(uc.cdp.fetch.RequestPaused, self.req_paused)
        self.main_tab.add_handler(
            uc.cdp.fetch.AuthRequired, self.auth_challenge_handler
        )
        await self.main_tab.send(uc.cdp.fetch.enable(handle_auth_requests=True))
        await self.main_tab.maximize()
        # page = await browser.get("https://api.ipify.org?format=json")
        # await asyncio.sleep(3)
        
        self.br = browser
        
        urla = "https://www.crediper.it/preventivatore/simulatore"
        page = await asyncio.wait_for(self.br.get(urla), timeout=30)
      
        await asyncio.sleep(3)

        self.br = browser

        fillFormState = False
        errString = ""

        self.page = page

    async def run(self, port):
        await asyncio.wait_for(self.brInit(port), timeout=20)
        await asyncio.wait_for(self.fillForm(), timeout=600)
        fillFormState = True
        # await asyncio.sleep(2000)
        # await self.getDetails()
        await self.page.close()
        # await self.br.quit()
        self.br.stop()

    async def auth_challenge_handler(self, event: uc.cdp.fetch.AuthRequired):
        # Split the credentials
        # Respond to the authentication challenge
        asyncio.create_task(
            self.main_tab.send(
                uc.cdp.fetch.continue_with_auth(
                    request_id=event.request_id,
                    auth_challenge_response=uc.cdp.fetch.AuthChallengeResponse(
                        response="ProvideCredentials",
                        username=self.USERNAME,
                        password=self.PASSWORD,
                    ),
                )
            )
        )

    async def req_paused(self, event: uc.cdp.fetch.RequestPaused):
        asyncio.create_task(
            self.main_tab.send(
                uc.cdp.fetch.continue_request(request_id=event.request_id)
            )
        )




def getList(inputDicOri):
    errString = ""
    addLogFile("inputDicOri", inputDicOri)
    globals_and_constants.set_value("accept-la", "it-it")
    isStateOk = False
    outputDic = {}
    outputDic.clear()

    outputList = []
    outputList.clear()
    nowPayNr = 50
    maxPayNr = 50
    csvFileName = None 
    for j in range(70):
        
        for k in range(1):

            port = globals_and_constants.INIT_PORTS[0]
            globals_and_constants.set_value("port", port)
            try:
                scraper = GetListScraper(port, inputDicOri, nowPayNr)
                # listContent = scraper.listContent
                outputDic = scraper.outputDic.copy()
                scraper.detailsHrefs.clear()
                scraper.outputDic.clear()
                scraper.detalailsLink.clear()
                nowPayNr = scraper.nowPayNr
                maxPayNr = scraper.maxPayNr
                csvFileName = scraper.csvFileName
                isStateOk = True
                outputList.append(outputDic)
                del scraper
                break
            except:
                errString = f"fillFormError: {traceback.format_exc()}"
                addLogFile("errGetList", errString)
                continue

        if not isStateOk:
            raise Exception(errString)

        addLogFile("nowPayNr >= maxPayNr", f"{nowPayNr} - {maxPayNr}")
        if nowPayNr >= maxPayNr:

            break
        nowPayNr = nowPayNr + 5
    if csvFileName is None:
        return False, "csv file is None", [], None
    else: 
        return True, "", outputList, csvFileName


if __name__ == "__main__":
    globals_and_constants._init()

    createNewFile()
    inputDicOri = {
        'id': 1, 
        'ENTITY': 'SANTANDER', 
        'total_amount': 18500, 
        'ON_OFF': 1
    }
    getList(inputDicOri)

