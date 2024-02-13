# YT-sub-organizing-project

Analyse channels base on your watch history, and unsubscribe the non interested ones via YouTube Data API.

## Table of Content

- To get started
- Functionality in a nutshell

## To get started

1. Obtain your watch history

   - Sign in to Google takeout
   - Select Youtube and Youtube Music
   - Change the history format in option to JSON
   - Make sure "history" in content option is included (may deselect the rest)
   - Put "watch-history.json" into the current dirctory and add the file name in the .env file

2. Set up Youtube application for API
   - Create a new project in [Google Developer Console](https://console.developers.google.com/?hl=zh-tw)
   - Search for Youtube Data API v3 in the library tab and enable it
   - Setup OAuth consent screen
     - Set the scope to **../auth/youtube** to **manage** your account
     - Set yourself as the test user
   - Create credentials > Oauth 2.0 client ID
     - Set application to **Desktop App**
     - Set your user name
     - Down load the client secret file (.json)
     - Put it in your project directory
     - type the file name in the .env file

### Project Setup

- Create virtual environment
- Install dependencies
  ```
  pip install -r requirement.txt
  ```
- Run theMainApp.py

## Functionality in a nutshell

### **Data Cleaning** (sub_clean.py)

Count videos viewed of every channel per month, and come up with two indicators

1. Unsubscibe suggestion
   - Contain every channel whose video hasn't been viewed with in a year
2. Interaction ranking
   - Sort every channel viewed in the past three month by the views of its videos.
   - The list is shown from least interacted to the most.

### **Youtube Data API** (YT_api.py)

- Get the subscription list of your Youtube channel to compare with your watch history.
- Granting the permission to unsubscribe to channels.

### **GUI** (gui.py)

- Visualize the unsubscibing suggestion list and the interaction ranking
- Only when the "unsubscribe the selected" button is clicked will the channels in both the lower two Listboxes be unsubscribed and deleted from list.
