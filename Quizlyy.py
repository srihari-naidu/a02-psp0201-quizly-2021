#----------------------------------------------------------------------------------------------------#

############# imports #############
import os
import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from tkinter.ttk import Progressbar

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
ACC_DATA_FILENAME = 'acc-info.json'
if not(os.path.exists(ACC_DATA_FILENAME)) or \
    (os.stat(ACC_DATA_FILENAME).st_size == 0):
    writeJSON([], ACC_DATA_FILENAME)
    

TEACHER_QUIZ_INFO_FILENAME = 'teacher-quiz-info.json'
if not(os.path.exists(TEACHER_QUIZ_INFO_FILENAME)) or \
    (os.stat(TEACHER_QUIZ_INFO_FILENAME).st_size == 0):
    writeJSON({}, TEACHER_QUIZ_INFO_FILENAME)


STUDENT_QUIZ_INFO_FILENAME = 'student-quiz-info.json'
if not(os.path.exists(STUDENT_QUIZ_INFO_FILENAME)) or \
    (os.stat(STUDENT_QUIZ_INFO_FILENAME).st_size == 0):
    writeJSON({}, STUDENT_QUIZ_INFO_FILENAME)


QCA_DATA_FILE = 'quiz-qca-data.json'
if not(os.path.exists(QCA_DATA_FILE)) or \
    (os.stat(QCA_DATA_FILE).st_size == 0):
    writeJSON({}, QCA_DATA_FILE)
################################################################################

#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#

def login(root):
    global c_background

    root.title('Welcome to Quizlyy')

    c_background = tk.Canvas(root, bg="Cornflower Blue", width=800, height=500, highlightthickness=0)
    c_background.grid(sticky="NSEW")

    global l_foreground
    l_foreground = tk.Frame(c_background, bg = "white")
    l_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

    title = tk.Label(l_foreground, text="Login To Your Account", fg="black", bg="white", font="Calibri 38")
    title.place(relx=0.12,rely=0.1)

    username = tk.Label(l_foreground, text="Username", fg="black", bg="white", font=("calibre", 12))
    username.place(relx=0.2,rely=0.39)
    u_input = tk.Entry(l_foreground, fg="black", bg="light grey", width="42")
    u_input.place(relx=0.35,rely=0.4)
    u_input.focus()

    password = tk.Label(l_foreground, text="Password", fg="black", bg="white", font=("calibre", 12))
    password.place(relx=0.2,rely=0.49)
    p_input = tk.Entry(l_foreground, show="*", fg="black", bg="light grey", width="42")
    p_input.place(relx=0.35,rely=0.5)

    def noaccount_btn_clicked():
        l_foreground.destroy()
        createaccount(root)

    def login_btn_clicked():
        u_name = u_input.get()
        p_name = p_input.get()
        if u_name == '' and p_name == '':
            mb.showinfo('Login Error', f'Please enter your username and password.')
        elif u_name == '':
            mb.showinfo('Login Error', f'Please enter your username.')
        elif p_name == '':
            mb.showinfo('Login Error', f'Please enter your password.')
        else:
            accData = loadJSON(ACC_DATA_FILENAME)
            
            userList = []
            for accDict in accData:
                userList.append(accDict["username"])

            if u_name in userList:
                accData = loadJSON(ACC_DATA_FILENAME)
                for accDict in accData:
                    if accDict["username"] == u_name:
                        accNamePass = [accDict["username"], accDict["password"]]
                        inputNamePass = [u_name, p_name]

                        if accNamePass == inputNamePass:

                            def teacher_or_student():
                                if accDict["user type"] == "Teacher":
                                    TEACHER = u_name
                                    tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)

                                    if TEACHER not in tData:
                                        tData[TEACHER] = []
                                        writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                        DATA_LST = [[]]
                                        mainPage.teacherPage(root, TEACHER, DATA_LST)
                                    
                                    elif TEACHER in tData:
                                        if tData[TEACHER] == []:
                                            DATA_LST = [[]]
                                            mainPage.teacherPage(root, TEACHER, DATA_LST)
                                        else:
                                            tData_lst = []

                                            quizDictList = tData[TEACHER]
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


                                elif accDict["user type"] == "Student":
                                    STUDENT = u_name
                                    sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)

                                    if STUDENT not in sData:
                                        # getAllQuizData
                                        sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
                                        tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
                                        sData_lst = []
                                        sDictList = []
                                        for TEACHER in tData:
                                            quizDictList = tData[TEACHER]
                                            
                                            for quizDict in quizDictList:
                                                quizTopic = quizDict["Quiz Topic"]
                                                quizName = quizDict["Quiz Name"]
                                                quizID = quizDict["ID"]
                                                quizStatus = quizDict["D/P"]

                                                if quizStatus == "Published":
                                                    s_quizName = f'{quizName}:{quizID}'
                                                    s_quizScore = ""
                                                    s_quizTaken = False

                                                    sDict = {
                                                        "Quiz Topic" : quizTopic,
                                                        "Quiz Name" : quizName,
                                                        "ID" : quizID,
                                                        "Quiz Score" : s_quizScore,
                                                        "Taken" : s_quizTaken
                                                    }
                                                    
                                                    sub_sData_lst = [s_quizName, s_quizScore, s_quizTaken]
                                                    sData_lst.append(sub_sData_lst)
                                                    sDictList.append(sDict)

                                        sData[STUDENT] = sDictList
                                        writeJSON(sData, STUDENT_QUIZ_INFO_FILENAME)

                                        DATA_LST = sData_lst
                                        if DATA_LST == []:
                                            DATA_LST = [[]]
                                    
                                        mainPage.studentPage(root, STUDENT, DATA_LST)
                                    
                                    elif STUDENT in sData:
                                        sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
                                        tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
                                        # else:
                                        sDictList = sData[STUDENT]

                                        fresh_sDictList = []
                                        tocheck_fresh_sDictList = []
                                        for TEACHER in tData:
                                            quizDictList = tData[TEACHER]
                                            
                                            for quizDict in quizDictList:
                                                quizTopic = quizDict["Quiz Topic"]
                                                quizName = quizDict["Quiz Name"]
                                                quizID = quizDict["ID"]
                                                quizStatus = quizDict["D/P"]

                                                s_quizName = f'{quizName}:{quizID}'
                                                s_quizScore = ""
                                                s_quizTaken = False

                                                sDict = {
                                                    "Quiz Topic" : quizTopic,
                                                    "Quiz Name" : quizName,
                                                    "ID" : quizID,
                                                    "Quiz Score" : s_quizScore,
                                                    "Taken" : s_quizTaken
                                                }

                                                tocheck_sDict = {
                                                    "Quiz Topic" : quizTopic,
                                                    "Quiz Name" : quizName,
                                                    "ID" : quizID,
                                                    "D/P" : quizStatus
                                                }
                                                
                                                sDictID_list = [sDict["ID"] for sDict in sDictList]

                                                if quizStatus == "Published":
                                                    if quizID not in sDictID_list:
                                                        sDictList.append(sDict)
                                                    fresh_sDictList.append(sDict) # clean list
                                                tocheck_fresh_sDictList.append(tocheck_sDict) # checker list
                                        
                                        tocheck_fresh_sDictID_list = [fresh_sDict["ID"] for fresh_sDict in tocheck_fresh_sDictList]
                    
                                        if sDictList != []:
                                            # update old sData to new sData
                                            for sDict in sDictList:
                                                sDict_Index = sDictList.index(sDict)
                                                sDict_ID = sDict["ID"]
                                                if sDict_ID in tocheck_fresh_sDictID_list:
                                                    for fresh_sDict in tocheck_fresh_sDictList:
                                                        if fresh_sDict["ID"] == sDict_ID:
                                                            if sDict["Quiz Topic"] != fresh_sDict["Quiz Topic"]:
                                                                sDict["Quiz Topic"] = fresh_sDict["Quiz Topic"]
                                                            if sDict["Quiz Name"] != fresh_sDict["Quiz Name"]:
                                                                sDict["Quiz Name"] = fresh_sDict["Quiz Name"]
                                                            if fresh_sDict["D/P"] == "Draft":
                                                                del sDictList[sDict_Index]
                                                                 
                                            sData[STUDENT] = sDictList
                                            writeJSON(sData, STUDENT_QUIZ_INFO_FILENAME)

                                        else:
                                            sData[STUDENT] = fresh_sDictList
                                            writeJSON(sData, STUDENT_QUIZ_INFO_FILENAME)

                                        
                                        # get sData_lst
                                        sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
                                        sDictList = sData[STUDENT]

                                        sData_lst = []
                                        for sDict in sDictList:
                                            quizName = sDict["Quiz Name"]
                                            quizID = sDict["ID"]
                                            
                                            s_quizName = f'{quizName}:{quizID}'
                                            s_quizScore = sDict["Quiz Score"]
                                            s_quizTaken = sDict["Taken"]

                                            sub_sData_lst = [s_quizName, s_quizScore, s_quizTaken]
                                            sData_lst.append(sub_sData_lst)
                                        
                                        DATA_LST = sData_lst
                                        if DATA_LST == []:
                                            DATA_LST = [[]]
                                    
                                        mainPage.studentPage(root, STUDENT, DATA_LST)

                            c_background.destroy()
                            l_foreground.destroy()
                            teacher_or_student()
                            break

                        elif accNamePass != inputNamePass:
                            mb.showinfo('Login Error', f'Your username and password does not match.')
            else:
                mb.showinfo('Login Error', f'Your username and password does not exist.')


    
    def deletepage():
        u_name = u_input.get()
        p_name = p_input.get()
        l_foreground.destroy()

        root.title('Confirmation Of Account Deletion')

        d_foreground = tk.Frame(c_background, bg = "white")
        d_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

        title = tk.Label(d_foreground, text="Delete Your Account", fg="black", bg="white", font="calibri 40")
        title.place(relx=0.13,rely=0.1)

        txt1 = tk.Label(d_foreground, text="By permanently deleting your account, all your information will be erased", fg="black", bg="white", font=("calibre", 12))
        txt2 = tk.Label(d_foreground, text=" from our system. Your username and password can no longer be used.", fg="black", bg="white", font=("calibre", 12))
        txt3 = tk.Label(d_foreground, text ='PLEASE NOTE THAT THIS ACTION CANNOT BE UNDONE!', fg="red", bg="white", font=("calibre", 12))
        txt1.place(relx=0.10,rely=0.353)
        txt2.place(relx=0.094,rely=0.411)
        txt3.place(relx=0.153, rely=0.48)


        def remove_account():
            result = mb.askyesno('Confirmation','Are you sure you want to continue with deleting your account?', icon='warning', default='no' )
            if result:
                accData = loadJSON(ACC_DATA_FILENAME)
                for accDict in accData:
                    for accDict in accData:
                        if accDict["username"] == u_name and accDict["password"] == p_name:
                            accDictIndex = accData.index(accDict)
                            if accDict["user type"] == "Teacher":
                                TEACHER = u_name
                                tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
                                sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
                                tDictList = tData[TEACHER]

                                quizList = []
                                for quizDict in tDictList:
                                    quizName = quizDict["Quiz Name"]
                                    quizID = quizDict["ID"]

                                    for STUDENT in sData:
                                        for quizDict in sData[STUDENT]:
                                            quizDictIndex = sData[STUDENT].index(quizDict)
                                            if quizDict["Quiz Name"] == quizName and quizDict["ID"] == quizID:
                                                del sData[STUDENT][quizDictIndex]
                                                writeJSON(sData, STUDENT_QUIZ_INFO_FILENAME)


                                    QUIZ = f'{quizName}:{quizID}'
                                    quizList.append(QUIZ)

                                del tData[TEACHER]
                                writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)

                                
                                qcaData = loadJSON(QCA_DATA_FILE)
                                for QUIZ in quizList:
                                    if QUIZ in qcaData:
                                        del qcaData[QUIZ]
                                writeJSON(qcaData, QCA_DATA_FILE)

                                del accData[accDictIndex]
                                writeJSON(accData, ACC_DATA_FILENAME)

                            elif accDict["user type"] == "Student":
                                STUDENT = u_name
                                sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
                                if STUDENT in sData:
                                    del sData[STUDENT]
                                    writeJSON(sData, STUDENT_QUIZ_INFO_FILENAME)

                                del accData[accDictIndex]
                                writeJSON(accData, ACC_DATA_FILENAME)




                mb.showinfo('Success', f'Your account has been permanently deleted.')
                d_foreground.destroy()
                c_background.destroy()
                login(root)
            else:
                pass
        
        def cancel():
            d_foreground.destroy()
            c_background.destroy()
            login(root)

        deleteaccount_btn = tk.Button(d_foreground,text='Delete',padx=5, pady=5, command=remove_account, bg="red", fg='black')
        deleteaccount_btn.configure(width=19, height=1, activebackground = "red3")
        deleteaccount_btn.place(relx=0.55,rely=0.65)

        cancel_btn = tk.Button(d_foreground,text='Cancel',padx=5, pady=5, command=cancel, bg="gray60", fg='black')
        cancel_btn.configure(width=19, height=1, activebackground = "gray",)
        cancel_btn.place(relx=0.19,rely=0.65)


    def dlt():
        u_name = u_input.get()
        p_name = p_input.get()
        if u_name == '' and p_name == '':
            mb.showinfo('Error', f'Please enter your username and password.')
        elif u_name == '':
            mb.showinfo('Error', f'Please enter your username.')
        elif p_name == '':
            mb.showinfo('Error', f'Please enter your password.')
        else:
            accData = loadJSON(ACC_DATA_FILENAME)
            
            userList = []
            for accDict in accData:
                userList.append(accDict["username"])

            if u_name in userList:
                accData = loadJSON(ACC_DATA_FILENAME)
                for accDict in accData:
                    if accDict["username"] == u_name:
                        accNamePass = [accDict["username"], accDict["password"]]
                        inputNamePass = [u_name, p_name]

                        if accNamePass == inputNamePass:
                            deletepage()
                            break
                        elif accNamePass != inputNamePass:
                            mb.showinfo('Account Error', f'Your username and password does not match.')
                            break
            else:
                mb.showinfo('Account Error', f'Your username and password does not exist.')

    def fp():
        l_foreground.destroy()
        root.title('Forgot Password')


        fp_foreground = tk.Frame(c_background, bg = "white")
        fp_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)
        style = ttk.Style()
        style.configure("black.Horizontal.TProgressbar", background='#153060')

        bar = Progressbar(fp_foreground, length=650, style='black.Horizontal.TProgressbar')
        bar['value'] = 33
        bar.grid(column=0, row=0)

        title1 = tk.Label(fp_foreground, text="Please Enter", fg="black", bg="white", font="calibri 40")
        title2 = tk.Label(fp_foreground, text="Your Username", fg="black", bg="white", font="calibri 40")
        title1.place(relx=0.29,rely=0.13)
        title2.place(relx=0.23,rely=0.28)


        usernameinput = tk.Entry(fp_foreground, font="Calibri 13", fg="black", bg="light grey", width="35")
        usernameinput.place(relx=0.25,rely=0.57)
        usernameinput.focus()

        def page2():
            username = usernameinput.get()
            with open(ACC_DATA_FILENAME) as f:
                data = json.loads(f.read())
                for account in data:
                    if username == '':
                        mb.showinfo('Error', f'Please enter your username.')
                        break
                    elif account["username"] == username :
                        fp_foreground.destroy()
                        root.title('Forgot Password')

                        fp2_foreground = tk.Frame(c_background, bg = "white")
                        fp2_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)
                        style = ttk.Style()
                        style.configure("black.Horizontal.TProgressbar", background='#153060')

                        bar = Progressbar(fp2_foreground, length=650, style='black.Horizontal.TProgressbar')
                        bar['value'] = 66
                        bar.grid(column=0, row=0)

                        title1 = tk.Label(fp2_foreground, text="Please Choose", fg="black", bg="white", font="calibri 40")
                        title2 = tk.Label(fp2_foreground, text="Your User Type", fg="black", bg="white", font="calibri 40")
                        title1.place(relx=0.25,rely=0.13)
                        title2.place(relx=0.23,rely=0.28)

                        bigfont = ("Calibri","13")
                        fp2_foreground.option_add("*TCombobox*Listbox*Font", bigfont)
                        style = ttk.Style()
                        style.configure('W.TCombobox',arrowsize = 13)
                        usertype = ttk.Combobox(fp2_foreground, state="readonly", values=("Teacher","Student"), width=30, font='Calibri 13',style='W.TCombobox')
                        usertype.place(relx=0.27,rely=0.55) 

                        def page3():
                            user_type = usertype.get()
                            with open(ACC_DATA_FILENAME) as f:
                                            data = json.loads(f.read())
                                            for account in data:
                                                if user_type == '':
                                                    mb.showinfo('Error', f'Please choose your user type.')
                                                    break
                                                elif account['username'] == username and account['user type'] == user_type:
                                                    fp2_foreground.destroy()
                                                    root.title('Reset Password')

                                                    fp3_foreground = tk.Frame(c_background, bg = "white")
                                                    fp3_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)
                                                    style = ttk.Style()
                                                    style.configure("black.Horizontal.TProgressbar", background='#153060')

                                                    bar = Progressbar(fp3_foreground, length=650, style='black.Horizontal.TProgressbar')
                                                    bar['value'] = 100
                                                    bar.grid(column=0, row=0)

                                                    title1 = tk.Label(fp3_foreground, text="Please Set A", fg="black", bg="white", font="calibri 40")
                                                    title2 = tk.Label(fp3_foreground, text="New Password", fg="black", bg="white", font="calibri 40")
                                                    title1.place(relx=0.28,rely=0.11)
                                                    title2.place(relx=0.24,rely=0.26)

                                                    new = tk.Label(fp3_foreground, text="Password", fg="black", bg="white", font=("calibre", 13))
                                                    new.place(relx=0.23,rely=0.519)
                                                    new_pw = tk.Entry(fp3_foreground, show="*", fg="black", bg="light grey", width="32", font="Calibri 13")
                                                    new_pw.place(relx=0.40,rely=0.51)
                                                    new_pw.focus()


                                                    confirm = tk.Label(fp3_foreground, text="Confirm Password", fg="black", bg="white", font=("calibre", 13))
                                                    confirm.place(relx=0.13,rely=0.619)
                                                    confirm_pw = tk.Entry(fp3_foreground, show="*", fg="black", bg="light grey", width="32", font="Calibri 13")
                                                    confirm_pw.place(relx=0.40,rely=0.61)

                                                    def returntologin(root):
                                                        fp3_foreground.destroy()  
                                                        c_background.destroy()
                                                        login(root) 

                                                    def password_check():
                                                        newpassword = new_pw.get()
                                                        confirmpassword = confirm_pw.get()
                                                        if newpassword == '' and confirmpassword == '':
                                                            mb.showinfo('Reset Password Failure', f'Please enter your new password.')
                                                        elif newpassword == '':
                                                            mb.showinfo('Reset Password Failure', f'Please enter your new password.')
                                                        elif confirmpassword == '':
                                                            mb.showinfo('Reset Password Failure', f'Please confirm your password.')
                                                        elif newpassword == confirmpassword:
                                                            mb.showinfo('Reset Password Success', f'Your password has been reset successfully. Please proceed to login.')
                                                            
                                                            with open(ACC_DATA_FILENAME, 'r') as f:
                                                                data = json.load(f)
        
                                                            for i in range(len(data)):
                                                                if data[i]["username"] == username and data[i]["user type"] == user_type:
                                                                    data[i]["password"]= newpassword
                                                                    break  
                                                    
                                                            with open(ACC_DATA_FILENAME, 'w') as f:
                                                                json.dump(data, f, indent=4)

                                                            returntologin(root)
                                                        else:
                                                           mb.showinfo('Reset Password Failure', f'Please make sure to type the same new password.')


                                                    confirm_btn = tk.Button(fp3_foreground, font="Calibri 12",text='Confirm', padx=5, pady=5, width=5, command=password_check, bg="#33B5E5")
                                                    confirm_btn.place(relx=0.55,rely=0.78)
                                                    confirm_btn.configure(width=15, height=1, activebackground = "#2a94bc")

                                                    def cancelbtn_func():
                                                        returntologin(root)

                                                    cancel_btn = tk.Button(fp3_foreground, font="Calibri 12",text='Cancel', padx=5, pady=5, width=5, command=cancelbtn_func, bg="gray60")
                                                    cancel_btn.place(relx=0.22,rely=0.78)
                                                    cancel_btn.configure(width=15, height=1, activebackground = "gray")

                                                    break
                                            else:
                                                mb.showinfo('Error', f'Your username and user type does not match.')
                                                fp()  
                        next_btn = tk.Button(fp2_foreground, font="Calibri 12",text='Next', padx=5, pady=5, width=5, command=page3, bg="#33B5E5")
                        next_btn.place(relx=0.40,rely=0.78)
                        next_btn.configure(width=15, height=1, activebackground = "#2a94bc")
                        break
                else:
                    mb.showinfo('Error', f'Your username does not exist.') 
            
        next_btn = tk.Button(fp_foreground, font="Calibri 12",text='Next', command=page2, padx=5, pady=5, width=5, bg = "#33B5E5")
        next_btn.place(relx=0.40,rely=0.75)
        next_btn.configure(width=15, height=1, activebackground = "#2a94bc")


    login_btn = tk.Button(l_foreground, font="Calibri 10",text="Log in", padx=5, pady=5, width=5, command = login_btn_clicked, bg = "#33B5E5")
    login_btn.place(relx=0.55,rely=0.65)
    login_btn.configure(width=15, height=1, activebackground = "#2a94bc")

    delete_btn = tk.Button(l_foreground,font="Calibri 10",text='Delete Account',padx=5, pady=5, command=dlt, bg="firebrick1",fg='black')
    delete_btn.configure(width=15, height=1,activebackground="#e30000")
    delete_btn.place(relx=0.25,rely=0.65)

    noaccount_btn = tk.Button(l_foreground,text='Don\'t Have An Account Yet?', padx=5, pady=5, command=noaccount_btn_clicked, bg="white",fg='blue')
    noaccount_btn.configure(width=20, height=1, activebackground = "#33B5E5", relief=tk.FLAT)
    noaccount_btn.place(relx=0.38,rely=0.8)

    forgotpassword_btn =  tk.Button(l_foreground,text='Forgot Password?',padx=5, pady=5, command=fp, bg="white",fg='blue')
    forgotpassword_btn.configure(width=20, height=1, activebackground = "#33B5E5", relief=tk.FLAT)
    forgotpassword_btn.place(relx=0.38,rely=0.87)
    return u_input.get()

def createaccount(root):
    l_foreground.destroy()
    root.title('Don\'t Have An Account Yet?')

    global c_foreground
    c_foreground = tk.Frame(c_background, bg = "white")
    c_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

    title = tk.Label(c_foreground, text="Create Your Account", fg="black", bg="white", font="calibri 40")
    title.place(relx=0.13,rely=0.1)

    username = tk.Label(c_foreground, text="Username", fg="black", bg="white", font=("calibre", 12))
    username.place(relx=0.21,rely=0.39)
    u_input = tk.Entry(c_foreground, fg="black", bg="light grey", width="42")
    u_input.place(relx=0.36,rely=0.4)
    u_input.focus()


    password = tk.Label(c_foreground, text="Password", fg="black", bg="white", font=("calibre", 12))
    password.place(relx=0.21,rely=0.49)
    p_input = tk.Entry(c_foreground, show="*", fg="black", bg="light grey", width="42")
    p_input.place(relx=0.36,rely=0.5)

    usertype = tk.Label(c_foreground, text="User Type", fg="black", bg="white", font=("calibre", 12))
    usertype.place(relx=0.21,rely=0.59)
    user_choice = ttk.Combobox(c_foreground, state="readonly", values=("Teacher","Student"))
    user_choice.place(relx=0.36,rely=0.6) 

    def register_btn_clicked(): 
        u_name = u_input.get()
        p_word = p_input.get()  
        u_type = user_choice.get()

        acc_dic = {'username': u_name, 'password': p_word, 'user type': u_type}
        l = []

        for info in acc_dic:
            if acc_dic[info] == "":
                l.append(info)
            s = ''
            for word in l:
                if word == l[-1] :
                    s += word + '.' 
                elif word == l[-2]:
                    s = s + word + ' and '
                else:
                    s = s + word + ', ' 
        
        # if there are fields that user haven't fill in
        if l != []:
            mb.showinfo('Registration error', f'Please enter your {s}')

        else:
            # check whether username is unique or has been taken
            with open(ACC_DATA_FILENAME) as f:
                data = json.loads(f.read())
                result = False
                for item in data:
                    if item["username"] == u_name:
                        result = True
            if result:
                mb.showinfo('Registration error', f'This username has been taken. Please enter another username.')
            else:
                account_save(ACC_DATA_FILENAME, acc_dic)
        
    def account_save(filename, acc_dic):
        with open(filename, 'r+') as f:
            data = json.load(f)
            data.append(acc_dic)
            # set back to initial point to avoid duplicate
            f.seek(0)
            json.dump(data, f, indent=4)
        mb.showinfo('Success', f'Registration is successful.')
        c_background.destroy()
        c_foreground.destroy()
        login(root)

    def loginfromregister():
        c_background.destroy()
        c_foreground.destroy()
        login(root)

    register_btn = tk.Button(c_foreground, text="Register", padx=5, pady=5, width=5, command=register_btn_clicked, bg = "#33B5E5")
    register_btn.place(relx=0.4,rely=0.8)
    register_btn.configure(width = 15,height=1, activebackground = "#2a94bc")

    login_btn = tk.Button(c_foreground,text='Already Have An Account?', padx=5, pady=5, command=loginfromregister, bg="white",fg='blue')
    login_btn.configure(width=18, height=1, activebackground="#33B5E5", relief=tk.FLAT)
    login_btn.place(relx=0.38, rely=0.9)



#----------------------------------------------------------------------------------------------------#
if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("800x500")
    root.resizable(0,0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0,weight=1)
    #------------------------------------------------------------------------------------------------#

    login(root)

    #------------------------------------------------------------------------------------------------#
    root.mainloop()

#----------------------------------------------------------------------------------------------------#