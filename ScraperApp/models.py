from django.db import models


class ScrapeData(models.Model):
    u_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=500)
    category = models.CharField(max_length=200)
    product_name = models.CharField(max_length=500, null=True)
    product_desc = models.TextField(null=True)
    price = models.CharField(max_length=200,null=True)
    rating = models.CharField(max_length=15, default=None, null=True)
    image = models.TextField(default=None, null=True)
    scraped_date = models.DateTimeField('date_scraped', auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    verbose = 'scrapedata'
