from flask import Flask, render_template, request
from bs4 import BeautifulSoup as BTS
import requests
import os
import sys

app = Flask(__name__, template_folder="views")

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route("/search")
def search():
    summoner = request.args.get('summoner')
    str_api = '?api_key='
    riot_api_keys = os.getenv('RIOT_API_KEY')
    url = "https://kr.api.riotgames.com/"
    get_id_url = "lol/summoner/v4/summoners/by-name/"
    
    print(url+get_id_url+summoner+str_api+riot_api_keys)
    id_req = requests.get(url+get_id_url+summoner+str_api+riot_api_keys)
    id_req_dict = id_req.json()
    enc_account = id_req_dict.get('accountId')
    enc_summoner = id_req_dict.get('id')

    get_rank_url = "/lol/league/v4/positions/by-summoner/" #encryptedSummonerId
    get_match_url = "/lol/match/v4/matchlists/by-account/" #encryptedAccountId
    
    rank_req = requests.get(url+get_rank_url+enc_summoner+str_api+riot_api_keys)
    match_req = requests.get(url+get_match_url+enc_account+str_api+riot_api_keys)
    
    rank_dict = rank_req.json()
    match_dict = match_req.json()
    
    result = {}
    
    for i in rank_dict:
        if i['queueType'] == 'RANKED_SOLO_5x5':
            result = {
                "소환사":summoner,
                "티어":i['tier'], "랭크":i['rank'], 
                '승':i['losses'],'패':i['wins']
            }

    return render_template('search.html', rank_req=result)
    
@app.route("/search2")
def search2():
    userInput = request.args.get('summoner')
    
    #
    #
    
    url = "http://www.op.gg/summoner/userName="
    response = requests.get(url+userInput)
    
    # 2. 승, 패 정보만 가져온다.
    doc = BTS(response.text)
    
    wins = doc.select_one("#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div.SummonerRatingMedium > div.TierRankInfo > div.TierInfo > span.WinLose > span.wins").text
    loses = doc.select_one("#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div.SummonerRatingMedium > div.TierRankInfo > div.TierInfo > span.WinLose > span.losses").text
    
    
    return render_template('search2.html',userInput=userInput, wins=int(wins[:-1])+15, loses=loses[:-1])