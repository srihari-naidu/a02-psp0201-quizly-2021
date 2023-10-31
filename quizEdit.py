#----------------------------------------------------------------------------------------------------#

############# imports #############
import os
import json
import tkinter as tk
import tkinter.messagebox as mb
import random,string 

import mainPage
###################################

#----------------------------------------------------------------------------------------------------#

################## methods ##################
def loadJSON(file):
    with open(file) as f:
        data = json.load(f)
    return data

def writeJSON(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)
#############################################

#----------------------------------------------------------------------------------------------------#

#################################### const. ####################################
QCA_DATA_FILENAME  = 'quiz-qca-data.json'
TEACHER_QUIZ_INFO_FILENAME = 'teacher-quiz-info.json'
################################################################################

#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#

def editQuiz_info(root, quizTitle, username, userdata):

    if quizTitle != None:
        quizTitle, quizTitleID = quizTitle.split(':')

    TEACHER = username


    rootFrame = tk.Frame(root)
    rootFrame.grid(sticky="NSEW")
    info_background = tk.Canvas(rootFrame, bg="Cornflower Blue", height=500, width=800, highlightthickness=0)
    info_background.pack()
    root.title('Quizlyy - Quiz Form')

    l_foreground = tk.Frame(info_background, bg = "white")
    l_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

    if quizTitle != None:
        title = tk.Label(l_foreground, text= quizTitle, fg="black", bg="white", font="Calibri 38")
        title.place(x=310, y=70, anchor="center")

        tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
        quizDictList = tData[TEACHER]

        for quizDict in quizDictList:
            if quizDict["Quiz Name"] == quizTitle and quizDict["ID"] == quizTitleID:
                init_quizTopic = quizDict["Quiz Topic"]
                init_quizName = quizDict["Quiz Name"]
                ID = quizDict["ID"]
                init_quizDP = quizDict["D/P"]


        topic_label = tk.Label(l_foreground,text="Quiz Topic :",bg="white", font=("calibre",16))
        topic_label.place(relx=0.17,rely=0.32)
        topic_entry = tk.Entry(l_foreground,width=28,bd=5,relief=tk.RIDGE, font=("calibre",13),justify=tk.CENTER)
        topic_entry.insert(0,init_quizTopic)
        topic_entry.place(relx=0.37,rely=0.32)

        name_label = tk.Label(l_foreground,text="Quiz Name :",fg="black",bg="white", font=("calibre",16))
        name_label.place(relx=0.17,rely=0.44)
        name_entry = tk.Entry(l_foreground,width=28,bd=5,relief=tk.RIDGE,font=("calibre",13),justify=tk.CENTER)
        name_entry.insert(0,init_quizName)
        name_entry.place(relx=0.37,rely=0.44)


        ## Radiobutton ##
        rad_value = tk.IntVar()
        rad_value.set(0)
        options = {0: "Draft", 1: "Published" }

        if init_quizDP == "Draft":
            rad_value.set(1)
        elif init_quizDP == "Published":
            rad_value.set(2)

        draft_entry = tk.Radiobutton(l_foreground, text=options[0], font=("calibre",14,),variable=rad_value,value=1,bg="white")
        publish_entry = tk.Radiobutton(l_foreground, text=options[1], font=("calibre",14), variable=rad_value,value=2 ,bg="white")
        draft_entry.place(relx=0.38,rely=0.58)
        publish_entry.place(relx=0.55,rely=0.58)


        ## Get value from Radiobutton (Draft/ Published) ##
        def dpValue():
            D_P =str(rad_value.get())

            if  D_P == "1":
                return ("Draft")
            elif D_P == "2":
                return ("Published")

        # unique ID generator #
        def idNum(size):
            idNum ="".join([random.choice(string.digits)
                            for num in range(size)])
            return idNum

        def backOut():
            rootFrame.destroy()

            TEACHER = username
            tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
            quizDictList = tData[TEACHER]

            tData_lst = []
            for quizDict in quizDictList:
                quizName = quizDict["Quiz Name"]
                quizID = quizDict["ID"]
                quizStatus = quizDict["D/P"]

                sub_tData_lst = [f'{quizName}:{quizID}', quizStatus, ""]
                tData_lst.append(sub_tData_lst)
                
            DATA_LST = tData_lst
            if DATA_LST == []:
                DATA_LST = [[]]
            mainPage.teacherPage(root, TEACHER, DATA_LST)
            

        def update(): 
            # Get value from entry & radiobutton #
            NewTopic = topic_entry.get()
            NewName = name_entry.get()
            NewDP = dpValue()

            # Check if user enters all the required fields #
            if NewName == "" or NewTopic == "" or NewDP == None:
                mb.showerror("Error", "Please FILL IN the required fields")
        
            else:
                updated_quizDict = {
                    "Quiz Topic": NewTopic,
                    "Quiz Name": NewName,
                    "ID": ID,
                    "D/P": NewDP
                }

                tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
                quizDictList = tData[TEACHER]

                # get the topic of the current quiz
                for quizDict in quizDictList:
                    if quizDict["Quiz Name"] == quizTitle and quizDict["ID"] == quizTitleID:
                        quizDictIndex = quizDictList.index(quizDict)
                        OldTopic = quizDict["Quiz Topic"]
                        OldName = quizDict["Quiz Name"]
                        OldDP = quizDict["D/P"]

                # get quizzes under the old topic
                quizName_inOldTopic = []
                for quizDict in quizDictList:
                    if quizDict["Quiz Topic"] == OldTopic:
                        quizName_inOldTopic.append(quizDict["Quiz Name"])

                # If no changes have been made (newName=oldName, newTopic=oldTopic, newDP=oldDP)
                if (NewName == OldName and NewTopic == OldTopic and NewDP == OldDP):
                    mb.showinfo("Info", "No changes have been made.")
                    backOut()

                # If changes made to the Status, and the (newName==oldName, newTopic=oldTopic)
                elif NewName == OldName and NewTopic == OldTopic and NewDP != OldDP:

                    if NewDP == "Draft":
                        quizDictList[quizDictIndex] = updated_quizDict
                        tData[TEACHER] = quizDictList
                        writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                        mb.showinfo("QUIZ STATUS:","Your quiz has now been Drafted.")                                                     
                        backOut()
                    
                    elif NewDP == "Published":
                        QUIZ = f'{NewName}:{ID}'
                        qcaData = loadJSON(QCA_DATA_FILENAME)

                        if QUIZ in qcaData and qcaData[QUIZ] != []:
                            quizDictList[quizDictIndex] = updated_quizDict
                            tData[TEACHER] = quizDictList
                            writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                            mb.showinfo("QUIZ STATUS:","Your quiz has now been Published.")                                                     
                            backOut()

                        elif QUIZ not in qcaData or qcaData[QUIZ] == []:
                            mb.showerror(
                                "QUIZ STATUS:",
                                "Your quiz cannot be published as the QCAs for this quiz has not be set-up.")                                                     
                            backOut()
            
                # If changes made to the Name, and the (newName!=oldName, newTopic=oldTopic)
                elif NewName != OldName and NewTopic == OldTopic:

                    # If newName already exists
                    if NewName in quizName_inOldTopic:
                        mb.showerror("Error", "A quiz of this Name, under this Topic, already exists. Try again.")
                    else:
                        quizDictList[quizDictIndex] = updated_quizDict
                        tData[TEACHER] = quizDictList
                        writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)
                        
                        oldQUIZ = f'{OldName}:{ID}'
                        newQUIZ = f'{NewName}:{ID}'

                        qcaData = loadJSON(QCA_DATA_FILENAME)
                        if oldQUIZ in qcaData:
                            qcaData[newQUIZ] = qcaData[oldQUIZ]
                            del qcaData[oldQUIZ]
                        writeJSON(qcaData, QCA_DATA_FILENAME)

                        mb.showinfo("Successful ","Quiz Name has been updated.")

                        if NewDP != OldDP:
                            if NewDP == "Draft":
                                quizDictList[quizDictIndex] = updated_quizDict
                                tData[TEACHER] = quizDictList
                                writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                mb.showinfo("QUIZ STATUS:","Your quiz has now been Drafted.")                                                     
                                backOut()
                    
                            
                            elif NewDP == "Published":
                                QUIZ = f'{NewName}:{ID}'
                                qcaData = loadJSON(QCA_DATA_FILENAME)

                                if QUIZ in qcaData and qcaData[QUIZ] != []:
                                    quizDictList[quizDictIndex] = updated_quizDict
                                    tData[TEACHER] = quizDictList
                                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                    mb.showinfo("QUIZ STATUS:","Your quiz has now been Published.")                                                     
                                    backOut()

                                elif QUIZ not in qcaData or qcaData[QUIZ] == []:
                                    updated_quizDict["D/P"] = "Draft"
                                    quizDictList[quizDictIndex] = updated_quizDict
                                    tData[TEACHER] = quizDictList
                                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                    mb.showerror(
                                        "QUIZ STATUS:",
                                        "Your quiz cannot be published as the QCAs for this quiz has not be set-up.")                                                     

                                    backOut()
                        else:
                            backOut()

                # If changes made to the Topic, and the (newName==oldName, newTopic!=oldTopic)
                elif NewName == OldName and NewTopic != OldTopic:
                    quizTopic_withNewQuiz = []
                    for quizDict in quizDictList:
                        if quizDict["Quiz Name"] == NewName:
                            quizTopic_withNewQuiz.append(quizDict["Quiz Topic"])

                    # If newTopic already exists
                    if NewTopic in quizTopic_withNewQuiz:
                        mb.showerror("Error", "A quiz of this Name, under this Topic, already exists. Try again.")
                    else:
                        quizDictList[quizDictIndex] = updated_quizDict
                        tData[TEACHER] = quizDictList
                        writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)
                        mb.showinfo("Successful ","Quiz Topic has been updated.")      

                        if NewDP != OldDP:
                            if NewDP == "Draft":
                                quizDictList[quizDictIndex] = updated_quizDict
                                tData[TEACHER] = quizDictList
                                writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                mb.showinfo("QUIZ STATUS:","Your quiz has now been Drafted.")                                                     
                                backOut()
                    
                            
                            elif NewDP == "Published":
                                QUIZ = f'{NewName}:{ID}'
                                qcaData = loadJSON(QCA_DATA_FILENAME)

                                if QUIZ in qcaData and qcaData[QUIZ] != []:
                                    quizDictList[quizDictIndex] = updated_quizDict
                                    tData[TEACHER] = quizDictList
                                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                    mb.showinfo("QUIZ STATUS:","Your quiz has now been Published.")                                                     
                                    backOut()

                                elif QUIZ not in qcaData or qcaData[QUIZ] == []:
                                    mb.showerror(
                                        "QUIZ STATUS:",
                                        "Your quiz cannot be published as the QCAs for this quiz has not be set-up.")                                                     

                                    updated_quizDict["D/P"] = "Draft"
                                    quizDictList[quizDictIndex] = updated_quizDict
                                    tData[TEACHER] = quizDictList
                                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                    backOut()
                        else:
                            backOut()
                
                # If changes made to the Topic and the Name
                elif NewName != OldName and NewTopic != OldTopic:

                    quizTopic_withNewQuiz = []
                    for quizDict in quizDictList:
                        if quizDict["Quiz Name"] == NewName:
                            quizTopic_withNewQuiz.append(quizDict["Quiz Topic"])

                    # If newTopic already exists
                    if NewTopic in quizTopic_withNewQuiz:
                        mb.showerror("Error", "A quiz of this Name, under this Topic, already exists. Try again.")
                    else:
                        quizDictList[quizDictIndex] = updated_quizDict
                        tData[TEACHER] = quizDictList
                        writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)
                        
                        oldQUIZ = f'{OldName}:{ID}'
                        newQUIZ = f'{NewName}:{ID}'

                        qcaData = loadJSON(QCA_DATA_FILENAME)
                        if oldQUIZ in qcaData:
                            qcaData[newQUIZ] = qcaData[oldQUIZ]
                            del qcaData[oldQUIZ]
                        writeJSON(qcaData, QCA_DATA_FILENAME)

                        mb.showinfo("Successful ","Quiz Topic and Quiz Name has been updated.")      

                        if NewDP != OldDP:
                            if NewDP == "Draft":
                                quizDictList[quizDictIndex] = updated_quizDict
                                tData[TEACHER] = quizDictList
                                writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                mb.showinfo("QUIZ STATUS:","Your quiz has now been Drafted.")                                                     
                                backOut()
                    
                            
                            elif NewDP == "Published":
                                QUIZ = f'{NewName}:{ID}'
                                qcaData = loadJSON(QCA_DATA_FILENAME)

                                if QUIZ in qcaData and qcaData[QUIZ] != []:
                                    quizDictList[quizDictIndex] = updated_quizDict
                                    tData[TEACHER] = quizDictList
                                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                    mb.showinfo("QUIZ STATUS:","Your quiz has now been Published.")                                                     
                                    backOut()

                                elif QUIZ not in qcaData or qcaData[QUIZ] == []:
                                    mb.showerror(
                                        "QUIZ STATUS:",
                                        "Your quiz cannot be published as the QCAs for this quiz has not be set-up.")                                                     

                                    updated_quizDict["D/P"] = "Draft"
                                    quizDictList[quizDictIndex] = updated_quizDict
                                    tData[TEACHER] = quizDictList
                                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                    backOut()
                        else:
                            backOut()

                else:
                    quizDictList[quizDictIndex] = updated_quizDict
                    tData[TEACHER] = quizDictList
                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)
                    mb.showinfo("Successful ","Quiz info has been updated.")                                                     
                    backOut()


        type_label = tk.Label(l_foreground,text="Quiz Type :",bg="white", font=("calibre",16))
        type_label.place(relx=0.17,rely=0.57)       

        update_btn = tk.Button(l_foreground, font="calibre 12",text="Update", padx=5, pady=5, width=5, command=update, bg = "#33B5E5")
        update_btn.place(relx=0.60,rely=0.75)
        update_btn.configure(width=15, height=1, activebackground = "#2a94bc")

        cancel_btn = tk.Button(l_foreground,text='Cancel',font="calibre 12",padx=5, pady=5, command=backOut, bg="gray60", fg='black')
        cancel_btn.configure(width=15, height=1, activebackground = "gray",)
        cancel_btn.place(relx=0.17,rely=0.75)


    # when new button is clicked
    else:
        title = tk.Label(l_foreground, text= "New Quiz", fg="black", bg="white", font="Calibri 38")
        title.place(x=310, y=70, anchor="center")

        tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
        quizDictList = tData[TEACHER]

        topic_label = tk.Label(l_foreground,text="Quiz Topic :",bg="white", font=("calibre",16))
        topic_label.place(relx=0.17,rely=0.32)
        topic_entry = tk.Entry(l_foreground,width=28,bd=5,relief=tk.RIDGE, font=("calibre",13),justify=tk.CENTER)
        topic_entry.place(relx=0.37,rely=0.32)

        name_label = tk.Label(l_foreground,text="Quiz Name :",fg="black",bg="white", font=("calibre",16))
        name_label.place(relx=0.17,rely=0.44)
        name_entry = tk.Entry(l_foreground,width=28,bd=5,relief=tk.RIDGE,font=("calibre",13),justify=tk.CENTER)
        name_entry.place(relx=0.37,rely=0.44)


        ## Radiobutton ##
        rad_value = tk.IntVar()
        rad_value.set(0)
        options = {0: "Draft", 1: "Published" }

        draft_entry = tk.Radiobutton(l_foreground, text=options[0], font=("calibre",14,),variable=rad_value,value=1,bg="white")

        publish_entry = tk.Radiobutton(l_foreground, text=options[1], font=("calibre",14), variable=rad_value,value=2 ,bg="white")
        draft_entry.place(relx=0.38,rely=0.58)
        publish_entry.place(relx=0.55,rely=0.58)

        publish_entry.configure(state = tk.DISABLED)
        
        ## Get value from Radiobutton (Draft/ Published) ##
        def dpValue():
            D_P =str(rad_value.get())

            if  D_P == "1":
                return ("Draft")
            elif D_P == "2":
                return ("Published")

        # unique ID generator #
        def idNum(size):
            idNum ="".join([random.choice(string.digits)
                            for num in range(size)])
            return idNum

        def backOut():
            rootFrame.destroy()

            TEACHER = username
            tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
            quizDictList = tData[TEACHER]

            tData_lst = []
            for quizDict in quizDictList:
                quizName = quizDict["Quiz Name"]
                quizID = quizDict["ID"]
                quizStatus = quizDict["D/P"]

                sub_tData_lst = [f'{quizName}:{quizID}', quizStatus, ""]
                tData_lst.append(sub_tData_lst)
                
            DATA_LST = tData_lst
            if DATA_LST == []:
                DATA_LST = [[]]

            mainPage.teacherPage(root, TEACHER, DATA_LST)

        def new(): 
            # Get value from entry & radiobutton #
            NewName = name_entry.get()
            NewTopic = topic_entry.get()
            NewDP = dpValue()
            ID = idNum(5)
            # Check if user enters all the required fields #
            if NewName == "" or NewTopic == "" or NewDP == None:
                mb.showerror("Error", "Please FILL IN the required fields")

            else:
                new_quizDict = {
                    "Quiz Topic": NewTopic,
                    "Quiz Name": NewName,
                    "ID": ID,
                    "D/P": NewDP
                    }

                tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
                quizDictList = tData[TEACHER]

                if quizDictList == []:
                    quizDictList.append(new_quizDict)
                    tData[TEACHER] = quizDictList
                    writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)
                    mb.showinfo("Successful ","Please take note of your quiz ID : " +ID)                                                     
                    backOut()
                else:
                    # get quizzes under this topic
                    quizName_inTopic = []
                    for quizDict in quizDictList:
                        if quizDict["Quiz Topic"] == NewTopic:
                            quizName_inTopic.append(quizDict["Quiz Name"])


                    if NewName in quizName_inTopic:
                        mb.showerror("Error", "A quiz of this Name, under this Topic, already exists. Try again.")
                        quizName_inTopic.clear()
                    
                    else:
                        quizDictList.append(new_quizDict)
                        tData[TEACHER] = quizDictList
                        writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)
                        mb.showinfo("Successful ","Please take note of your quiz ID : " +ID)                                                     
                        backOut()

        # clearEntry()
        type_label = tk.Label(l_foreground,text="Quiz Type :",bg="white", font=("calibre",16))
        type_label.place(relx=0.17,rely=0.57)       

        create_btn = tk.Button(l_foreground, font="calibre 12",text="Create", padx=5, pady=5, width=5, command=new, bg = "#33B5E5")
        create_btn.place(relx=0.60,rely=0.75)
        create_btn.configure(width=15, height=1, activebackground = "#2a94bc")

        cancel_btn = tk.Button(l_foreground,text='Cancel',font="calibre 12",padx=5, pady=5, command=backOut, bg="gray60", fg='black')
        cancel_btn.configure(width=15, height=1, activebackground = "gray",)
        cancel_btn.place(relx=0.17,rely=0.75)