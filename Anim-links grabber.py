
# ALL IMPORTS
import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import cloudscraper
import requests
from flask import Flask,render_template,jsonify
app = Flask(__name__)
BASE_URL = 'https://gogoanime.wiki/'

@app.route("/")
def index():
    return "Working Fine"

@app.route("/<anime_code>")
def main(anime_code):
	url = BASE_URL+anime_code
	download_url= get_gogo(url)
	vidstreaming_urls,streamsb_url=mp4_url(download_url)
	
	sbplay_urls = streamsb(streamsb_url)
	urls = {}
	urls['Vidstream'] = [vidstreaming_urls]
	urls['StreamSb'] = [sbplay_urls]
	return jsonify(urls)

def get_gogo(url):
	# creating request object
	req = requests.get(url)
	  
	# creating soup object
	data = BeautifulSoup(req.text, 'html.parser')
	
	# finding all li tags in ul and printing the text wimport reithin it
	for li in data.find_all(class_="dowloads"):
	
		return li.a.get('href')
    # return all download_url

def mp4_url(download_url):
	# creating request object
	scraper = cloudscraper.create_scraper()
	req = scraper.get(download_url)
	# creating soup object
	data = BeautifulSoup(req.text, 'html.parser')
	# print(data)
	# finding all li tags in ul and printing the text wimport reithin it
	urlcache =  data.find_all(class_="dowload")
	vidstream_urls = {}
	streamsb_url = ""
	for div in urlcache:
		tempurl = div.a.get('href')
		text_of_video = ""
	
		if "fembed" in tempurl:
			pass
		
		if "vidstreaming" in tempurl or "loadfast" in tempurl:
			print(tempurl)
			text_of_video = div.a.get_text()
			text_of_video.replace(" ", "")
			num = ''.join(filter(lambda i: i.isdigit(), text_of_video))
			print(num)
			main_quality = num[:-1]
			vidstream_urls[main_quality] = tempurl
		if "sbplay" in tempurl:
			sbplay_url = tempurl
	# print(vidstream_urls)
	# print(sbplay_url)

	# will return vidstream_urls in format {quality: url for video} and streamsb play url
	return vidstream_urls,sbplay_url


# https://sbplay2.com/d/w039rd30tszp
def streamsb(streamsb_url):
	req = requests.get(streamsb_url)
	  
	# creating soup object
	data = BeautifulSoup(req.text, 'html.parser')
	sb_url_cache = data.find_all('td')
	sbplay_urls = {}
	for td in sb_url_cache:
		
		# getting url
		try:
			download_video_func = td.a.get('onclick')
			
			
			download_streamsb_list = download_video_func.split("'")
			new_download_url = f"https://sbplay2.com/dl?op=download_orig&id={download_streamsb_list[1]}&mode={download_streamsb_list[3]}&hash={download_streamsb_list[5]}"
			

			down_req = requests.get(new_download_url)
			data = BeautifulSoup(down_req.text, 'html.parser')

			span = data.find('span')
			try:
				main_sb_url = span.a.get('href')
			except AttributeError:
				streamsb(streamsb_url)
			
			# getting quality
			main_quality = td.a.get_text()
			# assigning streamsb urls and quality in dictionary
			sbplay_urls[main_quality] = main_sb_url
		except:
			pass
	return sbplay_urls

if __name__ == '__main__':
	app.run(host='localhost', port=8000,debug=True)