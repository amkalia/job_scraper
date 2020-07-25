
import json 
import os 
import smtplib
import urllib
from bs4 import BeautifulSoup
from decouple import config
import pandas as pd
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 


## LOAD UP SETTINGS FOR GMAIL

"""
BASE_DIR = os.path.dirname((os.path.abspath(__file__)))




with open(os.path.join(os.path.dirname(BASE_DIR), "secrets.json")) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """
    #Get secret setting or fail with ImproperlyConfigured.
    """
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {setting} setting.")

"""

def load_indeed_jobs_div(job_title, location):
	args = {'q': job_title, 'l': location, 'fromage':'last', 'sort': 'date'}
	url = ('http://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(args))
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "lxml")
	jobs = soup.find(id="resultsCol")
	return jobs




def send_mail(jobs_list):
	jobs = pd.DataFrame(jobs_list)

	html = """\
	<html>
		<head></head>
		<body>
			{0}
		</body>
	</html>
	""".format(jobs.to_html())

	from_email = config(FROM_EMAIL)
	from_password = config(FROM_PASSWORD)








def extract_job_information_indeed(jobs, desired_result):
	job_elements = jobs.find_all('div', class_='jobsearch-SerpJobCard')

	cols = []
	extracted_info = []

	if 'titles' inn desired_result:
		titles = []
		cols.append('titles')
		for element in job_elements:
			titles.append(extract_job_title_indeed(element))
		extracted_info.append(titles)

	if 'companies' in desired_result:
		companies = []
		cols.append('companies')
		for element in job_elements:
			cols.append(extract_company_indeed(element))
		extracted_info.append(companies)

	if 'links' in desired_result:
		links = []
		cols.append('links')
		for element in job_elements:
			links.append(extract_link_indeed(element))
		extracted_info.append(links)

	if 'date_listed' in desired_result:
		dates = []
		cols.append('date_listed')
		for element in job_elements:
			dates.append(extract_date_indeed(element))
		extracted_info.append(dates)

	jobs_list = {}
	for j in range(len(cols)):
		jobs_list[cols[j]] = extracted_info[j]

	num_listings = len(extracted_info[0])
	return jobs_list, num_listings





def extract_job_title_indeed(element):
	title = element.find('h2', class_='title').text.strip()
	return title


def extract_company_indeed(element):
	company = element.find('span', class_='company'),text.strip()
	return company


def extract_link_indeed(element):
	link = 'www.indeed.co.uk/' + element.find('a')['href']
	return link 


def extract_date_indeed(element):
	date = element.find('span', class_='date').text.strip()
	return date



