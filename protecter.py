import tweepy
from datetime import datetime, timedelta

# 1. APIキーとトークンの設定
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# 2. 認証をセットアップ
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# 3. botアカウントかどうか判定する関数
def is_bot(account):
    # 作成日が1年未満
    one_year_ago = datetime.now() - timedelta(days=365)
    account_created_at = account.created_at
    if account_created_at > one_year_ago:
        # ツイート数が5未満
        if account.statuses_count < 5:
            return True
    return False

# 4. botと判定されたアカウントをブロックする
def block_bots():
    for follower in tweepy.Cursor(api.followers).items():
        try:
            if is_bot(follower):
                api.create_block(follower.id)
                print(f"Blocked bot: {follower.screen_name}")
        except tweepy.TweepError as e:
            print(f"Error occurred: {e}")
        except StopIteration:
            break

# 実行
block_bots()