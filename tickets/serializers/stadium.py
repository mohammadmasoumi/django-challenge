from rest_framework import serializers
from tickets.models import Stadium, Seat


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = (
            "stadium_id",
            "name",
            "location",
            "capacity",
            "is_active",
            "created_at",
            "updated_at",
        )


class SeatSerializer(serializers.ModelSerializer):
    stadium = StadiumSerializer()

    class Meta:
        model = Seat
        fields = (
            "seat_id",
            "stadium",
            "seat_number",
            "section",
            "created_at",
            "updated_at",
        )
