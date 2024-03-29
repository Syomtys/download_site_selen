import os
import re
import shutil
import random
import threading
from itertools import groupby
from random import choice
from string import ascii_uppercase
import requests
from datetime import datetime
from bs4 import BeautifulSoup

chdir_path = 'test'
rep_href_a = 0
prename = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 8)))

def Start():
    def pass1():
        pass

    def ReplaseUrl(ReplaceUrl, HrefFile):
        # print(HrefFile)
        HrefFile = HrefFile.replace('///', '//')
        if HrefFile[0:2] == '//':
            HrefFile = 'https:' + HrefFile
        elif HrefFile[0:4] == 'http':
            pass
        else:
            if HrefFile[0:9] == '../../../':
                HrefFile = ReplaceUrl + HrefFile[9:]
            if HrefFile[0:6] == '../../':
                HrefFile = ReplaceUrl + HrefFile[6:]
            elif HrefFile[0:4] == '././':
                HrefFile = ReplaceUrl + HrefFile[4:]
            elif HrefFile[0:3] == '../':
                HrefFile = ReplaceUrl + HrefFile[3:]
            elif HrefFile[0:1] == '/':
                HrefFile = ReplaceUrl + HrefFile[1:]
            elif HrefFile[0:1] == ' ':
                HrefFile = ReplaceUrl + HrefFile[1:]
            elif HrefFile[0:2] == './':
                HrefFile = ReplaceUrl + HrefFile[2:]
            elif HrefFile[0:3] == '/-/':
                HrefFile = ReplaceUrl + HrefFile[3:]
            else:
                HrefFile = ReplaceUrl + HrefFile
        # print(HrefFile)
        return HrefFile

    def SaveUrl(urls, file_writing):
        file_num = str(random.randint(0, 1000)) + ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 4)))
        try:
            req = requests.get(urls, headers=headers, timeout=2)
            content_type = str(req.headers['Content-Type'].split(';')[0].split('+')[0])
            if 'data:image' in urls:
                list_url[file_writing][urls] = ''
            elif 'css' in content_type or 'image' in content_type:
                url = urls
                if '//' in url:
                    url = '/'.join(url.split('/')[3:])
                if url[0:1] == '/':
                    url = url[1:]

                paths = url.split('/')[:-1]
                file_name = url.split('/')[-1]
                all_path = ''
                for path in paths:
                    all_path = all_path + '/' + path
                    if all_path[:1] == '/':
                        all_path = all_path[1:]
                    if not os.path.exists(all_path):
                        os.mkdir(all_path)
                print(url)
                with open(f'{url}', 'wb') as file:
                    file.write(req.content)
                list_url[file_writing][urls] = url
                # with open(file, 'wb') as outfile:
                #     outfile.write(req.content)
                # if url_type == 1:
                #     html_new = Replace_01(urls, '/' + url, html_new)
                # else:
                # html_new = Replace_01(urls, url, html_new)

                # file = prename + content_type.split('/')[0] + '/' + prename + str(file_num) + '.' + \
                #        content_type.split('/')[1]
                # with open(file, 'wb') as outfile:
                #     outfile.write(req.content)
                # list_url[file_writing][urls] = file
            else:
                list_url[file_writing][urls] = ''
        except requests.exceptions.SSLError:
            pass
        except KeyError:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.TooManyRedirects:
            pass
        except requests.exceptions.InvalidURL:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.InvalidSchema:
            pass
        except requests.exceptions.ChunkedEncodingError:
            pass

    def PostCleaninHTML(html_new):
        print('---- Cleaning ----\n')
        html_new = re.sub(r'"http.*?"', '""', html_new, flags=re.M)
        html_new = re.sub(r"'http.*?'", "''", html_new, flags=re.M)
        print('clean - http')
        # html_new = re.sub(r'href="/.*?"', '', html_new, flags=re.M)
        html_new = re.sub(r'((srcset=[\"|\'])([\s\S]*?)[\"])', ' ', html_new, flags=re.M)
        html_new = re.sub(r'((alt=[\"|\'])([\s\S]*?)[\"])', ' ', html_new, flags=re.M)
        html_new = re.sub(r'action=".*?"', ' ', html_new, flags=re.M)
        html_new = re.sub(r'loading="lazy"', '', html_new, flags=re.M)
        # html_new = re.sub(r'href="/"', '', html_new, flags=re.M)
        # html_new = re.sub(r'href=""', '', html_new, flags=re.M)
        if rep_href_a == 1:
            html_new = re.sub(r'<a ', '<span ', html_new, flags=re.M)
            html_new = re.sub(r'</a>', '</span>', html_new, flags=re.M)
        html_new_src = re.findall(r"src=[\"|\'](.*?)[\"|\']", html_new, flags=re.M)
        for its in html_new_src:
            if ' ' in its:
                itss = its.split(' ')[0]
                # html_new = html_new.replace(its, itss)
                html_new = html_new.replace(its, itss)
        # html_new_href = re.findall(r"(href=[\"|\'].*?[\"|\'])", html_new, flags=re.M)
        # for it in html_new_href:
        #     if prename not in it:
        #         # html_new = html_new.replace(it, '')
        #         if rep_href_a == 1:
        #             html_new = html_new.replace(it, '')
        #         else:
        #             html_new = html_new.replace(it, 'href="/"')

        link_rels = re.findall(r"(<link.*?>)", html_new, flags=re.M)
        for link in link_rels:
            if prename not in link:
                html_new = html_new.replace(link, '')
        while '\n\n' in html_new:
            html_new = html_new.replace('\n\n', '\n')

        return html_new

    def PreCleaninHTML(html_new):
        html_new = html_new.replace('&amp;', '&')
        html_new = html_new.replace('><', '>\n<')
        html_new = html_new.replace('&#x26;', '&')
        html_new = html_new.replace('&#38;', '&')
        html_new = html_new.replace('data-lazy-src', 'src')
        html_new = html_new.replace('data-src', 'src')
        html_new = html_new.replace('data-original', 'src')
        html_new = html_new.replace('data-srcset', 'src')
        html_new = html_new.replace('srcset', 'src')
        html_new = html_new.replace('data-bkimage', 'src')
        html_new = html_new.replace('data-dce-background-image-url', 'src')
        html_new = html_new.replace('crossorigin="anonymous"', '')
        print('---- Cleaning ----\n')
        html_new = re.sub(r"(<!--[\s\S]*?\n?[\s\S]*?-->)", '', html_new, flags=re.M)
        print('clean - comment')
        html_new = re.sub(r"<iframe[\s\S]*?>[\s\S]*?<\/iframe>", '', html_new, flags=re.M)
        print('clean - iframe')
        html_new = re.sub(r"<noscript[\s\S]*?>[\s\S]*?<\/noscript>", '', html_new, flags=re.M)
        print('clean - noscript')
        html_new = re.sub(r"<script[\s\S]*?>[\s\S]*?<\/script>", '', html_new, flags=re.M)
        print('clean - script')
        html_new = re.sub(r'onclick=".*?"', '', html_new, flags=re.M)
        html_new = re.sub(r'<meta.*?>', '', html_new, flags=re.M)
        html_new = re.sub(r'[\'|\"|\(](data:image.*?)[\'|\"|\)]', '', html_new, flags=re.M)
        return html_new

    def new_cleaning_html_file(string):
        string = re.sub(r"<noscript[\s\S]*?<\/noscript>", '', string, flags=re.M)
        string = re.sub(r"<script[\s\S]*?<\/script>", '', string, flags=re.M)
        string = re.sub(r"<iframe[\s\S]*?<\/iframe>", '', string, flags=re.M)
        # string = re.sub(r"http[\S]*?\"", '"', string, flags=re.M)
        # string = re.sub(r"http[\S]*?\'", "'", string, flags=re.M)
        string = re.sub(r"\<\!--[\s\S]*?\n?[\s\S]*?--\>", "", string, flags=re.M)
        string_href = re.findall(r"(http.*?\/\/.*?)[\"|\'|\)]", string, flags=re.M)
        for string_href_item in string_href:
            print(string_href_item)
            string = string.replace(string_href_item, '/')
        return string

    list_url = {}
    os.chdir(f'{chdir_path}') if os.path.exists(chdir_path) else os.mkdir(f'{chdir_path}')
    print('Print url for download')
    # user_input_url = 'https://sushikisen.com/'
    user_input_url = input()
    start_time = datetime.now()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36'
                             '(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    requests_url_input = requests.get(user_input_url, headers=headers)
    url_for_donload = user_input_url.split('/')
    url_for_donload = "/".join(url_for_donload[0:3]) + '/'
    filename = user_input_url.split('//')[1].split('/')[0]
    shutil.rmtree(filename) if os.path.exists(filename) else pass1()
    os.mkdir(filename)
    os.chdir('./' + filename)
    html_new = str(BeautifulSoup(requests_url_input.content, 'html.parser'))
    # html_new = PreCleaninHTML(html_new)

    # os.mkdir(prename + 'image')
    # os.mkdir(prename + 'text')

    hrefs3 = (re.findall(r"\"(.*?)\"", html_new, flags=re.M)) + (
        re.findall(r"'(.*?)'", html_new, flags=re.M))
    print(len(hrefs3))
    hrefs3_new = {}
    for hrefs3_item in hrefs3:
        if '.' in hrefs3_item and len(hrefs3_item) > 6:
            hrefs3_new[hrefs3_item] = ""

    print(len(hrefs3_new))
    hrefs2_list = []
    for item_hrefs3_new in hrefs3_new:
        hrefs2_list.append(item_hrefs3_new)
    hrefs2_list = sorted(hrefs2_list, key=len)
    hrefs2_list = list(reversed(hrefs2_list))
    threads = []
    list_url['index.html'] = {}
    new_hrefs2_list = []

    for url in hrefs2_list:
        url = url.replace('"', '')
        url = url.replace("'", '')
        if ' ' in url:
            url1 = url.split(' ')[0]
        else:
            url1 = url
        url_n = ReplaseUrl(url_for_donload, url1)
        new_hrefs2_list.append(url_n)
        if url in html_new:
            print('\nREPLACE - OK')
        html_new = html_new.replace(url, url_n)
        print(url)
        print(url_n)

    for url in new_hrefs2_list:
        t = threading.Thread(target=SaveUrl, args=(url, 'index.html'))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(list_url['index.html'])

    # with open('2.html', 'w') as file1:
    #     file1.write(html_new)

    for img_path in list_url['index.html']:
        print(img_path)
        print(list_url['index.html'][img_path])
        if img_path in html_new:
            print('REPLACE --- OK')
        else:
            print('REPLACE --- NO')
        html_new = html_new.replace(img_path, list_url['index.html'][img_path])

    # with open('3.html', 'w') as file1:
    #     file1.write(html_new)

    # hrefs3 = (re.findall(r"href=\"(.*?)[\"|\']", html_new, flags=re.M)) + (
    #     re.findall(r"url\((.*?)\)", html_new, flags=re.M)) + (
    #              re.findall(r"src=[\"|\'](.*?)[\"|\']", html_new, flags=re.M))
    # for url_orig in hrefs3:
    #     if prename not in url_orig and len(url_orig) > 2:
    #         html_new = html_new.replace(url_orig, '')

    # html_new = PostCleaninHTML(html_new)
    html_new = new_cleaning_html_file(html_new)
    while '\n\n' in html_new:
        html_new = html_new.replace('\n\n', '\n')
    with open('index.html', 'w') as file_html:
        file_html.write(html_new)

    print('\n---- ' + filename + ' ----\n')
    print('work time download - ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    Start()
