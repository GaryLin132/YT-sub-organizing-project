from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os
# load_dotenv()
# api_key = os.getenv('API_KEY')
# client_secrets_file = os.getenv('CLIENT_SECRETS_FILE')

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
scopes = ["https://www.googleapis.com/auth/youtube"]
api_service_name = 'youtube'
api_version = 'v3'

def create_api_client():
    # Get credentials and create an API client
    cred = None
    working_dir = os.getcwd()
    token_dir = ''
    token_file = 'access_token.json'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        cred = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), scopes)
        # with open(os.path.join(working_dir, token_dir, token_file), 'rb') as token:
        #   cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            # creds.refresh(Request())
            pass
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret_file.json', scopes)
            cred = flow.run_local_server()

        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(cred.to_json())

    # flow = InstalledAppFlow.from_client_secrets_file(
    #    'client_secret_file.json', scopes)
    # cred = flow.run_local_server()
    print("done")
    return cred

def get_sub_list(credentials):
    if credentials==None:
        credentials = create_api_client()

    youtube = build(
        api_service_name, api_version, credentials=credentials)
    
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50
    )
    response = request.execute()

    sub_list = []
    while 1:
        for i in response['items']:
            #subsciption id is not equal to channel id
            chan_title = i['snippet']['title']
            sub_ID = i['id']
            sub_list.append( [ chan_title, sub_ID ] )

        if 'nextPageToken' not in response.keys():
            break
        else:
            request = youtube.subscriptions().list(
                part="snippet,contentDetails",
                maxResults=50,
                mine=True,
                pageToken=response['nextPageToken']
            )
            response = request.execute()

    return sub_list

def delete_sub(credentials, sub_id):
    if credentials==None:
        credentials = create_api_client()
    
    youtube = build(
        api_service_name, api_version, credentials=credentials)
    request = youtube.subscriptions().delete(
        id=sub_id
    )
    request.execute()

if __name__=='__main__':
    cred = create_api_client()
    # sublist = get_sub_list(cred)
    # print(sublist[0][1])
    # delete_sub(cred, sublist[0][1])
    # print("unsubcribe to "+sublist[0][0])