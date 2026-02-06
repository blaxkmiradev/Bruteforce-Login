
## 🚀 Features

* **Color-Coded Output:** Real-time visual feedback (Success/Failure/Errors).
* **Logging:** Valid credentials are automatically saved to `found.txt`.
* **Smart Parsing:** Handles `user:pass` combo lists efficiently.
* **Request Masking:** Includes custom User-Agent headers to simulate real browser traffic.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/blaxkmiradev/Bruteforce-Login.git]
   cd K-SEC
Install dependencies: Make sure you have Python installed, then run:

Bash

pip install requests colorama
📖 How To Use
Prepare your Combo List: Create a .txt file (e.g., combo.txt) with the format:

Plaintext

admin:admin123
user:password
root:toor
Run the Script:

Bash

python bruteforce.py
Enter Configuration:

Target URL: The login endpoint (e.g., http://simplelogin.com/api/login)

Parameter Names: The name attribute of the HTML input fields (e.g., username, password)

Success Message: A string the server returns only when login is successful (e.g., "Welcome", "token", or "status":true)

⚠️ Disclaimer
This tool is for educational purposes and authorized security testing only. Brute-forcing targets you do not own or have explicit permission to test is illegal. The developer (blaxkmiradev) is not responsible for any misuse or damage caused by this program.

👨‍💻 Credits
Built with ⚡ by blaxkmiradev
