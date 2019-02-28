import argparse
import requests
import subprocess

parser = argparse.ArgumentParser()
# declare the arguments
parser.add_argument("--param1")
parser.add_argument("--param2")
parser.add_argument("--param3")
parser.add_argument("--param4")
parser.add_argument("--param5")
parser.add_argument("--input")


# parse the actual arguments
args = parser.parse_args()
print("Starting Run. "
   + "Param1 = " + str(args.param1)
   + ", Param2 = " + str(args.param2)
   + ", Param3 = " + str(args.param3)
   + ", Param4 = " + str(args.param4)
   + ", Param5 = "+ str(args.param5)
)

input = str(args.input)
param1 = str(args.param1)
param2 = str(args.param2)
param3 = str(args.param3)
param4 = str(args.param4)
param5 = str(args.param5)
problem = str(args.problem-id)



subprocess.run(['git', 'clone'])

url = "http://127.0.0.1:5000/result"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"score\"\r\n\r\n{}\n\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"result\"\r\n\r\n{}\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"param1\"\r\n\r\n{}\n\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"param2\"\r\n\r\n{}\n\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"param3\"\r\n\r\n{}\n\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"param4\"\r\n\r\n{}\n\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"param5\"\r\n\r\n{}\n\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"problem\"\r\n\r\n{}\r\n" \
          "------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(score, result, param1, param2, param3, param4, param5, problem)
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'postman-token': "685fab5d-6fe3-785a-878a-5ee0b18e3c14"
    }

_ = requests.request("POST", url, data=payload, headers=headers)
