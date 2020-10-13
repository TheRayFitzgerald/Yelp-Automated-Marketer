from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, platform
import json

URL = 'https://www.yelp.com/search?find_desc=Takeout&find_loc=CT06901&attrs=RestaurantsTakeOut&start='
MENU = '1599675614973x652726785232916400'
ZIP_CODES = ['06901', '06902', '06903', '06904', '06905', '06906', '06907', '06910', '06911', '06912', '06913', '06914', '06926', '06927']

dirpath = os.getcwd()
chromepath = dirpath + '/assets/chromedriver_%s' % (platform.system()).lower()

def get_menu(url):
    """ given a valid grubhub url, scrape the menu of a restaurant """
    print('Running...')
    chrome_options = Options()
    # To disable headless mode (for debugging or troubleshooting), comment out the following line:
    #chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
    browser.implicitly_wait(100)
    browser.get(url)
    time.sleep(10)
    innerHTML = browser.page_source

    html = BeautifulSoup(innerHTML, 'html.parser')
    menu = html.find_all("ul",{"class":"lemon--ul__09f24__1_cxs undefined list__09f24__17TsU"})[0]
    print(menu['class'])
    #menu = html.find_element(By.XPATH, '//*[@id="ghs-restaurant-menu"]/div/div/ghs-impression-tracker/div')
    if menu is None:
        print('menu fail')
        get_menu(url)
        return

    # Merchants
    merchants = menu.find_all('li', {'class':'lemon--li__09f24__1r9wz border-color--default__09f24__R1nRO'})
    #merchants = browser.find_elements_by_class_name('lemon--li__09f24__1r9wz border-color--default__09f24__R1nRO')

    print(len(merchants))
    for i in range(1, len(merchants)+1):
        try:
            element = browser.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[1]/div[1]/div[2]/div[2]/ul/li[%i]/div" % i)
            element.click()
            time.sleep(10)
            driver.execute_script("window.history.go(-1)")
            try:
                element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
                message_button = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[5]/div/div[2]/button/div/span/p')

                message_button.click()
                success_count += 1
                driver.execute_script("window.history.go(-1)")
            except:
                print('No message button')
                failure_count += 1
                driver.execute_script("window.history.go(-1)")

        except:
            pass



    #merchants = merchants[0:1]
    '''
    merchant_titles = [merchant.find('h3', class_='menuSection-title').text for merchant in merchants]
    merchant_items = [[itm.text for itm in merchant.find_all('a', class_='menuItem-name')] for merchant in merchants]
    prices = [[p.text for p in merchant.find_all('span', class_='menuItem-displayPrice')] for merchant in merchants]
    descriptions = [[itm.text for itm in merchant.find_all('p', class_='menuItemNew-description--trunmerchante')] for merchant in merchants]
    '''
    ids = []
    for merchant in merchants:
        merchant_ids = []
        items = merchant.find_all('div', class_='menuItem-inner')
        for item in items:
            merchant_ids.append(item.get('id'))
        ids.append(merchant_ids)

    full_menu = {}
    for ind, title in enumerate(merchant_titles):
        all_items = []
        for ind2, itm_name in enumerate(merchant_items[ind]):
            item = {}
            item['name_text'] = itm_name
            item['price_number'] = float(prices[ind][ind2].replace('$', ''))
            item['description_text']= descriptions[ind][ind2]
            item['menu_custom_menu'] = MENU
            item['menuitemmodifiers_list_custom_menuitemmodifiers'] = get_item(browser, ids[ind][ind2])
            all_items.append(item)
        full_menu[title] = all_items
    path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    with open(f'{path}/pizza.json', 'w') as f:
        json.dump(full_menu, f, indent=4)
    print('[Finished]')
    driver.quit()

def iterate_merchants(url):
    """ given a valid grubhub url, scrape the menu of a restaurant """
    print('Running...')
    success_count = 0
    failure_count = 0


    # To disable headless mode (for debugging or troubleshooting), comment out the following line:
    #chrome_options.add_argument("--headless")
    chrome_options = Options()
    browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
    browser.implicitly_wait(5)
    browser.get(url)
    time.sleep(10)

    innerHTML = browser.page_source
    html = BeautifulSoup(innerHTML, 'html.parser')

    menu = html.find_all("ul",{"class":"lemon--ul__09f24__1_cxs undefined list__09f24__17TsU"})[0]
    merchants = menu.find_all('li', {'class':'lemon--li__09f24__1r9wz border-color--default__09f24__R1nRO'})

    all_merchants = list()
    for i in range(6, 16):
        try:
            # find the merchant to click
            element = browser.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[1]/div[1]/div[2]/div[2]/ul/li[%i]/div" % i)
            element.click()


            try:
                innerHTML = browser.page_source
                html = BeautifulSoup(innerHTML, 'html.parser')
                last_index = len(html.find_all('div', {'class':'island-section__373c0__3SUh7'}))
                sections = html.find_all('section', {'class':'lemon--section__373c0__fNwDM margin-b3__373c0__q1DuY border-color--default__373c0__3-ifU'})
                for section_index in range(0, len(sections)):
                    children = sections[section_index].findChildren("div" , recursive=False)
                    for child in children:
                        if child.get('class') == 'lemon--div__373c0__1mboc padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-radius--regular__373c0__3KbYS background-color--white__373c0__2uyKj':
                            section_index += 1
                            break

                message_button = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div[%i]/div/div[2]/button/div/span/p' % (section_index, last_index))))
                #message_button = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[%i]/div/div[%i]/div/div[2]/button/div/span/p' % (section_index, last_index))

                if(message_button):
                    print('creating merchant object')
                    merchant = dict()
                    merchant['name'] = html.find('h1', class_='lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy').text
                    merchant['phone_number'] = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[2]/div/div[2]/p[2]').text
                    merchant['website'] = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[1]/div/div[2]/p[2]/a').text

                message_button.click()
                print('Button found')

                browser.find_element_by_id('message-textarea').send_keys('test')
                browser.find_element_by_id('firstname-input').send_keys('name')
                browser.find_element_by_name('email').send_keys('email_test')

                close_button = browser.find_element_by_xpath('//*[@id="modal-portal-container"]/div/div/div/div/div[1]/p/a')
                close_button.click()


                success_count += 1
                all_merchants.append(merchant)
                print(all_merchants)
                browser.back()
            except Exception as e:
                print('No message button')
                print(e)
                failure_count += 1
                #driver.execute_script("window.history.go(-1)")
                if (browser.current_url != url):
                    browser.back()
        except:
            pass

    print(success_count)
    print(failure_count)
    print(all_merchants)
    browser.quit()
    return all_merchants



data_dict = dict()
data_dict['data'] = list()
for zip_code in ZIP_CODES[2:3]:
    for page_number in range(1):

        data_dict['data'] = data_dict['data'] + iterate_merchants('https://www.yelp.com/search?find_desc=Takeout&find_loc=CT%s&attrs=RestaurantsTakeOut&start=%i' % (zip_code, page_number*10))
        #iterate_merchants(URL + str(page_number * 10))

path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
with open(f'{path}/data.json', 'w') as f:
    json.dump(data_dict, f, indent=4)
print('[Finished]')
