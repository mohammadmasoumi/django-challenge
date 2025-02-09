import uuid
from django.db import models


class Match(models.Model):
    """
    Represents a volleyball match scheduled at a stadium.
    """

    match_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    stadium = models.ForeignKey(
        "Stadium", on_delete=models.CASCADE, related_name="matches"
    )
    match_date = models.DateTimeField()
    team_host = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="matches_as_host"
    )
    team_guest = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="matches_as_guest"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team_host} vs {self.team_guest} at {self.stadium.name}"
