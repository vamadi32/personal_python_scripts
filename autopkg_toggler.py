#!/usr/bin/python3
 
# Created by Victor to toggle dev or prod for autopkg
import os
import sys, logging, subprocess
 
prod_url = 'enter_prod_url'
dev_url = 'enter_dev_url'

logging.basicConfig(level=logging.DEBUG, 
format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)
logging.debug('Start of Program')


def checkenviron_var(string):
    try:
        return os.environ[string]
    except KeyError:
        logging.debug(f'{string} cannot be empty')
        sys.exit()
    except:
        logging.debug('[Error] Something else failed')
        sys.exit()


def get_user_input():
    input_list = {'1':'production', '2':'development', '3':'exit',}
    comment = """\n\tThis script makes toggling between dev and prod environment
    \tfor autopkg easier. Please select from the options below:\n"""
    print(comment)
    for i, v in input_list.items():
        print(f"{i}: {v}")
    user_input = int(input('What environment are you working on today?:\n '))
    return user_input

def run_cmd_api_user(api_user):
    out_put = subprocess.run([
                'defaults',
                'write',
                'com.github.autopkg',
                'API_USERNAME',
                '-string',
                 api_user], 
                         stderr=subprocess.PIPE, 
                         universal_newlines=True)
    if not out_put.stderr:
        logging.debug("succesfully wrote api_user")
    

def run_cmd_api_pw(pw):
    out_put = subprocess.run([
                'defaults',
                'write',
                'com.github.autopkg',
                'API_PASSWORD',
                '-string',
                 pw], 
                         stderr=subprocess.PIPE, 
                         universal_newlines=True)
    if not out_put.stderr:
        logging.debug("succesfully wrote api_password")

def run_cmd_url(url):
    out_put = subprocess.run([
                'defaults',
                'write',
                'com.github.autopkg',
                'JSS_URL',
                '-string',
                 url], 
                         stderr=subprocess.PIPE, 
                         universal_newlines=True)
    if not out_put.stderr:
        logging.debug("succesfully wrote url")

def swap_to_development():
    # get dev info
    dev_user = checkenviron_var('JSS_DEV_USER')
    dev_pw = checkenviron_var('JSS_DEV_PASSWORD')
    run_cmd_api_user(dev_user)
    run_cmd_api_pw(dev_pw)
    run_cmd_url(dev_url)
    

def swap_to_production():
    # get dev info
    prod_user = checkenviron_var('JSS_USER')
    prod_pw = checkenviron_var('JSS_PASSWORD')
    run_cmd_api_user(prod_user)
    run_cmd_api_pw(prod_pw)
    run_cmd_url(prod_url)

def confirm_swap():
    out_put_user = subprocess.run([
                'defaults',
                'read',
                'com.github.autopkg',
                'API_USERNAME'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)

    print("api_user" + ": " + out_put_user.stdout)

    out_put_pw = subprocess.run([
                'defaults',
                'read',
                'com.github.autopkg',
                'API_PASSWORD'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    print("api_password" + ": " + out_put_pw.stdout)


def main():   
    user_input = get_user_input()
    if user_input == 1:
        logging.debug("Changing to production...")
        swap_to_production()
        confirm_swap()
    elif user_input == 2:
        logging.debug("Changing to development...")
        swap_to_development()
        confirm_swap()
    else:
        sys.exit()


if __name__ == "__main__":
    main()

