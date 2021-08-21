import requests
import subprocess
import zipfile

# Start lbrynet if not running
try:
    requests.post("http://localhost:5279")
except:
    startlbrynet()

def startLBRYnet():
    try:
        with open("lbrynet.log", "a") as log:
            lbrynet = subprocess.Popen(["lbrynet", "start"], stdout=log, stderr=log)
    except:
        instalLBRYnet()

def instalLBRYnet():
    lbrynetdl = requests.get("https://github.com/lbryio/lbry-sdk/releases/latest/download/lbrynet-mac.zip")
    open("lbrynet.zip","wb").write(lbrynetdl.content)
    lbrynetzip = ZipFile("lbrynet.zip")
    lbrynetzip.extractall(path="/usr/local/bin/")

def playContent(uri):
    request = requests.post("http://localhost:5279", json={"method": "get", "params": {"uri": uri}}).json()
    if request.get("result").get("streaming_url") == None:
        print("Oops, not a valid URI.\n")
        return
    print(request.get("result").get("streaming_url"))
    # videoplayer = subprocess.Popen(["mpv", request.get("result").get("streaming_url")], stdout=None, stderr=None)
    print("Your video was downloaded to " + str(request.get("result").get("download_path")))

while True:
    playContent(input("LBRY URI to play: \n"))