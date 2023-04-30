import json
from cipher import litencryptor
import mitmproxy.script
import mitmproxy.http
import logging
import requests




from panel import panel


class LitmatchAddon():
    applicationInfo = None
    uuid = None
    sessionId = None

    last_match_user = None

    

    def build_param(self) -> dict[str, str]:
        return {
            "sid": self.sessionId,
            "uuid": self.uuid,
            "platform": "android",
            "version": "6.15.0",
            "loc": "US",
        }


    def build_headers(self) -> dict[str, str]:
        return {
            "x-application-info": self.applicationInfo,
            "user-agent": "Mozilla/5.0 (Linux; Android 11; WayDroid x86_64 Device Build/RQ3A.211001.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Safari/537.36"
        }


    def info_by_huanxin(self, huanxin: str) -> dict[str, any]:
        response = requests.post("https://www.litatom.com/api/sns/v1/lit/user/info_by_huanxin",
                    params=self.build_param(),
                    headers=self.build_headers(),
                    data=litencryptor.encrypt_libguard(json.dumps({"ids":[huanxin]}), 3))
        print(response.text)
        return json.loads(response.text)


    def info(self, user_id: str) -> dict[str, any]:
        response = requests.get("https://www.litatom.com/api/sns/v1/lit/user/get_info/" + user_id,
                    params=self.build_param(),
                    headers=self.build_headers())
        print(response.text)
        return json.loads(response.text)


    def __init__(self) -> None:
        panel.start(self)
    def done(self):
        panel.close = True

    def response(self, flow: mitmproxy.http.HTTPFlow):
        decrypted_content = None
        if "Content-Type" not in flow.response.headers:
            return
        if flow.response.headers["Content-Type"] == 'application/json':
            decrypted_content = flow.response.content.decode()
        if flow.response.headers["Content-Type"] == "application/x-litatom-json":
            decrypted_content = litencryptor.decrypt_libguard(decrypted_content, 3)

        if decrypted_content is None:
            return
    
        decrypted_content = json.loads(decrypted_content)
        

        if flow.request.url.startswith("https://www.litatom.com/api"):
            if "x-application-info" in flow.request.headers:
                if self.applicationInfo == None:
                    logging.warn("Fetched login info!")
                self.applicationInfo = flow.request.headers["x-application-info"]
                self.uuid = flow.request.query["uuid"]
                self.sessionId = flow.request.query["sid"]
            if "api/sns/v1/lit/anoy_match" in flow.request.url:
                if "data" in decrypted_content and "matched_fake_id" in decrypted_content["data"]:
                    self.last_match_user = decrypted_content["data"]["matched_fake_id"]

addons = [LitmatchAddon()]