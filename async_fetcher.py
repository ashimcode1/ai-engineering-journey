import asyncio
import httpx
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

async def fetch_github_user(client, username):
    url = f"https://api.github.com/users/{username}"
    logger.info(f"Fetching: {username}")
    
    try:
        response = await client.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Got data for {username}")
            return {"username": username, "name": data.get("name", "N/A"), "followers": data["followers"]}
        
        elif response.status_code == 404:
            logger.warning(f"User '{username}' not found")
            return None
        
        else:
            logger.error(f"Unexpected status: {response.status_code}")
            return None
    
    except httpx.TimeoutException:
        logger.error(f"Timeout fetching {username}")
        return None

async def fetch_all_users(usernames):
    async with httpx.AsyncClient() as client:
        tasks = [fetch_github_user(client, username) for username in usernames]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

async def main():
    usernames = ["torvalds", "gvanrossum", "antirez", "yudkowsky"]
    
    logger.info(f"Fetching {len(usernames)} users simultaneously")
    
    start = time.time()
    users = await fetch_all_users(usernames)
    elapsed = time.time() - start
    
    print(f"\nFetched {len(users)} users in {elapsed:.2f} seconds\n")
    
    for user in users:
        print(f"Name      : {user['name']}")
        print(f"Username  : {user['username']}")
        print(f"Followers : {user['followers']:,}")
        print("---")

asyncio.run(main())