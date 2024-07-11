from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from email_data_send import send_data_to_email
from email_check import check_struct_email

ROOT_PATH = Path(__file__).parent
DRIVER_FOLDER = ROOT_PATH / 'drivers' / 'chromedriver'

steam_login_url = 'https://steamcommunity.com/login/home/?goto='
steam_menu_url = 'https://store.steampowered.com/'

steam_username = input("Digite seu login da Steam: ")
steam_password = input("Digite sua senha da Steam: ")
user_email = input("(Digite 'n' para NÃO ENVIAR (opcional))\nDigite seu email para receber os dados: ")    

service = Service(DRIVER_FOLDER)
browser = webdriver.Chrome(service=service)

def login_steam(username, password):
    browser.get(steam_login_url)
    time.sleep(4)
    
    user_input = browser.find_element(By.CSS_SELECTOR, 'input[type="text"]._2eKVn6g5Yysx9JmutQe7WV')
    user_input.send_keys(username)
    
    pass_input = browser.find_element(By.CSS_SELECTOR, 'input[type="password"]._2eKVn6g5Yysx9JmutQe7WV')
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)
    
    time.sleep(5)

def get_wishlist_page():
    browser.get(steam_menu_url)
    time.sleep(3)

    wishlist_input_get = browser.find_element(By.ID, 'wishlist_link')
    wishlist_input_get.click()

    time.sleep(3)

def get_wishlist_urls():
    time.sleep(3)

    wishtelist_page = BeautifulSoup(browser.page_source, 'html.parser')
    wishlist_items = wishtelist_page.find_all('div', class_='wishlist_row')
    urls = []
    
    for item in wishlist_items:
        url = item.find('a', class_='title').get('href')
        urls.append(url)
    
    return urls

def get_game_data(url):
    browser.get(url)
    time.sleep(3)

    wishlist_game_page = BeautifulSoup(browser.page_source, 'html.parser')

    game_name_get = wishlist_game_page.find('div', id='appHubAppName')
    price_original_get = wishlist_game_page.find('div', class_='discount_original_price')
    price_discount_get = wishlist_game_page.find('div', class_='discount_final_price')
    price_porcent_get = wishlist_game_page.find('div', class_='discount_pct')

    game_name = game_name_get.text.strip() if game_name_get else 'Nome do Jogo não encontrado!'
    original_price = price_original_get.text.strip() if price_original_get else 'Preço não encontrado!'
    discount_price = price_discount_get.text.strip() if price_discount_get else 'Preço não encontrado!'
    price_porcent = price_porcent_get.text.strip() if price_porcent_get else 'Porcentagem de Desconto não Encontrado!'
    
    return game_name, original_price, discount_price, price_porcent

login_steam(steam_username, steam_password)
get_wishlist_page()
wishlist_urls = get_wishlist_urls()

wishlist_data = []

for url in wishlist_urls:
    page_data = get_game_data(url)
    values_data = (f'{page_data[0]} - Preço Original: {page_data[1]} - Preço com Desconto: {page_data[2]} -> {page_data[3]}')
    wishlist_data.append(values_data)

browser.quit()

for data in wishlist_data:
    print(data)

if not check_struct_email(user_email) and user_email != 'n':
    print("\nAlgo estava errado na estrutura do seu email! - Não foi possível enviar.")

if user_email != 'n':
    send_data_to_email(user_email, steam_username, wishlist_data)