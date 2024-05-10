import requests
import socket

def get_local_ip_address():
    hostname = socket.gethostname()
    ip_addresses = socket.getaddrinfo(hostname, None)
    ipv4_addresses = [ip[4][0] for ip in ip_addresses if ip[0] == socket.AF_INET]
    return ipv4_addresses

myIP = get_local_ip_address()[0]
myPort = 8000

# 엔드포인트 URL
url = "http://"+str(myIP)+":"+str(myPort)+"/mileleage/flogging"
print(url)
# 이미지 파일 경로
image_path = "./empty.jpg"

# 쿠키 정보
cookies = {
    "user_id": "admin",
    "user_pw": "1234",
    "user_name" : "admin"
}

try:
    # 이미지 파일 열기
    
    #response = requests.post(url, cookies=cookies, files={"image": open(image_path, 'rb')})
    response = requests.post(url, cookies=cookies, files={"image": image_path})
    # 응답 확인
    if response.status_code == 200:
        print("요청이 성공적으로 처리되었습니다.")
        print(response.json())  # 서버에서 반환한 JSON 응답 확인
    else:
        print(f"요청 실패 - 상태 코드: {response.status_code}")
except Exception as e:
    print(f"요청 실패 - 에러: {e}")
