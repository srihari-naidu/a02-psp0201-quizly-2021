#----------------------------------------------------------------------------------------------------#

############ imports ############
import os
import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

import mainPage
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
TTL2 = ("Bahnschrift Bold SemiCondensed", "36")

TAG = ("Bahnschrift SemiCondensed", "14")
QSPACE = ("Bahnschrift", "13")
CSPACE = ("Bahnschrift SemiLight", "12")

BTN = ("Bahnschrift SemiBold", "12")
RDBTN = ("Bahnschrift SemiBold SemiCondensed", "12")
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
EMPTY_QCA = {
                "question": "",
                "choices": [
                    "",
                    "",
                    "",
                    ""
                ],
                "answer": None,
            }

QCA_DATA_FILE = 'quiz-qca-data.json'
TEACHER_QUIZ_INFO_FILENAME = 'teacher-quiz-info.json'
STUDENT_QUIZ_INFO_FILENAME = 'student-quiz-info.json'
################################################################################

#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#

class QCAForm():

    def __init__(self, root, quiz, username, index=0):

        ########## master-config ##########
        self.master = root
        self.master.title("Quizlyy - Q.C.A Manager")
        
        self.teacher = username

        ################# Frame #################
        self.apexFrame = self.create_apexFrame()
        self.mainFrame = self.create_mainFrame()


        ###### grid ######
        self.grid_config()


        ##################### pre-req #####################
        self.quiz = quiz
        self.quizName = quiz.split(':')[0]

        with open(QCA_DATA_FILE) as f:
            first_line = f.readline()
        if first_line == {}:
            writeJSON({self.quiz:[]}, QCA_DATA_FILE)
        
        self.qcaData = loadJSON(QCA_DATA_FILE)

        self.qcaIndex = index
        self.var = tk.IntVar()


        ########### misc ###########
        self.emptyQuiz_screen = None
        self.releaseCheckBTN = False


        ########################## program ##########################
        if self.quiz not in self.qcaData:
            self.create_splashScreen()
        
        elif self.qcaData[self.quiz] == []:
            self.create_splashScreen()

        else:
            self.qcaList = self.qcaData[self.quiz]
            self.show_QCAForm()

    #-----------------------------------------------------------------------------------------------#
    def show_QCAForm(self):

        ############################ preset ###########################
        self.quesQuestion = self.qcaList[self.qcaIndex]['question']
        self.quesChoice = self.qcaList[self.qcaIndex]['choices']
        self.quesAnswer = self.qcaList[self.qcaIndex]['answer']
        ###############################################################

        ############################ title ############################
        self.title_TAG = self.create_title_TAG(f'{self.quizName}')
        ###############################################################

        ########################### question ##########################
        self.question_TAG = self.create_question_TAG(self.qcaIndex)
        self.question_SPACE_var = tk.StringVar()
        self.question_SPACE = self.create_question_SPACE()
        ###############################################################

        ################################### choice ###################################
        self.default_select_answer = False

        
        self.choice1_SPACE_var = tk.StringVar(value=self.quesChoice[0])
        self.choice1_RDBTN = self.create_choice_RDBTN(1)
        
        self.choice2_SPACE_var = tk.StringVar(value=self.quesChoice[1])
        self.choice2_RDBTN = self.create_choice_RDBTN(2)
        
        self.choice3_SPACE_var = tk.StringVar(value=self.quesChoice[2])
        self.choice3_RDBTN = self.create_choice_RDBTN(3)
        
        self.choice4_SPACE_var = tk.StringVar(value=self.quesChoice[3])
        self.choice4_RDBTN = self.create_choice_RDBTN(4)
        

        self.choice_SPACE_varList = [
            self.choice1_SPACE_var, 
            self.choice2_SPACE_var, 
            self.choice3_SPACE_var, 
            self.choice4_SPACE_var
        ] 

        self.choice1_SPACE = self.create_choice_SPACE(1, self.choice_SPACE_varList[0])
        self.choice2_SPACE = self.create_choice_SPACE(2, self.choice_SPACE_varList[1])
        self.choice3_SPACE = self.create_choice_SPACE(3, self.choice_SPACE_varList[2])
        self.choice4_SPACE = self.create_choice_SPACE(4, self.choice_SPACE_varList[3])
        ##############################################################################

        ################## button ##################

        self.next_BTN = self.create_next_BTN()
        self.prev_BTN = self.create_prev_BTN()

        if self.qcaIndex == (len(self.qcaList)-1):
            self.next_BTN.config(state='disabled')

        if self.qcaIndex == 0:
            self.prev_BTN.config(state='disabled')

        self.add_BTN = self.create_add_BTN()
        self.del_BTN = self.create_del_BTN()


        if self.releaseCheckBTN == True:
            self.check_BTN = self.create_check_BTN()
            self.save_backOut_BTNv2 = self.create_exit_BTN_v2()
        else:
            self.save_backOut_BTNv1 = self.create_exit_BTN()
        ############################################

    #-----------------------------------------------------------------------------------------------#

    #---------------- apexFrame-config ----------------#
    def create_apexFrame(self):
        apexFrame = ttk.Frame(self.master)
        apexFrame.grid(row=0,sticky="NSEW")
        return apexFrame
    #--------------------------------------------------#

    #---------------- mainFrame-config ----------------#
    def create_mainFrame(self):
        mainFrame = ttk.Frame(self.master)
        mainFrame.grid(row=1,pady=(50,0),sticky="NSEW")
        return mainFrame
    #--------------------------------------------------#
    
    #------------------------ grid-config ------------------------#
    def grid_config(self):
        
        # master-grid
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # apexFrame-grid
        self.apexFrame.grid_rowconfigure((0), weight=1)
        self.apexFrame.grid_columnconfigure((1,2,3), weight=1)

        # mainFrame-grid
        self.mainFrame.grid_rowconfigure((1,2,3,4,5,6,7,8), weight=1)
        self.mainFrame.grid_columnconfigure((1,2,3), weight=1)

    #-------------------------------------------------------------#
       
    #------------------------------ splash-config ------------------------------#
    def create_splashScreen(self):
        self.splashFrame = ttk.Frame(self.master)
        self.splashFrame.grid(row=1)

        self.title_TAG = self.create_title_TAG(f'Q.C.A')
        self.create_splashScreen_WIDGETS()

        self.start_BTN = tk.Button(self.splashFrame, 
                                   text='S T A R T  ᐅ', 
                                   font=BTN, 
                                   relief="flat",
                                   fg=WHITEV1, 
                                   bg=BLUEV1, 
                                   activeforeground=WHITEV2, 
                                   activebackground=BLUEV2,
                                   command=self.startQCA)

        self.start_BTN.grid(
            row=5, column=1, 
            columnspan=3, 
            pady=(40,20), 
            ipady=0, 
            sticky="SEW"
            )

    def create_splashScreen_WIDGETS(self):

        self.backOut_BTN = self.create_backOut_BTN()
        self.backOut_BTN.grid(row=0, column=1, padx=(20,0), pady=(28,0), sticky="NW")
        
        ssq_TAG = ttk.Label(
            self.splashFrame, 
            text=(self.quizName), 
            font=TTL2)
        ssq_TAG.grid(row=2, column=1, columnspan=3)

        ss_TAG = ttk.Label(
            self.splashFrame,
            text=("START creating Q.C.As for the quiz."), 
            font=TAG)
        ss_TAG.grid(row=4, column=1, columnspan=3)


    def startQCA(self):
        if (self.quiz not in self.qcaData):
            self.qcaData[self.quiz] = [EMPTY_QCA]

        elif (self.qcaData[self.quiz]==[]):
            self.qcaData[self.quiz].append(EMPTY_QCA)

        self.qcaList = self.qcaData[self.quiz]

        self.clearFrame(self.apexFrame)
        self.splashFrame.destroy()
        self.show_QCAForm()
    #--------------------------------------------------------------------------#
    
    #------------------------------------- title-config --------------------------------------#
    def create_title_TAG(self, title):
        title_TAG = tk.Label(self.apexFrame, text=title, font=TTL, fg=WHITEV1, bg=BLUEV1)
        title_TAG.grid(row=0, column=1, columnspan=3, ipady=18, pady=(0,0), sticky="EW")
        return title_TAG
    #-----------------------------------------------------------------------------------------#

    #--------------------------------------- question-config ---------------------------------------#
    def get_question_SPACE_var(self, event):
        self.question_SPACE_var.set(self.quesQuestion)
        self.question_SPACE.replace("1.0", tk.END, self.question_SPACE_var.get())

    def create_question_TAG(self, n):
        question_SPACE = ttk.Label(self.mainFrame, text=f'QUESTION  {n+1}', font=TAG)
        question_SPACE.grid(row=1, column=1, padx=(0,0), pady=(20,50), sticky="E")
        return question_SPACE

    def create_question_SPACE(self):
        question_SPACE = tk.Text(self.mainFrame, 
                                 font=QSPACE,
                                 wrap=tk.NONE, 
                                 width=60, 
                                 height=4, 
                                 relief="flat", 
                                 bd=0.5)

        xscrollbar = ttk.Scrollbar(self.mainFrame, orient="horizontal", command=question_SPACE.xview)
        yscrollbar = ttk.Scrollbar(self.mainFrame, orient="vertical", command=question_SPACE.yview)
        question_SPACE.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        xscrollbar.grid(row=1, column=2, columnspan=2, padx=(41, 65), pady=(75,0), sticky="EW")
        yscrollbar.grid(row=1, column=3, padx=(0, 48), pady=(5,35), sticky="NES")
        question_SPACE.grid(row=1, column=2, columnspan=2, padx=(24,48), pady=(0,30), ipadx=1)

        question_SPACE.bind('<Configure>', self.get_question_SPACE_var)
        return question_SPACE
    #-----------------------------------------------------------------------------------------------#

    #------------------------------------- choice-config -------------------------------------#
    def create_choice_RDBTN(self, n):
        choice_RDBTN = tk.Radiobutton(self.mainFrame, 
                                      text=f'CHOICE  {n}', 
                                      font=RDBTN, 
                                      variable=self.var, 
                                      value=n, 
                                      activebackground=GRAY,   
                                      background=WHITEV3,   
                                      selectcolor=BLUEV1,
                                      indicator="false",
                                      relief="flat",
                                      offrelief="flat",
                                      overrelief="flat")

        choice_RDBTN.grid(row=n+1, column=1, padx=(60,0), pady=(0,3), sticky="EW")
        return choice_RDBTN

    def create_choice_SPACE(self, n, choice):
        choice_SPACE = tk.Entry(self.mainFrame, 
                              textvariable=choice, 
                              font=CSPACE, 
                              width=60, 
                              bg="WHITE", 
                              relief='flat')
        choice_SPACE.grid(row=n+1, column=2, columnspan=2, padx=(18,40), pady=(0,4), ipady=2)

        if not(self.default_select_answer):
            if (choice.get() == self.quesAnswer):
                self.var.set(n)
                self.default_select_answer = True
            else:
                self.var.set(0)

        return choice_SPACE
    #-----------------------------------------------------------------------------------------#

    #------------------------------ empty-config ------------------------------#
    def create_emptyQuiz_screen(self):
        self.clearFrame(self.mainFrame)

        self.title_TAG.grid_forget()
        self.title_TAG = self.create_title_TAG(f'EMPTY QUIZ')

        self.create_emptyQuiz_TAGS()

        self.add_BTN = self.create_add_BTN()
        self.save_backOut_BTN = self.create_exit_BTN()

        return True

    def create_emptyQuiz_TAGS(self):
        emptyQuiz_TTL = ttk.Label(
            self.mainFrame,
            text=("Such emptiness... :/"), 
            font=TTL2)
        emptyQuiz_TTL.grid(row=3, column=1, columnspan=3)

        emptyQuiz_TAG = ttk.Label(
            self.mainFrame, 
            text=("Click on  ' ADD+ '  to move on and start creating QCAs.\n"
                  "Click on ' SAVE & BACKOUT ' to leave the quiz empty as is."), 
            font=TAG)
        emptyQuiz_TAG.grid(row=4, column=1, columnspan=3)
        

    #-------------------------------------- button-config ------------------------------------------#
    ################################## next_BTN ##################################
    def nextQCA(self):
        self.saveQCA(check_on_save=False)
        self.qcaIndex+=1
        self.show_QCAForm()


    def create_next_BTN(self):
        next_BTN = tk.Button(self.apexFrame, 
                             text=' > ', 
                             font=BTN, 
                             relief="flat", 
                             fg=WHITEV1, 
                             bg=BLUEV2, 
                             activeforeground=WHITEV2, 
                             activebackground=BLUEV1,
                             command=self.nextQCA)

        next_BTN.grid(row=0, column=3, padx=(0,20), pady=(28,0), sticky="NE")
        return next_BTN
    ##############################################################################

    ################################## prev_BTN ##################################
    def prevQCA(self):
        self.saveQCA(check_on_save=False)
        self.qcaIndex-=1
        self.show_QCAForm()


    def create_prev_BTN(self):
        prev_BTN = tk.Button(self.apexFrame, 
                             text=' < ', 
                             font=BTN, 
                             relief="flat",
                             fg=WHITEV1, 
                             bg=BLUEV2, 
                             activeforeground=WHITEV2, 
                             activebackground=BLUEV1,
                             command=self.prevQCA)

        prev_BTN.grid(row=0, column=1, padx=(20,0), pady=(28,0), sticky="NW")
        return prev_BTN
    ##############################################################################
    
    ################################### add_BTN ##################################
    def addQCA(self):

        # It'll not check saveQCA at the emptyQuiz_screen
        if len(self.qcaList) != 0:
            self.saveQCA(check_on_save=False)

        # If the emptyQuiz_screen has been shown, it'll be cleared after addQCA
        if self.emptyQuiz_screen is not None:
            self.clearFrame(self.mainFrame)

        self.qcaList.append(EMPTY_QCA)
        self.qcaIndex=len(self.qcaList)-1 

        self.show_QCAForm()   


    def create_add_BTN(self):
        add_BTN = tk.Button(self.apexFrame, 
                             text='A D D  ✙', 
                             font=BTN,
                             fg=WHITEV1, 
                             bg=BLUEV2, 
                             activeforeground=WHITEV2, 
                             activebackground=BLUEV1,
                             relief="flat", 
                             command=self.addQCA)

        add_BTN.grid(row=0, column=3, padx=(0,66), pady=(28,0), sticky="NE")
        return add_BTN         
    ##############################################################################

    ################################### del_BTN ##################################
    def delQCA(self):
        del_MB = mb.askyesno(
                 "WARNING! - Q.C.A",
                 ("Are you sure you want to delete this Q.C.A?\n"
                  "This action cannot be undone."),
                  icon="warning")
        
        if del_MB:
            del self.qcaList[self.qcaIndex]
            self.qcaData[self.quiz] = self.qcaList
            writeJSON(self.qcaData, QCA_DATA_FILE)
            self.qcaIndex-=1

        if self.qcaIndex < 0:
            self.qcaIndex = 0
        
        if len(self.qcaList) == 0:
            self.create_emptyQuiz_screen()
            self.emptyQuiz_screen = True
            
        else:
            self.show_QCAForm()


    def create_del_BTN(self):
        del_BTN = tk.Button(self.apexFrame, 
                            text='🗑  D E L', 
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV2, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV1,
                            command=self.delQCA)

        del_BTN.grid(row=0, column=1, padx=(66,0), pady=(28,0), sticky="NW")
        return del_BTN
    ##############################################################################
    
    ########################################### saveQCA ###########################################
    def saveQCA(self, check_on_save=True):

        question = self.question_SPACE.get('1.0', 'end-1c')
        
        choices = [
            self.choice1_SPACE.get(),
            self.choice2_SPACE.get(),
            self.choice3_SPACE.get(),
            self.choice4_SPACE.get()
            ]

        selection = self.var.get()

        if selection == 0:
            answer = None
        else:
            answer = self.choice_SPACE_varList[selection-1].get()
            if answer == "":
                answer = None

        QCA = {
            "question": question,
            "choices": choices,
            "answer": answer,
        }
        
        self.qcaList[self.qcaIndex] = QCA
        self.qcaData[self.quiz] = self.qcaList
        writeJSON(self.qcaData, QCA_DATA_FILE)


        if check_on_save:

            if question == "":
                mb.showwarning(title="WARNING INFO! - Question",
                               message=("You have left your 'Question' space blank!\n"
                                        "Please fill it up before you SAVE & BACKOUT."))
            
            elif (choices[0] == "") or \
                    (choices[1] == "") or \
                        (choices[2] == "") or \
                            (choices[3] == ""):

                mb.showwarning(title="WARNING INFO! - Choices",
                               message=("You have left your Choice(s) space blank!\n"
                                        "Please fill it up before you SAVE & BACKOUT."))

            elif selection == 0:
                mb.showwarning(title="WARNING INFO! - Answer",
                    message=("You have left your Answer (Choice #) unselected!\n"
                             "Please select it before you SAVE & BACKOUT."))
            else:
                mb.showinfo("INFO - Q.C.A", "This Q.C.A is looking complete ;)")

    ###############################################################################################

    ######################################### exit_BTN ############################################
    def exitQCA(self):
        # 'EXIT' at emptyQuiz_screen page
        if len(self.qcaList) == 0:
            self.qcaData[self.quiz] = self.qcaList
            writeJSON(self.qcaData, QCA_DATA_FILE)
            mb.showinfo("STATUS - Q.C.A", "Quiz was saved empty.")

            self.backOut()

        else:
            self.saveQCA(check_on_save=False)        
                
            INCOMPLETE_noList = []

            for QCA_INDEX, QCA in enumerate(self.qcaList):
                if QCA['question'] != "" and \
                   QCA['choices'] != ["","","",""] and \
                   QCA['answer'] != None:

                    COMPLETE_no = str(QCA_INDEX+1)
                    if COMPLETE_no in INCOMPLETE_noList:
                        INCOMPLETE_noList.remove(COMPLETE_no)

                elif QCA['question']=="" or \
                     QCA['choices']==["","","",""] or \
                     QCA['answer']==None:

                    INCOMPLETE_no = str(QCA_INDEX+1)
                    if INCOMPLETE_no not in INCOMPLETE_noList:
                        INCOMPLETE_noList.append(INCOMPLETE_no)

            if INCOMPLETE_noList != []:

                if len(INCOMPLETE_noList) == 1:
                    delMB = mb.askyesnocancel(
                             title="WARNING! - Q.C.A",
                             message=("It seems that Question {0} is blank/incomplete.\n"
                                      "Are you sure you still want to backout?\n\n"
                                      "Hit 'YES' to delete blank/incomplete question and exit.\n"
                                      "Hit 'NO' to check on what's incomplete in Question {0}"
                                     ).format(INCOMPLETE_noList[0]),
                             icon='warning')

                else:
                    delMB = mb.askyesnocancel(
                             title="WARNING! - Q.C.A",
                             message=("It seems that Questions {0} were blank/incomplete.\n"
                                      "Are you sure you still want to backout?\n\n"
                                      "Hit 'YES' to delete the blank/incomplete questions and exit.\n"
                                      "Hit 'NO' to check on what's incomplete in Question {1}"
                                      ).format(', '.join(INCOMPLETE_noList), INCOMPLETE_noList[0]),
                             icon='warning')
                
                if delMB == True:
                    INCOMPLETE_noList.clear()

                    self.qcaList = list(filter(lambda QCA: QCA['question'] != "" and 
                                                           QCA['choices'] != ["","","",""] and 
                                                           QCA['answer'] != None, 
                                                           self.qcaList))

                    self.qcaData[self.quiz] = self.qcaList
                    writeJSON(self.qcaData, QCA_DATA_FILE)

                    if len(self.qcaList)==0:
                        mb.showinfo("STATUS - Q.C.A", "Quiz was saved empty.")
                    elif len(self.qcaList)==1:
                        mb.showinfo("STATUS - Q.C.A", "Q.C.A was saved successfully.")
                    elif len(self.qcaList)>1:
                        mb.showinfo("STATUS - Q.C.A", "Q.C.As were saved successfully.")

                    self.backOut()

                
                elif delMB == False:

                    self.clearFrame(self.mainFrame)
                    self.releaseCheckBTN = True
                    self.qcaIndex = int(INCOMPLETE_noList[0])-1
                    self.show_QCAForm()

                                                                
            else:
                self.saveQCA(check_on_save=False)
                self.qcaData[self.quiz] = self.qcaList
                writeJSON(self.qcaData, QCA_DATA_FILE)

                if len(self.qcaList)==0:
                    mb.showinfo("STATUS - Q.C.A", "Quiz was saved empty.")
                elif len(self.qcaList)==1:
                    mb.showinfo("STATUS - Q.C.A", "Q.C.A was saved successfully.")
                elif len(self.qcaList)>1:
                    mb.showinfo("STATUS - Q.C.A", "Q.C.As were saved successfully.")

                self.backOut()



    def create_exit_BTN(self):
        exit_BTN = tk.Button(self.mainFrame, 
                               text='💾  S A V E  &  B A C K O U T  ⮌',
                               font=BTN, 
                               relief="flat",
                               fg=WHITEV1, 
                               bg=BLUEV1, 
                               activeforeground=WHITEV2, 
                               activebackground=BLUEV2,
                               command=self.exitQCA)

        exit_BTN.grid(row=7, column=1, columnspan=3, padx=20, pady=(40,20), sticky="SEW")
        return exit_BTN


    def create_exit_BTN_v2(self):
        exit_BTN = tk.Button(self.mainFrame,
                               text='💾  S A V E  &  B A C K O U T  ⮌', 
                               font=BTN, 
                               relief="flat",
                               fg=WHITEV1, 
                               bg=BLUEV1, 
                               activeforeground=WHITEV2, 
                               activebackground=BLUEV2,
                               command=self.exitQCA)

        exit_BTN.grid(row=7, column=1, columnspan=3, padx=(410,20), pady=(40,20), sticky="SEW")
        return exit_BTN
    ###############################################################################################

    ######################################### button-check ########################################
    def checkQCA(self):
        self.saveQCA(check_on_save=True)

    def create_check_BTN(self):
        check_BTN = tk.Button(self.mainFrame, 
                              text='✔  C H E C K  Q C A', 
                              font=BTN, 
                              relief="flat",
                              fg=WHITEV1, 
                              bg=BLUEV1, 
                              activeforeground=WHITEV2, 
                              activebackground=BLUEV2,
                              command=self.checkQCA)

        check_BTN.grid(row=7, column=1, columnspan=3, padx=(20,410), pady=(40,20), sticky="SEW")
        return check_BTN
    ###############################################################################################

    ######################################## button-backout #######################################
    def backOut(self):
        self.apexFrame.destroy()
        self.mainFrame.destroy()

        # get tData_lst
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

        mainPage.teacherPage(self.master, self.teacher, DATA_LST)

        
    def create_backOut_BTN(self):
        backOut_BTN = tk.Button(self.apexFrame, 
                            text='⮐  B A C K', 
                            font=BTN, 
                            relief="flat",
                            fg=WHITEV1, 
                            bg=BLUEV2, 
                            activeforeground=WHITEV2, 
                            activebackground=BLUEV1,
                            command=self.backOut)

        backOut_BTN.grid(row=0, column=1, padx=(66,0), pady=(28,0), sticky="NW")
        return backOut_BTN
    ###############################################################################################
    #---------------------------------------------------------------------------------------------#

    #--------------------------------------- method-config ---------------------------------------#
    ################ clearFrame ################
    def clearFrame(self, frame):
        for child in frame.winfo_children():
            child.destroy()
    ############################################
    #------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------#