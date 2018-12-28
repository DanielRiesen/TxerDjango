import time
import threading
import calendar


class AnnouncementProcess():

    def __init__(self, thread_id, announcement, student_list, teacher_list, classes, debug=False, log=False):

        self.threadID = thread_id
        self.classes = classes
        self.teacher_list = teacher_list
        self.thread_id = thread_id
        self.errors = 0
        self.students = []
        self.announcement = announcement
        self.announcement_decoded = self.decode_announcement(announcement)
        self.end_time = 0
        self.student_list = student_list
        self.student_list_id = {student.student_id: student for student in student_list}
        self.debug = debug
        self.log = log
        self.finished = {}

    def __str__(self):
        return "Announcement Process: {}".format(self.threadID)

    def run(self):



        try:
            if self.announcement['assigneeMode'] == 'INDIVIDUAL_STUDENTS':
                for student_idd in self.announcement['individualStudentsOptions']['studentIds']:
                    if student_idd in self.student_list_id:
                        self.students.append(self.student_list_id[student_idd])

        except KeyError:  # In google is its not Individual assignment then they don't specify. This means all students
            self.student_list = self.students

        finished = self.update_tutorial(
            tutorial_id=self.announcement['id'],
            students=self.student_list,
            teachers=self.teacher_list,
            classes=self.classes,
            **self.announcement_decoded
        )

        self.end_time = time.time()
        self.finished = finished

    @staticmethod
    def decode_announcement(announcement):  # Turns Google API format to a dictionary

        announcement_decoded = {}

        # Splits text into lines and removes spaces
        text = [x.split(' ') for x in announcement['text'].split('\n')]
        for y in text:  # Iterates through the text lines testing for keywords
            if y[0] == 'Date:':
                announcement_decoded['Date'] = [x.replace(',', '') for x in y if x != 'Date:']

            elif y[0] == 'Start':
                announcement_decoded['Start_Time'] = y[2]
                try:
                    if y[3]:
                        announcement_decoded['am_pm'] = y[3]
                except IndexError:
                    pass

            elif y[0] == 'End':
                announcement_decoded['End_Time'] = y[2]
                try:
                    if y[3]:
                        announcement_decoded['am_pm_end'] = y[3]
                except IndexError:
                    pass

            elif y[0] == 'Student':
                announcement_decoded['Joinable'] = True

            elif y[0] == 'Minimum':
                announcement_decoded['MinStudent'] = y[2]

            elif y[0] == 'Max':
                announcement_decoded['MaxStudent'] = y[2]

            elif y[0] == 'Location:':
                announcement_decoded['Location'] = y[1]

            elif y[0] == 'Description:':
                announcement_decoded['Desc'] = "".join(x+" " for x in y[1:])

            elif y[0] == 'Made by:':
                announcement_decoded['Made'] = 'YES'

        return announcement_decoded

    def update_tutorial(self, **kwargs):
        months = {'January'  : 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
                  'September': 9, 'October': 10,
                  'November' : 11, 'December': 12}

        instance = {}


        for key, value in kwargs.items():
            if key not in ['students', 'teacher', 'Date', 'Start_Time', 'End_Time', 'classes', 'Made', 'am_pm',
                           'am_pm_end']:
                instance[key] = value

        instance['teachers'] = []
        instance['students'] = []
        instance['tutorial_id'] = 0

        for key, value in kwargs.items():
            if key == 'classes':
                instance['classes'] = value

            elif key == 'Made':
                self.errors += 1
                return False
            elif key == 'teachers':
                for x in value:
                    instance['teachers'].append(x)
            elif key == 'students':
                for x in value:
                    instance['students'].append(x)
            elif key == 'Date':
                to_add_start = 0
                to_add_end = 0

                if 'am_pm' in kwargs:
                    if kwargs['am_pm'] == 'pm':
                        to_add_start = 12
                        if (int(kwargs['Start_Time'].split(':')[0]) + 12) >= 24:
                            if (int(kwargs['Start_Time'].split(':')[0]) + 12) == 24:
                                kwargs['Start_Time'] = str(int(kwargs['Start_Time'].split(':')[0]) - 12) + ":" + str(
                                    int(kwargs['Start_Time'].split(':')[1])) + "0"

                if 'am_pm_end' in kwargs:

                    if kwargs['am_pm_end'] == 'pm':
                        to_add_end = 12
                        if (int(kwargs['End_Time'].split(':')[0]) + 12) >= 24:
                            if (int(kwargs['End_Time'].split(':')[0]) + 12) == 24:
                                kwargs['End_Time'] = int(kwargs['End_Time'].split(':')[0]) - 12 + int(
                                    kwargs['End_Time'].split(':')[1])
                try:
                    instance['Start_Time'] = '{}-{}-{} {}:{}'.format(int(kwargs['Date'][2]), months[kwargs['Date'][0]],
                                                                     int(kwargs['Date'][1]),
                                                                     int(kwargs['Start_Time'].split(':')[0])
                                                                     + to_add_start,
                                                                     int(kwargs['Start_Time'].split(':')[1]))

                    instance['End_Time'] = '{}-{}-{} {}:{}'.format(int(kwargs['Date'][2]), months[kwargs['Date'][0]],
                                                                   int(kwargs['Date'][1]),
                                                                   int(kwargs['End_Time'].split(':')[0]) + to_add_end,
                                                                   int(kwargs['End_Time'].split(':')[1]))
                except (IndexError, ValueError):
                    pass

        try:
            instance['Start_Time']
        except KeyError:
            return None

        return instance
