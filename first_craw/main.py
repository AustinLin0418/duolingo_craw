from fastapi import FastAPI, HTTPException
from curl_cffi import requests

app = FastAPI()

# ================= 填入你的真實資料 =================
USERNAME = 'ur.austinlin'
JWT_TOKEN = '你的_JWT_TOKEN_超長字串'
# ====================================================

@app.get("/duolingo")
def get_duolingo_data():
    url = "https://duolingo.com"
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Type": "application/json"
    }
    query = """
    query ($username: String!) {
      user(username: $username) {
        streak
        totalXp
        gems
        lingots
      }
    }
    """
    payload = {"query": query, "variables": {"username": USERNAME}}
    
    try:
        # 在雲端伺服器上用 chrome 指紋硬扛破防！
        res = requests.post(url, json=payload, headers=headers, impersonate="chrome", timeout=10)
        if res.status_code == 200:
            user = res.json().get('data', {}).get('user', {})
            if user:
                return {
                    "streak": user.get("streak", 0),
                    "gems": user.get("gems") or user.get("lingots", 0),
                    "total_xp": user.get("totalXp", 0)
                }
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=res.status_code, detail="Blocked by Duolingo")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
