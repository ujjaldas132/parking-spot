import cv2 as open_cv
import numpy as np
import os
import pickle

from colors import COLOR_WHITE
from drawing_utils import draw_contours
import logging

#TODO : make the cordiante fix so that you dont have to draw everytime
#TODO : want to redraw a box>>>> if a box have been drawn wronly , so there mightbe a process to redraw the box

#TODO a can detect a rectangle should be redraw , but how to remove that box

# TODO one thing we can do that first get each and every box then write to the output



class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = open_cv.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []
        self.saveCordinate={}

        # [(371, 332), (389, 359), (438, 354), (407, 328)] sample of cordiante
        # what ever present in the pickle upload to workplace
        if(os.path.exists("data\\pastCordinate.pickle")):
            dbfile = open("data\\pastCordinate.pickle", 'rb')
            db = pickle.load(dbfile)
            for keys in db:
                self.coordinates+=db[keys]
                # self.__handle_done()
                print(keys, '=>', db[keys])
                self.unique_box()
                print(keys, '=>', db[keys])
        print(self.saveCordinate)




        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)
        open_cv.setMouseCallback(self.caption, self.__mouse_callback)

    def generate(self):
        while True:
            open_cv.imshow(self.caption, self.image)
            key = open_cv.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        open_cv.destroyWindow(self.caption)
        """
        make self.ids=0 and final upload of the boxes
        """
        self.ids=0
        for box in self.saveCordinate:
            if(self.saveCordinate[box]!=[]):
                self.coordinates=self.saveCordinate[box].copy()
                self.__handle_done()

    def __mouse_callback(self, event, x, y, flags, params):

        if event == open_cv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1

            if self.click_count >= 4:
                self.unique_box()

            elif self.click_count > 1:
                self.__handle_click_progress()

        open_cv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        open_cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)

    def __handle_done(self):
        """
        to write the final box
        save ids and cordinate of the box in the self.output
        :return:
        """
        print(self.coordinates)
        open_cv.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color,
                     1)
        open_cv.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color,
                     1)

        self.click_count = 0
        coordinates = np.array(self.coordinates)


        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)

        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1


    def unique_box(self):
        """
        to store all unique box


        in each and every lick the cordinate will will uploaded and come to this function
        if new box is overlap with the previously build box >>> update the old box as new
        :return:
        """
        coordinates = np.array(self.coordinates)
        open_cv.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color,
                     1)
        open_cv.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color,
                     1)
        mid_x=(self.coordinates[0][0]+self.coordinates[1][0]+self.coordinates[2][0]+self.coordinates[3][0])/4
        mid_y=(self.coordinates[0][1]+self.coordinates[1][1]+self.coordinates[2][1]+self.coordinates[3][1])/4
        check=True
        for box in self.saveCordinate:
            x_max=max(self.saveCordinate[box][0][0],self.saveCordinate[box][1][0],self.saveCordinate[box][2][0],self.saveCordinate[box][3][0])
            x_min = min(self.saveCordinate[box][0][0], self.saveCordinate[box][1][0], self.saveCordinate[box][2][0],self.saveCordinate[box][3][0])
            y_max = max(self.saveCordinate[box][0][1], self.saveCordinate[box][1][1], self.saveCordinate[box][2][1],self.saveCordinate[box][3][1])
            y_min = min(self.saveCordinate[box][0][1], self.saveCordinate[box][1][1], self.saveCordinate[box][2][1],self.saveCordinate[box][3][1])
            if(mid_x>x_min and mid_y>y_min and mid_x<x_max and mid_y<y_max ):
                self.saveCordinate[box]=self.coordinates.copy()
                draw_contours(self.image, coordinates, str(box), COLOR_WHITE)
                check=False
                self.ids-=1
                self.click_count = 0
                break
        if check:
            draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)
            self.saveCordinate[self.ids+1]=self.coordinates.copy()
            logging.warning(self.saveCordinate)
        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1
        self.click_count = 0

