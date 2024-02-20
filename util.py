# 查询余额

import requests
import datetime
import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

# 填入api-key
# apikey = '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'
apikey = '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'


def check_usage(apikey):
    # check openai usage
    
    total = 0
    total_usage = 0
    apikey = apikey
    subscription_url = "https://api.openai.com/v1/dashboard/billing/subscription"
    headers = {
        "Authorization": "Bearer " + apikey,
        "Content-Type": "application/json"
    }
    subscription_response = requests.get(subscription_url, headers=headers)
    if subscription_response.status_code == 200:
        data = subscription_response.json()
        total = data.get("hard_limit_usd")
    else:
        print(subscription_response.text)
    start_date = (datetime.datetime.now() - datetime.timedelta(days=99)).strftime("%Y-%m-%d")
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    billing_url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
    billing_response = requests.get(billing_url, headers=headers)
    if billing_response.status_code == 200:
        data = billing_response.json()
        total_usage = data.get("total_usage") / 100
    else:
        print(billing_response.text)
    print(f"Total: {total} USD", f"Total Usage: {total_usage} USD", f"Remaining: {total - total_usage} USD")

if __name__ == '__main__':
    check_usage(apikey)