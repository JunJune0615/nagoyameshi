from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Category(models.Model):
    category_name = models.CharField(verbose_name="カテゴリ名",max_length=200)
    create_date = models.DateField(verbose_name="作成日時", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    def __str__(self):
        return self.category_name


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Restaurant(models.Model):
    restaurant_name = models.CharField(verbose_name="店舗名", max_length=200)
    budget = models.PositiveIntegerField(verbose_name="予算")
    information = models.TextField(verbose_name="店舗説明")
    img = models.ImageField(verbose_name="店舗画像" , blank=True, null=True)
    create_date = models.DateField(verbose_name="作成日時", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    postal_number = models.CharField(verbose_name="郵便番号", max_length=100, null=True, blank=True)
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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='名前', max_length=100)
    email = models.CharField(verbose_name='メールアドレス', unique=True, max_length=100)
    password = models.CharField(verbose_name='パスワード', max_length=100)
    vip_member = models.BooleanField("有料会員ステータス", default=False)
    create_date = models.DateField(verbose_name="作成日時", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_card_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    #AbstractBaseUserにはMyUserManagerが必要
    objects = MyUserManager()

    #一意の識別子として使用されます
    USERNAME_FIELD = 'email'
    #ユーザーを作成するときにプロンプ​​トに表示されるフィールド名のリストです。
    REQUIRED_FIELDS = ['username']

    
class Review(models.Model):
    review = models.TextField(verbose_name="店舗レビュー")
    create_date = models.DateField(verbose_name="作成日時", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('restaurant', 'user')


class FavoriteRestaurant(models.Model):
    create_date = models.DateField(verbose_name="作成日時", auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('restaurant', 'user')

