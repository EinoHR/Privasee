import requests
import subprocess
import zipfile
import os
import stat

# Checks if LBRYNET is installed
# If not, it calls install_lbrynet, if it is it starts it
def start_lbrynet():
    try:
        with open("lbrynet.log", "w") as log:
            print("Starting LBRYNet...")
            log.seek(0)
            log.truncate()
            lbrynet = subprocess.Popen(["lbrynet", "start"], stdout=log, stderr=log)
    except:
        print("LBRYNet not found. Installing...")
        install_lbrynet()

# Installs latest build of LBRYNET and moves it to the appropriete directory.
def install_lbrynet():
    lbrynetdl = requests.get("https://github.com/lbryio/lbry-sdk/releases/latest/download/lbrynet-mac.zip")
    open("lbrynet.zip","wb").write(lbrynetdl.content)
    zip = zipfile.ZipFile("lbrynet.zip")
    zip.extractall(path="/usr/local/bin/")
    os.remove("lbrynet.zip")
    execstat = os.stat("/usr/local/bin/lbrynet")
    os.chmod("/usr/local/bin/lbrynet", execstat.st_mode | stat.S_IEXEC)
    start_lbrynet()

def is_running():
    request = requests.post("http://localhost:5279", json={"method": "status", "params": {}}).json()
    return request.get("result").get("is_running")

# Start lbrynet if not running
try:
    requests.post("http://localhost:5279")
except:
    start_lbrynet()


# Uses LBRYNet to get content
def play_content(uri):
    request = requests.post("http://localhost:5279", json={"method": "get", "params": {"uri": uri}}).json()
    if request.get("result").get("streaming_url") == None:
        print("Oops, not a valid URI.\n")
        return
    print(request.get("result").get("streaming_url"))
    # videoplayer = subprocess.Popen(["mpv", request.get("result").get("streaming_url")], stdout=None, stderr=None)
    print("Your video was downloaded to " + str(request.get("result").get("download_path")))

# Search content using LBRYNet and make the user choose one to download
def search_content(searchterm):
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
            play_content(resulturis[int(choice)])
            return
        except:
            print("Not found in list")
            choose()
    choose()

# while True:
#     pass