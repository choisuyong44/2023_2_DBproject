import requests

def get_public_ip():
    # get method 호출
    try:
        response = requests.get('https://httpbin.org/ip')
        if response.status_code == 200:
            data = response.json()
            public_ip = data.get('origin')
            return public_ip
        
        else:
            print("HTTP 요청이 실패하였습니다. 상태 코드:", response.status_code)
    
    # exception 처리            
    except requests.RequestException as e:
        print("오류 발생:", e)
        
    return None

