import requests
import base64

urls = ["https://jupiter.fh-swf.de/sign-language/cnn_5_150_150",
        "https://jupiter.fh-swf.de/sign-language/vgg19_224_224",
        "https://jupiter.fh-swf.de/sign-language/vgg19_224_224_v2"]

with open("examples\\e.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

params = [
    ('image_base_64', encoded_string)
]
files = [

]
headers = {}

for url in urls:
    response = requests.post(url, headers=headers, data=params, files=files)
    print(response.text)
