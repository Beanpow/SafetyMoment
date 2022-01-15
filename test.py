import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process, Pipe
import multiprocessing
import random
import time
import matplotlib
import matplotlib.cm as cm
matplotlib.use('Qt5Agg') 

class Test:
    def __init__(self) -> None:
        self.data = [[0, 50, 100]]

        self.isDraw = False


    def Update(self, conn):
        std = random.randint(50, 60)
        mean = random.randint(0, 100)

        # self.data = np.vstack((self.data, np.array([[mean - std, mean, mean + std]]).reshape((1,3)) ))
        self.data.append([mean - std, mean, mean + std])
        conn.send([mean - std, mean, mean + std])


    def DrawPic(self, conn, data):
        color = cm.viridis(0.7)
        data = np.array(data)

        total = 0
        start = time.time()
        
        fig = plt.figure()

        ax1 = fig.add_subplot(221)
        ax1.set_ylim([-50, 100])
        ax1.set_xlim([0, 50])

        line, = ax1.plot(data[-50:, 1])
        zone = ax1.fill_between(range(len(data[-50:, 0])), data[-50:, 0], data[-50:, 2], color=color, alpha=0.2)

        print(zone)

        fig.canvas.draw()

        axbackground = fig.canvas.copy_from_bbox(ax1.bbox)
        plt.show(block=False)

        while self.isDraw:
            total += 1
            print(total / (time.time() - start))

            # ax1.cla()

            temp = conn.recv()
            data = np.vstack((data, temp))

            line.set_data(range(len(data[-50:, 1])), data[-50:, 1])


            # a = ax1.plot(data[-50:, 1])
            # a = ax1.fill_between(range(len(data[-50:, 0])), data[-50:, 0], data[-50:, 2], color=color, alpha=0.2)
            

            fig.canvas.restore_region(axbackground)

            # redraw just the points
            # ax1.draw_artist(zone)
            ax1.draw_artist(line)


            # fill in the axes rectangle
            fig.canvas.blit(ax1.bbox)


            fig.canvas.flush_events()
            # plt.pause(0.0000000000001)
            # plt.draw()



def main():
    main_conn, plot_conn = Pipe()

    t = Test()
    p = Process(target=t.DrawPic, args=(plot_conn, t.data, ))
    t.isDraw = True
    p.start()

    indx = 0
    while True:
        t.Update(main_conn)
        indx += 1


if __name__ == "__main__":
    main()