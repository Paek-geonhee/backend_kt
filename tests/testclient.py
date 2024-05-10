import requests

url = "http://172.21.109.192:8000/mileleage/flogging"

with open("C:/Users/jscha/OneDrive/Desktop/study&project/khuthon/test/timage.png", "rb") as f:
    image_data = f.read()

dict1 ={
    "type":"byte",
    "value" : bytes(image_data)
}

response = requests.post(url, data = dict1)

print(response.text)