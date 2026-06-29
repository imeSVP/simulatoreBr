#!/usr/bin/env python
# -*- coding: utf-8 -*-


finalita_map = [
      {
        "code": "E",
        "description": "Ristrutturazione casa",
        "setChecked": True
      },
      {
        "code": "I",
        "description": "Auto usata",
        "setChecked": False
      },
      {
        "code": "H",
        "description": "Auto nuova o Km zero",
        "setChecked": False
      },
      {
        "code": "D",
        "description": "Arredamento",
        "setChecked": False
      },
      {
        "code": "W",
        "description": "Consolidamento",
        "setChecked": False
      },
      {
        "code": "Z",
        "description": "Liquidità",
        "setChecked": False
      },
      {
        "code": "Q",
        "description": "Spese mediche",
        "setChecked": False
      },
      {
        "code": "J",
        "description": "Motoveicolo nuovo",
        "setChecked": False
      },
      {
        "code": "K",
        "description": "Motoveicolo usato",
        "setChecked": False
      },
      {
        "code": "U",
        "description": "Matrimonio e cerimonie",
        "setChecked": False
      },
      {
        "code": "0",
        "description": "Green Casa",
        "setChecked": False
      },
      {
        "code": "S",
        "description": "Viaggi e vacanze",
        "setChecked": False
      },
      {
        "code": "T",
        "description": "Hobbies e tempo libero",
        "setChecked": False
      },
      {
        "code": "Y",
        "description": "Acquisto immobile/box",
        "setChecked": False
      },
      {
        "code": "V",
        "description": "Beni strumentali",
        "setChecked": False
      },
      {
        "code": "A",
        "description": "Informatica e PC",
        "setChecked": False
      },
      {
        "code": "B",
        "description": "Articoli elettronica",
        "setChecked": False
      },
      {
        "code": "F",
        "description": "Impianti per la casa",
        "setChecked": False
      },
      {
        "code": "P",
        "description": "Riparazione auto",
        "setChecked": False
      },
      {
        "code": "G",
        "description": "Elettrodomestici",
        "setChecked": False
      },
      {
        "code": "M",
        "description": "Camper usato",
        "setChecked": False
      },
      {
        "code": "L",
        "description": "Camper nuovo",
        "setChecked": False
      },
      {
        "code": "C",
        "description": "Corsi di formazione",
        "setChecked": False
      },
      {
        "code": "R",
        "description": "Estetica e benessere",
        "setChecked": False
      },
      {
        "code": "O",
        "description": "Nautica usato",
        "setChecked": False
      },
      {
        "code": "N",
        "description": "Nautica nuovo",
        "setChecked": False
      },
      {
        "code": "X",
        "description": "Green Veicoli",
        "setChecked": False
      },
      {
        "code": "1",
        "description": "Green Altre finalità",
        "setChecked": False
      }
    ]
cityMap = {
    '':'16006', #defualt Milan
    'Milano (MI)':'16006',
    'Torino (TO)':'10009'
}
assicurazioneMap= {'Yes':'1','No':'0'}
impiegoMap = {
    'Dipendente Privato':'1',
    'Dipendente Pubblico':'2',
    "Pensionato":'5',
    'Libero Professionista':'3',
    'Autonomo / Ditta individuale':'4',
    'Altro':'6',
    'Libero professionista':'3',
    'Altro impiego':'-1'

}
#'Dipendente Pubblico':'2',
impiegoAttualeMap = {
    'Dipendente Statale':'2',
    'Dipendente Pubblico':'3',
    'Dipendente Para-pubblico':'4',
    '':''
}

#"Pensionato":'5'
entePesioniMap = {
    'Inps - pensione di anzianità':'31',
    'Inps - pensione sociale':'32',
    'Altro ente':'33',
    '':''
}
#'Libero Professionista':'3',
alboMap = {
    'Architetto':'5',
    'Medico':'9',
    'Avvocato':'6',
    'Commercialista':'7',
    'Ingegnere':'3',
    'Notaio':'10',
    '':''
}
# 'Autonomo / Ditta individuale':'4',
settoreMap = {
    'Artigiano':'15',
    'Commerciante':'19',
    'Imprenditore':'22',
    'Agente di Assicurazione':'12',
    'Agricoltore/allevatore':'13',
    'Ambulante':'14',
    'Artista':'16',
    'Autotrasportatore':'17',
    'Collaboratrice domestica':'18',
    'Consulente':'20',
    'Geometra':'21',
    'Lavoratore a domicilio':'23',
    'Perito':'24',
    'Promotore finanziario':'25',
    'Ragioniere':'26',
    'Rappresentante/Agente':'27',
    'Socio di società':'28',
    'Sportivo professionista':'29',
    '':''
}


tipoContrattoMap = {
    "Determinato": '1',
    "Indeterminato":'2',
    '':''
}
numDipendentiMap = {
    'Meno di 5':'0',
    'Tra 5 e 15':'5',
    'Tra 16 e 29':'16',
    '30 e oltre':'30',
    '':''
}
