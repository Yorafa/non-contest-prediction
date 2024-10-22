from LeetcodeAPI import LeetcodeAPI, load_headers
from typing import List, Dict
from tqdm import tqdm
import json
import requests

def get_all_questions(limit: int = 50) -> List[Dict]:
    hds = load_headers()
    leetcode = LeetcodeAPI(hds)
    skip = 0
    res = leetcode.problemList(0, 1)
    total = res["problemsetQuestionList"]["total"]
    results = []
    for skip in tqdm(range(0, total, limit)):
        res = leetcode.problemList(skip, limit)
        results += res["problemsetQuestionList"]["questions"]
    return results

def get_question_stats(titleSlug: str) -> Dict:
    hds = load_headers()
    leetcode = LeetcodeAPI(hds)
    res = leetcode.questionStats(titleSlug)
    # leetcode.com return a string, we need to convert it to a dict
    res = res["question"]["stats"]
    res = json.loads(res)
    return res

def get_ratings() -> Dict:
    url = "https://zerotrac.github.io/leetcode_problem_rating/data.json"
    res = requests.get(url)
    res = res.json()
    ratings = {}
    for r in tqdm(res):
        ratings[r["ID"]] = r
    return ratings

def merge_question_ratings(questions: List[Dict], ratings: Dict):
    for q in tqdm(questions):
        dic_info = ratings.get(q["frontendQuestionId"], {})
        q["rating"] = None
        if not dic_info or dic_info["TitleSlug"] != q["titleSlug"]:
            # print(f"Error: {q['frontendQuestionId']} {q['titleSlug']}")
            continue
        q["rating"] = dic_info["Rating"]
    return questions

def merge_question_stats(questions: List[Dict]):
    for q in tqdm(questions):
        dic_info = get_question_stats(q["titleSlug"])
        # merge the stats to the question
        q.update(dic_info)
    return questions

def save_questions(questions, path: str = "../data/questions.json"):
    with open(path, 'w', encoding="utf-8") as w:
        json.dump(questions, w, ensure_ascii=False, indent=4)
    
def load_questions(path: str = "../data/questions.json"):
    with open(path, 'r', encoding="utf-8") as r:
        return json.load(r)

def save_ratings(ratings, path: str = "../data/ratings.json"):
    with open(path, 'w', encoding="utf-8") as w:
        json.dump(ratings, w, ensure_ascii=False, indent=4)

def load_ratings(path: str = "../data/ratings.json"):
    with open(path, 'r', encoding="utf-8") as r:
        return json.load(r)

if __name__ == "__main__":
    questions = get_all_questions()
    ratings = get_ratings()
    save_questions(questions)
    save_ratings(ratings)
    # questions = load_questions()
    # ratings = load_ratings()
    questions = merge_question_ratings(questions, ratings)
    questions = merge_question_stats(questions)
    save_questions(questions, "../data/questions_with_rating.json")