import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def fetch_questions(site, tagged=None, pagesize=5):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "activity",
        "site": site,
        "pagesize": pagesize,
        "filter": "withbody",
        "key": os.environ.get("STEX_API_KEY")
    }
    if tagged:
        params["tagged"] = tagged
    
    response = requests.get(url, params=params)
    return response.json().get("items", [])

def fetch_answers_for_post(site, post_id, post_type="questions"):
    url = f"https://api.stackexchange.com/2.3/{post_type}/{post_id}/answers"
    params = {
        "order": "desc",
        "sort": "activity",
        "site": site,
        "filter": "withbody",
        "key": os.environ.get("STEX_API_KEY")
    }

    response = requests.get(url, params=params)
    return response.json().get("items", [])

def fetch_comments_for_post(site, post_id, post_type="questions"):
    url = f"https://api.stackexchange.com/2.3/{post_type}/{post_id}/comments"
    params = {
        "order": "desc",
        "sort": "creation",
        "site": site,
        "filter": "withbody",
        "key": os.environ.get("STEX_API_KEY")
    }

    response = requests.get(url, params=params)
    return response.json().get("items", [])

if __name__ == "__main__":
    site = "bricks"
    questions = fetch_questions(site, tagged="python", pagesize=2)
    results = []
    for q in questions:
        comments = fetch_comments_for_post(site, q["question_id"])
        comments_body = [c.get("body", "") for c in comments]
        answers = fetch_answers_for_post(site, q["question_id"])
        answers_body = [a.get("body", "") for a in answers]
        results.append({
            "post": q.get("body", ""),
            "comments": comments_body,
            "answers": answers_body
        })
    print(json.dumps(results, indent=1))