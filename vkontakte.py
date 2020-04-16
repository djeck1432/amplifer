import os
import requests
from dotenv import load_dotenv
import datetime


def get_payload(vk_token,offset):
    payload = {
        'access_token': vk_token,
        'v': '5.103',
        'count': 100,
        'offset': offset,
    }
    return payload


def fetch_posts(vk_token,vk_group_name):
    url = 'https://api.vk.com/method/wall.get'
    offset = 0
    count_posts = 100
    posts_ids = []
    while offset < count_posts:
        extra_payload = {'domain': vk_group_name,'filter': 'owner'}
        payload = get_payload(vk_token,offset)
        payload.update(extra_payload)
        response = requests.post(url=url, data=payload)
        response_json = response.json()['response']
        if 'error' in response_json:
            return response_json['error']
        else:
            offset += 100
            count_posts = response_json['count']
            post_items = response_json['items']
            post_ids = [post_items[post_number]['id'] for post_number, item in enumerate(post_items)]
            posts_ids.extend(post_ids)
    return posts_ids


def get_group_id(vk_token, vk_group_name):
    url = 'https://api.vk.com/method/groups.getById'
    params = {
        'group_id': vk_group_name,
        'access_token': vk_token,
        'v': '5.103'
    }
    response = requests.get(url=url, params=params)
    response_json = response.json()['response']
    if 'error' in response_json:
        return response_json['error']
    else:
        return f"-{response_json[0]['id']}"


def fetch_commetns(vk_token, post_id, group_id):
    url = 'https://api.vk.com/method/wall.getComments'
    offset = 0
    count_comments = 100
    comments = []
    while offset < count_comments:
        extra_payload = {'owner_id': group_id,'post_id': post_id}
        payload = get_payload(vk_token, offset)
        payload.update(extra_payload)
        response = requests.post(url=url, data=payload)
        response_json = response.json()['response']
        if 'error' in response_json:
            return response_json['error']
        else:

            offset += 100
            count_comments = response_json['count']
            comments_count = len(response_json['items'])
            if comments_count > 0:
                for comment_number in range(comments_count):
                    comments.append(response_json['items'][comment_number])
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
        extra_payload = {'type': 'post', 'owner_id': group_id,'item_id': post_id}
        payload = get_payload(vk_token, offset)
        payload.update(extra_payload)
        response = requests.post(url=url, data=payload)
        response_json = response.json()['response']
        if 'error' in response_json:
            return response_json['error']
        else:
            offset += 100
            count_likes = response_json['count']
            likes.extend(response_json['items'])

    return set(likes)


def run_vk():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    vk_group_name = os.getenv('VK_GROUP_NAME')
    group_id = get_group_id(vk_token, vk_group_name)

    posts = fetch_posts(vk_token,vk_group_name)[:5]
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
