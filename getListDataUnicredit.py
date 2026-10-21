#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from camoufox.async_api import AsyncCamoufox
from playwright.async_api import Locator
import asyncio
from logging import exception
# import nodriver as uc
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
# from Update_heartbeat import update_heartbeat
import os
import sys



country = "it"

class GetListScraper:
    # main_tab: uc.Tab

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
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        try:
            asyncio.run(self.run(port))
        except:
            errString = f"fillFormError: {traceback.format_exc()}"
            raise BaseException(errString)


    def __del__(self):

        addLogFile("info_del", "__del__")
    ''' 
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
    '''
    async def type_human_with_verify(self, element: Locator, value):
        """逐字符输入并验证 (Playwright / Camoufox 版本)"""
        value_str = str(value)
        
        # 1. 点击元素
        await element.click()
        await asyncio.sleep(2)  # 保持原有的 2 秒等待
        
        # 2. 用 JS 清空并触发 React/Vue 事件
        # Playwright 的 evaluate 第一个参数是 JS 表达式，第二个参数传给 JS 函数
        await element.evaluate("""
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
        
        # 3. 逐字符输入
        # 方案 A：如果你想严格控制每个字的随机延迟，继续用循环：
        for char in value_str:
            await element.press(char) # 或者使用 page.keyboard.type(char)
            await asyncio.sleep(0.15)
            
        # 💡 方案 B (更优雅的 Playwright 自带原生仿真人类输入)：
        # Playwright 提供了 delay 参数（单位是毫秒！），可以直接一行搞定：
        # await element.press_sequentially(value_str, delay=150)
        
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
            acceptCookieBtn = await page.query_selector(
                f'xpath=//button[contains(text(),"ACCETTO TUTTI I COOKIE")]'
            )
            await acceptCookieBtn.click(timeout=5000)

            await asyncio.sleep(1)
        except:
            pass
        # '''
        #
        prestitiBtn = await page.query_selector(
            'xpath=//a[@href="/it/privati/prestiti.html"]',
        )
        await prestitiBtn.click(timeout=5000)

        await asyncio.sleep(5)

        findMoreBtn = await page.query_selector(
            'xpath=//a[contains(text(),"Scopri di più")]',
        )
        await findMoreBtn.click(timeout=5000)

        await asyncio.sleep(5)
        askBtn = await page.query_selector(
            'xpath=//a[text()="Procedi con la richiesta da qui"]',
        )
        await askBtn.click(timeout=5000)
        
        await asyncio.sleep(2)
        askOnlineBtn = await page.query_selector(
            'xpath=//button[text()="Richiedi Online"]',
        )


        
        await askOnlineBtn.click(timeout=5000)
        #
        # 在点击前开始监听所有响应
        await asyncio.sleep(5)
        # await page.reload(wait_until="domcontentloaded")
        # await asyncio.sleep(5)
        # '''
        #
        #
        '''
        page.goto("https://prodotti-per-te.unicredit.it/loginPublic?state=%2Fworkflow%2FCFN_V4")

        await asyncio.sleep(5)
        
        await page.reload(wait_until="domcontentloaded")
        await asyncio.sleep(10)  # 给页面一点反应时间
        '''
        '''
        print("===== 点击后诊断 =====")
        print("当前 URL:", page.url)
        print("当前标题:", await page.title())
        print("页面数量:", len(page.context.pages))
        for i, p in enumerate(page.context.pages):
            print(f"  标签 {i}: {p.url}")
        print("======================")

        # 直接等金额输入框出现，给它 60 秒时间
        try:
            await page.wait_for_selector('input#requested_amount_input', timeout=60000)
            print("✅ 金额输入框已出现，进入下一步")
        except Exception as e:
            print(f"❌ 等不到金额框，错误: {e}")
            # 卡住了，先不管，看看到底停在哪
            await asyncio.sleep(30)
        '''
        for n_time in range(20):
            addLogFile('info', f"wait .... {n_time}")
            total_amount_sel = await page.query_selector(
                'xpath=//input[@id="requested_amount_input"]',
            )
            try:
                await total_amount_sel.click(timeout=5000)
                
                # await asyncio.sleep(5)
                break
            except:

                await asyncio.sleep(5)
                btn_ricomincia = await page.query_selector(
                    'xpath=//button/span[text()="Ricomincia"]',
                )
                try:
                    await btn_ricomincia.click(timeout=5000)
                except:
                    pass
                if n_time % 4 == 3:

                    # page.goto("https://prodotti-per-te.unicredit.it/loginPublic?state=%2Fworkflow%2FCFN_V4")
                    await page.reload(wait_until="domcontentloaded")


        total_amount_int = self.inputDicOri['total_amount']
        # total_amount_int = 30000 
        addLogFile("total_amount_value", str(total_amount_int))
                 
        await asyncio.sleep(5)
        await self.type_human_with_verify(total_amount_sel, total_amount_int)

        await asyncio.sleep(5)

        rata_mensile_sel = await page.query_selector(
            'xpath=//input[@aria-label="select options"]'
        )

        await rata_mensile_sel.click()

        await asyncio.sleep(5)

        rata_mensile_li_list = page.locator('xpath=//*[@id="react-select-2-listbox"]/div')

        for rata_mensile_time in range(5):

            try:
                first_element_text = await rata_mensile_li_list.nth(0).inner_text()
            except Exception:
                first_element_text = ""

            if "No options" in first_element_text or not first_element_text:
                await asyncio.sleep(5)
                # 更新定位器
                rata_mensile_li_list = page.locator(
                    'xpath=//div[contains(@id, "react-select-") and contains(@id, "-listbox")]'
                )
            else:
                break

        list_count = await rata_mensile_li_list.count()
        for rata_mensile_timez in tqdm(range(list_count), desc="rate", leave=False):
            rata_mensile_timeyz = rata_mensile_timez + 1
            
            # 1. 定位当前循环的下拉项并获取文本、点击
            rata_mensile_li = page.locator(
                f'xpath=(//div[contains(@id, "react-select-") and contains(@id, "-listbox")]/div)[{rata_mensile_timeyz}]'
            )
            
            # 获取文本并清洗
            rata_mensile_str = (await rata_mensile_li.inner_text()).replace('€', '').strip()
            addLogFile('rata_mensile', rata_mensile_str)
            
            # 点击该选项
            await rata_mensile_li.click()

            # 显式等待数据刷新（保持原逻辑的 5 秒，或者建议使用后文的 wait_for 优化）
            await asyncio.sleep(5)
            
            # 2. 抓取刷新后的页面数据
            TS15Sel = page.locator('xpath=(//div/span[text()=" mesi"])/../span[2]')
            TS15Str = await TS15Sel.inner_text()
            addLogFile('TS15Str', TS15Str)

            TS16Sel = page.locator('xpath=(//div/span[text()=" mesi"])/../span[4]')
            TS16Str = await TS16Sel.inner_text()
            addLogFile('TS16Str', TS16Str)

            TS07Sel = page.locator('xpath=(//span[text()="TAN"])/../../../div[2]/span')
            TS07Str = (await TS07Sel.inner_text()).replace('%', '').strip()
            addLogFile('TS07Str', TS07Str)
            
            TS09Sel = page.locator('xpath=(//span[text()="TAEG"])/../../../div[2]/span')
            TS09Str = (await TS09Sel.inner_text()).replace('%', '').strip()
            addLogFile('TS09Str', TS09Str)
            
            # 3. 组装数据并输出
            outTemp = {}
            # outTemp.clear() # 字典刚定义，无需 clear
            outTemp['TS01'] = total_amount_int
            outTemp['TS13'] = rata_mensile_str
            outTemp['TS15'] = TS15Str
            outTemp['TS16'] = TS16Str
            outTemp['TS07'] = TS07Str
            outTemp['TS09'] = TS09Str

            await self.getDetails(outTemp)
            # 1. 定位元素（Playwright 的 locator 是惰性的，这一步不需要 await 和 timeout）
            rata_mensile_sel = page.locator('xpath=//input[@aria-label="select options"]')

            # 2. 点击元素（在操作时传入 timeout，单位为毫秒，5秒对应 5000）
            # Playwright 会自动等待元素可见并处于可点击状态（Actionability）
            await rata_mensile_sel.click(timeout=5000)

            # 3. 保持原逻辑的固定等待
            await asyncio.sleep(5)




        '''
         
        for rata_mensile_timez in tqdm(range(len(rata_mensile_li_list)), desc="rate", leave=False):
            rata_mensile_timeyz = rata_mensile_timez + 1
            rata_mensile_li = await page.find(
                f'(//div[contains(@id, "react-select-") and contains(@id, "-listbox")]/div)[{rata_mensile_timeyz}]'
            )
            rata_mensile_str = rata_mensile_li.text_all.replace('€','').strip()
            addLogFile('rata_mensile', rata_mensile_str)
            
            await rata_mensile_li.click()

            await asyncio.sleep(5)
            
            TS15Sel = await page.find('(//div/span[text()=" mesi"])/../span[2]')
            TS15Str = TS15Sel.text_all
            addLogFile('TS15Str', TS15Str)
 
            TS16Sel = await page.find('(//div/span[text()=" mesi"])/../span[4]')
            TS16Str = TS16Sel.text_all
            addLogFile('TS16Str', TS16Str)


            

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
            outTemp['TS15'] = TS15Str
            outTemp['TS16'] = TS16Str
            outTemp['TS07'] = TS07Str
            outTemp['TS09'] = TS09Str

            await self.getDetails(outTemp) 



            rata_mensile_sel = await page.find(
                '//input[@aria-label="select options"]',
                timeout = 5
            )
            await rata_mensile_sel.mouse_click()

            await asyncio.sleep(5)

        '''
        await asyncio.sleep(3)

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
        TS15 = outTemp['TS15']
        TS16 = outTemp['TS16']
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
        await self.context.close()




    async def brInit(self, port):
        target_url = "https://www.unicredit.it/"
        context = await self.br.new_context(
            locale="it-IT",
            timezone_id="Europe/Rome"  # 强制锁定罗马时区，斩断时区差引发的 Bot 标记
        )
        context = await self.br.new_context(
            locale="it-IT",
            timezone_id="Europe/Rome"  # 强制锁定罗马时区，斩断时区差引发的 Bot 标记
        )
        page = await context.new_page()

        # await context.clear_cookies()
        # await page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        # await page.goto("about:blank") # 彻底切断之前的页面状态
        # addLogFile("info",f"====== 2. 正在通过域名代理跨越 DataDome 边界: {target_url} ======")
        
        await page.goto('https://api.ipify.org?format=json')

        await asyncio.sleep(4)
        # 发起请求。由于经过海外住宅网络域名路由，我们将超时时间放宽至 35 秒以应对国际链路抖动
        await page.goto(target_url, wait_until="domcontentloaded", timeout=35000)
        
        # 成功进站后，给予探针 JavaScript 4 秒的数据比对与信任刷新时间
        
        title = await page.title()
        current_url = page.url
        content = await page.content()
        self.context = context
        self.page = page
        # await asyncio.sleep(400)

        
        



    '''
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
    '''
    async def run(self, port):

        proxy_config = {
            "server": f"http://{globals_and_constants.ENDPOINT}:{port}",
            "username": globals_and_constants.USERNAME,
            "password": globals_and_constants.PASSWORD
        }
        addLogFile("info", "====== 1. [完美域名合体] 正在初始化 Camoufox 内核并绑定住宅代理 ======")

        async with AsyncCamoufox(
            headless=False,             # Windows Server 上可直接开启高效后台无头模式
            proxy=proxy_config,         # 绑定您提供的有密住宅代理
            os="windows",               # 模拟的用户操作系统指纹，与您的宿主机完美共鸣
            geoip=True,                 # 根据代理 IP 自动下发同步意大利当地时区、语言环境
            humanize=True,
            block_images=False,         # 必须保持图片加载，用以通过 DataDome 隐式的画布图形校验
        ) as browser:
            self.br = browser 
            await asyncio.wait_for(self.brInit(port), timeout=20)
            await asyncio.wait_for(self.fillForm(), timeout=600)
            fillFormState = True





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
    for i in range(5):
        
        try:
            getList(inputDicOri)
            break
        except:
            pass
