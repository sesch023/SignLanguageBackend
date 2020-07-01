import requests

urls = ["https://jupiter.fh-swf.de/sign-language/cnn_5_150_150",
        "https://jupiter.fh-swf.de/sign-language/vgg19_224_224"]

payload = {}
headers = {}

for url in urls:
    response = requests.post(url, headers=headers, data=payload, files=[
        ('image', open('examples\\e.jpg', 'rb'))
    ])
    print(response.text.encode('utf8'))
