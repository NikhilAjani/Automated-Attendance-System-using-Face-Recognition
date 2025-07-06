import face_recognition
import numpy as np
from datetime import datetime
import os
import cv2
import keyboard
import pyautogui
import customtkinter as cstk
import tkinter as tk
from tkinter import filedialog, PhotoImage

path = "Student_Images"
only_name = r"only_name"
attend_csv_path = r"Attendance.csv"
cstk.set_appearance_mode("dark")
cstk.set_default_color_theme("green")
root = cstk.CTk()
root.geometry("1920x1080")
root.title("Facial Recognition System")

images = []
global image_names
global filesz
global encodeList
encodeList=[]
filesz=tuple()
image_names = []  
mylist = os.listdir(path)
savedImg = []
global attend_dict
attend_dict={}
print(mylist)
global del_names,del_ind
del_names=[]
del_ind=[]

def access():
    global images,image_names
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        image_names.append(os.path.splitext(cl)[0])
    print(image_names)
    image_names2 = image_names[:]

def find_encodings(images):
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodeList.append(encode)
    return encodeList

def save_img(imagesz,nami):
    savedImg=os.listdir(only_name)
    if nami not in savedImg:
        cv2.imwrite(rf"{only_name}+\{nami}.jpg", imagesz)

def markAttendance(name):
    print(name)
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'{name}, {time}, {date}\n')

def webcam_scan():
    cap = cv2.VideoCapture(0)

    while True:
        success,img = cap.read()
        
        img = cv2.flip(img, 1)
        height, width, _ = img.shape
        cen_x = int(width/2)
        cen_y = int(height/2)
        rec_width = 250
        rec_height = 250
        a1 = cen_x - int(rec_width/2)
        b1 = cen_y - int(rec_height/2)
        a2 = cen_x + int(rec_width/2)
        b2 = cen_y + int(rec_height/2)
        cv2.rectangle(img, (a1, b1), (a2, b2), (0, 0, 255), 2)
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS,faces_in_frame)

        for encodeFace,FaceLoc in zip(encoded_faces,faces_in_frame):
            matches = face_recognition.compare_faces(encoded_face_train,encodeFace,tolerance=0.5)
            faceDist = face_recognition.face_distance(encoded_face_train,encodeFace)
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                name = image_names[matchIndex].upper()
                y1,x2,y2,x1=FaceLoc
                y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4

                
                if a1 <= x1 <= a2 and b1 <= y1 <= b2 and a1 <= x2 <= a2 and b1 <= y2 <= b2:
                    cv2.rectangle(img, (x1,y1),(x2,y2) ,(0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2),(0, 255, 0), cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                    save_img(img, name)
                    markAttendance(name)

            else:
                    name = "Unknown"
                    y1, x2, y2, x1 = FaceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Camera',img)
        cv2.waitKey(1)

        if keyboard.is_pressed('esc'):
            cv2.destroyWindow('Camera')
            break

def take_a_pic():
    new_name = pyautogui.prompt('What is your name?',title="Name",default="new_image")

    if new_name in del_names:
        loc=del_ind[del_names.index(new_name)]
        image_names[loc]=new_name

        new_name += ".jpg"
        tk.messagebox.showinfo("Alert", "Look at the Camera in 3 sec !")
        result, new_img = cv2.VideoCapture(0).read()
        cv2.imwrite(rf"Student_Images\{new_name}", new_img)
        cv2.imshow("New Image", new_img)
        cv2.waitKey(0)
        cv2.destroyWindow('New Image')

    else:
        new_name+= ".jpg"
        tk.messagebox.showinfo("Alert", "Look at the Camera in 3 sec !")
        result, new_img = cv2.VideoCapture(0).read()
        cv2.imwrite(rf"Student_Images\{new_name}",new_img)
        cv2.imshow("New Image",new_img)
        cv2.waitKey(0)
        cv2.destroyWindow('New Image')

        images.append(cv2.imread(fr'Student_Images\{new_name}'))
        image_names.append(os.path.splitext(new_name)[0])
        print(os.path.splitext(new_name)[0])
        encodeList.append(face_recognition.face_encodings(images[-1])[0])

def open_images_to_delete():
    L1 = image_names
    L2 = []
    li2 = os.listdir(r"Student_Images")
    filesz = filedialog.askopenfilenames(title = "Select image files", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    print("Selected files:", filesz)
    for xx in filesz:
        os.remove(xx)
        xx = os.path.splitext(xx[xx.find('nce') + 4:])[0]
        del_ind.append(L1.index(xx))
        del_names.append(image_names[L1.index(xx)])
        image_names[L1.index(xx)] = "unknown"
        print("removed : ", xx)

    set_dif = []
    for x in li2:
        L2.append(os.path.splitext(x)[0])
    set_dif = list(set(L1).symmetric_difference(set(L2)))
    set_dif = list(filter(lambda t: t != "unknown", set_dif))
    removed_names = ""
    for j in set_dif:
        removed_names += j + " , "
    tk.messagebox.showinfo("showinfo", f"Faces removed = {len(set_dif)}\n{removed_names}\nClose the Window")

def delete_a_face():
    root1 = tk.Toplevel()
    root1.geometry("310x220")
    root1.title("delete")
    image2 = PhotoImage(file=r"path to \other_files\delete.png")
    bg1label = tk.Label(root1, image=image2, width=300, height=180)
    bg1label.pack()
    button9 = tk.Button(root1, text="Select the images", command=open_images_to_delete, width=300,pady=5)
    button9.pack()
    root1.mainloop()

def know_faces():
    os.startfile(r"Student_Images")

access()
encoded_face_train = find_encodings(images)
print("Encoding Completed..")

imag = tk.PhotoImage(file=r"path to \other_files\background.png")

frame = cstk.CTkFrame(master=root)
frame.pack(padx=60,pady=20,fill="both",expand=True)

label = cstk.CTkLabel(master=frame,text="Attendance System",font=("Times New Roman",24),compound="left")
label.pack(pady=12,padx=10)

bglabel = cstk.CTkLabel(master=frame,image=imag,text="", width=1080,height=1080)
bglabel.pack()

button1 = cstk.CTkButton(master=frame,text="Mark Attendance",command=webcam_scan,height=80,width=250,font=("Times New Roman",24))
button1.place(relx=0.3,rely=0.3,anchor="e")

button4 = cstk.CTkButton(master=frame,text="Student Images",command=know_faces,height=80,width=250,font=("Times New Roman",24))
button4.place(relx=0.75,rely=0.3,anchor="w")

button5 = cstk.CTkButton(master=frame,text="Add a New Face",command=take_a_pic,height=80,width=250,font=("Times New Roman",24))
button5.place(relx=0.3,rely=0.57,anchor="e")

button6 = cstk.CTkButton(master=frame,text="Delete a Face",command=delete_a_face,height=80,width=250,font=("Times New Roman",24))
button6.place(relx=0.75,rely=0.562,anchor="w")

root.mainloop()