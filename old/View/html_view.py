import wx 
import wx.html2 

class HtmlPanel(wx.Panel): 
    def __init__(self, parent, title, content, _type, data, eventParent): 
        wx.Panel.__init__(self, parent, wx.ID_ANY, (0, 0), (0, 0))
        sizer = wx.BoxSizer(wx.VERTICAL) 
        self.browser = wx.html2.WebView.New(self)
        self.browser.SetPage(content, "")
        sizer.Add(self.browser, 1, wx.EXPAND|wx.ALL, 5) 
        self.SetSizer(sizer)