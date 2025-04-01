from rest_framework import serializers
from .models import Job, JobApplication, Candidate

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category', 'job_type',
            'job_level', 'experience', 'qualification', 'gender',
            'min_salary', 'max_salary', 'address', 'country', 'city',
            'contact', 'location', 'required_skills', 'expired_date',
            'posted_date', 'status'
        ]
        read_only_fields = ['posted_date', 'id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert choice fields to their display values
        representation['category'] = instance.get_category_display()
        representation['job_type'] = instance.get_job_type_display()
        representation['job_level'] = instance.get_job_level_display()
        representation['experience'] = instance.get_experience_display()
        representation['qualification'] = instance.get_qualification_display()
        representation['gender'] = instance.get_gender_display()
        representation['status'] = instance.get_status_display()
        return representation

class JobApplicationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = [
            'id', 'full_name', 'email', 'phone', 'position_applied',
            'resume', 'resume_url', 'cover_letter', 'status', 'status_display',
            'applied_on'
        ]
        read_only_fields = ['applied_on', 'status']

    def get_resume_url(self, obj):
        if obj.resume:
            return self.context['request'].build_absolute_uri(obj.resume.url)
        return None

class CandidateSerializer(serializers.ModelSerializer):
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            'id', 'cand_id', 'name', 'email', 'phone',
            'applied_role', 'applied_date', 'resume', 'resume_url',
            'status'
        ]
        read_only_fields = ['cand_id']

    def get_resume_url(self, obj):
        if obj.resume:
            return self.context['request'].build_absolute_uri(obj.resume.url)
        return None 