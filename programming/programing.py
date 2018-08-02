import json
import requests
from bs4 import BeautifulSoup



def isbracket(c):
    if (c == '(' or c == '[' or c == '{' or c == '}' or c == ']' or c == ')'):
        return True
    return False

def isopposite(a,b):
    if (a == '(' and b == ')'):
        return True
    elif (a == '{' and b == '}'):
        return True
    elif (a == '[' and b == ']'):
        return True
    else:
        return False

def update(handle):
    url = "https://www.codechef.com/users/"+handle
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.find_all('script')[36]
    startindex = script.text.find("all_rating")
    while (script.text[startindex] != '['):
        startindex = startindex + 1
    endindex = startindex + 1
    stack = ['[']
    while (len(stack) > 0):
        if (isbracket(script.text[endindex])):
            if (isopposite(stack[len(stack)-1],script.text[endindex])):
                stack.pop()
            else:
                stack.append(script.text[endindex])
        endindex = endindex + 1
    return script.text[startindex:endindex]

def getUserRating(handlename):
	res = requests.get('http://codeforces.com/api/user.rating?handle='+handlename)
	return res.text


def cleanurl(url):
    if (url.find("codeforces.com") != -1):
        begin = url.find("codeforces.com") + len("codeforces.com")
        url = url[begin:]
    url.strip()
    return url

def accepted(datadiv):
    status = datadiv.find_all('td')[5].find_all('span')[1].text
    if (status == "Accepted"):
        return True
    return False

def dailychallengeupdate(handle, problemName):
    data = requests.get("https://codeforces.com/api/user.status?handle="+handle)
    data = json.loads(data.text)
    for i in data['result']:
        if i['problem']['name'] in problemName:
            if i['verdict'] == 'OK':
                return True
    return False
