import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import cloudscraper
import requests
#()
from flask import Flask,render_template
app = Flask(__name__)
# anime_code = input("enter anime code: ")
# url = "https://gogoanime.wiki/"+anime_code
  

def get_gogo(url):
	# creating request object
	req = requests.get(url)
	  
	# creating soup object
	data = BeautifulSoup(req.text, 'html.parser')
	
	# finding all li tags in ul and printing the text wimport reithin it
	for li in data.find_all(class_="dowloads"):
	
		return li.a.get('href')


def mp4_url(download_url):
	# creating request object
	scraper = cloudscraper.create_scraper()
	req = scraper.get(download_url)
	# creating soup object
	data = BeautifulSoup(req.text, 'html.parser')
	# print(data)
	# finding all li tags in ul and printing the text wimport reithin it
	urlcache =  data.find_all(class_="dowload")
	for div in urlcache:
		print(div.a.get('href'))

# https://sbplay2.com/d/w039rd30tszp
def streamsb(streamsb_url):
	req = requests.get(streamsb_url)
	  
	# creating soup object
	data = BeautifulSoup(req.text, 'html.parser')
	sb_url_cache = data.find('td')
	download_video_func = sb_url_cache.a.get('onclick')
	
	download_streamsb_list = download_video_func.split("'")
	new_download_url = f"https://sbplay2.com/dl?op=download_orig&id={download_streamsb_list[1]}&mode={download_streamsb_list[3]}&hash={download_streamsb_list[5]}"
	

	down_req = requests.get(new_download_url)
	data = BeautifulSoup(down_req.text, 'html.parser')

	span = data.find('span')
	try:
		download_video_func = span.a.get('href')
	except AttributeError:
		streamsb(streamsb_url)
	print(download_video_func)

streamsb_url = input('Enter Streamsb URL: ')
streamsb(streamsb_url)

  