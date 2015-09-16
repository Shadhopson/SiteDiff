import urllib2
import time
import re
from bs4 import BeautifulSoup
import sqlite3 as lite

EDITORSITENAMES = ["macmillain","publishersmarketplace","bookjobs","mediabistro","simonandschuster","disney",'hachette','bloomsbury','candlewickpress']
EDITORSITELIST = ['https://re21.ultipro.com/HOL1002/JobBoard/ListJobs.aspx','http://www.publishersmarketplace.com/jobs/','http://www.bookjobs.com/search-jobs?editSubmit=1&prmSearchStr=&prmPublisher=0&prmLocation=&prmJobPrefIDs[]=32&editSubmit=Search','http://www.mediabistro.com/Book-Publishing-jobs.html','https://cbs.avature.net/cbssscareers','http://disneycareers.com/en/search-jobs/jobsearch-results/?jqs=[{%22c%22%3A%22US%257CCA%22%2C%22s%22%3A%22%22%2C%22g%22%3A%22%22%2C%22co%22%3A%22%22%2C%22in%22%3A%22Publishing%22%2C%22p%22%3A%22%22%2C%22jc%22%3A%22%22%2C%22e%22%3A%22%22%2C%22q%22%3A%22%22%2C%22r%22%3A%22%22}]','https://hire.jobvite.com/CompanyJobs/Careers.aspx?c=q5u9Vfwn&cs=9YmbVfwa&nl=0','http://bloomsbury.com/us/company/careers/','http://www.candlewick.com/about_careers.asp?f=1']


def getManyHTML(siteList):
    totalSoup =[]
    for site in siteList:
        editorSite = urllib2.urlopen(site)
        siteHtml = editorSite.read()
        editorSite.close()
        soup = BeautifulSoup(siteHtml, "lxml")
        totalSoup.append(unicode(soup))
    return totalSoup


def makeSQLData(Names, Urls,Htmls,Date):
    tupleArgs =()
    for item in range(0,len(Names)):
        tupleArgs = tupleArgs + ((Names[item],Urls[item],Htmls[item],Date),)
    return tupleArgs

def saveAsSQL(SQLcursor,dataList):
    today =time.strftime("%b%d%Y")
    SQLcursor.execute("CREATE TABLE IF NOT EXISTS %s (Name TEXT, URL TEXT, HTML TEXT, Date TEXT)" % "Jerbs")
    SQLcursor.execute("DELETE FROM Jerbs WHERE Date = '%s'" % today) 
    SQLcursor.executemany("INSERT INTO %s" % "Jerbs" +" VALUES (?,?,?,?)",dataList)

def getHtmlOnDate(SQLcursor,website,date):
    SQLcursor.execute("SELECT HTML FROM Jerbs WHERE Date = '%s' AND Name = '%s'" % (date,website))
    return SQLcursor.fetchall()[0][0]

def compareDatesHtml(SQLcursor,website, oldDate, newDate):
    oldHtml = getHtmlOnDate(SQLcursor,website,oldDate)
    newHtml = getHtmlOnDate(SQLcursor,website,newDate)
    oldHtml = oldHtml.split("\n")
    newHtml = newHtml.split("\n")
    htmlDiff =[]
    for line in newHtml:
        if len(line)<5:
            continue
        if (line not in oldHtml):
            htmlDiff.append(line.strip())
    return "<br>".join(htmlDiff)
    
def main():
    today =time.strftime("%b%d%Y")

    con = lite.connect("editorJobs.db")

    with con:
        cur = con.cursor()

        sitesHtmls = getManyHTML(EDITORSITELIST)
        dataList = makeSQLData(EDITORSITENAMES,EDITORSITELIST,sitesHtmls,today)
        saveAsSQL(cur,dataList)
        compareDatesHtml(cur,"macmillain","Sep092015",today)


if __name__ == '__main__':
    main()
