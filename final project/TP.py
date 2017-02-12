# Kai Lung
# Andrew ID: klung
# Section: MM
# TERM PROJECT

######################################
#             WELCOME TO             #
# _   _ _    _ _        __ __ ___    #
# | \ | | |  | | |      /_ /_ |__\   #
# |  \| | |__| | |       | || |  ) | #
# | . ` |  __  | |       | || | / /  #
# | |\  | |  | | |____   | || |/ /_  #
# |_| \_|_|  |_|______|  |_||_|____| #
######################################

from bs4 import BeautifulSoup
from tkinter import *
import requests, webbrowser
from datetime import date
import random, math

# framework from course website
# http://www.cs.cmu.edu/~112/notes/events-example0.py

##### PLAYER CLASSES #####

class Player(object):
	def __init__(self, cx, cy, r, number, vx=0, vy=0):
		self.cx, self.cy, self.r = cx, cy, r
		self.number = number
		self.vx, self.vy = vx, vy

	def move(self):
		self.cx += self.vx
		self.cy += self.vy

class Forward(Player):
	pass

class Defense(Player):
	pass

class Goalie(Player):
	pass

class Puck(object):
	def __init__(self, cx, cy, r, vx=0, vy=0):
		self.cx, self.cy, self.r = cx, cy, r
		self.vx, self.vy = vx, vy

	def move(self):
		self.cx += self.vx
		self.cy += self.vy

##### INIT #####

def initIntro(data):
	data.mode = "intro"
	data.introImage = PhotoImage(file = "images/intro.gif") # http://www.zastavki.com/pictures/originals/2014/Sport___Hockey_Hockey_player_of_los_angeles_Drew_Doughty_055932_.jpg
	data.loadCount = 0

def init(data):
	initSplash(data)
	initRink(data)
	initTeams(data)
	initSummary(data)
	data.FantasyOrSimulate = "simulate"
	data.loadCount = 0
	loadImages(data)
	data.mode = "splash" # todo: change to splash

def loadImages(data):
	data.playersImage = PhotoImage(file = "images/players.gif") # http://previews.123rf.com/images/untouchablephoto/untouchablephoto1112/untouchablephoto111200106/11625382-ice-rink-blue-background-Stock-Photo-hockey.jpg
	data.loadImage = PhotoImage(file = "images/loading.gif") # http://neselects.com/wp-content/uploads/2015/05/hockey-rink-background-min.jpg
	data.splashImage = PhotoImage(file = "images/splash.gif") # http://i42.tinypic.com/69fjq1.png
	data.rinkImage = PhotoImage(file = "images/rink.gif") # http://wallpapercave.com/wp/TRDVduj.jpg
	data.goalImages = [PhotoImage(file = "images/goal/goal1.gif").subsample(4), # http://hockeypngs.com/wp-content/uploads/2016/09/Senko-PNG.png
					   PhotoImage(file = "images/goal/goal2.gif")] # http://i43.tinypic.com/295tpxd.jpg
	data.intermissionImages = [PhotoImage(file = "images/intermission/intermission1.gif").subsample(8), # http://i.imgur.com/VwVpkKy.png
							   PhotoImage(file = "images/intermission/intermission2.gif").subsample(4)] # http://i.imgur.com/2pCH1Oa.png
	data.linesImages = [PhotoImage(file = "images/lines/lines1.gif").subsample(3), # http://i246.photobucket.com/albums/gg95/ccrenders/275Kane.png
						PhotoImage(file = "images/lines/lines2.gif").subsample(2)] # http://www.vhlforum.com/uploads/gallery/album_1/gallery_16_1_441157.png
	data.summaryImages = [PhotoImage(file = "images/summary/summary1.gif").subsample(8), # http://i.imgur.com/trbKF5O.png
						  PhotoImage(file = "images/summary/summary2.gif").subsample(4)] # http://i.imgur.com/MEmnNV0.png
	data.nhlTodayImage = PhotoImage(file = "images/nhlToday.gif") # https://s-media-cache-ak0.pinimg.com/originals/97/0e/30/970e300bb5db979d12096f72cfbca5a8.jpg
	
def initSplash(data): # initialize splash screen
	data.boxHeight = data.height*3/20
	data.boxSpacing = data.height/20
	data.marginX = data.width/6
	data.splashcx = data.width*3/10
	data.NHLToday = (data.boxHeight + 2*data.boxSpacing, "NHL TODAY")
	data.Fantasy = (data.NHLToday[0] + 2*data.boxSpacing, "FANTASY")
	data.Simulate = (data.Fantasy[0] + 2*data.boxSpacing, "SIMULATE")
	data.About = (data.Simulate[0] + 2*data.boxSpacing, "HELP")
	data.modes = [data.NHLToday, data.Fantasy, data.Simulate, data.About]

def initTeams(data): # initialize team selection screen
	getTeams(data)
	getAbbrevs(data)
	data.teams = []
	data.teamSelectMessage = "SELECT THE HOME TEAM"
	data.selectedTeamsRowCol = []
	data.forwardLines = ["1st Line", "2nd Line", "3rd Line", "4th Line"]
	data.defenseLines = ["1st Pairing", "2nd Pairing", "3rd Pairing"]

	data.teamsSorted = sorted(data.NHLteams)
	data.teamsRows = 15
	data.teamsCols = 2
	data.teamsMarginX = data.width/10
	data.teamsMarginY = data.height/5 # init # initialize team selection screen

def initSummary(data):# initialize summary screen
	data.boxscoreRows = 3
	data.boxscoreMarginX = data.width/10
	data.boxscoreMarginY = data.height/5

def initPlayers(data):
	data.homeForwardLines, data.homeDefenseLines, data.homePlayers, data.homeGoalies = getPlayers(data, data.teams[0]) # init home team
	data.awayForwardLines, data.awayDefenseLines, data.awayPlayers, data.awayGoalies = getPlayers(data, data.teams[1]) # init away team

def initPlayerLocations(data): # initialize player visualizations
	data.playerR = 20
	data.homeLW = Forward(data.rinkCX - 30, data.rinkCY/2, data.playerR, "LW")
	data.homeC = Forward(data.rinkCX - 30, data.rinkCY, data.playerR, "C")
	data.homeRW = Forward(data.rinkCX - 30, data.rinkCY*3/2, data.playerR, "RW")
	data.homeLD = Defense(data.rinkX0 + data.zoneWidth - 30, data.height/3, data.playerR, "LD")
	data.homeRD = Defense(data.rinkX0 + data.zoneWidth - 30, data.height*2/3, data.playerR, "RD")
	data.homeG = Goalie(data.rinkX0 + 30, data.rinkCY, data.playerR, "G", vx=1)

	data.awayRW = Forward(data.rinkCX + 30, data.rinkCY/2, data.playerR, "RW")
	data.awayC = Forward(data.rinkCX + 30, data.rinkCY, data.playerR, "C")
	data.awayLW = Forward(data.rinkCX + 30, data.rinkCY*3/2, data.playerR, "LW")
	data.awayRD = Defense(data.rinkX1 - data.zoneWidth + 30, data.height/3, data.playerR, "RD")
	data.awayLD = Defense(data.rinkX1 - data.zoneWidth + 30, data.height*2/3, data.playerR, "LD")
	data.awayG = Goalie(data.rinkX1 - 30, data.rinkCY, data.playerR, "G", vx=-1)

	data.homeTeam = [data.homeLW, data.homeC, data.homeRW, data.homeLD, data.homeRD, data.homeG]
	data.awayTeam = [data.awayRW, data.awayC, data.awayLW, data.awayRD, data.awayLD, data.awayG]

	data.puck = Puck(data.width/2, data.height/2, 10, vx=10, vy=10)

	data.playerSpeed = 10
	initPlayerSpeeds(data)

def initGame(data): # initialize game
	initPlayerLocations(data)
	data.homeColor = "black"
	data.awayColor = "white"
	data.homeFill = "white"
	data.awayFill = "black"
	data.clock = 20*60 # 20 min * 60s/min
	data.clockSpeed = 1
	data.period = 1
	data.homeScore = 0
	data.awayScore = 0
	data.gameStart = True
	data.playStopped = True # initialize game screen
	data.intermission = False
	data.goalScored = False
	data.gameOver = False
	data.goalInfo = ""

def initPlayerSpeeds(data): # initialize speeds for visualization
	for player in data.homeTeam[:-1] + data.awayTeam[:-1]:
		player.vx = random.randint(-data.playerSpeed, data.playerSpeed)
		player.vy = random.randint(-data.playerSpeed, data.playerSpeed)

def initRink(data): # initialize ice rink for game
	data.rinkWidth = data.width*3/5
	data.rinkHeight = data.height*3/5
	data.zoneWidth = data.width/5

	data.rinkX0 = data.width/5
	data.rinkY0 = data.height/5
	data.rinkX1 = data.rinkX0 + data.rinkWidth
	data.rinkY1 = data.rinkY0 + data.rinkHeight
	data.rinkCX = (data.rinkX0 + data.rinkX1)/2
	data.rinkCY = (data.rinkY0 + data.rinkY1)/2

	data.topBoardsXY = (data.rinkX0, data.rinkY0, data.rinkX1, data.rinkY0)
	data.bottomBoardsXY = (data.rinkX0, data.rinkY1, data.rinkX1, data.rinkY1)
	data.leftGoalLineXY = (data.rinkX0, data.rinkY0, data.rinkX0, data.rinkY1)
	data.rightGoalLineXY = (data.rinkX1, data.rinkY0, data.rinkX1, data.rinkY1)
	data.centerRedLineXY = (data.rinkCX, data.rinkY0, data.rinkCX, data.rinkY1)
	data.leftBlueLineXY = (data.rinkX0 + data.zoneWidth, data.rinkY0, data.rinkX0 + data.zoneWidth, data.rinkY1)
	data.rightBlueLineXY = (data.rinkX1 - data.zoneWidth, data.rinkY0, data.rinkX1 - data.zoneWidth, data.rinkY1)

	data.leftEndX = data.zoneWidth/2
	data.rightEndX = data.width - data.leftEndX
	data.leftBoardsXY = (data.leftEndX, data.rinkY0, data.leftEndX + data.zoneWidth, data.rinkY1)
	data.rightBoardsXY = (data.rightEndX - data.zoneWidth, data.rinkY0, data.rightEndX, data.rinkY1)

	data.netDepth = data.width/30
	data.leftNetXY = (data.rinkX0 - data.netDepth, data.rinkCY - data.netDepth, data.rinkX0, data.rinkCY + data.netDepth)
	data.rightNetXY = (data.rinkX1, data.rinkCY - data.netDepth, data.rinkX1 + data.netDepth, data.rinkCY + data.netDepth)

def initFantasy(data): # initialize fantasy screen
	data.forwardRows = 4
	data.forwardCols = 3
	data.defenseRows = 3
	data.defenseCols = 2
	data.goalieRows = 2
	data.goalieCols = 1
	data.fantasyCurrRowCol = None
	data.fantasyLine = ""
	data.fantasyTeam = []
	data.fantasyStats = dict()
	data.allStats = dict()
	data.allPlayers = dict()
	data.allGoalies = dict()
	data.forwardTeamCells = dict()
	data.defenseTeamCells = dict()
	data.goalieTeamCells = dict()
	data.fantasySelectTeam = ""
	data.fantasyOpponent = ""
	data.fantasySelectDone = False
	data.homeStats = dict()
	data.currPlayer = ""
 
def initRosterScreen(data): # initialize roster screen
	data.numPlayers = len(data.homePlayers)
	data.rosterRows = math.ceil(data.numPlayers//2)
	data.rosterCols = 2

def initNHLToday(data): # initialize NHL today
	data.date = date.today()
	getGames(data)
	data.gamesRows = len(data.games)
	data.gamesCols = 3
	data.gamesMarginX = data.width/5
	data.gamesMarginY = data.height/10
	data.gamesGridWidth = data.width - 2*data.gamesMarginX
	data.gamesGridHeight = data.height - 2*data.gamesMarginY

##### WEB SCRAPING #####

def getTeams(data): # get all the NHL teams
	url = "https://www.nhl.com/info/teams"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	generalData = soup.find_all("section", {"class":"conference"})

	data.conferences = []
	data.divisions = []
	data.NHLteams = []

	for info in generalData:
		data.conferences += info.find("h2")
		data.divisions += info.find_all("h3")
	data.divisions = [division.text for division in data.divisions]

	generalData = soup.find_all("div", {"class":"ticket-team"})
	for info in generalData:
		data.NHLteams += [info.find_all("a")[0].text.strip().replace("é", "e").replace(".", "")]

def getPlayers(data, team): # get players on NHL team
	teamId = "-".join(team.lower().split())
	url = "http://leftwinglock.com/line-combinations/%s/?team=%s&strength=EV&gametype=GD" % (teamId, teamId)
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	info = soup.find_all("div", {"class":"table-container"})
	players = []

	for player in info:
		links = player.find_all("a")
		for link in links:
			players += [link.text]
	forwardLines, defenseLines = dict(), dict()
	i = 0
	for key in data.forwardLines:
		forwardLines[key] = players[i:i+3]
		i += 3
	for key in data.defenseLines:
		defenseLines[key] = players[i:i+2]
		i += 2

	goalies = getGoalies(teamId)
	return forwardLines, defenseLines, players, goalies

def getGoalies(teamId): # get the goalies
	url = "http://www.chirphockey.com/nhl-line-combinations/%s/" % teamId
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	info = soup.find_all("div", {"id":"pp2"})
	
	goalies = []
	for goalie in info:
		goalies += goalie.find_all("l5")
	goalies = [goalie.text for goalie in goalies[-2:]]

	return goalies

def getAbbrevs(data): # get NHL team abbreviations
	url = "https://en.wikipedia.org/wiki/Template:NHL_team_abbreviations"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	generalData = soup.find_all("p")
	teams = []
	abbrevMap = dict()

	for info in generalData:
		teams += info.text.splitlines()

	for team in teams:
		teamInfo = team.split("–")
		try:
			teamName = teamInfo[1].strip().replace(".", "")
			teamAbbrev = teamInfo[0].strip()
		except:
			pass
		if len(teamAbbrev) == 3:
			abbrevMap[teamName] = teamAbbrev
	abbrevMap["New Jersey Devils"] = "NJD" # necessary hardcode as the website listed them as just NJ
	abbrevMap["Team 42"] = "T42"
	data.abbrevMap = abbrevMap

def getTeamStats(data, team): # get relevant team statistics (GF/G, GA/G)
	abbrev = data.abbrevMap[team]
	url = "http://www.hockey-reference.com/teams/%s/2017.html" % abbrev
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	gamesPlayed = int(soup.find("td", {"data-stat":"games"}).text)
	goalsFor = int(soup.find("td", {"data-stat":"goals"}).text)
	goalsAgainst = int(soup.find("td", {"data-stat":"opp_goals"}).text)
	data.totalLeagueGPG = float(soup.find_all("td", {"data-stat":"total_goals_per_game"})[-1].text)

	GFPG = goalsFor/gamesPlayed
	GAPG = goalsAgainst/gamesPlayed

	return GFPG, GAPG

def getPlayerStats(data, team): # get individual player statistics (G, A)
	stats = []
	players = []
	goals = []
	assists = []

	abbrev = data.abbrevMap[team]
	url = "http://www.hockey-reference.com/teams/%s/2017.html" % abbrev
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	stats = soup.find("div", {"id":"all_skaters"})
	games = [int(games.text) for games in stats.find_all("td", {"data-stat":"games_played"})][:-1]
	players = [player.text.title() for player in stats.find_all("td", {"data-stat":"player"})][:-1]
	goals += [int(goal.text) for goal in stats.find_all("td", {"data-stat":"goals"})]
	assists += [int(assist.text) for assist in stats.find_all("td", {"data-stat":"assists"})]
	
	statsDict = dict()
	for i in range (len(players)):
		statsDict[players[i]] = (goals[i]/goals[-1], assists[i]/assists[-1], goals[i], assists[i], games[i])

	return statsDict

def getGames(data): # get NHL games from that day
	date = str(data.date).split("-")
	year, month, day = date
	url = "http://www.hockey-reference.com/boxscores/?year=%s&month=%s&day=%s" % (year, month, day)
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	generalData = soup.find_all("div", {"class":"game_summary"})
	games = []
	urls = []

	for info in generalData:
		games += [[info.find_all("a")[0].text.replace(".", ""), info.find_all("a")[2].text.replace(".", "")]]

	for game in games:
		home = "-".join(game[0].lower().split())
		away = "-".join(game[1].lower().split())
		date = "".join(date)
		urls += ["http://www.tsn.ca/nhl/game/%s-%s-%s/" % (home, away, date)]

	data.games = games
	data.urls = urls

##### SIMULATION #####

def predictOutcome(data): # decides the score of the game
	homeScore, awayScore = 0, 0
	data.homeScoringChance = (data.homeGFPG + data.awayGAPG)/(data.totalLeagueGPG/2)
	data.awayScoringChance = (data.awayGFPG + data.homeGAPG)/(data.totalLeagueGPG/2)
	data.homeScoreTimes = []
	data.awayScoreTimes = []
	data.homeGoalScorers = []
	data.awayGoalScorers = []
	data.allGoalInfo = []
	data.goalsByPeriod = dict()

	for period in range (1, 4):
		data.goalsByPeriod[period] = [0,0]
		for time in range (1200, -1, -1):
			if data.homeScoringChance > random.random()*3600:
				homeScore += 1
				data.homeScoreTimes += [(period, time)]
				data.homeGoalScorers += [getGoalScorers(data.homeStats)]
				data.goalsByPeriod[period][0] += 1
			elif data.awayScoringChance > random.random()*3600:
				awayScore += 1
				data.awayScoreTimes += [(period, time)]
				data.awayGoalScorers += [getGoalScorers(data.awayStats)]
				data.goalsByPeriod[period][1] += 1
	period = 4
	while homeScore == awayScore: # overtime! goal scored in overtime means over
		data.goalsByPeriod[period] = [0,0]
		for time in range (1200, -1, -1):
			if data.homeScoringChance > random.random()*3600:
				homeScore += 1
				data.homeScoreTimes += [(period, time)]
				data.homeGoalScorers += [getGoalScorers(data.homeStats)]
				data.goalsByPeriod[period][0] += 1
				break
			elif data.awayScoringChance > random.random()*3600:
				awayScore += 1
				data.awayScoreTimes += [(period, time)]
				data.awayGoalScorers += [getGoalScorers(data.awayStats)]
				data.goalsByPeriod[period][1] += 1
				break
	data.finalScore = (homeScore, awayScore)

def getGoalScorers(statsDict): # determines players who get goals and assists
	goalScorers, assistScorers = [], []
	for player in statsDict:
		stats = statsDict[player]
		goalProb = stats[0]*2
		assistProb = stats[1]*4
		currPlayer = player

		num = random.random()
		if num < goalProb:
			goalScorers += [player]
		elif num < assistProb:
			assistScorers += [player]

	if len(goalScorers) == 0:
		goalPlayer = currPlayer
	else:
		goalPlayer = goalScorers[0]

	if len(assistScorers) == 0:
		assistPlayer = "Unassisted"
	else:
		assistPlayer = assistScorers[:2]

	return goalPlayer, assistPlayer

def interpretFantasyStats(data): # determine team strength of a fantasy team
	goals, assists, games = 0, 0, 0
	for player in data.fantasyTeam:
		data.homeStats[player] = []
		goals += data.fantasyStats[player][2]
		assists += data.fantasyStats[player][3]
		games += data.fantasyStats[player][4]
	
	data.homeGFPG = goals/games
	data.homeGAPG = data.totalLeagueGPG/2
	
	for player in data.fantasyTeam:
		goal = data.fantasyStats[player][2]
		assist = data.fantasyStats[player][3]
		data.homeStats[player] += [goal/goals, assist/assists]

##### MOUSE EVENTS #####

def splashMousePressed(event, data):
	newMode = inBoxBounds(data, event.x, event.y)
	if newMode != None:
		if newMode == "NHL TODAY":
			data.mode = newMode
		elif newMode == "FANTASY":
			data.FantasyOrSimulate = "fantasy"
			initFantasy(data)
			data.mode = "lines"
		elif newMode == "SIMULATE":
			data.FantasyOrSimulate = "simulate"
			data.mode = "teams"
		elif newMode == "HELP":
			data.mode = "ABOUT"

def simulateMousePressed(event, data):
	if (data.teamsMarginX <= event.x <= data.width - data.teamsMarginX and
		data.teamsMarginY <= event.y <= data.height - data.teamsMarginY):

		(row, col) = getTeamsCell(data, event.x, event.y)
		currTeam = data.teamsSorted[row*data.teamsCols + col]
		if currTeam not in data.teams and len(data.teams) < 2:
			data.teams += [currTeam]
			data.selectedTeamsRowCol += [(row, col)]
		elif currTeam in data.teams:
			data.teams.remove(currTeam)
			data.selectedTeamsRowCol.remove((row, col))
		if len(data.teams) == 0:
			data.teamSelectMessage = "SELECT THE HOME TEAM"
		elif len(data.teams) == 1:
			data.teamSelectMessage = "SELECT THE AWAY TEAM"
	if (len(data.teams) == 2 and data.width/4 <= event.x <= data.width*3/4 and
		data.height/20 <= event.y <= data.height*3/20):
		initPlayers(data)
		data.mode = "loading"

def fantasyMousePressed(event, data):
	if (data.teamsMarginX <= event.x <= data.width - data.teamsMarginX and data.teamsMarginY <= event.y <= data.height - data.teamsMarginY):
			(row, col) = getTeamsCell(data, event.x, event.y)
			if data.fantasySelectDone:
				data.fantasyOpponent = data.teamsSorted[row*data.teamsCols + col]
				data.awayForwardLines, data.awayDefenseLines, data.awayForwards, data.awayGoalies = getPlayers(data, data.fantasyOpponent)
				data.mode = "loading"
			else:
				data.fantasySelectTeam = data.teamsSorted[row*data.teamsCols + col]
				data.homePlayers = []
				if data.fantasySelectTeam not in data.allPlayers:
					data.homeForwardLines, data.homeDefenseLines, data.homeForwards, data.homeGoalies = getPlayers(data, data.fantasySelectTeam)
					fantasyStatsDict = getPlayerStats(data, data.fantasySelectTeam)
					for player in fantasyStatsDict:
						data.homePlayers += [player]
					data.homePlayers.sort()
					for goalie in data.homeGoalies:
						if goalie in data.homePlayers:
							data.homePlayers.remove(goalie)
					data.allPlayers[data.fantasySelectTeam], data.allGoalies[data.fantasySelectTeam] = data.homePlayers, data.homeGoalies
					data.allStats.update(fantasyStatsDict)
				else:
					data.homePlayers, data.homeGoalies = data.allPlayers[data.fantasySelectTeam], data.allGoalies[data.fantasySelectTeam]
				if data.fantasyLine == "goalie":
					data.homePlayers = data.homeGoalies
				initRosterScreen(data)
				data.mode = "roster"

def linesMousePressed(event, data):
	data.currPlayer = ""
	x, y = event.x, event.y	
	lineCell = getForwardLinesCell(data, x, y)
	if lineCell != None:
		data.fantasyCurrRowCol = lineCell
		data.fantasyLine = "forward"
		data.mode = "teams"
	
	lineCell = getDefenseLinesCell(data, x, y)
	if lineCell != None:
		data.fantasyCurrRowCol = lineCell
		data.fantasyLine = "defense"
		data.mode = "teams"
	
	lineCell = getGoalieLinesCell(data, x, y)
	if lineCell != None:
		data.fantasyCurrRowCol = lineCell
		data.fantasyLine = "goalie"
		data.mode = "teams"

	if (len(data.fantasyTeam) == 20 and data.width/5 <= event.x <= data.width*4/5 and
			0 <= event.y <= data.height/10):
			data.fantasySelectDone = True
			data.mode = "teams"

def rosterMousePressed(event, data):
	if (data.teamsMarginX <= event.x <= data.width - data.teamsMarginX and
			data.teamsMarginY <= event.y <= data.height - data.teamsMarginY):

			(row, col) = getRostersCell(data, event.x, event.y)
			data.currPlayer = data.homePlayers[row*data.teamsCols + col].title()
			currPlayer = data.currPlayer

			if currPlayer not in data.fantasyTeam:
				if not ((data.fantasyLine == "goalie" and data.currPlayer not in data.homeGoalies) 
					or (data.fantasyLine != "goalie" and data.currPlayer in data.homeGoalies)):
					if data.fantasyLine == "forward":
						if data.fantasyCurrRowCol in data.forwardTeamCells:
							removedPlayer = data.forwardTeamCells[data.fantasyCurrRowCol]
							data.fantasyTeam.remove(removedPlayer)
							del data.fantasyStats[removedPlayer]
						data.forwardTeamCells[data.fantasyCurrRowCol] = currPlayer
						data.fantasyTeam += [currPlayer]
						data.fantasyStats[currPlayer] = data.allStats[currPlayer]

					elif data.fantasyLine == "defense":
						if data.fantasyCurrRowCol in data.defenseTeamCells:
							removedPlayer = data.defenseTeamCells[data.fantasyCurrRowCol]
							data.fantasyTeam.remove(removedPlayer)
							del data.fantasyStats[removedPlayer]
						data.defenseTeamCells[data.fantasyCurrRowCol] = currPlayer
						data.fantasyTeam += [currPlayer]
						data.fantasyStats[currPlayer] = data.allStats[currPlayer]

					elif data.fantasyLine == "goalie":
						if data.fantasyCurrRowCol in data.goalieTeamCells:
							removedPlayer = data.goalieTeamCells[data.fantasyCurrRowCol]
							data.fantasyTeam.remove(removedPlayer)
							del data.fantasyStats[removedPlayer]
						data.goalieTeamCells[data.fantasyCurrRowCol] = currPlayer
						data.fantasyTeam += [currPlayer]
						data.fantasyStats[currPlayer] = data.allStats[currPlayer]
					data.mode = "lines"

def NHLTodayMousePressed(event, data):
	if (data.gamesMarginX <= event.x <= data.width - data.gamesMarginX and
			data.gamesMarginY <= event.y <= data.height - data.gamesMarginY):
			(row, col, mode) = getGamesCell(data, event.x, event.y)
			if mode == "simulate":
				data.teams = data.games[row]
				initPlayers(data)
				data.mode = "loading"
			elif mode == "link":
				url = data.urls[row]
				webbrowser.open(url)

def summaryMousePressed(event, data):
	if data.height/3 < event.y < data.height*9/10:
		if data.width*3/20 < event.x < data.width/3:
			data.mode = "boxscore"
		elif data.width*3/5 < event.x < data.width*9/10:
			data.mode = "scoring"

def mousePressed(event, data):
	if data.mode == "splash":
		splashMousePressed(event, data)
	else:
		returnToScreen(event, data)
		
		if data.mode == "teams":
			if data.FantasyOrSimulate == "simulate":
				simulateMousePressed(event, data)
			elif data.FantasyOrSimulate == "fantasy":
				fantasyMousePressed(event, data)

		elif data.mode == "lines":
			linesMousePressed(event, data)

		elif data.mode == "roster":
			rosterMousePressed(event, data)

		elif data.mode == "NHL TODAY":
			NHLTodayMousePressed(event, data)

		elif data.mode == "summary":
			summaryMousePressed(event, data)

def returnToScreen(event, data):
	x, y = event.x, event.y
	if 0 <= x <= data.width/15 and 0 <= y <= data.height/15:
		if data.mode == "boxscore" or data.mode == "scoring":
			data.mode = "summary"
		elif data.mode == "roster":
			data.mode = "lines"
		else:
			if not (data.mode == "ABOUT" or data.mode == "NHL TODAY"):
				init(data)
			data.mode = "splash"

##### KEY EVENTS #####

def keyPressed(event, data):
	if data.mode == "game":
		if data.gameOver:
			if event.keysym == "space":
				data.mode = "summary"
		else:
			if event.keysym == "space":
				if data.gameStart:
					data.gameStart = False
				elif data.goalScored:
					data.goalScored = False
				elif data.intermission:
					data.intermission = False
				data.playStopped = not data.playStopped
			elif event.keysym == "Down" and data.clockSpeed > 1:
				data.clockSpeed //= 2
			elif event.keysym == "Up":
				data.clockSpeed *= 2

	elif data.mode == "players":
		if event.keysym == "space":
			data.mode = "game"

##### TIMER FIRED #####

def loadingTimerFired(data):
	if data.loadCount == 5:
		initGame(data)
		if data.FantasyOrSimulate == "simulate":
			data.homeGFPG, data.homeGAPG = getTeamStats(data, data.teams[0])
			data.awayGFPG, data.awayGAPG = getTeamStats(data, data.teams[1])
			data.homeStats = getPlayerStats(data, data.teams[0])
			data.awayStats = getPlayerStats(data, data.teams[1])
		elif data.FantasyOrSimulate == "fantasy":
			data.teams = ["Team 42", data.fantasyOpponent]
			data.awayGFPG, data.awayGAPG = getTeamStats(data, data.fantasyOpponent)
			interpretFantasyStats(data)
			data.awayStats = getPlayerStats(data, data.fantasyOpponent)
		predictOutcome(data)
		data.mode = "players"
	data.loadCount += 1

def gameTimerFired(data):
	# game backend timerfired
	if data.clock == 0:
		initPlayerLocations(data)
		data.playStopped = True
		data.intermission = True
		if data.period < 3 or data.homeScore == data.awayScore:
			data.clock = 20*60
			data.period += 1
			if data.homeScore == data.awayScore:
				data.period == 4
		else:
			data.gameOver = True

	elif not data.playStopped:
		newTime = data.clock - data.clockSpeed
		data.clock = newTime if newTime >= 0 else 0

		for homeGoal in data.homeScoreTimes:
			if data.period == homeGoal[0] and newTime < homeGoal[1]:
				data.playStopped = True
				data.goalScored = True
				data.homeScore += 1
				data.clock = homeGoal[1]

				data.homeScoreTimes.remove(homeGoal)
				data.goalInfo = (data.teams[0], homeGoal, data.homeGoalScorers.pop(0))
				data.allGoalInfo += [data.goalInfo]
				
		for awayGoal in data.awayScoreTimes:
			if data.period == awayGoal[0] and newTime < awayGoal[1]:
				data.playStopped = True
				data.goalScored = True
				data.awayScored = True
				data.awayScore += 1
				data.clock = awayGoal[1]

				data.awayScoreTimes.remove(awayGoal)
				data.goalInfo = (data.teams[1], awayGoal, data.awayGoalScorers.pop(0))
				data.allGoalInfo += [data.goalInfo]

		if data.period > 3 and data.goalScored:
			data.gameOver = True
				
	# visualization timerfired

	visualizeSimulation(data)
	if data.goalScored:
		initPlayerLocations(data)

def timerFired(data):
	if data.mode == "loading":
		loadingTimerFired(data)
	
	elif data.mode == "game":
		gameTimerFired(data)

	elif data.mode == "intro":
		if data.loadCount == 1:
			initNHLToday(data)
			init(data)
		data.loadCount += 1

##### VISUALIZATION #####

def splashRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width = 0) # background
	canvas.create_text(data.splashcx, data.height*4/5, text="NHL 112", font = "Arial 120 bold", fill = "white")
	for mode in data.modes:
		drawBoxes(canvas, data, mode[0], data.boxSpacing, text=mode[1])
	canvas.create_image(data.width*3/4, data.height/3, image = data.splashImage) # crosby

def gameRedrawAll(canvas, data):
	canvas.create_image(data.width/2, data.height/2, image = data.rinkImage)
	drawRink(canvas, data)
	drawPlayers(canvas, data)
	drawPuck(canvas, data)
	drawScoreBoard(canvas, data)
	displayGoalScorer(canvas, data)
	if not data.gameOver:
		if data.gameStart:
			canvas.create_rectangle(0, data.height/5, data.width, data.height*4/5, fill = "black")
			canvas.create_text(data.width/2, data.height/4, text = "Press Space to Start!", font = "Arial 48", fill = "white")
			canvas.create_text(data.width/2, data.height/2, text = "Press Up to Speed Up Simulation", font = "Arial 48", fill = "white")
			canvas.create_text(data.width/2, data.height*3/4, text = "Press Down to Slow Down Simulation", font = "Arial 48", fill = "white")
		elif data.goalScored:
			canvas.create_rectangle(0, data.height/5, data.width, data.height*4/5, fill = "black")
			canvas.create_image(data.width/5, data.height/2, image = data.goalImages[1])
			canvas.create_image(data.width*17/20, data.height*9/20, image = data.goalImages[0])
			canvas.create_text(data.width/2, data.height/2, text = "GOAL!", font = "Arial 144 bold", fill = "white")
			canvas.create_text(data.width/2, data.height*4/5, text = "Press Space to Continue", font = "Arial 24", fill = "white", anchor = "s")
		elif data.intermission:
			canvas.create_rectangle(0, data.height/5, data.width, data.height*4/5, fill = "black")
			canvas.create_image(data.width/10, data.height/2, image = data.intermissionImages[0])
			canvas.create_image(data.width*4/5, data.height/2, image = data.intermissionImages[1])
			canvas.create_text(data.width/2, data.height/2, text = "INTERMISSION!", font = "Arial 100 bold", fill = "white")
			canvas.create_text(data.width/2, data.height*4/5, text = "Press Space to Continue", font = "Arial 24", fill = "white", anchor = "s")
		elif data.playStopped:
			canvas.create_rectangle(0, data.height/5, data.width, data.height*4/5, fill = "black")
			canvas.create_text(data.width/2, data.height/2, text = "PAUSED!", font = "Arial 150 bold", fill = "white")
			canvas.create_text(data.width/2, data.height*4/5, text = "Press Space to Continue", font = "Arial 24", fill = "white", anchor = "s")
	else:
		canvas.create_rectangle(0, data.height/5, data.width, data.height*4/5, fill = "black")
		canvas.create_text(data.width/2, data.height/2, text = "GAME OVER!", font = "Arial 100", fill = "white")
		canvas.create_text(data.width/2, data.height*4/5, text = "Press Space to Continue", font = "Arial 24", fill = "white", anchor = "s")

def teamsRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width = 0) # background

	teamInd = 0
	(rows, cols) = data.teamsRows, data.teamsCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = getTeamsCellBounds(data, row, col)
			colors = ("black", "white") if (row, col) not in data.selectedTeamsRowCol else ("white", "black")
			canvas.create_rectangle(left, top, right, bottom, fill = colors[0], outline = colors[1], width = 1)
			cx, cy = (left + right)/2, (top+bottom)/2
			canvas.create_text(cx, cy, text=data.teamsSorted[teamInd], fill = colors[1], font = "Arial 12")
			teamInd += 1

	if data.FantasyOrSimulate == "simulate":
		canvas.create_text(data.width/2, data.height/10, text = data.teamSelectMessage,
					fill = "white", font = "Arial 24 ", anchor = "s")
		if len(data.teams) < 2:
			canvas.create_text(data.width/2, data.height/10, text = "Click team again to deselect",
					fill = "white", font = "Arial 24", anchor = "n")
		else:
			canvas.create_rectangle(data.width/4, data.height/20, data.width*3/4, data.height*3/20,
									fill = "white", width = 0)
			canvas.create_text(data.width/2, data.height/10, text = "NEXT", fill = "black", font = "Arial 48")
		# Draws Home Team: ___ Away Team: ____
		canvas.create_text(data.width/4, data.height-data.teamsMarginY/2,
				text = "HOME TEAM:", fill = "white", font = "Arial 24", anchor = "s")

		canvas.create_text(data.width*3/4, data.height-data.teamsMarginY/2,
				text = "AWAY TEAM:", fill = "white", font = "Arial 24", anchor = "s")
		try:
			canvas.create_text(data.width/4, data.height-data.teamsMarginY/2,
				text = data.teams[0], fill = "white", font = "Arial 24", anchor = "n")
			canvas.create_text(data.width*3/4, data.height-data.teamsMarginY/2,
				text = data.teams[1], fill = "white", font = "Arial 24", anchor = "n")
		except:
			pass

	elif data.fantasySelectDone:
		canvas.create_text(data.width/2, data.height/10, text = "Select your opponent!",
					fill = "white", font = "Arial 48")

	else:
		canvas.create_text(data.width/2, data.height/10, text = "Select a team!",
					fill = "white", font = "Arial 48")

def loadingRedrawAll(canvas, data):
	canvas.create_image(data.width/2, data.height/2, image=data.loadImage)
	canvas.create_text(data.width/2, data.height*3/5, text="Loading Simulation...", font = "Arial 48 bold", fill = "black", anchor = "n")

def playersRedrawAll(canvas, data):
	canvas.create_image(data.width/2, data.height/2, image=data.playersImage)
	canvas.create_text(data.width/2, data.height/10, text = "Press Space to Continue", font = "Arial 36 bold", fill = "black", anchor = "s")
	initialHeight = data.height/4
	spacing = data.height/15

	color = "black"
	font = "Arial 16"
	
	i = .5
	if data.FantasyOrSimulate == "simulate":
		canvas.create_text(data.width/4, data.height/5, text=data.teams[0], font = "Arial 24 bold", fill = color, anchor = "s")
		canvas.create_text(data.width*3/4, data.height/5, text=data.teams[1], font = "Arial 24 bold", fill = color, anchor = "s")
		for line in data.forwardLines:
			canvas.create_text(data.width/4, initialHeight + spacing*i,
					text = " - ".join(data.homeForwardLines[line]).title(), fill = color, font = font)
			i += 1
		i += .5
		for line in data.defenseLines:
			canvas.create_text(data.width/4, initialHeight + spacing*i,
					text = " - ".join(data.homeDefenseLines[line]).title(), fill = color, font = font)
			i += 1
		i += .5
		for goalie in data.homeGoalies:
			canvas.create_text(data.width/4, initialHeight + spacing*i,
				text = goalie, fill = color, font = font)
			i += 1
	else:
		canvas.create_text(data.width/4, data.height/5, text="Team 42", font = "Arial 24 bold", fill = color, anchor = "s")
		canvas.create_text(data.width*3/4, data.height/5, text=data.fantasyOpponent, font = "Arial 24 bold", fill = color, anchor = "s")
		



		data.homeForwardLines = dict()
		data.homeDefenseLines = dict()
		for row in range (data.forwardRows):
			data.homeForwardLines[row] = []
		for row in range (data.defenseRows):
			data.homeDefenseLines[row] = []
		for row in range (data.forwardRows):
			for col in range (data.forwardCols):
				data.homeForwardLines[row] += [data.forwardTeamCells[(row, col)].title()]
		for row in range (data.defenseRows):
			for col in range (data.defenseCols):
				data.homeDefenseLines[row] += [data.defenseTeamCells[(row, col)].title()]
		data.homeGoalies = [data.goalieTeamCells[(0, 0)].title(), data.goalieTeamCells[(1, 0)].title()]




		for row in range (data.forwardRows):
			canvas.create_text(data.width/4, initialHeight + spacing*i,
					text = " - ".join(data.homeForwardLines[row]), fill = color, font = font)
			i += 1
		i += .5
		for row in range (data.defenseRows):
			canvas.create_text(data.width/4, initialHeight + spacing*i,
					text = " - ".join(data.homeDefenseLines[row]), fill = color, font = font)
			i += 1
		i += .5
		for goalie in data.homeGoalies:
			canvas.create_text(data.width/4, initialHeight + spacing*i,
				text = goalie, fill = color, font = font)
			i += 1
	
	i = .5
	for line in data.forwardLines:
		canvas.create_text(data.width*3/4, initialHeight + spacing*i,
				text = " - ".join(data.awayForwardLines[line]).title(), fill = color, font = font)
		i += 1
	i += .5
	for line in data.defenseLines:
		canvas.create_text(data.width*3/4, initialHeight + spacing*i,
				text = " - ".join(data.awayDefenseLines[line]).title(), fill = color, font = font)
		i += 1
	i += .5
	for goalie in data.awayGoalies:
		canvas.create_text(data.width*3/4, initialHeight + spacing*i,
			text = goalie, fill = color, font = font)
		i += 1

def summaryRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill = "light blue", width = 0)
	winner = data.teams[0] if data.homeScore > data.awayScore else data.teams[1]
	canvas.create_text(data.width/2, data.height/10, text = "Winner: %s" % winner, font = "Arial 72")
	canvas.create_image(data.width/4, data.height/2, image = data.summaryImages[0])
	canvas.create_image(data.width*3/4, data.height/2, image = data.summaryImages[1])
	canvas.create_text(data.width/4, data.height*3/4, text = "Boxscore", font = "Arial 48 underline", anchor = "n")
	canvas.create_text(data.width*3/4, data.height*3/4, text = "Scoring", font = "Arial 48 underline", anchor = "n")

def boxscoreRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill = "light blue", width = 0)
	canvas.create_text(data.width/2, data.height/10, text = "Boxscore:", font = "Arial 96")
	for row in range (data.boxscoreRows):
		for col in range (data.period+2):
			left, top, right, bottom = getBoxscoreCellBounds(data, row, col)
			canvas.create_rectangle(left, top, right, bottom, outline = "black", width = 1)
			if row == 0:
				messages = ["", "FIRST", "SECOND", "THIRD"]
				messages += ["OT"]*(data.period-3)
				messages += ["FINAL"]
				msg = messages[col]
			elif col == 0:
				msg = data.abbrevMap[data.teams[0]] if row == 2 else data.abbrevMap[data.teams[1]]
			elif 0 < col <= data.period:
				msg = data.goalsByPeriod[col][0] if row == 2 else data.goalsByPeriod[col][1]
			else:
				msg = data.finalScore[0] if row == 2 else data.finalScore[1]
			cx, cy = (left + right)/2, (top+bottom)/2
			canvas.create_text(cx, cy, text = msg, font = "Arial 24")

def scoringRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill = "light blue", width = 0)
	canvas.create_text(data.width/2, data.height/10, text = "Scoring Summary:", font = "Arial 96")
	textHeight = data.height/10
	textSpacing = min(data.height/10, (data.width-2*textHeight)/(data.homeScore + data.awayScore))
	i = 1
	for currPeriod in range(1, data.period+1):
		periodMsg = str(currPeriod) if currPeriod <= 3 else "OT"
		canvas.create_text(data.width/20, textHeight+i*textSpacing, text = periodMsg, font = "Arial 24 bold", anchor = "w")
		i += 1
		for goal in data.allGoalInfo:
			if currPeriod == goal[1][0]: # if current period matches the period of the goal
				team = data.abbrevMap[goal[0]]
				time = goal[1]
				info = goal[2]

				suffix = ["", "st", "nd", "rd"]
				period = time[0]
				period = str(period) + suffix[period%4]

				clock = time[1]
				mins = str(clock//60)
				secs = clock%60
				secs = str(secs) if secs >= 10 else "0" + str(secs)

				goalScorer = info[0]
				assistScorer = info[1]

				if isinstance(assistScorer, str):
					assistsMessage = "UNASSISTED"
				else:
					if len(assistScorer) == 1:
						assistsMessage = "ASSISTS: %s" % assistScorer[0]
					else:
						assistsMessage = "ASSISTS: %s, %s" % (assistScorer[0], assistScorer[1])

				goalMessage = "%s:%s %s - %s GOAL: %s %s " % (mins, secs, period, team, goalScorer, assistsMessage)
				canvas.create_text(data.width/20, textHeight+i*textSpacing, text = goalMessage, font = "Arial 16", anchor = "w")
				i += 1

def NHLTodayRedrawAll(canvas, data):
	#canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width = 0)
	canvas.create_image(data.width/2, data.height/2, image = data.nhlTodayImage)
	canvas.create_text(data.width/2, data.height/10, text = data.date.strftime("%A, %B %d, %Y"), fill = "black", font = "Arial 36", anchor = "s")
	team = ""
	for row in range (data.gamesRows):
		for col in range (data.gamesCols):
			left, top, right, bottom = getGamesCellBounds(data, row, col)
			canvas.create_rectangle(left, top, right, bottom, width = 0)
			cx, cy = (left + right)/2, (top + bottom)/2
			if col == 0:
				team = data.games[row][0]
			elif col == 2:
				team = data.games[row][1]
			if col == 1:
				canvas.create_text(cx, cy, text = "SIMULATE", fill = "blue", font = "Arial 12 underline", anchor = "s")
				canvas.create_text(cx, cy, text = "LINK", fill = "blue", font = "Arial 12 underline", anchor = "n")
			else:
				if col == 0:
					canvas.create_text(right, cy, text = team, fill = "black", font = "Arial 20 bold", anchor = "e")
				elif col == 2:
					canvas.create_text(left, cy, text = team, fill = "black", font = "Arial 20 bold", anchor = "w")

def aboutRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width = 0)
	canvas.create_text(data.width/20, data.height/7, text = "NHL TODAY", font = "Arial 36 underline", fill = "white", anchor = "w")
	msg = ["View all games going on in the NHL today!","Then simulate the result of that game, or be redirected to a preview article"]
	canvas.create_text(data.width/20, data.height*2/7, text = msg[0], font = "Arial 24", fill = "white", anchor = "sw")
	canvas.create_text(data.width/20, data.height*2/7, text = msg[1], font = "Arial 24", fill = "white", anchor = "nw")
	canvas.create_text(data.width/20, data.height*3/7, text = "FANTASY", font = "Arial 36 underline", fill = "white", anchor = "w")
	msg = ["Build your own fantasy team with any players you want from the NHL", "Then simulate a game between your fantasy team and a chosen NHL team"]
	canvas.create_text(data.width/20, data.height*4/7, text = msg[0], font = "Arial 24", fill = "white", anchor = "sw")
	canvas.create_text(data.width/20, data.height*4/7, text = msg[1], font = "Arial 24", fill = "white", anchor = "nw")
	canvas.create_text(data.width/20, data.height*5/7, text = "SIMULATE", font = "Arial 36 underline", fill = "white", anchor = "w")
	msg = "Choose any two NHL teams, then simulate the result of that game!"
	canvas.create_text(data.width/20, data.height*6/7, text = msg, font = "Arial 24", fill = "white", anchor = "w")

def redrawAll(canvas, data):
	if data.mode == "splash":
		splashRedrawAll(canvas, data)

	elif data.mode == "game":
		gameRedrawAll(canvas, data)

	elif data.mode == "teams":
		teamsRedrawAll(canvas, data)

	elif data.mode == "loading":
		loadingRedrawAll(canvas, data)

	elif data.mode == "summary":
		summaryRedrawAll(canvas, data)

	elif data.mode == "boxscore":
		boxscoreRedrawAll(canvas, data)

	elif data.mode == "scoring":
		scoringRedrawAll(canvas, data)

	elif data.mode == "NHL TODAY":
		NHLTodayRedrawAll(canvas, data)

	elif data.mode == "lines":
		canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width = 0)
		canvas.create_text(data.width/2, data.height/10, fill = "white",
				text = "Fill in your Dream Team! Select a position to fill!", font = "Arial 24", anchor = "s")
		displayLines(canvas, data)

	elif data.mode == "roster":
		canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width = 0)
		canvas.create_text(data.width/2, data.height/10, fill = "white",
				text = "Select a player from the %s" % data.fantasySelectTeam, font = "Arial 24", anchor = "s")
		displayRosters(canvas, data)
		if data.currPlayer in data.fantasyTeam:
			canvas.create_rectangle(data.width/4, 0, data.width*3/4, data.height/10, fill = "white", width = 0)
			canvas.create_text(data.width/2, data.height/10,
				text = "ERROR: Player already in your team", font = "Arial 24", anchor = "s")

	elif data.mode == "ABOUT":
		aboutRedrawAll(canvas, data)

	elif data.mode == "players":
		playersRedrawAll(canvas, data)

	if data.mode != "intro":
		drawBackButton(canvas, data)
	else:
		canvas.create_image(data.width/2, data.height/2, image=data.introImage)
		canvas.create_text(data.width*7/10, data.height*2/5, text = "WELCOME", font = "Arial 72 bold")
		canvas.create_text(data.width*7/10, data.height*3/5, text = "TO NHL 112", font = "Arial 72 bold")
		canvas.create_text(data.width*7/10, data.height*4/5, text = "Brought to you by", font = "Arial 36", anchor = "s")
		canvas.create_text(data.width*7/10, data.height*4/5, text = "Kai Lung", font = "Arial 36", anchor = "n")

def visualizeSimulation(data): # the visualization for the simulation
	if not data.playStopped:
		i = 0
		for player in data.homeTeam + data.awayTeam:
			if i < 6:
				if isinstance(player, Forward):
					if not data.rinkCX-data.zoneWidth+player.r < player.cx < data.rinkCX+data.zoneWidth-player.r:
						player.vx *= -1
					if not data.rinkY0+data.rinkHeight*i/3+player.r < player.cy < data.rinkY0+data.rinkHeight*(i+1)/3-player.r:
						player.vy *= -1
				elif isinstance(player, Defense):
					if not data.rinkX0+player.r < player.cx < data.rinkCX-player.r:
						player.vx *= -1
					if not data.rinkY0+data.rinkHeight*(i-3)/2+player.r < player.cy < data.rinkY0+data.rinkHeight*(i+1-3)/2-player.r:
						player.vy *= -1
				else: # goalie
					if not data.rinkX0+player.r < player.cx < data.rinkX0+data.netDepth:
						player.vx *= -1
				player.move()
			else:
				j = i%6
				if isinstance(player, Forward):
					if not data.rinkCX-data.zoneWidth+player.r < player.cx < data.rinkCX+data.zoneWidth-player.r:
						player.vx *= -1
					if not data.rinkY0+data.rinkHeight*j/3+player.r < player.cy < data.rinkY0+data.rinkHeight*(j+1)/3-player.r:
						player.vy *= -1
				elif isinstance(player, Defense):
					if not data.rinkCX+player.r < player.cx < data.rinkX1-player.r:
						player.vx *= -1
					if not data.rinkY0+data.rinkHeight*(j-3)/2+player.r < player.cy < data.rinkY0+data.rinkHeight*(j+1-3)/2-player.r:
						player.vy *= -1
				else: # goalie
					if not data.rinkX1-data.netDepth < player.cx < data.rinkX1-player.r:
						player.vx *= -1
				player.move()
			if intersect(player, data.puck):
				if player in data.homeTeam:
					data.puck.vx = abs(data.puck.vx)
				else:
					data.puck.vx = -abs(data.puck.vx)
				data.puck.vy *= -1
			i += 1

		if not data.rinkY0+player.r < data.puck.cy < data.rinkY1-player.r:
			data.puck.vy *= -1
		if not data.leftEndX+player.r < data.puck.cx < data.rightEndX-player.r:
			data.puck.vx *= -1
		data.puck.move()

def intersect(obj1, obj2): # determine if two circular objects intersect
	r1, r2 = obj1.r, obj2.r
	cx1, cx2 = obj1.cx, obj2.cx
	cy1, cy2 = obj1.cy, obj2.cy
	distance = ((cx1-cx2)**2 + (cy1-cy2)**2)**0.5
	return r1+r2 >= distance

def drawBackButton(canvas, data):
	if data.mode != "splash":
		if data.mode == "game" or data.mode == "summary" or data.mode == "boxscore" or data.mode == "scoring":
			color = ("black", "white")
		else:
			color = ("white", "black")
		canvas.create_rectangle(0, 0, data.width/15, data.height/15, fill = color[0], width = 1)
		cx, cy = data.width/30, data.height/30
		canvas.create_text(cx, cy, text = "BACK", font = "Arial 16", fill = color[1])

def getGamesCellBounds(data, row, col): # for team selection
	gridWidth = data.width - 2*data.gamesMarginX
	gridHeight = data.height - 2*data.gamesMarginY
	colWidth = gridWidth / data.gamesCols
	rowHeight = gridHeight / data.gamesRows
	left = data.gamesMarginX + col*colWidth
	top = data.gamesMarginY + row*rowHeight
	right = left + colWidth
	bottom = top + rowHeight
	return left, top, right, bottom

def getGamesCell(data, x, y): # for team selection
	(rows, cols) = data.gamesRows, data.gamesCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = getGamesCellBounds(data, row, col)
			if left <= x <= right and top <= y <= bottom:
				if col != 1:
					return (row, col, "")
				else:
					cy = (top + bottom)/2
					if top <= y <= cy:
						return (row, col, "simulate")
					else:
						return (row, col, "link")

def displayRosters(canvas, data):
	i = 0
	for row in range (data.rosterRows):
		for col in range (data.rosterCols):
			left, top, right, bottom = getRostersCellBounds(data, row, col)
			canvas.create_rectangle(left, top, right, bottom, outline = "white", width = 1)
			if i < data.numPlayers:
				cx, cy = (left+right)/2, (top+bottom)/2
				canvas.create_text(cx, cy, text = data.homePlayers[i], fill = "white", font = "Arial 12")
			i += 1

def getRostersCellBounds(data, row, col): # for team selection
	gridWidth = data.width - 2*data.teamsMarginX
	gridHeight = data.height - 2*data.teamsMarginY
	colWidth = gridWidth / data.rosterCols
	rowHeight = gridHeight / data.rosterRows
	left = data.teamsMarginX + col*colWidth
	top = data.teamsMarginY + row*rowHeight
	right = left + colWidth
	bottom = top + rowHeight
	return left, top, right, bottom

def getRostersCell(data, x, y): # for team selection
	(rows, cols) = data.rosterRows, data.rosterCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = getRostersCellBounds(data, row, col)
			if left <= x <= right and top <= y <= bottom:
				return (row, col)

def forwardLinesCellBounds(data, row, col): # building fantasy player screen
	marginX = data.width/5
	gridWidth = data.width - 2*marginX
	colWidth = gridWidth/data.forwardCols
	rowHeight = data.height/15
	left, top = marginX + col*colWidth, (row+3)*rowHeight
	right, bottom = left + colWidth, top + rowHeight
	return left, top, right, bottom	

def defenseLinesCellBounds(data, row, col): # building fantasy player screen
	marginX = data.width*3/10
	gridWidth = data.width - 2*marginX
	colWidth = gridWidth/2
	rowHeight = data.height/15
	left, top = marginX + col*colWidth, (row+8)*rowHeight
	right, bottom = left + colWidth, top + rowHeight
	return left, top, right, bottom

def goalieLinesCellBounds(data, row, col): # building fantasy player screen
	marginX = data.width*2/5
	gridWidth = data.width - 2*marginX
	rowHeight = data.height/15
	left, top = marginX, (row+12)*rowHeight
	right, bottom = left + gridWidth, top + rowHeight
	return left, top, right, bottom

def getForwardLinesCell(data, x, y): # for fantasy player selection
	rows, cols = data.forwardRows, data.forwardCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = forwardLinesCellBounds(data, row, col)
			if left <= x <= right and top <= y <= bottom:
				return (row, col)

def getDefenseLinesCell(data, x, y): # for fantasy player selection
	rows, cols = data.defenseRows, data.defenseCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = defenseLinesCellBounds(data, row, col)
			if left <= x <= right and top <= y <= bottom:
				return (row, col)

def getGoalieLinesCell(data, x, y): # for fantasy player selection
	rows, cols = data.goalieRows, data.goalieCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = goalieLinesCellBounds(data, row, col)
			if left <= x <= right and top <= y <= bottom:
				return (row, col)

def displayLines(canvas, data):
	canvas.create_image(data.width/8, data.height*7/10, image = data.linesImages[0])
	canvas.create_image(data.width*7/8, data.height*7/10, image = data.linesImages[1])
	if len(data.fantasyTeam) == 20:
		canvas.create_rectangle(data.width/5, 0, data.width*4/5, data.height/10,
								fill = "yellow", width = 0)
		canvas.create_text(data.width/2, 0, text = "NEXT", font = "Arial 48", anchor = "n")
	
	canvas.create_text(data.width/2, 2*data.height/15, text = "Forwards", font = "Arial 24", fill = "white", anchor = "n")
	canvas.create_text(data.width/2, 7*data.height/15, text = "Defense", font = "Arial 24", fill = "white", anchor = "n")
	canvas.create_text(data.width/2, 11*data.height/15, text = "Goalies", font = "Arial 24", fill = "white", anchor = "n")
	
	rows, cols = data.forwardRows, data.forwardCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = forwardLinesCellBounds(data, row, col)
			canvas.create_rectangle(left, top, right, bottom, fill = "white", width = 1)
			if (row, col) in data.forwardTeamCells:
				cx, cy = (left+right)/2, (top+bottom)/2
				canvas.create_text(cx, cy, text=data.forwardTeamCells[(row, col)], font = "Arial 16")
	
	rows, cols = data.defenseRows, data.defenseCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = defenseLinesCellBounds(data, row, col)
			canvas.create_rectangle(left, top, right, bottom, fill = "white", width = 1)
			if (row, col) in data.defenseTeamCells:
				cx, cy = (left+right)/2, (top+bottom)/2
				canvas.create_text(cx, cy, text=data.defenseTeamCells[(row, col)], font = "Arial 16")

	rows, cols = data.goalieRows, data.goalieCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = goalieLinesCellBounds(data, row, col)
			canvas.create_rectangle(left, top, right, bottom, fill = "white", width = 1)
			if (row, col) in data.goalieTeamCells:
				cx, cy = (left+right)/2, (top+bottom)/2
				canvas.create_text(cx, cy, text=data.goalieTeamCells[(row, col)], font = "Arial 16")

def displayGoalScorer(canvas, data): # display the goal information
	if data.goalInfo == "":
		pass
	else:
		team = data.abbrevMap[data.goalInfo[0]]
		time = data.goalInfo[1]
		info = data.goalInfo[2]

		suffix = ["th", "st", "nd", "rd"]
		period = time[0]
		period = str(period) + suffix[period%4]

		clock = time[1]
		mins = str(clock//60)
		secs = clock%60
		secs = str(secs) if secs >= 10 else "0" + str(secs)

		goalScorer = info[0]
		assistScorer = info[1]

		if isinstance(assistScorer, str):
			assistsMessage = "UNASSISTED"
		else:
			if len(assistScorer) == 1:
				assistsMessage = "ASSISTS: %s" % assistScorer[0]
			else:
				assistsMessage = "ASSISTS: %s, %s" % (assistScorer[0], assistScorer[1])

		goalMessage = "%s:%s %s - %s GOAL: %s %s " % (mins, secs, period, team, goalScorer, assistsMessage)
		canvas.create_text(data.width/2, data.height*9/10, text="Last Goal:", font = "Arial 24", anchor = "s")
		canvas.create_text(data.width/2, data.height*9/10, text=goalMessage, font = "Arial 24", anchor = "n")

def drawBoxes(canvas, data, height, spacing, text): # for splash screen
	cx = data.splashcx
	canvas.create_rectangle(cx-data.marginX, height-spacing, cx+data.marginX, height+spacing, fill="black", outline = "white", width = 1)
	canvas.create_text(cx, height, text=text, font = "Arial 20", fill = "white")

def inBoxBounds(data, x, y): # for splash screen
	cx = data.splashcx
	for mode in data.modes:
		if cx-data.marginX <= x <= cx+data.marginX and mode[0]-data.boxSpacing <= y <= mode[0]+data.boxSpacing:
			return mode[1]

def getBoxscoreCellBounds(data, row, col): # for team selection
	gridWidth = data.width - 2*data.boxscoreMarginX
	gridHeight = data.height - 2*data.boxscoreMarginY
	colWidth = gridWidth / (data.period+2)
	rowHeight = gridHeight / data.boxscoreRows
	left = data.boxscoreMarginX + col*colWidth
	top = data.boxscoreMarginY*3/2 + row*rowHeight
	right = left + colWidth
	bottom = top + rowHeight
	return left, top, right, bottom

def getTeamsCellBounds(data, row, col): # for team selection
	gridWidth = data.width - 2*data.teamsMarginX
	gridHeight = data.height - 2*data.teamsMarginY
	colWidth = gridWidth / data.teamsCols
	rowHeight = gridHeight / data.teamsRows
	left = data.teamsMarginX + col*colWidth
	top = data.teamsMarginY + row*rowHeight
	right = left + colWidth
	bottom = top + rowHeight
	return left, top, right, bottom

def getTeamsCell(data, x, y): # for team selection
	(rows, cols) = data.teamsRows, data.teamsCols
	for row in range (rows):
		for col in range (cols):
			left, top, right, bottom = getTeamsCellBounds(data, row, col)
			if left <= x <= right and top <= y <= bottom:
				return (row, col)

def drawRink(canvas, data): # for game screen
	canvas.create_line(data.topBoardsXY, width = 5) # top boards
	canvas.create_line(data.bottomBoardsXY, width = 5) # bottom boards
	canvas.create_arc(data.leftBoardsXY, start = 90, extent = 180, width = 5, style = "arc") # left arc
	canvas.create_arc(data.rightBoardsXY, start = 90, extent = -180, width = 5, style = "arc") # right arc
	canvas.create_line(data.leftGoalLineXY, fill = "red", width = 2) # left goal line
	canvas.create_line(data.rightGoalLineXY, fill = "red", width = 2) # right goal line
	canvas.create_line(data.centerRedLineXY, fill = "red", width = 10) # center red line
	canvas.create_line(data.leftBlueLineXY, fill = "blue", width = 10) # left blue line
	canvas.create_line(data.rightBlueLineXY, fill = "blue", width = 10) # right blue line
	canvas.create_rectangle(data.leftNetXY, width = 5) # left net
	canvas.create_rectangle(data.rightNetXY, width = 5) # right net

def drawPlayers(canvas, data): # for game screen
	for player in data.homeTeam:
		cx, cy, r = player.cx, player.cy, player.r
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = data.homeColor, outline = data.awayColor, width = 1)
		canvas.create_text(cx, cy, text = str(player.number), font = "Arial 12 bold", fill = data.homeFill)
	for player in data.awayTeam:
		cx, cy, r = player.cx, player.cy, player.r
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = data.awayColor, outline = data.homeColor, width = 1)
		canvas.create_text(cx, cy, text = str(player.number), font = "Arial 12 bold", fill = data.awayFill)

def drawPuck(canvas, data): # for game screen
	cx, cy, r = data.puck.cx, data.puck.cy, data.puck.r
	canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill = "black", width = 0)

def drawScoreBoard(canvas, data): # for game screen
	canvas.create_rectangle(data.width/10, data.height/40, data.width*9/10, data.height*7/40, outline = "black", width = 5)
	minutes = data.clock//60
	seconds = data.clock%60
	minutes = str(minutes)
	seconds = str(seconds) if seconds >= 10 else "0" + str(seconds)
	time = "%s:%s" % (minutes, seconds)
	canvas.create_text(data.width/2, data.height/10, text = time, font = "Arial 24", anchor = "s")

	period = str(data.period) if data.period <= 3 else "OT"
	periodText = "Period: %s" % period
	canvas.create_text(data.width/2, data.height/10, text = periodText, font = "Arial 24", anchor = "n")

	canvas.create_text(data.width/4, data.height/10, text = data.teams[0], font = "Arial 24", anchor = "s")
	canvas.create_text(data.width*3/4, data.height/10, text = data.teams[1], font = "Arial 24", anchor = "s")
	canvas.create_text(data.width/4, data.height/10, text = data.homeScore, font = "Arial 24", anchor = "n")
	canvas.create_text(data.width*3/4, data.height/10, text = data.awayScore, font = "Arial 24", anchor = "n")	

####################################
# use the run function as-is
####################################

# run function from course website
# http://www.cs.cmu.edu/~112/notes/events-example0.py

def runTP(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()    

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	# create the root and the canvas
	root = Tk()
	initIntro(data)
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

runTP(1270, 650)
