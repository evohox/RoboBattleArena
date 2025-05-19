import requests
import json

class Tournament:
    def __init__(self, id, login, password, api_url):
        self.api_url = api_url
        self.id = id
        self.auth(login, password)
        
    def auth(self, login, password):
        response = requests.get(f"{self.api_url}/login?login={login}&password={password}")
        print(response.json().get('token'))
        self.token = response.json().get('token')
        self.fight_id = response.json().get('fight_id')
        
        
    def set_fight(self, id, stat, apiurl):
        url = f"{apiurl}/api/fights/{id}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "fight_id": id,
            "fight_state": stat
        }
        
        response = requests.post(
            url,
            headers=headers,
            cookies={"token": self.token},
            data=json.dumps(data),
            allow_redirects=True,
            timeout=None
        )
        
        return response.status_code
    
    def set_ready(self, id, stat, apiurl):
        url = f"{apiurl}/api/fights/{id}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "fight_id": id,
            stat: "1"
        }
        
        response = requests.post(
            url,
            headers=headers,
            cookies={"token": self.token},
            data=json.dumps(data),
            allow_redirects=True,
            timeout=None
        )
        
        return response.status_code
    
    def reload_page(self, apiurl):
        url = f"{apiurl}/events"
        response = requests.post(
            url
        )
        
        return response.status_code