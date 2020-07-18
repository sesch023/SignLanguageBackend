import requests

urls = [
    "https://jupiter.fh-swf.de/sign-language/150x150_cnn_5",
    "https://jupiter.fh-swf.de/sign-language/224x224_vgg19",
    "https://jupiter.fh-swf.de/sign-language/224x224_vgg19_v2",
    "https://jupiter.fh-swf.de/sign-language/224x224_vgg19_v3",
    "https://jupiter.fh-swf.de/sign-language/150x150_cnn_5_v2"
]

payload = {}
headers = {}

for url in urls:
    response = requests.post(url, headers=headers, data=payload, files=[
        ('image', open('examples\\e.jpg', 'rb'))
    ])
    print(response.text.encode('utf8'))
