import argparse
import os
import random
import sys
from datetime import date

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from datacenter.models import (
    Schoolkid,
    Mark, Chastisement,
    Subject, Lesson,
    Commendation
)


commendations = (
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!'
)


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Правка успехов ученика'
    )

    parser.add_argument(
        'subject_name',
        type=str,
        help='Название предмета для похвалы')

    parser.add_argument(
        '--full_name',
        type=str,
        default='Фролов Иван',
        help='Имя ученика'
    )

    return parser.parse_args()


def find_kid(schoolkid):
    try:
        kid = Schoolkid.objects.get(full_name__contains=schoolkid)
    except Schoolkid.DoesNotExist:
        sys.exit('Нет такого ученика')
    except Schoolkid.MultipleObjectsReturned:
        sys.exit('Найдено несколько учеников')
    return kid


def fix_marks(kid):
    Mark.objects.filter(schoolkid=kid, points__lt=4).update(points=5)


def remove_chastisements(kid):
    Chastisement.objects.filter(schoolkid=kid).delete()


def get_subject(kid, arg_subject):
    try:
        subject = Subject.objects.get(
            title=arg_subject,
            year_of_study=kid.year_of_study
        )        
    except Subject.DoesNotExist:
        sys.exit('Нет такого предмета')
    return subject


def create_commendation(kid, subject, commendations, today):
    lesson = Lesson.objects.filter(
        year_of_study__contains=kid.year_of_study,
        group_letter__contains=kid.group_letter,
        subject=subject,
        date__lt=today
    ).order_by('-date').first()

    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=kid,
        subject=subject,
        teacher=lesson.teacher
    )


def limiting_commendation_number(kid):
    if Commendation.objects.filter(schoolkid=kid).count() > 15:
        (Commendation.objects
            .filter(schoolkid=kid)
            .order_by('created')
            .first()
            .delete())


if __name__ == '__main__':
    args = get_arguments()
    schoolkid = args.full_name
    arg_subject = args.subject_name
    kid = find_kid(schoolkid)
    today = date.today().strftime('%y-%m-%d')
    fix_marks(kid)
    remove_chastisements(kid)
    subject = get_subject(kid, arg_subject)
    create_commendation(kid, subject, commendations, today)
    limiting_commendation_number(kid)
