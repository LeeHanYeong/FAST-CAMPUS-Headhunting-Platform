from django.db import models

__all__ = (
    'JobCategory',
    'JobGroup',
    'Course',
    'CoursePeriod',
)


class JobCategory(models.Model):
    title = models.CharField('분야명', max_length=100, db_index=True)

    class Meta:
        verbose_name = '분야'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.title


class JobGroup(models.Model):
    category = models.ForeignKey(
        JobCategory, on_delete=models.CASCADE, related_name='group_set', verbose_name='분야')
    title = models.CharField('직군명', max_length=100, db_index=True)

    class Meta:
        ordering = ('category__title', 'title')
        verbose_name = '직군'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return f'{self.category.title} - {self.title}'


class Course(models.Model):
    group = models.ForeignKey(
        JobGroup, on_delete=models.CASCADE, related_name='course_set', verbose_name='직군')
    title = models.CharField('과정명', max_length=50)

    class Meta:
        verbose_name = '과정'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['title']

    def __str__(self):
        return f'{self.group.category.title} - {self.group.title} - {self.title}'


class CoursePeriod(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        verbose_name='과정', related_name='periods',
    )
    title = models.CharField('기수명', max_length=30)

    class Meta:
        verbose_name = '과정 기수'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['course__title', 'title']

    def __str__(self):
        return (f'{self.course.group.category.title} - '
                f'{self.course.group.title} - '
                f'{self.course.title} - '
                f'{self.title}')
