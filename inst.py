import os
from dotenv import load_dotenv
from instabot import Bot
import datetime
import collections


def fetch_posts_ids(bot):
    user_id = bot.get_user_id_from_username('cocacolarus')
    posts_ids = bot.get_user_medias(user_id, filtration=False)
    return posts_ids


def fetch_all_users_ids_in_posts(bot, posts_ids, period=90):
    users_posts_ids = []
    users = []
    time_delta = datetime.datetime.now() - datetime.timedelta(days=period)
    for post_number, post in enumerate(posts_ids):
        post_comments = bot.get_media_comments_all(post)
        users_ids = set()
        for comment in post_comments:
            formatted_date = datetime.datetime.fromtimestamp(comment['created_at'])
            if time_delta < formatted_date:
                users.append(comment['user_id'])
                users_ids.add(comment['user_id'])
        users_posts_ids += list(users_ids)
    return {
        'users_posts_ids': users_posts_ids,
        'users': users
        }


def run_inst():
    load_dotenv()
    inst_password = os.getenv('INSTAGRAM_PASSWORD')
    inst_login = os.getenv('INSTAGRAM_LOGIN')

    bot = Bot()
    bot.login(username=inst_login, password=inst_password)
    posts_ids = fetch_posts_ids(bot)
    users_ids = fetch_all_users_ids_in_posts(bot, posts_ids)
    users_posts_ids = users_ids['users_posts_ids']
    users = users_ids['users']
    posts_rating = collections.Counter(users_posts_ids)
    comments_rating = collections.Counter(users)
    print(f'Comments Top:{comments_rating}\n\nPosts Top:{posts_rating}')


if __name__ == '__main__':
    run_inst()
