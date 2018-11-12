import Tutorials.models as tutorial_models
from TxerAPI.Shortcuts.shortcuts import *
from Txer.models import *
import random
import string


def register_or_update_class(teachers, students, class_id, class_url, name):  # Should be given as list of model instances
    instance, created = tutorial_models.Classes.objects.get_or_create(class_id=class_id)
    instance.teacher.clear()
    instance.students.clear()
    for teacher in teachers:
        instance.teacher.add(teacher)
    for student in students:
        instance.students.add(student)
    instance.class_id = class_id
    instance.url = class_url
    instance.name = name
    instance.teacher_name = instance.teacher.first().username
    print(instance)
    instance.save()


def get_student_list(lst, model):
    product = []
    try:
        for userr in lst['students']:
            try:
                product.append(model.objects.get(student_id=userr['profile']['id']))
            except model.DoesNotExist:
                pass
        return product
    except:
        return []


def get_teacher_list(lst, model):
    product = []
    for userr in lst['teachers']:
        try:
            product.append(model.objects.get(student_id=userr['profile']['id']))
        except model.DoesNotExist:
            pass
    return product


def update_tutorial(**kwargs):
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10,
              'November': 11, 'December': 12}
    temp_kwargs = {}
    for key, value in kwargs.items():
        if key not in ['students', 'teacher', 'Date', 'Start_Time', 'End_Time', 'classes', 'Made']:
            temp_kwargs[key] = value
    Tutorial.objects.filter(tutorial_id=kwargs['tutorial_id']).delete()
    instance, _ = Tutorial.objects.get_or_create(**temp_kwargs)
    for key, value in kwargs.items():
        if key == 'classes':
            for x in value:
                instance.classes.add(x)
        elif key == 'Made':
            return 1
        elif key == 'teacher':
            for x in value:
                instance.teacher.add(x)
        elif key == 'students':
            for x in value:
                instance.students.add(x)
        elif key == 'Date':
            instance.Start_Time = '{}-{}-{} {}:{}'.format(int(kwargs['Date'][2]), months[kwargs['Date'][0]],
                                                          int(kwargs['Date'][1]),
                                                          int(kwargs['Start_Time'].split(':')[0]),
                                                          int(kwargs['Start_Time'].split(':')[1]))
            instance.End_Time = '{}-{}-{} {}:{}'.format(int(kwargs['Date'][2]), months[kwargs['Date'][0]],
                                                        int(kwargs['Date'][1]), int(kwargs['End_Time'].split(':')[0]),
                                                        int(kwargs['End_Time'].split(':')[1]))

    instance.save()


def decode_announcement(announcement):
    announcement_decoded = {}
    text = announcement['text']
    text = text.split('\n')
    text = [x.split(' ') for x in text]
    for y in text:
        if y[0] == 'Date:':
            announcement_decoded['Date'] = [x.replace(',', '') for x in y if x != 'Date:']
        elif y[0] == 'Start':
            announcement_decoded['Start_Time'] = y[2]
        elif y[0] == 'End':
            announcement_decoded['End_Time'] = y[2]
        elif y[0] == 'Student':
            announcement_decoded['Joinable'] = True
        elif y[0] == 'Minimum':
            announcement_decoded['MinStudent'] = y[2]
        elif y[0] == 'Max':
            announcement_decoded['MaxStudent'] = y[2]
        elif y[0] == 'Location:':
            announcement_decoded['Location'] = y[1]
        elif y[0] == 'Description:':
            announcement_decoded['Desc'] = ''.join([x + ' ' for x in y[1:]])
        elif y[0] == 'Made by:':
            announcement_decoded['Made'] = 'YES'
    return announcement_decoded


def check_announcements_and_update(requesting_classes_id, requesting_teacher):
    api = build_classroom_api(requesting_teacher)
    for requesting_class in requesting_classes_id:
        for announcement in api.courses().announcements().list(courseId=requesting_class).execute()['announcements']:
            try:
                student_list = []
                announcement_decoded = decode_announcement(announcement)
                if announcement['assigneeMode'] == 'INDIVIDUAL_STUDENTS':
                    for student_idd in announcement['individualStudentsOptions']['studentIds']:
                        try:
                            student_list.append(UserProfile.objects.get(student_id=student_idd))
                        except:
                            pass
                else:
                    student_list = Classes.objects.get(class_id=requesting_class).students.all()
                update_tutorial(
                    tutorial_id=announcement['id'],
                    students=student_list,
                    teacher=UserProfile.objects.filter(user=requesting_teacher.user),
                    classes=Classes.objects.filter(class_id=requesting_class),
                    **announcement_decoded
                )
            except:
                pass


def create_announcement(requesting_class_id, requesting_teachcer, data):
    old_months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May':5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10,
              'November': 11, 'December': 12}
    months = {}
    for key, value in old_months.items():
        months[value] = key

    teacher_cred = CredentialModel.objects.get(user=requesting_teachcer)
    classroom = build_classroom_api(teacher_cred)
    text = "Tutorial\n\n"
    do_not_display = ['csrfmiddlewaretoken', 'students', 'course', 'token', 'min_students', 'joinable', 'max_students']
    translate = {
        'desc': 'Description: ',
        'start_time': 'Start Time: ',
        'end_time': 'End Time: ',
        'location': 'Location: ',
        'date': 'Date: ',
        'mandatory': 'Mandatory: ',
        'off': 'No',
        'on': 'Yes',
        'Made By': 'Made By: ',
        }
    for key, value in data.items():
        if key in do_not_display:
            pass
        elif key == 'mandatory':
            text += translate[key] + str(translate[value[0]]) + '\n'
        elif key == 'date':
            value_split = value[0].split('/')
            text += translate[key] + '{} {}, {}'.format(months[int(value_split[1])], value_split[2], value_split[0]) + '\n'
        else:
            text += translate[key] + str(value[0]) + '\n'

    students = []

    cur_class = Classes.objects.get(class_id=requesting_class_id).students.all()
    for x in cur_class:
        if x.student_id in data['students']:
            students.append(x.student_id)

    classroom.courses().announcements().create(body={"text": text, "assigneeMode": "INDIVIDUAL_STUDENTS", "individualStudentsOptions": {"studentIds": students}}, courseId=requesting_class_id).execute()

    return '200'
