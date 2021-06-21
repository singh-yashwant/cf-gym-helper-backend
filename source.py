import requests, random
from collections import defaultdict

from flask_restful import Resource
from flask import request
import json

class Problems(Resource):
    def __init__(self):
        self.result = {"Status": True, "data": {}}

    def get(self):
        reqData = json.loads(request.data) if request.data else None
        if not handles:
            return {"Missing handles"}, 400
        handles = reqData["handles"]
        
        # remove invalid handles
        handles = self.validate_handles(handles)
        ratingwise_problems = self.retrive_all_problems()
        # print(ratingwise_problems.keys())

        problemsToFetch = reqData["problems"]
        print(problemsToFetch)
            
        for rating in problemsToFetch.keys():
            self.result["data"][rating] = []
            print("Rating: " + rating)
            unsolved = self.get_n_unsolved_problems(problemsToFetch[rating], ratingwise_problems, int(rating), handles)
            for u in unsolved:
                ind = str(u[0]) + u[1]
                link = 'https://codeforces.com/problemset/problem/{}/{}'.format(u[0], u[1])
                self.result["data"][rating].append(link)
                print(ind + " : " + link + "\n")
            
        print("ALL PROBLEMS FETCHED")
        return self.result, 200 


    def validate_handles(self, handles):
        for i in range(len(handles)):
            handles[i] = handles[i].strip()
        print("validating the handles")
        for h in handles:
            print("validating", h, end=" ")
            r = requests.get('https://codeforces.com/api/user.info?handles=' + h).json()
            print(r['status'])
            if(r['status'] == 'FAILED'):
                handles.remove(h)
        return handles

    def retrive_all_problems(self):
        r = requests.get('https://codeforces.com/api/problemset.problems').json()
        
        ratingwise_problems = defaultdict(lambda : [])
        if r['status'] == 'FAILED':
            print("request failed")
        else:
            problems = r['result']['problems']
            problems_statistics = r['result']['problemStatistics']

            for p in problems:
                try:
                    ratingwise_problems[p['rating']].append([p['contestId'], p['index']])
                except KeyError:
                    pass
    
        ans = dict(ratingwise_problems)
        for key in ans.keys():
            random.shuffle(ans[key])
        return ans

    def is_problem_unsolved(self, handles, contestId, problemId):
        s = 'https://codeforces.com/api/contest.standings?contestId={}&from=1&showUnofficial=true'.format(contestId) + '&handles=' + ';'.join(handles)
        r2 = requests.get(s).json()
        if r2['status'] == 'FAILED':
            print("request failed")
        else:
            rows = r2['result']['rows']
            problem_indices = []
            for p in r2['result']['problems']:
                problem_indices.append(p['index'])
            
            for row in rows[1:]:
                p = row['problemResults']
                i = 0
                solved = []
                for i in range(len(p)):
                    if p[i]['points'] > 0.0:
                        solved.append(problem_indices[i])
                if problemId in solved:
                    return False
        return True

    def get_n_unsolved_problems(self, n, ratingwise_problems, rating, handles):
        unsolved = []
        for p in ratingwise_problems[rating]:
            print("checking", p)
            if self.is_problem_unsolved(handles, p[0], p[1]):
                print("valid")
                unsolved.append(p)
            else:
                print("invalid")
            if len(unsolved) == n:
                return unsolved
