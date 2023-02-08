import threading
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
# uc.TARGET_VERSION = 109
chdir_path = 'test-selen'
pagemod = 0  # 1 - full page site
windows_mod = 1  # 1 - open in windows,0 - dont open windows
log_mod = 1  # 1-log ||| 0 - nolog
req_verif = 0  # 1-no verife
js_download = 0  # 1 - download java script ||| 0 - no script
all_list = {}
clean_brand = 0
now = datetime.now()
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}


def start():
    def pass1():
        pass

    print('print url')
    first_url = input()
    print('go')
    options = uc.ChromeOptions()
    options.add_argument(f"--incognito")
    if windows_mod == 1:
        options.add_argument(f"--window-size={random.randint(1000, 1500)},{random.randint(600, 1000)}")
        options.add_argument("--disable-extensions")
    elif windows_mod == 0:
        options.add_argument("--headless")
    options.add_argument(f'--user-agent={headers}')
    print('1')
    # driver = uc.Chrome(options=options, executable_path='chromedriver/', desired_capabilities={'version': '110.0.5481.30'})
    # driver = uc.Chrome(options=options, desired_capabilities={'version': '109.0.5414.119'})
    # driver = uc.Chrome('chromedriver.exe', options=options)
    driver = uc.Chrome(options=options)
    # driver = uc.Chrome(executable_path='chromedriver')
    print('0')
    driver.get(first_url)
    if windows_mod == 1:
        print('type random key')
        input()
    elif windows_mod == 0:
        pass
    main_page = driver.page_source
    driver.quit()
    start_time = datetime.now()
    pass1() if os.path.exists(chdir_path) else os.mkdir(f'{chdir_path}')
    os.chdir(f'{chdir_path}')

    def replace_str_in_html(old_str, new_str, orig_str):
        # print(f"[first pattern]:  {old_str}")
        # print(f"[second pattern]: {new_str}")
        if old_str in orig_str:
            orig_str = orig_str.replace(old_str, new_str)
            # print('[REPLACE - OK]')
        else:
            # print('[REPLACE - ERROR 1]')
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

    def save_content_on_url(url_for_donload, urls):
    # def save_content_on_url(url_for_donload, urls, url, html_new, url_type):
        urls = urls.replace('"', '')
        urls = urls.replace("'", "")
        urls = urls.split(' ')[0]
        # print(urls)
        url_down = replace_url_to_download(url_for_donload, urls)
        # print(url_down)
        try:
            req = requests.get(url_down, headers=headers, timeout=2)
            content_type = str(req.headers['Content-Type'].split(';')[0].split('+')[0])
            # print(f"[Content-Type]: {content_type}")

            if 'data:image' in urls:
                all_list[urls]['replaced'] = ''
                all_list[urls]['type'] = False
                # print(f"[data:image DLT]")

            elif 'css' in content_type or 'image' in content_type:
                url = url_down.split('?')[0]
                if '//' in url:
                    url = '/'.join(url.split('/')[3:])
                if url[0:1] == '/':
                    url = url[1:]

                paths = '/'.join(url.split('/')[:-1])
                file_name = url.split('/')[-1]
                # print(url)
                # print(f"[path]: {paths}")
                # print(f"[file_name]: {file_name}")
                # if file_name.lower() != 'css':
                #     if len(file_name) >= 2:
                #         if len(paths) >= 2:
                #             try:
                #                 os.makedirs(paths)
                #             except FileExistsError:
                #                 pass
                #         if 'webp' in content_type:
                #             url = ('.'.join(url.split('.')[:-1])) + '.png'
                #             image = Image.open(BytesIO(req.content))
                #             image.save(f'{url}', format='png')
                #         else:
                #             with open(f'{url}', 'wb') as file:
                #                 file.write(req.content)
                all_list[urls]['replaced'] = url
                all_list[urls]['type'] = True
                all_list[urls]['content'] = req.content
                all_list[urls]['file_name'] = file_name
                all_list[urls]['paths'] = paths
                all_list[urls]['content_type'] = content_type

            else:
                print('[INVALID TYPE FILE]')
                all_list[urls]['replaced'] = ''
                all_list[urls]['type'] = False
        except requests.exceptions.SSLError:
            print('[SSL ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False
        except KeyError:
            print('[KeyError ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False
        except requests.exceptions.ConnectionError:
            print('[requests.exceptions.ConnectionError ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False
        except requests.exceptions.TooManyRedirects:
            print('[requests.exceptions.TooManyRedirects ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False
        except requests.exceptions.InvalidURL:
            print('[requests.exceptions.InvalidURL ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False
        except requests.exceptions.ReadTimeout:
            print('[requests.exceptions.ReadTimeout ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False
        except requests.exceptions.InvalidSchema:
            print('[requests.exceptions.InvalidSchema ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False
        except requests.exceptions.ChunkedEncodingError:
            print('[requests.exceptions.ChunkedEncodingError ERROR]')
            all_list[urls]['replaced'] = ''
            all_list[urls]['type'] = False

    def start_pars_html():
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

        # if pagemod == 1:
        #     hrefs = (re.findall(r"href=\"(.*?)[\"|\']", html_new, flags=re.M)) + (
        #         re.findall(r"url\((.*?)\)", html_new, flags=re.M)) + (
        #                 # re.findall(r"url\([\'|\"](.*?)[\'|\"]\)", html_new, flags=re.M)) + (
        #                 re.findall(r"src=[\"|\'](.*?)[\"|\']", html_new, flags=re.M))
        # else:
        #     hrefs = (re.findall(r"link.*?href=\"(.*?)[\"|\']", html_new, flags=re.M)) + (
        #         # re.findall(r"url[\'|\"|\(](.*?)[\'|\"|\)]", html_new, flags=re.M)) + (
        #         re.findall(r"url\((.*?)\)", html_new, flags=re.M)) + (
        #                 re.findall(r"src=[\"|\'](.*?)[\"|\']", html_new, flags=re.M))
        # hrefs = [el for el, _ in groupby(hrefs)]
        # hrefs2_list = hrefs
        # print('[LEN HREF]')
        # for href1 in hrefs:
        #     if len(href1) <= 6:
        #         hrefs2_list.remove(href1)
        # hrefs2_list = sorted(hrefs2_list, key=len)
        # hrefs2_list = list(reversed(hrefs2_list))

        href_in_html = soup.find_all(href=True)
        for href_in_html_item in href_in_html:
            # print(href_in_html_item['href'])
            all_list[href_in_html_item['href']] = {'replaced': '',
                                                   'type': '',
                                                   'content': '',
                                                   'file_name': '',
                                                   'content_type': '',
                                                   'paths': ''}
        src_in_html = soup.find_all(src=True)
        for src_in_html_item in src_in_html:
            # print(src_in_html_item['src'])
            all_list[src_in_html_item['src']] = {'replaced': '',
                                                 'type': '',
                                                 'content': '',
                                                 'file_name': '',
                                                 'content_type': '',
                                                 'paths': ''}
        print(len(href_in_html) + len(src_in_html))

        print('\ndownload hrefs:')
        threads = []
        for url_i in all_list:
            t = threading.Thread(target=save_content_on_url, args=(url_for_donload, url_i))
            # t = threading.Thread(target=save_content_on_url, args=(url_for_donload, url_i, html_new, url_type))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # print(all_list)
        print('REPALCE IN HTML')
        for item in all_list:
            item_replaced = all_list[item]['replaced']
            item_type = all_list[item]['type']
            print('\n|-------|||-------|\n'+item)
            print(item_replaced)
            print(item_type)
            # print(item_content)


            if not item_type:
                html_new = html_new.replace(item, item_replaced)
            elif item_type:
                html_new = html_new.replace(item, item_replaced)
                item_content = all_list[item]['content']
                item_file_name = all_list[item]['file_name']
                item_content_type = all_list[item]['content_type']
                item_paths = all_list[item]['paths']
                print(item_file_name)
                print(item_content_type)
                print(item_paths)
                if len(item_file_name) >= 2:
                    if len(item_paths) >= 2:
                        try:
                            os.makedirs(item_paths)
                        except FileExistsError:
                            pass
                    if 'webp' in item_content_type:
                        item_replaced = ('.'.join(item_replaced.split('.')[:-1])) + '.png'
                        image = Image.open(BytesIO(item_content))
                        image.save(f'{item_replaced}', format='png')
                    else:
                        with open(f'{item_replaced}', 'wb') as file:
                            file.write(item_content)
        # sorted_all_list = sorted(all_list, key=len, reverse=True)
        # print(sorted_all_list)
        # for item1 in sorted_all_list:
        #     print(item1['replaced'])

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
