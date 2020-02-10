# Web Crawler for the https://www.photo.rmn.fr/ (Réunion des Musées Nationaux-Grand Palais (RMN)) photo archive
# Author(s): Mehrdad Tabrizi, Aug. 2018
# Attention: In order to use this code, you have to have the firefox/chrome driver. You need also their path in your Hard drive.
# This crawler uses Firefox driver (geckodriver.exe)

import rmn
import rmn_Parameters as Parameters

def Main():
    current_page = 1
    browser = rmn.browser_open()
    browser = rmn.search_for_the_keyword(browser)
    PAGE_EXISTS = True
    rmn.create_csv_file(Parameters.CSV_File_PATH)

    while (PAGE_EXISTS):
        print('Working on page', str(current_page), '...')
        if (rmn.page_loaded_successfully(browser)):
            #rmn_dic.extend(rmn.extract_page_metadatas(browser,current_page))
            page_dic = rmn.extract_page_metadatas(browser,current_page)
            PAGE_EXISTS = rmn.go_to_next_page(browser)
            current_page += 1
            print('________________')
            rmn.append_metadata_to_CSV(page_dic)

    rmn.browser_quit(browser)

if __name__ == '__main__':
    Main()