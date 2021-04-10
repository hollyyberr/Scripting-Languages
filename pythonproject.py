#Holly Bernich
#python Project Scriptin Languages CS371

#import python libraries needed for the project and files
import re
import datetime
import requests
import PyRSS2Gen

mu_news_url = "https://www.monmouth.edu/news/archives/page/2/"

#html request
html = str(requests.get(mu_news_url).content, "utf-8")

#RSS module
rss = PyRSS2Gen.RSS2(
    title = "MU News Articles",
    link = mu_news_url,
    description = "All news articles and urls from the first 2 pages of Monmouth University news archives.",
    lastBuildDate = datetime.datetime.now(),
    #items array
    items = []
)

#create article list

article_html_list = re.findall(r'<a *class="anchorMargin".*?<hr.*?>', html, re.DOTALL)[:25]

#Get headlines
for article_html in article_html_list:
    headline = re.sub(r'(<.*?>|&.*?;|#.*?;)'), '', 
    re.findall(r'<strong>.*? </strong', article_html, re.DOTALL)[0])
    link = mu_news_url + "#" + re.findall(r'name=".+?"', article_html)[0][6:-1]
    #Description array
    description = []

#Split and functions
for p in re.findall(r'<p>.*? </p>', article_html, re.DOTALL)[1:]:
    if not re.match(r'.*?<img.*?', p, re.DOTALL) and len(p):
        description.extend(re.split(r'/s+', re.sub(r'(<.*?>|&.*?;)', '', p)))

#use a for loop here to add to RSS
#This adds information to the RSS files
for x in range(0,len(items)):
    rss.items.append(PyRSS2Gen.RSSItem(
    title = headline,
    link = link,
    description = description
))
#Write to XML file
rss.write_xml(open("mu_news.rss.xml", "w"))