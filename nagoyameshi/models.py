from django.db import models
from django.utils import timezone

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    create_date = models.DateField(verbose_name="作成日時", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.category_name

    
class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200,verbose_name="店舗名")
    budget = models.PositiveIntegerField(verbose_name="予算")
    information = models.TextField(verbose_name="店舗説明")
    img = models.ImageField(verbose_name="店舗画像" , blank=True, default='noImage.png')
    create_date = models.DateField(verbose_name="作成日時", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    address = models.CharField(verbose_name="住所", max_length=100, null=True, blank=True)
    tel = models.CharField(verbose_name="電話番号", max_length=100, null=True, blank=True)
    open_time = models.TimeField(verbose_name="開店時間", default="09:00:00")
    close_time = models.TimeField(verbose_name="閉店時間", default="21:00:00")
    closed_monday = models.BooleanField(verbose_name="月曜定休", default=False)
    closed_tuesday = models.BooleanField(verbose_name="火曜定休", default=False)
    closed_wednesday = models.BooleanField(verbose_name="水曜定休", default=False)
    closed_thursday = models.BooleanField(verbose_name="木曜定休", default=False)
    closed_friday = models.BooleanField(verbose_name="金曜定休", default=False)
    closed_saturday = models.BooleanField(verbose_name="土曜定休", default=False)
    closed_sunday = models.BooleanField(verbose_name="日曜定休", default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_closed_days(self):
        days = []
        if self.closed_monday:
            days.append("月曜")
        if self.closed_tuesday:
            days.append("火曜")
        if self.closed_wednesday:
            days.append("水曜")
        if self.closed_thursday:
            days.append("木曜")
        if self.closed_friday:
            days.append("金曜")
        if self.closed_saturday:
            days.append("土曜")
        if self.closed_sunday:
            days.append("日曜")
        return ", ".join(days) if days else "なし"
    
    def get_businesshour(self):
        return  f"{self.open_time}～{self.close_time}" 
    

    def __str__(self):
        return self.restaurant_name

