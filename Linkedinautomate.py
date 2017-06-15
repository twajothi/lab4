import argparse, os, time
import urlparse, random
from selenium import webdriver
#from selenium import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#from pandas import *
#import pandas
from collections import deque
import getpass
import Tkinter
import tkFileDialog
import re
def getPeopleLinks(browser,noofpage):
    links = []   
    for i in range(1,noofpage):           
        page = BeautifulSoup(browser.page_source)
        for link in page.find_all("a","title"):
            url = link.get("href")
            links.append(url)
        pagination = browser.find_element_by_xpath("//li[@class='next']/a")
        # if pagination:
        pagination.click()
        time.sleep(5)
    return links
        
def getID(url):
   pUrl = urlparse.urlparse(url)
   return urlparse.parse_qs(pUrl.query)["id"][0]


def getProfileDetails(detailprofile):
    try:
        name = detailprofile.find("span","full-name").get_text(strip=True)
    except:
        name = ""
        
    try:
        headline = detailprofile.find("p","title").get_text(strip=True)
    except:
        headline = ""
    
    try:    
        location= detailprofile.find("span","locality").get_text(strip=True)
    except:
        location = ""
    
    try:
        cur = detailprofile.find("tr",id="overview-summary-current").find_all("a",href=re.compile("/company/"))
        curcompany= ' '.join(g.get_text() for g in cur)
    except:
        curcompany=""
    try:
        pas =detailprofile.find("tr",id="overview-summary-past").find_all("a",href=re.compile("/company/"))
        pastcompany= ' '.join(g.get_text() for g in pas)
    except:
        pastcompany="" 
    try:
        edu =detailprofile.find("tr",id="overview-summary-education").find_all("a",href=re.compile("/edu/"))
        education= ' '.join(g.get_text() for g in edu)
    except:
        education=""
    
    try:
        contact = detailprofile.find("div",id="contact-comments-view").get_text(strip=True)
    except:
        contact =""
    
    try:
        email = detailprofile.find("li",id="relationship-email-item-0").get_text(strip=True)
    except:
        email =""
    
    try:
        phone = detailprofile.find("div",id="relationship-phone-numbers-view").get_text(strip=True)
    except:
        phone =""
        
    return name, headline, location , curcompany,pastcompany, education, contact,email,phone
    

def ViewBot(browser,noofpage):
    visited = {}
    pList = []
    count = 0
    people = getPeopleLinks(browser,noofpage)
    Name= []
    HeadLine=[]
    Location = []
    CurCompany = []
    Pastcompany = []
    Education = []
    Contact = []
    Email = []
    Phone=[]
    ProfileLink=[]
    while True:
	#sleep to make sure everything loads, add random to make us look human.
        time.sleep(1) 
        if people:
            for person in people:
                try:
                    ID = getID(person)
                    if ID not in visited:
                        pList.append(person)
                        visited[ID] = 1
                except:
                    print "ID not Found"
                    
        pList=deque(pList)
        if pList: #if there is people to look at look at them
            detailprofile=""
            person = pList.popleft()
            browser.get(person)
            time.sleep(1.5)
            try:
                contactinfo = browser.find_element_by_xpath("//div[@class='show-more-info relationship-contact']/a")
                contactinfo.click()
            except:
                print "No contact"                
            time.sleep(1.5)
            detailprofile = BeautifulSoup(browser.page_source)
            name, headline, location,curcompany,pastcompany, education, contact,email,phone = getProfileDetails(detailprofile)
            Name.append(name)
            HeadLine.append(headline)
            Location.append(location)
            CurCompany.append(curcompany)
            Pastcompany.append(pastcompany)
            Education.append(education)
            Contact.append(contact)
            Email.append(email)
            Phone.append(phone)
            ProfileLink.append(person)
            count += 1
        else: #otherwise find people via the job pages
            print "Im Lost Exiting"
            break

		#Output (Make option for this)			
        print count

    Linkedin = DataFrame({'Name' : Series(Name).str.title(),
    'HeadLine' : Series(HeadLine).str.title(),
    'Location' : Series(Location).str.title(),
    'Current company' : Series(CurCompany).str.title(),
    'Past company': Series(Pastcompany).str.title(), 
    'Education' : Series(Education).str.title(),
    'Contact' : Series(Contact).str.replace('\n','').str.encode('ascii','ignore'),
    'Email' : Series(Email).str.encode('ascii','ignore'),
    'Phone' : Series(Phone).str.encode('ascii','ignore'),
    'Profile Link' : Series(ProfileLink)})
    return Linkedin

    
				        
        #else: #otherwise find people via the job pages
         #   print "Complete"
         #   break

        
def Main():
    
    
    #parser = argparse.ArgumentParser()
    #parser.add_argument("email", help="linkedin email")
    #parser.add_argument("password", help="linkedin password")
    #parser.add_argument("Profile", help="linkedin profile")
    #args = parser.parse_args()
    #noofpage=int(round(float(args.Profile)/10)+1)
    Email = raw_input('Enter your Email: ')
    Password= getpass.getpass(prompt='Enter your password: ')
    Query=raw_input('Enter your search URL : ')
    noofprofile=int(input('Enter no of profile: '))
  
    noofpage=int(round(float(noofprofile)/10)+1)
    print "Name the file for save the result"
    root = Tkinter.Tk()
    root.withdraw() #use to hide tkinter window
    currdir = os.getcwd()
    formats = [('Comma Separated values', '*.csv'), ]
    tempdir = tkFileDialog.asksaveasfilename(parent=root, filetypes=formats,initialdir=currdir, title='Please select a directory')
    
    #driverpath='c:\\chromedriver.exe'
    browser = webdriver.Firefox()
    
    browser.get("https://linkedin.com/uas/login")
    

    emailElement = browser.find_element_by_id("session_key-login")
    emailElement.send_keys(Email)
    passElement = browser.find_element_by_id("session_password-login")
    passElement.send_keys(Password)
    passElement.submit()
    
    os.system("cls")
    print "[+] Success! Logged In, Bot Starting!"
    time.sleep(random.uniform(5.5,6.9))
    SelectElement=browser.find_element_by_id("jobs")
    Select(SelectElement).select_by_value("people")
    SearchElement = browser.find_element_by_id("main-search-box")
    SearchElement.send_keys(Query)
    SearchElement.submit()
    browser.get(Query)
    time.sleep(5)
    Linkedin1 = ViewBot(browser,noofpage) 
    #Linkedin1.to_csv('C:\\Users\\karamchand.g\\Desktop\\' + 'Freelancer' +'.csv',encoding='utf-8',index=False)
    Linkedin1.to_csv( str(tempdir).replace('/','\\') +'.csv',encoding='utf-8',index=False)   
    time.sleep(5)
    browser.close()

if __name__ == "__main__":
    Main()
