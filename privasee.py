import requests
import subprocess
import zipfile
import os
import stat

# Checks if LBRYNET is installed
# If not, it calls InstalLBRYNet, if it is it starts it
def StartLBRYNet():
    try:
        with open("lbrynet.log", "a") as log:
            lbrynet = subprocess.Popen(["lbrynet", "start"], stdout=log, stderr=log)
    except:
        InstalLBRYNet()

# Installs latest build of LBRYNET and moves it to the appropriete directory.
def InstalLBRYNet():
    lbrynetdl = requests.get("https://github.com/lbryio/lbry-sdk/releases/latest/download/lbrynet-mac.zip")
    open("lbrynet.zip","wb").write(lbrynetdl.content)
    zip = zipfile.ZipFile("lbrynet.zip")
    zip.extractall(path="/usr/local/bin/")
    os.remove("lbrynet.zip")
    execstat = os.stat("/usr/local/bin/lbrynet")
    os.chmod("/usr/local/bin/lbrynet", execstat.st_mode | stat.S_IEXEC)
    StartLBRYNet()


# Start lbrynet if not running
try:
    requests.post("http://localhost:5279")
except:
    StartLBRYNet()


# Uses LBRYNet to get content
def playContent(uri):
    request = requests.post("http://localhost:5279", json={"method": "get", "params": {"uri": uri}}).json()
    if request.get("result").get("streaming_url") == None:
        print("Oops, not a valid URI.\n")
        return
    print(request.get("result").get("streaming_url"))
    # videoplayer = subprocess.Popen(["mpv", request.get("result").get("streaming_url")], stdout=None, stderr=None)
    print("Your video was downloaded to " + str(request.get("result").get("download_path")))

# Search content using LBRYNet and make the user choose one to download
def searchContent(searchterm):
    request = requests.post("http://localhost:5279", json={"method": "claim_search", "params": {"text": searchterm}}).json()
    results = request.get("result").get("items")
    resulturis = []
    for i in range(len(results)):
        result = results[i]
        resulturis.append(result.get("canonical_url"))
        try:
            print(f'{i}: {result.get("value").get("title")} - {result.get("signing_channel").get("value").get("title")}')
        except:
            print(f'{i}: {result.get("value").get("title")}')
    def choose():
        choice = input("Input the number of the video you want to watch (-1 to search again): ")
        if choice == "-1":
            return
        try:
            playContent(resulturis[int(choice)])
            return
        except:
            print("Not found in list")
            choose()
    choose()

while True:
    searchContent(input("Search: "))
