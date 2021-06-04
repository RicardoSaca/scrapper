# tutorial = https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import time
import csv
import parameters
import re

def linkedin():
    #Load page on driver and go to linkedin
    driver.get('https://www.linkedin.com/')

    #find username box using by_class_name and input email
    username = driver.find_element_by_id('session_key')
    username.send_keys(parameters.linkedin_email)
    time.sleep(0.5)

    #find password box using by_class_name and input password
    password = driver.find_element_by_id('session_password')
    password.send_keys(parameters.linkedin_password)
    time.sleep(0.5)

    #locate submit button by x_path and click
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    time.sleep(0.5)

    # Add a phone number for security
    # skip_button = driver.find_element_by_class_name("secondary-action")
    # skip_button.click()

def get_google(num_links=10, searchQuery=parameters.search_query):

    num_pages = int(num_links / 10)

    #open google
    driver.get('https://www.google.com/')
    time.sleep(2)

    #locate search bar and input query
    search_query = driver.find_element_by_name('q')
    search_query.send_keys(searchQuery)
    time.sleep(0.5)

    search_query.send_keys(Keys.RETURN)
    time.sleep(2)

    page = 0
    linkedin_urls =[]

    for i in range(0,num_pages):
        # locate and extract linkedin urls
        links = driver.find_elements_by_xpath("//div[@class='g']//div[@class='yuRUbf']/a['@href']")
        links = [url.get_attribute("href") for url in links]

        # add links to url list
        linkedin_urls += links
        time.sleep(0.5)

        # go to next page
        # consider add a limit if i = max
        next = driver.find_element_by_xpath("//span[contains(text(), 'Next')]")
        next.click()

    # #locate and extract linkedin urls
    # linkedin_urls = driver.find_elements_by_xpath("//div[@class='g']//div[@class='yuRUbf']/a['@href']")
    # linkedin_urls = [url.get_attribute("href") for url in linkedin_urls]
    # time.sleep(0.5)
    # page += 1
    # print(page)
    # print('length of urls', len(linkedin_urls))
    # next = driver.find_element_by_xpath("//span[contains(text(), 'Next')]")
    # next.click()

    return linkedin_urls

def parse_urls(urls, wanted):
    #Open and sign in to linkedin
    linkedin()

    #go through urls
    for url in urls:
        #open url
        driver.get(url)
        time.sleep(5)

        #assing the source code for the page to a var sel
        sel = Selector(text=driver.page_source)

        #get name
        name = sel.xpath("//h1[not(@class='global-nav__branding')]/text()").extract_first()

        if name:
            name = name.strip()

        #get jobtitle
        job_title = sel.xpath("//div[@class='text-body-medium break-words']/text()").extract_first()

        if job_title:
            job_title = job_title.strip()

        #get company
        company = sel.xpath("//div[@aria-label='Current company']/text()").extract_first()

        if company:
            company = company.strip()

        #get college
        college = sel.xpath("//div[@aria-label='Education']/text()").extract_first()
        if college:
            college = college.strip()

        #get college different way
        # not working ####################################################
        #find ul item:
        resultSet = sel.xpath("//*[@id='ember572']")
        options = resultSet.find_elements_by_tag_name("li")
        #loop through li:
        for option in options:
            print(option.text)


        # get location
        location = sel.xpath("//span[@class='text-body-small inline t-black--light break-words']/text()").extract_first()

        if location:
            location = location.strip()

        linkedin_url = driver.current_url

        #validating if the fields exist on the profile
        name = validate_field(name)
        job_title = validate_field(job_title)
        company = validate_field(company)
        college =  validate_field(college)
        location = validate_field(location)
        linkedin_url = validate_field(linkedin_url)

        # print to terminal
        # print_url(name, job_title, company, college, location, linkedin_url)

        #write to file output
        writer.writerow([name, job_title, company, college, location, linkedin_url])

#ensure all key data fields hava a value
def validate_field(field):# if field is present pass
    if field:
        pass
# if field is not present print text
    else:
        field = 'No results'
    return field

def print_url(name, job_title, company, college, location, linkedin_url):
        # print to terminal
        print('\n')
        print('Name: ' + name)
        print('Job Title: ' + job_title)
        print('Company ' + company)
        print('College: ' + college)
        print('Location: ' + location)
        print('URL: ' + linkedin_url)

def inputs(): #main program
    more = 'Y'
    wanted = []

    while(more != 'N'):
        #Ask for number of people wanted
        number_links = int(input('Input number of search results wanted: '))
        #Ask for position and location wanted
        query = 'site:linkedin.com/in/ AND '
        print('What is the query you are looking for? ')
        query += str(input('site:linkedin.com/in/ AND ? '))
        # position = re.search('\"(.*?)\"', query)
        # if position:
        #     position = position.group(0).strip('"')
        #Ask if searching for more positions
        more = input('Searching for another position? (Y/N) ').upper()
        wanted.append([number_links, query])

    return wanted

##################
## Main program ##
##################

#ask for inputs
wanted = inputs()

#Create a new instance of Chrome
driver = webdriver.Chrome(executable_path=parameters.path)

linkedin_urls = []
for i in wanted:
    #find ulrs of interest
    linkedin_urls += get_google(i[0], i[1])

# open file
with open('results.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    #write to file object
    writer.writerow(['Name','Job Title','Company','College','Location','URL'])

    #parse urls and extract data
    results = parse_urls(linkedin_urls, wanted)

#terminate the application
driver.quit()

print("Scrapping Completed")

#################################################
# TO - DO:
# Univeristy improvement
# Skills?
#
#
#################################################