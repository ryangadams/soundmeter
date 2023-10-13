from soundmeter.meter import Meter
from pubsub import pub
from math import log10

_volume = []


class MyMeter(Meter):
    def monitor(self, rms):
        decibel = 20 * log10(rms) if rms != 0 else 0
        pub.sendMessage("audio.volume", data=decibel)


def listen(data):
    """
    Listener for pubsub - stores the volume level in a list
    """
    global _volume
    _volume.append(data)


def done():
    """
    poststop hook for soundmeter
    prints the list of captured volumes
    """
    global _volume
    print("Metering is done, printing volumes")
    print(_volume)


if __name__ == "__main__":
    print(
        """
    Showing a simple sound meter implementation.
    Running the meter for 2 seconds, capturing the volume (in dB)
    Then at the end, printing the list of volumes
    """
    )
    pub.subscribe(listen, "audio.volume")

    sound_meter = MyMeter(
        collect=False,
        verbose=False,
        seconds=2,
    )
    sound_meter.poststop = done
    sound_meter.start()
