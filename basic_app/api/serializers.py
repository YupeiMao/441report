from rest_framework import serializers
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rid', 'cid', 'pid','date','summary','pros','cons','advices_to_management','overall_ratings','work_balance_stars','culture_values_stars','career_opportunities_stars','company_benefit_stars','senior_management_stars','helpful_count')
