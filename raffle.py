import requests
import time
import urllib
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#Open browser and go to facebook loginn page
login_url = 'https://www.facebook.com/'

chrome_options = Options()
# Disable notifications in chrome options
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(chrome_options=chrome_options)

def login():
	""" Login """
	driver.find_element_by_id('email').send_keys('EMAIL')
	driver.find_element_by_id('pass').send_keys('PASSWORD' + '\n')

def show_all_comments():
	""" Get all comments """
	# Click on the comment sort button
	driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div/div[3]/div[1]/div/div/div/div/div/a').click()
	time.sleep(2)
	# Click "from newest comment to oldest"
	driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div/div/div/ul/li[2]/a/span/span/div').click()
	time.sleep(2)
	# Save the "load more comments" element in to a variable
	elem = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div/div[3]/div[3]/div/a/div/span')
	# Set the number of show more clicks (Facebook will show 50 more comments per show more click)
	no_of_showmores = 42
	#no_of_showmores = 1
	no_clicks = 0
	while no_of_showmores:
		# Click showmore and scroll down
		elem.click()
		time.sleep(2)
		scroll_down()
		no_of_showmores -= 1
		no_clicks += 1
		print (no_clicks)

def scroll_down():
	""" Scroll down """
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# Go to Facebook login page
driver.get(login_url)
time.sleep(1)
login()
time.sleep(3)
# Go to raffle url
driver.get('https://www.facebook.com/hiustuotteet.fi/posts/171018270962997?comment_id=1045874042411705&notif_id=1578208568821225&notif_t=feed_comment')
show_all_comments()
# Set number of comments to 1
no_of_comments = 1
# Get all the comments now that they have been loaded to the DOM
list_of_comments = driver.find_elements_by_css_selector("._2h2j")
print(len(list_of_comments))

for comment in list_of_comments:
	# Iterate through each comment 
	try:
		# Save commentors name to a variable
		name_x_path =    f"/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div/div[3]/ul/li[{no_of_comments}]/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div/a"
		element_name = driver.find_element_by_xpath(f'{name_x_path}')
		name = element_name.get_attribute('text')
		# Increase number of comments by 1
		no_of_comments += 1
		print(name)
		# Save the name to a textfile
		filename = 'raffle.txt'
		with open(filename, 'a') as file_object:
			file_object.write(f'{name}\n')
	except NoSuchElementException:
		no_of_comments += 1
		continue
	except UnicodeEncodeError:
		no_of_comments += 1
		continue

print(f"Number of comments: {no_of_comments}")
