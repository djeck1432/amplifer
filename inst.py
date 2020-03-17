import os
from dotenv import load_dotenv
from instabot import Bot
import datetime
import collections


def fetch_posts_ids(bot):
    user_id = bot.get_user_id_from_username('cocacolarus')
    posts_ids = bot.get_user_medias(user_id, filtration=False)
    return posts_ids


def fetch_all_comments_in_posts(bot, posts_ids, period=90):
    users_comments_ids = set()
    users_posts_ids = {}
    time_delta = datetime.datetime.now() - datetime.timedelta(days=period)
    for post_number, post in enumerate(posts_ids):
        users = set()
        post_comments = bot.get_media_comments_all(post)
        for comment in post_comments:
            formatted_date = datetime.datetime.fromtimestamp(comment['created_at'])
            if time_delta < formatted_date:
                users_comments_ids.add(comment['user_id'])
                users.add(comment['user_id'])
        users_posts_ids[post_number] = list(users)
    return {'users_comments_ids': users_comments_ids, 'users_posts_ids': users_posts_ids}


def get_posts_rating(users_posts_ids, users_comments_ids):
    posts_rating = dict((user, 0) for user in users_comments_ids)
    for post, users in users_posts_ids.items():
        for user in users_comments_ids:
            if user in users:
                posts_rating[user] += 1
    return posts_rating


def inst_run():
    load_dotenv()
    inst_password = os.getenv('INSTAGRAM_PASSWORD')
    inst_login = os.getenv('INSTAGRAM_LOGIN')

    bot = Bot()
    bot.login(username=inst_login, password=inst_password)

    posts_ids = fetch_posts_ids(bot)
    comments = fetch_all_comments_in_posts(bot, posts_ids)
    users_posts_ids = comments['users_posts_ids']
    users_comments_ids = comments['users_comments_ids']
    posts_result = get_posts_rating(users_posts_ids, users_comments_ids)
    comments_result = collections.Counter(users_comments_ids)
    print(f'Comments Top:{comments_result}\n\nPosts Top:{posts_result}')


if __name__ == '__main__':
    inst_run()
