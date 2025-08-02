import os
import time
import requests
import re
import sys
from bs4 import BeautifulSoup as bs
from getpass import getpass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_post_id(url):
    try:
        response = requests.post('https://id.traodoisub.com/api.php', data={'link': url})
        return response.json().get('id')
    except:
        return None

def get_facebook_pages(user_access_token):
    url = 'https://graph.facebook.com/v18.0/me/accounts'
    headers = {'Authorization': f'Bearer {user_access_token}'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [{'name': page['name'], 'accessToken': page['access_token']} 
                    for page in response.json()['data']]
        return None
    except:
        return None

def display_header():
    clear_screen()
    print('\n\x1b[1;92m' + '='*50 + '\x1b[0m')
    print('\x1b[1;92m       FACEBOOK PAGE AUTO REACTION TOOL       \x1b[0m')
    print('\x1b[1;92m' + '='*50 + '\x1b[0m')
    print('\x1b[1;97mOwner     : Bryson\x1b[0m')
    print('\x1b[1;97mFB UID    : 61578130127315\x1b[0m')
    print('\x1b[1;97mGitHub    : bryyot\x1b[0m')
    print('\x1b[1;92m' + '='*50 + '\x1b[0m\n')

def auto_react():
    display_header()
    
    # Get hidden access token input
    token = getpass('\x1b[1;91mEnter the access token (hidden): \x1b[0m')
    
    # Get post URL (red color)
    post_url = input('\x1b[1;91mEnter the post URL: \x1b[0m')
    post_id = is_post_id(post_url)
    print(post_id)
    
    if not post_id:
        print("\x1b[1;91mInvalid post URL or couldn't get post ID\x1b[0m")
        input("\n\x1b[1;97mPress Enter to continue...\x1b[0m")
        return
    
    # Display reaction menu
    print("\n\x1b[1;97mChoose reaction type:\x1b[0m")
    print("\x1b[1;92m[1] LIKE    [3] HAHA\x1b[0m")
    print("\x1b[1;92m[2] LOVE    [4] WOW\x1b[0m")
    print("\x1b[1;92m[5] SAD     [6] ANGRY\x1b[0m")
    
    # Get reaction type (red color)
    reaction_choice = input('\x1b[1;91mSelect reaction (1-6): \x1b[0m')
    reactions = {
        '1': 'LIKE',
        '2': 'LOVE', 
        '3': 'HAHA',
        '4': 'WOW',
        '5': 'SAD',
        '6': 'ANGRY'
    }
    
    reaction_type = reactions.get(reaction_choice, 'LIKE')
    
    # Get delay (red color)
    try:
        delay = int(input('\x1b[1;91mEnter the delay between requests (in seconds): \x1b[0m'))
    except:
        delay = 1
    
    # Get user ID
    user_id = is_post_id(post_url.split('/posts/')[0])
    print(user_id)
    
    if not user_id:
        print("\x1b[1;91mCouldn't get user ID from URL\x1b[0m")
        input("\n\x1b[1;97mPress Enter to continue...\x1b[0m")
        return
    
    post_id = f"{user_id}_{post_id}"
    
    # Red "Please wait..." message
    print("\x1b[1;91mPlease wait...\x1b[0m")
    
    # Get pages
    pages = get_facebook_pages(token)
    if not pages:
        print("\x1b[1;91mNo pages found or invalid token\x1b[0m")
        input("\n\x1b[1;97mPress Enter to continue...\x1b[0m")
        return
    
    # Show available pages
    print("\n\x1b[1;92mAvailable Pages:\x1b[0m")
    for i, page in enumerate(pages, 1):
        print(f"\x1b[1;92m[{i}] {page['name']}\x1b[0m")
    
    # Red confirmation prompt
    cont = input("\n\x1b[1;91mDo you want to continue reacting? (yes/no): \x1b[0m").lower()
    if cont != 'yes':
        return
    
    # Red limit input
    try:
        limit = int(input('\x1b[1;91mEnter the limit for reactions: \x1b[0m'))
    except:
        limit = 1
    
    # Start reacting
    for i in range(limit):
        page = pages[i % len(pages)]
        try:
            url = f'https://graph.facebook.com/{post_id}/reactions'
            params = {
                'type': reaction_type,
                'access_token': page['accessToken']
            }
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                print(f"\x1b[1;92mSUCCESS: {reaction_type} reaction sent via {page['name']}\x1b[0m")
            else:
                print(f"\x1b[1;91mERROR: Failed to react (Status: {response.status_code})\x1b[0m")
            
            if i < limit - 1:
                time.sleep(delay)
                
        except Exception as e:
            print(f"\x1b[1;91mError: {str(e)}\x1b[0m")
    
    print("\n\x1b[1;92mOperation completed!\x1b[0m")
    input("\n\x1b[1;97mPress Enter to continue...\x1b[0m")

if __name__ == "__main__":
    while True:
        try:
            auto_react()
        except KeyboardInterrupt:
            print("\n\x1b[1;91mTool stopped by user\x1b[0m")
            break
        except Exception as e:
            print(f"\x1b[1;91mError: {str(e)}\x1b[0m")
            input("\n\x1b[1;97mPress Enter to continue...\x1b[0m")