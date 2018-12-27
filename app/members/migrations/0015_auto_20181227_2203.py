# Generated by Django 2.1.3 on 2018-12-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_auto_20181227_2126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyuserhirejobgroupwithapprovalstatus',
            options={'verbose_name': '채용희망직군(상태포함)', 'verbose_name_plural': '채용희망직군(상태포함) 목록'},
        ),
        migrations.AlterField(
            model_name='user',
            name='_hire_job_groups',
            field=models.ManyToManyField(blank=True, related_name='hire_company_user_set', related_query_name='hire_company_user', through='members.CompanyUserHireJobGroupWithApprovalStatus', to='courses.JobGroup', verbose_name='채용희망직군'),
        ),
    ]
