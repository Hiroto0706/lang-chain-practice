import os

import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.getenv("TWEEPY_BEARER_TOKEN"),
    consumer_key=os.getenv("TWEEPY_API_KEY"),
    consumer_secret=os.getenv("TWEEPY_API_KEY_SECRET"),
    access_token=os.getenv("TWEEPY_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWEEPY_ACCESS_TOKEN_SECRET"),
)


def scrape_user_tweets(username, num_tweets=5, mock: bool = False):
    """
    Scrapes a Twitter user's original tweet
    """
    tweet_list = []

    if mock:
        EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json"
        tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()

        # tweets = [
        #     {
        #         "id": 1887302545758142866,
        #         "text": "凡人が天才に勝つためには、何かを犠牲にする必要がある。\n\nそのためには目標を一つに絞る、徹底したデジタルデトックスにあると思います。この2つを実践することで圧倒的な生産性と他とは違う成果を出せるようになる。\n\n凡人が天才に勝つにはそれくらいの覚悟が必要ということですね。",
        #         "url": "https://twitter.com/channel_monta/status/1887302545758142866",
        #     },
        #     {
        #         "id": 1887106906482966539,
        #         "text": "自分の意見を伝えたい時は、相手に納得感を持ってもらうことが重要。\n\n相手に納得してもらうためには、徹底的に相手目線になる必要がある。\n\n相手目線に立っていないと、独りよがりになってしまう。それでは相手は納得しない。\n\n相手を納得させるにはどうすれば良いか。これを考えることが大事。",
        #         "url": "https://twitter.com/channel_monta/status/1887106906482966539",
        #     },
        #     {
        #         "id": 1886758764696797421,
        #         "text": "脳に負荷をかけることを意識したら3ヶ月かかる資格も1ヶ月で取得できる。\n\n脳に負荷をかけるとは、何も見ずに思い出そうとするということ。\n\n特にテスト形式はめちゃくちゃ脳に負荷がかかるので効果的。\n\nChatGPTに選択形式で問題を作ってもらうとかが今だとおすすめです。",
        #         "url": "https://twitter.com/channel_monta/status/1886758764696797421",
        #     },
        # ]

        for tweet in tweets:
            tweet_dict = {}
            tweet_dict["text"] = tweet["text"]
            tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
            tweet_list.append(tweet_dict)
    else:
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
        )

        for tweet in tweets.data:
            tweet_dict = {}
            tweet_dict["text"] = tweet["text"]
            tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
            tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    print("Scrape Twitter User")

    tweets = scrape_user_tweets(username="channel_monta", mock=True)
    print(tweets)
