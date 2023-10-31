#----------------------------------------------------------------------------------------------------#

############ imports ############
import json
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from tkinter.ttk import Progressbar

import mainPage
import quizQCA
#################################

#----------------------------------------------------------------------------------------------------#

####### colours #######
GRAY = "#717D7F"

BLUEV1 = "Cornflower Blue"
BLUEV2 = "#557FCC"

WHITEV1 = "#F9F9F9"
WHITEV2 = "#E7E7E7"
#######################

#----------------------------------------------------------------------------------------------------#

################## font-styles ##################
TTL = ("Bahnschrift Bold SemiCondensed", "28",)
TTL2 = ("Bahnschrift Bold SemiCondensed", "36",)
TAG = ("Bahnschrift SemiCondensed", "14")

QLBL = ("Bahnschrift", "14")
CLBL = ("Bahnschrift SemiLight", "13")

BTN = ("Bahnschrift SemiBold", "12")

#################################################

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

############################################### const. ###############################################
QCA_DATA_FILE = 'quiz-qca-data.json'
TEACHER_QUIZ_INFO_FILENAME = 'teacher-quiz-info.json'
STUDENT_QUIZ_INFO_FILENAME = 'student-quiz-info.json'
######################################################################################################

#----------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------#

class QuizRun:

    def __init__(self, root, quiz, mode, username, index=0):

        ########## master-config ##########
        self.master = root
        self.master.title("Quizlyy - Take")

        self.mode = mode
        
        if self.mode == "student":
            self.student = username
            # self.sData_lst = userdata
        elif self.mode == "teacher":
            self.teacher = username
            # self.tData_lst = userdata


        ################### frame & others ###################
        self.apexFrame = self.create_apexFrame()
        self.masterFrame = self.create_masterFrame()
        self.mainCanvas = self.create_mainCanvas()
        self.mainFrame_SCRLBR = self.create_mainFrame_SCRLBR()
        self.mainFrame = self.create_mainFrame()

    
        ###### grid ######
        self.grid_config()


        ################################## pre-req ##################################
        self.quiz = quiz
        self.quizName, self.quizID = quiz.split(':')

        self.quesData = loadJSON(QCA_DATA_FILE)
        self.quesList = self.quesData[self.quiz]
        self.quesData_size = len(self.quesList)

        if self.mode == "student":
            EMPTY_STUDENT_GUESS = ["" for _ in range(len(self.quesData[self.quiz]))]
            self.student_guessList = EMPTY_STUDENT_GUESS

        self.quesIndex = index
        self.choice_var = tk.StringVar()
        

        ###### misc ######
        if self.mode == "student":
            self.correct = 0


        #### program ####
        self.create_splashScreen()


    #-----------------------------------------------------------------------------------------------#
    def startQuiz(self):

        self.clearFrame(self.mainFrame)
        
        ############################ preset ###########################
        self.quesQuestion = self.quesList[self.quesIndex]['question']
        self.quesChoice = self.quesList[self.quesIndex]['choices']
        self.quesAnswer = self.quesList[self.quesIndex]['answer']

        self.quesAnswerList = []
        for i in range(len(self.quesList)):
            self.quesAnswerList.append(self.quesList[i]['answer'])
        ###############################################################

        ############################ title ############################
        self.lbl_title = self.create_lbl_title(f'{self.quizName}')
        ###############################################################

        ########################### question ##########################
        self.lbl_question = self.create_lbl_question_no(self.quesIndex)
        self.lbl_question = self.create_lbl_question()
        ###############################################################

        ############################ choice ###########################
        self.default_select_student_guess = False


        self.choice1_RDBTN = self.create_choice_RDBTN(1)
        self.choice2_RDBTN = self.create_choice_RDBTN(2)
        self.choice3_RDBTN = self.create_choice_RDBTN(3)
        self.choice4_RDBTN = self.create_choice_RDBTN(4)


        self.lbl_choice1 = self.create_lbl_choice(1, self.quesChoice[0])
        self.lbl_choice2 = self.create_lbl_choice(2, self.quesChoice[1])
        self.lbl_choice3 = self.create_lbl_choice(3, self.quesChoice[2])
        self.lbl_choice4 = self.create_lbl_choice(4, self.quesChoice[3])
        ################################################################

        ##################### button #####################
        self.btn_next = self.create_btn_next()
        if self.quesIndex+1 == self.quesData_size:
            self.btn_next.config(state='disabled')

        self.btn_prev = self.create_btn_prev()
        if self.quesIndex == 0:
            self.btn_prev.config(state='disabled')

        if self.mode == "student":
            if self.quesIndex == (len(self.quesList)-1):
                self.btn_submit = self.create_btn_submit()

        if self.mode == "teacher":
            self.btn_edit = self.create_btn_edit()
            self.backOut_BTN = self.create_backOut_BTN()
        ##################################################

    #-----------------------------------------------------------------------------------------------#

    #------------- titleFrame-config ---------------#
    def create_apexFrame(self):
        apexFrame = ttk.Frame(self.master)
        apexFrame.grid(row=0,sticky="NSEW")

        return apexFrame
    #-----------------------------------------------#

    #-------------- mainFrame-config ---------------#
    def create_masterFrame(self):
        masterFrame = ttk.Frame(self.master)
        masterFrame.grid(row=1, sticky="NSEW")

        return masterFrame
    #-----------------------------------------------#
  
    #-------------- mainCanvas-config --------------#
    def create_mainCanvas(self):
        mainCanvas = tk.Canvas(self.masterFrame,
                        highlightthickness=0)
        mainCanvas.grid(row=1, sticky="NSEW")

        return mainCanvas
    #-----------------------------------------------#

    #---------------- SCRLBR-config ----------------#
    def create_mainFrame_SCRLBR(self):
        SCRLBR = ttk.Scrollbar(
            self.masterFrame, 
            orient="vertical", 
            command=self.mainCanvas.yview
            )

        SCRLBR.grid(row=1, column=1, sticky="NS")

        self.mainCanvas.configure(
            yscrollcommand=SCRLBR.set
            )
            
        return SCRLBR
    #-----------------------------------------------#

    #-------------- mainFrame-config ---------------#
    def create_mainFrame(self):
        mainFrame = tk.Frame(self.mainCanvas)
      
        self.mainCanvas.create_window(
            (0, 0), 
            window=mainFrame, 
            anchor="nw"
            )
        
        mainFrame.bind(
            "<Configure>",
            lambda e: self.mainCanvas.configure(
            scrollregion=self.mainCanvas.bbox("all")
            )
        )
        
        # Scroll with mousewheel
        self.mainCanvas.bind_all(
            "<MouseWheel>", 
            lambda event: self.yview(
                'scroll', 
                int(-1*(event.delta/120)), 'units'
                )
            )

        return mainFrame

    # Checks if the content fits within the canvas.
    def yview(self, *args):
        if self.mainCanvas.yview() == (0.0, 1.0):
            return
        self.mainCanvas.yview(*args)
    #-----------------------------------------------#

    #----------------------- grid-config -----------------------#
    def grid_config(self):

        # window-grid
        self.master.grid_rowconfigure((1), weight=1)
        self.master.grid_columnconfigure((0), weight=1)

        # apexFrame-grid
        self.apexFrame.grid_rowconfigure((0), weight=1)
        self.apexFrame.grid_columnconfigure((1,2,3), weight=1)
        
        # masterFrame-grid
        self.masterFrame.grid_rowconfigure((1), weight=1)
        self.masterFrame.grid_columnconfigure((0), weight=1)

    #-----------------------------------------------------------#
    
    #------------------------------ splash-config ------------------------------#
    def create_splashScreen(self):
        self.splashFrame = ttk.Frame(self.masterFrame)
        self.splashFrame.grid(row=1)

        self.lbl_title = self.create_lbl_title(f'QUIZ')
        self.create_splashScreen_WIDGETS()

        self.start_BTN = tk.Button(self.splashFrame, 
                                   text='S T A R T  ᐅ', 
                                   font=BTN, 
                                   relief="flat",
                                   fg=WHITEV1, 
                                   bg=BLUEV1, 
                                   activeforeground=WHITEV2, 
                                   activebackground=BLUEV2,
                                   command=self.start)

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
        ssq_TAG.grid(row=3, column=1, columnspan=3)

        
        if self.mode == "student":
            ss_TAG = ttk.Label(
                self.splashFrame,
                text=f"START when you're ready, {self.student}.",
                font=TAG)
            ss_TAG.grid(row=4, column=1, columnspan=3)
        
        
        elif self.mode == "teacher":
            ss_TAG = ttk.Label(
                self.splashFrame,
                text=f"START viewing your quiz, {self.teacher}.",
                font=TAG)
            ss_TAG.grid(row=4, column=1, columnspan=3)
    

    def start(self):
        self.clearFrame(self.apexFrame)
        self.splashFrame.destroy()
        self.startQuiz()
    #--------------------------------------------------------------------------#
    
    #------------------------------------- title-config --------------------------------------#
    def create_lbl_title(self, title):
        lbl_title = tk.Label(self.apexFrame, text=title, font=TTL, fg=WHITEV1, bg=BLUEV1)
        lbl_title.grid(row=0, column=1, columnspan=3, ipady=18, sticky="EW")
        return lbl_title
    #-----------------------------------------------------------------------------------------#

    #------------------------------------ question-config ------------------------------------#
    def create_lbl_question_no(self, n):
        lbl_question_no = ttk.Label(self.mainFrame, text=f'{n+1}. ', font=QLBL)
        lbl_question_no.grid(row=1, column=1, padx=(80,0), pady=(70,20), sticky="NE")
        return lbl_question_no

    def create_lbl_question(self):
        lbl_question = ttk.Label(self.mainFrame, 
                                 text=f'{self.quesQuestion}', 
                                 font=QLBL, 
                                 wraplength=600)
        lbl_question.grid(row=1, column=2, columnspan=5, pady=(70,20), sticky="NWE")
        return lbl_question
    #-----------------------------------------------------------------------------------------#

    #------------------------------------- choice-config -------------------------------------#
    def create_choice_RDBTN(self, n):
        s = ttk.Style()
        s.configure('TRadiobutton', font=CLBL, wraplength=600, highlightthickness=0)
        rdbtn_choice = ttk.Radiobutton(self.mainFrame, 
                                      text=f'{self.quesChoice[n-1]}', 
                                      variable=self.choice_var, 
                                      value=self.quesChoice[n-1],
                                      style='TRadiobutton') 

        if n!=4:
            rdbtn_choice.grid(row=n+1, column=2, columnspan=3, pady=(10,0), sticky="W")
        else:
            rdbtn_choice.grid(row=n+1, column=2, columnspan=3, pady=(10,70), sticky="W")

        return rdbtn_choice


    def create_lbl_choice(self, n, choice):
        lbl_choice = ttk.Label(self.mainFrame, text=choice, font=CLBL, width=60)

        if self.mode == "student":
            if not(self.default_select_student_guess):
                if (lbl_choice['text'] == self.student_guessList[self.quesIndex]):
                    self.choice_var.set(lbl_choice['text'])
                    self.default_select_student_guess = True
                else:
                    self.choice_var.set("noGuess")

        return lbl_choice
    #-----------------------------------------------------------------------------------------#

    #-------------------------------------- button-config ------------------------------------------#
    ################################# button-next #################################
    def nextQues(self):
        if self.mode == "student":
            self.save_student_guess()
        self.quesIndex+=1
        self.startQuiz()
    

    def create_btn_next(self):
        btn_next = tk.Button(self.apexFrame, 
                             text=' > ', 
                             font=BTN, 
                             fg=WHITEV1, 
                             bg=BLUEV2, 
                             activeforeground=WHITEV2, 
                             activebackground=BLUEV1,
                             relief="flat", 
                             command=self.nextQues)

        btn_next.grid(row=0, column=3, padx=(0,20), pady=(28,0), sticky="NE")
        return btn_next
    ###############################################################################

    ################################# button-prev #################################
    def prevQues(self):
        if self.mode == "student":
            self.save_student_guess()
        self.quesIndex-=1
        self.startQuiz()


    def create_btn_prev(self):
        btn_prev = tk.Button(self.apexFrame, 
                             text=' < ', 
                             font=BTN, 
                             fg=WHITEV1, 
                             bg=BLUEV2, 
                             activeforeground=WHITEV2, 
                             activebackground=BLUEV1,
                             relief="flat",
                             command=self.prevQues)

        btn_prev.grid(row=0, column=1, padx=(20,0), pady=(28,0), sticky="NW")
        return btn_prev
    ###############################################################################
    
    ######################################## button-submit ########################################
    def submitQues(self):
        self.save_student_guess()
                
        UNGUESSED_noList = []
        for GUESS_index, GUESS in enumerate(self.student_guessList):

            if GUESS == "noGuess" or "":
                UNGUESSED_no = str(GUESS_index+1)
                if UNGUESSED_no not in UNGUESSED_noList:
                    UNGUESSED_noList.append(UNGUESSED_no)
            else:
                GUESSED_no = str(GUESS_index+1)
                if GUESSED_no in UNGUESSED_noList:
                    UNGUESSED_noList.remove(GUESSED_no)


        if UNGUESSED_noList != []:
            if len(UNGUESSED_noList) == 1:
                unguessed_MB = mb.askyesno(
                                title="WARNING! - Blank Question",
                                message=("It seems that Question {0} was left unanswered.\n"
                                        "Do you want to submit anyway?"
                                        ).format(UNGUESSED_noList[0]),
                                icon='warning')
            else:
                unguessed_MB = mb.askyesno(
                                title="WARNING! - Blank Question",
                                message=("It seems that Questions {0} were left unanswered.\n"
                                        "Do you want to submit anyway?"
                                        ).format(', '.join(UNGUESSED_noList)),
                                icon='warning')

            if unguessed_MB == True:
                self.getResult(len(UNGUESSED_noList))
                self.showResult()
                
                UNGUESSED_noList.clear()
                self.student_guessList.clear()
            
        else:
            subMB = mb.askyesno("SUBMIT", "Are you sure you want to submit now?")
            if subMB == True:
                self.getResult(blank=0)
                self.showResult()
                
                self.student_guessList.clear()



    def getResult(self, blank):

        for student_guess in self.student_guessList:
            student_guess_index = self.student_guessList.index(student_guess)
            if student_guess == self.quesAnswerList[student_guess_index]:
                self.correct+=1

        self.blank = blank
        self.wrong = self.quesData_size - self.correct - self.blank
        self.score = int(self.correct / self.quesData_size * 100)


        # get sData_lst
        sData = loadJSON(STUDENT_QUIZ_INFO_FILENAME)
        sDictList = sData[self.student]

        for sDict in sDictList:
            if sDict["Quiz Name"] == self.quizName and \
                sDict["ID"] == self.quizID:
                sDict["Quiz Score"] = str(self.score)+'%'
                sDict["Taken"] = True

        sData[self.student] = sDictList 
        writeJSON(sData, STUDENT_QUIZ_INFO_FILENAME)


    def showResult(self):
        self.apexFrame.destroy()
        self.masterFrame.destroy()
        self.master.title("Quizlyy - Results")

        self.mainCanvas.unbind_all("<MouseWheel>")

        result_background = tk.Canvas(self.master, bg=BLUEV1, highlightthickness=0)
        result_background.pack(expand=True, fill="both")
        result_foreground = tk.Frame(result_background, bg = "white")
        result_foreground.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

        titleLBL = tk.Label(result_foreground, text="Quiz Results", fg="black", bg="white", font=("Bahnschrift SemiBold", 38))
        titleLBL.place(relx=0.27,rely=0.08)

        style = ttk.Style(result_background)
        # style.theme_use('default')
        style.layout('text.darkblue.Horizontal.TProgressbar',
        [('Horizontal.Progressbar.trough',
        {'children': [('Horizontal.Progressbar.pbar',
                        {'side': 'left', 'sticky': 'ns'})],
        'sticky': 'nswe'}),
        ('Horizontal.Progressbar.label', {'sticky': ''})])
        style.configure('text.darkblue.Horizontal.TProgressbar', text = f"{self.score}%", font="Bahnschrift 20", background='#153060',foreground = 'black',thickness=30)

        bar = ttk.Progressbar(result_foreground, length=400, style='text.darkblue.Horizontal.TProgressbar', mode = 'determinate')
        bar['value'] = self.score
        bar.pack(pady=116)

        correctLBL = tk.Label(result_foreground, text=f"Correct : {self.correct}", fg="black", bg="white", font=("Bahnschrift", 16))
        correctLBL.place(relx=0.370,rely=0.45)
        wrongLBL = tk.Label(result_foreground, text=f"Wrong : {self.wrong}", fg="black", bg="white", font=("Bahnschrift", 16))
        wrongLBL.place(relx=0.385,rely=0.52)
        blankLBL = tk.Label(result_foreground, text=f"Blank : {self.blank}", fg="black", bg="white", font=("Bahnschrift", 16))
        blankLBL.place(relx=0.395,rely=0.592)
        scoreLBL = tk.Label(result_foreground, text=f" Total Score : {self.score}%", fg="black", bg="white", font=("Bahnschrift", 16))
        scoreLBL.place(relx=0.307,rely=0.664)
        
        def back():
            result_background.destroy()
            result_foreground.destroy()
            self.backOut()


        back_btn = tk.Button(
            result_foreground,
            text='⮐  B A C K',
            font=("Bahnschrift SemiBold", "12"),
            padx=5, pady=0,
            command=back, 
            bg=BLUEV1,
            fg='black', 
            relief="flat")

        back_btn.configure(width=42,activebackground=BLUEV2)
        back_btn.place(relx=0.19,rely=0.80)

    
    def create_btn_submit(self):
        btn_submit = tk.Button(self.apexFrame, 
                               text='S U B M I T', 
                               font=BTN, 
                               relief="flat",
                               fg=WHITEV1, 
                               bg=BLUEV2, 
                               activeforeground=WHITEV2, 
                               activebackground=BLUEV1,
                               command=self.submitQues)

        btn_submit.grid(row=0, column=3, padx=(0,66), pady=(28,0), sticky="NE")
        return btn_submit
    ###############################################################################################
    ######################################### button-edit #########################################
    def editQues(self):
        self.apexFrame.destroy()
        self.masterFrame.destroy()
        self.mainCanvas.unbind_all("<MouseWheel>")
        quizQCA.QCAForm(self.master, self.quiz, self.teacher, self.quesIndex)

    
    def create_btn_edit(self):
        btn_edit = tk.Button(self.apexFrame, 
                               text='E D I T  🖉', 
                               font=BTN, 
                               relief="flat",
                               fg=WHITEV1, 
                               bg=BLUEV2, 
                               activeforeground=WHITEV2, 
                               activebackground=BLUEV1,
                               command=self.editQues)

        btn_edit.grid(row=0, column=3, padx=(0,66), pady=(28,0), sticky="NE")
        return btn_edit
    ###############################################################################################
    ######################################## button-backout ########################################
    def backOut(self):
        self.apexFrame.destroy()
        self.masterFrame.destroy()


        if self.mode == "student":
            # get sData_lst
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

            mainPage.studentPage(self.master, self.student, DATA_LST)

        elif self.mode == "teacher":
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
    #############################################
    

    ####################### save_guess #######################
    def save_student_guess(self):
        student_guess = self.choice_var.get()
        self.student_guessList[self.quesIndex] = student_guess
    ##########################################################
    #------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------#