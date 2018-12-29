# 디스코드 롤 챗봇

python 으로 만든 discord bot입니다. 간략한 소스코드 설명입니다.

1. main.py: 디스코드 봇을 실행시키는 스크립트입니다. 명령어를 불러오고 작동하게 합니다.
2. discord_command.py: 명령어 함수가 들어있는 스크립트입니다. 반복 사용하는 함수는 따로 저장하고 불러와서 씁니다.
3. summoner_info.py: riotAPI를 다룰때 쓰는 스크립트입니다. 
4. util.py: db를 초기화시키거나, 경로 설정 및 불러오기를 할 때 쓰는 스크립트입니다. 토큰코드는 CREDENTIAL.py 에 저장해서 불러와야 합니다.
> discord 봇 토큰이나 riotAPI에 쓸 토큰의 경우 깃허브에 올리면 큰일납니다!! 

> 도용가능성 99%. 반드시 따로 저장하고 업로드 하지 맙시다.

이외에 discord_func.py, minDiffPartitioning.py는 명령어에서 자주 쓰이는 함수를 저장한 코드고  
discord_logging.py는 디버깅용 로그를 남길때 쓰는 스크립트입니다. 

사용한 라이브러리
1. numpy, pandas, sklearn 
2. discord

1번의 라이브러리는 https://winpython.github.io/ 에서 3.6.7버젼 다운받으면 있을거에요.  
2번의 경우 discord.py-rewrite.zip 파일을 다운받아서 다음 명령어로 설치해줍니다.  
`python -m pip install discord.py-rewrite.zip`


---

위 봇은 아래와 같이 작동합니다.  
  
  
`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/01.%20guide.gif)

`!dice` : 주사위 1~100 까지 굴리기

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/02.%20dice.gif)


`!voice` : 자신이 있는 채널 맴버들 출력

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/03.%20voice.gif)


`!rank` : !rank 아이디: Rank 확인하기

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/04.%20rank.gif)


`!most` : !most 아이디: MostN 확인하기. default: N=3, 기간=1

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/05.%20most.gif)


`!most N 기간` :  !most 아이디 N 기간: MostN 확인하기. 기간은 0~5 사이 지정. default: N=3, 기간=1

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/06.%20mostN.gif)


`!position` :  !position id1 id2 id3 id4 id5: 5명 팀일때 포지션 자동 분배하기

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/07.%20position.gif)


`!team` :  !team id1 id2 ... id10: 내전 10명일때 팀,포지션 자동 분배하기

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/08.%20team.gif)


`!setrank` : !setrank id1 rank number: id1의 rank를 수정합니다.

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/09.%20setrank.gif)


`!register` : !register id1: 자신의 discord 아이디를 id1으로 등록합니다.

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/10.%20register.gif)


`!register2` : !register2 id#tag id1: id#tag의 discord 아이디를 id1으로 등록합니다.

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/11.%20register2.gif)


`!predict` : !predict chmp1 chmp2 ... chmp10: 탑, 정글, 미드, 원딜, 서폿 순으로 두팀씩 조합을 제시해줬을 때, 어느 팀이 유리한지 예측해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/RiotDiscordAPI/master/images/12.%20predict.gif)
  
---

## 사용법

### @봇 !명령어

명령어를 입력하면 개인-맞춤형 음식이 추천되어 나옵니다.

### 명령어 모음

`help`,`food_list`,`food`, `no` , `yes`, `location`, `visualize`, `evaluation`
1. !food: 음식 하나를 추천해줍니다. 
2. !yes: !food 입력 후 이 음식이 마음에 들 경우, 근처 맛집을 검색할 수 있습니다.
3. !no: !food 입력 후 이 음식이 마음에 안 들 경우, 다음 음식을 추천 받을 수 있습니다.
4. !food_list: 명령어를 통해 전체 음식 리스트를 출력할 수 있습니다.
5. !location 위치: 명령어를 통해 검색할 지역을 지정할 수 있습니다. default는 강남역입니다. 
ex). !location 신촌역
6. !visualize: 음식의 선택 기준을 데이터 입력 갯수에 따라 시각화합니다.
7. !evaluation: 평가표를 출력합니다.

처음 이 서비스를 이용하는 경우, 10번동안 무작위 랜덤 추출로 음식을 추천해줍니다.
이후부터 음식 선호도 결과를 반영해 음식을 추천해줍니다.

---

## 디스코드 앱 설정법

1. 디스코드 앱부터 만듭니다.(https://discordapp.com/developers/applications/)

2. 봇을 만들게 되면 BOT_CLIENT_ID로 자신의 봇을 채널에 추가할 수 있습니다. 밑에서 설명 더 합니다!

3. Settings - Bot 메뉴에서 TOKEN키를 확인할 수 있습니다.

CREDENTIAL.py 에 DISCORD_TOKEN 명으로 해당 토큰값을 저장해줍시다!

4. 봇을 자신의 채널에 초대하기
https://discordapp.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot
YOUR_CLIENT_ID을 자신의 것에 맞게 변경하고 들어가면 됩니다.

---

### 소스 설명

```
#main.py: 봇을 실행시킬때 쓰는 소스입니다. 

#discord_command.py: 봇에 명령어를 추가하고 싶을 때 이 소스부분에 넣으면 됩니다.
소스 설명은 추후에 추가할 예정!

```

---

##### 질문이나 안되는 기능은 이슈에 적어 주세요.
