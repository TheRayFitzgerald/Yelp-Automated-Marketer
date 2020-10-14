from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys, os, platform
import json

URL = 'https://www.yelp.com/search?find_desc=Takeout&find_loc=CT06901&attrs=RestaurantsTakeOut&start='
ZIP_CODES = ['06901', '06902', '06903', '06904', '06905', '06906', '06907', '06910', '06911', '06912', '06913', '06914', '06926', '06927']

dirpath = os.getcwd()
chromepath = dirpath + '/assets/chromedriver_%s' % (platform.system()).lower()

def get_section_index(rows, section_index):
    print('Checking section index: %i' % section_index)
    for child in rows:
        if child.get_attribute("class") == 'lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU':
            print('found modal')

            print('section index %i' % section_index)
            return section_index
    return False

def execute_on_merchant(url):
    success_count = 0
    failure_count = 0

    chrome_options = Options()
    browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
    browser.implicitly_wait(5)
    browser.get(url)


    innerHTML = browser.page_source
    html = BeautifulSoup(innerHTML, 'html.parser')

    try:
        innerHTML = browser.page_source
        html = BeautifulSoup(innerHTML, 'html.parser')
        last_index = len(html.find_all('div', {'class':'island-section__373c0__3SUh7'}))
        sections = html.find_all('section', {'class':'lemon--section__373c0__fNwDM margin-b3__373c0__q1DuY border-color--default__373c0__3-ifU'})
        print('###')
        sections = browser.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section')
        print('number of sections %i' % len(sections))
        for section_index in range(1, len(sections) + 1):
            children = browser.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div' % section_index)
            print(len(children))
            section_index = get_section_index(children, section_index)
            if (section_index):
                break

        message_button = WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div[%i]/div/div[2]/button/div/span/p' % (section_index, last_index))))
                                                                                               #'//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[2]/div/div[5]/div/div[2]/button/div/span/p'

        #message_button = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div[%i]/div/div[2]/button/div/span/p' % (section_index, last_index))

        if(message_button):
            print('creating merchant object')
            merchant = dict()
            merchant['name'] = html.find('h1', class_='lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy').text
            merchant['phone_number'] = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[2]/div/div[2]/p[2]').text
            merchant['website'] = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[1]/div/div[2]/p[2]/a').text
            print('Merchant: ')
            print(merchant)

        message_button.click()
        print('Button found')

        browser.find_element_by_id('message-textarea').send_keys('test')
        browser.find_element_by_id('firstname-input').send_keys('name')
        browser.find_element_by_name('email').send_keys('email_test')

        close_button = browser.find_element_by_xpath('//*[@id="modal-portal-container"]/div/div/div/div/div[1]/p/a')
        close_button.click()


        success_count += 1
        browser.back()
    except Exception as e:
        print('No message button')
        print(e)
        print('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div[%i]/div/div[2]/button/div/span/p' % (section_index, last_index))
        print('############')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        failure_count += 1



def iterate_merchants(browser, url):
    """ given a valid grubhub url, scrape the menu of a restaurant """
    print('Running...')
    success_count = 0
    failure_count = 0
    not_messageable_count = 0
    all_merchants = list()

    browser.get(url)

    for i in range(6, 16):
        try:
            # find the merchant to click
            element = WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div/div[1]/div[1]/div[2]/div[2]/ul/li[%i]/div' % i)))
            element.click()

            try:
                #innerHTML = browser.page_source
                #html = BeautifulSoup(innerHTML, 'html.parser')
                #last_index = len(html.find_all('div', {'class':'island-section__373c0__3SUh7'}))
                #sections = html.find_all('section', {'class':'lemon--section__373c0__fNwDM margin-b3__373c0__q1DuY border-color--default__373c0__3-ifU'})
                #sections = browser.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section')
                #sections = WebDriverWait(browser, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section')))

                #print('number of sections %i' % len(sections))
                '''
                for section_index in range(1, len(sections) + 1):
                    children = browser.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div' % section_index)
                    #print(len(children))
                    section_index = get_section_index(children, section_index)
                    if (section_index):
                        last_index = len(children)
                        break
                '''
                #last_index = len(browser.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div'))
                #section_index = 1

                message_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="link__373c0__343sR"]/div/span/p')))


                #message_button = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div[%i]/div/div[2]/button/div/span/p' % (section_index, last_index))

                if(message_button):
                    print('creating merchant object')
                    merchant = dict()
                    #merchant['name'] = html.find('h1', class_='lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy').text
                    items = WebDriverWait(browser, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU"]')))

                    merchant['name'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/h1'))).text
                    #merchant['phone_number'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[2]/div/div[2]/p[2]'))).text
                    merchant['phone_number'] = items[1].find_element_by_xpath('.//div/div[2]/p[2]').text
                    merchant['website'] = items[0].find_element_by_xpath('.//div/div[2]/p[2]/a').text
                    #merchant['website'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[1]/div/div[2]/p[2]/a'))).text
                    #merchant['website'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//div[1][@class="island-section__373c0__3SUh7"]/div/div[2]/p[2]/a'))).text
                                                                                #                                     //*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[2]/div/div[1]/div/div[2]/p[2]/a
                    merchant['address'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//address[@class="lemon--address__373c0__2sPac"]/p[1]/span'))).text + \
                        ', ' + WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//address[@class="lemon--address__373c0__2sPac"]/p[2]/span'))).text

                message_button.click()
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'message-textarea'))).send_keys('test')
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, 'firstname-input'))).send_keys('test')
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.NAME, 'email'))).send_keys('test')

                #browser.find_element_by_id('message-textarea').send_keys('test')
                #browser.find_element_by_id('firstname-input').send_keys('name')
                #browser.find_element_by_name('email').send_keys('email_test')

                close_button = browser.find_element_by_xpath('//*[@id="modal-portal-container"]/div/div/div/div/div[1]/p/a')
                close_button.click()
                print('############')
                print('Message Sent Successfully\nRestaurant Number: %i' % (i-5))
                print('############\n')
                success_count += 1
                all_merchants.append(merchant)
                #print(all_merchants)
                browser.back()


            except Exception as e:
                print('############')
                print('No message button\nRestaurant Number: %i' % (i-5))
                print(e)
                #print('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div[%i]/div/div[2]/button/div/span/p' % (section_index, last_index))

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print('############\n')
                failure_count += 1
                #driver.execute_script("window.history.go(-1)")
                if (browser.current_url != url):
                    browser.back()
        except:
            pass

    #print(success_count)
    #print(failure_count)
    return_dict = dict()
    return_dict['merchants'] = all_merchants
    return_dict['success_count'] = success_count
    return_dict['failure_count'] = failure_count
    return_dict['not_messageable_count'] = not_messageable_count

    print(all_merchants)
    browser.quit()
    return return_dict


def main():
    success_count = 0
    failure_count = 0
    not_messageable_count = 0
    total_merchants = 0
    start = time.time()
    data_dict = dict()
    data_dict['data'] = list()


    chrome_options = Options()
    # To disable headless mode (for debugging or troubleshooting), comment out the following line:
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)

    for zip_code in ZIP_CODES[3:6]:
        for page_number in range(1):
            try:
                print('Zip Code: %s\nPage Number: %i' % (zip_code, page_number))
                return_dict = iterate_merchants(browser, 'https://www.yelp.com/search?find_desc=Takeout&find_loc=CT%s&attrs=RestaurantsTakeOut&start=%i' % (zip_code, page_number*10))

                data_dict['data'] = data_dict['data'] + return_dict['merchants']
                success_count += return_dict['success_count']
                failure_count += return_dict['failure_count']
                not_messageable_count += return_dict['not_messageable_count']
                total_merchants += 10
                #data_dict['data'] = data_dict['data'] + iterate_merchants('https://www.yelp.com/search?find_desc=Takeout&find_loc=CT%s&attrs=RestaurantsTakeOut&start=%i' % (zip_code, page_number*10))
                #iterate_merchants(URL + str(page_number * 10))
            except Exception as e:
                print('Post code doesnt have this many pages %i' % page_number)
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    with open(f'{path}/data.json', 'w') as f:
        json.dump(data_dict, f, indent=4)
    print('[Finished]')
    end = time.time()
    print('---------------------------------')
    print('Total Merchants: %i' % total_merchants)
    print('Success Count: %i' % success_count)
    print('Failure Count: %i' % failure_count)
    print('Not Messageable Count: %i' % not_messageable_count)
    print('Time taken: ')
    #print(success_count)
    #print(failure_count)
    print(end - start)

if __name__ == '__main__':
    #execute_on_merchant('https://www.yelp.com/biz/the-stillery-stamford?osq=Takeout')
    main()


