import requests, pprint, random
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
    # print(s)
    r2 = requests.get(s).json()
    if r2['status'] == 'FAILED':
        print("request failed")
    else:
        rows = r2['result']['rows']

        for row in rows[1:]:
            p = row['problemResults']
            temp = "ABCDEFGHIJKLMNOPQRSTUVWZYZ"
            i = 0
            solved = []
            for i in range(len(p)):
                if p[i]['points'] > 0.0:
                    solved.append(temp[i])
            # print(row['party']['members'])
            # print(*solved)
            if problemId in solved:
                return False
    return True

def get_n_unsolved_problems(n, ratingwise_problems, rating, handles):
    unsolved = []
    while True:
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
    handles = ['yashwant_singh', 'deepanshu_pali', '0xero7', 'ravishekr7']

    ratingwise_problems = retrive_all_problems()
    print(len(ratingwise_problems[800]))

    # print(is_problem_unsolved(handles, 1401, 'A'))
    # print(is_problem_unsolved(handles, 1401, 'B'))
    # print(is_problem_unsolved(handles, 1401, 'C'))
    # print(is_problem_unsolved(handles, 1401, 'D'))
    # print(is_problem_unsolved(handles, 1401, 'E'))
    # print(is_problem_unsolved(handles, 1401, 'F'))

    print(get_n_unsolved_problems(5, ratingwise_problems, 800, handles))


if __name__ == "__main__":
    main()
