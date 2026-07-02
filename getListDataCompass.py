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


    @task_retry(max_retry_count=2)
    async def fillForm(self):
        addLogFile("inputDicOri_fillForm", self.inputDicOri)
        '''
        {'id': 1, 'ENTITY': 'COMPASS', 'total_amount': 1000, 
        'monthly_repayment': 50, 'PURPOSE': 'Spese familiari', 'ON_OFF': 1}
        '''
        page = self.page
        if page is None:
            raise Exception("page is None")

        await asyncio.sleep(2)
        try:
            acceptCookieBtn = await page.find(
                f'//button[contains(text(),"Accetta tutti i cookie")]'
            )
            await acceptCookieBtn.click()

            await asyncio.sleep(1)
        except:
            pass
        all_ranges = await self.page.find_all('input#range')

        addLogFile("all_ranges_lenth", len(all_ranges))
        total_amount_sel = all_ranges[0]
        # await total_amount_sel.set_value('50.00')
        #
        
        total_amount_int = int(self.inputDicOri['total_amount'])
        
        total_amount_persent = (total_amount_int-1000)/290
        
        await total_amount_sel.apply("""
            (elem) => {
                elem.value = '%s';
                elem.dispatchEvent(new Event('input', { bubbles: true }));
                elem.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """ % total_amount_persent)

        minpaySel = await page.find('((//div[@class="range-caption"])[2]/span)[1]')
        minpayStr = int(minpaySel.text.replace(".",""))
        addLogFile('minpayStr', minpayStr)


        maxpaySel = await page.find('((//div[@class="range-caption"])[2]/span)[2]')
        maxpayStr = int(maxpaySel.text.replace(".",""))

        addLogFile('maxpayStr', maxpayStr)
        
        self.minPayNr = minpayStr
        self.maxPayNr = maxpayStr

        # monthly_repayment_int = int(self.inputDicOri['monthly_repayment'])
        monthly_repayment_int =  self.nowPayNr
        nowPaySel = await page.find('(//div[@class="range-tooltip"])[2]')
        nowPayStr = int(nowPaySel.text_all.replace('€','').replace('.','').strip())
        addLogFile('nowPayStr', nowPayStr)

        if maxpayStr == minpayStr:
            repay_persent = 0
        else:
            # repay_persent = (monthly_repayment_int - minpayStr)*100/(maxpayStr - minpayStr)
            step = 1
            n = int(100/step)
            for i in range(n):
                nowPersent = i*100 / n
                monthly_repayment_sel = all_ranges[1]
                await monthly_repayment_sel.apply("""
                    (elem) => {
                        elem.value = '%s';
                        elem.dispatchEvent(new Event('input', { bubbles: true }));
                        elem.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                """ % nowPersent)
                nowPaySel = await page.find('(//div[@class="range-tooltip"])[2]')
                nowPayStr = int(nowPaySel.text_all.replace('€','').replace('.','').strip())
                addLogFile('nowPayStr', nowPayStr)
                
                if nowPayStr >= monthly_repayment_int:
                    self.nowPayNr = nowPayStr
                    break
        addLogFile("info",f"find pay {nowPayStr} -- {monthly_repayment_int}")


           



        # return 
        # await asyncio.sleep(3000)

        '''
        monthly_repayment_sel = all_ranges[1]
        await monthly_repayment_sel.apply("""
            (elem) => {
                elem.value = '%s';
                elem.dispatchEvent(new Event('input', { bubbles: true }));
                elem.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """ % repay_persent)
i       '''
        purpose_sel = await page.find('//div[@class="select-button"]')
        await purpose_sel.mouse_click()

        await asyncio.sleep(1)
        purpose_str = self.inputDicOri['PURPOSE']
        # purpose_str = "Acquisto beni per la casa"
        purpose_li = await page.find(f'//li/span[contains(text(),"{purpose_str}")]')
        await purpose_li.click()

        submitBtn = await page.find('//button/p[text()="CONTINUA"]')
        await submitBtn.mouse_click()

        try:
            testSel = await page.find('//p[contains(., "Importo totale credito")]', timeout=2)
            a = testSel.text
        except:

            raise Exception("cannot go to deteal page")


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
 

        TS01Sel = await page.find('//span[contains(text(),"Importo totale credito:")]/..', timeout=2)
        TS01 = TS01Sel.text_all.split(":")[1].replace("€","").strip()
         
        TS3334Sel = await page.find('//span[contains(text(),"Importo totale dovuto:")]/..', timeout=2)
        TS33 = TS3334Sel.text_all.split('da MIN')[1].split(' € a MAX')[0].strip()
        TS34 = TS3334Sel.text_all.split(' € a MAX')[1].replace("€","").strip()

        
        TS0304Sel = await page.find(f'//span[contains(text(),"TAN:")]/..', timeout=2)
        TS03 = TS0304Sel.text_all.split('da MIN')[1].split('a MAX')[0].replace("%","").strip()
        TS04 = TS0304Sel.text_all.split('a MAX')[1].replace("%","").strip()

        TS0506Sel = await page.find(f'//span[contains(text(),"TAEG:")]/..', timeout=2)
        TS05 = TS0506Sel.text_all.split('da MIN ')[1].split('a MAX')[0].replace("%","").strip()
        TS06 = TS0506Sel.text_all.split('a MAX')[1].replace("%","").strip()

         
        TS1112Sel = await page.find(f'//span[contains(text(),"Importo rata:")]/..', timeout=2)
        TS11 = TS1112Sel.text_all.split("nell'intervallo tra")[1].split('(per durata pari a ')[0].replace("€","").strip()
        TS12 = TS1112Sel.text_all.split(' mesi) e')[1].split('(per durata pari a ')[0].replace("€","").strip()

         
        TS1819Sel = await page.find(f'//span[contains(text(),"Spese di istruttoria finanziate:")]/..', timeout=2)
        addLogFile("TS1819Sel", TS1819Sel.text_all)
        if 'da' in TS1819Sel.text_all:
            TS18 = TS1819Sel.text_all.split("da")[1].split('€ a')[0].replace("€","").strip()
            TS19 = TS1819Sel.text_all.split(' a')[1].replace("€","").strip()
        else:
            TS18 = TS1819Sel.text_all.split(":")[1].replace("€","").strip()
            TS19 = TS1819Sel.text_all.split(":")[1].replace("€","").strip()
         
        TS2425Sel = await page.find(f'//span[contains(text(),"Commissioni di incasso e gestione pratica")]/..', timeout=2)
        if 'da' in TS2425Sel.text_all:
            TS24 = TS2425Sel.text_all.split("da")[1].split(' a')[0].replace("€","").strip()
            TS25 = TS2425Sel.text_all.split(' a')[1].replace("€","").replace("rata;","").strip()
        else:
            TS24 = TS2425Sel.text_all.split(":")[1].replace("€","").replace("rata;","").strip()
            TS25 = TS2425Sel.text_all.split(":")[1].replace("€","").replace("rata;","").strip()

        TS15165Sel = await page.find(f'//span[contains(text(),"Durata totale del finanziamento:")]/..', timeout=2)
        if 'da' in TS15165Sel.text_all:
            TS15 = TS15165Sel.text_all.split("da MIN")[1].split('a MAX')[0].split('mese')[0].replace("mesi","").strip()
            TS16 = TS15165Sel.text_all.split('a MAX')[1].split('mese')[0].replace("mesi","").strip()
        else:
            TS15 = TS15165Sel.text_all.split(":")[1].replace("mese","").replace("mesi","").replace(";","").strip()
            TS16 = TS15165Sel.text_all.split(":")[1].replace("mese","").replace("mesi","").replace(";","").strip()

        TS27282930Sel = await page.find(f'//span[contains(text(),": TAN min")]', timeout=2)
        TS27 = TS27282930Sel.text_all.split(": TAN min")[1].split("TAN max")[0].replace("%","").strip()
        TS28 = TS27282930Sel.text_all.split("TAN max")[1].split("TAEG min")[0].replace("%","").strip()

        TS29 = TS27282930Sel.text_all.split("TAEG min")[1].split("TAEG max")[0].replace("%","").strip()
        TS30 = TS27282930Sel.text_all.split("TAEG max")[1].split(".")[0].replace("%","").strip()


        outputDic["fetching_date"] = datetime.now().strftime("%Y-%m-%d")
        outputDic["id_input"] = self.inputDicOri['id']
        outputDic["rata_mensile"] = self.nowPayNr
        
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
        urla = f"https://www.compass.it/simulatore-prestito-online/"
        page = await asyncio.wait_for(self.br.get(urla), timeout=30)
 
        '''
        urla = f"https://duckduckgo.com/?q=https%3A%2F%2F{urlab}%2F&t=h_&ia=web"

        self.br = browser
        page = await asyncio.wait_for(self.br.get(urla), timeout=30)

        await asyncio.sleep(5)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # await page.save_screenshot(f"debug_screenshot_{timestamp}.png")
        # print(f"截图已保存: debug_screenshot_{timestamp}.png")

        homebtn = await page.find(f'//a[@href="{urlab}/"]')
        await homebtn.click()
        '''
        """
        for i in range(5):

            await asyncio.sleep(5)
            frame_data = await self.main_tab.send(uc.cdp.page.get_frame_tree())
            current_url = frame_data.frame.url
            addLogFile("current_url", current_url)
            current_html = await page.get_content()
            if not "'t':'fe'" in current_html:
                addLogFile("info", "no fe")
                break
            page = await asyncio.wait_for(self.br.get(urla), timeout=30)

        requests_style_cookies = await browser.cookies.get_all(
            requests_cookie_format=True
        )
        """
       
        await asyncio.sleep(3)

        self.br = browser

        fillFormState = False
        errString = ""

        self.page = page

    async def run(self, port):
        await asyncio.wait_for(self.brInit(port), timeout=20)
        await asyncio.wait_for(self.fillForm(), timeout=150)
        fillFormState = True
        await asyncio.sleep(2)
        await self.getDetails()
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
