import requests

url = "https://jupiter.fh-swf.de/sign-language/cnn_5_150_150"

payload = {}
files = [
  ('image', open('z.jpg', 'rb'))
]
headers = {}

response = requests.post(url, headers=headers, data=payload, files=files)

print(response.text.encode('utf8'))
