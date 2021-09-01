from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys, os, platform, csv, json, requests
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from random import choice
from selenium.webdriver.common.proxy import Proxy, ProxyType


URL = 'https://www.yelp.com/search?find_desc=Takeout&find_loc=CT06901&attrs=RestaurantsTakeOut&start='
ZIP_CODES = ['06901', '06902', '06903', '06904', '06905', '06906', '06907', '06910', '06911', '06912', '06913', '06914', '06926', '06927']

SENDER_EMAIL = 'john@email.com'
SENDER_NAME = 'John Appleseed'

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

def execute_on_merchant(merchant, OUTBOUND_MESSAGE):
    success_count = 0
    not_messageable_count = 0

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
    browser.get(merchant['yelp_url'])

    try:
        message_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="link__373c0__343sR"]/div/span/p')))
        '''
        if(message_button):
            print('############\ncreating merchant object')

            merchant = dict()
            items = WebDriverWait(browser, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU"]')))

            merchant['name'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/h1'))).text

            merchant['phone_number'] = items[1].find_element_by_xpath('.//div/div[2]/p[2]').text
            merchant['website'] = items[0].find_element_by_xpath('.//div/div[2]/p[2]/a').text
            merchant['address'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//address[@class="lemon--address__373c0__2sPac"]/p[1]/span'))).text + \
                ', ' + WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//address[@class="lemon--address__373c0__2sPac"]/p[2]/span'))).text
            merchant['yelp_url'] = browser.current_url


        '''
        message_button.click()
        WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.ID, 'firstname-input'))).send_keys(SENDER_NAME)
        WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.NAME, 'email'))).send_keys(SENDER_EMAIL)
        WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.ID, 'message-textarea'))).send_keys(OUTBOUND_MESSAGE % merchant['name'])

        submit_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-portal-container"]/div/div/div/div/div[2]/div/form/div[4]/div[1]/button')))

        submit_button.click()
        confirmation_modal = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-portal-container"]/div/div/div/div/div[2]')))
        print('!!! Confirmation on screen !!!')
        time.sleep(3)


        #close_button = browser.find_element_by_xpath('//*[@id="modal-portal-container"]/div/div/div/div/div[1]/p/a')
        #close_button.click()

        print('############\n')
        print('Success\n############')
        browser.quit()
        return

    except Exception as e:
        print('############')

        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print('############\n')
        not_messageable_count += 1
        browser.quit()
        return


def main_2():
    f = open("outbound_message.txt", "r")
    OUTBOUND_MESSAGE = f.read()
    with open('data_copy/data_merge.json') as f:
      data = json.load(f)


    duplicate_monitor_dict = dict()

    for merchant in data['data']:

        if merchant['yelp_url'] in duplicate_monitor_dict:
            pass
        else:
            duplicate_monitor_dict[merchant['yelp_url']] = ''
            execute_on_merchant(merchant, OUTBOUND_MESSAGE)


def proxy_generator():
    try:
        response = requests.get("https://sslproxies.org/")
        soup = BeautifulSoup(response.content, 'lxml')
        proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text,
    	   soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
        return proxy
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def iterate_merchants(browser, OUTBOUND_MESSAGE, data_dict, url):

    print('Running...')
    success_count = 0
    not_messageable_count = 0
    all_merchants = list()
    try:
        browser.get(url)
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    for i in range(6, 16):
        try:
            #element = WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div/div[1]/div[1]/div[2]/div[2]/ul/li[%i]/div' % i)))
            element = WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/yelp-react-root/div[1]/div[4]/div/div[1]/div[1]/div[2]/div/ul/li[%i]/div' % i)))
            element.click()
            #/html/body/yelp-react-root/div[1]/div[4]/div/div[1]/div[1]/div[2]/div/ul/li[8]/div

            try:
                message_button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap"]/div[3]/yelp-react-root/div/div[3]/div/div/div[2]/div/div[2]/div/div/section[1]/div/div[4]/div/div[1]/button')))
                # //*[@id="wrap"]/div[3]/yelp-react-root/div/div[3]/div/div/div[2]/div/div[2]/div/div/section[1]/div/div[4]/div/div[1]/button
                # //button[@class="link__373c0__343sR"]/div/span/p
                '''
                if(message_button):
                    print('############\ncreating merchant object')

                    merchant = dict()
                    items = WebDriverWait(browser, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="lemon--div__373c0__1mboc island-section__373c0__3SUh7 border--top__373c0__3gXLy border-color--default__373c0__3-ifU"]')))

                    merchant['name'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/h1'))).text

                    merchant['phone_number'] = items[1].find_element_by_xpath('.//div/div[2]/p[2]').text
                    merchant['website'] = items[0].find_element_by_xpath('.//div/div[2]/p[2]/a').text
                    merchant['address'] = WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//address[@class="lemon--address__373c0__2sPac"]/p[1]/span'))).text + \
                        ', ' + WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.XPATH, '//address[@class="lemon--address__373c0__2sPac"]/p[2]/span'))).text
                    merchant['yelp_url'] = browser.current_url
                '''


                message_button.click()
                WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.ID, 'firstname-input'))).send_keys(SENDER_NAME)
                WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.NAME, 'email'))).send_keys(SENDER_EMAIL)
                #WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.ID, 'message-textarea'))).send_keys(OUTBOUND_MESSAGE % merchant['name'])
                WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.ID, 'message-textarea'))).send_keys(OUTBOUND_MESSAGE % 'test')

                submit_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-portal-container"]/div/div/div/div/div[2]/div/form/div[4]/div[1]/button')))
                #submit_button.click()

                #data_dict['data'].append(merchant)
                with open('data.json', 'w') as f:
                    json.dump(data_dict, f, indent=4)

                #close_button = browser.find_element_by_xpath('//*[@id="modal-portal-container"]/div/div/div/div/div[1]/p/a')
                #close_button.click()

                print('Message Sent Successfully\nRestaurant Number: %i' % (i-5))
                print('############\n')
                success_count += 1
                all_merchants.append(merchant)
                browser.back()

            except Exception as e:
                print('############')
                print('No message button\nRestaurant Number: %i' % (i-5))
                print(e)

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print('############\n')
                not_messageable_count += 1

                if (browser.current_url != url):
                    browser.back()
        except:
            pass


    return_dict = dict()
    return_dict['merchants'] = all_merchants
    return_dict['success_count'] = success_count
    return_dict['not_messageable_count'] = not_messageable_count
    return_dict['data_dict'] = data_dict

    browser.quit()
    return return_dict

def main():
    success_count = 0
    not_messageable_count = 0
    total_merchants = 0
    start = time.time()
    data_dict = dict()
    data_dict['data'] = list()

    f = open("outbound_message.txt", "r")
    OUTBOUND_MESSAGE = f.read()


    '''
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path = chromepath)
    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
    driver.quit()
    proxies = []


    #for i in range(0, len(ips)):
    #    proxies.append(ips[i]+':'+ports[i])
    #print(proxies)
    '''

    for zip_code in ZIP_CODES[4:]:
        #req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
        #proxies = req_proxy.get_proxy_list() #this will create proxy list
        for page_number in range(16, 24):
            try:
                #options = Options()
                #proxy = (proxy_generator())['https']
                #print("Proxy currently being used: {}".format(proxy))
                #print(proxy['https'])
                #options.add_argument('--proxy-server={}'.format(proxy['https']))
                '''
                prox = Proxy()
                prox.proxy_type = ProxyType.MANUAL
                prox.http_proxy = proxy
                prox.socks_proxy = proxy
                prox.ssl_proxy = proxy

                capabilities = webdriver.DesiredCapabilities.CHROME
                prox.add_to_capabilities(capabilities)


                PROXY = "1.20.101.24:51681"
                chrome_options = Options()
                chrome_options.add_argument('--proxy-server=%s' % PROXY)


                #PROXY = proxies[page_number].get_address()
                #webdriver.DesiredCapabilities.CHROME['proxy']={"httpProxy":PROXY, "ftpProxy":PROXY, "sslProxy":PROXY, "proxyType":"MANUAL"}
                #chrome_options.add_argument("--headless")
                #browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
                #browser.get("http://google.com")
                #time.sleep(30)
                #browser.get("https://www.whatismyip.com/my-ip-information/")
                while True:
                    try:
                        proxy = proxy_generator()
                        print("Proxy currently being used: {}".format(proxy))
                        #response = requests.get("http://yelp.com", timeout=7)
                        break
                        # if the request is successful, no exception is raised
                    except Exception as e:
                        print(e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                print("2. Proxy currently being used: {}".format(proxy))

                chrome_options = Options()
                #chrome_options.add_argument('--proxy-server=%s' % '108.163.66.164:8080')
                browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
                '''

                #chrome_options.add_argument('--proxy-server=%s' % '108.163.66.164:8080')
                chrome_options = Options()
                #chrome_options.add_argument("--headless")
                browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
                print('Zip Code: %s\nPage Number: %i' % (zip_code, page_number))
                print('Before')
                return_dict = iterate_merchants(browser, OUTBOUND_MESSAGE, data_dict, 'https://www.yelp.com/search?find_desc=Takeout&find_loc=CT%s&attrs=RestaurantsTakeOut&start=%i' % (zip_code, page_number*10))
                print('After')
                time.sleep(3)
                data_dict = return_dict['data_dict']
                success_count += return_dict['success_count']
                not_messageable_count += return_dict['not_messageable_count']
                total_merchants += 10
                if success_count > 105:
                    break

            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        if success_count > 109:
            print('breaking again')
            break
    path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    #with open(f'{path}/data.json', 'w') as f:
    #    json.dump(data_dict, f, indent=4)
    print('[Finished]')
    end = time.time()
    print('---------------------------------')
    print('Total Merchants: %i' % total_merchants)
    print('Success Count: %i' % success_count)
    print('Not Messageable Count: %i' % not_messageable_count)
    print('Time taken: ')
    print(end - start)


if __name__ == '__main__':

    #('https://www.yelp.com/biz/the-stillery-stamford?osq=Takeout', OUTBOUND_MESSAGE)
    main()
    #main_2()


