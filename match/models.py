from django.db import models
from django.utils import timezone
from stadium.models import Stadium


class Team(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="teams/", blank=True, null=True)
    achievements = models.TextField(blank=True)
    coach = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="players"
    )
    name = models.CharField(max_length=255)
    number = models.PositiveIntegerField()
    position = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    nationality = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="players/", blank=True, null=True)

    class Meta:
        ordering = ["team", "number"]
        unique_together = ["team", "number"]

    def __str__(self):
        return self.name


class Match(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        LIVE = "live", "Live"
        FINISHED = "finished", "Finished"
        CANCELED = "canceled", "Canceled"

    stadium = models.ForeignKey(
        Stadium,
        on_delete=models.CASCADE,
        related_name="matches"
    )
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches"
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches"
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()

    image = models.ImageField(upload_to="matches/", blank=True, null=True)
    video_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    live_minute = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING
    )

    def is_upcoming(self):
        return self.start_datetime > timezone.now()

    def is_live(self):
        return self.status == self.Status.LIVE

    def is_sold_out(self):
        return self.available_tickets == 0

    def reduce_available_tickets(self, count=1):
        if self.available_tickets >= count:
            self.available_tickets -= count
            self.save()

    def update_score(self, home_score, away_score):
        self.home_score = home_score
        self.away_score = away_score
        self.save()

    def mark_as_finished(self):
        self.status = self.Status.FINISHED
        self.save()

    def cancel_match(self):
        self.status = self.Status.CANCELED
        self.save()

    class Meta:
        ordering = ["-start_datetime"]

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

