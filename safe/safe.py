import requests
import time
import datetime as dt
from discord_webhook import DiscordWebhook


class Request:

    BASE_URL = "https://safebooru.org"
    API_URL = "/index.php?page=dapi&s=post&q=index&json=1"
    IMG_URL = f"{BASE_URL}/images/"

    def __init__(self) -> None:
        pass

    def request(self, url: str):
        re = requests.get(url=url)
        return re.json()


class Posts(Request):
    def get_posts(self) -> list[dict[str, str]]:
        return self.request(self.BASE_URL + self.API_URL)

    def save(self, update_url: str, webhook_url: str) -> bool:
        data = self.get_posts()
        success = 0
        fail = 0
        s_list = []
        f_list = []
        try:
            for i in data:
                if i["image"].endswith(".gif"):
                    pass
                else:
                    headers = {
                        "id": str(i["id"]),
                        "tags": i["tags"],
                        "img": self.IMG_URL + i["directory"] + "/" + i["image"],
                    }
                    re = requests.get(url=update_url, headers=headers)
                    result = re.json()
                    if result["data"]:
                        success += 1
                        s_list.append(i["id"])
                    else:
                        fail += 1
                        f_list.append(i["id"])
                    time.sleep(1)
            s_text = f"성공갯수 : {success}\n{s_list}"
            f_text = f"실패갯수 : {fail}\n{f_list}"
            webhook = DiscordWebhook(url=webhook_url, content=self.log(s_text, f_text))
            response = webhook.execute()
            return True
        except Exception as E:
            print(E)
            return False

    def log(self, s_text, f_text):
        x = dt.datetime.now()
        times = x.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        txt = f"""
        {times} 실행결과
        -------------------------------------------------
        {s_text}

        {f_text}
        -------------------------------------------------
        """
        return txt
