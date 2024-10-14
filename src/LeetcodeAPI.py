from typing import Dict
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

def load_headers():
    hds = {}
    with open("hds.txt", 'r', encoding="utf-8") as r:
        for line in r.readlines():
            sep = line.find(":")
            if sep != -1:
                hds[line[:sep]] = line[sep+1:].strip()
    return hds

class LeetcodeAPI:
    def __init__(self, headers: Dict) -> None:
        self.baseURL = "https://leetcode.com"
        self.headers = headers
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://leetcode.com/graphql/", headers=headers)
        # Create a GraphQL client using the defined transport
        self.client = Client(transport=transport, fetch_schema_from_transport=False)

    def problemList(self, skip: int, limit: int) -> Dict:
        query = gql("""\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    """)
        variables = {"categorySlug": "all-code-essentials", "limit": "%d" % limit, "skip": "%d" % skip, "filters": {}}
        return self.client.execute(query,variable_values=variables, operation_name="problemsetQuestionList")
    
    def questionStats(self, titleSlug: str) -> Dict:
        query = gql("""\n    query questionStats($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    stats\n  }\n}\n    """)
        variables = {"titleSlug": titleSlug}
        return self.client.execute(query,variable_values=variables, operation_name="questionStats")