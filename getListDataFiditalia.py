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

from csvToolZ import get_csv
import os
import aiohttp
from pathlib import Path

import json



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


    @task_retry(max_retry_count=2)
    def __init__(self, port, inputDicOri, nowPayNr, csvFileName):
        errString = ""
        self.datadomeCodez = "null"
        self.inputDicOri = inputDicOri
        self.nowPayNr = nowPayNr
        self.csvFileName = csvFileName
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

    async def set_slider_value(self, page, slider_id, target_value):
        """使用加减按钮设置滑块值"""
        try:
            # 等待滑块出现
            await page.wait_for(f"#{slider_id}", timeout=10)
            await asyncio.sleep(0.5)
            
            # 获取滑块元素
            slider = await page.select(f"#{slider_id}")
            if not slider:
                print(f"找不到滑块: {slider_id}")
                return False
            
            # 使用 attrs 属性获取
            current_value = int(slider.attrs.get("data-start", 0))
            min_val = int(slider.attrs.get("data-min", 0))
            max_val = int(slider.attrs.get("data-max", 0))
            step = int(slider.attrs.get("data-step", 0))
            
            # print(f"当前值: {current_value}, 目标值: {target_value}")
            
            # 确保目标值在范围内
            if target_value < min_val:
                target_value = min_val
            if target_value > max_val:
                target_value = max_val
            
            # 计算需要点击的次数
            diff = target_value - current_value
            clicks = abs(int(diff / step))
            
            if clicks == 0:
                # print(f"已经是目标值: {target_value}")
                return True
            
            # 选择按钮
            if diff < 0:
                btn_selector = f"[data-less='{slider_id}']"
                btn_text = "less"
            else:
                btn_selector = f"[data-more='{slider_id}']"
                btn_text = "more"
            
            # print(f"需要点击 {btn_text} {clicks} 次")
            
            # 点击
            for i in range(clicks):
                btn = await page.select(btn_selector, timeout=5)
                if not btn:
                    print(f"找不到按钮: {btn_selector}")
                    return False
                
                await btn.click()
                # print(f"点击 {btn_text} ({i+1}/{clicks})")
                await asyncio.sleep(0.2)
            
            # print(f"设置完成: {slider_id} -> {target_value}")
            await asyncio.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"失败 {slider_id}: {e}")
            import traceback
            traceback.print_exc()
            return False
       

    @task_retry(max_retry_count=5)
    async def fillForm(self):
        addLogFile("inputDicOri_fillForm", self.inputDicOri)
        '''
        {'id': 127, 'ENTITY': 'FIDITALIA', 'total_amount': 3000, 
        'rate': -1, 'PURPOSE': '-1', 'duration': 24, 'ON_OFF': 1}
        '''
        page = self.page
        if page is None:
            raise Exception("page is None")
        await asyncio.sleep(2)
        try:
            acceptCookieBtn = await page.find(
                f'//button[contains(text(),"Accetta tutti")]'
            )
            await acceptCookieBtn.mouse_click()

            await asyncio.sleep(1)
        except:
            pass
        
        try:
            await page.wait_for_load_state("networkidle", timeout=60)
        except:
            pass
        total_amount_int = self.inputDicOri['total_amount']
        # total_amount_int = 30000 
        addLogFile("total_amount_value", str(total_amount_int))
        await self.set_slider_value(page,"amounts", total_amount_int)
        duration_int = self.inputDicOri['duration']
        await self.set_slider_value(page,"payments", duration_int)

        await asyncio.sleep(1)

        continueBtn = await page.find('//a[@aria-label="Fidiamo continua"]')
        await continueBtn.mouse_click()
    
        '''
        await asyncio.sleep(2)
        pdf_data = []
                
        
        downloadBtn = await page.find('//a[@id="generateSecciBtn"]')
        await downloadBtn.mouse_click()

        await asyncio.sleep(2)
        tabs = self.br.tabs
        pdf_tab = tabs[-1]  # 最新打开的标签页

        print(f"📄 切换到最新标签页")
        await pdf_tab.activate()
        await asyncio.sleep(1)
       
        await pdf_tab.set_download_path('./downloads')

        url = await pdf_tab.evaluate("window.location.href")
        input_id = self.inputDicOri['id']
        nowTimez = datetime.now().strftime("Y%m%d%H%M%S")
        pdfName = f"FIDITALIA_INPUT{input_id}{nowTimez}.pdf"
        await pdf_tab.download_file(url, filename=pdfName)
        
        print("✅ PDF已下载")
        '''
        await asyncio.sleep(1)
        await self.getDetails() 

        


        # addLogtoFile('testPdf', testPdf, True)
        
        await asyncio.sleep(2)
        return 


    async def getDetails(self):
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
        
        # TS00 = "Finanziatore Fiditalia S.p.A., società finanziaria, soggetta alla vigilanza della Banca d’Italia"
        # TS00 = "FIDITALIA"
        allData = await page.find('input#offer2')

        

        allDataStr = allData.attrs['value']
        addLogFile('inputDataStr', allDataStr)
        allDataDic = json.loads(allDataStr)

        TS01 = int(allDataDic['importoRichiesto'].replace('.',''))
        TS17 = int(allDataDic['numeroRate'])
        TS13 = allDataDic['rata']
        TS26 = allDataDic['incassoRata']
        TS35 = allDataDic['importoDovuto']
        TS07 = allDataDic['tan'].replace('%','')
        TS09 = allDataDic['taeg'].replace('%','')
        TS20 = allDataDic['speseIstruttoria']


        outputDic["fetching_date"] = datetime.now().strftime("%Y-%m-%d")
        outputDic["id_input"] = self.inputDicOri['id']
        outputDic["rata_mensile"] = TS13.replace('.','')
        
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
        get_csv(outputDic,self.csvFileName) 








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
        urla = "https://www.fiditalia.it/prestiti/fidiamo"
        page = await asyncio.wait_for(self.br.get(urla), timeout=30)
      
        await page.set_download_path('./downloads')
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




def getList(inputDicOri, csvFileName):
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
 
    for j in range(70):
        
        for k in range(1):

            port = globals_and_constants.INIT_PORTS[0]
            globals_and_constants.set_value("port", port)
            try:
                scraper = GetListScraper(port, inputDicOri, nowPayNr,csvFileName)
                # listContent = scraper.listContent
                outputDic = scraper.outputDic.copy()
                scraper.detailsHrefs.clear()
                scraper.outputDic.clear()
                scraper.detalailsLink.clear()
                nowPayNr = scraper.nowPayNr
                maxPayNr = scraper.maxPayNr
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

    return True, "", outputList, csvFileName


if __name__ == "__main__":
    globals_and_constants._init()

    createNewFile()
    inputDicOri = {
        'id': 127,
        'ENTITY': 'FIDITALIA',
        'total_amount': 3000,
        'rate': -1,
        'PURPOSE': '-1',
        'duration': 24,
        'ON_OFF': 1
    }
    getList(inputDicOri)
