import requests

url = "https://open.spotify.com/user/31junzitapcjrhhvlvg2ofuwwsey/recently-played-artists"

html = requests.get(url).text

print(len(html))
print(html[:1000])