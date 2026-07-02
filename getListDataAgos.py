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
import base64

from ocr_italian import recognize

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
    outputDic ={}
    detailsHrefs.clear()
    outputDic.clear()
    detalailsLink.clear()
    @task_retry(max_retry_count=2)
    def __init__(self, port, inputDicOri):
        errString = ""
        self.datadomeCodez = "null"
        self.inputDicOri = inputDicOri

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
        {'id': 2, 'ENTITY': 'AGOS', 'total_amount': 1000, 
        'duration': 24, 'ON_OFF': 1}
        '''
        page = self.page
        if page is None:
            raise Exception("page is None")

        try:
            acceptCookieBtn = await page.find(
                f'//button/span[contains(text(),"Accetta tutti i cookie")]',
                timeout=5 
            )
            await acceptCookieBtn.click()

            await asyncio.sleep(1)
        except:
            pass
        # all_ranges = await self.page.find_all('input#range')

        # addLogFile("all_ranges_lenth", len(all_ranges))
        total_amount_sel = await page.find('input#range-slider-amount')
        # await total_amount_sel.set_value('50.00')
        #
        
        total_amount_int = int(self.inputDicOri['total_amount'])
        
        total_amount_persent = (total_amount_int-500)/295
        
        await total_amount_sel.apply("""
            (elem) => {
                elem.value = '%s';
                elem.dispatchEvent(new Event('input', { bubbles: true }));
                elem.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """ % total_amount_persent)

        mindurationSel = await page.find('//div[@data-id="n-min-rate"]')
        mindurationStr = int(mindurationSel.text.replace(".","").replace("rate","").strip())
        addLogFile('mindurationStr', mindurationStr)
        

        maxdurationSel = await page.find('//div[@data-id="n-max-rate"]')
        maxdurationStr = int(maxdurationSel.text.replace(".","").replace("rate","").strip())

        addLogFile('maxdurationStr', maxdurationStr)
        
        durationint = int(self.inputDicOri['duration'])
        if maxdurationStr == mindurationStr:
            duration_persent = 0
        else:
            duration_persent = (durationint - mindurationStr)*100/(maxdurationStr - mindurationStr)
        
        duration_sel = await page.find('input#range-slider-rate')
        await duration_sel.apply("""
            (elem) => {
                elem.value = '%s';
                elem.dispatchEvent(new Event('input', { bubbles: true }));
                elem.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """ % duration_persent)
        
        '''
        purpose_sel = await page.find('//div[@class="select-button"]')
        await purpose_sel.mouse_click()

        await asyncio.sleep(1)
        purpose_str = self.inputDicOri['PURPOSE']
        # purpose_str = "Acquisto beni per la casa"
        purpose_li = await page.find(f'//li/span[contains(text(),"{purpose_str}")]')
        await purpose_li.click()
        '''

        await asyncio.sleep(2)
        submitBtn = await page.find('a#btn-goto-form')
        await submitBtn.mouse_click()

        all_tabs = self.br.tabs
        page = all_tabs[-1]
        self.page = page
        # await asyncio.sleep(100)
        btn_stampa_secci = None
        try:
            btn_stampa_secci = await page.find('a#stampa-secci', timeout=10)
            await btn_stampa_secci.mouse_click()
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
        await asyncio.sleep(5)
        img_elements = await page.find_all('//div[@id="img-secci"]/img', timeout = 10)
        addLogFile('img_elements', len(img_elements))
        for i, elem in enumerate(img_elements):
            # 获取 src 属性
            img_src = elem.attrs['src']
            
            # 判断是否为 data URI
            if img_src and img_src.startswith('data:image'):
                # 提取 base64 数据部分
                # data:image/png;base64, 后面的就是base64数据
                header, encoded = img_src.split(',', 1)
                
                # 解码 base64
                img_data = base64.b64decode(encoded)
                
                # 保存为文件
                with open(f'image_{i}.png', 'wb') as f:
                    f.write(img_data)
                print(f'img saved: image_{i}.png')

                test = recognize(f'image_{i}.png')
                addLogFile(f'image_{i}.png', test)


        return
 

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
        urla = f"https://www.agos.it/"
        page = await asyncio.wait_for(self.br.get(urla), timeout=30)
 
      
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
    for k in range(1):

        port = globals_and_constants.INIT_PORTS[0]
        globals_and_constants.set_value("port", port)
        try:
            scraper = GetListScraper(port, inputDicOri)
            # listContent = scraper.listContent
            outputDic = scraper.outputDic.copy()
            scraper.detailsHrefs.clear()
            scraper.outputDic.clear()
            scraper.detalailsLink.clear()

            isStateOk = True
            del scraper
            break
        except:
            errString = f"fillFormError: {traceback.format_exc()}"
            addLogFile("errGetList", errString)
            continue
    if not isStateOk:
        raise Exception(errString)
    return True, "", outputDic
