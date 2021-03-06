# Библиотеки для сариализации
from rest_framework import serializers, viewsets

# Модели данных

# --Работа с образовательной программой
from workprogramsapp.models import EducationalProgram, GeneralCharacteristics, Department, ProfessionalAreaOfGeneralCharacteristics,\
    ProfessionalStandard, PkCompetencesInGeneralCharacteristics

# Другие сериализаторы
from dataprocessing.serializers import userProfileSerializer
from workprogramsapp.serializers import CompetenceSerializer, ImplementationAcademicPlanSerializer


class EducationalProgramSerializer(serializers.ModelSerializer):
    """Сериализатор образовательной программы"""
    manager = userProfileSerializer()
    academic_plan_for_ep = ImplementationAcademicPlanSerializer()


    class Meta:
        model = EducationalProgram
        fields = "__all__"


class EducationalProgramUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор образовательной программы"""


    class Meta:
        model = EducationalProgram
        fields = "__all__"


class EducationalCreateProgramSerializer(serializers.ModelSerializer):
    """Сериализатор образовательной программы"""


    class Meta:
        model = EducationalProgram
        fields = ['qualification', 'manager', 'year_of_recruitment', 'academic_plan_for_ep']


class ProfessionalStandardSerializer(serializers.ModelSerializer):
    """Сериализатор образовательной программы"""


    class Meta:
        model = ProfessionalStandard
        fields = "__all__"


class ProfessionalAreaOfGeneralCharacteristicsSerializer(serializers.ModelSerializer):
    """Сериализатор образовательной программы"""
    professional_standard = ProfessionalStandardSerializer(many = True)


    class Meta:
        model = ProfessionalAreaOfGeneralCharacteristics
        fields = "__all__"


class PkCompetencesInGeneralCharacteristicsSerializer(serializers.ModelSerializer):
    """Сериализатор Компетенций"""
    competence = CompetenceSerializer()


    class Meta:
        model = PkCompetencesInGeneralCharacteristics
        fields = ['id','labor_functions', 'competence']


class GeneralCharacteristicsSerializer(serializers.ModelSerializer):
    """Сериализатор образовательной программы"""
    area_of_activity = ProfessionalAreaOfGeneralCharacteristicsSerializer(many = True)
    educational_program = EducationalProgramSerializer()
    ok_competences = CompetenceSerializer(many = True)
    kc_competences = CompetenceSerializer(many = True)
    pk_competences = PkCompetencesInGeneralCharacteristicsSerializer(source = 'pkcompetencesingeneralcharacteristics_set', many = True)
    np_competences = CompetenceSerializer(many = True)
    developers = userProfileSerializer(many = True)
    employers_representatives = userProfileSerializer(many = True)
    director_of_megafaculty = userProfileSerializer()
    dean_of_the_faculty = userProfileSerializer()
    scientific_supervisor_of_the_educational_program = userProfileSerializer()


    class Meta:
        model = GeneralCharacteristics
        fields = ['id', 'area_of_activity', 'educational_program', 'ok_competences', 'kc_competences', 'np_competences', 'pk_competences', 'developers', 'employers_representatives', 'director_of_megafaculty', 'dean_of_the_faculty', 'scientific_supervisor_of_the_educational_program',
                  'objects_of_activity', 'kinds_of_activity', 'tasks_of_activity', 'type_of_activity', 'annotation']


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор образовательной программы"""
    dean = userProfileSerializer()

    class Meta:
        model = Department
        fields = "__all__"
