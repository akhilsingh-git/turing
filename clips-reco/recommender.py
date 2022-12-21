#Model Prediction
import time
import networkx as nx
from collections import defaultdict
import pickle
import boto3


s3 = boto3.resource('s3')
G = pickle.loads(s3.Bucket("mlmodelrecommender").Object("clip/network_all.sav").get()['Body'].read())
score = pickle.loads(s3.Bucket("mlmodelrecommender").Object("clip/video_score_matrix.sav").get()['Body'].read())



def giveVideoMaxScore(a):
    return (score[a]['Maxscore'])
    
def recommend_video_based_on_video_score_page(to_user,start_from=0):
    video_in_page = 100
    initial =time.time()
    prev_watched_videos = list(set(G.neighbors(to_user)))
    prev_watched_videos.sort(key=giveVideoMaxScore)
    recommended_videos = {}
    for video in prev_watched_videos[:100]:
        for video_to_add in list(score[video].keys()):
            try:
                recommended_videos[video_to_add]=max(recommended_videos[video_to_add],score[video][video_to_add])
            except:
                recommended_videos[video_to_add]=score[video][video_to_add]
    for video in prev_watched_videos:
        recommended_videos[video] = -1
    recommended_videos['Maxscore'] = -1
    sorted_recommended_video = sorted(recommended_videos.items(), key=lambda x:-x[1])
    print("time for execution"+str(time.time()-initial))
    #for all video comment out this line
    # return(sorted_recommended_video)
    #for pagination return code change video in page to control videos in a page
    return(sorted_recommended_video[start_from:start_from + video_in_page])

def recommend_video_based_on_video_score(to_user,start_from=0):
    video_in_page = 100
    initial =time.time()
    prev_watched_videos = list(set(G.neighbors(to_user)))
    prev_watched_videos.sort(key=giveVideoMaxScore)
    recommended_videos = {}
    for video in prev_watched_videos[:100]:
        for video_to_add in list(score[video].keys()):
            try:
                recommended_videos[video_to_add]=max(recommended_videos[video_to_add],score[video][video_to_add])
            except:
                recommended_videos[video_to_add]=score[video][video_to_add]
    for video in prev_watched_videos:
        recommended_videos[video] = -1
    recommended_videos['Maxscore'] = -1
    sorted_recommended_video = sorted(recommended_videos.items(), key=lambda x:-x[1])
    print("time for execution"+str(time.time()-initial))
    #for all video comment out this line
    return(sorted_recommended_video)
  


  
