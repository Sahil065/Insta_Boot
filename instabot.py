import requests
import urllib
import matplotlib.pyplot as plot
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

BASIC_URL='https://api.instagram.com/v1/'
Access_token='3524313198.b5d6b75.a998fb5b08cf46799ad976179b47bc91'


def self_info():
    request_url=(BASIC_URL + "users/self/?access_token=%s")%(Access_token)
    print "request url is:%s"%(request_url)
    user_info=requests.get(request_url).json()
    print user_info
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print "\n"
            print "USERNAME : %s"%(user_info['data']['username'])
            print "NUMBER OF FOLLOWERS :%d"%(user_info['data']['counts']['followed_by'])
            print "FOLLOWING :%d"%(user_info['data']['counts']['follows'])
            print "NUMBER OF POSTS : %d"%(user_info['data']['counts']['media'])
        else:
            print "USER DOESN'T EXIST"
    else:
        print "STATUS CODE OTHER THAN 200 IS RECIEVED"


def get_user_id(username):
    request_url=(BASIC_URL+"users/search?q=%s&access_token=%s")%(username,Access_token)
    print request_url
    user_info=requests.get(request_url).json()
    print user_info
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return  None
    else:
        print "STATUS CODE OTHER THAN 200 IS RECIEVED"
        exit()

def user_info(username):
    user_id=get_user_id(username)
    if user_id==None:
        print "USER DOESN'T EXIST"
        exit()
    request_url=(BASIC_URL + "users/%s/?access_token=%s")%(user_id,Access_token)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print "\n"
            print "USERNAME : %s"%(user_info['data']['username'])
            print "NUMBER OF FOLLOWERS :%d"%(user_info['data']['counts']['followed_by'])
            print "FOLLOWING :%d"%(user_info['data']['counts']['follows'])
            print "NUMBER OF POSTS : %d"%(user_info['data']['counts']['media'])
        else:
            print "USER DOESN'T EXIST"
    else:
        print "STATUS CODE OTHER THAN 200 IS RECIEVED"


def get_own_recent_post():
    request_url=(BASIC_URL + 'users/self/media/recent/?access_token=%s')%(Access_token)
    print request_url
    my_media=requests.get(request_url).json()
    print my_media
    if my_media['meta']['code']==200:
        if len(my_media['data']):
            return my_media['data'][0]['id']
        else:
            print "NO POST FOUND"
            return None
    else:
        print "STATUS CODE OTHER THAN 200 RECIEVED"


def like_own_post():
    media_id=get_own_recent_post()
    request_url=(BASIC_URL + "media/%s/likes")%(media_id)
    payload={"access_token":Access_token}
    print "POST REQUEST TO LIKE MEDIA :%s"%(request_url)
    like_post=requests.post(request_url,payload).json()
    print like_post
    if like_post['meta']['code']==200:
        print "SUCCESSFUL"
    else:
        print "TRY AGAIN"



def user_recent_media(username):
    user_id=get_user_id(username)
    if user_id==None:
        print "USER DOESN'T EXIST"
        exit()
    request_url=(BASIC_URL + "users/%s/media/recent/?access_token=%s")%(user_id,Access_token)
    print request_url
    user_media=requests.get(request_url).json()
    print user_media
    if user_media['meta']['code']==200:
       if len(user_media['data']):
            image_name= user_media['data'][0]['id']+'.jpg'
            image_url=user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print "YOUR IMAGE IS DOWNLOADED SUCCESSFULLY"
            return user_media['data'][0]['id']
       else:
           print "NO RECENT POST FOUND"
    else:
        print "STATUS CODE OTHER THAN 200 RECIEVED"


def like_user_post(username):
    media_id=user_recent_media(username)
    request_url=(BASIC_URL + "media/%s/likes")%(media_id)
    payload={"access_token":Access_token}
    print "POST REQUEST TO LIKE MEDIA :%s"%(request_url)
    like_post=requests.post(request_url,payload).json()
    print like_post
    if like_post['meta']['code']==200:
        print "SUCCESSFUL"
    else:
        print "TRY AGAIN"

def comment_on_user_post(username):
    media_id=user_recent_media(username)
    comment=raw_input("ENTER YOUR COMMENT")
    payload={"access_token":Access_token,"text":comment}
    request_url=(BASIC_URL+ "media/%s/comments")%(media_id)
    print "POST REQUEST TO COMMENT ON MEDIA :%s"%(request_url)
    comment_post=requests.post(request_url,payload).json()
    print comment_post
    if comment_post['meta']['code']==200:
        print"COMMENT ADDED SUCCESSFULLY"
    else:
        print "ERROR: TRY AGAIN"


def comment_on_own_post():
    media_id=get_own_recent_post()
    comment=raw_input("ENTER YOUR COMMENT")
    payload={"access_token":Access_token,"text":comment}
    request_url=(BASIC_URL+ "media/%s/comments")%(media_id)
    print "POST REQUEST TO COMMENT ON MEDIA :%s"%(request_url)
    comment_post=requests.post(request_url,payload).json()
    print comment_post
    if comment_post['meta']['code']==200:
        print"COMMENT ADDED SUCCESSFULLY"
    else:
        print "ERROR: TRY AGAIN"


def existed_self_post_comment():
    media_id=get_own_recent_post()
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print request_url
    comment_list=requests.get(request_url).json()
    print comment_list
    if comment_list['meta']['code']==200:
        if comment_list['data']:
            position=1
            for temp in comment_list['data']:
                print "%d.%s : %s"%(position,temp['from']['username'],temp['text'])
                position=position+1
        else:
            print "NO COMMENT FOUND"
    else:
        print "STATUS CODE OTHER THAN 200 IS RECIEVED"


def self_post_piechart():
    media_id=get_own_recent_post()
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print request_url
    comment_list=requests.get(request_url).json()
    print comment_list
    if comment_list['meta']['code']==200:
        count_pos=0
        count_neg=0
        count_neut=0
        if comment_list['data']:
            position=1
            for temp in comment_list['data']:
                print "%d.%s : %s"%(position,temp['from']['username'],temp['text'])
                blob= TextBlob(temp['text'], analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.classification=="pos":
                    count_pos=count_pos+1
                elif blob.sentiment.classification=="neg":
                    count_neg=count_neg+1
                else:
                    count_neut=count_neut+1
                position=position+1
            labels = 'POSITIVE','NEGATIVE','NEUTRAL'
            sizes = [count_pos,count_neg,count_neut]
            colors = ['green', 'red', 'yellow']
            explode = (0, 0, 0)  # explode 1st slice

            # Plot
            plot.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=140)

            plot.axis('equal')
            plot.show()
        else:
            print "NO COMMENT FOUND"
    else:
        print "STATUS CODE OTHER THAN 200 IS RECIEVED"



def user_post_piechart(username):
    media_id=user_recent_media(username)
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print request_url
    comment_list=requests.get(request_url).json()
    print comment_list
    if comment_list['meta']['code']==200:
        if comment_list['data']:
            position=1
            count_pos=0
            count_neg=0
            count_neut=0
            for temp in comment_list['data']:
                print "%d.%s : %s"%(position,temp['from']['username'],temp['text'])
                blob = TextBlob(temp['text'], analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.classification == "pos":
                    count_pos = count_pos + 1
                elif blob.sentiment.classification=="neg":
                    count_neg = count_neg + 1
                else:
                    count_neut=count_neut+1
                position = position + 1
            labels = 'POSITIVE', 'NEGATIVE', 'NEUTRAL'
            sizes = [count_pos, count_neg, count_neut]
            colors = ['green', 'red', 'yellow']
            explode = (0, 0, 0)  # explode 1st slice

            # Plot
            plot.pie(sizes, explode=explode, labels=labels, colors=colors,
                     autopct='%1.1f%%', shadow=True, startangle=140)

            plot.axis('equal')
            plot.show()

        else:
            print "NO COMMENT FOUND"
    else:
        print "STATUS CODE OTHER THAN 200 IS RECIEVED"




def existed_user_post_comment(username):
    media_id=user_recent_media(username)
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print request_url
    comment_list=requests.get(request_url).json()
    print comment_list
    if comment_list['meta']['code']==200:
        if comment_list['data']:
            position=1
            for temp in comment_list['data']:
                print "%d.%s : %s"%(position,temp['from']['username'],temp['text'])
                position=position+1
        else:
            print "NO COMMENT FOUND"
    else:
        print "STATUS CODE OTHER THAN 200 IS RECIEVED"



def choice():
    choice=1
    while choice!=4:
        print "\nWHAT YOU WANT TO DO"
        print "\n1.VIEW INFORMATION \n2.VIEW POST \n3.LIKE \n4.COMMENT \n5.EXIT"
        choice=int(raw_input("ENTER YOUR CHOICE"))
        if choice==1:
            print"\n1.VIEW YOUR OWN DETAILS \n2.VIEW OTHER USER DETAILS"
            option=int(raw_input("ENTER YOUR CHOICE"))
            if option==1:
                self_info()
            elif option==2:
                username=raw_input("ENTER NAME OF OTHER USER")
                user_info(username)
            else:
                print "INVALID INPUT"

        elif choice==2:
            print"\n1.VIEW YOUR OWN POST \n2.VIEW OTHER USER'S POST"
            option = int(raw_input("ENTER YOUR CHOICE"))
            if option == 1:
                get_own_recent_post()
            elif option == 2:
                username = raw_input("ENTER NAME OF OTHER USER")
                user_recent_media(username)
            else:
                print "INVALID INPUT"

        if choice == 3:
            print"\n1.LIKE YOUR OWN POST \n2.LIKE OTHER USER'S POST"
            option = int(raw_input("ENTER YOUR CHOICE"))
            if option == 1:
                like_own_post()
            elif option == 2:
                username = raw_input("ENTER NAME OF OTHER USER")
                like_user_post(username)
            else:
                print "INVALID INPUT"

        if choice==4:

            print"\n1.VIEW ALL COMMENTS ON SELF POST  \n2.VIEW ALL COMMENTS ON USER'S POST \n3.COMMENT ON YOUR OWN POST \n4.COMMENT ON  OTHER USER'S POST \n5.PLOT A PIECHART"
            option = int(raw_input("ENTER YOUR CHOICE"))
            if option == 1:
                existed_self_post_comment()
            elif option == 2:
                username = raw_input("ENTER NAME OF OTHER USER")
                existed_user_post_comment(username)
            elif option==3:
                comment_on_own_post()
            elif option==4:
                username = raw_input("ENTER NAME OF OTHER USER")
                comment_on_user_post(username)
            elif option==5:
                user_post_piechart('ls211998')

            else:
                print "INVALID INPUT"
