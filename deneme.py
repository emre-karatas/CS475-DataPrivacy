import requests

url = "https://www.instagram.com/tugrulsaglam06/?__a=1"
PROFILE_ENDPOINT2 = "https://graph.instagram.com/7277830478993793"

response = requests.get(PROFILE_ENDPOINT2)
print(response)