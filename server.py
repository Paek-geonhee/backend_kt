from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import socket

from routes import guideline_api, login_api, mileleage_api, animalcatalog_api


app = FastAPI()

# middleware - cors설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(guideline_api.router)
app.include_router(login_api.router)
app.include_router(mileleage_api.router)
<<<<<<< HEAD
app.include_router(animalcatalog_api.router)
=======
>>>>>>> 705fa18a19adbe70f19f8ddbab56445413e7287a
    


# IP 주소 변경
def get_local_ip_address():
    hostname = socket.gethostname()
    ip_addresses = socket.getaddrinfo(hostname, None)
    ipv4_addresses = [ip[4][0] for ip in ip_addresses if ip[0] == socket.AF_INET]
    return ipv4_addresses

myIP = get_local_ip_address()[0]
myPort = 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host=myIP, port=myPort, reload=True)
