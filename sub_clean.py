# import tKinter as tk
import os
import json
from dotenv import load_dotenv
import YT_api
import numpy as np


def processing(yt_search):
   
   # traverse all data
   channel_hash = {}

   # get the latest time of the list
   ini_time = [ int(yt_search[0]['time'].split('-')[0]), int(yt_search[0]['time'].split('-')[1]) ]
   month_count = 0
   delete_suggest = set()
   inter_freq = []

   for i in yt_search:   # i is type dict
      # count month
      # may have bug if didn't watch youtube for a month
      curr_time = [ int(i['time'].split('-')[0]), int(i['time'].split('-')[1]) ]

      if (ini_time[0]-curr_time[0])*12 + ini_time[1]-curr_time[1] :
         month_count = month_count + (ini_time[0]-curr_time[0])*12 + ini_time[1]-curr_time[1]
         ini_time = curr_time

      # implement sparse array with scipy.sparse

      if 'details' in i.keys() and i['details'][0]['name'] == "From Google Ads":  #i.get('details')!=None
         continue

      if 'subtitles' not in i.keys():
         continue

      # print(i['time'])
      channel = i['subtitles'][0]['name']
      if channel in channel_hash:
         arr_len = len(channel_hash[ channel ])
         if( arr_len<=month_count ): 
            append_arr = np.ones( month_count-arr_len+1, dtype=int)*channel_hash[channel][ arr_len-1 ]
            channel_hash[channel] = np.concatenate( [channel_hash[channel], append_arr])
            # channel_hash[channel][month_count] = channel_hash[channel][month_count] + channel_hash[channel][month_count-1]
            # use the accumulative count
            
         channel_hash[ channel ][month_count] = channel_hash[ channel ][month_count] + 1
      else:
         value = np.zeros( month_count+1, dtype=int )
         value[ month_count ] = 1

         channel_hash[ channel ] = value

      # suggest channel to delete
      if len(channel_hash[ channel ])>=11 and not channel_hash[ channel ][10]:   # the 'not' means 0==false
         # delete channel that hasn't watched in 1 year
         delete_suggest.add(channel)

      # sort channel with interating frequency
      if month_count==3:  # after month_count==2 is done
         # ascending order a.k.a least interacted to most interacted
         inter_freq = [k for k,v in sorted(channel_hash.items(), key=lambda element: element[1][-1])]
         # itemgetter is more efficient when key=lambda element: element[1], but we need [-1] so can't use

   delete_suggest = list(delete_suggest)

   return channel_hash, delete_suggest, inter_freq


def clean(cred, watch_history):
    # analyze watch history
    with open(watch_history,"r", encoding='utf-8') as file:
        yt_search = json.load(file)   # yt_search is type: list
    chan_dict, del_suggest, interact_freq = processing(yt_search)

    # get subsciption list
    # credentials = YT_api.create_api_client()
    sublist = YT_api.get_sub_list(cred)

    # compare subsciption with watch list
    curr_idx = 0
    for i in del_suggest.copy():
        match = 0
        for j in sublist:
            if i == j[0]:
                match = 1
                del_suggest[curr_idx] = j
                break
        if match!=1:   
            del_suggest.remove(i)
        else:
            curr_idx+=1
    curr_idx = 0
    for i in interact_freq.copy():
        match = 0
        for j in sublist:
            if i == j[0]:
                match = 1
                interact_freq[curr_idx] = j
                break
        if match!=1:   
            interact_freq.remove(i)
        else:
            curr_idx+=1
            
    return del_suggest, interact_freq
    
    

if __name__=='__main__':
    
    load_dotenv()
    watch_history = os.getenv('WATCH_HISTORY')
    cred = YT_api.create_api_client()

    del_suggest, interact_freq = clean(cred, watch_history)
