#Import tweepy stuff
import json
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import TweepError

#Token variables
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
#Create a var for my user id
account_user_id = "700875055379550208"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

class StdOutListener(StreamListener):

	def following(self, tweetId, screenName, tweetText):
		reply = '@' + screenName + ' '
		if len(reply) > 140:
			reply = reply[0:137] + '...'

		time.sleep(60*5)
		api.update_status(reply, tweetId)
		print(reply)
		


	def on_data(self, data):
		try:
			tweet = json.loads(data.strip())

			retweeted = tweet.get('retweeted', False)
			print(retweeted)
			from_self = tweet.get('user', {}).get('id_str', '') == account_user_id

			#If the retweet value of the tweet we have is none, then it is not a tweet and we ignore it
			#If the tweet is not a retweet and it is not from ourself,
			#then we get the tweet ID, screen name, and the text of the tweet
			if retweeted is not None and not retweeted and not from_self:
				tweetId = tweet.get('id_str')
				screenName = tweet.get('user').get('screen_name')
				tweetText = tweet.get('text')

				#Check if the user who tweeted follows one of the following Penn State affliated twitter accounts
				exists_Onward_State = api.show_friendship(source_screen_name=screenName, target_id='17489445')
				onwardSource, onwardTarget = exists_Onward_State

				exists_Penn_State = api.show_friendship(source_screen_name=screenName, target_id='119376050')
				pennStateSource, pennStateTarget = exists_Penn_State

				exists_Penn_State_Football = api.show_friendship(source_screen_name=screenName, target_id='53103297')
				pennStateFootballSource, pennStateFootballTarget = exists_Penn_State_Football

				exists_Coach_Franklin = api.show_friendship(source_screen_name=screenName, target_id='249974958')
				franklinSource, franklinTarget = exists_Coach_Franklin

				exists_Onward_Sports = api.show_friendship(source_screen_name=screenName, target_id='2329720436')
				onwardSportsSource, onwardSportsTarget = exists_Onward_Sports

				if 	onwardSource.following or pennStateSource.following or pennStateFootballSource.following or franklinSource.following or onwardSource.following:
					self.following(tweetId, screenName, tweetText)
				return True	
		except TweepError:
			print("Rate Limit Error\n")
			time.sleep(60*10)
			

	def on_error(self, status):
		print status
			
if __name__ == '__main__':
	listener = StdOutListener()
	stream = Stream(auth, listener)
	stream.filter(track=['PSU', 'Penn State'])

