import asyncio
import undetected_chromedriver.v2 as uc
import json
import os
import requests
from bs4 import BeautifulSoup
import shutil
import re
import random
from random import choice
from string import ascii_uppercase
from itertools import groupby
from datetime import datetime
import threading

# setting
# ----

rep_href_a = 1 # clean and replace <a href = "">

# ----
# ----
def Start():
    now = datetime.now()
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    print('print url')
    first_url = input()
    print('go')
    options = uc.ChromeOptions()
    options.add_argument(f"--incognito")#incognito
    options.add_argument(f"--window-size={random.randint(1000, 1500)},{random.randint(600, 1000)}")
    options.add_argument("--disable-extensions")
    options.add_argument(f'--user-agent={headers}')
    print('1')
    driver = uc.Chrome(options=options)
    print('0')
    driver.get(first_url)
    print('type random key')
    input()
    main_page = driver.page_source
    driver.quit()

    start_time = datetime.now()

    with open('brand_list_3.json', 'r') as f:
        list_brands = json.load(f)
    os.chdir('./vites')

    def StartParsHTML():
        list_url = {}
        pagemod = 0  # 1 - full page site
        log_mod = 1  # 1-log ||| 0 - nolog
        req_verif = 0  # 1-no verife
        js_download = 0  # 1 - download java script ||| 0 - no script
        clean_brand = 0
        url_type = 0
        filenum = 1
        # file_num = 0
        page_num = 0
        prename = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 8)))

        def Replace_01(old_str, new_str, orig_str, text, url_for_donload):
            print(f"[{text}][first pattern]:{old_str}")
            print(f"[{text}][second pattern]:{new_str}")
            if old_str in orig_str:
                orig_str = orig_str.replace(old_str, new_str)
                print('[REPLACE - OK]\n')
            else:
                if url_for_donload in old_str:
                    old_str = old_str.replace(url_for_donload, '')
                    if old_str in orig_str:
                        orig_str = orig_str.replace(old_str, new_str)
                        print(f"[{text}][replace pattern]:{old_str}")
                        print('[REPLACE 1 - OK]\n')
                    else:
                        print('[REPLACE - ERROR 2]\n')
                else:
                    print('[REPLACE - ERROR 1]\n')
            return orig_str

        def pass1():
            pass

        def ReplaseUrl(ReplaceUrl, HrefFile):
            print(HrefFile)
            HrefFile = HrefFile.replace('///', '//')
            HrefFile = HrefFile.replace('"', '')
            HrefFile = HrefFile.replace("'", '')
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
            print(HrefFile)
            return HrefFile

        def CleaninHTML(html_new):
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
                    html_new = Replace_01(its, itss, html_new, 'split_src', url_for_donload)
            html_new_href = re.findall(r"(href=[\"|\'].*?[\"|\'])", html_new, flags=re.M)
            for it in html_new_href:
                if prename not in it:
                    # html_new = html_new.replace(it, '')
                    if rep_href_a == 1:
                        html_new = Replace_01(it, '', html_new, 'cleaning_html', url_for_donload)
                    else:
                        html_new = Replace_01(it, 'href="/"', html_new, 'cleaning_html', url_for_donload)

            link_rels = re.findall(r"(<link.*?>)", html_new, flags=re.M)
            for link in link_rels:
                if prename not in link:
                    html_new = html_new.replace(link, '')
            while '\n\n' in html_new:
                html_new = html_new.replace('\n\n', '\n')

            return html_new

        def SaveUrl(url_for_donload, urls, url_type, file_writing):
            # print(file_writing)
            global page_num
            file_num = str(random.randint(0, 1000)) + ''.join(
                choice(ascii_uppercase) for i in range(random.randint(3, 4)))
            urls = urls.replace('"', '')
            urls = urls.replace("'", "")
            # urls = urls.split(' ')[0]
            # url_down = ReplaseUrl(url_for_donload, urls)
            # list_first_second_url[urls] = url_down
            try:
                req = requests.get(urls, headers=headers, timeout=2)
                content_type = str(req.headers['Content-Type'].split(';')[0].split('+')[0])
                if 'data:image' in urls:
                    list_url[file_writing][urls] = ''
                elif 'css' in content_type or 'image' in content_type:
                    # elif 'css' in content_type or 'image' in content_type or 'application/javascript' in content_type:
                    file = prename + content_type.split('/')[0] + '/' + prename + str(file_num) + '.' + \
                           content_type.split('/')[1]
                    # print(f"[save fail patch]: {file}")
                    with open(file, 'wb') as outfile:
                        outfile.write(req.content)
                        if url_type == 1:
                            list_url[file_writing][urls] = '/' + file
                        else:
                            list_url[file_writing][urls] = file

                elif ('html' in content_type) and (filename in urls) and (int(len(urls)) > 3):
                    if pagemod == 1:
                        # print(f'[this is page]: pagemod = 1')
                        # print(f"[save fail patch]: {prename+str(page_num)+'page/index.html'}")
                        page_num += 1
                        # html_new = html_new.replace(urls, '/'+prename+str(page_num)+'page/', 1)
                        # html_new = re.sub(url_start, '/'+prename+str(page_num)+'page/', html_new, count=1, flags=re.M)
                        os.mkdir(prename + str(page_num) + 'page')
                        pg_req = requests.get(urls, headers=headers)
                        soup = BeautifulSoup(pg_req.content, 'html.parser')
                        pg_req = str(soup)
                        pg_req = re.sub(r"href=[\"|\'](.*?)[\"|\']", '/', pg_req, flags=re.M)
                        pg_req = re.sub(r"scr=[\"|\'](.*?)[\"|\']", '/', pg_req, flags=re.M)
                        pg_req = CleaninHTML(pg_req)
                        with open(prename + str(page_num) + 'page/index.html', 'w') as pg_file:
                            pg_file.write(pg_req)
                    else:
                        # print(f'[this is page]: pagemod = 0')
                        pass
                else:
                    # print('[INVALID TYPE FILE]')
                    list_url[file_writing][urls] = ''
            except requests.exceptions.SSLError:
                pass
                # print('[SSL ERROR]')
            except KeyError:
                pass
                # print('[KeyError ERROR]')
            except requests.exceptions.ConnectionError:
                pass
                # print('[requests.exceptions.ConnectionError ERROR]')
            except requests.exceptions.TooManyRedirects:
                pass
                # print('[requests.exceptions.TooManyRedirects ERROR]')
            except requests.exceptions.InvalidURL:
                pass
                # print('[requests.exceptions.InvalidURL ERROR]')
            except requests.exceptions.ReadTimeout:
                pass
                # print('[requests.exceptions.ReadTimeout ERROR]')
            except requests.exceptions.InvalidSchema:
                pass
                # print('[requests.exceptions.InvalidSchema ERROR]')
            except requests.exceptions.ChunkedEncodingError:
                pass
                # print('[requests.exceptions.ChunkedEncodingError ERROR]')
            # html_new = Replace_01(urls, '', html_new)

            # return html_new

        def Clean_Brands(text):
            for brand in list_brands:
                pattern_replace = brand
                if pattern_replace in text:
                    if int(len(pattern_replace)) >= 6:
                        print('yes - ' + pattern_replace)
                        text = text.replace(pattern_replace.lower(), '')
                        text = text.replace(pattern_replace.upper(), '')
                        text = text.replace(pattern_replace.capitalize(), '')
                    else:
                        print('no - ' + pattern_replace)
            return text

        # global filenum, url, url_for_donload, filename, html_new, respown, soup, pagenum, url_type
        url = first_url
        url_for_donload = url.split('/')
        url_for_donload = "/".join(url_for_donload[0:3]) + '/'
        filename = url.split('//')[1].split('/')[0]
        print(url_for_donload)
        print('\n---- ' + filename + ' ----\n')
        shutil.rmtree(filename) if os.path.exists(filename) else pass1()
        os.mkdir(filename)
        os.chdir('./' + filename)
        soup = BeautifulSoup(main_page, 'html.parser')
        html_new = str(soup)
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
        if js_download != 1:
            html_new = re.sub(r"<script[\s\S]*?>[\s\S]*?<\/script>", '', html_new, flags=re.M)
            print('clean - script')
        html_new = re.sub(r"<noscript[\s\S]*?>[\s\S]*?<\/noscript>", '', html_new, flags=re.M)
        print('clean - noscript')
        html_new = re.sub(r'onclick=".*?"', '', html_new, flags=re.M)
        html_new = re.sub(r'<meta.*?>', '', html_new, flags=re.M)
        html_new = re.sub(r'[\'|\"|\(](data:image.*?)[\'|\"|\)]', '', html_new, flags=re.M)

        os.mkdir(prename + 'image')
        os.mkdir(prename + 'text')

        style_in_html = (re.findall(r"<style[\s\S]*?>([\s\S]*?)<\/style>", html_new, flags=re.M))
        html_new = re.sub(r'<style[\s\S]*?>([\s\S]*?)<\/style>', '', html_new, flags=re.M)
        css_style_text = ''
        for css_item in style_in_html:
            css_style_text = css_style_text+css_item
        with open(prename + 'text' + '/' + prename + 'style.css', 'w') as pg_file:
            pg_file.write(css_style_text)
        # for css_item in style_in_html:
        #     with open(prename + 'text' + '/' + prename + f'style{random.randint(1,99)}.css', 'w') as pg_file:
        #         pg_file.write(css_item)

        if pagemod == 1:
            hrefs = (re.findall(r"href=\"(.*?)[\"|\']", html_new, flags=re.M)) + (
                re.findall(r"url\((.*?)\)", html_new, flags=re.M)) + (
                # re.findall(r"url\([\'|\"](.*?)[\'|\"]\)", html_new, flags=re.M)) + (
                        re.findall(r"src=[\"|\'](.*?)[\"|\']", html_new, flags=re.M))
        else:
            hrefs = (re.findall(r"link.*?href=\"(.*?)[\"|\']", html_new, flags=re.M)) + (
                # re.findall(r"url[\'|\"|\(](.*?)[\'|\"|\)]", html_new, flags=re.M)) + (
                re.findall(r"url\((.*?)\)", html_new, flags=re.M)) + (
                        re.findall(r"src=[\"|\'](.*?)[\"|\']", html_new, flags=re.M))
        hrefs = [el for el, _ in groupby(hrefs)]
        hrefs2_list = hrefs
        print('[LEN HREF]')
        for href1 in hrefs:
            if len(href1) <= 6:
                hrefs2_list.remove(href1)
        hrefs2_list = sorted(hrefs2_list, key=len)
        hrefs2_list = list(reversed(hrefs2_list))

        print('\ndownload hrefs:')
        # with open('index.html','w') as htm:
        #     htm.write(html_new)
        threads = []
        list_first_second_url = {}
        list_url['index.html'] = {}
        new_hrefs2_list = []
        for url in hrefs2_list:
            url_n = ReplaseUrl(url_for_donload, url)
            new_hrefs2_list.append(url_n)
            html_new = html_new.replace(url, url_n)
        for url in new_hrefs2_list:
            t = threading.Thread(target=SaveUrl, args=(url_for_donload, url, url_type, 'index.html'))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        # with open('index.html','r') as htm:
        #     html_new = htm.read()

        # print('[DLT HREFS]')
        # hrefs_post = re.findall(r"href=\"\S+[\"]", html_new, flags=re.M)
        # for hrefs_post_item in hrefs_post:
        #     if prename not in hrefs_post_item:
        #         html_new = Replace_01(hrefs_post_item, '', html_new)


        url_type+=1
        print('\ndownload file in css:') if log_mod == 1 else pass1()
        list_css = os.listdir(prename + 'text')
        for css_file in list_css:
            if 'DS_Store' not in css_file:
                list_url[prename + 'text/' + css_file] = {}
                # print(f"\n[{str(list_css.index(css_file))}/{str(len(list_css))}]")
                # print(css_file)
                try:
                    with open(prename + 'text/'+css_file, 'r') as file_css:
                        text_css = file_css.read()
                    url_in_css = re.findall(r"url[\(]([\s\S]*?)[\)]", text_css, flags=re.M)

                    threads = []
                    for url_in_css_item in url_in_css:
                        t = threading.Thread(target=SaveUrl, args=(url_for_donload, url_in_css_item, url_type, prename + 'text/'+css_file))
                        threads.append(t)
                        t.start()
                    for t in threads:
                        t.join()
                    with open(prename + 'text/'+css_file, 'w') as file_css_2:
                        file_css_2.write(text_css)
                except UnicodeDecodeError:
                    print('UnicodeDecodeError: [ERROR]')

        with open('index.html', 'w') as html_index1:
            html_index1.write(html_new)

        # print(f'list_url - {list_url}')
        print('|||--------------------|||--------------------|||\n')
        for i1 in list_url:
            print(f'             -||- {i1} -||-')

            with open(i1 ,'r') as file_rep:
                text_file_rep = file_rep.read()

            for i in list_url[i1]:
                text_file_rep = Replace_01(str(i), str(list_url[i1][i]), text_file_rep, 'download_file', url_for_donload)
            # print(text_file_rep)
            with open(i1 ,'w') as file_rep1:
                file_rep1.write(text_file_rep)
        print('\n|||--------------------|||--------------------|||')
        with open('index.html', 'r') as html_index2:
            html_new = html_index2.read()

        html_new = CleaninHTML(html_new)

        html_new = html_new.replace('</title>',
                                    f'</title>\n<link href="{prename}text/{prename}style.css" rel="stylesheet" type="text/css"/>')
        html_new = html_new.replace('</title>',
                                    f'</title>\n<meta charset="utf-8"/>')

        if clean_brand == 1:
            html_new = Clean_Brands(html_new)

        with open('index.html', 'w', encoding='UTF-8') as html_index:
            html_index.write(html_new)

        print('\n---- ' + filename + ' ----\n')
        print('\nwork time download - ' + str(datetime.now() - start_time))


    StartParsHTML()
    print('\nall work time - ' + str(datetime.now() - now))

if __name__ == "__main__":
    Start()
