import wx
from matplotlib import pyplot as plt, animation as animation
from matplotlib.axes import Axes
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from pubsub import pub


class Plot(wx.Panel):
    _volume = [0 for x in range(1, 300)]
    ax = None

    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = plt.figure(dpi=dpi, figsize=(2, 2))
        self.canvas = FigureCanvas(self, -1, self.figure)
        # self.axes = self.figure.gca()
        self.plot_graph([], "start")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)

        pub.subscribe(self.update_volume, "audio.volume")

        self.animator = animation.FuncAnimation(
            self.figure, self.update_volume_control, interval=500
        )

        self.add_parent_sizer(parent)

    def update_volume(self, data):
        self._volume.append(data)

    def update_volume_control(self, a):
        self._volume = self._volume[-300:]
        label = f"{self._volume[0]}" if len(self._volume) > 0 else "empty"
        self.plot_graph(self._volume, label)

    def plot_graph(self, data, label):
        if hasattr(self.ax, "remove"):
            self.ax.remove()
        self.ax: Axes = self.figure.add_subplot(
            111, frameon=False, label=label, xticks=[], yticks=[]
        )
        self.ax.set_ylim(top=120.0)

        self.add_guidelines()
        self.ax.plot(data)

    def add_guidelines(self):
        self.ax.axhline(y=40, linewidth=0.5, color="g", ls="--")  # "silence"
        plt.text(-20, 41, "Quiet", fontsize="small")
        self.ax.axhline(y=65, linewidth=0.5, color="orange", ls="--")  # "speech"
        plt.text(-20, 66, "Speech", fontsize="small")
        self.ax.axhline(y=90, linewidth=0.5, color="r", ls="--")  # "loud"
        plt.text(-20, 91, "Loud", fontsize="small")

    def add_parent_sizer(self, parent):
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(self, 1, wx.SHAPED, 0)
        frame_sizer.SetSizeHints(parent)
        parent.SetSizer(frame_sizer)


class TextBox(wx.TextCtrl):
    _volume = []

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        pub.subscribe(self.update_volume, "audio.volume")

    def update_volume(self, data):
        self._volume.append(data)
        wx.CallAfter(self.set_text_value)

    def set_text_value(self):
        output = ", ".join([str(x) for x in self._volume])
        self.ChangeValue(output)


class MonitorUI(wx.App):
    frm = None

    def __init__(self, stop_monitor_event):
        wx.App.__init__(self)
        self.stop_monitor_event = stop_monitor_event

    def OnInit(self):
        self.frm = wx.Frame(None, -1, title="Your sound level")
        self.frm.Bind(wx.EVT_CLOSE, self.close_app)
        self.frm.Show()
        self.SetTopWindow(self.frm)
        return True

    def close_app(self, event):
        self.stop_monitor_event.set()

        wx.CallAfter(self.frm.Destroy)
