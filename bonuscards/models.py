from django.db import models
from django.db.models.query_utils import Q



class BonusCardSearchManager(models.Manager):
    search_fields = {
        'number': '__contains',
        'series': '__contains',
        'release_date': '',
        'activity_expires_date': '',
        'activity_status': '',
    }

    def search(self, search_query):
        q = []
        for search_param in search_query.keys():
            if self.search_fields.get(search_param):
                param = {'{}{}'.format(search_param, self.search_fields[search_param]):search_query[search_param]}
                q.append(Q(**param))
        if q:
            return self.get_queryset().filter(*q)
        else:
            return self.get_queryset().all()



class BonusCard(models.Model):
    """
     Бонусные карты
     Поля:
     - серия карты
     - номер карты
     - дата выпуска карты
     - дата окончания активности карты
     - дата использования
     - сумма
     - статус карты (не активирована/активирована/просрочена).

     Функционал приложения:
      1. список карт с полями: серия, номер, дата выпуска, дата окончания активности, статус
      2. создание карты
      3. поиск по этим же полям
      4. удаление карты
    """
    NOT_ACTIVE = 1
    ACTIVE = 2
    EXPIRED = 3

    STATUS = (
        (NOT_ACTIVE, 'не активирована'),
        (ACTIVE, 'активирована'),
        (EXPIRED, 'просрочена'),
    )

    series = models.CharField(max_length=4, verbose_name='Cерия')
    number = models.CharField(max_length=12, verbose_name='Номер', unique=True)
    release_date = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата выпуска')
    activity_expires_date = models.DateField(db_index=True, verbose_name='Дата окончания активности', )
    use_date = models.DateField(verbose_name='Дата использования', null=True, blank=True)
    amount = models.IntegerField(verbose_name='Cумма баллов', default=0)
    activity_status = models.PositiveSmallIntegerField(
        db_index=True,
        choices=STATUS, 
        default=NOT_ACTIVE, 
        verbose_name='Статус'
    )

    objects = models.Manager()
    search_objects = BonusCardSearchManager()

    class Meta:
        ordering = ['release_date']
        verbose_name_plural = "Бонусные карты"


    def __str__(self):
        return '{0} {1}'.format(self.series, self.number)

  


