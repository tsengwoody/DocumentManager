# -*- coding: utf-8 -*-
import io
import json
import os
import logging

import wx
from wx.lib import scrolledpanel
from pubsub import pub

class FrameView(wx.Frame):
    def __init__(self, parent, title, size=wx.Size(800, 400)):
        wx.Frame.__init__(self, None, title = title)
        self.Centre()
        self.SetMinSize(size)
        self.SetSize(size) 
        pub.subscribe(self.setData, "data_changed")

    def show(self, isShow=True):
        self.Show(isShow)

    def setData(self, data):
        print("data msg in frame view:", data) 

    def setMenuBar(self, fileMenu):
        self.fileMenu = fileMenu
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.fileMenu, 'Add')
        self.SetMenuBar(self.menubar)
