"""
My first application
"""
import os
import sys

from PIL import Image 
import PIL

import cv2
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import imutils

from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil

import numpy as np
from skimage.transform import resize

import pickle
import sqlite3

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel
from PySide2.QtGui import QIcon, QPixmap, QImage

import requests
import json
import urllib3
import mysql.connector as mc
urllib3.disable_warnings()
from insert import Ui_Form
class Deployer(QtWidgets.QDialog):
    """
    An instance of this class is a GUI that has the potential to
    install standard packages, delete specified paths and deliver custom files.
    It currently has no functionality, but functionality can be added where it
    says #add functionality HERE to make it fully functional.
    """

    def __init__(self):
        super().__init__()

        #create the widgets for the window
        self.createVerticalLabels("img\\vehicle.gif")
        self.createFormGroupBox()

        #create the main layout
        mainLayout = QtWidgets.QVBoxLayout()
	    
        #add the widgets to the main layout
        mainLayout.addWidget(self.verticalLabels)
        self.createVerticalLabels("img\\installPackages.jpg")
        mainLayout.addWidget(self.verticalLabels)
        mainLayout.addWidget(self.formGroupBox)

        #set the layout
        self.setLayout(mainLayout)

        #set the window title and image in the upper left corner
        self.setWindowTitle('Vehicle plate recognition')
        self.setWindowIcon(QtGui.QIcon('img\\0.png')) 
       

    def createVerticalLabels(self, image):
        """
        Creates a Vertical Box and fills it will the given image
        Parameter image: The relative path to the image
        Precondition: image is a string
        """
        #set the layout to Vertical Box Layout
        vbox = QtWidgets.QVBoxLayout(self)
        self.verticalLabels = QtWidgets.QGroupBox("")

        #add the picture to the window
        pixmap = QtGui.QPixmap(image)
        pixmap = pixmap.scaled(1100, 1200, QtCore.Qt.KeepAspectRatio)
        lbl = QtWidgets.QLabel(self)
        lbl.setAlignment(QtCore.Qt.AlignHCenter)
        lbl.setPixmap(pixmap)
        vbox.addWidget(lbl)

        #set the layout
        self.verticalLabels.setLayout(vbox)


    def createFormGroupBox(self):
        """
        Creates the text box's to fill in Machine Name,
        User Name, Deadline Pool Name, Deadline Version
        """
        #set the layout to Form Layout
        self.formGroupBox = QtWidgets.QGroupBox("")
        layout = QtWidgets.QFormLayout()

        btn2 = QtWidgets.QPushButton("Insert Plate To DB", self)
        btn2.clicked.connect(self.insert)

        layout.addRow(btn2)
        #create the field for Machine Name
        btn = QtWidgets.QPushButton("Select Vehicle Images", self)
        btn.clicked.connect(self.selectImage)

        layout.addRow(QtWidgets.QLabel("Vehicle Plate Image:"), btn)


       
        self.formGroupBox.setLayout(layout)

    def selectImage(self):
       
        w2 = W2()
        if w2.exec_():
            self.w3 = W3()    
            self.w3.show()

    def insert(self):
        # execfile('C:/Users/USER/Desktop/vpnrs/insert.py')  
        # self.ui.setupUi()  
        print('btn clicked')  

class W2(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        #create the widgets for the window
        self.createVerticalLabels("img\\vehicle.gif")
        self.deliverCustomFiles()

        #create the main layout
        mainLayout = QtWidgets.QVBoxLayout()
	    
        self.createVerticalLabels("img\\deliverCustomFiles.jpg")
        mainLayout.addWidget(self.verticalLabels)
        # mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.deliverCustomFiles)

        #set the layout
        self.setLayout(mainLayout)

        #set the window title and image in the upper left corner
        self.setWindowTitle('Vehicle plate recognition')
        self.setWindowIcon(QtGui.QIcon('img\\0.png'))

    def createVerticalLabels(self, image):
        """
        Creates a Vertical Box and fills it will the given image
        Parameter image: The relative path to the image
        Precondition: image is a string
        """
        #set the layout to Vertical Box Layout
        vbox = QtWidgets.QVBoxLayout(self)
        self.verticalLabels = QtWidgets.QGroupBox("")

        #add the picture to the window
        pixmap = QtGui.QPixmap(image)
        pixmap = pixmap.scaled(1100, 1200, QtCore.Qt.KeepAspectRatio)
        lbl = QtWidgets.QLabel(self)
        lbl.setAlignment(QtCore.Qt.AlignHCenter)
        lbl.setPixmap(pixmap)
        vbox.addWidget(lbl)

        #set the layout
        self.verticalLabels.setLayout(vbox)

    def deliverCustomFiles(self):
        """
        Creates the text box's to fill in the Source Folder 
        and Destination Folder under the Deliver Custom Files label.
        """
        #set the layout to Form Layout
        self.deliverCustomFiles = QtWidgets.QGroupBox("")
        layout = QtWidgets.QFormLayout()

        # name, t = QtWidgets.QFileDialog.getSaveFileName(
        #     self, 'Save File', "")
        # if name:
        #     print("FILENAME")
        #     print(name)


        ####################################
        #####  codes for the cnn     #######
        #####      configuration     #######
        ####################################
        # read the image collected
        filename = './car6.jpg'

        if os.path.exists('output'):
            shutil.rmtree('output')

        os.makedirs('output')

        self.cap = cv2.VideoCapture(filename)
        # cap = cv2.VideoCapture(0)
        count = 0
        while self.cap.isOpened():
            ret,frame = self.cap.read()
            if ret == True:
                cv2.imshow('Vehicle Plate',frame)
                cv2.imwrite("./output/frame.jpg", frame)
                count = count + 1
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()
        #
        # car image -> grayscale image -> binary image
        car_image = imread("./output/frame.jpg", as_gray=True)
        #car_image = imutils.rotate(car_image, 270)
        #car_image = imread(car_image, as_gray=True)
        print(car_image.shape)

        gray_car_image = car_image * 255
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.imshow(gray_car_image, cmap="gray")
        threshold_value = threshold_otsu(gray_car_image)
        binary_car_image = gray_car_image > threshold_value

        ax2.imshow(binary_car_image, cmap="gray")

        label_image = measure.label(binary_car_image)

        # getting the maximum width, height and minimum width and height that a license plate can be
        plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
        plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
        min_height, max_height, min_width, max_width = plate_dimensions
        plate_objects_cordinates = []
        plate_like_objects = []

        fig, (ax1) = plt.subplots(1)
        ax1.imshow(gray_car_image, cmap="gray")
        flag =0
        # regionprops creates a list of properties of all the labelled regions
        for region in regionprops(label_image):
            # print(region)
            if region.area < 50:
                #if the region is so small then it's likely not a license plate
                continue
                # the bounding box coordinates
            min_row, min_col, max_row, max_col = region.bbox

            region_height = max_row - min_row
            region_width = max_col - min_col

            # ensuring that the region identified satisfies the condition of a typical license plate
            if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
                flag = 1
                plate_like_objects.append(binary_car_image[min_row:max_row,
                                        min_col:max_col])
                plate_objects_cordinates.append((min_row, min_col,
                                                max_row, max_col))
                rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                            linewidth=2, fill=False)
                ax1.add_patch(rectBorder)

        if(flag==0):
            min_height, max_height, min_width, max_width = plate_dimensions2
            plate_objects_cordinates = []
            plate_like_objects = []

            fig, (ax1) = plt.subplots(1)
            ax1.imshow(gray_car_image, cmap="gray")

            # regionprops creates a list of properties of all the labelled regions
            for region in regionprops(label_image):
                if region.area < 50:
                    #if the region is so small then it's likely not a license plate
                    continue
                    # the bounding box coordinates
                min_row, min_col, max_row, max_col = region.bbox
                # print(min_row)
                # print(min_col)
                # print(max_row)
                # print(max_col)

                region_height = max_row - min_row
                region_width = max_col - min_col
                # print(region_height)
                # print(region_width)

                # ensuring that the region identified satisfies the condition of a typical license plate
                if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
                    # print("hello")
                    plate_like_objects.append(binary_car_image[min_row:max_row,
                                            min_col:max_col])
                    plate_objects_cordinates.append((min_row, min_col,
                                                    max_row, max_col))
                    rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                                linewidth=2, fill=False)
                    ax1.add_patch(rectBorder)
                    # let's draw a red rectangle over those regions
            # print(plate_like_objects[0])
            # plt.show()
        # salute_label.text = "Hello {}!".format(name_input.value)
        # The invert was done so as to convert the black pixel to white pixel and vice versa


        ######SEGMENT CHARACTERS
        license_plate = np.invert(plate_like_objects[0])

        labelled_plate = measure.label(license_plate)

        fig, ax1 = plt.subplots(1)
        ax1.imshow(license_plate, cmap="gray")
        # the next two lines is based on the assumptions that the width of
        # a license plate should be between 5% and 15% of the license plate,
        # and height should be between 35% and 60%
        # this will eliminate some
        character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
        min_height, max_height, min_width, max_width = character_dimensions

        characters = []
        counter=0
        column_list = []
        for regions in regionprops(labelled_plate):
            y0, x0, y1, x1 = regions.bbox
            region_height = y1 - y0
            region_width = x1 - x0

            if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
                roi = license_plate[y0:y1, x0:x1]

                # draw a red bordered rectangle over the character.
                rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                            linewidth=2, fill=False)
                ax1.add_patch(rect_border)

                # resize the characters to 20X20 and then append each character into the characters list
                resized_char = resize(roi, (20, 20))
                characters.append(resized_char)

                # this is just to keep track of the arrangement of the characters
                column_list.append(x0)
        # print(characters)
        # plt.show()


        #####PREDICT CHARACTERS

        print("Loading model")
        filename = 'finalized_model.sav'
        model = pickle.load(open(filename, 'rb'))

        print('Model loaded. Predicting characters of number plate')
        classification_result = []
        for each_character in characters:
            # converts it to a 1D array
            each_character = each_character.reshape(1, -1);
            result = model.predict(each_character)
            classification_result.append(result)

        print('Classification result')
        print(classification_result)

        plate_string = ''
        for eachPredict in classification_result:
            plate_string += eachPredict[0]

        print('Predicted license plate')
        print(plate_string)

        # it's possible the characters are wrongly arranged
        # since that's a possibility, the column_list will be
        # used to sort the letters in the right order

        column_list_copy = column_list[:]
        column_list.sort()
        rightplate_string = ''
        for each in column_list:
            rightplate_string += plate_string[column_list_copy.index(each)]

        print('License plate :')
        print(rightplate_string)

        ####################################
        #####  codes for the cnn     #######
        #####      configuration     #######
        ####################################

        ####################################
        ##### codes for the database #######
        #####      configuration     #######
        ####################################


        try:
            mydb = mc.connect(
 
                host="localhost",
                user="root",
                password="",
                database="vehiclerecognition"
            )
 
            mycursor = mydb.cursor(buffered=True)

            sql = """SELECT * FROM `user` WHERE `plate`=%s"""
            mycursor.execute(sql, (rightplate_string,))

            result = mycursor.fetchall()
            for row in result:
                #print (row[1])
                #create the Enter Source Folder to Transport text field
                transportMessage = 'Vehicle Image :'
                l1 = QLabel()
                pixmap = QPixmap(QImage("./output/frame.jpg"))
                pixmap = pixmap.scaled(300, 400, QtCore.Qt.KeepAspectRatio)
                l1.setPixmap(pixmap)
                layout.addRow(QtWidgets.QLabel(transportMessage), l1) 
                self.lineEdit6 = QtWidgets.QLabel(self)
                self.lineEdit6.setText(row[1])
                destinationMessage = "Vehicle Owner :"
                layout.addRow(QtWidgets.QLabel(destinationMessage), self.lineEdit6)

                self.lineEdit7 = QtWidgets.QLabel(self)
                self.lineEdit7.setText(row[3])
                destinationMessage = "Phone Number :"
                layout.addRow(QtWidgets.QLabel(destinationMessage), self.lineEdit7)

                self.lineEdit5 = QtWidgets.QLabel(self)
                self.lineEdit5.setText(rightplate_string)
                destinationMessage = "Licence Plate :"
                layout.addRow(QtWidgets.QLabel(destinationMessage), self.lineEdit5)

                

                if rightplate_string:
            
                    greeting = 'HELLO, '
                    to_name = row[1]
                    to_plate = rightplate_string
                    to_message = ' YOUR CAR IS WRONGLY PARKED PLEASE COME AND RE_ADJUST' 
                    conc_message = greeting + to_name + ' ' + '('  + to_plate + ')' + to_message
                    sender = 'platenumberdetector'      
                    to = row[3]        
                    message = conc_message
                    type = '0'       
                    routing = '3'    
                    token = 'UYOMpEMjP1Eo7tV7DI7QTZjRCO1hqSsqZqJWqweiRjHKn7alH2WiYjKprtrjvzNT7k2oOt12uEsB0zSRBrk4s1LqYcZtU0AgXlBx'

                    payload={
                        'sender': sender,
                        'to': to,
                        'message': message,
                        'type': type,
                        'routing': routing,
                        'token': token,
                    }

                    baseurl = 'https://smartsmssolutions.com/api/json.php?'

                    response = requests.get(baseurl, params=payload)
                    #response = json_decode(response)
                   
                    print(response)
                    # print(response.json())
                    self.lineEdit8 = QtWidgets.QLabel(self)
                    self.lineEdit8.setText("")
                    destinationMessage = "SMS Status :"
                    layout.addRow(QtWidgets.QLabel(destinationMessage), self.lineEdit8)
                    


            mydb.commit()
            
        except mc.Error as e:
            print(e)
       
        
        
        ####################################
        ##### codes for the database #######
        #####      configuration     #######
        ####################################
	    
        
        #set the layout
        self.deliverCustomFiles.setLayout(layout)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = Deployer()
    sys.exit(dialog.exec_())


