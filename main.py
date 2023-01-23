import io
import sys
import argparse
from auth import consumer_key, consumer_secret, access_key, access_secret
 
import tweepy

__version__ = '2.0'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
twitter = tweepy.API(auth)

def crawl_tweets(tweet_ids):
    tweets = {}
    for n_ids in [tweet_ids[i:i+100] for i in range(0, len(tweet_ids), 100)]:
        n_tweets = twitter.lookup_statuses(n_ids)
        for tw in n_tweets:
            if tw:
                tweets[tw.id_str] = ' '.join(tw.text.split())

    return tweets

if __name__ == '__main__':
    prog = 'tweet-crawler'
    description = 'Download tweets'
    parser = argparse.ArgumentParser(prog=prog,
                                     description=description)
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%s %s' % (prog, __version__))
    parser.add_argument('-i',
                        '--idfile',
                        metavar='',
                        dest='idfile',
                        type=str,
                        help='<tweet-ids file>')
    parser.add_argument('-o',
                        '--output',
                        metavar='',
                        dest='outfile',
                        type=str,
                        help='<output-file>')
    args = parser.parse_args(sys.argv[1:])
    ofp = io.open(args.outfile, mode='w', encoding='utf-8')
    # crawl tweets
    with open(args.idfile) as fp:
        tweet_ids = fp.read().split()
    tweets = crawl_tweets(tweet_ids)
   
    for tid in tweet_ids:
        if tid not in tweets:
            sys.stderr.write('Tweet not found :: t_id %s :: \n' %tid)
        else:
            tweet = tweets[tid]
            print(tweet)
            ofp.write('%s\n\n' % tweet)
    # close files
    ofp.close()