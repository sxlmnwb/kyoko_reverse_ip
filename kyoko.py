#!/usr/bin/env python3

import requests
import os
from datetime import datetime
import threading

def display_banner():
    banner = """
██╗  ██╗██╗   ██╗ ██████╗ ██╗  ██╗ ██████╗ 
██║ ██╔╝╚██╗ ██╔╝██╔═══██╗██║ ██╔╝██╔═══██╗
█████╔╝  ╚████╔╝ ██║   ██║█████╔╝ ██║   ██║
██╔═██╗   ╚██╔╝  ██║   ██║██╔═██╗ ██║   ██║
██║  ██╗   ██║   ╚██████╔╝██║  ██╗╚██████╔╝
╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝                   
Welcome to KYOKO (Reverse IP Lookup. Based @elliottophellia)
Build on Python 3.x // Maintainer @sxlmnwb        
    """
    print(banner)

def reverse_ip(target, output_data):
    url = f"https://reverseip.rei.my.id/{target}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        result_list = result["RequestResult"]["ResultDomainList"]
        result_total = result["RequestResult"]["ResultDomainTotal"]
        output_data.append(f"{target} [{result_total}]")
        for result_domain in result_list:
            output_data.append(result_domain)
        print(f"{target} [{result_total}]")
    else:
        print(f"Failed to fetch data for target: {target}")

def main():
    display_banner()
    input_file = input("[INPUT DOMAIN LIST] > ")
    print()

    with open(input_file, 'r') as f:
        targets = f.read().splitlines()
    targets = [target.replace("http://", "").replace("https://", "").replace("www.", "") for target in targets]

    output_data = []

    threads = []
    for target in targets:
        thread = threading.Thread(target=reverse_ip, args=(target, output_data))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output_directory = os.path.join(os.getcwd(), "output")
    os.makedirs(output_directory, exist_ok=True)

    output_file = os.path.join(output_directory, f"{os.path.basename(input_file).split('.')[0]}-{datetime.utcnow().isoformat()}.log")

    with open(output_file, 'w') as f:
        for item in output_data:
            if "[" not in item:
                f.write("%s\n" % item)

    print(f"\n[SAVED ON] {output_file}")

if __name__ == "__main__":
    main()
