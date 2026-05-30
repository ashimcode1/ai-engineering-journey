import requests
import logging

logging.root.handlers = [] 

logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
logger = logging.getLogger(__name__)
def fetch_github_repos(username,max_repos=5):
        url = f"https://api.github.com/users/{username}/repos"
        headers={"Accept": "application/vnd.github.v3+json"}
        params={"sort": "stars",
            "direction": "desc",
            "per_page": max_repos}
        logger.info(f"fetching top {max_repos} for the {username}")   
        try:
            response=requests.get(url,headers=headers,params=params,timeout=10)
            if response.status_code==200:
                repos=response.json()
                logger.info(f"Got {len(repos)} repos")
                return repos
            elif response.status_code==404:
                logger.warning(f"failed :{response.status_code}")
                return []
            else:
                logger.error(f"Failed: {response.status_code}")
                return []
        
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            return []
        
        except requests.exceptions.ConnectionError:
            logger.error("No internet connection")
            return []

    # call it
repos = fetch_github_repos("torvalds", max_repos=5)
print(type(repos))   # ← ADD THIS
print(repos)         # ← AND THIS
for repo in repos:
    print(f"{repo['name']} — ⭐ {repo['stargazers_count']}")
