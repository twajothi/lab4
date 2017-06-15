import argparse, os, time
import urlparse, random 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # enter data to the screen
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup 

def getPeopleLinks(page): 
    links = [] 
    for link in page.find_all('a'):
        url = link.get('href')
        if url: 
            if 'profile/view?id' in url: 
                links.append(url)
    return links 

def getJobLinks(page): 
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url: 
            if '/jobs' in url: 
                links.append(url)
    return links 

def getID(url): 
    pUrl = urlparse.urlparse(url)
    print pUrl
    return urlparse.parse_qs(pUrl.query)['id'][0]
def ViewBot (browser): 
    visited = {}   # already visited people 
    pList = [] # people that we need to visit 
    count = 0 
    while True: 
        # sleep to make sure everything works 
        # add rendom to make this bot look human. 
        time.sleep(random.uniform(3.5, 6.9))
        page = BeautifulSoup(browser.page_source)
        people = getPeopleLinks(page)
        print people
        if people: 
            for person in people: 
                ID = getID(person)
                if ID not in visited: 
                    pList.append(person)
                    visited[ID] = 1
        if pList: # if there is people to look at then look at them 
            person = pList.pop()
            browser.get(person)
            count +=1 
        else: #otherwise find people via job pages 
            jobs = getJobLinks(page)
            if jobs: 
                    job = random.choice(jobs)
                    root = 'http://www.linkedin.com'
                    roots = 'http://www.linkedin.com'
                    if root not in job or roots not in job: 
                        job = 'https://www.linkedin.com'+job
                        browser.get(job)
                    else: 
                            print "I am fuckin lost "
                            break
        #output make option for this 
        print "[+]"+browser.title+" Visited! \n ("\
                                +str(count)+"/"+str(len(pList))+ ") visited/Queue"

def Main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help = "linkedin email" )
    parser.add_argument("password", help = "linkedin password")
    args = parser.parse_args()
    
    # binary = FirefoxBinary('path/to/installed firefox binary')
    #browser = webdriver.Firefox(firefox_binary = binary)
    browser = webdriver.Firefox()
    browser.get ("https://linkedin.com/uas/login")

    emailElement = browser.find_element_by_id("session_key-login")
    emailElement.send_keys(args.email)
    passElement = browser.find_element_by_id("session_password-login")
    passElement.send_keys(args.password)
    passElement.submit()

    os.system('clear')
    print "[++] Hell year success! Logged In, Bot starting "
    ViewBot(browser)
    browser.close()
if __name__ == '__main__': 
    Main()
