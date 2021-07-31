import requests
import statistics
import json
import re
from bs4 import BeautifulSoup

def getRunsFromRow(row):
	return row.find_all("td")[0].text

def getPlayerStatsFromRow(row):
	cells = row.find_all("td")
	pid = re.findall(r'[0-9]*$', cells[0].find_all("a")[0]['href'].rstrip('.html'))[0]
	startYear = re.findall(r'^[0-9]*', cells[1].text)[0]
	return {
		"name": cells[0].text,
		"pid": pid,
		"avg": float(cells[7].text),
		"sr": float(cells[9].text.rstrip("*")),
		"startYear": int(startYear)
	}

def isValidScore(score):
	return score.isdigit() or score.rstrip('*').isdigit()

def getPlayerPage(playerId):
	URL = "https://stats.espncricinfo.com/ci/engine/player/" + playerId + ".html?class=1;template=results;type=batting;view=innings"
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	return  soup.find(id="ciHomeContentlhs")

def extractInnings(homeContent): 
	engneTables = homeContent.find_all("table", class_="engineTable")
	inningsTable = engneTables[3].find_all("tbody")[0]
	inningsRows = inningsTable.find_all("tr")
	return list(map(getRunsFromRow, inningsRows))


def consolidateNotOuts(scores):
	consolidatedScores = []
	currentScore = 0
	for current in scores:
		if (current.endswith('*')):
			currentScore += int(current.rstrip("*"))
		else: 
			consolidatedScores.append(currentScore + int(current))
			currentScore = 0
	consolidatedScores[-1] += currentScore
	return consolidatedScores

def cleanInnings(inningsScores):
	scoresOnly = list(filter(isValidScore, inningsScores))
	return consolidateNotOuts(scoresOnly)

def getPlayerStdev(playerId):
	homeContent = getPlayerPage(playerId)
	inningsScores = extractInnings(homeContent)
	cleanInningsScores = cleanInnings(inningsScores)
	stdev = statistics.stdev(cleanInningsScores)
	return float(stdev)

def listPlayers():
	numPlayers = 200
	URL = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=batting_strike_rate;qualmin1=3000;qualval1=runs;size=" + str(numPlayers) + ";spanmin1=1+jan+1970;spanval1=span;template=results;type=batting"
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	homeContent = soup.find(id="ciHomeContentlhs")
	engneTables = homeContent.find_all("table", class_="engineTable")
	playersTable = engneTables[2].find_all("tbody")[0]
	playerRows = playersTable.find_all("tr")
	return list(map(getPlayerStatsFromRow, playerRows))

def getPlayerConsistencyIndex():
	players = listPlayers()
	filterPlayers = list(filter(lambda player: player['avg'] > 25 and player['startYear'] > 1970, players))
	for player in filterPlayers:
		stdev = getPlayerStdev(player['pid'])
		avg = player['avg']
		consIndex = stdev / avg
		player['consIndex'] = consIndex
		print(player)
	print(filterPlayers)
	with open('outputs/playerData.json', 'w', encoding='utf-8') as f:
		json.dump(filterPlayers, f, ensure_ascii=False, indent=4)

getPlayerConsistencyIndex()
