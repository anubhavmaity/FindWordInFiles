import wx
import os
import main

MAXIMUM_ALLOWED_FILES = 6

class SecondFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Results", size=(500,500))
        self.panel = wx.Panel(self)
        #results list
        self.files_result = []
        #SIZER
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        self.sizer = wx.GridBagSizer(0, 0)
        #Results label
        self.files_location_label = wx.StaticText(self.panel, -1, "Results:", (10,10))
        self.sizer.Add(self.files_location_label, (10,10))

    def get_results_from_search(self,files_with_word, freq):

        self.word_occ_label = wx.StaticText(self.panel, -1, str(freq) +" occurences", (10,25))
        self.sizer.Add(self.word_occ_label, (10,25))
        for i, files in enumerate(files_with_word):
            self.files_result.append(wx.StaticText(self.panel, -1, files, (10, 20 + (i+1)*20)))
            self.sizer.Add(self.files_result[-1], (10,20+(i+1)*20))



class gui(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self,parent,id,'Find Words In Files', size=(700,600))
        self._defaultDirectory = "/home"
        self.panel = wx.ScrolledWindow(self,wx.ID_ANY)
         

        #SIZER
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        self.sizer = wx.GridBagSizer(0,0)

        #List of files and no of it
        self.no_of_files = 1
        self.fileCtrl = []

        #list of folders and no of it
        self.no_of_folders = 1
        self.folderCtrl = []

        #search
        self.search_label = wx.StaticText(self.panel, -1, "Search Words: ", (100,35))
        self.sizer.Add(self.search_label,(100, 35))
        self.search_name = wx.TextCtrl(self.panel, pos=(200,30), size=(260, -1))
        self.sizer.Add(self.search_name, (200, 30))
        
        
        #Files location
        self.files_location_label = wx.StaticText(self.panel, -1, "Where to search?", (100,120))

        #Adding file button
        self.button = wx.Button(self.panel, label="Add Files", pos=(100,150), size=(130,-1))
        self.sizer.Add(self.button, (100,150))
        self.Bind(wx.EVT_BUTTON, self.add_files_button, self.button)

        self.fileCtrl.append(wx.FilePickerCtrl(self.panel, pos=(100, 200), size=(260,-1)))
        self.sizer.Add(self.fileCtrl[0], (100,200))
        
        #Removing file button
        self.button_remove = wx.Button(self.panel, label="Remove Files", pos=(100, 445), size=(150,-1)) 
        self.Bind(wx.EVT_BUTTON, self.remove_files_button, self.button_remove)
        self.sizer.Add(self.button_remove, (100, 445))
        
        #Adding folder button
        self.button_add_folder = wx.Button(self.panel, label="Add Folders", pos=(400,150), size=(150, -1))
        self.sizer.Add(self.button_add_folder, (400, 150))
        self.Bind(wx.EVT_BUTTON, self.add_folders_button, self.button_add_folder)

        self.folderCtrl.append(wx.DirPickerCtrl(self.panel, pos=(400, 200), size=(260,-1)))
        self.sizer.Add(self.folderCtrl[0], (400,200))

        #Removing folder button
        self.button_remove_folder = wx.Button(self.panel, label="Remove Folders", pos=(400, 445), size=(150,-1)) 
        self.Bind(wx.EVT_BUTTON, self.remove_folders_button, self.button_remove_folder)
        self.sizer.Add(self.button_remove_folder, (400, 445))

        #running the program button
        self.button_run = wx.Button(self.panel, label="Search", pos=(500,500), size=(70,-1))
        self.Bind(wx.EVT_BUTTON, self.run_program, self.button_run)
        self.sizer.Add(self.button_run, (500, 500))
        

    def add_files_button(self, event):
        if self.no_of_files <= MAXIMUM_ALLOWED_FILES:
            height = self.no_of_files * 35 + 200
            self.fileCtrl.append(wx.FilePickerCtrl(self.panel, pos=(100, height), size=(260,-1)))
            self.sizer.Add(self.fileCtrl[self.no_of_files], (100,height))
            self.no_of_files = self.no_of_files + 1

    def remove_files_button(self, event):
        self.sizer.Detach(self.fileCtrl[-1])
        self.fileCtrl[-1].Destroy()
        del self.fileCtrl[-1]
        self.no_of_files = self.no_of_files - 1
    
    def add_folders_button(self, event):
        if self.no_of_folders <= MAXIMUM_ALLOWED_FILES:
            height = self.no_of_folders * 35 + 200
            self.folderCtrl.append(wx.DirPickerCtrl(self.panel, pos=(400, height), size=(260,-1)))
            self.sizer.Add(self.folderCtrl[self.no_of_folders], (400,height))
            self.no_of_folders = self.no_of_folders + 1

    def remove_folders_button(self, event):
        self.sizer.Detach(self.folderCtrl[-1])
        self.folderCtrl[-1].Destroy()
        del self.folderCtrl[-1]
        self.no_of_folders = self.no_of_folders - 1

    def run_program(self, event):
        frame = SecondFrame()
        keyword =  self.search_name.GetValue()

        if not keyword:
            box = wx.MessageDialog(None, 'Search Term Not Mentioned', 'Ivalid Request', wx.OK)
            answer = box.ShowModal()
            box.Destroy()

        #getting files list from the file dialog
        files_list = []
        for file_path in self.fileCtrl:
            files_list.append(file_path.GetPath())
        files_list = filter(None, files_list)
        print files_list

        #getting folders list from the folder dialog
        folders_list = []
        for folder_path in self.folderCtrl:
            folders_list.append(folder_path.GetPath())
        folders_list = filter(None, folders_list)
        print folders_list

        #getting the files list from the folders given
        if folders_list:
            files_list = self.getFilesFromFolder(folders_list, files_list)
        
        #sending the data to main.py
        if files_list:
            files_with_word, freq = main.search(keyword, files_list)
            frame.get_results_from_search(files_with_word, freq)
            frame.Show()
        else:
            box = wx.MessageDialog(None, 'Files not mentioned', 'Invalid Request', wx.OK)
            answer = box.ShowModal()
            box.Destroy()


    def getFilesFromFolder(self, folders_list, files_list):
        for folder in folders_list:
            for f in os.listdir(folder):
                if f.endswith(".txt"):
                    files_list.append(os.path.abspath(f))

        return files_list

            


    
if __name__ == '__main__':
    app = wx.App(False)
    frame = gui(parent=None, id=-1)
    frame.Show()
    app.MainLoop()