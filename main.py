from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Free Domain Metrics Checker")

@app.get("/check-metrics")

def check_metrics(domain: str = Query(..., description="Domain URL to check")):
    try:
        url = "https://www.linkbuildinghq.com/wp-admin/admin-ajax.php"
        params = {
            "action": "get_moz_ahref_metrics",
            "target_url": domain
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.linkbuildinghq.com/"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        # Debug check: what is the actual content type?
        if "application/json" not in response.headers.get("Content-Type", ""):
            return {"error": "Did not receive JSON", "raw": response.text[:300]}

        data = response.json().get("data", {})

        return {
            "domain": domain,
            "Domain Authority": data.get("da", "N/A"),
            "Domain Rating": data.get("dr", "N/A"),
            "Spam Score": f"{data.get('spam_score', 'N/A')}%",
            "Page Authority": data.get("pa", "N/A"),
            "Site Traffic": data.get("org_traffic", "N/A"),
        }

    except Exception as e:
        return {"error": str(e)}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
