import smtplib
import urllib2
from bs4 import BeautifulSoup
from credentials import gmail_password, gmail_user


sent_from = gmail_user
to = [gmail_user]
subject = 'OMG Super Important Message'
body = 'Hey'


email_text = """\
From: %s
To: %ss
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
try:
    server.ehlo()
    server.login(gmail_user, gmail_password)



    # specify the url
    url = 'https://secure.stinkysocks.net/NCH/NCH-201810162100SOM.html'
    # url = 'http://www.google.com/search?q=sdf&rlz=1C1GGRV_enUS761US761&oq=sdf&aqs=chrome..69i64j69i58j69i60l4.4797j1j7&sourceid=chrome&ie=UTF-8'
    # quote_page = 'http://www.bloomberg.com/quote/SPX:IND'
    # query the website and return the html to the variable
    # page = urllib2.urlopen(quote_page, headers={'User-Agent' : "Magic Browser"})


    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    con = urllib2.urlopen( req )
    print con.read()

    # print(page)


    # print("sending mail")
    # server.sendmail(sent_from, to, email_text)









finally:
    print("closing")
    server.close()
