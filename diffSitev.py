from editorJobScrape import *
from flask import Flask
from flask import render_template
import sqlite3 as lite
import time
import os
app = Flask(__name__)

@app.route("/")
def form():
    today =time.strftime("%b%d%Y")
    con = lite.connect("editorJobs.db")
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name FROM Jerbs WHERE Date = '%s'" %today)
        job_sites = cur.fetchall()
        cur.execute("SELECT DISTINCT Date FROM Jerbs")
        job_dates = cur.fetchall()
    cat = "meow"
    return render_template('mainPage.html',jobSites = job_sites, jobDates = job_dates)

@app.route('/siteInfo/<date>/<website>')
def changes(date,website):
    today =time.strftime("%b%d%Y")
    con = lite.connect("editorJobs.db")
    with con:
        cur = con.cursor()
        HTMLDiff = compareDatesHtml(cur,website,date,today)
    return '<h1>'+website+'</h1>'+'<br>'+ HTMLDiff

@app.route("/nate")
def nate():
    #awesomeString = ""
    #for num in range(0,50):
    #    awesomeString = awesomeString + " Is Great"
    today =time.strftime("%b%d%Y")
    con = lite.connect("editorJobs.db")
    with con:
        cur = con.cursor()
        HTMLDiff = compareDatesHtml(cur,"mediabistro","Sep122015",today)
    return '<h1>'+EDITORSITENAMES[0]+'</h1>'+'<br>'+ str( HTMLDiff)
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host ='0.0.0.0')
