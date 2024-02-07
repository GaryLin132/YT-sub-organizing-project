import tkinter as tk
import YT_api

class listApp(tk.Frame):
    def __init__(self, parent, del_suggest, topic):
        super().__init__(parent)   # super don't need to pass "self"
        self.del_suggest = del_suggest
        self.final_del = []

        self.var_del = tk.StringVar(self, list(map(lambda x:x[0], self.del_suggest))) # or use tk.StringVar(value=del_suggest)
        self.var_final = tk.StringVar(self, [])

        self.label = tk.Label(self, text=topic)

        self.del_list = tk.Listbox(self, listvariable=self.var_del,
                                     selectmode="extended")

        self.delBtn = tk.Button(self, text="Add to delete list", 
                                   command=self.delBtn_click) 
        self.resBtn = tk.Button(self, text="Resume delete list", 
                                   command=self.resBtn_click) 
        
        self.final_list = tk.Listbox(self, listvariable=self.var_final, 
                                     selectmode="extended")
        
        self.label.pack()
        self.del_list.pack() 
        self.delBtn.pack(fill=tk.BOTH)
        self.resBtn.pack(fill=tk.BOTH) 
        self.final_list.pack()
 
    def delBtn_click(self):
        sel_idx = self.del_list.curselection() # sel_idx is a tuple
        for i in sel_idx[::-1]: # to avoid the index mistake after popping elements
            self.final_del.append( self.del_suggest[i] )
            self.del_suggest.pop(i)  
        # YT_api.delete_sub(selection)
        self.var_del.set(list(map(lambda x:x[0], self.del_suggest)))
        self.var_final.set(list(map(lambda x:x[0], self.final_del)))

    def resBtn_click(self):
        sel_idx = self.final_list.curselection()
        for i in sel_idx[::-1]: # to avoid the index mistake after popping elements
            self.del_suggest.append( self.final_del[i] )
            self.final_del.pop(i)  
        # YT_api.delete_sub(selection)
        self.var_del.set(list(map(lambda x:x[0], self.del_suggest)))
        self.var_final.set(list(map(lambda x:x[0], self.final_del)))

class App(tk.Frame):
    def __init__(self, parent, cred, del_suggest, interact_freq):
        super().__init__(parent)
        self.cred = cred
        self.comp1 = listApp(self, del_suggest, "Subsciption not seen over 1 year")
        self.comp2 = listApp(self, interact_freq, "Subsciption least interacted in 3 month")
        self.submitDel_Btn = tk.Button(self, text="unsubscibe the selected", 
                                   command=self.submitDelete)
        
        self.comp1.grid(row=0, column=0, sticky=tk.E+tk.W) #ew
        self.comp2.grid(row=0, column=1, sticky="ew") #ew
        self.submitDel_Btn.grid(row=2, columnspan=2, sticky=tk.N)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)
        # self.comp1.pack()
        # self.comp2.pack()
        # self.submitDel_Btn.pack()
        
    def submitDelete(self):
        comp1 = self.comp1
        comp2 = self.comp2
        # print(*self.comp1.final_del)
        # print(*self.comp2.final_del)
        for i in comp1.final_del+comp2.final_del:
            YT_api.delete_sub(self.cred, i[1])
            print(i)
        comp1.final_del = []
        comp2.final_del = []
        comp1.var_final.set([])
        comp2.var_final.set([])