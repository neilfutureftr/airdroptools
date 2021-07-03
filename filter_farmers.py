words_you_dont_want_to_see_in_the_tweets=["giveway","give","airdrop"]
column_of_the_twitter_links=2#The CSG file is a list of [id,twitter_link,SOL address]
list_of_lines = pd.read_csv("FTR airdrop_2.csv").values.tolist()



import time
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import pandas as pd
#We set up the tweepy client
#Get your own ids here : https://developer.twitter.com/
auth = tweepy.OAuthHandler("XX", "XX")
auth.set_access_token("XX","XX")
api = tweepy.API(auth)
#Extract the csv :


def is_airdrop_farmer(twitter_link):
    reason=""

    #We get the id of the user from the twitter link
    twitter_profile=twitter_link.split("/")
    twitter_profile_name=twitter_profile[3]

    #We retreive the last 20 tweets
    resultats = api.user_timeline(twitter_profile_name,count=20,tweet_mode='extended')
    time.sleep(1)

    #If there is less than 20 tweets we consider its not fair and this account is a farmer
    if len(resultats)<20:

        reason="Bro you have less than 20 tweets... "
        return True,reason

    else:

        nb_tweets=0
        nb_airdrop_giveway_give=0
        #We go through the tweets
        for tweet in resultats:
            nb_tweets=nb_tweets+1
            #If there is a word we dont want to see in the current tweet -> adding 1
            for word in words_you_dont_want_to_see_in_the_tweets:
                if word in tweet.full_text.lower():
                    nb_airdrop_giveway_give=nb_airdrop_giveway_give+1
                    continue
            #If the tweet is actually a retweet and the retweet contains a word we dont want -> +1
            if tweet.is_quote_status:
                try:
                    for word in words_you_dont_want_to_see_in_the_tweets:
                        if word in tweet.quoted_status.full_text.lower():
                            nb_airdrop_giveway_give = nb_airdrop_giveway_give + 1
                            continue
                except:
                    deleted_tweet=1
        if nb_airdrop_giveway_give/nb_tweets>0.5:
            reason="You're an airdrop farmer, more than 50% of your last tweets are giveways, airdrop and co"
            return True,reason
        else:
            return False, ""
    return False,""

errored_addresses=[]
for add in list_of_lines:
    errored_addresses.append(0)


ff=0
is_airdrop_farmer_results=[]

while True:

    print(int(ff/len(list_of_lines)*100))
    twitter_account=""
    is_airdrop_farmer_res=True
    reason="Error with your twitter"

    try:
        print(list_of_lines[ff][column_of_the_twitter_links-1])
        is_airdrop_farmer_res,reason=is_airdrop_farmer(list_of_lines[ff][column_of_the_twitter_links-1])
        print([is_airdrop_farmer_res,reason])
        is_airdrop_farmer_results.append([list_of_lines[ff][column_of_the_twitter_links],is_airdrop_farmer_res,reason])

        ff=ff+1
    except:
        errored_addresses[ff]=errored_addresses[ff]+1
        if errored_addresses[ff]>3:
            is_airdrop_farmer_results.append(
                [list_of_lines[ff][column_of_the_twitter_links-1], True, "Error when checking if its an airdrop farmer"])
            ff = ff + 1
            print("Error with " + str(list_of_lines[ff][column_of_the_twitter_links-1])+ " " + str(errored_addresses[ff]))
        else:
            time.sleep(10)
    if ff>len(list_of_lines)-1:
        break




indipd = pd.DataFrame(is_airdrop_farmer_results)
indipd.to_csv("is_airdrop_farmer_results.csv", encoding='utf-8', index=False)

