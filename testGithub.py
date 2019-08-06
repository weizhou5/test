import json
import base64
import requests
import sys
TOKEN="-token"
HOST="-host"
PROJECT="-project"
BRANCH="-branch"
MSG="-msg"
RP="-rp"
PATH="-path"
tokenKey = "token"
hostKey = "host"
msgKey = "msg"
projectKey = "project"
branchKey = "branch"
pathKey = "path"
contentKey = "content"
rpKey = "rp"
global namespace
global args
args = dict()
def getTreesha(token,host,projectName,branch):
    headers={'Authorization': 'token {}'.format(token)}
    url = "{}/repos/{}/branches/{}".format(host,projectName,branch)
    try:
        resp = requests.get(url,headers=headers)
        result = json.loads(resp.text)
        treeSha = result['commit']['commit']['tree']['sha']
        return treeSha
    except Exception as e:
        print('get tree sha error!')
        sys.exit(1)

def getTree(token,host,projectName,branch):
    treeSha = getTreesha(token,host,projectName,branch)
    headers={'Authorization': 'token {}'.format(token)}
    url = "{}/repos/{}/git/trees/{}?recursive=1".format(host,projectName,treeSha)
    try:
        resp = requests.get(url,headers=headers)
        data = json.loads(resp.text)
        result = [(d['path'], d['type']) for d in data['tree']]
        return result
    except Exception as e:
        print('get tree error!')
        sys.exit(1)

def isExistFile(token,host,projectName,filePath,branch):
    tree = getTree(token,host,projectName,branch)
    for tp in tree:
        if tp[0] == filePath:
            return True
    return False

def getFilesha(token,host,projectName,filePath,branch):
    headers={'Authorization': 'token {}'.format(token)}
    url = "{}/repos/{}/contents/{}?ref={}".format(host,projectName,filePath,branch)
    try:
        resp = requests.get(url,headers=headers)
        result = json.loads(resp.text)
        return result['sha']
    except Exception as e:
        print('get file sha error!')
        sys.exit(1)

def uploadFile(token,host,projectName,branch,commitMsg,filePath,content):
    headers={'Authorization': 'token {}'.format(token)}
    url = "{}/repos/{}/contents/{}".format(host,projectName,filePath)
    try:
        if isExistFile(token,host,projectName,filePath,branch):
            sha = getFilesha(token,host,projectName,filePath,branch)
            params = {'branch': '{}'.format(branch),'message': '{}'.format(commitMsg),'content': '{}'.format(base64.b64encode(content)),'sha': '{}'.format(sha)}
            resp = requests.put(url,data=json.dumps(params),headers=headers)
            print(resp.text)
        else:
            params = {'branch': '{}'.format(branch),'message': '{}'.format(commitMsg).format(commitMsg),'content': '{}'.format(base64.b64encode(content))}
            resp = requests.put(url,data=json.dumps(params),headers=headers)
            print(resp.text)
    except Exception as e:
        print('upload file error!')
        sys.exit(1)
def getNamespace(token,host):
    headers={'Authorization': 'token {}'.format(token)}
    url = "{}/user".format(host)
    try:
        resp = requests.get(url,headers=headers)
        print(resp.text)
        data = json.loads(resp.text)
        return data['login']
    except Exception as e:
        print("token or host error!")
        sys.exit(1)
def checkTokenAndHost(token,host):
    headers={'Authorization': 'token {}'.format(token)}
    url = "{}/user".format(host)
    try:
        resp = requests.get(url,headers=headers)
    except Exception as e:
        print("token or host error!")
        sys.exit(1)
def checkArgs():
    if len(sys.argv) != 15:
        return False
    if (TOKEN in sys.argv) == False:
        printUsage("missing {}!".format(TOKEN))
        return False
    if (HOST in sys.argv) == False:
        printUsage("missing {}!".format(HOST))
        return False
    if (PROJECT in sys.argv) == False:
        printUsage("missing {}!".format(PROJECT))
        return False
    if (BRANCH in sys.argv) == False:
        printUsage("missing {}!".format(BRANCH))
        return False
    if (MSG in sys.argv) == False:
        printUsage("missing {}!".format(MSG))
        return False
    if (PATH in sys.argv) == False:
        printUsage("missing {}!".format(PATH))
        return False
    if (RP in sys.argv) == False:
        printUsage("missing {}!".format(RP))
        return False
    for i in range(0,len(sys.argv)):
        if sys.argv[i] == TOKEN:
            args[tokenKey] = sys.argv[i + 1]
            if len(args[tokenKey]) == 0:
                print ("token is empty!")
                return False
        if sys.argv[i] == HOST:
            args[hostKey] = sys.argv[i + 1]
            if len(args[hostKey]) == 0:
                print ("host is empty!")
                return False
        if sys.argv[i] == PROJECT:
            args[projectKey] = sys.argv[i + 1]
            if len(args[projectKey]) == 0:
                print ("project is empty!")
                return False
        if sys.argv[i] == MSG:
            args[msgKey] = sys.argv[i + 1]
            if len(args[msgKey]) == 0:
                print ("msg is empty!")
                return False
        if sys.argv[i] == PATH:
            args[pathKey] = sys.argv[i + 1]
            if len(args[pathKey]) == 0:
                print ("path is empty!")
                return False
        if sys.argv[i] == BRANCH:
            args[branchKey] = sys.argv[i + 1]
            if len(args[branchKey]) == 0:
                print ("branch is empty!")
                return False
        if sys.argv[i] == RP:
            args[rpKey] = sys.argv[i + 1]
            if len(args[rpKey]) == 0:
                print ("branch is empty!")
                return False
    checkTokenAndHost(args[tokenKey],args[hostKey])
    return True
def readFile(path):
    status = False
    fileobj = open(path, 'r')
    try:
        fileContent = fileobj.read()
        args[contentKey] = fileContent
        status = True
    finally:
        fileobj.close()
    return status
if __name__ == "__main__":
    #print(getTreeSha("ec1e6170c79ec0df26a43b1544657142cd1ae0fe","https://api.github.com","weizhou5/test","master"))
    #print(getTree("ec1e6170c79ec0df26a43b1544657142cd1ae0fe","https://api.github.com","weizhou5/test","master"))
    #print(isExistFile("ec1e6170c79ec0df26a43b1544657142cd1ae0fe","https://api.github.com","weizhou5/test","test/testAPI.txt","master"))
    #print(getFilesha("ec1e6170c79ec0df26a43b1544657142cd1ae0fe","https://api.github.com","weizhou5/test","test/testAPI.txt","master"))
    #print(uploadFile("ec1e6170c79ec0df26a43b1544657142cd1ae0fe","https://api.github.com","weizhou5/test","master","test python github API","test/pythonTestAPI.txt","test python rest API 001"))
    status = checkArgs()
    if status == True:
        if readFile(args[pathKey]) == True:
            projectName = '{}/{}'.format(getNamespace(args[tokenKey],args[hostKey]),args[projectKey])
            uploadFile(args[tokenKey], args[hostKey], projectName, args[branchKey], args[msgKey], args[rpKey], args[contentKey])
    #        if isExistFile(args[tokenKey], args[hostKey], args[projectKey], args[rpKey], args[branchKey]) == True:
    #            uploadFile(args[tokenKey], args[hostKey], args[projectKey], args[branchKey], args[msgKey], "update", args[rpKey], args[contentKey])
    #        else:
    #            uploadFile(args[tokenKey], args[hostKey], args[projectKey], args[branchKey], args[msgKey], "create", args[rpKey], args[contentKey])
    #    else:
    #        print("Failed to read file!")
    #else:
    #    printUsage("parameter error!")
        #    uploadFile("CE5HrtuNtMc4Wjm2vjvB","https://git.lug.ustc.edu.cn",'test',"master","commit msg","update","test/test.txt","python test for gitlab api-----") 
    #downloadFile("PxVrbrQBWz-E9W3xSL3S","http://10.27.22.109",'test1',"master","README.md") 
    #downloadFile("PxVrbrQBWz-E9W3xSL3S","http://10.27.22.109",'test1',"master","test/test.txt") 
    #print getProjectId("PxVrbrQBWz-E9W3xSL3S","http://10.27.22.109",'dao')
    #print isExistFile("PxVrbrQBWz-E9W3xSL3S","http://10.27.22.109",'test1','test/test.txt')
    #print('test/test.txt'.replace('/','%2F'))
print(__name__)
