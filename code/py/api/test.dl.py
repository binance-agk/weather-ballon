import requests

url='https://www.grc.nasa.gov/WWW/K-12/airplane/Images/socdrag.jpg'
url='https://www.tradingview.com/x/lGCqNmdD/'
r = requests.get(url, stream=True)

with open('hh6.jpg', 'wb') as f:
    try:
        for block in r.iter_content(2020):
            f.write(block)
    except KeyboardInterrupt:
        print(KeyboardInterrupt.__str__())
        pass



