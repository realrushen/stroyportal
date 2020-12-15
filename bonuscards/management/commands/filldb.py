from django.core. management.base import BaseCommand, CommandError
from bonuscards.models import BonusCard
from datetime import date, timedelta
from random import randint

def generate_card_series(i: int, length=4, size=10**2):
    return '{0:0>{length}}'.format(str(i // size), length=length)[:length]


def generate_card_number(i:int, length=8):
    return '{0:0>{length}}'.format(str(i), length=length)[:length]

def generate_release_date(i: int):
    if i % 10 == 0:
        return date.today() + timedelta(days=i // 2)
    else:
        return date.today()

def generate_use_date(i):
    if i % 10 == 0:
        return
    elif i % 5 == 0:
        return date.today() + timedelta(days=i + randint(6, 10))
    elif i % 2 == 0:
        return date.today() + timedelta(days=i + randint(1, 5))


class Command(BaseCommand):
    args = '<n_rows> default 1000'
    help = 'Fills database with random test data'
    def handle(self, *args, **options):
        n = int(args[0]) or 1000
        if isinstance(n, int) and n > 0:
            for i in range(n):
                try:
                    bonus_card = BonusCard.objects.create(
                        series=generate_card_series(i),
                        number=generate_card_number(i),
                        release_date=generate_release_date(i),
                        activity_expires_date=date.today() + timedelta(days=i - randint(0, i)),
                        use_date=generate_use_date(i),
                        amount=100 * (i + 1) - randint(0, 100),
                        activity_status=randint(1, 3),
                    )
                except Exception as e:
                    self.stderr.write(e, e.args)
                else:
                    bonus_card.save()
                    self.stdout.write('Successfully created %s object' % bonus_card)
        else:
            raise RuntimeError("'%s' must be int and > 0" % n)


