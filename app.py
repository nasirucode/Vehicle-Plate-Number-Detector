"""
android app
"""
import toga
from toga.style import Pack
from toga.style.pack import *

from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import imutils
import cv2

from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

import numpy as np
from skimage.transform import resize

import pickle

import sqlite3


class platenumber(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        name_label = toga.Label('VEHICLE PLATE NUMBER DETECTION SYSTEM', style=Pack(text_align=CENTER))
        # name_input = toga.Icon()
        owner_detail = toga.Label("", style=Pack(text_align=LEFT))
        owner_phone = toga.Label("", style=Pack(text_align=LEFT))
        plate_label = toga.Label("", style=Pack(text_align=LEFT))
        success_info = toga.Label("", style=Pack(color='GREEN', font_size=7))
        salute_image = toga.ImageView('images/image1.jpg')
        # input_form = toga.TogaForm()
        # input_form=toga.ImageView("")

        def button_handler(widget):


            ####DETECT PLATENUMBER
            filename = './car8.jpg'

            if os.path.exists('output'):
                shutil.rmtree('output')

            os.makedirs('output')

            cap = cv2.VideoCapture(filename)
            #cap = cv2.VideoCapture(0)
            count = 0
            while cap.isOpened():
                ret,frame = cap.read()
                if ret == True:
                    cv2.imshow('window-name',frame)
                    cv2.imwrite("./output/frame%d.jpg" % count, frame)
                    # count = count + 1
                    # if cv2.waitKey(0) & 0xFF == ord('q'):
                    if cv2.waitKey(10) == 27:
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()
            #
            # car image -> grayscale image -> binary image
            #car_image = imread("./output/frame%d.jpg"%(count-1), as_gray=True)
            #car_image = imread("./output/frame%d.jpg"%(count), as_gray=True)web
            # car_image = imutils.rotate(car_image, 270)
            car_image = imread("src/licenseplate/Test/car 1.jpg", as_gray=True)
            car_image = toga.ImageView(car_image)
            # it should be a 2 dimensional array
            print(car_image.shape)

            # the next line is not compulsory however, a grey scale pixel
            # in skimage ranges between 0 & 1. multiplying it with 255
            # will make it range between 0 & 255 (something we can relate better with

            gray_car_image = car_image * 255
            fig, (ax1, ax2) = plt.subplots(1, 2)
            ax1.imshow(gray_car_image, cmap="gray")
            threshold_value = threshold_otsu(gray_car_image)
            binary_car_image = gray_car_image > threshold_value
            # print(binary_car_image)
            ax2.imshow(binary_car_image, cmap="gray")
            # ax2.imshow(gray_car_image, cmap="gray")
            # plt.show()

            # CCA (finding connected regions) of binary image


            # this gets all the connected regions and groups them together
            label_image = measure.label(binary_car_image)

            # print(label_image.shape[0]) #width of car img

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
                    flag = 1
                    plate_like_objects.append(binary_car_image[min_row:max_row,
                                            min_col:max_col])
                    plate_objects_cordinates.append((min_row, min_col,
                                                    max_row, max_col))
                    rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                                linewidth=2, fill=False)
                    ax1.add_patch(rectBorder)
                    # let's draw a red rectangle over those regions
            if(flag == 1):
                # print(plate_like_objects[0])
                plt.show()




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

            ###DATABASE
            conn = sqlite3.connect('licenceplate.db')
            conn.execute("DELETE FROM VEHICLEOWNERS")
            conn.commit()
            conn.execute('''CREATE TABLE IF NOT EXISTS VEHICLEOWNERS(ID INT PRIMARY KEY  AUTOINCREMENT,
                                                                    NAME           TEXT    NOT NULL,
                                                                    PLATENUMBER    CHAR(50)     NOT NULL,
                                                                    PHONENUMBER    CHAR(50)  NOT NULL);''')
            conn.execute(''' INSERT INTO VEHICLEOWNERS(NAME,PLATENUMBER,PHONENUMBER) VALUES('FELIX ALEX', 'YG17391A','09020275269');''')
            # conn.execute(''' INSERT INTO VEHICLEOWNERS(NAME,PLATENUMBER,PHONENUMBER) VALUES('UCHE ALEX', 'GWA952CP','08133472158');''')
            # conn.execute(''' INSERT INTO VEHICLEOWNERS(NAME,PLATENUMBER,PHONENUMBER) VALUES('ADA ALEX', 'MHO1AV8866','0902021589');''')
            # conn.execute(''' INSERT INTO VEHICLEOWNERS(NAME,PLATENUMBER,PHONENUMBER) VALUES('ANY NAME', '','');''')
            conn.commit()
            sysplatenumber = rightplate_string
            cursor = conn.execute("SELECT * FROM VEHICLEOWNERS")
            for row in cursor:
                dbname = row[1]
                dbplatenumber = row[2]
                dbphonenumber = row[3]
                print(dbname)
            plate_label.text = "Licence Plate Number Captured:  {}".format(rightplate_string)
            owner_detail.text = "Owner Name:  {}".format(dbname)
            owner_phone.text = "Owner Phone:  {}".format(dbphonenumber)
            if dbplatenumber == rightplate_string:
                
                import requests
                import json
                import urllib3
                urllib3.disable_warnings()

                greeting = 'HELLO, '
                to_name = dbname
                to_plate = rightplate_string
                to_message = ' YOUR CAR IS WRONGLY PARKED PLEASE COME AND RE_ADJUST' 
                conc_message = greeting + to_name + ' ' + '('  + to_plate + ')' + to_message
                sender = 'platenumberdetector'      
                to = dbphonenumber         
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
                print(response.json())

        
        button = toga.Button('Capture', on_press=button_handler)
        button.style.padding = 20
        button.style.flex = 1
        button.style.width = 100
        button.style.color = 'WHITE'
        button.style.font_size = 10
        button.style.align = CENTER
        name_label.style.update(padding_left=10, color='WHITE', font_size=15, font_weight=BOLD)
        # name_input.style.update(width=200, padding_top=10, padding_left=10)
        plate_label.style.update(padding_top=10, padding_left=10, color='WHITE', font_size=10, font_weight=BOLD)
        owner_detail.style.update(padding_top=10, padding_left=10, color='WHITE', font_size=10, font_weight=BOLD)
        owner_phone.style.update(padding=10, padding_left=10, color='WHITE', font_size=10, font_weight=BOLD)
        salute_image.style.update(padding=10, height=250)


        main_box.add(name_label)
        #main_box.add(name_input)
        main_box.add(salute_image)
        main_box.add(plate_label)
        main_box.add(owner_detail)
        main_box.add(owner_phone)
        # main_box.add(name_input)
        # main_box.add(input_form)
        main_box.add(button)


        main_box.style.update(direction=COLUMN, padding_top=10, background_color='GRAY', height=800)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return platenumber()


