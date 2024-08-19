import instaloader
import json
import os
from dotenv import load_dotenv

L = instaloader.Instaloader()
load_dotenv()

name = os.getenv("INSTA_NAME")
password = os.getenv("INSTA_PASS")

def save_followers(name, followers):
    followers_list = [user.username for user in followers]
    with open(f'{name}_followers.json', 'w') as f:
        json.dump(followers_list, f)

def load_followers(name):
    file_path = f'{name}_followers.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = f.read().strip()
                if data:  
                    return set(json.loads(data))
                else:
                    return set()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading followers: {e}")
            return set()
    return set()

try:
    L.login(name, password)
except instaloader.exceptions.BadResponseException:
    print("Invalid Username or Password")
    exit()

profile = instaloader.Profile.from_username(L.context, name)
current_followers = set(profile.get_followers())
print(f"People who follow you: {len(current_followers)}")
previous = load_followers(name)
print(f"Previous followers: {len(previous)}")

save_followers(name, current_followers)
unf = previous - current_followers

if unf:
    print("People who unfollowed you:")
    for user in unf:
        print(user.username)
else:
    print("No one unfollowed you")
