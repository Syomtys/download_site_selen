from io import BytesIO
import undetected_chromedriver.v2 as uc
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
from PIL import Image

from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable

service_object = Service(binary_path)

chdir_path = 'test-selen'
pagemod = 0  # 1 - full page site
log_mod = 1  # 1-log ||| 0 - nolog
req_verif = 0  # 1-no verife
js_download = 0  # 1 - download java script ||| 0 - no script
clean_brand = 0
now = datetime.now()
url_type = 0
filenum = 1
file_num = 0
page_num = 0
prename = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 8)))
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}


def start():
    def pass1():
        pass

    print('print url')
    first_url = input()
    print('go')
    options = uc.ChromeOptions()
    print('5')
    options.add_argument(f"--incognito")
    print('4')
    options.add_argument(f"--window-size={random.randint(1000, 1500)},{random.randint(600, 1000)}")
    print('3')
    options.add_argument("--disable-extensions")
    print('2')
    options.add_argument(f'--user-agent={headers}')
    print('1')
    driver = uc.Chrome(options=options, service=service_object)
    print('0')
    driver.get(first_url)
    print('type random key')
    input()
    main_page = driver.page_source
    driver.quit()
    start_time = datetime.now()
    pass1() if os.path.exists(chdir_path) else os.mkdir(f'{chdir_path}')
    os.chdir(f'{chdir_path}')

    def replace_str_in_html(old_str, new_str, orig_str):
        print(f"[first pattern]:  {old_str}")
        print(f"[second pattern]: {new_str}")
        if old_str in orig_str:
            orig_str = orig_str.replace(old_str, new_str)
            print('[REPLACE - OK]')
        else:
            print('[REPLACE - ERROR 1]')
            old_str = old_str.replace(' ', '')
        return orig_str

    def pass1():
        pass

    def replace_url_to_download(replace_url, href_file):
        href_file = href_file.replace('///', '//')
        href_file = href_file.replace('"', '')
        href_file = href_file.replace("'", '')
        href_file = href_file.replace("\\", '')
        if href_file[0:2] == '//':
            href_file = 'https:' + href_file
        elif href_file[0:4] == 'http':
            pass
        else:
            if href_file[0:9] == '../../../':
                href_file = replace_url + href_file[9:]
            if href_file[0:6] == '../../':
                href_file = replace_url + href_file[6:]
            elif href_file[0:4] == '././':
                href_file = replace_url + href_file[4:]
            elif href_file[0:3] == '../':
                href_file = replace_url + href_file[3:]
            elif href_file[0:1] == '/':
                href_file = replace_url + href_file[1:]
            elif href_file[0:1] == ' ':
                href_file = replace_url + href_file[1:]
            elif href_file[0:2] == './':
                href_file = replace_url + href_file[2:]
            elif href_file[0:3] == '/-/':
                href_file = replace_url + href_file[3:]
            else:
                href_file = replace_url + href_file
        return href_file

    def cleaning_html(html_new):
        print('---- Cleaning ----\n')
        html_new = re.sub(r"((http(.*?))([\w|\/]))", '', html_new, flags=re.M)
        print('clean - http')
        html_new = re.sub(r'"://.*?"', '/', html_new, flags=re.M)
        html_new = re.sub(r'((srcset=[\"|\'])([\s\S]*?)[\"])', ' ', html_new, flags=re.M)
        html_new = re.sub(r'((alt=[\"|\'])([\s\S]*?)[\"])', ' ', html_new, flags=re.M)
        html_new = re.sub(r'loading="lazy"', '', html_new, flags=re.M)
        html_new = re.sub(r'href="/"', '', html_new, flags=re.M)
        html_new = re.sub(r'href=""', '', html_new, flags=re.M)
        html_new = re.sub(r'<a ', '<span ', html_new, flags=re.M)
        html_new = re.sub(r'</a>', '</span>', html_new, flags=re.M)
        return html_new

    def save_content_on_url(url_for_donload, urls, html_new, url_type):
        global file_num, page_num
        urls = urls.replace('"', '')
        urls = urls.replace("'", "")
        urls = urls.split(' ')[0]
        print(urls)
        url_down = replace_url_to_download(url_for_donload, urls)
        print(url_down)
        # url_down = replace_url_to_download(url_for_donload, urls)
        file_num += 1
        # print('\n')
        # print(f'[first url]: {urls}')
        # print(f'[second url]: {url_down}')
        try:
            req = requests.get(url_down, headers=headers, timeout=2)
            content_type = str(req.headers['Content-Type'].split(';')[0].split('+')[0])
            print(f"[Content-Type]: {content_type}")

            if 'data:image' in urls:
                html_new = replace_str_in_html(urls, '', html_new)
                print(f"[data:image DLT]")

            elif 'css' in content_type or 'image' in content_type:
                # elif 'css' in content_type or 'image' in content_type or 'application/javascript' in content_type:
                #     if 'application/javascript' in content_type:
                #         file = prename + 'text' + '/' + prename + str(file_num) + '.' + content_type.split('/')[1]
                #     else:
                #         file = prename + content_type.split('/')[0] + '/' + prename + str(file_num) + '.' + content_type.split('/')[1]
                #     print(f"[save fail patch]: {file}")
                url = url_down.split('?')[0]
                if '//' in url:
                    url = '/'.join(url.split('/')[3:])
                if url[0:1] == '/':
                    url = url[1:]

                paths = '/'.join(url.split('/')[:-1])
                file_name = url.split('/')[-1]
                print(url)
                print(f"[path]: {paths}")
                print(f"[file_name]: {file_name}")
                if file_name.lower() != 'css':
                    if len(file_name) >= 2:
                        if len(paths) >= 2:
                            try:
                                os.makedirs(paths)
                            except FileExistsError:
                                pass
                        if 'webp' in content_type:
                            url = ('.'.join(url.split('.')[:-1])) + '.png'
                            image = Image.open(BytesIO(req.content))
                            image.save(f'{url}', format='png')
                        else:
                            with open(f'{url}', 'wb') as file:
                                file.write(req.content)
                html_new = replace_str_in_html(urls, url, html_new)
            else:
                print('[INVALID TYPE FILE]')
                html_new = replace_str_in_html(urls, '', html_new)
        except requests.exceptions.SSLError:
            print('[SSL ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        except KeyError:
            print('[KeyError ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        except requests.exceptions.ConnectionError:
            print('[requests.exceptions.ConnectionError ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        except requests.exceptions.TooManyRedirects:
            print('[requests.exceptions.TooManyRedirects ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        except requests.exceptions.InvalidURL:
            print('[requests.exceptions.InvalidURL ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        except requests.exceptions.ReadTimeout:
            print('[requests.exceptions.ReadTimeout ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        except requests.exceptions.InvalidSchema:
            print('[requests.exceptions.InvalidSchema ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        except requests.exceptions.ChunkedEncodingError:
            print('[requests.exceptions.ChunkedEncodingError ERROR]')
            html_new = replace_str_in_html(urls, '', html_new)
        return html_new

    def start_pars_html():
        global filenum, url_type
        url = first_url
        url_for_donload = url.split('/')
        url_for_donload = "/".join(url_for_donload[0:3]) + '/'
        filename = url.split('//')[1].split('/')[0]
        print(url_for_donload)
        print('\n---- ' + filename + ' ----\n')
        shutil.rmtree(filename) if os.path.exists(filename) else pass1()
        os.mkdir(filename)
        os.chdir(filename)
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
        html_new = re.sub(r'[\'|\"|\(](data:image.*?)[\'|\"|\)]', '', html_new, flags=re.M)


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
        # print('[REPLACE HREFS TO SPACE]')
        # for href1 in hrefs:
        #     if ' ' in href1:
        #         href2 = href1.split(' ')[0]
        #         html_new = replace_str_in_html(href1, href2, html_new)
        #         hrefs2_list.remove(href1)
        #         hrefs2_list.append(href2)
        print('[LEN HREF]')
        for href1 in hrefs:
            if len(href1) <= 6:
                hrefs2_list.remove(href1)

        hrefs2_list = sorted(hrefs2_list, key=len)
        hrefs2_list = list(reversed(hrefs2_list))
        print('\ndownload hrefs:')
        for url_i in hrefs2_list:
            print(f"\n[{str(hrefs2_list.index(url_i))}/{str(len(hrefs2_list))}]")
            html_new = save_content_on_url(url_for_donload, url_i, html_new, url_type)

        html_new = cleaning_html(html_new)

        html_new = html_new.replace('</title>',
                                    f'</title>\n<meta charset="utf-8"/>')

        while '\n\n' in html_new:
            html_new = html_new.replace('\n\n', '\n')

        with open('index.html', 'w', encoding='UTF-8') as html_index:
            html_index.write(html_new)

        print('\n---- ' + filename + ' ----\n')

    start_pars_html()
    print('\nall work time - ' + str(datetime.now() - now))
    print('\nwork time download - ' + str(datetime.now() - start_time))


if __name__ == "__main__":
    start()
