import requests, random
from collections import defaultdict


def retrive_all_problems():
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

def is_problem_unsolved(handles, contestId, problemId):
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

def get_n_unsolved_problems(n, ratingwise_problems, rating, handles):
    unsolved = []
    for p in ratingwise_problems[rating]:
        print("checking", p)
        if is_problem_unsolved(handles, p[0], p[1]):
            print("valid")
            unsolved.append(p)
        else:
            print("invalid")
        if len(unsolved) == n:
            return unsolved

def main():
    f1 = open('handles.txt', 'r')
    f2 = open('problems.txt', 'w')
    handles = f1.read().split('\n')

    ratingwise_problems = retrive_all_problems()

    print("Enter number of unique rating problems: ")
    t = int(input())
    print("Enter number of problems of each type: ")
    n = int(input())

    types = []
    for i in range(1, t+1):
        print("Enter the rating of problem type {}[800 - 3500]: ".format(i))
        types.append(int(input()))
        
    for t in types:
        f2.write("Rating: " + str(t) + '\n')
        unsolved = get_n_unsolved_problems(n, ratingwise_problems, t, handles)
        for u in unsolved:
            ind = str(u[0]) + u[1]
            link = 'https://codeforces.com/problemset/problem/{}/{}'.format(u[0], u[1])
            f2.write(ind + " : " + link + "\n")
        f2.write("\n")

    f1.close()
    f2.close()

if __name__ == "__main__":
    main()

