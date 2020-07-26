from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os 
from smtplib import SMTP 
import smtplib
import ssl 
import sys
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
    #Get secret setting or fail with ImproperlyConfigured.
    
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {setting} setting.")

"""
def search_job_listings(job_title, location, desired_result, output):
	job_soup = load_indeed_jobs_div(job_title, location)
	job_list, num_listings = extract_job_information_indeed(job_soup, desired_result)

	if output == 1:
		send_mail(job_list)

	elif output == 2:
		filename = input("Please enter a filename\n.\
			For example 'job_listings'.\n> ").split(".")[0]
		save_jobs_to_excel(job_list, filename)


	print(f"{num_listings} new job postings retrieved from Indeed.")



## Output options. Email and Excel.

def send_mail(jobs_list):
	jobs = pd.DataFrame(jobs_list)

	from_email = config("FROM_EMAIL")
	from_password = config("FROM_PASSWORD")
	to_email = config("TO_EMAIL")
	message = MIMEMultipart()

	now = datetime.now().strftime("%d/%m/%Y at %H:%M:%S")
	message['Subject'] = f'Job listings on {now}'
	message['From'] = from_email
	message['To'] = to_email
	html = """\
	<html>
		<head></head>
		<body>
			{0}
		</body>
	</html>
	""".format(jobs.to_html())

	#message.set_content(html)
	s = SMTP()

	part1 = MIMEText(html, 'html')
	message.attach(part1)

	# Send email using Gmail
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(from_email, from_password)
		server.sendmail(
			from_email, to_email, message.as_string()
		)
	print(f"Email sent to {to_email}")

def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)

## INDEED JOB SEARCH FUNCTIONS 


def extract_job_information_indeed(jobs, desired_result):
	job_elements = jobs.find_all('div', class_='jobsearch-SerpJobCard')

	cols = []
	extracted_info = []

	if 'titles' in headers:
		titles = []
		cols.append('Title')
		for element in job_elements:
			titles.append(extract_job_title_indeed(element))
		extracted_info.append(titles) 

	if 'companies' in headers:
		companies = [] 
		cols.append('Companies')
		for element in job_elements:
			companies.append(extract_company_indeed(element)) 
		extracted_info.append(companies) 

	if 'links' in headers:
		links = []
		cols.append('Links')
		for element in job_elements:
			links.append(extract_link_indeed(element))
		extracted_info.append(links)


	if 'date_listed' in headers:
		dates = []
		cols.append('Listed')
		for element in job_elements:
			dates.append(extract_date_indeed(element))
		extracted_info.append(dates)


	jobs_list = {}
	# print(cols)
	# # print(range(len(extracted_info)))
	# # print(jobs_list) 
	# print(len(extracted_info[0]))
	# quit()
	for j in range(len(cols)): 
		jobs_list[cols[j]] = extracted_info[j] 


	num_listings = len(extracted_info[0])
	return jobs_list, num_listings

def load_indeed_jobs_div(job_title, location):
	args = {'q': job_title, 'l': location, 'fromage':'last', 'sort': 'date'}
	url = ('http://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(args))
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "lxml")
	jobs = soup.find(id="resultsCol")
	return jobs

def extract_job_title_indeed(element):
	title = element.find('h2', class_='title').text.strip()
	return title


def extract_company_indeed(element):
	company = element.find('span', class_='company').text.strip()
	return company


def extract_link_indeed(element):
	link = 'www.indeed.co.uk' + element.find('a')['href']
	return link 


def extract_date_indeed(element):
	date = element.find('span', class_='date').text.strip()
	return date


if __name__ == '__main__':
	intro = """\
	###############################
	#                             # 
	#      INDEED JOB SCRAPER     #   
	#                             #	 
	###############################
	"""
	print(intro)

	job_title = input("Enter a job title to search listings.\n> ")

	location = input("Enter a location.\n> ")

	try:
		output = int(input("""
Select a method to retrieve results.\n
Type 1 for Email.\n
Type 2 for Excel.\n> """))
	except ValueError:
		output = int(input("""
There has been an error.\n
Please enter the number 1 for results in an email format\n
or 2 for an Excel output.\n> """))

	headers = ['titles', 'companies', 'links', 'date_listed']
	search_job_listings(job_title, location, headers, output)

