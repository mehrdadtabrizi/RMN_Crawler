from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict
import rmn_Parameters as Parameters
from urllib import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import time

def browser_open():
    driver = webdriver.Firefox(executable_path=Parameters.Firefox_Driver_PATH)
    return driver

def browser_open_url(browser, url) :
    browser.get(url)
    return browser

def get_html_page(browser):
    res = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, 'lxml')
    return soup

def search_for_the_keyword(browser):
    browser= browser_open_url(browser,Parameters.search_URL)
    title_box = browser.find_element_by_xpath('//*/input[@id="a4.1.1.2.4.1:MainAutoComp"]')
    title_box.send_keys(Parameters.KEYWORD)
    submit = browser.find_element_by_xpath('//*/div[@id="a4.1.1.2.4:SearchBtn"]')
    submit.click()
    time.sleep(5)

    wait = WebDriverWait(browser, 60)
    table = wait.until(EC.presence_of_element_located((By.ID, 'a1.1.3.3:ImgContainerPnl')))
    #Finds first item to click.
    first_item = browser.find_element_by_xpath('//*/div[@id="a1.1.3.3.1"]')
    first_item.click()
    #makes sure that the first item is loaded and ready to go.
    wait = WebDriverWait(browser, 60)
    table = wait.until(EC.presence_of_element_located((By.ID, 'a1.2.1.1.1.4:MainPnl')))

    return browser

def page_loaded_successfully(browser):

    wait = WebDriverWait(browser, 60)
    table = wait.until(EC.presence_of_element_located((By.ID, 'a1.1.3.3:ImgContainerPnl')))
    if  (table is not None):
        print('Loaded Successfully!')
        return True
    else:
        return False

def extract_page_links(browser):

    page_links = []
    soup = get_html_page(browser)
    img_container_tags = soup.find_all('div' , {'class': 'ABS AvoidBreak VF'})
    if img_container_tags is not None:
        for img in img_container_tags:
            img_link_tag = img.find('a', {'target' : '_MatrixPopup'})
            if img_link_tag is not None:
                image_link = Parameters.base_url + '/' + img_link_tag.get('href')
                page_links.append(image_link)

    return page_links

def extract_page_metadatas(browser,current_page):
    page_metadata = []
    artist = ''
    location = ''
    date = ''
    genre = ''
    material = ''
    title = ''
    subtitle = ''
    Image_URL = ''
    repository_number = ''
    height = ''
    width = ''
    details_url = ''
    #page_url_list = extract_page_links(browser)
    #temp_browser = browser_open()
    current_item = 1
    if 1:
    #for item_link in page_url_list:
        #temp_browser = browser_open_url(browser,item_link)
        soup = get_html_page(browser)

        artist_tag = soup.find('div', {'id': 'a1.2.1.1.1.4.1:K1'})
        if artist_tag is not None:
            artist = artist_tag.text

        title_tag = soup.find('div', {'id': 'a1.2.1.1.1.4:Title'})
        if title_tag is not None:
            title = title_tag.text

        height_tag = soup.find('div', {'id': 'a1.2.1.1.1.4:Height'})
        if height_tag is not None:
            height = height_tag.text

        width_tag = soup.find('div', {'id': 'a1.2.1.1.1.4:Length'})
        if width_tag is not None:
            width = width_tag.text

        repository_tag = soup.find('span', {'id': 'a1.2.1.1.1.4:IdClientMother_Lbl'})
        if repository_tag is not None:
            repository_number = repository_tag.text

        genre_tag = soup.find('span', {'id': 'a1.2.1.1.1.4:Custom_8_Lbl'})
        if genre_tag is not None:
            genre = genre_tag.text

        date_tag = soup.find('div', {'id': 'a1.2.1.1.1.4.3:K1'})
        if date_tag is not None:
            date = date_tag.text

        location_tag = soup.find('div', {'id': 'a1.2.1.1.1.4:LocationName'})
        if location_tag is not None:
            location = location_tag.text

        material_tag = soup.find('div', {'id': 'a1.2.1.1.1.4.7:ListPnl'})
        if material_tag is not None:
            material = material_tag.text

        subtitle_tag = soup.find('span', {'id': 'a1.2.1.1.1.4:CaptionLong_Lbl'})
        if subtitle_tag is not None:
            subtitle = subtitle_tag.text

        Image_tag = soup.find('img', {'id': 'a1.2.1.1.1.2:I_img'})
        if Image_tag is not None:
            Image_URL = Parameters.base_url + Image_tag.get('src')

        Link_tag = soup.find('div', {'id': 'a1.2.1.1.1.4:SEOUrlLbl'})
        if Link_tag is not None:
            details_url = Link_tag.text

        file_name = 'page_' + str(current_page) + '_item_' + str(current_item) + '_' + Image_URL.split('/')[-1]
        download_image(Image_URL,file_name)

        print(date)
        print(repository_number)
        print(genre)
        print(height)
        print(width)
        print(details_url)

        item_metadata = {
            'Photo Archive'     : Parameters.base_url,
            'Iconography'       : Parameters.Iconography,
            'Branch'            : 'ArtHist',
            'File Name'         : file_name,
            'Title'             : title,
            'Additional Information' : subtitle,
            'Artist'            : artist,
            'Earliest Date'     : date,
            'Current Location'  : location,
            'Repository Number' : repository_number,
            'Height of Object'  : height,
            'Width of Object'   : width,
            'Genre'             : genre,
            'Material'          : material,
            'Details URL'       : details_url,
            'Image Credits'     : Image_URL,
        }
        keyorder = Parameters.Header
        item_metadata = OrderedDict(sorted(item_metadata.items(), key=lambda i: keyorder.index(i[0])))
        print('Item ' + str(current_item) + ' ...Done!')

        current_item += 1

    return item_metadata

def go_to_next_page(browser):
    nextPage = browser.find_element_by_xpath('//*/div[@id="a1.2.1.3:NextBtn"]')

    if nextPage is not None :
        s = nextPage.get_attribute('class')
        if s == 'CT Button ABS 6231hio0':
            nextPage.click()
            time.sleep(2)
            return True

    return False


def download_image(url,file_name):
    path = Parameters.Images_PATH + file_name
    request.urlretrieve(url, path)


def create_csv_file(file_path):
    keyorder = Parameters.Header

    with open(file_path, "w") as f:
        wr = csv.DictWriter(f, dialect="excel", fieldnames=keyorder)
        wr.writeheader()


def append_metadata_to_CSV(dic):
    keyorder = Parameters.Header
    with open(Parameters.CSV_File_PATH, "a") as fp:
        wr = csv.DictWriter(fp,dialect="excel",fieldnames=keyorder)
        wr.writerow(dic)

def browser_quit(browser):
    browser.quit()