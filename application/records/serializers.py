from collections import defaultdict

from rest_framework import serializers

from dataprocessing.serializers import userProfileSerializer
from workprogramsapp.disciplineblockmodules.ze_module_logic import ze_cutter
from workprogramsapp.expertise.models import Expertise
from workprogramsapp.models import WorkProgram, WorkProgramInFieldOfStudy, AcademicPlan, ImplementationAcademicPlan, \
    EvaluationTool, DisciplineBlockModule
from workprogramsapp.serializers import PrerequisitesOfWorkProgramInWorkProgramSerializer, \
    OutcomesOfWorkProgramInWorkProgramSerializer
from workprogramsapp.workprogram_additions.models import StructuralUnit


class ImplementationAcademicPlanForStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImplementationAcademicPlan
        fields = ['id', 'ap_isu_id', 'year', 'title']


class WorkProgramDescriptionOnlySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, instance):
        try:
            return Expertise.objects.get(work_program=instance).expertise_status
        except Expertise.DoesNotExist:
            return "WK"

    class Meta:
        model = WorkProgram
        fields = ['id', 'discipline_code', 'title', 'description', 'status']


class WorkProgramEvaluationToolsStatSerializer(serializers.ModelSerializer):
    tools_counter = serializers.SerializerMethodField()

    def get_tools_counter(self, instance):
        types_dict = defaultdict(int)
        for eva in EvaluationTool.objects.filter(evaluation_tools__work_program=instance):
            types_dict[eva.type] += 1
        return types_dict

    class Meta:
        model = WorkProgram
        fields = ['id', 'discipline_code', 'title', 'tools_counter']


class WorkProgramDuplicatesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    count = serializers.IntegerField()
    work_programs = serializers.ListField()


class ShortAcademicPlan(serializers.ModelSerializer):
    """
    Cериализатор УП
    """

    class Meta:
        model = AcademicPlan
        fields = ["id", "educational_profile"]


class ShortStructuralUnitSerializerRecord(serializers.ModelSerializer):
    """
    Cериализатор подразделения разработчика РПД
    """

    class Meta:
        model = StructuralUnit
        fields = "__all__"


class WorkProgramSerializerForStatistic(serializers.ModelSerializer):
    editors = userProfileSerializer(many=True)

    class Meta:
        model = WorkProgram
        fields = ['id', 'title', 'discipline_code', "editors"]


class WorkProgramSerializerForStatisticExtended(serializers.ModelSerializer):
    editors = userProfileSerializer(many=True)
    academic_plans = serializers.SerializerMethodField()
    structural_unit = ShortStructuralUnitSerializerRecord(many=False)

    def get_academic_plans(self, instance):
        return AcademicPlansStatisticSerializer(
            instance=AcademicPlan.objects.filter(
                discipline_blocks_in_academic_plan__modules_in_discipline_block__change_blocks_of_work_programs_in_modules__work_program=instance.id),
            many=True).data

    class Meta:
        model = WorkProgram
        fields = ['id', 'title', "structural_unit", 'discipline_code', "editors", "academic_plans"]


class Meta:
    model = WorkProgram
    fields = ['id', 'title', 'discipline_code', "editors", "academic_plans"]


class WorkProgramInFieldOfStudySerializerForStatistic(serializers.ModelSerializer):
    work_program = WorkProgramSerializerForStatistic(many=False)

    class Meta:
        model = WorkProgramInFieldOfStudy
        fields = "__all__"


class StructuralUnitWithWpSerializer(serializers.ModelSerializer):
    workprogram_in_structural_unit = WorkProgramSerializerForStatistic(many=True)

    class Meta:
        model = StructuralUnit
        fields = ["id", "title", "workprogram_in_structural_unit"]


class SuperShortWorkProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkProgram
        fields = ['id', 'title', 'discipline_code']


class AcademicPlansStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicPlan
        fields = ['id', 'educational_profile', 'number', 'approval_date', 'year', 'education_form', 'qualification',
                  'author']


class RecordWorkProgramSerializer(serializers.ModelSerializer):
    # editors = userProfileSerializer(many=True)
    class Meta:
        model = WorkProgram
        fields = ['id', 'title', 'structural_unit', 'editors', 'language', 'discipline_sections',
                  'work_program_in_change_block']


class RecordAcademicPlanSerializer(serializers.ModelSerializer):
    print()

    class Meta:
        model = AcademicPlan
        fields = ['number']


class AcademicPlansDescriptionWpSerializer(serializers.ModelSerializer):
    wp_in_academic_plan = serializers.SerializerMethodField()
    academic_plan_in_field_of_study = ImplementationAcademicPlanForStatisticSerializer(many=True)

    def get_wp_in_academic_plan(self, instance):
        wp_all = WorkProgram.objects.none()
        for change in instance.get_all_changeblocks_from_ap():
            wp_all = wp_all | change.work_program.all()
        print(instance.id, len(wp_all))
        return WorkProgramDescriptionOnlySerializer(instance=wp_all.distinct(), many=True).data

    class Meta:
        model = AcademicPlan
        fields = ['id', 'academic_plan_in_field_of_study', 'wp_in_academic_plan', ]


class WorkProgramPrerequisitesAndOutcomesSerializer(serializers.ModelSerializer):
    prerequisites = PrerequisitesOfWorkProgramInWorkProgramSerializer(source='prerequisitesofworkprogram_set',
                                                                      many=True)
    outcomes = OutcomesOfWorkProgramInWorkProgramSerializer(source='outcomesofworkprogram_set', many=True)

    class Meta:
        model = WorkProgram
        fields = ['id', 'title', 'prerequisites', 'outcomes']


class ImplementationAcademicPlanWpStatisticSerializer(serializers.ModelSerializer):
    total_count_of_wp = serializers.SerializerMethodField()
    accepted_wp = serializers.SerializerMethodField()
    wp_on_expertise = serializers.SerializerMethodField()
    wp_with_editors = serializers.SerializerMethodField()

    def get_total_count_of_wp(self, obj):
        return WorkProgram.objects.filter(
            zuns_for_wp__work_program_change_in_discipline_block_module__discipline_block_module__descipline_block__academic_plan__academic_plan_in_field_of_study=obj).distinct().count()

    def get_accepted_wp(self, obj):
        return WorkProgram.objects.filter(
            zuns_for_wp__work_program_change_in_discipline_block_module__discipline_block_module__descipline_block__academic_plan__academic_plan_in_field_of_study=obj,
            expertise_with_rpd__expertise_status="AC").distinct().count()

    def get_wp_on_expertise(self, obj):
        return WorkProgram.objects.filter(
            zuns_for_wp__work_program_change_in_discipline_block_module__discipline_block_module__descipline_block__academic_plan__academic_plan_in_field_of_study=obj,
            expertise_with_rpd__expertise_status__in=["WK", "EX"]).distinct().count()

    def get_wp_with_editors(self, obj):
        return WorkProgram.objects.filter(
            zuns_for_wp__work_program_change_in_discipline_block_module__discipline_block_module__descipline_block__academic_plan__academic_plan_in_field_of_study=obj,
            editors__isnull=False).distinct().count()

    class Meta:
        model = ImplementationAcademicPlan
        fields = ['academic_plan', 'title', 'year', 'total_count_of_wp', 'wp_with_editors', 'accepted_wp',
                  'wp_on_expertise']


class AcademicPlanRealisedInYearSerializer(serializers.ModelSerializer):
    work_programs = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ImplementationAcademicPlan.objects.get(academic_plan=instance).title

    def get_work_programs(self, instance):
        request = self.context['request']
        year_of_sending = int(request.query_params.get("year").split("/")[0])
        plan_year = ImplementationAcademicPlan.objects.get(academic_plan=instance).year
        wps = []
        for changeblock in instance.get_all_changeblocks_from_ap():
            semester_start = changeblock.semester_start
            if not semester_start:
                try:
                    ze_list = changeblock.credit_units.split(", ")
                    for i, el in enumerate(ze_list):
                        if int(el) != 0:
                            semester_start = [i + 1]
                            break
                except IndexError:
                    semester_start = []
                except AttributeError:
                    semester_start = []
            for wp in changeblock.work_program.all():
                try:
                    #print(wp.ze_v_sem, wp.title)
                    ze_v_sem = [int(unit) for unit in wp.ze_v_sem.split(", ")]
                    duration = len([el for el in ze_v_sem if el != 0])
                except TypeError:
                    continue
                except AttributeError:
                    continue
                for sem in semester_start:
                    sem = sem-1
                    if plan_year + sem // 2 <= year_of_sending <= plan_year + (sem + duration-1) // 2:
                        wps.append(SuperShortWorkProgramSerializer(instance=wp, ).data)
        return wps

    """def get_work_programs(self, instance):
        request = self.context['request']
        year_of_sending = request.query_params.get("year").split("/")[0]
        object_list = None
        wps_list = WorkProgram.objects.filter(
            work_program_in_change_block__discipline_block_module__descipline_block__academic_plan=instance)

        for now_semester in range(12):
            many_term_regex = r""
            for i in range(12):
                if i == now_semester:
                    many_term_regex += "(([^0]\.[0-9])|([^0])),\s"
                else:
                    many_term_regex += "(([0-9]\.[0-9])|[0-9]),\s"
            many_term_regex = many_term_regex[:-3]
            wp_for_year = wps_list.filter(
                work_program_in_change_block__discipline_block_module__descipline_block__academic_plan__academic_plan_in_field_of_study__year=int(
                    year_of_sending) - now_semester // 2,
                zuns_for_wp__zuns_for_wp__ze_v_sem__iregex=many_term_regex)
            if object_list:
                object_list = object_list | wp_for_year
            else:
                object_list = wp_for_year
        object_list=object_list.distinct()
        return SuperShortWorkProgramSerializer(instance=object_list, many=True).data"""

    class Meta:
        model = AcademicPlan
        fields = ['id', 'ap_isu_id', 'title', 'work_programs', ]


class ModulesWithoutRulesSerializer(serializers.ModelSerializer):
    #editors = userProfileSerializer(many=True)

    class Meta:
        model = DisciplineBlockModule
        fields = ['id', 'name', 'editors']
