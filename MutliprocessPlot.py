import matplotlib.pyplot as plt
import numpy as np
import random
import time
from multiprocessing import Pipe, Process
import matplotlib

matplotlib.use('Qt5Agg') 


class MutliprocessPlot():   
    def __init__(self, conn, drawSize = 100, bound = [-100, 200]) -> None:
        self.conn = conn

        self.p = Process(target=self.DrawPic)
        self.p.daemon = True

        self.drawSize = drawSize
        self.isDraw = False
        self.bound = bound

        

    def initFig(self):
        self.fig = plt.figure(figsize=(13, 6))
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)

        self.ax1.set_ylim(self.bound)
        self.ax1.set_xlim([0, self.drawSize])
        self.ax2.set_ylim(self.bound)
        self.ax2.set_xlim([0, self.drawSize])
        self.ax3.set_ylim(self.bound)
        self.ax3.set_xlim([0, self.drawSize])
        self.ax4.set_ylim(self.bound)
        self.ax4.set_xlim([0, self.drawSize])

        plt.ioff()

    def SetStatus(self, status):
        self.isDraw = status

    def Start(self):
        self.p.start()


    def DrawPic(self):
        self.initFig()
        data = np.array([]).reshape(0,3)
        
        lineMean1, = self.ax1.plot(data[-self.drawSize:, 1], 'g-', lw = 1)
        lineStdUp1, = self.ax1.plot(data[-self.drawSize:, 2], 'g-', lw = 0.5)
        lineStdDown1, = self.ax1.plot(data[-self.drawSize:, 0], 'g-', lw = 0.5)
        lineMean2, = self.ax2.plot(data[-self.drawSize:, 1])
        lineStdUp2, = self.ax2.plot(data[-self.drawSize:, 2])
        lineStdDown2, = self.ax2.plot(data[-self.drawSize:, 0])
        lineMean3, = self.ax3.plot(data[-self.drawSize:, 1])
        lineStdUp3, = self.ax3.plot(data[-self.drawSize:, 2])
        lineStdDown3, = self.ax3.plot(data[-self.drawSize:, 0])
        lineMean4, = self.ax4.plot(data[-self.drawSize:, 1])
        lineStdUp4, = self.ax4.plot(data[-self.drawSize:, 2])
        lineStdDown4, = self.ax4.plot(data[-self.drawSize:, 0])

        self.fig.canvas.draw()

        axbackground1 = self.fig.canvas.copy_from_bbox(self.ax1.bbox)
        axbackground2 = self.fig.canvas.copy_from_bbox(self.ax2.bbox)
        axbackground3 = self.fig.canvas.copy_from_bbox(self.ax3.bbox)
        axbackground4 = self.fig.canvas.copy_from_bbox(self.ax4.bbox)

        plt.show(block=False)

        while self.isDraw:
            temp = self.conn.recv()
            data = np.vstack((data, temp))

            lineMean1.set_data(range(len(data[-self.drawSize:, 1])), data[-self.drawSize:, 1])
            lineStdUp1.set_data(range(len(data[-self.drawSize:, 2])), data[-self.drawSize:, 2])
            lineStdDown1.set_data(range(len(data[-self.drawSize:, 0])), data[-self.drawSize:, 0])
            lineMean2.set_data(range(len(data[-self.drawSize:, 1])), data[-self.drawSize:, 1])
            lineStdUp2.set_data(range(len(data[-self.drawSize:, 2])), data[-self.drawSize:, 2])
            lineStdDown2.set_data(range(len(data[-self.drawSize:, 0])), data[-self.drawSize:, 0])
            lineMean3.set_data(range(len(data[-self.drawSize:, 1])), data[-self.drawSize:, 1])
            lineStdUp3.set_data(range(len(data[-self.drawSize:, 2])), data[-self.drawSize:, 2])
            lineStdDown3.set_data(range(len(data[-self.drawSize:, 0])), data[-self.drawSize:, 0])
            lineMean4.set_data(range(len(data[-self.drawSize:, 1])), data[-self.drawSize:, 1])
            lineStdUp4.set_data(range(len(data[-self.drawSize:, 2])), data[-self.drawSize:, 2])
            lineStdDown4.set_data(range(len(data[-self.drawSize:, 0])), data[-self.drawSize:, 0])


            self.fig.canvas.restore_region(axbackground1)
            self.fig.canvas.restore_region(axbackground2)
            self.fig.canvas.restore_region(axbackground3)
            self.fig.canvas.restore_region(axbackground4)

            self.ax1.draw_artist(lineMean1)
            self.ax1.draw_artist(lineStdUp1)
            self.ax1.draw_artist(lineStdDown1)
            self.ax2.draw_artist(lineMean2)
            self.ax2.draw_artist(lineStdUp2)
            self.ax2.draw_artist(lineStdDown2)
            self.ax3.draw_artist(lineMean3)
            self.ax3.draw_artist(lineStdUp3)
            self.ax3.draw_artist(lineStdDown3)
            self.ax4.draw_artist(lineMean4)
            self.ax4.draw_artist(lineStdUp4)
            self.ax4.draw_artist(lineStdDown4)


            self.fig.canvas.blit(self.ax1.bbox)
            self.fig.canvas.blit(self.ax2.bbox)
            self.fig.canvas.blit(self.ax3.bbox)
            self.fig.canvas.blit(self.ax4.bbox)

            self.fig.canvas.flush_events()
            # plt.pause(0.0000000000001)
            # plt.draw()



def Update(conn):
    std = random.randint(50, 60)
    mean = random.randint(0, 100)
    conn.send([mean - std, mean, mean + std])

def main():
    main_conn, plot_conn = Pipe()

    t = MutliprocessPlot(plot_conn)
    t.SetStatus(True)
    t.Start()

    while True:
        Update(main_conn)


if __name__ == "__main__":
    main()