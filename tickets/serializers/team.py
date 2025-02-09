from rest_framework import serializers
from tickets.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "team_id",
            "name",
            "code",
            "created_at",
            "updated_at",
        )
