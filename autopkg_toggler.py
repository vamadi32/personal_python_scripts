#!/usr/bin/python3
 
# Created by Victor to toggle dev or prod for autopkg
import os
import sys, logging, subprocess
import argparse

logging.basicConfig(level=logging.DEBUG, 
format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)
logging.info('Start of Program')


def checkenviron_var(string):
    try:
        return os.environ[string]
    except KeyError:
        logging.debug(f'{string} cannot be empty')
        sys.exit()
    except:
        logging.debug('[Error] Something else failed')
        sys.exit()

def setup_parse():
    parser = argparse.ArgumentParser(description="""
    This script would help with toggling between a development
    and a production environment when using Autopkg
    """)
    parser.add_argument('endpoint', choices=['prod', 'dev'], default='dev', 
    help='The environment you are working in')
    args = parser.parse_args()

    return args.endpoint

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
        logging.info("succesfully wrote api_user")
    

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
        logging.info("succesfully wrote api_password")

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
        logging.info("succesfully wrote url")

def swap_to_development():
    # get dev info
    dev_user = checkenviron_var('JSS_DEV_USER')
    dev_pw = checkenviron_var('JSS_DEV_PASSWORD')
    dev_url = checkenviron_var('JSS_DEV_URL')
    run_cmd_api_user(dev_user)
    run_cmd_api_pw(dev_pw)
    run_cmd_url(dev_url)
    

def swap_to_production():
    # get dev info
    prod_user = checkenviron_var('JSS_USER')
    prod_pw = checkenviron_var('JSS_PASSWORD')
    prod_url=checkenviron_var('JSS_URL')
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
    logging.info("Api user" + ": " + out_put_user.stdout)
    out_put_pw = subprocess.run([
                'defaults',
                'read',
                'com.github.autopkg',
                'API_PASSWORD'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    logging.info("Api password" + ": " + out_put_pw.stdout)
    out_put_url = subprocess.run([
                'defaults',
                'read',
                'com.github.autopkg',
                'JSS_URL'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)
    logging.info("Jamf pro url" + ": " + out_put_url.stdout)

def main():
    arg_environment = setup_parse()
    logging.info(f"Chosen environment: {arg_environment}")

    if arg_environment == 'prod':
        logging.info("Changing to production...")
        swap_to_production()
        confirm_swap()
    if arg_environment == 'dev':
        logging.info("Changing to development...")
        swap_to_development()
        confirm_swap()

if __name__ == "__main__":
    main()

