#----------------------------------------------------------------------------------------------------#

############ imports ############
import os
import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

import copy

import Quizlyy
import quizQCA
import quizRun
import quizEdit
#################################

#----------------------------------------------------------------------------------------------------#

######### colours #########
BLUEV1 = "Cornflower Blue"
BLUEV2 = "#557FCC"

WHITEV1 = "#F9F9F9"
WHITEV2 = "#E7E7E7"
WHITEV3 = "#D8D8D8"

GRAY = "#717D7F"
###########################

#----------------------------------------------------------------------------------------------------#

#################### font-styles ####################
TTL = ("Bahnschrift Bold SemiCondensed", "28")
HDR = ("Bahnschrift Bold", "16")
CONT = ("Bahnschrift", "14")
BTN = ("Bahnschrift SemiBold", "12")
TAG = ("Bahnschrift SemiCondensed", "14")
#####################################################

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
TEACHER_QUIZ_INFO_FILENAME = 'teacher-quiz-info.json'
STUDENT_QUIZ_INFO_FILENAME = 'student-quiz-info.json'
QCA_DATA_FILE = 'quiz-qca-data.json'
################################################################################

#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#
  
class StudentTable:

    # Student's  View
    # |   Quiz   |  Score  |   Action   |
    # -----------------------------------
    # |  Quiz A  |   [ ]   |    [Run]   |
    # |  Quiz B  |   [ ]   |    [Run]   |
    # |  Quiz C  |   [ ]   |    [Run]   |
    
    def __init__(self, root, username, data):
        
        ############### master-config ###############
        # createMaster
        self.master = root
        self.master.title("Quizlyy Menu - Student")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)


        ############# pre-req #############
        self.noQuiz = False
        
        # getStudent
        self.student = username
        
        # getActualDataList
        self.sData_lst = data


        # getInitStudentDataList
        self.init_sData_lst = copy.deepcopy(self.sData_lst)
        if self.init_sData_lst == [[]]:
            self.noQuiz = True
        

        # init_sData_lst_mod
        if self.noQuiz == False:
            sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
            sDictList = sData[self.student]

            for x in range(len(self.init_sData_lst)):
                quizName, quizID = self.init_sData_lst[x][0].split(':')
                if sDictList[x]["Quiz Name"] == quizName and sDictList[x]["ID"] == quizID:
                    quizTopic = sDictList[x]["Quiz Topic"]
                    new_quizName = f'TOPIC: {quizTopic}\nNAME: {quizName}'
                    self.init_sData_lst[x][0] = new_quizName

        sHeader_lst = ["Quiz", "Score", "Action"]
        if self.init_sData_lst[0] != sHeader_lst:
            self.init_sData_lst.insert(0,sHeader_lst)


        # getStudentDataList
        self.modded_sData_lst = self.init_sData_lst

        # getStudentViewTotalRows
        sRows = len(self.modded_sData_lst)
        
        # getStudentViewTotalColumns
        sColumns = len(self.modded_sData_lst[0])


        ############################## title-config ##############################
        # createTitleFrame
        self.apexFrame = tk.Frame(self.master)
        self.apexFrame.grid(row=0, sticky="NSEW")
        self.apexFrame.grid_columnconfigure((0,1,2,3), weight=1)


        #createTitle
        self.lbl_title = tk.Label(
            self.apexFrame, 
            text = f"{self.student}'s Quizzes", 
            font=TTL, 
            fg=WHITEV1, bg=BLUEV1)

        self.lbl_title.grid(row=0, columnspan=4, ipady=18, sticky="EW")


        # createLogOutButton
        self.logOut_BTN = tk.Button(
                            self.apexFrame, 
                            text='L O G O U T', 
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV2, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV1,
                            command=self.logOut
                            )

        self.logOut_BTN.grid(row=0, column=3, padx=(0,20), pady=(28,0), sticky="NE")
        

        ############################## canvasFrame-config ##############################
        #createCanvasFrame
        self.canvasFrame = tk.Frame(self.master)
        self.canvasFrame.grid(row=1, column=0, pady=55, sticky="NSEW")
        self.canvasFrame.grid_rowconfigure(0, weight=1)
        self.canvasFrame.grid_columnconfigure(0,weight=1)
        

        ############################## tableCanvas-config ##############################
        #createTableCanvas
        self.tableCanvas = tk.Canvas(self.canvasFrame, highlightthickness=0)
        self.tableCanvas.grid(row=0, column=0, sticky="NSEW")


        ############################## SCRLBR-config ##############################
        #createSCRLBR
        self.vSCRLBR = tk.Scrollbar(
            self.canvasFrame, 
            orient="vertical", 
            command=self.tableCanvas.yview)

        self.vSCRLBR.grid(row=0, column=1, sticky="NS")
        self.tableCanvas.configure(yscrollcommand=self.vSCRLBR.set)


        ############################## tableFrame-config ##############################
        # createTableFrame
        self.tableFrame = tk.Frame(self.tableCanvas, bg='white')

        #createTableWindow
        self.tableCanvas.create_window((0,0), window=self.tableFrame, anchor="nw")

        self.tableFrame.bind(
            "<Configure>",
            lambda e: self.tableCanvas.configure(
                scrollregion=self.tableCanvas.bbox("all")
            )
        )

        # mouseScroll-config
        self.tableCanvas.bind_all(
            "<MouseWheel>", 
            lambda event: self.yview(
                'scroll', 
                int(-1*(event.delta/120)), 'units'
            )
        )

#----------------------------------------------------------------------------------------------------#

        # createTable
        for i in range(sRows):
            for j in range(sColumns):
                
                # Header Row
                if i == 0 and j < sColumns-2:
                    #createHeaderLabel
                    self.lbl = tk.Label(
                        self.tableFrame, 
                        text=self.modded_sData_lst[i][j],
                        width=25,
                        height=2, 
                        fg='white',
                        bg='cornflower blue',
                        font=HDR)

                    self.lbl.grid(row=i, column=j, pady=(0,2), sticky="NSEW")
                
                # Score Column Header
                if i == 0 and j == sColumns-2:
                    #createHeaderLabel
                    self.lbl = tk.Label(
                        self.tableFrame, 
                        text=self.modded_sData_lst[i][j],
                        height=2, 
                        width=19,
                        fg='white',
                        bg='cornflower blue',
                        font=HDR)

                    self.lbl.grid(row=i, column=j, pady=(0,2), sticky="NSEW")

                # Action Column Header
                elif i == 0 and j == sColumns-1:
                    #createHeaderLabel
                    self.lbl = tk.Label(
                        self.tableFrame, 
                        text=self.modded_sData_lst[i][j],
                        height=2, 
                        width=20,
                        fg='white',
                        bg='cornflower blue',
                        font=HDR)

                    self.lbl.grid(row=i, column=j, pady=(0,2), sticky="NSEW")

                if self.noQuiz == False:
                    # Content Rows
                    if i > 0 and j != sColumns-2:
                        #createContentLabel
                        self.lbl = tk.Label(
                            self.tableFrame, 
                            text=self.modded_sData_lst[i][j],
                            wraplength=200,
                            fg='black',
                            bg=WHITEV2,
                            font=CONT)
                        
                        self.lbl.grid(row=i, column=j, padx=2, pady=2, sticky="NSEW")
                        
                        if i == sRows-1:
                            self.lbl.grid(row=i, column=j, padx=2, pady=(2,4), sticky="NSEW")

                    # Score Content Row
                    if i > 0 and j == sColumns-2:
                        #createContentLabel
                        self.lbl = tk.Label(
                            self.tableFrame, 
                            text=self.modded_sData_lst[i][j],
                            wraplength=200,
                            fg='black',
                            bg=WHITEV2,
                            font=CONT)
                        
                        self.lbl.grid(row=i, column=j, padx=(2,4), pady=2, sticky="NSEW")
                        
                        if i == sRows-1:
                            self.lbl.grid(row=i, column=j, padx=(2,4), pady=(2,4), sticky="NSEW")

                    # Button Content Row
                    if i > 0 and j == sColumns-1:

                        #createButtonFrame
                        self.btn_frame = tk.Frame(self.tableFrame, bg="white")
                        self.btn_frame.grid(row=i, column=j, pady=2, sticky="NSEW")
                        
                        if i == sRows-1:
                            self.btn_frame.grid(row=i, column=j, pady=(2,4), sticky="NSEW")

                        #createTakeButton
                        self.take_BTN = tk.Button(
                            self.btn_frame, 
                            text="T A K E", 
                            fg="white", 
                            bg="#2b2b2b",   
                            font=BTN,
                            command=lambda row=i: self.takeQuiz(row))

                        #createReTakeButton
                        self.retake_BTN = tk.Button(
                            self.btn_frame, 
                            text="R E T A K E", 
                            fg="white", 
                            bg="#2b2b2b",   
                            font=BTN,
                            command=lambda row=i: self.takeQuiz(row))

                        if self.modded_sData_lst[i][j] == True:
                            self.retake_BTN.pack(fill="both",expand=True)
                        elif self.modded_sData_lst[i][j] == False:
                            self.take_BTN.pack(fill="both",expand=True)


                elif self.noQuiz == True:

                    #creatEmptyIntroLabel
                    self.lbl = tk.Label(
                        self.canvasFrame, 
                        text=f'Lay back, {self.student}. ;)',
                        font=HDR)

                    self.lbl.grid(row=1, columnspan=3, padx=2, pady=2, sticky="NSEW")

                    #creatEmptyLabel
                    self.lbl2 = tk.Label(
                        self.canvasFrame,
                        text="Your teachers have not published any quizzes, for you to do, yet.",
                        font=CONT)

                    self.lbl2.grid(row=2, columnspan=3, padx=2, pady=2, sticky="NSEW")

    #--------------------------------------- method-config ---------------------------------------#
    ################### refreshFrame ###################
    def refresh(self):
        self.apexFrame.destroy()
        self.canvasFrame.destroy()

        sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
        sDictList = sData[self.student]

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
                                        
        self.__init__(self.master, self.student, DATA_LST)
    ####################################################

    ############ runQuiz ############
    def takeQuiz(self, row):
        self.apexFrame.destroy()
        self.canvasFrame.destroy()
        QUIZ = self.sData_lst[row-1][0]
        quizRun.QuizRun(
            self.master, 
            QUIZ, 
            "student", 
            self.student
        )
    #################################

    ################ yview-Scroll ################
    # Checks if the content fits within the canvas
    def yview(self, *args):
        if self.tableCanvas.yview() == (0.0, 1.0):
            return
        self.tableCanvas.yview(*args)
    ##############################################
    
    ############ logOut ############
    def logOut(self):
        confirmation = mb.askyesno(
            'Logout Confirmation',
            'Are you sure you want to log out?', 
            icon='warning', 
            default='no' )
            
        if confirmation:
            self.apexFrame.destroy()
            self.canvasFrame.destroy()
            Quizlyy.login(self.master)
    ################################
    #------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------#

class TeacherTable:

    # Teacher's View
    # |   Quiz   |    Status   |        Action        |
    # -------------------------------------------------
    # |  Quiz A  |  Published  | [Edit] [View] [Del-] |
    # |  Quiz B  |  Published  | [Edit] [View] [Del-] |
    # |  Quiz C  |  Published  | [Edit] [View] [Del-] |
    
    def __init__(self, root, username, data):

        ############### master-config ###############
        # createMaster
        self.master = root
        self.master.title("Quizlyy Menu - Teacher")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)


        ############# pre-req #############
        self.noQuiz = False
        
        # getTeacher
        self.teacher = username
        
        # getActualDataList
        self.tData_lst = data


        # getInitTeacherDataList
        self.init_tData_lst = copy.deepcopy(self.tData_lst)
        if self.init_tData_lst == [[]]:
            self.noQuiz = True
        

        if self.noQuiz == False:
            # checks if the quiz can be viewable
            qcaData = loadJSON(QCA_DATA_FILE)

            for sub_tData_lst in self.init_tData_lst:
                quizName = sub_tData_lst[0]
                if quizName not in qcaData or qcaData[quizName] == []:
                    sub_tData_lst[2] = False
            

        # init_tData_lst_mod
            tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
            quizDictList = tData[self.teacher]

            for x in range(len(self.init_tData_lst)):
                quizName, quizID = self.init_tData_lst[x][0].split(':')
                if quizDictList[x]["Quiz Name"] == quizName and quizDictList[x]["ID"] == quizID:
                    quizTopic = quizDictList[x]["Quiz Topic"]
                    new_quizName = f'TOPIC: {quizTopic}\nNAME: {quizName}'
                    self.init_tData_lst[x][0] = new_quizName

        tHeader_lst = ["Quiz", "Status", "Action"]
        if self.init_tData_lst[0] != tHeader_lst:
            self.init_tData_lst.insert(0,tHeader_lst)

        # getTeacherDataList
        self.modded_tData_lst = self.init_tData_lst

        # getTeacherViewTotalRows
        tRows = len(self.modded_tData_lst)

        # getTeacherViewTotalColumns
        tColumns = len(self.modded_tData_lst[0])   


        ############################## title-config ##############################
        # createTitleFrame
        self.apexFrame = tk.Frame(self.master)
        self.apexFrame.grid(row=0, sticky="NSEW")
        self.apexFrame.grid_columnconfigure((0,1,2), weight=1)

        # createTitle
        self.lbl_title = tk.Label(
            self.apexFrame, 
            text = f"{self.teacher}'s Quizzes", 
            font=TTL, 
            fg=WHITEV1, bg=BLUEV1)
        self.lbl_title.grid(row=0, columnspan=3, ipady=18, sticky="EW")

        # createLogOutButton
        self.logOut_BTN = tk.Button(
                            self.apexFrame, 
                            text='L O G O U T', 
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV2, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV1,
                            command=self.logOut
                            )

        self.logOut_BTN.grid(row=0, column=2, padx=(0,20), pady=(28,0), sticky="NE")


        ############################## canvasFrame-config ##############################
        #createCanvasFrame
        self.canvasFrame = tk.Frame(self.master)
        self.canvasFrame.grid(row=1, column=0, pady=45, sticky='NSEW')
        self.canvasFrame.grid_rowconfigure(0, weight=1)
        self.canvasFrame.grid_columnconfigure(0,weight=1)
        

        ############################## tableCanvas-config ##############################
        #createTableCanvas
        self.tableCanvas = tk.Canvas(self.canvasFrame, highlightthickness=0)
        self.tableCanvas.grid(row=0, column=0, sticky="NSEW")


        ############################## SCRLBR-config ##############################
        #createSCRLBR
        self.vSCRLBR = tk.Scrollbar(
            self.canvasFrame, 
            orient="vertical", 
            command=self.tableCanvas.yview)
        self.vSCRLBR.grid(row=0, column=1, sticky="NS")

        self.tableCanvas.configure(yscrollcommand=self.vSCRLBR.set)

        self.vSCRLBR.grid(row=0, column=1, sticky="NS")
        self.tableCanvas.configure(yscrollcommand=self.vSCRLBR.set)


        ############################## tableFrame-config ##############################
        # createTableFrame
        self.tableFrame = tk.Frame(self.tableCanvas, bg='white')

        # createTableWindow
        self.tableCanvas.create_window((0,0), window=self.tableFrame, anchor="nw")

        self.tableFrame.bind(
            "<Configure>",
            lambda e: self.tableCanvas.configure(
                scrollregion=self.tableCanvas.bbox("all")
            )
        )

        # mouseScroll-config
        self.tableCanvas.bind_all(
            "<MouseWheel>", 
            lambda event: self.yview(
                'scroll', 
                int(-1*(event.delta/120)), 'units'
            )
        )
  
#----------------------------------------------------------------------------------------------------#

        # createTable
        for i in range(tRows):
            for j in range(tColumns):
                
                # Header Row
                if i == 0 and j < tColumns-2:
                    #createHeaderLabel
                    self.lbl = tk.Label(
                        self.tableFrame, 
                        text=self.modded_tData_lst[i][j],
                        width=25,
                        height=2, 
                        fg='white',
                        bg='cornflower blue',
                        font=HDR)

                    self.lbl.grid(row=i, column=j, pady=(0,2), sticky="NSEW")

                # Status Column Header 
                elif i == 0 and j == tColumns-2:
                    #createHeaderLabel
                    self.lbl = tk.Label(
                        self.tableFrame, 
                        text=self.modded_tData_lst[i][j],
                        height=2, 
                        width=19,
                        fg='white',
                        bg='cornflower blue',
                        font=HDR)

                    self.lbl.grid(row=i, column=j, pady=(0,2), sticky="NSEW")
                
                # Action Column Header 
                elif i == 0 and j == tColumns-1:
                    #createHeaderLabel
                    self.lbl = tk.Label(
                        self.tableFrame, 
                        text=self.modded_tData_lst[i][j],
                        height=2, 
                        width=20,
                        fg='white',
                        bg='cornflower blue',
                        font=HDR)

                    self.lbl.grid(row=i, column=j, pady=(0,2), sticky="NSEW")

                if self.noQuiz == False:
                    # Content Rows
                    if i > 0 and j < tColumns-2:
                        #createContentLabel
                        self.lbl = tk.Label(
                            self.tableFrame, 
                            text=self.modded_tData_lst[i][j],
                            wraplength=200,
                            fg='black',
                            bg=WHITEV2,
                            font=CONT)

                        self.lbl.grid(row=i, column=j, padx=2, pady=2, sticky="NSEW")
                        
                        if i == tRows-1:
                            self.lbl.grid(row=i, column=j, padx=2, pady=(2,4), sticky="NSEW")

                    # Status Content Rows
                    elif i > 0 and j == tColumns-2:
                        #createContentLabel
                        self.lbl = tk.Label(
                            self.tableFrame, 
                            text=self.modded_tData_lst[i][j],
                            wraplength=200,
                            fg='black',
                            bg=WHITEV2,
                            font=CONT)

                        self.lbl.grid(row=i, column=j, padx=(2,4), pady=2, sticky="NSEW")
                        
                        if i == tRows-1:
                            self.lbl.grid(row=i, column=j, padx=(2,4), pady=(2,4), sticky="NSEW")
                    
                    # Button Content Row
                    if i > 0 and j == tColumns-1:

                        #createButtonFrame
                        self.btn_frame = tk.Frame(self.tableFrame, bg="white")
                        self.btn_frame.grid(row=i, column=j, pady=2, sticky="NSEW")
                        
                        if i == tRows-1:
                            self.btn_frame.grid(row=i, column=j, pady=(2,4), sticky="NSEW")

                        #createManageButton
                        self.manage_BTN = tk.Button(
                            self.btn_frame, 
                            text="M A N A G E", 
                            fg="white", 
                            bg="#2b2b2b",   
                            font=BTN,
                            command=lambda row=i: self.create_managerScreen(row))

                        #createViewButton
                        self.view_BTN = tk.Button(
                            self.btn_frame,
                            text="V I E W", 
                            fg="white", 
                            bg="#2b2b2b",   
                            font=BTN,
                            command=lambda row=i: self.viewQuiz(row))

                        self.manage_BTN.pack(side="top",fill="both",expand=True)
                        self.view_BTN.pack(side="top",fill="both",expand=True)
                        if self.modded_tData_lst[i][j] == False:
                            self.view_BTN.config(state='disabled')
                
                elif self.noQuiz == True:

                    #creatEmptyIntroLabel
                    self.lbl = tk.Label(
                        self.canvasFrame,
                        text=f'Such emptiness here, {self.teacher}. :/',
                        font=HDR)

                    self.lbl.grid(row=1, columnspan=3, padx=2, pady=2, sticky="NSEW")

                    #creatEmptyLabel
                    self.lbl2 = tk.Label(
                        self.canvasFrame,
                        text="'ADD QUIZ' to start creating quizzes and 'MANAGE' them.",
                        font=CONT)

                    self.lbl2.grid(row=2, columnspan=3, padx=2, pady=2, sticky="NSEW")


        addQuiz_BTN = tk.Button(self.canvasFrame, 
                               text='A D D  Q U I Z', 
                               font=BTN, 
                               relief="flat",
                               fg=WHITEV1, 
                               bg=BLUEV1, 
                               activeforeground=WHITEV2, 
                               activebackground=BLUEV2,
                               command=self.addQuiz)

        addQuiz_BTN.grid(row=10, column=0, columnspan=3, padx=(0,18), pady=(10,0), sticky="SEW")
    
    #--------------------------------------- method-config ---------------------------------------#
    ######################## refreshFrame ########################
    def refresh(self):
        self.apexFrame.destroy()
        self.canvasFrame.destroy()

        tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
        quizDictList = tData[self.teacher]

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

        self.__init__(self.master, self.teacher, DATA_LST)
    ##############################################################


    ############ viewQuiz ###########
    def viewQuiz(self, row):
        self.apexFrame.destroy()
        self.canvasFrame.destroy()
        QUIZ = self.tData_lst[row-1][0]
        quizRun.QuizRun(
            self.master, 
            QUIZ, 
            "teacher", 
            self.teacher
        )
    #################################


    ######################## manageQuizScreen ########################
    def create_managerScreen(self, row):
        self.master.title("Quizlyy - Manager")
        QUIZ = self.tData_lst[row-1][0].split(':')[0]

        self.apexFrame.destroy()
        self.canvasFrame.destroy()

        self.tableCanvas.unbind_all("<MouseWheel>")

        self.managerFrame = ttk.Frame(self.master)
        self.managerFrame.grid(row=1)


        ############################## title-config ##############################
        # createTitleFrame
        self.apexFrame = tk.Frame(self.master)
        self.apexFrame.grid(row=0, sticky="NSEW")
        self.apexFrame.grid_columnconfigure((0,1,2), weight=1)

        #createTitle
        self.lbl_title.destroy()
        self.lbl_title = tk.Label(
            self.apexFrame, 
            text = f"{QUIZ} Manager", 
            font=TTL, 
            fg=WHITEV1, bg=BLUEV1)
        self.lbl_title.grid(row=0, columnspan=3, ipady=18, sticky="EW")


        ############################### backOut button ###############################
        self.backOut_BTN = tk.Button(
                            self.apexFrame, 
                            text='⮐  B A C K', 
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV2, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV1,
                            command=self.backOut
                            )

        self.backOut_BTN.grid(row=0, column=0, padx=(20,0), pady=(28,0), sticky="NW")

        
        ############################### edit-QCA ###############################
        ############ edit-QCA ###########
        def editQCA():
            self.apexFrame.destroy()
            self.canvasFrame.destroy()
            self.managerFrame.destroy()

            QUIZ = self.tData_lst[row-1][0]
            quizQCA.QCAForm(
                self.master, 
                QUIZ,
                self.teacher)
        #################################

        self.editQCA_LBL = ttk.Label(
                            self.managerFrame, 
                            text=f"🛠 Setup or Modify {QUIZ}'s Question/Choice/Answer.",
                            font=TAG)
        self.editQCA_LBL.grid(row=1, column=1, columnspan=3, pady=(20,0))

        self.editQCA_BTN = tk.Button(
                            self.managerFrame, 
                            text='D E P L O Y  Q C A  F O R M',
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV1, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV2,
                            command=editQCA
                            )

        self.editQCA_BTN.grid(
            row=2, column=1, 
            columnspan=3, 
            pady=(5,40),
            sticky="SEW"
            )
        ########################################################################

        ############################### editQuiz ###############################
        ############ editQuiz ###########
        def editQuiz():
            self.apexFrame.destroy()
            self.canvasFrame.destroy()
            self.managerFrame.destroy()

            QUIZ = self.tData_lst[row-1][0]
            quizEdit.editQuiz_info(
                self.master, 
                QUIZ, 
                self.teacher, 
                self.tData_lst
                )
        #################################

        self.editQuiz_LBL = ttk.Label(
                            self.managerFrame, 
                            text=f"⚙ Modify {QUIZ}'s Name/Topic/Status.", 
                            font=TAG)
        self.editQuiz_LBL.grid(row=4, column=1, columnspan=3)

        self.editQuiz_BTN = tk.Button(
                            self.managerFrame, 
                            text='D E P L O Y  Q U I Z  F O R M', 
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV1, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV2,
                            command=editQuiz
                            )

        self.editQuiz_BTN.grid(
            row=5, column=1, 
            columnspan=3, 
            pady=(5,40),
            sticky="SEW"
            )
        ########################################################################

        ############################### del-Quiz ###############################
        ####################### delQuiz #######################
        def delQuiz():

            delMB = mb.askyesno(
                 "WARNING! - QUIZ DELETION",
                 ("Are you sure you want to delete this Quiz?\n"
                  "NOTE: The quiz QCAs will be deleted too.\n\n"
                  "This action cannot be undone."),
                  icon="warning")

            if delMB:
                self.managerFrame.destroy()

                QUIZ = self.tData_lst[row-1][0]
                quizName, quizID = QUIZ.split(':')


                tData = loadJSON(TEACHER_QUIZ_INFO_FILENAME)
                quizDictList = tData[self.teacher]

                for quizDict in quizDictList:
                    if quizDict["Quiz Name"] == quizName and \
                        quizDict["ID"] == quizID:
                        quizIndex = quizDictList.index(quizDict)
                        del quizDictList[quizIndex]

                tData[self.teacher] = quizDictList
                writeJSON(tData, TEACHER_QUIZ_INFO_FILENAME)


                sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)

                for STUDENT in sData:
                    for sDict in sData[STUDENT]:
                        sDict_Index = sData[STUDENT].index(sDict)
                        if sDict["Quiz Name"] == quizName and \
                            sDict["ID"] == quizID:
                            del sData[STUDENT][sDict_Index]

                writeJSON(sData, STUDENT_QUIZ_INFO_FILENAME)


                qcaData = loadJSON(QCA_DATA_FILE)

                if QUIZ in qcaData:
                    del qcaData[QUIZ]
                
                writeJSON(qcaData,QCA_DATA_FILE)

                self.refresh()
        #######################################################

        self.delQuiz_LBL = ttk.Label(
                            self.managerFrame, 
                            text=f"🗑 Delete {QUIZ}.", 
                            font=TAG)
        self.delQuiz_LBL.grid(row=7, column=1, columnspan=3)

        self.delQuiz_BTN = tk.Button(
                            self.managerFrame, 
                            text='D E L E T E  Q U I Z', 
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV1, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV2,
                            command=delQuiz
                            )

        self.delQuiz_BTN.grid(
            row=8, column=1, 
            columnspan=3, 
            pady=(5,0),
            sticky="SEW"
            )
        ########################################################################
    
    ###############################################################################################\

    ############ addQuiz ############
    def addQuiz(self):
        self.apexFrame.destroy()
        self.canvasFrame.destroy()
        quizEdit.editQuiz_info(
            self.master, 
            None, 
            self.teacher, 
            self.tData_lst)
        pass
    #################################

    ################ yview-Scroll ################
    # Checks if the content fits within the canvas
    def yview(self, *args):
        if self.tableCanvas.yview() == (0.0, 1.0):
            return
        self.tableCanvas.yview(*args)
    ##############################################

    ############ backOut ############
    def backOut(self):
        self.managerFrame.destroy()
        self.refresh()
    #################################

    ############ logOut ############
    def logOut(self):
        confirmation = mb.askyesno(
            'Logout Confirmation',
            'Are you sure you want to log out?', 
            icon='warning', 
            default='no' )

        if confirmation:
            self.apexFrame.destroy()
            self.canvasFrame.destroy()
            Quizlyy.login(self.master)
    ################################
    #------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------#


#----------------------------------------------------------------------------------------------------#