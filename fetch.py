import requests

def get_user_contest_ranking_info(username):
    url = "https://leetcode.com/graphql/"
    headers = {
        "Content-Type": "application/json",
    }

    query = """
        query userContestRankingInfo($username: String!) {
          userContestRanking(username: $username) {
            attendedContestsCount
            rating
            globalRanking
            totalParticipants
            topPercentage
            badge {
              name
            }
          }
          userContestRankingHistory(username: $username) {
            attended
            trendDirection
            problemsSolved
            totalProblems
            finishTimeInSeconds
            rating
            ranking
            contest {
              title
              startTime
            }
          }
        }
    """

    variables = {
        "username": username,
    }

    payload = {
        "query": query,
        "variables": variables,
        "operationName": "userContestRankingInfo",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            contestList = data['data']['userContestRankingHistory']
            count = 2
            mostRecentContest = {'rating': 1500,'ranking': 25000}
            prevContest = {'rating': 1500}
            for contest in reversed(contestList):
                if contest['attended'] == True:
                    if count == 2:
                        mostRecentContest = contest
                    elif count == 1:
                        prevContest = contest
                    count-=1
                    if count == 0 : 
                        break
            data =  {
                'ratingChange' : mostRecentContest['rating']-prevContest['rating'],
                'prevRank': mostRecentContest['ranking'],
                'prevRating' : mostRecentContest['rating'],
                'attemptedContest' : data['data']['userContestRanking']['attendedContestsCount']
            }
            print('Added Succesfully')
            return data
        except:
            print('Got some error')
            return {
                'ratingChange' : '-1',
                'prevRank': '-1',
                'prevRating' : '-1',
                'attemptedContest' : '-1'
            }
    else:
        print("Error:", response.status_code, response.text)
