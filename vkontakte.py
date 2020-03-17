import os
import requests
from dotenv import load_dotenv
import datetime


def fetch_posts(vk_token):
    url = 'https://api.vk.com/method/wall.get'
    offset = 0
    count_posts = 100
    posts_ids = []
    while offset < count_posts:
        payload = {
            'domain': 'cocacola',
            'access_token': vk_token,
            'v': '5.103',
            'filter': 'owner',
            'offset': offset,
            'count': 100
        }

        response = requests.post(url=url, data=payload)
        response.raise_for_status()
        offset += 100
        count_posts = response.json()['response']['count']
        post_items = response.json()['response']['items']
        [posts_ids.append(post_items[post_number]['id']) for post_number in range(len(post_items))]
    return posts_ids


def get_group_id(vk_token, group_name):
    url = 'https://api.vk.com/method/groups.getById'
    params = {
        'group_id': group_name,
        'access_token': vk_token,
        'v': '5.103'
    }
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    return '-' + str(response.json()['response'][0]['id'])


def fetch_commetns(vk_token, post_id, group_id):
    url = 'https://api.vk.com/method/wall.getComments'
    offset = 0
    count_comments = 100
    comments = []
    while offset < count_comments:
        payload = {
            'access_token': vk_token,
            'v': '5.103',
            'owner_id': group_id,
            'post_id': post_id,
            'offset': offset,
            'count': 100,
        }
        response = requests.post(url=url, data=payload)
        response.raise_for_status()
        offset += 100
        count_comments = response.json()['response']['count']
        comments_count = len(response.json()['response']['items'])
        if comments_count > 0:
            for comment_number in range(comments_count):
                comments.append(response.json()['response']['items'][comment_number])
    return comments


def fetch_comments_period(comments, period=1209600):
    last_comments = {}
    now = datetime.datetime.now().strftime('%s')
    for comment in comments:
        if comment.get('text'):
            date = comment['date']
            timedelta = int(now) - date
            if period < timedelta:
                last_comments[comment['id']] = comment['text']
    return last_comments


def fetch_comments_id(last_comments, group_id):
    filter_comments = []
    for user_id in last_comments.keys():
        if user_id != group_id:
            filter_comments.append(user_id)
    return set(filter_comments)


def fetch_all_likes(vk_token, group_id, post_id):
    url = 'https://api.vk.com/method/likes.getList'
    offset = 0
    likes = []
    count_likes = 100
    while offset < count_likes:
        payload = {
            'access_token': vk_token,
            'v': '5.103',
            'type': 'post',
            'owner_id': group_id,
            'item_id': post_id,
            'offset': offset,
            'count': 100,
        }
        response = requests.post(url=url, data=payload)
        response.raise_for_status()
        offset += 100
        count_likes = response.json()['response']['count']
        likes.extend(response.json()['response']['items'])

    return set(likes)


def run_vk():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    group_id = get_group_id(vk_token, 'cocacola')
    posts = fetch_posts(vk_token)[:3]
    cern = []
    for post_id in posts:
        comments = fetch_commetns(vk_token, post_id, group_id)
        last_comments = fetch_comments_period(comments)
        comments = fetch_comments_id(last_comments, group_id)
        likes = fetch_all_likes(vk_token, group_id, post_id)
        cern.append(comments.difference(likes))
    print(cern)


if __name__ == '__main__':
    run_vk()
