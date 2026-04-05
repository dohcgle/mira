import urllib.request
import urllib.error
try:
    url = 'http://localhost:8000/api/loans/4/doc/buyruq/'
    with urllib.request.urlopen(url) as response:
        print(f"Status: {response.status}")
        print(f"Content-Type: {response.getheader('Content-Type')}")
        # PDF bo'lsa baytlarni o'qimasligimiz mumkin
except urllib.error.HTTPError as e:
    print(f"Status: {e.code}")
    print(e.read().decode()[:5000])
except Exception as e:
    print(f"Error: {e}")
