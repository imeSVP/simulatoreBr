#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import nodriver as uc
import globals_and_constants
import time
from addLogtoFile import createNewFile, addLogFile
import json
import urllib.parse
import random
import requests

my_key = "3da74b773dc0832937e86caa8e85cfff"
country = 'it'

class Scraper:
    main_tab: uc.Tab

    USERNAME = globals_and_constants.USERNAME
    PASSWORD = globals_and_constants.PASSWORD   

    datadomeCodez: str

    br = None
    page = None

    def __init__(self,port):
        self.datadomeCodez = "NULL" 
        uc.loop().run_until_complete(self.run(port))

    def getDataDomeCodez(self):
        current_datadomeCodez= self.datadomeCodez
        for i in range(100):
            current_datadomeCodez= self.datadomeCodez
            addLogFile("current_datadomeCodez",current_datadomeCodez)
            if not "NULL" in current_datadomeCodez:
                time.sleep(1)
                break
        return current_datadomeCodez

    async def run(self,port):
        try:
            await page.close()
        except:
            pass
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        PROXY = f"{country}-{globals_and_constants.ENDPOINT}:{port}"
        browser = await uc.start(
            browser_args=[
                #f'--user-agent={user_agent}',
                f"--proxy-server={PROXY}",
                "--accept-lang=it-IT"
            ],
            no_sandbox=True
        )
        self.main_tab = await browser.get("draft:,")
        self.main_tab.add_handler(uc.cdp.fetch.RequestPaused, self.req_paused)
        self.main_tab.add_handler(
            uc.cdp.fetch.AuthRequired, self.auth_challenge_handler
        )
        await self.main_tab.send(uc.cdp.fetch.enable(handle_auth_requests=True))
        #page = await browser.get("https://api.ipify.org?format=json")
        #await asyncio.sleep(3)
        page = await browser.get("https://www.prestitionline.it/prestiti-personali/scheda-prestito.asp?gs=eb903b4c-2161-4cc6-99b8-106e93c2b66f&fad=KmY%2br6mYGnjgokexWh9nWsZnL06tYpqNmi30q6Fl9okCC5a6kUEFrRpQcli9cK8dNPmRjFXtlwFdNrFMeKusHmc99mBqwCqFIcJng3%2fcxbP%2bfYy7p97v9HGYNlcPMEovp6hHxpdWvsRf1F%2bgeYcEdQ%3d%3d&posizioneOfferta=1&codFinalitaRicerca=E&codProfessioneRicercaPP=1&giorniErogazione=3&finanziabilita=NELLA+MEDIA")
        
        for i in range(5):

            await asyncio.sleep(5)
            frame_data = await self.main_tab.send(uc.cdp.page.get_frame_tree())
            current_url = frame_data.frame.url
            addLogFile('current_url',current_url)
            current_html = await page.get_content()
            if not "'t':'fe'"in current_html:
                addLogFile('info','no fe')
                break
            
        requests_style_cookies = await browser.cookies.get_all(requests_cookie_format=True)

        # use in requests:
        for cookieItem in requests_style_cookies:
            cookieStr = str(cookieItem)
            addLogFile("cookieItem", cookieStr)
            if "datadome=" in cookieStr:
                datadomeCode = cookieStr.split('datadome=')[1].split('for')[0].strip()
                break
        addLogFile('datadomeCode',datadomeCode)
        self.datadomeCodez = datadomeCode
        
        self.br = browser
        await asyncio.sleep(5000)
        await asyncio.sleep(3)
        #await page.close()

    async def get_browser(self):
        pass
        return self.br

    async def goto(self,url_str):
        page = await self.br.get(url_str)
        return page

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


if __name__ == "__main__":
    createNewFile()
    port = random.randint(20001,29999)
    scraper = Scraper(port)
    datadomez= scraper.getDataDomeCodez()
    addLogFile('datadomez',datadomez)
    #scraper.goto("https://www.prestitionline.it/prestiti-personali/")
    time.sleep(5000)
