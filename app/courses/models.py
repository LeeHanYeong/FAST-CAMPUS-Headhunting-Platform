from django.db import models

__all__ = (
    'Course',
    'CoursePeriod',
)


class Course(models.Model):
    title = models.CharField('과정명', max_length=50)

    class Meta:
        verbose_name = '과정'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['title']

    def __str__(self):
        return self.title


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
        return f'{self.course.title} {self.title}'
