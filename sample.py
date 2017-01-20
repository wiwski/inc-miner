#HTTP Request for scral
import requests

#HTML parser
from bs4 import BeautifulSoup

import json

#Make the query and get a list of links to scrap
def search_query(query, search_engine):
	if search_engine == 'bing':
		url = 'https://api.cognitive.microsoft.com/bing/v5.0/search?q='+query
		header = {'ocp-apim-subscription-key': '386047532b4243369df5e5abd2c76dab'}
		r = requests.get(url, headers=header)
		query_json = r.json
		links = x["webPages"]["value"]

		for link in links:
			links_list.append(link["displayUrl"])

		return links_list		



	elif search_engine == 'google':
		url  = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCKOXT3npc_zHa3VTDMTkT6erzeKhu3FN0&q='+query+'&cx=001235176516091570544:z2abylo6azu'
		header = None	
	
	r = requests.get(url, headers=header)
	return r

def getUrlsFromBing(data):
	with open('modcloth_bing.json', 'r') as f:
		links_list = list()

		x = json.load(f)
		f.closed

		links_contain = x["webPages"]["value"]
		
		#pickup the links and make sure starts with 'http'
		for link in links_contain:
			if link["displayUrl"][0:4] != 'http':
				link["displayUrl"] = 'http://'+link['displayUrl']
			links_list.append(link["displayUrl"])

		return links_list		


def getHtml(url):
	r = requests.get(url)
	return r.text


def cleanHtml(html):
    for script in html(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    

    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '. '.join(chunk for chunk in chunks if chunk)
    return text

#for test : write to a file
def write_file(data, fname):
	with open(fname, 'w') as f:
		f.write(data)
	f.closed

###MAIN###

#Comment because working with json file for now
#urls_to_scrap = search_query('modcloth', 'bing')

#use for test with query = modcloth stored in json
#write_file(query.text, 'modcloth_bing.json')
scrap_info = list()

with open('modcloth_bing.json', 'r') as f:
	x = json.load(f)
f.closed
urls_to_scrap = getUrlsFromBing(x)

for url in urls_to_scrap:
	to_parse = getHtml(url)
	soup = BeautifulSoup(to_parse, 'lxml')
	html_btfy = cleanHtml(soup)
	scrap_info.append(html_btfy)

scrap_info_json = json.dumps(scrap_info)
write_file(scrap_info_json, 'results.txt')


