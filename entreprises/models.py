from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import datetime


class Entreprise(models.Model):
    name = models.CharField(max_length=50)  # The longest name found is 38
    # There are 5 unique sector in the intial 1000 data. I added OTHER as a choice
    # The sector classe represents the choices that the field sector can have
    class Sector(models.TextChoices):
        SERVICES = "Services"
        ELECTRONIC = "Electronic"
        ENERGY = "Energy"
        LUXURY = "Luxury"
        RETAIL = "Retail"
        OTHER = "Other"

    sector = models.CharField(
        help_text="Choice (Services, Electronic, Energy, Luxury, Retail or Other)",
        max_length=10,
        choices=Sector.choices,
        default=Sector.OTHER,
    )
    # SIREN(système d'identification du répertoire des entreprises)a 9 digit id
    siren = models.CharField(
        help_text="A unique number of 9 digits",
        max_length=9,
        unique=True,
        validators=[RegexValidator(r"^\d{9}$", message="SIREN must have 9 digits")],
    )

    def __str__(self):
        return "{self.name}_{self.siren}".format(self=self)


class Result(models.Model):
    ca = models.PositiveIntegerField(help_text="Capital")
    margin = models.IntegerField()
    ebitda = models.IntegerField(
        help_text="EBITDA (Earnings before interest, taxes, depreciation, and amortization)"
    )
    loss = models.IntegerField()
    year = models.PositiveIntegerField()
    entreprise = models.ForeignKey(
        Entreprise,
        related_name="results",
        on_delete=models.CASCADE,
    )

    class Meta:
        # Adding constraints on years. No entreprise with duplicate years
        # Years must not be older than 1980 or greater than current year
        constraints = [
            models.UniqueConstraint(
                fields=["entreprise", "year"], name="unique_year_result"
            ),
            models.CheckConstraint(
                check=models.Q(year__lte=datetime.date.today().year),
                name="year_lte_now",
            ),
            models.CheckConstraint(
                check=models.Q(year__gte=1980), name="year_gte_1980"
            ),
        ]

    def __str__(self):
        return "{self.entreprise}_{self.year}".format(self=self)
