import requests

userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
header = {
    # "origin": "https://jira.byton.com",
    "Referer": "https://jira.byton.com/login.jsp",
    'User-Agent': userAgent,
}

def jiraLogin(account, pwd):
    print("Start to login jira")
    postUrl = "https://jira.byton.com/login.jsp"
    postData = {
        "os_username": account,
        "os_password": pwd,
    }

    responseRes = requests.post(postUrl, data=postData, headers=header)
    print(f"statusCode = {responseRes.status_code}")
    print(f"text = {responseRes.text}")


if __name__ == '__main__':
    login_name = 'longfei.li'
    login_pwd = 'Byton0903[]\;'
    jiraLogin(login_name, login_pwd)