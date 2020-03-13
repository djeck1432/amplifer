import os
from dotenv import load_dotenv
import datetime
import requests


def fetch_posts_ids(fb_token, group_id):
    posts_ids = []
    url = f'https://graph.facebook.com/v6.0/{group_id}/feed'
    params = {'access_token': fb_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    for post in response.json()['data']:
        posts_ids.append(post['id'])
    return posts_ids


def fetch_posts_comments(fb_token, post_id):
    post_comments = []
    params = {'access_token': fb_token}
    response = requests.get(f'https://graph.facebook.com/v5.0/{post_id}/comments', params=params)
    response.raise_for_status()
    comments = response.json()['data']
    for comment in comments:
        post_comments.append({
            'user_id': comment['from']['id'],
            'created_time': comment['created_time'],
            'message': comment['message'],
        })
    return post_comments


def fetch_comments_period(comments, period=30):
    last_comments = []
    for comment in comments:
        date,time = comment['created_time'].split('T')
        comment_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        now = datetime.datetime.now()
        timedelta = now - comment_date
        if datetime.timedelta(days=period) > timedelta:
            last_comments.append(comment['user_id'])
    return last_comments


def fetch_post_reactions(fb_token, post_id):
    post_reactions = []
    params = {'access_token': fb_token}
    response = requests.get(f'https://graph.facebook.com/v5.0/{post_id}/reactions', params=params)
    response.raise_for_status()
    reactions = response.json()['data']
    for reaction in reactions:
        post_reactions.append({
            'user_id': reaction['id'],
            'type': reaction['type'],
        })
    return post_reactions


def fetch_post_details(fb_token, posts_ids):
    users_id = []
    users_like = []
    for post_id in posts_ids:
        post_comments = fetch_posts_comments(fb_token, post_id)
        comments_period = fetch_comments_period(post_comments)
        post_reactions = fetch_post_reactions(fb_token, post_id)
        if comments_period is not None:
            users_id.append(comments_period)
        if post_reactions is not None:
            users_like.append(post_reactions)
    return users_id,users_like


def main():
    load_dotenv()
    fb_token = os.getenv('FACEBOOK_TOKEN')
    fb_group_id = os.getenv('FACEBOOK_GROUP_ID')
    posts_ids = fetch_posts_ids(fb_token, fb_group_id)
    users_id, users_like = fetch_post_details(fb_token, posts_ids)
    print(f'{users_id}\n{users_like}')


if __name__ == '__main__':
    main()
