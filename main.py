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

# service_object = Service(binary_path)
# driver = webdriver.Chrome(service=service_object)

pagemod = 0  # 1 - full page site
log_mod = 1  # 1-log ||| 0 - nolog
req_verif = 0  # 1-no verife
js_download = 0  # 1 - download java script ||| 0 - no script
clean_brand = 0

url_type = 0
trash = []
filenum = 1
file_num = 0
page_num = 0
prename = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 8)))
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}


def Start():
    print('print url')
    first_url = input()
    options = uc.ChromeOptions()
    options.add_argument(f"--incognito")#incognito
    options.add_argument(f"--window-size={random.randint(1000, 1500)},{random.randint(600, 1000)}")
    options.add_argument("--disable-extensions")
    driver = uc.Chrome(options=options)
    driver.get(first_url)
    print('type random key')
    input()
    main_page = driver.page_source
    driver.quit()


    with open('brand_list_3.json', 'r') as f:
        list_brands = json.load(f)

    os.chdir('./vites')

    def pass1():
        pass

    def ReplaseUrl(ReplaceUrl, HrefFile):
        HrefFile = HrefFile.replace('///', '//')
        HrefFile = HrefFile.replace('"', '')
        HrefFile = HrefFile.replace("'", '')
        if HrefFile[0:2] == '//':
            HrefFile = 'https:' + HrefFile
        elif HrefFile[0:4] == 'http':
            pass
        else:
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
        return HrefFile

    def CleaninHTML(html_new):
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
        # hrefsinhtml = re.findall(r"(href=[\"|\'].*?[\"|\'])", html_new, flags=re.M)
        # for numh in range(len(hrefsinhtml)):
        #     if str(hrefsinhtml[numh][-4:]).lower() == 'tml"':
        #         if pagemod == 1:
        #             print('it is html - ' + str(hrefsinhtml[numh]))
        #             html_new = html_new.replace(str(hrefsinhtml[numh]), f'href="{prename + str(numh)}page.html"')
        #         else:
        #             html_new = html_new.replace(str(hrefsinhtml[numh]), 'href="/"')
        #             print('replace href - ' + str(hrefsinhtml[numh]))
        #     elif str(hrefsinhtml[numh][6:9]) == prename[0:3]:
        #         print('it is clone - ' + str(hrefsinhtml[numh]))
        #     else:
        #         html_new = html_new.replace(str(hrefsinhtml[numh]), 'href="/"')
        #         print('replace href - ' + str(hrefsinhtml[numh]))
        final_str = re.sub(r"((http(\S+))([\w|\/]))", '', html_new, flags=re.M)
        print('clean - http')
        final_str = re.sub(r'href="/.*?"', '', final_str, flags=re.M)
        final_str = re.sub(r'onclick=".*?"', '', final_str, flags=re.M)
        final_str = re.sub(r'((data:image)\S+[\"])', '"', final_str, flags=re.M)
        final_str = re.sub(r'((srcset=[\"|\'])([\s\S]*?)[\"])', ' ', final_str, flags=re.M)
        final_str = re.sub(r'((alt=[\"|\'])([\s\S]*?)[\"])', ' ', final_str, flags=re.M)
        final_str = re.sub(r'loading="lazy"', '', final_str, flags=re.M)
        final_str = re.sub(r'href="/"', '', final_str, flags=re.M)
        final_str = re.sub(r'href=""', '', final_str, flags=re.M)
        final_str = re.sub(r'<a ', '<span ', final_str, flags=re.M)
        final_str = re.sub(r'/a>', '/span>', final_str, flags=re.M)
        html_new = final_str
        return html_new

    async def SaveUrl(url_for_donload, urls, html_new, url_type):
        global file_num, trash, page_num
        url_down = ReplaseUrl(url_for_donload, urls)
        file_num += 1
        print('\n')
        print(f'[first url]: {urls}')
        print(f'[second url]: {url_down}')
        try:
            req = requests.get(url_down, headers=headers, timeout=2)
            content_type = str(req.headers['Content-Type'].split(';')[0].split('+')[0])
            print(f"[Content-Type]: {content_type}")
            if 'css' in content_type or 'image' in content_type:
                print(f"[save fail patch]: {prename + content_type.split('/')[0] + '/' + prename + str(file_num) + '.' + content_type.split('/')[1]}")
                with open(prename + content_type.split('/')[0] + '/' + prename + str(file_num) + '.' +
                          content_type.split('/')[1], 'wb') as outfile:
                    outfile.write(req.content)
                    if url_type == 1:
                        html_new = html_new.replace(urls, '/' + prename + content_type.split('/')[0] + '/' + prename + str(
                        file_num) + '.' + content_type.split('/')[1])
                    else:
                        html_new = html_new.replace(urls, prename + content_type.split('/')[0] + '/' + prename + str(
                                                        file_num) + '.' + content_type.split('/')[1])
            elif ('html' in content_type) and (filename in url_down) and (int(len(urls)) > 3):
                if pagemod == 1:
                    print(f'[this is page]: pagemod = 1')
                    # print(f"[Content-Type]: {content_type}")
                    # print(f'[second url]: {url_down}')
                    print(f"[save fail patch]: {prename+str(page_num)+'page/index.html'}")
                    page_num += 1
                    html_new = html_new.replace(urls, '/'+prename+str(page_num)+'page/', 1)
                    # html_new = re.sub(url_start, '/'+prename+str(page_num)+'page/', html_new, count=1, flags=re.M)
                    os.mkdir(prename+str(page_num)+'page')
                    pg_req = requests.get(url_down, headers=headers)
                    soup = BeautifulSoup(pg_req.content, 'html.parser')
                    pg_req = str(soup)
                    pg_req = re.sub(r"href=[\"|\'](.*?)[\"|\']",'/', pg_req, flags=re.M)
                    pg_req = re.sub(r"scr=[\"|\'](.*?)[\"|\']",'/', pg_req, flags=re.M)
                    pg_req = CleaninHTML(pg_req)
                    with open(prename+str(page_num)+'page/index.html', 'w') as pg_file:
                        pg_file.write(pg_req)
                else:
                    print(f'[this is page]: pagemod = 0')
            else:
                print('[INVALID TYPE FILE]')
        except requests.exceptions.SSLError:
            print('[SSL ERROR]')
        except KeyError:
            print('[KeyError ERROR]')
        except requests.exceptions.ConnectionError:
            print('[requests.exceptions.ConnectionError ERROR]')
        except requests.exceptions.TooManyRedirects:
            print('[requests.exceptions.TooManyRedirects ERROR]')
        except requests.exceptions.InvalidURL:
            print('[requests.exceptions.InvalidURL ERROR]')
        except requests.exceptions.ReadTimeout:
            print('[requests.exceptions.ReadTimeout ERROR]')
        html_new = html_new.replace(urls, '/')
        return html_new

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

    def StartParsHTML():
        global filenum, url, url_for_donload, filename, html_new, respown, soup, pagenum, url_type
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
        html_new = html_new.replace('crossorigin="anonymous"', '')

        os.mkdir(prename + 'image')
        os.mkdir(prename + 'text')

        print('\ndownload hrefs:') if log_mod == 1 else pass1()
        if pagemod == 1:
            hrefs = (re.findall(r"href=\"(\S+)[\"|\']", html_new, flags=re.M)) + (
                re.findall(r"url[\(]([\s\S]*?)[\)]", html_new, flags=re.M)) + (
                        re.findall(r"src=[\"|\'](\S+)[\"|\']", html_new, flags=re.M)) + (
                        re.findall(r"data-dce-background-image-url=(\S+)[\"|']", html_new, flags=re.M))
        else:
            hrefs = (re.findall(r"link.*?href=\"(\S+)[\"|\']", html_new, flags=re.M)) + (
                re.findall(r"url[\(]([\s\S]*?)[\)]", html_new, flags=re.M)) + (
                        re.findall(r"src=[\"|\'](\S+)[\"|\']", html_new, flags=re.M)) + (
                        re.findall(r"data-dce-background-image-url=(\S+)[\"|']", html_new, flags=re.M))
        hrefs = [el for el, _ in groupby(hrefs)]
        hrefs2_list = hrefs
        for href1 in hrefs:
            if ' ' in href1:
                href2 = href1.split(' ')[0]
                html_new = html_new.replace(href1, href2)
                hrefs2_list.remove(href1)
                hrefs2_list.append(href2)
        # hrefs_list =[]
        # for i1 in hrefs:
        #     hrefs_list.append(ReplaseUrl(url_for_donload, i1))
        hrefs2_list = sorted(hrefs2_list, key=len)
        hrefs2_list = list(reversed(hrefs2_list))
        for url_i in hrefs2_list:
            html_new = asyncio.run(SaveUrl(url_for_donload, url_i, html_new, url_type))
            # html_new = SaveUrl(url_for_donload, url_i, html_new)
        # hrefs_post = re.findall(r"href=\"(\S+)[\"]", html_new, flags=re.M)
        # for hrefs_post_item in hrefs_post:
        #     if prename not in hrefs_post_item:
        #         html_new = html_new.replace(hrefs_post_item, '')
        url_type+=1
        print('\ndownload file in css:') if log_mod == 1 else pass1()
        for css_file in os.listdir(prename + 'text'):
            if 'DS_Store' not in css_file:
                print(css_file)
                try:
                    with open(prename + 'text/'+css_file, 'r') as file_css:
                        text_css = file_css.read()
                    url_in_css = re.findall(r"url[\(]([\s\S]*?)[\)]", text_css, flags=re.M)
                    for url_in_css_item in url_in_css:
                        text_css = asyncio.run(SaveUrl(url_for_donload, url_in_css_item, text_css, url_type))
                        # text_css = text_css.replace('url(', 'url(/')
                        text_css = text_css.replace(';', ';\n')
                        text_css = text_css.replace('}', '}\n\n')
                        text_css = text_css.replace('{', '{\n')
                        while '\n\n' in text_css:
                            text_css = text_css.replace('\n\n', '\n')
                    with open(prename + 'text/'+css_file, 'w') as file_css_2:
                        file_css_2.write(text_css)
                except UnicodeDecodeError:
                    print('UnicodeDecodeError: [ERROR]')
        print(trash)
        for i in trash:
            if len(i) >= 2:
                print('trash -')
                print(i)
                html_new = html_new.replace(i, '/')

        html_new = CleaninHTML(html_new)

        while '\n\n' in html_new:
            html_new = html_new.replace('\n\n', '\n')

        if clean_brand == 1:
            html_new = Clean_Brands(html_new)

        with open('index.html', 'w') as html_index:
            html_index.write(html_new)
        print('\n---- ' + filename + ' ----\n')

    StartParsHTML()


if __name__ == "__main__":
    Start()