#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os
import sys
def get_csv(productData,csvfileName):

    #fileName = globals_and_constants.get_value('csv_filename')
    fileName = csvfileName
    file_exists = os.path.exists(fileName)
    if not file_exists:
        #Create the file and write the data
        with open(fileName, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f,productData.keys())
            writer.writeheader()
            writer.writerow(productData)
    else:
        #Opens file and append new datas
        with open(fileName, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f,productData.keys())
            # Veriyi dosyaya ekle
            writer.writerow(productData)
    return True
