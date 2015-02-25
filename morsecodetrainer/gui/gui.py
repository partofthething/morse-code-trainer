"""
GUI for Morse Code Trainer
"""

import threading
import gettext

import wx
import wx.grid

from morsecodetrainer.trainer import Trainer
from morsecodetrainer import config
from morsecodelib.config import WORDS_PER_MINUTE

myEVT_NEWWORD = wx.NewEventType()
EVT_NEWWORD = wx.PyEventBinder(myEVT_NEWWORD, 1)
myEVT_DONE = wx.NewEventType()
EVT_DONE = wx.PyEventBinder(myEVT_DONE, 1)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        #kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        # begin wxGlade: MyFrame.__init__
        self.num_words = 0
        self.answers = []
        self.morse_sound = None
        
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.level = wx.SpinCtrl(self.panel, wx.ID_ANY, "2", min=2, max=35)
        self.level_label = wx.StaticText(self.panel, wx.ID_ANY, "Number of letters", style=wx.ALIGN_RIGHT)
        self.accuracy = wx.StaticText(self.panel, wx.ID_ANY, "Accuracy: 0%")
        self.start = wx.Button(self.panel, wx.ID_ANY, "Start Training Session")
        self.stop = wx.Button(self.panel, wx.ID_ANY, "Stop Training Session")
        self.morsegrid = wx.grid.Grid(self.panel, wx.ID_ANY, size=(1, 1))
        
        # Menu Bar
        self.menu = wx.MenuBar()
        self.file = wx.Menu()
        self.settings = wx.MenuItem(self.file, wx.ID_ANY, "Settings", "", wx.ITEM_NORMAL)
        self.file.AppendItem(self.settings)
        self.close = wx.MenuItem(self.file, wx.ID_ANY, "Close", "", wx.ITEM_NORMAL)
        self.file.AppendItem(self.close)
        self.menu.Append(self.file, "File")
        self.help = wx.Menu()
        self.about = wx.MenuItem(self.help, wx.ID_ANY, "About", "", wx.ITEM_NORMAL)
        self.help.AppendItem(self.about)
        self.menu.Append(self.help, "Help")
        self.SetMenuBar(self.menu)
        # Menu Bar end
        self.statusbar = self.CreateStatusBar(3, 0)

        self.Bind(wx.EVT_BUTTON, self.on_start, self.start)
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.stop)
        self.Bind(EVT_NEWWORD, self.on_new_word)
        self.Bind(EVT_DONE, self.on_done)
        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(1000)    # 1 second interval


    def on_timer(self, event):
        if self.morse_sound:
            self.statusbar.SetStatusText("{0}".format(self.morse_sound.trainer.elapsed_seconds), 1)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Morse Code Trainer")
        self.accuracy.SetForegroundColour(wx.Colour(0, 255, 0))
        self.accuracy.SetFont(wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.morsegrid.CreateGrid(int(config.MINUTES_OF_TRAINING * WORDS_PER_MINUTE) + 100 , 3)
        self.morsegrid.SetColLabelValue(0, "You")
        self.morsegrid.SetColLabelValue(1, "Computer")
        self.morsegrid.SetColLabelValue(2, "Accurate")
        self.statusbar.SetStatusWidths([-1, 100, 100])
        # statusbar fields
        statusbar_fields = ["Morse Code Trainer", "0:00 / 5:00", "{0} WPM".format(WORDS_PER_MINUTE)]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        two_main_columns = wx.BoxSizer(wx.HORIZONTAL)
        control_sizer_base = wx.BoxSizer(wx.VERTICAL)
        lower_control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lower_control_sizer.Add(self.start, 0, 0, 0)
        lower_control_sizer.Add(self.stop, 0, 0, 0)
        upper_control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        upper_control_sizer.Add(self.level, 0, 0, 0)
        upper_control_sizer.Add(self.level_label, 0, 0, 0)
        control_sizer_base.Add(upper_control_sizer, 1,  wx.ALIGN_CENTER_HORIZONTAL, 0)
        control_sizer_base.Add(self.accuracy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        control_sizer_base.Add(lower_control_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        two_main_columns.Add(control_sizer_base, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        two_main_columns.Add(self.morsegrid, 1, wx.EXPAND, 0)
        self.panel.SetSizer(two_main_columns)
        main_sizer.Add(self.panel, 1, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        #main_sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def on_start(self, event):
        """
        Start the training.
        
        Start it in another thread. 
        """
        self.num_words = 0
        self.answers = []
        self.morsegrid.ClearGrid()
        self.morse_sound = SoundThread(self)
        self.morse_sound.start()
        self.morsegrid.SetCellBackgroundColour(0, 0, wx.GREEN)
        self.morsegrid.ForceRefresh()
        
    def on_stop(self, event):
        """
        Stop the training.
. 
        """
        self.morse_sound.stop()
        
        
    def on_new_word(self, evt):
        new_word = evt.GetValue()
        self.morsegrid.SetCellBackgroundColour(self.num_words, 0, wx.WHITE)
        self.morsegrid.SetCellBackgroundColour(self.num_words + 1, 0, wx.GREEN)
        self.morsegrid.ForceRefresh()
        #
        self.num_words +=1
        self.answers.append(new_word)
        
    def on_done(self, evt):
        """
        Training is done. Show results
        """
        correct = 0
        ai = 0
        self.morsegrid.SetCellBackgroundColour(self.num_words, 0, wx.WHITE)
        for ai,answer in enumerate(self.answers):
            self.morsegrid.SetCellValue(ai, 1, answer)
            user_input = self.morsegrid.GetCellValue(ai, 0)
            if user_input.upper() == answer:
                correct += 1
                self.morsegrid.SetCellBackgroundColour(ai, 2, wx.GREEN)
                self.morsegrid.SetCellValue(ai, 2, 'Yes!')
                
            else:
                self.morsegrid.SetCellValue(ai, 2, 'no')
                
        self.accuracy.SetLabel('Accuracy: {0:3.0f}%'.format( correct / float(ai+1) * 100))

class SoundThread(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self._parent = parent
        self.trainer = GuiTrainer(parent)
        self.trainer.set_num_characters(self._parent.level.GetValue())
        
    def run(self):
        self.trainer.run()
        self.end_training()
        
    def stop(self):
        self.trainer.stop()
        self.end_training()
        
    def end_training(self):
        evt = DoneEvent(myEVT_DONE, -1)
        wx.PostEvent(self._parent, evt)
        

class GuiTrainer(Trainer):
    def __init__(self, parent):
        self._parent = parent
        Trainer.__init__(self)
        
    def render_correct_answer(self, word):
        evt = NewWordEvent(myEVT_NEWWORD, -1, word)
        wx.PostEvent(self._parent, evt)

class NewWordEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value
        
    def GetValue(self):
        return self._value
    
class DoneEvent(wx.PyCommandEvent):
    """
    Training is done. 
    """
    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value
        
    def GetValue(self):
        return self._value
    
if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    gui = MyFrame(None, title = "Morse Code",size=(700, 600))
    app.SetTopWindow(gui)
    gui.Show()
    app.MainLoop()
    