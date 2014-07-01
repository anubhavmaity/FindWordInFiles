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
        self.sizer = wx.GridBagSizer(5, 5)
        #Results label
        self.files_location_label = wx.StaticText(self.panel, -1, "Results:", (10,10))
        self.sizer.Add(self.files_location_label, (5,5))

    def get_results_from_search(self,files_with_word, freq):

        self.word_occ_label = wx.StaticText(self.panel, -1, str(freq) +" occurences", (10,25))
        self.sizer.Add(self.word_occ_label, (5,5))
        for i, files in enumerate(files_with_word):
            self.files_result.append(wx.StaticText(self.panel, -1, files, (10, 20 + (i+1)*20)))
            self.sizer.Add(self.files_result[-1], (5,5))



class gui(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self,parent,id,'Find Words In Files', size=(600,500))
        self._defaultDirectory = "/home"
        self.panel = wx.ScrolledWindow(self,wx.ID_ANY)
        self.panel.SetScrollbars(1, 1, 2, 3)

        

        #SIZER
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        self.sizer = wx.GridBagSizer(10, 10)

        
        self.no_of_files = 1
        self.fileCtrl = []
        #search
        self.search_label = wx.StaticText(self.panel, -1, "Search Words: ", (100,35))
        self.sizer.Add(self.search_label, (6,6))
        self.search_name = wx.TextCtrl(self.panel, pos=(200,30), size=(260, -1))
        self.sizer.Add(self.search_name, (1, 1))
        
        
        #Files location
        self.files_location_label = wx.StaticText(self.panel, -1, "Where to search?", (100,120))
        #Adding file button
        self.button = wx.Button(self.panel, label="Add Files/Folders", pos=(100,150), size=(130,35))
        self.sizer.Add(self.button, (5,5))
        self.fileCtrl.append(wx.FilePickerCtrl(self.panel, pos=(100, 200), size=(260,35)))
        self.Bind(wx.EVT_BUTTON, self.add_files_button, self.button)
        self.sizer.Add(self.fileCtrl[0], (5,5))
        #Removing file button
        self.button_remove = wx.wx.Button(self.panel, label="Remove Files/Folders", pos=(100, 445), size=(150,35)) 
        self.Bind(wx.EVT_BUTTON, self.remove_files_button, self.button_remove)

        
        
        #running the program button
        self.button_run = wx.Button(self.panel, label="Search", pos=(500,440), size=(70,35))
        self.Bind(wx.EVT_BUTTON, self.run_program, self.button_run)

        

    def add_files_button(self, event):

        if self.no_of_files <= MAXIMUM_ALLOWED_FILES:
            height = self.no_of_files * 35 + 200
            self.fileCtrl.append(wx.FilePickerCtrl(self.panel, pos=(100, height), size=(260,35)))
            self.sizer.Add(self.fileCtrl[self.no_of_files], (5,5))
            self.no_of_files = self.no_of_files + 1

    def remove_files_button(self, event):
        self.sizer.Detach(self.fileCtrl[-1])
        self.fileCtrl[-1].Destroy()
        del self.fileCtrl[-1]
        self.no_of_files = self.no_of_files - 1
    
    def run_program(self, event):
        frame = SecondFrame()
        keyword =  self.search_name.GetValue()

        files_list = []
        for file_path in self.fileCtrl:
            files_list.append(file_path.GetPath())

        
        files_list = filter(None, files_list)
        print files_list
        
        if files_list:
            files_with_word, freq = main.search(keyword, files_list)

            frame.get_results_from_search(files_with_word, freq)
            frame.Show()
        else:

            box = wx.MessageDialog(None, 'Files not mentioned', 'Ivalid Request', wx.OK)
            answer = box.ShowModal()
            box.Destroy()
                
        


    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = gui(parent=None, id=-1)
    frame.Show()
    app.MainLoop()