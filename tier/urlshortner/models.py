from django.db import models


class TierURL(models.Model):
    id = models.AutoField(primary_key=True)
    main_url = models.URLField(null=False, blank=False)
    short_url = models.URLField(unique=True, max_length=100, null=False, blank=False)

    def __str__(self):
        return " {} : {}".format(self.main_url, self.short_url)


class URLVisit(models.Model):
    id = models.AutoField(primary_key=True)
    tier_url = models.ForeignKey(TierURL, on_delete=models.CASCADE, related_name='urlvisits')
    visits = models.IntegerField()

    def __str__(self):
        return "{} : {}".format(self.tier_url.short_url, self.visits)

