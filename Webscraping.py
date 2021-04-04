import json
import os

import pickle
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

"url = https://httpbin.org/ip"
class Webscraping:
    def __init__(self):
        self.proxy_url = "https://sslproxies.org/"

    def create_path(self):
        folder_name = 'Temp_file'  # this is folder name
        current_dir = os.getcwd()  # this is path
        path = os.path.join(current_dir, folder_name)  # create folder path
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        return path
    
    def creatname(self,url):
        nstr = (url.replace('https://','')).split('.')
        try:
            str1 = nstr[1]
            # remove any spacial charater 
            sr = (''.join(x for x in str1 if x.isalpha()))
        except IndexError:
            str1 = nstr[0]
            sr = (''.join(x for x in str1 if x.isalpha()))
        except :
            str1 = "Defult"
            sr = (''.join(x for x in str1 if x.isalpha()))
        return sr

    def proxy_generator(self,url):
        response = requests.get(self.proxy_url)
        soup = BeautifulSoup(response.content, 'html5lib')
        proxy = ((list(map(lambda x: x[0] + ':' + x[1], list(
            zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8]))))))[0:100])
        
        jurl = self.creatname(url) + '.json'  # this is for create new name every time url change
        pg_file = self.create_path() + '\\' + jurl
        with open(pg_file, 'w')as op:
            json.dump(proxy, op)

    def jproxy(self,url):
        flist = os.listdir(self.create_path())
        jurl = self.creatname(url) + '.json'  # this is for create new name every time url change
        jp_file = self.create_path() + '\\' + jurl
        if jurl in flist:
            with open(jp_file, 'r')as op:
                jlod = json.load(op)
        else:
            self.proxy_generator(url)
            with open(jp_file, 'r')as op:
                jlod = json.load(op)
        return jlod

    def cokiere(self,url):
        flist = os.listdir(self.create_path())
        nurl = self.creatname(url)  # remove all spacial charater and number # this is for create new name every
        # time url change
        ck_nurl = self.create_path() + '\\' + nurl
        if nurl in flist:
            with open(ck_nurl, 'rb')as op:
                jscokie = pickle.load(op)
        else:
            jscokie = None
        return jscokie

    def webpage(self,url):
        ua = UserAgent()
        jcoke = self.cokiere(url)
        # this is for create new name if every time url change (string value return)
        gjurl = self.creatname(url) + 'goodproxy.json' 
        # this is temp_file in goodproxy.json file link
        wp_gjurl = self.create_path() + '\\' + gjurl
        # this is goodproxy.json file
        file = os.listdir(self.create_path())
        count = 0
        while True:
            hd = ua.random  # random user agent only
            _ua = {'User-Agent': hd}
            try:
                try:
                    with open(wp_gjurl, 'r')as op:
                        old_proxy = json.load(op)
                    res = requests.get(url, proxies=old_proxy, timeout=7, headers=_ua, cookies=jcoke)
                    return res
                    break

                except FileNotFoundError:
                    pxy = (self.jproxy(url))[count]
                    proxy = dict(https=pxy)
                    res = requests.get(url, proxies=proxy, timeout=7, headers=_ua, cookies=jcoke)
                    with open(wp_gjurl, 'w')as op:
                        json.dump(proxy, op)
                    nurl = self.creatname(url)
                    ck_nurl = self.create_path() + '\\' + nurl
                    with open(ck_nurl, 'wb')as f:
                        pickle.dump(res.cookies, f)
                    if count ==100:
                        count -=100
                        self.proxy_generator(url)
                    else:
                        pass
                    return res
                    break

                except :
                    os.remove(wp_gjurl)
                    pxy = (self.jproxy(url))[count]
                    proxy = dict(https=pxy)
                    res = requests.get(url, proxies=proxy, timeout=7, headers=_ua, cookies=jcoke)
                    with open(wp_gjurl, 'w')as op:
                        json.dump(proxy, op)
                    nurl = self.creatname(url)
                    ck_nurl = self.create_path() + '\\' + nurl
                    with open(ck_nurl, 'wb')as f:
                        pickle.dump(res.cookies, f)
                    if count ==100:
                        count -=100
                        self.proxy_generator(url)
                    else:
                        pass
                    return res
                    break

            except:
                pass
            count +=1