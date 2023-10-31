import quizTable


def studentPage(root, username, data):
    quizTable.StudentTable(root, username, data)

def teacherPage(root, username, data):
    quizTable.TeacherTable(root, username, data)