from django.db import models
# from django.contrib.auth.models import User


class ToDoList(models.Model):
    name = models.CharField(max_length=140)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class ToDoCategory(models.Model):
    name = models.CharField(max_length=140)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    bg_color = models.CharField(max_length=21, default="HASHffffff")
    text_color = models.CharField(max_length=21, default="HASH000000")
    bg_header_color = models.CharField(max_length=21, default="HASH000000")
    title_color = models.CharField(max_length=21, default="HASHffffff")
    all_classes = models.CharField(max_length=255, default="")
    header_classes = models.CharField(max_length=255, default="")
    box_classes = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name


class ToDo(models.Model):
    group = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    category = models.ForeignKey(ToDoCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description = models.TextField(max_length=500)
    priority = models.IntegerField(default=999)
    date = models.DateField(auto_now=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return '[' + self.category.name + ']' + self.title + ' - ' + self.group.name
