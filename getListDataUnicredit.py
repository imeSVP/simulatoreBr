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



country = "it"

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
    
    async def type_human_with_verify(self,element, value):
        """逐字符输入并验证"""
        value_str = str(value)
        
        # 点击
        await element.mouse_click()
        await asyncio.sleep(2)
                   # 用 JS 清空并触发事件
        await element.apply("""
            (elem) => {
                elem.focus();
                elem.value = '';
                // 触发 React 的 input 事件
                const event = new Event('input', { bubbles: true });
                elem.dispatchEvent(event);
                // 触发 change 事件
                const changeEvent = new Event('change', { bubbles: true });
                elem.dispatchEvent(changeEvent);
            }
        """)
        await asyncio.sleep(0.2)
        # 逐字符输入
        for char in value_str:
            await element.send_keys(char)
            await asyncio.sleep(0.15)
        
        await asyncio.sleep(0.5)
       
        return

    @task_retry(max_retry_count=5)
    async def fillForm(self):
        addLogFile("inputDicOri_fillForm", self.inputDicOri)
        '''
        {'id': 1, 'ENTITY': 'UNICREDIT', 'total_amount': 4000, 'ON_OFF': 1}
        '''
        page = self.page
        if page is None:
            raise Exception("page is None")

        await asyncio.sleep(2)
        try:
            acceptCookieBtn = await page.find(
                f'//button[contains(text(),"ACCETTO TUTTI I COOKIE")]'
            )
            await acceptCookieBtn.mouse_click()

            await asyncio.sleep(1)
        except:
            pass
        # '''
        #
        prestitiBtn = await page.find(
            '//a[@href="/it/privati/prestiti.html"]',
            timeout=5
        )
        await prestitiBtn.mouse_click()

        await asyncio.sleep(2)

        findMoreBtn = await page.find(
            '//a[contains(text(),"Scopri di più")]',
            timeout=5
        )
        await findMoreBtn.mouse_click()

        await asyncio.sleep(2)
        askBtn = await page.find(
            '//a[text()="Procedi con la richiesta da qui"]',
            timeout=5
        )
        await askBtn.mouse_click()
        
        askOnlineBtn = await page.find(
            '//button[text()="Richiedi Online"]',
            timeout = 10
        )
        await askOnlineBtn.mouse_click()
        await asyncio.sleep(20)
        # '''

        try:
            await page.wait_for_load_state("networkidle", timeout=60)
        except:
            pass
        for n_time in range(20):
            addLogFile('info', f"wait .... {n_time}")
            total_amount_sel = await page.find(
                '//input[@id="requested_amount_input"]',
                timeout = 10
            )
            try:
                await total_amount_sel.mouse_click()
                
                await asyncio.sleep(5)
                break
            except:

                await asyncio.sleep(5)
                btn_ricomincia = await page.find(
                    '//button/span[text()="Ricomincia"]',
                    timeout =5
                )
                try:
                    await btn_ricomincia.mouse_click()
                except:
                    pass
                if n_time % 5 == 4:
                    await page.reload()


        total_amount_int = self.inputDicOri['total_amount']
        # total_amount_int = 30000 
        addLogFile("total_amount_value", str(total_amount_int))
         
        await self.type_human_with_verify(total_amount_sel, total_amount_int)

        await asyncio.sleep(5)

        rata_mensile_sel = await page.find(
            '//input[@aria-label="select options"]',
            timeout = 5
        )

        await rata_mensile_sel.mouse_click()

        await asyncio.sleep(5)
        rata_mensile_li_list = await page.find_all(
            '//*[@id="react-select-2-listbox"]/div'
        )

        for rata_mensile_time in range(5):
            if "No options" in rata_mensile_li_list[0].text_all:
                
                await asyncio.sleep(5)
                rata_mensile_li_list = await page.find_all(
                    '//div[contains(@id, "react-select-") and contains(@id, "-listbox")]'
                )
            else:
                break

        
        for rata_mensile_timez in tqdm(range(len(rata_mensile_li_list)), desc="rate", leave=False):
            rata_mensile_timeyz = rata_mensile_timez + 1
            rata_mensile_li = await page.find(
                f'(//div[contains(@id, "react-select-") and contains(@id, "-listbox")]/div)[{rata_mensile_timeyz}]'
            )
            rata_mensile_str = rata_mensile_li.text_all.replace('€','').strip()
            addLogFile('rata_mensile', rata_mensile_str)
            
            await rata_mensile_li.click()

            await asyncio.sleep(5)
            
            TS17Sel = await page.find('(//div/span[text()=" mesi"])/preceding-sibling::span')
            TS17Str = TS17Sel.text_all
            addLogFile('TS17Str', TS17Str)

            TS07Sel = await page.find('(//span[text()="TAN"])/../../../div[2]/span')
            TS07Str = TS07Sel.text_all.replace('%','').strip()
            addLogFile('TS07Str', TS07Str)
            
            TS09Sel = await page.find('(//span[text()="TAEG"])/../../../div[2]/span')
            TS09Str = TS09Sel.text_all.replace('%','').strip()
            addLogFile('TS09Str', TS09Str)
            outTemp = {}
            outTemp.clear()
            outTemp['TS01'] = total_amount_int
            outTemp['TS13'] = rata_mensile_str
            outTemp['TS17'] = TS17Str
            outTemp['TS07'] = TS07Str
            outTemp['TS09'] = TS09Str

            await self.getDetails(outTemp) 



            rata_mensile_sel = await page.find(
                '//input[@aria-label="select options"]',
                timeout = 5
            )
            await rata_mensile_sel.mouse_click()

            await asyncio.sleep(5)
        await asyncio.sleep(30)

        return

    async def getDetails(self, outTemp):
        willContinue = False
        errStr = ""
        page = self.page
        if page is None:
            raise Exception("page is None")

        outputDic = {}
        errStr = ""

        TS00 = self.inputDicOri['ENTITY']
        TS01 = outTemp['TS01']
        TS02 = None
        TS03 = None
        TS04 = None
        TS05 = None
        TS06 = None
        TS07 = outTemp['TS07']
        TS08 = None
        TS09 = outTemp['TS09']
       
        TS10 = None
        TS11 = None
        TS12 = None
        TS13 = outTemp['TS13']
        TS14 = None
        TS15 = None
        TS16 = None
        TS17 = outTemp['TS17']
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
 

        outputDic["fetching_date"] = datetime.now().strftime("%Y-%m-%d")
        outputDic["id_input"] = self.inputDicOri['id']
        outputDic["rata_mensile"] = outTemp['TS13']
        
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

        # addLogFile('outputDic', outputDic)
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
        
        urla = f"https://www.unicredit.it/it/privati/prestiti/tutti-i-prestiti/per-le-esigenze-di-tutti-i-giorni/prestito-unicredit.html"
        urla = f"https://www.unicredit.it/"
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
    csvFolderPath = globals_and_constants.csvFolderPath
    nowtime = datetime.now().strftime("%Y%m%d%H%M%S")
    csvFileName = f"{csvFolderPath}/outputCompass{nowtime}.csv"

 
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
        'id': 1, 
        'ENTITY': 'COMPASS', 
        'total_amount': 3000, 
        'monthly_repayment': 610, 
        'PURPOSE': 'Spese Familiari', 
        'ON_OFF': 1
    }
    getList(inputDicOri)
