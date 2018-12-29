# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
from CREDENTIAL import DISCORD_TOKEN,DISCORD_TOKEN_TEST, RIOT_API_KEY
from sklearn.externals import joblib
PATH = os.path.dirname(os.path.realpath(sys.argv[0]))[:-5]
DB_PATH = PATH + "\\db"
REGION = "kr"
RF_MODEL = joblib.load(DB_PATH+"\\my_model.pkl")
ptpDFList = []
for i in range(23):
    ptpDFList.append(pd.read_csv(DB_PATH+"\\ptp\\data_"+str(i)+".csv", index_col=0))
    
def initialize():
    initial = pd.DataFrame([],columns = ['summonerName', 'summonerId', 'accountId', 'rank', 'pp','updated_date'])
    initial.to_csv(DB_PATH + '\\summonerNameData.csv', index=False, encoding="euc-kr")

def initialize_discord():
    initial = pd.DataFrame([],columns = ['discord_id_tag', 'nickname'])
    initial.to_csv(DB_PATH + '\\discordNickNameChange.csv', index=False, encoding="euc-kr")
    
def changeStrToList(str1):
    result = []
    temp = str1.split(",")
    result.append([temp[0][3:-1],int(temp[1][1:-1])])
    result.append([temp[2][3:-1],int(temp[3][1:-2])])
    return result