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
from image_to_text import image_to_text

from csvToolZ import get_csv
# from ocr_italian import recognize

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
    csvFileName = ""

    @task_retry(max_retry_count=2)
    def __init__(self, port, inputDicOri,csvFileName):
        errString = ""
        self.datadomeCodez = "null"
        self.inputDicOri = inputDicOri
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
        """设置滑块值 - 从0%逐步增加"""
        addLogFile("info", f"set_slider_value begin.... 目标: {target_value}")
        try:
            await page.wait_for(f'input#{slider_id}', timeout=10)
            await asyncio.sleep(1)
            
            slider = await page.find(f'input#{slider_id}')
            
            # 获取范围
            min_val = int(slider.attrs['aria-valuemin'].replace('.',''))
            max_val = int(slider.attrs['aria-valuemax'].replace('.',''))
            
            addLogFile("info", f"范围: {min_val} - {max_val}")
            
            # 验证目标值
            if target_value < min_val:
                target_value = min_val
            if target_value > max_val:
                target_value = max_val
            
            # 获取滑块物理范围
            slider_min = int(slider.attrs['min'])
            slider_max = int(slider.attrs['max'])
            
            # 先归零
            addLogFile("info", "🔄 先归零...")
            await page.evaluate(f"""
                (function() {{
                    const slider = document.getElementById('{slider_id}');
                    if (!slider) return;
                    
                    slider.value = {slider_min};
                    slider.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    slider.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }})()
            """)
            
            await asyncio.sleep(0.5)
            
            # 从 1% 到 200%
            addLogFile("info", f"🔄 从 1% 逐步增加...")
            
            for i in range(1, 201):  # 1% 到 200%
                # 计算当前百分比对应的滑块值
                percent = i / 100  # 1% = 0.01, 200% = 2.0
                current_slider_value = round(slider_min + (slider_max - slider_min) * min(percent, 1.0))
                
                # 设置滑块值
                await page.evaluate(f"""
                    (function() {{
                        const slider = document.getElementById('{slider_id}');
                        if (!slider) return;
                        
                        slider.value = {current_slider_value};
                        slider.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        slider.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }})()
                """)
                
                await asyncio.sleep(0.05)
                
                # 获取当前 valuenow
                slider = await page.find(f'input#{slider_id}')
                current_value = int(slider.attrs['aria-valuenow'].replace('.',''))
                
                # 每10步打印一次
                if i % 10 == 0 or i == 1:
                    addLogFile("info", f"  {i}%: 当前值={current_value}")
                
                # 如果达到目标值，停止
                if current_value >= target_value:
                    addLogFile("info", f"✅ 达到目标: {current_value} >= {target_value} (在 {i}% 位置)")
                    break
            
            # 最终验证
            slider = await page.find(f'input#{slider_id}')
            final_value = int(slider.attrs['aria-valuenow'].replace('.',''))
            addLogFile("info", f"✅ 设置完成: {final_value}")
            return True
            
        except Exception as e:
            addLogFile('err_info', traceback.format_exc(), True)
            return False


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
                timeout=20 
            )
            await acceptCookieBtn.click()

            await asyncio.sleep(1)
        except:
            pass
        # all_ranges = await self.page.find_all('input#range')

        # addLogFile("all_ranges_lenth", len(all_ranges))
        # total_amount_sel = await page.find('input#range-slider-amount')
        # await total_amount_sel.set_value('50.00')
        #
         
        await asyncio.sleep(2)
        total_amount_int = int(self.inputDicOri['total_amount'])
        addLogFile('info'," begin set_slider_value total_amount")
        await self.set_slider_value(page,'range-slider-amount', total_amount_int)
        
        await asyncio.sleep(5)
        durationint = int(self.inputDicOri['duration'])
        await self.set_slider_value(page,'range-slider-rate', durationint)

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
        img_elements = await page.find_all('//div[@id="img-secci"]/img', timeout = 60)
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
                                
                if i in [0,1]:
                    with open(f'image_{i}.png', 'wb') as f:
                        f.write(img_data)
                    print(f'img saved: image_{i}.png')

                    text = await asyncio.to_thread(
                        image_to_text,
                        f'image_{i}.png'
                    )
                    addLogFile(f'image_{i}.png', text)

                    if i == 0:
                        TS01 = text.split("Importo totale del credito")[1]\
                            .split(",00")[0]\
                            .replace('\n', ' ').replace('Euro',"")\
                            .replace('.','').strip()
                        addLogFile("TS01", TS01, True)
                        
                        TS13 = text.split("Importo Rata")[1]\
                            .split("Numero Rate")[0]\
                            .replace('\n', ' ').replace('Euro',"")\
                            .replace('.','').strip()

                        addLogFile("TS13", TS13, True)
                        
                        TS17 = text.split("Numero Rate")[1]\
                            .split("Periodicita' Mensile")[0]\
                            .replace('\n', ' ').strip()

                        addLogFile("TS17", TS17, True)

                        TS35 = text.split("Importo totale dovuto dal consumatore")[1]\
                            .split("Importo del capitale preso")[0]\
                            .replace('\n', ' ').replace('Euro',"")\
                            .replace('.','').strip()

                        addLogFile("TS35", TS35, True)

                        TS07 = text.split("Tasso di interesse o (se applicabile) tassi di interesse diversi che si applicano")[1]\
                            .split("al contratto di credito")[0]\
                            .replace('TAN','').replace('%','')\
                            .replace('\n', ' ').strip()

                        addLogFile("TS07", TS07, True)
                        TS09 = text.split("Tasso annuo effettivo globale (TAEG)")[1]\
                            .split("Costo totale del credito espresso in percentuale")[0]\
                            .replace('TAEG','').replace('%','')\
                            .replace('\n', ' ').strip()

                        addLogFile("TS09", TS09, True)

                    if i == 1:
                        TS23 = text.split("Spesa mensile gestione pratica")[1]\
                            .split("Imposta")[0]\
                            .replace('\n', ' ').replace('Euro',"")\
                            .replace('.','').strip()
                        addLogFile("TS23", TS23, True)

                        TS20 = text.split("Costi attivita' istruttoria")[1]\
                            .split("\n")[2]\
                            .replace('\n', ' ').replace('Euro',"")\
                            .replace('.','').strip()
                        addLogFile("TS20", TS20, True)




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




def getList(inputDicOri, csvFileName):
    errString = ""
    addLogFile("inputDicOri", inputDicOri)
    globals_and_constants.set_value("accept-la", "it-it")
    isStateOk = False
    outputDic = {}
    outputDic.clear()
    for k in range(5):

        port = globals_and_constants.INIT_PORTS[0]
        globals_and_constants.set_value("port", port)
        try:
            scraper = GetListScraper(port, inputDicOri,csvFileName)
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
