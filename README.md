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

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)

`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)


`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)


`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)


`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)


`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)

`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)


`!guide` : 명령어 입력 방법을 출력해줍니다.

![](https://raw.githubusercontent.com/JaehunSim/food_recommend_slack_bot/master/slack_bot/doc/4helpfood_list.gif)





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

## 설정법

1. 슬랙 앱부터 만듭니다.(https://api.slack.com/apps/)
![](https://www.fullstackpython.com/img/160604-simple-python-slack-bot/sign-in-slack.png)
저기서 만드시면 됩니다.

2. 만드신 후 여기(https://api.slack.com/bot-users)로 이동하셔서, 봇을 만드세요.
![](https://www.fullstackpython.com/img/160604-simple-python-slack-bot/custom-bot-users.png)
왜 앱에서 봇을 만드냐면, 앱만이 interaction(사용자의 버튼 클릭 등)을 할 수 있거든요!

3. oAuth도 만들어서 등록합니다.
![](https://raw.githubusercontent.com/hero0926/HQ_bot/master/slack2.png)

아래 있는 토큰을 TOKEN 에 등록하세요.

위 곳에서 등록할 수 있습니다.(사실 어디인지 찾기가 아주 불편합니다)

4. 이 내용들을 commandBook.py안에 등록하여 사용합니다.
> 자신의 개인정보는 소중하니 이 정보들을 깃허브 등에 올리지 않게 주의 하도록 하세요. (깃허브에 올리면 자동으로 토큰이 무효됩니다.)

> visualize_weight_change.py 에도 plotly.tools.set_credentials_file(username='자신의id', api_key='자신의api_key')를 입력하셔야 합니다.

5. 자기가 쓸 채널에 만든 봇을 추가하세요. `/invite @봇이름`

6. 	`python -m pip install plotly`
	`python -m pip install slackclient`로 필요한 라이브러리들을 설치 한 후,

7. 봇을 `python botV2.py` 로 실행 해 보세요

---

### 소스 설명

```
#botV2.py: 봇을 실행시킬때 쓰는 소스입니다. slackclient를 구동시킬 수 있고 이와 관련된 코드가 있습니다.

#commandBook.py: 봇에 명령어를 추가하고 싶을 때 이 소스부분에 넣으면 됩니다.
	#slack_client: 슬랙 클라이언트 설정을 하는 부분입니다.
	#dice: 무작위로 1~100 숫자를 출력해줍니다. 봇이 제대로 구동되고 있나 테스트할때 쓰면 유용합니다.
	#guide: 명령어를 보여주는 부분입니다. 
	#food_list: 음식 메뉴를 보여줍니다.
	#food: 음식 메뉴를 한가지 추천해줍니다. 이미지 출력이 시간이 오래 걸려 이미지출력파트를 빼면 빠른 반응속도를 기대할 수 있습니다.
	#yes: 추천된 음식이 마음에 들면 설정한 지역명 + 음식명으로 웹에서 검색후 결과값을 출력해줍니다. 추천된 log_id와 yes 값을 디비에 저장합니다. !food나 !no 입력후 120초 내로 응답해야만 됩니다.
	#no: 추천된 음식이 마음에 안 들면 추천된 food_id와 no 값을 디비에 저장합니다. !food 과정을 반복합니다. !food 입력후 120초 내로 응답해야만 됩니다.
	#set_loc: 사용자의 지역값을 설정할 수 있습니다. 사용자의 id와 지역값을 디비에 저장합니다.
	#visualize: 로그가 쌓임에 따라 사용자별로 추천 과정이 어떻게 이루어졌는지 각 음식 값들의 weight들을 보여주어 visualize 합니다.
	#evaluation: 설문 응답값을 넣으면(제가 조사한 결과값이 default로 넣어져 있습니다.) 제가 고안한 평가 방법에 따라 성능 평가 후 그래프를 출력합니다.
	


```

---

##### 질문이나 안되는 기능은 이슈에 적어 주세요.
