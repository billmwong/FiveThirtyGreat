from bs4 import BeautifulSoup
from lxml import html
import requests
from urllib2 import urlopen
import urllib2,cookielib
import pandas as pd
import nba_py as nba
from nba_py import player
import sys


def makeSoup(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
	req = urllib2.Request(url, headers=hdr)
	try:
	    page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
	    print e.fp.read()
	content = page.read()

	soup = BeautifulSoup(content, 'lxml')
	return soup


def makeHeaders(soup):

	column_headers = [th.getText() for th in soup.findAll('th')]
	return  column_headers

def makeDataframe(soup):

	column_headers = makeHeaders(soup)
	data_rows = soup.findAll('tr')[1:]
	player_data = [[td.getText() for td in data_rows[i].findAll('td')] for i in range(len(data_rows))]

	df = pd.DataFrame(player_data, columns=column_headers)
	print df.head()
	return df


def getPlayerId(name):
    name = name.split(' ')

    # If returned with execption 400 bad request for url, you sometimes have to open the link in your browser then it will work. Weird bug.

    player = nba.player.get_player(name[0], name[1], just_id=True)
    return player

def getURL(id):

	print 'ID: ', int(id)
	id = str(int(id))
	url ='http://nbasavant.com/ajax/getShotsByPlayer.php?hfST=&hfQ=&pid%5B%5D='+id+'&hfSZB=&hfSZA=&hfSZR=&ddlYear=2014&txtGameDateGT=&txtGameDateLT=&ddlGameTimeGT_min=&ddlGameTimeGT_sec=&ddlGameTimeLT_min=&ddlGameTimeLT_sec=&ddlShotClockGT=&ddlShotClockLT=&ddlDefDistanceGT=&ddlDefDistanceLT=&ddlDribblesGT=&ddlDribblesLT=&ddlTouchTimeGT=&ddlTouchTimeLT=&ddlShotDistanceGT=&ddlShotDistanceLT=&ddlTeamShooting=&ddlTeamDefense=&hfPT=&ddlGroupBy=player&ddlOrderBy=shots_made_desc&hfGT=0%7C&ddlShotMade=&ddlMin=0&player_id='+id+'&data=null&_=1459806001585'
    
	return url

def getData(name):
	id = getPlayerId(name)
	url = getURL(id)
	soup = makeSoup(url)
	df = makeDataframe(soup)
	return df


if __name__ == '__main__':
	getData('stephen curry')

