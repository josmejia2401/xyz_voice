import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd

class SearchInternet:
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

    @staticmethod
    def search_google(query):
        #query = "colombia vs francia"
        query = query.replace(' ', '+')
        URL = f"https://www.google.com/search?q={query}"
        headers = {"user-agent": SearchInternet.USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            return soup
        else:
            raise Exception("Error")
    
    @staticmethod
    def search_translate(de, a, query):
        if "español" in de:
            de = "es"
        elif "espanol" in de:
            de = "es"
        if "ingles" in de:
            de = "en"
        elif "inglés" in de:
            de = "en"

        if "español" in a:
            a = "es"
        elif "espanol" in a:
            a = "es"
        if "ingles" in a:
            a = "en"
        elif "inglés" in a:
            a = "en"

        query = query.replace(' ', '+')
        URL = f"https://translate.google.com/#view=home&op=translate&sl={de}&tl={a}&text={query}"
        headers = {"user-agent": SearchInternet.USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            return soup
        else:
            raise Exception("Error")

    @staticmethod
    def _process(resp):
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        if "temperatura" in query:
            results.append(get_weather_states(soup))
        elif "que+es" in query:
            results.append(get_definition(soup))
        elif "vs" in query:
            results.append(get_football(soup))
        else:
            for g in soup.find_all('div', class_='rc'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    item = {
                        "title": title,
                        "link": link
                    }
                    results.append(item)
        df = pd.DataFrame(data=results)#, columns=['title', 'link'])
        print(df.to_string())
    
    @staticmethod
    def get_weather_states(soup):
        item = {}
        for g in soup.find_all('div', class_='g'):

            wob_loc = g.find_all(class_='wob_loc')
            if wob_loc:
                r = wob_loc[0].text
                item['place'] = r
            
            wob_dcp = g.find_all(class_='wob_dcp')
            if wob_dcp:
                r = wob_dcp[0].text
                item['weather'] = r

            TVtOme = g.find_all('div', class_='vk_bk TylWce')
            if TVtOme:
                r = TVtOme[0].find_all('span', 'wob_t TVtOme')
                item['temperature'] = r[0].text

            TVtOme = g.find_all('div', class_='vk_bk wob-unit')
            if TVtOme:
                r = TVtOme[0].find_all('span', 'wob_t')
                item['degrees'] = r[0].text
            
            TVtOme = g.find('span', id='wob_pp')
            if TVtOme:
                item['probabilities'] = TVtOme.text
            
            TVtOme = g.find('span', id='wob_hm')
            if TVtOme:
                item['humidity'] = TVtOme.text

            TVtOme = g.find('span', id='wob_ws', class_='wob_t')
            if TVtOme:
                item['wind'] = TVtOme.text

            break

        return item

    @staticmethod
    def get_definition(soup):
        item = {}
        for g in soup.find_all('div', class_='g'):
            lW8rQd = g.find_all('div', class_='lW8rQd')
            if lW8rQd:
                r = lW8rQd[0].text
                item['gender'] = r
            eQJLDd = g.find_all('ol', class_='eQJLDd')
            if eQJLDd:
                li = eQJLDd[0].find_all('li')
                li = li[0].find_all('div', class_='QIclbb XpoqFe')
                span = li[0].find_all('span')
                item['definition'] = span[0].text
            break
        return item

    @staticmethod
    def get_football(soup):
        item = {}
        for g in soup.find_all('div', class_='g'):
            lW8rQd = g.find_all('div', class_='imso_mh__first-tn-ed imso_mh__tnal-cont imso-tnol')
            if lW8rQd:
                r = lW8rQd[0].find_all('div', class_='ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx')
                item['local'] = r[0].text
            
            lW8rQd = g.find_all('div', class_='imso_mh__l-tm-sc imso_mh__scr-it imso-light-font')
            if lW8rQd:
                item['local_r'] = lW8rQd[0].text

            lW8rQd = g.find_all('div', class_='imso_mh__second-tn-ed imso_mh__tnal-cont imso-tnol')
            if lW8rQd:
                r = lW8rQd[0].find_all('div', class_='ellipsisize liveresults-sports-immersive__team-name-width kno-fb-ctx')
                item['visitor'] = r[0].text
            
            lW8rQd = g.find_all('div', class_='imso_mh__r-tm-sc imso_mh__scr-it imso-light-font')
            if lW8rQd:
                item['visitor_r'] = lW8rQd[0].text

            break
        return item

    @staticmethod
    def get_translate(soup):
        item = {}
        for g in soup.find_all('div', class_='tlid-result result-dict-wrapper'):
            lW8rQd = g.find_all('span', class_='tlid-translation translation')
            if lW8rQd:
                r = lW8rQd[0].text
                item['translate'] = r
            break
        return item