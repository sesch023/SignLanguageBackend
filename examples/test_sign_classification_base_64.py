import requests
import base64

urls = [
    "https://jupiter.fh-swf.de/sign-language/150x150_cnn_5",
    "https://jupiter.fh-swf.de/sign-language/224x224_vgg19",
    "https://jupiter.fh-swf.de/sign-language/224x224_vgg19_v2",
    "https://jupiter.fh-swf.de/sign-language/224x224_vgg19_v3",
    "https://jupiter.fh-swf.de/sign-language/150x150_cnn_5_v2"
]

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
