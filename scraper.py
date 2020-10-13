from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os, platform
import json

URL = 'https://www.yelp.com/search?find_desc=Takeout&find_loc=CT06901'
MENU = '1599675614973x652726785232916400'



dirpath = os.getcwd()
chromepath = dirpath + '/assets/chromedriver_%s' % (platform.system()).lower()


def get_item(browser, id):
    """ given an id, scrape a menu item and all of its options """
    #button = browser.find_element_by_id(id)
    browser.execute_script("arguments[0].click();", id)
    time.sleep(1)

    innerHTML = browser.page_source
    html = BeautifulSoup(innerHTML, 'html.parser')

    _options = []

    options = html.find_all('div', class_='menuItemModal-options') # menuItemModal-choice-option-description
    for option in options:
        single_option=dict()
        single_option['modifiername_text'] = name = option.find(class_='menuItemModal-choice-name').text

        instruction_text = option.find(class_='menuItemModal-choice-instructions').text.replace('.','').split(' - ')

        if instruction_text[0] == 'Required':
            single_option['required_boolean']=True
            single_option['numberallowedselections_number']= [int(s) for s in instruction_text[1].split() if s.isdigit()][0]
        else:
            single_option['required_boolean']=False
            if instruction_text[1] == "Choose as many as you like":
                single_option['numberallowedselections_number']=0
            else:
                single_option['numberallowedselections_number']= [int(s) for s in instruction_text[1].split() if s.isdigit()][0]

        _choices=[]
        choices = option.find_all('span', class_='menuItemModal-choice-option-description')
        for choice in choices:
            #print(choice.text.split(' + ')[0] + choice.text.split(' + ')[1])
            if ' + ' in choice.text:
                _choices.append({'name_text':choice.text.split(' + ')[0], 'price_number':float(choice.text.split(' + ')[1].replace('$', ''))})
            else:
                _choices.append({'name_text':choice.text, 'price_number':0})

        single_option['modifiermenuitems_list_custom_menuitem'] = _choices
        #append the dictionary
        _options.append(single_option)
    return _options

def get_menu(url):
    """ given a valid grubhub url, scrape the menu of a restaurant """
    print('Running...')
    chrome_options = Options()
    # To disable headless mode (for debugging or troubleshooting), comment out the following line:
    #chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
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
    chrome_options = Options()
    # To disable headless mode (for debugging or troubleshooting), comment out the following line:
    #chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(options=chrome_options, executable_path = chromepath)
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
    for i in range(1, len(merchants)):
        try:
            element = browser.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[1]/div[1]/div[2]/div[2]/ul/li[%i]/div" % i)
            element.click()
            time.sleep(10)
            #driver.execute_script("window.history.go(-1)")
            try:
                message_button = browser.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[4]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/section[1]/div/div[5]/div/div[2]/button/div/span/p')
                message_button.click()
                print('Button found')
                success_count += 1
                #driver.execute_script("window.history.go(-1)")
                #browser.back()
            except:
                print('No message button')
                failure_count += 1
                #driver.execute_script("window.history.go(-1)")
                if (browser.current_url != URL):
                    browser.back()
        except:
            pass

    print(success_count)
    print(failure_count)
    browser.quit()
iterate_merchants(URL)
#example link: 'https://www.grubhub.com/restaurant/insomnia-cookies-76-pearl-st-new-york/295836'
