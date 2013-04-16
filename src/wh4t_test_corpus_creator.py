#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
@author Hernani Marques <h2m@access.uzh.ch>, 2012
"""

from wx import App, Frame, Menu, MenuBar, MessageDialog, TextCtrl, \
               OK, CANCEL, ID_ABOUT, ID_EXIT, ID_OK, ICON_QUESTION, \
               EVT_CLOSE, EVT_MENU, TE_MULTILINE

class Dialog_Frame(Frame):
    def __init__(self, title):
        Frame.__init__(self, None, title=title, size=(350, 200))
        self.Bind(EVT_CLOSE, self.OnClose)
        self.Show(True)
        
    def OnClose(self, event):
        dlg = MessageDialog(self,
                               "Do yu really want to close this app?",
                               "Confirm exit", OK|CANCEL|ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == ID_OK:
            self.Destroy()

class MainWindow(Frame):
    def __init__(self, parent, title):
        Frame.__init__(self, parent, title=title, size=(200,100))
        self.control = TextCtrl(self, style=TE_MULTILINE)
        self.CreateStatusBar()
        
        filemenu = Menu()
        
        menuItem_about = filemenu.Append(ID_ABOUT, "&About", " Info about this app")
        #filemenu.AppendSeperator()
        menuItem_exit = filemenu.Append(ID_EXIT, "&Exit", " Terminate the program")
        
        menuBar = MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        self.Show(True)
        self.Bind(EVT_MENU, self.OnAbout, menuItem_about)
        self.Bind(EVT_MENU, self.OnExit, menuItem_exit)
        
    def OnAbout(self, event):
        dlg = MessageDialog(self, "A small program", "Abut something", OK)
        dlg.ShowModal()
        #dlg.Destroy()
        
    def OnExit(self, event):
        self.control.SetValue("Exit")
        self.Destroy()

app = App(False)
#frame = Dialog_Frame('Dialog')
frame = MainWindow(None, "Sample editor")
app.MainLoop()