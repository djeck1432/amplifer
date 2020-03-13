import os
from dotenv import load_dotenv
from instabot import Bot
import datetime
import time


def get_amount(key):
    return key[1]


def fetch_posts_id(bot):
    user_id = bot.get_user_id_from_username('cocacolarus')
    posts_id = bot.get_user_medias(user_id, filtration=False)
    return posts_id


def fetch_all_comments_in_post(bot, posts_id, period=90):
    users_comments = set()
    users_posts = {}
    users = set()
    time_delta = datetime.datetime.now() - datetime.timedelta(days=period)
    for post_number, post in enumerate(posts_id):
        post_comments = bot.get_media_comments_all(post)
        for comment in post_comments:
            date_formatted = datetime.datetime.fromtimestamp(comment['created_at'])
            if time_delta < date_formatted:
                users_comments.add(comment['user_id'])
                users.add(comment['user_id'])
        users_posts[post_number] = list(users)
        users.clear()
    return {'users_comments': users_comments, 'users_posts': users_posts}


def get_rating_comments(users_comments):
    rating_comments = {}
    for user in users_comments:
        if rating_comments.get(user) is None:
            rating_comments[user] = 1
        else:
            rating_comments[user] += 1
    return rating_comments


def get_rating_posts(users_posts, comment_users):
    rating_post = dict((user, 0) for user in comment_users)
    for number in users_posts.keys():
        users = users_posts[number]
        for user in comment_users:
            if user in users:
                rating_post[user] += 1
    return rating_post


def main():
    load_dotenv()
    inst_password = os.getenv('INSTAGRAM_PASSWORD')
    inst_login = os.getenv('INSTAGRAM_LOGIN')

    bot = Bot()
    bot.login(username=inst_login, password=inst_password)

    posts_id = fetch_posts_id(bot)
    comments = fetch_all_comments_in_post(bot, posts_id)
    users_posts = comments['users_posts']
    users_comments = comments['users_comments']
    posts_result = get_rating_posts(users_posts,users_comments)
    comments_result = get_rating_comments(users_comments)
    print(f'Comments Top:{comments_result}\n\nPosts Top:{posts_result}')


if __name__ == '__main__':
    main()
