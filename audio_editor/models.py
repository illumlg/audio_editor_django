from django.db import models


class Request(models.Model):
    date = models.DateTimeField('date sent')
    name = models.CharField(max_length=200, default='name')
    status = models.CharField(max_length=200, default='status')
    status_code = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default='description')
    params = models.CharField(max_length=200, default='params')

    def __str__(self):
        return ', '.join([str(self.date), self.name, self.status, str(self.status_code), self.description, self.params])
