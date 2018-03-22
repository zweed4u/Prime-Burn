#!/usr/bin/python3
import os
import time
import random
import string
import secrets
import requests
import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import Select

root_directory = os.getcwd()
c = configparser.ConfigParser()
configFilePath = os.path.join(root_directory, 'config.cfg')
c.read(configFilePath)


class Config:
    customer_name = c.get('userInfo', 'customerName')
    card_name = c.get('userInfo', 'cardName')
    burner_password = c.get('userInfo', 'burnerPassword')
    card_number = c.get('userInfo', 'cardNumber')
    card_month = c.get('userInfo', 'cardMonth')
    card_year = c.get('userInfo', 'cardYear')
    card_address = c.get('userInfo', 'address')
    card_city = c.get('userInfo', 'city')
    card_state = c.get('userInfo', 'state')
    card_zipcode = c.get('userInfo', 'zip')
    card_country = c.get('userInfo', 'country')
    phone = c.get('userInfo', 'phone')


class GuerrillaMail:
    def __init__(self):
        """https://www.guerrillamail.com/GuerrillaMailAPI.html"""
        self.session = requests.session()
        self.root_api_url = 'http://api.guerrillamail.com/ajax.php'
        self.root_url = 'https://www.guerrillamail.com/ajax.php'
        self.email_used = None
        self.domain_change_email = None
        self.start_time = str(int(time.time()*1000))
        self.domains = [
            'sharklasers.com',
            'guerrillamail.info',
            'grr.la',
            'guerrillamail.biz',
            'guerrillamail.com',
            'guerrillamail.de',
            'guerrillamail.net',
            'guerrillamail.org',
            'guerrillamailblock.com',
            'pokemail.net',
            'spam4.me'
        ]

    def get_email(self):
        """
        {'email_addr': 'qujtxtwk@guerrillamailblock.com', 'email_timestamp': 1521322849, 'alias': 'awhvuc+5pft4are5v7p4', 'sid_token': 'h21rc8tr61cdtjg68a94rnbmg2'}
        """
        get_email_query_params = {
            'f': 'get_email_address',
            'lang': 'en',
            'SUBSCR': '',
            'site': 'guerrillamail.com',
            '_': self.start_time
        }
        get_email_response = self.session.get(self.root_api_url, params=get_email_query_params).json()
        self.email_used = get_email_response['email_addr']
        self.domain_change_email = f'{self.email_used.split("@")[0]}@{random.choice(self.domains)}'

    def check_email(self):
        """
        {'list': [], 'count': '0', 'email': 'qujtxtwk@guerrillamailblock.com', 'alias': 'awhvuc+5pft4are5v7p4', 'ts': 1521322849, 'sid_token': 'h21rc8tr61cdtjg68a94rnbmg2', 
        'stats': {'sequence_mail': '51,104,924', 'created_addresses': 38163242, 'received_emails': '7,211,419,259', 'total': '7,160,314,335', 'total_per_hour': '163899'}, 
        'auth': {'success': True, 'error_codes': []}}
        """
        check_email_query_params = {
            'f': 'check_email',
            'seq': '1',
            'site': 'guerrillamail.com',
            '_': self.start_time
        }
        return self.session.get(self.root_api_url, params=check_email_query_params).json()

    def return_email(self):
        if self.email_used is None or self.domain_change_email is None:
            self.get_email() 
        return self.email_used, self.domain_change_email

    def delete_mail(self):
        # Check status code and retry if needed
        email_list_query = {
            'f': 'get_email_list',
            'offset': '0',
            'site': 'guerrillamail.com',
            '_': str(int(time.time())*1000)
        }
        emails = self.session.get(self.root_url, params=email_list_query).json()['list']
        print('Fetching emails - waiting until at least 2 are found - 30 second poll')
        while len(emails) < 2:
            emails = self.session.get(self.root_url, params=email_list_query).json()['list']
            time.sleep(30)
        for email in emails:
            del_email = {
                'f': 'del_email',
            }
            del_data = {
                'email_ids[]': email['mail_id'],
                'site': 'guerrillamail.com'
            }
            print(f'Deleting {email["mail_id"]}')
            self.session.post(self.root_url, params=del_email, data=del_data)
            time.sleep(2)


class RegisterAmazon:
    def __init__(self):
        self.name = None
        self.email = None
        self.password = None
        self.driver = webdriver.Chrome(f'{os.getcwd()}/chromedriver')

    def create_account(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

        #self.driver.get('https://www.amazon.com/ap/register?openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=usflex&ignoreAuthState=1&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&prevRID=610HEHXNYAXH2ECK3T47&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
        self.driver.get('https://www.amazon.com/ap/register?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_custrec_newcust')

        customer_name = self.driver.find_element_by_id('ap_customer_name')
        customer_name.clear()
        customer_name.send_keys(self.name)

        customer_email = self.driver.find_element_by_id('ap_email')
        customer_email.clear()
        customer_email.send_keys(self.email)

        customer_pwd = self.driver.find_element_by_id('ap_password')
        customer_pwd.clear()
        customer_pwd.send_keys(self.password)

        customer_rpwd = self.driver.find_element_by_id('ap_password_check')
        customer_rpwd.clear()
        customer_rpwd.send_keys(self.password)

        register_button = self.driver.find_element_by_css_selector('#continue')
        register_button.click()

    def initiate_prime_trial(self, card_number, card_holder_name, card_month, card_year, address, city, state, zip, country, phone):
        """
        :param card_number: str 16 digits
        :param card_holder_name:
        :param card_month: str not padded 1-12
        :param card_year: str full year eg 2020
        :param address: str
        :param city: str
        :param state: str - abbr. eg. NY
        :param zip: str
        :param country: str - abbr eg. US
        :param phone: str - 10 digits
        :return:
        """
        self.driver.get('https://www.amazon.com/gp/primecentral?ie=UTF8&ref_=nav_youraccount_prime')
        # Better detection - add timeouts and make use of isDisplayed method
        while 1:
            try:
                prime_button = self.driver.find_element_by_css_selector('#injectable-button-id > span > span > input')
                break
            except Exception as e:
                continue
        prime_button.click()
        while 1:
            try:
                prime_card_number = self.driver.find_element_by_name('addCreditCardNumber')
                prime_card_holder = self.driver.find_element_by_name('accountHolderName')
                prime_card_month = Select(self.driver.find_element_by_name('expirationMonth'))
                prime_card_year = Select(self.driver.find_element_by_name('expirationYear'))
                next_button = self.driver.find_element_by_id('pmts-id-17-announce')
                prime_modal = self.driver.find_element_by_class_name('a-popover-wrapper')
                break
            except Exception as e:
                continue

        prime_card_number.clear()
        prime_card_number.send_keys(str(card_number))
        prime_card_holder.clear()
        prime_card_holder.send_keys(card_holder_name)
        prime_card_month.select_by_value(str(card_month))
        prime_card_year.select_by_value(str(card_year))
        next_button.click()

        while 1:
            try:
                address_line = self.driver.find_element_by_name('line1')
                city_line = self.driver.find_element_by_name('city')
                state_line = self.driver.find_element_by_name('stateOrRegion')
                zip_line = self.driver.find_element_by_name('postalCode')
                country_select = Select(self.driver.find_element_by_name('countryCode'))
                phone_line = self.driver.find_element_by_name('phoneNumber')
                save_address_button = self.driver.find_element_by_id('pmts-id-40-announce')
                break
            except Exception as e:
                continue

        address_line.clear()
        address_line.send_keys(str(address))

        city_line.clear()
        city_line.send_keys(str(city))

        state_line.clear()
        state_line.send_keys(str(state))

        zip_line.clear()
        zip_line.send_keys(str(zip))

        country_select.select_by_value(str(country))

        phone_line.clear()
        phone_line.send_keys(str(phone))

        save_address_button.click()

        while 1:
            try:
                start_trial_button = self.driver.find_element_by_css_selector('#wlp-prime-button-container-parent > div > div > div.a-column.a-span6.a-text-left.a-spacing-base.a-ws-span6.a-span-last > span > span > input')
                break
            except Exception as e:
                continue

        while start_trial_button.is_displayed() is False:
            pass

        start_trial_button.click()

        while 1:
            try:
                continue_button = self.driver.find_element_by_css_selector('#usp-wlp-popover-content-inner > div.a-section.wlp-prime-main-container > div:nth-child(1) > div > div.a-column.a-span12.a-text-center.a-ws-span6.wlp-prime-welcome-button-container > div > span > span > span > a')
                break
            except Exception as e:
                continue
        continue_button.click()
        self.cancel_trial()
        self.remove_card()
        self.remove_address()
        self.driver.close()

    def cancel_trial(self):
        self.driver.get('https://www.amazon.com/gp/primecentral?ie=UTF8&ref_=nav_youraccount_prime')

        while 1:
            try:
                end_trial_button = self.driver.find_element_by_id('endMembershipLink')
                break
            except Exception as e:
                self.driver.refresh()
            time.sleep(5)
        end_trial_button.click()

        while 1:
            try:
                end_benefits = self.driver.find_element_by_css_selector('#continue-btn > span > input')
                break
            except Exception as e:
                continue
        end_benefits.click()

        while 1:
            try:
                continue_cancel_button = self.driver.find_element_by_css_selector('#continue-to-cancel > span > input')
                break
            except Exception as e:
                continue
        continue_cancel_button.click()

        while 1:
            try:
                end_membership_button = self.driver.find_element_by_css_selector('#endMembershipLaterBtn > span > input')
                break
            except Exception as e:
                continue
        end_membership_button.click()

    def remove_card(self):
        self.driver.get('https://www.amazon.com/cpe/managepaymentmethods?ref_=ya_d_c_pmt_mpo')
        try:
            customer_pwd = self.driver.find_element_by_id('ap_password')
            customer_pwd.clear()
            customer_pwd.send_keys(self.password)

            sign_in_button = self.driver.find_element_by_id('signInSubmit')
            sign_in_button.click()
        except Exception as e:
            # Sometimes we need don't need to sign in
            pass
        card_panel = self.driver.find_element_by_css_selector('#cpefront-mpo-widget > div > form > div.a-section.a-spacing-small.pmts-instrument-list > div > div.a-row.a-spacing-top-mini.a-ws-row > div > a')
        card_panel.click()

        delete_button = self.driver.find_element_by_css_selector('#a-autoid-2 > span > input')
        delete_button.click()

        while 1:
            try:
                confirm_delete = self.driver.find_element_by_name('ppw-widgetEvent:DeleteInstrumentEvent')
                break
            except Exception as e:
                continue

        while confirm_delete.is_enabled() is False or confirm_delete.is_displayed() is False:
            pass
        time.sleep(2)
        confirm_delete.click()

        while 1:
            try:
                close_button = self.driver.find_element_by_css_selector('#a-popover-4 > div > div.a-popover-header > button')
                break
            except Exception as e:
                continue

        time.sleep(2)
        close_button.click()

    def remove_address(self):
        self.driver.get('https://www.amazon.com/a/addresses?ref_=ya_d_c_addr')
        address_panel_delete_button = self.driver.find_element_by_css_selector('#ya-myab-address-delete-btn-0 > span')
        address_panel_delete_button.click()

        while 1:
            try:
                #confirm_address_deletion = self.driver.find_element_by_css_selector('#deleteAddressModal-0-submit-btn > span > input')
                confirm_address_deletion = self.driver.find_element_by_class_name('a-button-input')
                break
            except Exception as e:
                continue

        while confirm_address_deletion.is_enabled() is False or confirm_address_deletion.is_displayed() is False:
            pass
        time.sleep(2)
        confirm_address_deletion.click()


def generate_random_password(password_string_length):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(password_string_length))


my_config = Config()
my_burner_email = GuerrillaMail()
#my_burner_pass = generate_random_password(15)
my_burner_pass = my_config.burner_password
my_burner_email.get_email()

my_prime = RegisterAmazon()
my_prime.create_account(my_config.customer_name, my_burner_email.return_email()[0], my_burner_pass)
print(f'Amazon credentials:\nemail: {my_burner_email.email_used}\npassword: {my_burner_pass}')
my_prime.initiate_prime_trial(my_config.card_number, my_config.card_name, my_config.card_month,
                              my_config.card_year, my_config.card_address, my_config.card_city,
                              my_config.card_state, my_config.card_zipcode, my_config.card_country,
                              my_config.phone)
print('Prime trial initiated and card removed')
my_burner_email.delete_mail()
