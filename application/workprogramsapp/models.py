from django.db import models
from dataprocessing.models import Items
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class FieldOfStudyWorkProgram(models.Model):
    '''
    Модель для связи направления и рабочей программы
    '''
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE, verbose_name = 'Образовательная программа')
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE, verbose_name = 'Рабочая программа')
    #competence = models.ForeignKey('Competence',null=True,  on_delete=models.CASCADE, verbose_name = 'Компетенции')

    class Meta:
        unique_together = ('work_program', 'field_of_study')


class WorkProgram(models.Model):
    '''
    Модель для рабочей программы
    '''
    PRIMARY_VOCATIONAL_EDUCATION = 'primary_vocational_education'
    SECONADARY_VOCATIONAL_EDUCATION = 'secondary_vocational_education'
    BACHELOR = 'bachelor'
    SPECIALIST = 'specialist'
    MASTER = 'master'
    QUALIFICATION_CHOICES = (
        (PRIMARY_VOCATIONAL_EDUCATION, 'Primary vocational education'),
        (SECONADARY_VOCATIONAL_EDUCATION, 'Secondary vocational education'),
        (BACHELOR, 'Bachelor'),
        (SPECIALIST, 'Specialist'),
        (MASTER, 'Master')
    )

    discipline_code = models.CharField(max_length=1024, blank=True, null=True)
    prerequisites = models.ManyToManyField(Items, related_name='WorkProgramPrerequisites',)
    qualification = models.CharField(choices=QUALIFICATION_CHOICES, max_length=1024, verbose_name = 'Квалификация', blank=True, null=True)
    prerequisites = models.ManyToManyField(Items, related_name='WorkProgramPrerequisites',
                                           through='PrerequisitesOfWorkProgram', blank=True, null=True, verbose_name = "Пререквизиты")
    outcomes = models.ManyToManyField(Items, related_name='WorkProgramOutcomes', through='OutcomesOfWorkProgram', verbose_name = "Постреквизиты")
    title = models.CharField(max_length=1024, verbose_name = "Название")
    hoursFirstSemester = models.IntegerField(blank=True, null=True, verbose_name = "Количество часов в 1 семестре")
    hoursSecondSemester = models.IntegerField(blank=True, null=True, verbose_name = "Количество часов в 2 семестре")
    #goals = models.CharField(max_length=1024, verbose_name = "Цели освоения" )
    #result_goals = models.CharField(max_length=1024, verbose_name = "Результаты освоения" )
    field_of_studies = models.ManyToManyField('FieldOfStudy', through=FieldOfStudyWorkProgram, verbose_name = "Предметная область")
    # list_of_references = models.TextField(blank=True, null=True)
    # guidelines = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class PrerequisitesOfWorkProgram(models.Model):
    '''
    Модель для пререквизитов рабочей программы
    '''
    # class Meta:
    #     auto_created = True

    item = models.ForeignKey(Items, on_delete=models.CASCADE, verbose_name ="Пререквизит" )
    workprogram = models.ForeignKey(WorkProgram, on_delete=models.CASCADE, verbose_name = "Рабочая программа")
    MasterylevelChoices = [
        ('1', 'low'),
        ('2', 'average'),
        ('3', 'high'),
    ]
    masterylevel = models.CharField(
        max_length=1,
        choices=MasterylevelChoices,
        default=1, verbose_name = "Уровень"
    )
    # def __str__(self):
    #     return self.item

class OutcomesOfWorkProgram(models.Model):
    '''
    Модель для результатов обучения по рабочей программе
    '''
    # class Meta:
    #     auto_created = True

    item = models.ForeignKey(Items, on_delete=models.CASCADE, verbose_name = "Постреквизит")
    workprogram = models.ForeignKey(WorkProgram, on_delete=models.CASCADE, verbose_name = "Рабочая программа" )
    MasterylevelChoices = [
        ('1', 'low'),
        ('2', 'average'),
        ('3', 'high'),
    ]
    masterylevel = models.CharField(
        max_length=1,
        choices=MasterylevelChoices,
        default=1, verbose_name = "Уровень"
    )

#
# class User(AbstractUser):
#     '''
#     Модель для пользователей
#     '''
#     first_name = models.CharField(max_length=1024)
#     last_name = models.CharField(max_length=1024)
#     patronymic = models.CharField(max_length=1024)
#     isu_number = models.CharField(max_length=1024)
#
#     def __str__(self):
#         return self.first_name + ' ' + self.last_name


class FieldOfStudy(models.Model):
    '''
    Модель для направлений
    '''
    PRIMARY_VOCATIONAL_EDUCATION = 'primary_vocational_education'
    SECONADARY_VOCATIONAL_EDUCATION = 'secondary_vocational_education'
    BACHELOR = 'bachelor'
    SPECIALIST = 'specialist'
    MASTER = 'master'
    QUALIFICATION_CHOICES = (
        (PRIMARY_VOCATIONAL_EDUCATION, 'Primary vocational education'),
        (SECONADARY_VOCATIONAL_EDUCATION, 'Secondary vocational education'),
        (BACHELOR, 'Bachelor'),
        (SPECIALIST, 'Specialist'),
        (MASTER, 'Master')
    )

    INTERNAL = 'internal'
    EXTRAMURAL = 'extramural'
    EDUCATION_FORM_CHOICES = (
        (INTERNAL, 'Internal'),
        (EXTRAMURAL, 'Extramural'),
    )
    number = models.CharField(unique=True, max_length=1024, verbose_name = 'Шифр ОП')
    title = models.CharField(unique=True, max_length=1024, verbose_name = 'Название ОП', blank = True, null = True)
    qualification = models.CharField(choices=QUALIFICATION_CHOICES, max_length=1024, verbose_name = 'Квалификация')
    educational_profile = models.CharField(unique=True, max_length=1024, verbose_name = 'Профиль ОП', blank = True, null = True)
    education_form = models.CharField(choices=EDUCATION_FORM_CHOICES, max_length=1024, verbose_name = 'Форма обучения')

    def __str__(self):
        return self.number


# class CompetenceIndicator(models.Model):
#     '''
#     Модель для связи компетенций и индикаторов
#     '''
#     competence = models.ForeignKey('Competence', on_delete=models.CASCADE)
#     indicator = models.ForeignKey('Indicator', on_delete=models.CASCADE)
#     #field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('competence', 'indicator')


class Competence(models.Model):
    '''
    Модель для компетенций
    '''
    number = models.CharField(unique=True, max_length=1024)
    name = models.CharField(unique=True, max_length=1024)
    field_of_study = models.ManyToManyField('FieldOfStudy')
    work_program = models.ManyToManyField('WorkProgram')
    # indicators = models.ManyToManyField('Indicator', through=CompetenceIndicator)

    def __str__(self):
        return self.name


class IndicatorWorkProgram(models.Model):
    '''
    Модель для связи рабочих программ и индикаторов
    '''
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE)
    indicator = models.ForeignKey('Indicator', on_delete=models.CASCADE)
    #competence = models.ForeignKey('Competence', on_delete=models.CASCADE)
    knowledge = models.CharField(max_length=1024)
    skills = models.CharField(max_length=1024)
    proficiency = models.CharField(max_length=1024)

    # class Meta:
    #     unique_together = ('competence', 'work_program', 'indicator')
    def __str__(self):
        return self.name


class Indicator(models.Model):
    '''
    Модель для индикаторов
    '''
    number = models.CharField(unique=True, max_length=1024)
    name = models.CharField(max_length=1024)
    work_programs = models.ManyToManyField('WorkProgram', through=IndicatorWorkProgram, blank=True, null=True)
    competence = models.ForeignKey('Competence', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EvaluationTool(models.Model):
    '''
    Модель для оценочных средств
    '''
    type = models.CharField(max_length=1024, verbose_name = "Тип оценочного средства")
    name = models.CharField(unique=True, max_length=1024, verbose_name = "Наименование оценочного средства")
    description = models.CharField(max_length=1024, verbose_name = "Описание", blank = True, null = True)
    check_point = models.BooleanField(verbose_name = "Контрольная точка", blank = True, null = True)
    deadline = models.IntegerField(verbose_name = "Срок сдачи в неделях", blank = True, null = True)
    min = models.IntegerField(verbose_name = "Максимальное значение", blank = True, null = True)
    max = models.IntegerField(verbose_name = "Минимальное значение", blank = True, null = True)


    def __str__(self):
        return self.name


class DisciplineSection(models.Model):
    '''
    Модель для разделов дисциплин
    '''

    ordinal_number = models.IntegerField(max_length=1024, verbose_name = "номер раздела")
    name = models.CharField(max_length=1024, verbose_name = "Раздел")
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE, verbose_name='Рабочая программа', related_name='discipline_sections')
    evaluation_tools = models.ManyToManyField('EvaluationTool', verbose_name='Фонды оценочных средств', blank = True, null = True, related_name='evaluation_tools')
    #description = models.CharField(max_length=1024, verbose_name = "Раздел", blank = True, null = True)
    contact_work = models.IntegerField(verbose_name = "Контактная работа", blank = True, null = True)
    lecture_classes = models.IntegerField(verbose_name = "Занятия лекционного типа", blank = True, null = True)
    laboratory = models.IntegerField(verbose_name = "Лабораторные занятия", blank = True, null = True)
    practical_lessons = models.IntegerField(verbose_name = "Практические занятия", blank = True, null = True)
    SRO = models.IntegerField(verbose_name = "СРО", blank = True, null = True)
    total_hours = models.IntegerField(verbose_name = "Всего часов", blank = True, null = True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['ordinal_number']


class Topic(models.Model):
    '''
    Модель для темы
    '''
    discipline_section = models.ForeignKey('DisciplineSection', on_delete=models.CASCADE, verbose_name = "Раздел", related_name = "topics")
    number = models.CharField(unique=True, max_length=1024, verbose_name = "Номер")
    description = models.CharField(max_length=1024, verbose_name = "Описание", blank = True, null = True)
    online_course = models.CharField(max_length=1024, verbose_name = "Реализация раздела дисциплины с помощью онлайн-курса", blank = True, null = True)

    def __str__(self):
        return (self.number + self.description)


class RouteComposition(models.Model):
    '''
    Модель для состава маршрутов (связь маршрутов и рабочих программ)
    '''
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('route', 'user', 'work_program')


class Route(models.Model):
    '''
    Модель для маршрутов
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    work_programs = models.ManyToManyField('WorkProgram', through=RouteComposition)


class Certification(models.Model):
    '''
    Модель для аттестации
    '''
    CERTIFICATION_TYPE_CHOICES = [
        ('EX', 'Exam'),
        ('DF', 'Differentiated classification'),
        ('OS', 'Offset'),
    ]
    type = models.CharField(choices = CERTIFICATION_TYPE_CHOICES, max_length=1024)
    semestr = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1024, verbose_name = "Описание", blank = True, null = True)
    deadline = models.IntegerField(verbose_name = "Срок сдачи в неделях", blank = True, null = True)
    work_program = models.ForeignKey('WorkProgram', on_delete=models.CASCADE, related_name='discipline_certification')