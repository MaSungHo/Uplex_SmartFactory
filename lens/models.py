from django.db import models

# Create your models here.
class Instance(models.Model):
    trt_lot_no = models.CharField(max_length=200)
    prt_lot_no = models.CharField(max_length=200)
    treat_mch_no = models.CharField(max_length=200)
    treat_trt_uptime = models.IntegerField()
    print_mch_no = models.CharField(max_length=200)
    print_prt_uptime = models.IntegerField()
    print_raw_mat = models.CharField(max_length=200)
    print_dry_no = models.CharField(max_length=200)
    print_heat_treat = models.CharField(max_length=200)
    print_prd_type = models.CharField(max_length=200)
    mold_snd_mch_no = models.CharField(max_length=200)
    mold_snd_uptime = models.IntegerField()
    mold_snd_raw_mat = models.CharField(max_length=200)
    mold_snd_dry_no = models.CharField(max_length=200)
    mold_snd_heat = models.CharField(max_length=200)
    material_cd_no = models.CharField(max_length=200)
    material_mat_nm = models.CharField(max_length=200)
    material_mat_emit_no = models.CharField(max_length=200)
