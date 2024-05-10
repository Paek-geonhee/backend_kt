import requests
import socket
# 엔드포인트 URL
def get_local_ip_address():
    hostname = socket.gethostname()
    ip_addresses = socket.getaddrinfo(hostname, None)
    ipv4_addresses = [ip[4][0] for ip in ip_addresses if ip[0] == socket.AF_INET]
    return ipv4_addresses

myIP = get_local_ip_address()[0]
myPort = 8000
url = "http://" + str(myIP) +':'+ str(myPort) + "/flogging"

print("url", url)

# 이미지 파일 경로
image_path = "./empty.jpg"

# 쿠키 정보
cookies = {
    "id": "admin",
    "user_name": "1234"
}

try:
    # 이미지 파일 열기
    with open(image_path, "rb") as f:
        image_data = f.read()

    # POST 요청 보내기
    response = requests.post(url, files={"image": image_data}, cookies=cookies)

    # 응답 확인
    if response.status_code == 200:
        print("요청이 성공적으로 처리되었습니다.")
        print(response.json())  # 서버에서 반환한 JSON 응답 확인
    else:
        print(f"요청 실패 - 상태 코드: {response.status_code}")
except Exception as e:
    print(f"요청 실패 - 에러: {e}")