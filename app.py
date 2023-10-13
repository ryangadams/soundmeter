from threading import Thread, Event

from monitor_ui import Plot, MonitorUI, TextBox
from my_sound_meter import MyMeter

monitoring_stopped = Event()


def monitor_with_event(event):
    sound_meter = None
    while not event.isSet():
        sound_meter = MyMeter(
            collect=False,
            verbose=False,
            seconds=2,
        )
        sound_meter.start()

    if sound_meter and hasattr(sound_meter, "stop"):
        sound_meter.stop()


if __name__ == "__main__":
    thread = Thread(target=monitor_with_event, args=(monitoring_stopped,))
    thread.start()
    app = MonitorUI(stop_monitor_event=monitoring_stopped)
    Plot(app.frm)
    # TextBox(app.frm)
    app.MainLoop()
