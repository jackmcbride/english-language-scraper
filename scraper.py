from bs4 import BeautifulSoup
import requests
import io
import os
import json
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

def scrape_html(url):
    site=requests.get(url)
    data=site.content.decode("utf-8")
    soup=BeautifulSoup(data, "lxml")

    return soup


def scrape_menu(soup):
    pages=[]
    
    for data in soup.find("div", {"class" : "list-page-wrapper"}):
        for a in data.find_all("a"):
            if "basics/speaking_basics_" in a.get("href"):
                pages.append(a.get("href"))
    
    return pages


def scrape_links(prefix, pages):
    links=[]

    for page in pages:    
        soup=scrape_html(prefix+page)

        for data in soup.find_all("div", {"class" : "steps-learn"}):
            for a in data.find_all("a"):
                if "lessondetails" in a.get("href"):
                    links.append("http://www.talkenglish.com"+a.get("href"))
        
    return links


def scrape_phrases(links):
    phrases={}
    
    for link in links:
        phrase_dict={}
        soup=scrape_html(link)

        #Set dictionary key to phrase root
        key=soup.find("h1").get_text().strip()
        print("Populating brain with phrases for: %s" % key + "...")

        phrase_list=[]
        
        for data in soup.find_all("div", {"class" : "sm2-playlist-bd"}):
            for a in data.find_all("a"):
                for phrase in a:
                    if len(phrase) > 0 and "Listen to the Entire Lesson" not in phrase:
                        phrase_list.append(phrase)
        phrase_dict[key] = phrase_list

        phrases.update(phrase_dict)
    
    print("Brain populated!")
    #print(phrases)
    return phrases
   
                
def main():
    #Scrape HTML from "english-for-students" home page
    html = scrape_html("http://www.talkenglish.com/speaking/listbasics.aspx")
    prefix = "http://www.talkenglish.com/speaking/"
    #Scrape menu links
    pages = scrape_menu(html)
    #Scrape links from sub pages
    links = scrape_links(prefix, pages)
    #Scrape phrases from sub pages
    phrases = scrape_phrases(links)

    with io.open("data/phrases/phrase_data.json", 
                 "w", encoding="utf-8") as outfile:
                 str_ = json.dumps(phrases, indent=2, sort_keys=False,
                                   separators=(',', ': '), ensure_ascii=False)
                 outfile.write(to_unicode(str_))

if __name__ == "__main__":
    main()