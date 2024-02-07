from sub_clean import clean
from gui import App
import os
from dotenv import load_dotenv
import YT_api
import tkinter as tk





if __name__=='__main__':
    load_dotenv()
    
    watch_history = os.getenv('WATCH_HISTORY')
    api_key = os.getenv('API_KEY')
    client_secrets_file = os.getenv('CLIENT_SECRETS_FILE')

    cred = YT_api.create_api_client()

    del_suggest, interact_freq = clean(cred, watch_history)

    root = tk.Tk()
    root.geometry('420x450')
    App(root, cred, del_suggest, interact_freq).place(x=0, y=0, relwidth=1, relheight=1)
    root.mainloop()