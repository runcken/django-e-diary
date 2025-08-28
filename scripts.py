import argparse
import os
import random
import sys
from datetime import date, timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from datacenter.models import Schoolkid, Mark, Chastisement
from datacenter.models import Subject, Lesson, Commendation


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
    'Очень хороший ответ!,'
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!'
)


def get_argument():
    parser = argparse.ArgumentParser(
        description='Правка успехов ученика'
    )

    parser.add_argument(
        '--full_name',
        type=str,
        default='Фролов Иван',
        help='Имя ученика'
    )

    args = parser.parse_args()
    kid_name = args.full_name
    return kid_name


def find_kid(schoolkid):
    try:
        kid = Schoolkid.objects.get(full_name__contains=schoolkid)
    except Schoolkid.DoesNotExist:
        sys.exit('Нет такого ученика')
    except Schoolkid.MultipleObjectsReturned:
        sys.exit('Найдено несколько учеников')
    return kid


def fix_marks(kid):
    kid_marks = Mark.objects.filter(schoolkid=kid, points__lt=4)
    for kid_mark in kid_marks:
        kid_mark.points = 5
        kid_mark.save()


def remove_chastisements(kid):
    kid_reprovals = Chastisement.objects.filter(schoolkid=kid)
    for kid_reproval in kid_reprovals:
        kid_reproval.delete()


def create_commendation(kid, subject, commendations, today, find_lesson_days):
    for day in range(find_lesson_days):
        find_lesson_date = (today - timedelta(days=day)).strftime('%Y-%m-%d')
        lesson = Lesson.objects.filter(
            year_of_study__contains=kid.year_of_study,
            group_letter__contains=kid.group_letter,
            subject=subject,
            date=find_lesson_date
        )
        if lesson.exists():
            found_lesson = lesson.first()
            break

    if not found_lesson:
        return

    Commendation.objects.create(
        text=random.choice(commendations),
        created=found_lesson.date,
        schoolkid=kid,
        subject=subject,
        teacher=found_lesson.teacher
    )


def limiting_commendation_number(kid):
    if Commendation.objects.filter(schoolkid=kid).count() > 15:
        (Commendation.objects
            .filter(schoolkid=kid)
            .order_by('created')
            .first()
            .delete())


if __name__ == '__main__':
    schoolkid = get_argument()
    kid = find_kid(schoolkid)
    subject = random.choice(
        Subject.objects.filter(year_of_study=kid.year_of_study)
        )
    today = date.today().strftime('%y-%m-%d')
    find_lesson_days = 14
    found_lesson = None
    fix_marks(kid)
    remove_chastisements(kid)
    create_commendation(kid, subject, commendations, today, find_lesson_days)
    limiting_commendation_number(kid)
