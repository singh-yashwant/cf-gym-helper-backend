# cf-gym-helper API

### GET request format
This is a sample request
{
    "handles": ["yashwant_singh", "0xero7"],
    "problems": {
        "800": 3,
        "1200": 4,
    }
}

## return object 
Return object for above request
{
    "Status": true,
    "data": {
        "800": [
            "https://codeforces.com/problemset/problem/1270/A",
            "https://codeforces.com/problemset/problem/1104/A",
            "https://codeforces.com/problemset/problem/769/A"
        ],
        "1200": [
            "https://codeforces.com/problemset/problem/1433/D",
            "https://codeforces.com/problemset/problem/1013/B",
            "https://codeforces.com/problemset/problem/1491/B",
            "https://codeforces.com/problemset/problem/802/M"
        ]
    }
}

with *HTTP 200" response

## Keys explained
- In "handles": [], include all the handles you want to get unique unsolved problems for
- In "problems", include the key value pairs about the details of the problems requried, eg in above request we asked for 3 800 rating and 4 1200 rating problems