import json

from django.db import models
from django.db.models.query_utils import Q

from .utils import serialize_to_json



class BonusCardSearchManager(models.Manager):
    """
    Кастомныйм енеджер реализовывает поиск бонусных карт
    """
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
    Бонусная карта
    """
    objects = models.Manager()
    search_objects = BonusCardSearchManager()
    serialization_fields = (
            'series', 
            'number', 
            'release_date', 
            'activity_expires_date', 
            'activity_status'
    )
    
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


    class Meta:
        ordering = ['release_date']
        verbose_name_plural = "Бонусные карты"


    def __str__(self):
        return '{0} {1}'.format(self.series, self.number)
    

    def as_dict(self):
        """
        Не нашел хорошей замены JsonRespose, поэтому пришлось добавить костыль
        """
        return json.loads(serialize_to_json([self], type(self).serialization_fields))
            
        

  


