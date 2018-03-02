import requests #importing requests lib
import urllib
from pprint import pprint #importing pretty print

response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']#Access token different for every user
BASE_URL='https://api.instagram.com/v1/'#common url address

def self_info(): #function for user or owner info
    r = requests.get('%susers/self/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print 'Username: %s' % (r['data']['username'])
        print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])
    else:
        print 'Status code other than 200 received!'



def self_post(): #function for user or owner info
    r = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        #pprint(r)
        print r['data'][0]['images']['standard_resolution']['url']
        url = r ['data'][0]['images']['standard_resolution']['url']
        name = r['data'][0]['id'] + '.jpg'
        urllib.urlretrieve(url,name)
        print "Downloaded"

    else:
        print 'Status code other than 200 received!'


def get_user_id(uname):
    r = requests.get('%susers/search?q=%s&access_token=%s'%(BASE_URL,uname, APP_ACCESS_TOKEN)).json()
    return r['data'][0]['id']

def user_info(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/%s/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print 'Username: %s' % (r['data']['username'])
        print 'No. of followers: %s' % (r['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])
    else:
        print 'Status code other than 200 received!'


def user_post(username):
    user_id =get_user_id(username)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        #pprint(r)
        print r['data'][0]['images']['standard_resolution']['url']
        url = r['data'][0]['images']['standard_resolution']['url']
        name = r['data'][0]['id'] + '.jpg'
        urllib.urlretrieve(url, name)
        print "Downloaded"
        print r['data'][0]['videos']['standard_resolution']['url']
        url = r['data'][0]['videos']['standard_resolution']['url']
        name = r['data'][0]['id'] + '.mp4'
        urllib.urlretrieve(url, name)
        print "Downloaded video"

    else:
        print 'Status code other than 200 received!'

def get_media_id(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        return r['data'][3]['id']
    else:
        print 'Status code other than 200 received!'


def like_post(uname):
    media_id = get_media_id(uname)
    payload = {"access_token": APP_ACCESS_TOKEN}
    url = BASE_URL + 'media/%s/likes' % (media_id)
    r =requests.get(url, payload).json()
    if r['meta']['code'] == 200:
        print "like successful"
    else:
        print 'like unsuccessful'


def comment_post(uname):
    media_id = get_media_id(uname)
    comment = raw_input("What is your comment")
    payload = {"access_token": APP_ACCESS_TOKEN, 'text':comment}
    url = BASE_URL + 'media/%s/comments' % (media_id)
    r = requests.get(url, payload).json()
    if r['meta']['code'] == 200:
        print "comment successful"
    else:
        print 'comment unsuccessful'


def start_bot():
    show_menu = True
    while show_menu:
        query = input("What do you want to do? \n 1. Get Owner Info. \n 2. Get Owner Post \n 3. Get Other User Info \n 4. Get Other User Post \n 5. Like A Post \n 6. Comment On Post \n 0. Exit ")
        if query == 1:
            self_info()
        elif query == 2:
            self_post()
        elif query == 3:
            user_name = raw_input('What is the user name?')
            user_info(user_name)
        elif query ==4:
            user_name = raw_input('What is the user name?')
            user_post(user_name)
        elif query ==5:
            user_name = raw_input('What is the user name?')
            like_post(user_name)
        elif query ==6:
            user_name = raw_input('What is the user name?')
            comment_post(user_name)
        elif query == 0:
            show_menu = False
        else:
            print 'Error'

start_bot()
