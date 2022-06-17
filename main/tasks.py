from celery import shared_task
from django.db import transaction

from main.models import Lesson


@shared_task
def add(x, y):
    return x + y


@shared_task
def lesson_save(name, section_id, file_name, file_chunks):
    with transaction.atomic():
        file_path = "media/" + file_name
        lesson = Lesson.objects.create(
            name=name,
            section_id=section_id,
        )
        with open(file_path, 'wb+') as f:
            for chunk in file_chunks.decode():
                f.write(chunk)
            f.close()
        lesson.file = file_name
        lesson.save()
        print('celery')
        return {"status": True}
