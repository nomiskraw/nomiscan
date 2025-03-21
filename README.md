# nomiscan

A Python script designed to scan open ports on a target host, and perform an SSH brute-force attack if the SSH service is available.

**Currently Implemented Features:**
- Scans open ports (e.g., SSH, HTTP, FTP, SMTP, DNS, Telnet, Remote Desktop).
- Identifies if SSH (port 22) is open.
- Performs asynchronous SSH brute-force attacks with username and password lists.

**Future Enhancements:**
- Extend brute-force capability to additional protocols (FTP, Telnet, SMTP, etc.).

## Requirements

Before running the script, install the following Python package:

```bash
pip install asyncssh
```

## Usage

```bash
python3 nomiscan.py <ip_address_or_hostname>
```

Upon execution, the script will:
1. Scan predefined common ports.
2. Prompt to initiate an SSH brute-force attack if SSH is detected as open.
3. Request username and password list files for the attack. (must be .txt files)

## Recommended Testing Setup

For testing purposes, it is recommended to set up a virtual lab environment:

Attacker Machine: Debian or similar Linux distribution with Python on it.

Victim Machine: Metasploitable 2 (https://docs.rapid7.com/metasploit/metasploitable-2) installed locally using VirtualBox.

This controlled environment helps ensure safe and ethical testing.

## Important Notes

- **Use this script responsibly and ethically.** Unauthorized scanning or brute-force attacks against systems without explicit permission are illegal and unethical.
- Intended primarily for cybersecurity education and penetration testing in controlled environments.
- for testing the script you can install an Metasploitable 2 server

