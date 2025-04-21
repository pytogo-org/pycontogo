import socket





# no need to pip install anything
from urllib.request import urlopen  # to make the request to the API
import json  # to parse the API response

# declare your IP Address here
ip_address = "192.168.1.204"

# get your token from IPinfo's account dashboard
token = "607b2818596e6a"

# create the url for the API, using f-string


def host_IP():
    try:
        hname = socket.gethostname()
        hip = socket.gethostbyname(hname)
        print("Hostname:  ", hname)
        print("IP Address: ", hip)
        url = f"https://www.ipinfo.io/{ip_address}?token={token}"
        # call the API and save the response
        with urlopen(url) as response:
            response_content = response.read()
        
        data = json.loads(response_content)
        print(data)
        print(response_content)
    
    except:
        print("Unable to get Hostname and IP")


# Driver code
host_IP()  # Function call
