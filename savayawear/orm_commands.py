import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "savayawear.settings")
django.setup()

from promo.models import PromoPeople, Question, Manager


def get_manager_telegram_id(speaker_fullname: str) -> str:
    speaker = Manager.objects.get(fullname=speaker_fullname)
    return speaker.telegram_id


def get_manager_by_telegam_id(user_id: str) -> Manager:
    manager = Manager.objects.get(telegram_id=user_id)
    return manager


if __name__ == '__main__':
    print(get_manager_by_telegam_id('709161558'))
