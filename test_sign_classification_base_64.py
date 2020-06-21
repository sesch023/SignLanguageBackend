import requests
import base64

url = "https://jupiter.fh-swf.de/sign-language/cnn_5_150_150"

with open("z.jpg", "rb") as image_file:
  encoded_string = base64.b64encode(image_file.read())

params = [
  ('image_base_64', encoded_string)
]
files = [

]
headers = {}

response = requests.post(url, headers=headers, data=params, files=files)

print(response.text.encode('utf8'))
