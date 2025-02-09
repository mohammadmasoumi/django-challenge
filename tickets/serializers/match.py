from rest_framework import serializers
from tickets.models import Match
from tickets.serializers import TeamSerializer, StadiumSerializer


class MatchSerializer(serializers.ModelSerializer):
    team_host = TeamSerializer()
    team_guest = TeamSerializer()
    stadium = StadiumSerializer()

    class Meta:
        model = Match
        fields = (
            "match_id",
            "stadium",
            "match_date",
            "team_host",
            "team_guest",
            "created_at",
            "updated_at",
        )
