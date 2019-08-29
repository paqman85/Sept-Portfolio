from django.db import models


class Subscriber(models.Model):
    """A Subscriber model"""

    full_name = models.CharField(max_length=200, blank = False, null=False , help_text="Full Name")
    email= models.CharField(blank=False, null=False, max_length = 200, help_text="Email Address")
    

    def __str__(self):
        """string representation of this object"""
        return self.full_name

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"