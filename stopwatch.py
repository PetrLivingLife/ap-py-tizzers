from tkinter import *
import time


class StopWatch(Frame):
    """ Implements a stop watch frame widget. """

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.make_widgets()

    def make_widgets(self):
        """ Make the time label. """
        lbl = Label(self, textvariable=self.timestr, font=("arial", 78))
        self._set_time(self._elapsedtime)
        lbl.pack(fill=X, expand=NO, pady=2, padx=2)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._set_time(self._elapsedtime)
        self._timer = self.after(100, self._update)

    def _set_time(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        hours = int(elap / 60 / 60)
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        # hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.timestr.set(f'{hours:02d}:{minutes:02d}:{seconds:02d}')

    def start(self):
        """ start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def stop(self):
        """ stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._set_time(self._elapsedtime)
            self._running = 0

    def reset(self):
        """ reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._set_time(self._elapsedtime)


def main():
    root = Tk(screenName="Stopwatch", className="Stopwatch")
    sw = StopWatch(root)
    sw.pack(side=TOP)

    btns = Frame(master=root)
    btns.pack(side=BOTTOM)
    Button(btns, text='start', command=sw.start).pack(side=LEFT)
    Button(btns, text='stop', command=sw.stop).pack(side=LEFT)
    Button(btns, text='reset', command=sw.reset).pack(side=LEFT)
    Button(btns, text='Quit', command=root.quit).pack(side=LEFT)

    root.mainloop()


if __name__ == '__main__':
    main()
