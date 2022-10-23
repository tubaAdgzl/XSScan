import optparse
import chromedriver_autoinstaller
from colorama import Fore, Back
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-u","--url",dest="target_url",help="Enter target url address ex:https://example.com/?q=XSS")

    inputs = parse_object.parse_args()[0]
    if not inputs.target_url:
        print("Enter target url address ex:https://example.com/?q=XSS")
    if  'https://' in inputs.target_url or  'http://' in inputs.target_url:
        print(Fore.RED +"[+][+][+]** starting.... **[+][+][+]")
    else:
        print("Enter target url ex:https://example.com/?q=XSS")
    if not 'XSS' in inputs.target_url:
        print("Add XSS parameter to target url!")

    return inputs

def driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-xss-auditor')
    options.add_argument('--disable-web-security')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-notifications')

inputs=get_user_input()
wordlist = 'payloads.txt'
target = inputs.target_url

options = driver_options()
chromedriver_autoinstaller.install()

if  'https://' in target or 'http://' and 'XSS' in target:
    try:
        driver = webdriver.Chrome(chrome_options=options)
        for payload in open(wordlist,'r').readlines():
            url = target.replace('XSS',payload)
            print(url)
            driver.get(url)
            try:
                WebDriverWait(driver, 3).until(expected_conditions.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print(Back.GREEN + "[+] XSS worked with this :", payload)
            except TimeoutException:
                print(Back.YELLOW + "[-] XSS didn't work with this : ",payload)
        driver.quit()
    except KeyboardInterrupt:
        print("Program interrupted.")
else:
    print(Fore.RED + "Enter url:\nex:https://example.com/?q=XSS")
