#!/usr/bin/python
import nmap 
import ipaddress
import re #Regular Exepressions
import requests

port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
port_min = 0
port_max = 65535

menu_options = {
    1: 'nmap',
    2: 'dirb',
    3: 'coming soon...',
    0: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
    while True:
        ip_add_entered = input("\nPlease enter the ip address that you want to scan: ")   
        try:
            ip_address_obj = ipaddress.ip_address(ip_add_entered)
            print("You entered a valid ip address.")
            break
        except:
            print("You entered an invalid ip address")


    while True:

        # You can scan 0-65535 ports. This scanner is basic and doesn't use multithreading so scanning all the ports is not advised.
        print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
        port_range = input("Enter port range: ")
        port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
        if port_range_valid:
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            break

    nm = nmap.PortScanner()
    for port in range(port_min, port_max + 1):
        try:
            result = nm.scan(ip_add_entered, str(port))
            port_status = (result['scan'][ip_add_entered]['tcp'][port]['state'])
            print(f"Port {port} is {port_status}")
        except:
            print(f"Cannot scan port {port}.")
        

def option2():
    def request(url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass

    target_url = input("Enter Target URL: ")

    file = open("Project_RedTeam/common.txt","r")
    for line in file:
        word = line.strip()
        full_url = target_url + "/" + word
        response = request(full_url)
        if response:
            print("Discovered directory at this link: " + full_url)

def option3():
    print("New Options available soon !")

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 0:
            print('Good Bye')
            exit()
        else:
            print('Invalid option. Please enter a number between 0 and 3.')
