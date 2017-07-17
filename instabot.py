#IMPORTING LIBRARIES IN ORDER TO USE THEM
import requests
import urllib
import matplotlib.pyplot as plot
from PIL import Image
from termcolor import colored
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


#BASIC URL AND ACCESS TOKEN ----GLOBAL VARIABLES
BASIC_URL='https://api.instagram.com/v1/'
Access_token=''


#FUNCTION TO FETCH SELF DETAILS
def self_info():
    request_url=(BASIC_URL + "users/self/?access_token=%s")%(Access_token)
    print "\nrequest url is:%s"%(request_url)
    self_info=requests.get(request_url).json()
    if self_info['meta']['code']==200:
        if len(self_info['data']):
            print "\n"
            print colored("USERNAME : %s"%(self_info['data']['username']),'green')
            print colored("NUMBER OF FOLLOWERS :%d"%(self_info['data']['counts']['followed_by']),'green')
            print colored("FOLLOWING :%d"%(self_info['data']['counts']['follows']),'green')
            print colored("NUMBER OF POSTS : %d"%(self_info['data']['counts']['media']),'green')
        else:
            print colored("\nSORRY I GOT NO DETAILS ABOUT YOU",'red')
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 IS RECIEVED",'red')



#FUNCTION TO GET OWN RECENT POST
def get_own_recent_post():
    request_url=(BASIC_URL + 'users/self/media/recent/?access_token=%s')%(Access_token)
    print "\n"+request_url
    my_media=requests.get(request_url).json()
    if my_media['meta']['code']==200:
        if len(my_media['data']):
            image_name = my_media['data'][0]['id'] + '.jpg'
            image_url = my_media['data'][0]['images']['standard_resolution']['url']

            #DOWNLOADING RECENT POSTED MEDIA
            urllib.urlretrieve(image_url, image_name)
            print colored("\nYOUR IMAGE IS DOWNLOADED SUCCESSFULLY",'green')
            im = Image.open(my_media['data'][0]['id'] + '.jpg')
            im.show()
            return my_media['data'][0]['id']
        else:
            print colored("\nNO POST FOUND",'red')
            return None
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 RECIEVED",'red')



#FUNCTION TO GET OWN RECENT LIKED POST
def own_liked_recent_post():
    request_url = (BASIC_URL + 'users/self/media/liked?access_token=%s') % (Access_token)
    print "\n" + request_url
    my_media = requests.get(request_url).json()
    if my_media['meta']['code'] == 200:
        if len(my_media['data']):
            image_name = my_media['data'][0]['id'] + '.jpg'
            image_url = my_media['data'][0]['images']['standard_resolution']['url']

            #DOWNLOADING OWN RECENT LIKED MEDIA
            urllib.urlretrieve(image_url, image_name)
            im = Image.open(my_media['data'][0]['id'] + '.jpg')
            im.show()
            print colored("\nYOUR IMAGE IS DOWNLOADED SUCCESSFULLY",'green')
        else:
            print colored("\nNO POST FOUND",'red')
            return None
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 RECIEVED",'red')



#FUNCTION TO LIKE OWN POST
def like_own_post():
    media_id=get_own_recent_post()
    request_url=(BASIC_URL + "media/%s/likes")%(media_id)
    payload={"access_token":Access_token}
    print "\nPOST REQUEST TO LIKE MEDIA :%s"%(request_url)
    like_post=requests.post(request_url,payload).json()
    if like_post['meta']['code']==200:
        print colored("\nYOUR POST IS SUCCESSFULLY LIKED",'green')
    else:
        print colored("\nSORRY.UNABLE TO LIKE YOUR POST......\nTRY AGAIN",'red')



#FUNCTION TO COMMENT ON OWN POST
def comment_on_own_post():
    media_id=get_own_recent_post()

    #ASKING THE COMMENT
    comment=raw_input("ENTER YOUR COMMENT")
    payload={"access_token":Access_token,"text":comment}
    request_url=(BASIC_URL+ "media/%s/comments")%(media_id)
    print "\nPOST REQUEST TO COMMENT ON MEDIA :%s"%(request_url)
    comment_post=requests.post(request_url,payload).json()
    if comment_post['meta']['code']==200:
        print colored("\nCOMMENT TO YOUR POST IS ADDED SUCCESSFULLY",'green')
        start_choice()
    else:
        print colored("\nERROR: UNABLE TO ADD COMMENT....PLEASE TRY AGAIN",'red')
        start_choice()



#FUNCTION TO GET LIST OF ALL  EXISTED COMMENTS ON OWN POST
def existed_self_post_comment():
    media_id=get_own_recent_post()
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print "\n" + request_url
    comment_list=requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        if comment_list['data']:
            position=1

            #PRINTING ALL EXISTED COMMENTS
            for temp in comment_list['data']:
                print colored("%d.%s : %s"%(position,temp['from']['username'],temp['text']),'blue')
                position=position+1
        else:
            print colored("\nNO COMMENT FOUND",'red')

    else:
        print colored("\nSTATUS CODE OTHER THAN 200 IS RECIEVED",'red')
    start_choice()



#FUNCTION TO GET POST BASED ON TEXT IN CAPTION OF POST
def self_caption_based_media():

    #USE THESE TAGS----- DarkMagician , Fan , Raees, Man, Black, Euro
    tag=raw_input("ENTER THE TAG NAME")
    request_url = (BASIC_URL + "tags/%s/media/recent?access_token=%s")%(tag, Access_token)
    print '\n' + request_url
    my_media = requests.get(request_url).json()
    if my_media['meta']['code'] == 200:
        if len(my_media['data']):
            image_name = my_media['data'][0]['id'] + '.jpg'
            image_url = my_media['data'][0]['images']['standard_resolution']['url']

            # DOWNLOADING RECENT POSTED MEDIA BASED ON TEXT IN CAPTION OF POST
            urllib.urlretrieve(image_url, image_name)
            print colored("\nYOUR IMAGE IS DOWNLOADED SUCCESSFULLY",'green')
            im = Image.open(my_media['data'][0]['id'] + '.jpg')
            im.show()
        else:
            print colored("\nNO POST FOUND",'red')
            return None
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 RECIEVED",'red')
        return None



#FUNCTION TO PLOT PIECHART BASED ON SENTIMENTS OF EXISTED COMMENTS ON OWN POST
def self_post_piechart():
    media_id=get_own_recent_post()
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print "\n" + request_url
    comment_list=requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        count_pos=0
        count_neg=0
        if comment_list['data']:
            position=1

            #PRINTING COMMENTS WITH SENTIMENTS
            for temp in comment_list['data']:
                print colored("%d.%s : %s"%(position,temp['from']['username'],temp['text']),'blue')
                blob= TextBlob(temp['text'], analyzer=NaiveBayesAnalyzer())
                print colored(blob.sentiment,'red')
                if blob.sentiment.classification=="pos":
                    count_pos=count_pos+1
                else:
                    count_neg=count_neg+1
                position=position+1
            labels = 'POSITIVE','NEGATIVE'
            sizes = [count_pos,count_neg]
            colors = ['green', 'red']
            explode = (0.1, 0)  # explode 1st slice

            #PLOTING PIE CHART
            plot.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=140)

            plot.axis('equal')
            plot.legend(labels)
            plot.tight_layout()
            plot.show()
        else:
            print colored("\nNO COMMENT FOUND",'red')
    else:
        print ("\nSTATUS CODE OTHER THAN 200 IS RECIEVED",'red')
    start_choice()



#FUNCTION TO GET USER ID .......USERNAME IS BEING PASSED AS ARGUMENT TO THE FUNCTION
def get_user_id(username):
    request_url=(BASIC_URL+"users/search?q=%s&access_token=%s")%(username,Access_token)
    print "\n"+ request_url
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return  None
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 IS RECIEVED",'red')


#FUNCTION TO GET USER'S DETAILS USING USER ID
def user_info(username):
    user_id=get_user_id(username)
    if user_id==None:
        print colored("USER DOESN'T EXIST",'red')
        return None
    request_url=(BASIC_URL + "users/%s/?access_token=%s")%(user_id,Access_token)
    print "\n" + request_url
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print "\n"

            #PRINTING DETAILS
            print colored("USERNAME : %s"%(user_info['data']['username']),'green')
            print colored("NUMBER OF FOLLOWERS :%d"%(user_info['data']['counts']['followed_by']),'green')
            print colored("FOLLOWING :%d"%(user_info['data']['counts']['follows']),'green')
            print colored("NUMBER OF POSTS : %d"%(user_info['data']['counts']['media']),'green')
        else:
            print colored("\nUSER DOESN'T EXIST",'red')
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 IS RECIEVED",'red')



#FUNCTION TO GET USER'S RECENT POST USING USER ID
def user_recent_media(username):
    user_id=get_user_id(username)
    if user_id==None:
        print "USER DOESN'T EXIST"
        return None
    request_url=(BASIC_URL + "users/%s/media/recent/?access_token=%s")%(user_id,Access_token)
    print "\n" + request_url
    user_media=requests.get(request_url).json()
    if user_media['meta']['code']==200:
       if len(user_media['data']):
            image_name= user_media['data'][0]['id']+'.jpg'
            image_url=user_media['data'][0]['images']['standard_resolution']['url']

            #DOWNLOADING RECENT POST
            urllib.urlretrieve(image_url,image_name)
            print colored("\nYOUR IMAGE IS DOWNLOADED SUCCESSFULLY",'green')
            im = Image.open(user_media['data'][0]['id'] + '.jpg')
            im.show()
            return user_media['data'][0]['id']
       else:
           print colored("\nNO RECENT POST FOUND",'red')
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 RECIEVED",'red')




#FUNCTION TO GET USER'S POST WHOSE CAPTION HAS A PARTICULAR TEXT
def user_caption_based_media(username):
        user_id = get_user_id(username)
        if user_id == None:
            print "USER DOESN'T EXIST"
            return None
        request_url = (BASIC_URL + "users/%s/media/recent/?access_token=%s") % (user_id, Access_token)
        print "\n" + request_url
        user_media = requests.get(request_url).json()

        #IF SELECTED ls211998 AS USERNAME THEN TEXT YOU MAY ENTER ARE---ROONEY,RONALDO,MANCHESTER,UNITED
        text=raw_input("ENTER THE TEXT")
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                flag=0
                for temp in user_media['data']:

                    #x IS A LIST HERE
                    x = temp['caption']['text'].split()

                    #SEARCHING FOR  text IN x
                    for i in x:
                        if i.upper() == text.upper():
                            image_name = temp['id'] + '.jpg'
                            image_url = temp['images']['standard_resolution']['url']

                            #DOWNLOADING POST
                            urllib.urlretrieve(image_url, image_name)
                            im = Image.open(temp['id'] + '.jpg')
                            im.show()
                            flag=1
                            break

                if flag==1:
                     print colored("\nYOUR POST HAS BEEN DOWNLOADED", 'green')
                else:
                    print colored("\n %s IS NOT  FOUND IN CAPTION OF ANY IMAGE"%(text), 'red')

            else:
                print colored("\nNO POST FOUND", 'red')
        else:
                print colored("\nSTATUS CODE OTHER THAN 200 RECIEVED", 'red')


#FUNCTION TO LIKE USER'S POST
def like_user_post(username):
    media_id=user_recent_media(username)
    request_url=(BASIC_URL + "media/%s/likes")%(media_id)
    print request_url
    payload={"access_token":Access_token}
    print "\nPOST REQUEST TO LIKE MEDIA :%s"%(request_url)
    like_post=requests.post(request_url,payload).json()
    print like_post
    if like_post['meta']['code']==200:
        print colored("\n%s POST IS LIKED SUCCESSFULLY",'green')%(username)
    else:
        print colored("\n CAN\'T LIKE %s \'s POST TRY AGAIN",'red')%(username)



#FUNCTION TO POST A COMMENT ON USER'S RECENT POST
def comment_on_user_post(username):
    media_id=user_recent_media(username)

    #ASKING FOR COMMENT
    comment=raw_input("ENTER YOUR COMMENT")
    payload={"access_token":Access_token,"text":comment}
    request_url=(BASIC_URL+ "media/%s/comments")%(media_id)
    print "\nPOST REQUEST TO COMMENT ON MEDIA :%s"%(request_url)
    comment_post=requests.post(request_url,payload).json()
    if comment_post['meta']['code']==200:
        print colored("\nCOMMENT TO %s \'s POST ADDED SUCCESSFULLY",'green')%(username)
        start_choice()
    else:
        print colored("\nERROR: CAN\'T COMMENT %s \'s POST TRY AGAIN",'red')%(username)
        start_choice()


#FUNCTION TO PLOT A PIECHART BASED ON SENTIMNETS OF EXISTING COMMENTS ON USER'S POST
def user_post_piechart(username):
    media_id=user_recent_media(username)
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print '\n' + request_url
    comment_list=requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        if comment_list['data']:
            position=1
            count_pos=0
            count_neg=0

            #PRINTING COMMENT LIST WITH SENTIMENTS
            for temp in comment_list['data']:
                print colored("%d.%s : %s"%(position,temp['from']['username'],temp['text']),'blue')
                blob = TextBlob(temp['text'], analyzer=NaiveBayesAnalyzer())
                print colored(blob.sentiment,'red')
                if blob.sentiment.classification == "pos":
                    count_pos = count_pos + 1
                else:
                    count_neg=count_neg+1
                position = position + 1
            labels = 'POSITIVE', 'NEGATIVE'
            sizes = [count_pos, count_neg]
            colors = ['green', 'red']
            explode = (0.1, 0)  # explode 1st slice

            #PLOTING PIE CHART
            plot.pie(sizes, explode=explode, labels=labels, colors=colors,
                     autopct='%1.1f%%', shadow=True, startangle=140)

            plot.axis('equal')
            plot.legend(labels)
            plot.tight_layout()
            plot.show()

        else:
            print colored("SORRY NO COMMENT FOUND",'red')
    else:
        print colored("STATUS CODE OTHER THAN 200 IS RECIEVED",'red')
    start_choice()



#FUNCTION TO GET EXISTED COMMENTS ON USER'S RECENT POST
def existed_user_post_comment(username):
    media_id=user_recent_media(username)
    request_url=(BASIC_URL+"media/%s/comments?access_token=%s")%(media_id,Access_token)
    print '\n' + request_url
    comment_list=requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        if comment_list['data']:
            position=1

            #PRINTING EXISTED COMMENTS
            for temp in comment_list['data']:
                print colored("%d.%s : %s"%(position,temp['from']['username'],temp['text']),'blue')
                position=position+1
        else:
            print colored("\nNO COMMENT FOUND",'red')
            start_choice()
    else:
        print colored("\nSTATUS CODE OTHER THAN 200 IS RECIEVED",'red')
    start_choice()




#FUNCTION FROM WHERE MAIN PROGRAM STARTS
def start_choice():

    #ASKING FOR USERNAME

    #I RECOMMEND YOU TO USE ls211998
    #1.ls211998 ,2.samanskull, 3.sahil_singh_6315071, 4.sharma.swayam, 5.sarabjeets45
    print colored("\n\nBEFORE WE GET STARTED....", 'green')
    username=raw_input("ENTER USERNAME")
    choice=1
    while choice!=4:

        #ASKING TO SELECT PARTICULAR CATEGORY
        print colored("\nSELECT YOUR CATEGORY",'yellow')
        print colored("\n1.VIEW INFORMATION \n2.VIEW POST \n3.LIKE \n4.COMMENT \n5.CHANGE USER \n6.EXIT",'blue')
        choice=int(raw_input("ENTER YOUR CHOICE"))

        if choice==1:
            print colored("\n1.VIEW YOUR OWN DETAILS \n2.VIEW %s's DETAILS"%(username),'blue')
            option=int(raw_input("ENTER YOUR CHOICE"))
            if option==1:
                self_info()
            elif option==2:
              user_info(username)
            else:
                print colored("INVALID INPUT",'red')


        elif choice==2:
            print colored("\n1.VIEW YOUR OWN RECENT POST \n2.VIEW RECENT POST LIKED BY YOU  \n3.VIEW OWN POST WHOSE CAPTION HAS A PARTICULAR TEXT \n4.VIEW  %s's RECENT POST \n5.VIEW %s's POST WHOSE CAPTION HAS A PARTICULAR TEXT"%(username,username),'blue')
            option = int(raw_input("ENTER YOUR CHOICE"))
            if option == 1:
                get_own_recent_post()
            elif option == 2:
                own_liked_recent_post()
            elif option == 3:
                self_caption_based_media()
            elif option==4:
                user_recent_media(username)
            elif option==5:
                user_caption_based_media(username)
            else:
                print colored("INVALID INPUT",'red')


        elif choice == 3:
            print colored("\n1.LIKE YOUR OWN POST \n2.LIKE %s's POST"%(username),'blue')
            option = int(raw_input("ENTER YOUR CHOICE"))
            if option == 1:
                like_own_post()
            elif option == 2:
                like_user_post(username)
            else:
                print colored("INVALID INPUT", 'red')


        elif choice==4:
            print colored("\n1.VIEW ALL COMMENTS ON SELF POST  \n2.VIEW ALL COMMENTS ON %s's POST \n3.COMMENT ON YOUR OWN POST \n4.COMMENT ON %s's POST \n5.PLOT A PIECHART"%(username,username),"blue")
            option = int(raw_input("ENTER YOUR CHOICE"))
            if option == 1:
                existed_self_post_comment()
            elif option == 2:
                existed_user_post_comment(username)
            elif option==3:
                comment_on_own_post()
            elif option==4:
                comment_on_user_post(username)

            #PIECHART
            elif option==5:
                print colored("\n1.CREATE YOUR RECENT POST PIECHART \n2.CREATE %s's RECENT POST PIECHART"%(username),"blue")
                intake=int(raw_input("ENTER YOUR CHOICE"))
                if intake==1:
                    self_post_piechart()
                elif intake==2:
                    user_post_piechart(username)
                else:
                    print colored("INVALID INPUT", 'red')
                    start_choice()
            else:
                print colored("INVALID INPUT", 'red')
                start_choice()


        elif choice==5:
            start_choice()


        elif choice==6:
            exit("GOOD \n BYE HAVE A GOOD DAY")


        else:
            print colored("INVALID INPUT", 'red')



