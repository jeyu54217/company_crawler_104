from django.db import models
from django.utils import timezone

class result_list(models.Model):
    company_id = models.CharField(
        max_length = 255, 
        blank = False, 
        null = True, 
        )
    company_name = models.CharField(
        max_length = 255, 
        blank = False, 
        null = False, 
        )
    company_profile = models.TextField(
        blank = True, 
        null = False, 
        )
    company_product = models.TextField(
        blank = True, 
        null = True, 
        )
    user_note = models.TextField(
        blank = True, 
        null = True, 
        default = "",
        )
    checked = models.BooleanField(
        default = False,
        )
class Company_info_gov(models.Model):
    tax_id = models.CharField(
        max_length = 255, 
        blank = False, 
        null = False, 
        )
    company_tax_name = models.CharField(
        max_length = 255, 
        blank = False, 
        null = False, 
        )
    company_address = models.CharField(
        max_length = 255,
        blank = True, 
        null = False, 
        )
    company_capital = models.CharField(
        max_length = 255,
        blank = True, 
        null = True, 
        )
  
class Company_info_closed(models.Model):
    not_open_id = models.CharField(
        max_length = 255, 
        blank = False, 
        null = False, 
        )
    not_open_name = models.CharField(
        max_length = 255, 
        blank = False, 
        null = False, 
        )

class RM_Confirmed(models.Model):
    RM_confirmed_id = models.CharField(
        max_length = 255, 
        blank = False, 
        null = False, 
        )
    RM_channel_chi_desc = models.CharField(
        max_length = 255, 
        blank = False, 
        null = False, 
        )