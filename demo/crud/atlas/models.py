from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Ocean(models.Model):
    """Geographic ocean data model."""

    name = models.CharField(
        _("name"),
        max_length=250,
        primary_key=True,
        help_text=_("Ocean name"),
    )
    area = models.BigIntegerField(
        _("area"),
        help_text=mark_safe(_("Area in km²")),
        validators=[MinValueValidator(1)],
    )
    slug = models.SlugField(
        _("slug"),
        help_text=_("URL-friendly identifier"),
    )
    description = models.TextField(
        _("description"),
        help_text=_("Description of the ocean"),
    )
    map_url = models.URLField(
        _("map url"),
        help_text=_("URL to a map of the ocean"),
    )

    class Meta:
        verbose_name = _("ocean")
        verbose_name_plural = _("oceans")
        ordering = ["name"]

    def __str__(self):
        return self.name if self.name is not None else "Ocean"

    @property
    def formatted_area(self):
        """Format area with thousands separator."""
        return f"{self.area:,} km²"

    # formatted_area.short_description = _("Formatted Area")


class Sea(models.Model):
    """Geographic sea data model with hierarchical relationships."""

    name = models.CharField(
        _("name"),
        max_length=250,
        help_text=_("Sea name"),
    )
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        verbose_name=_("parent"),
        on_delete=models.CASCADE,
        help_text=_("Parent sea if this is a sub-sea"),
        related_name="child_seas",
    )
    ocean = models.ForeignKey(
        Ocean,
        verbose_name=_("ocean"),
        on_delete=models.CASCADE,
        help_text=_("Ocean this sea belongs to"),
        related_name="seas",
    )
    area = models.BigIntegerField(
        _("area"),
        help_text=mark_safe(_("km²")),
        validators=[MinValueValidator(1)],
    )
    avg_depth = models.IntegerField(
        _("average depth"),
        help_text=_("meters"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    max_depth = models.IntegerField(
        _("maximum depth"),
        help_text=_("meters"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    basin_countries = models.ManyToManyField(
        "Country",
        related_name="seas",
        blank=True,
        verbose_name=_("basin countries"),
        help_text=_("Countries that border this sea"),
    )

    def get_parent_id_display(self):
        return self.parent

    class Meta:
        verbose_name = _("sea")
        verbose_name_plural = _("seas")
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def depth_range(self):
        """Return the depth range if both min and max are available."""
        if self.avg_depth and self.max_depth:
            return f"{self.avg_depth} - {self.max_depth} m"
        return None

    # depth_range.short_description = _("Depth Range")

    def child_seas_count(self):
        """Count of child seas."""
        return self.child_seas.count()

    # child_seas_count.short_description = _("Child Seas")


class Continent(models.Model):
    """Geographic continent data model."""

    name = models.CharField(
        _("name"),
        max_length=250,
        primary_key=True,
        help_text=_("Continent name"),
    )
    area = models.BigIntegerField(
        _("area"),
        help_text=mark_safe(_("km²")),
        validators=[MinValueValidator(1)],
    )
    population = models.BigIntegerField(
        _("population"),
        help_text=_("Number of inhabitants"),
        validators=[MinValueValidator(0)],
    )
    population_density = models.DecimalField(
        _("population density"),
        decimal_places=2,
        max_digits=8,
        help_text=mark_safe(_("people/km²")),
    )
    largest_country = models.OneToOneField(
        "Country",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("largest country"),
        help_text=_("Largest country by area"),
    )
    biggest_city = models.OneToOneField(
        "City",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("biggest city"),
        help_text=_("Largest city by population"),
    )
    longest_river = models.CharField(
        _("longest river"),
        max_length=250,
        blank=True,
        null=True,
        help_text=_("Name of the longest river"),
    )
    biggest_mountain = models.CharField(
        _("biggest mountain"),
        max_length=250,
        blank=True,
        null=True,
        help_text=_("Name of the highest mountain"),
    )
    oceans = models.ManyToManyField(
        Ocean,
        verbose_name=_("oceans"),
        help_text=_("Oceans bordering this continent"),
    )
    hemisphere = models.CharField(
        _("hemisphere"),
        max_length=5,
        choices=(("NORTH", _("North")), ("SOUTH", _("South")), ("BOTH", _("Both"))),
        help_text=_("Hemisphere location"),
    )

    def __str__(self):
        return self.name if self.name is not None else "Continent"

    class Meta:
        verbose_name = _("continent")
        verbose_name_plural = _("continents")
        ordering = ["name"]

    def countries_count(self):
        """Count countries in this continent."""
        return self.countries.count()

    countries_count.short_description = _("Countries")
    countries_count.column_type = "numeric"

    @property
    def formatted_population(self):
        """Format population with thousands separator."""
        return f"{self.population:,}"

    # formatted_population.short_description = _("Formatted Population")


class Country(models.Model):
    """Geographic country data model."""

    code = models.CharField(
        _("code"),
        max_length=3,
        unique=True,
        help_text=_("Country code (3 letters)"),
    )
    name = models.CharField(
        _("name"),
        max_length=250,
        help_text=_("Country name"),
    )
    independence_day = models.DateField(
        _("independence day"),
        null=True,
        blank=True,
        help_text=_("Date of independence"),
    )
    democratic_status = models.BooleanField(
        _("democratic status"),
        null=True,
        help_text=_("Whether the country is considered a democracy"),
    )
    continent = models.ForeignKey(
        Continent,
        null=True,
        related_name="countries",
        on_delete=models.CASCADE,
        verbose_name=_("continent"),
        help_text=_("Continent where this country is located"),
    )

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def years_since_independence(self):
        """Calculate years since independence."""
        if self.independence_day:
            today = date.today()
            years = today.year - self.independence_day.year
            if (today.month, today.day) < (self.independence_day.month, self.independence_day.day):
                years -= 1
            return years
        return None

    # years_since_independence.short_description = _("Years Independent")


class City(models.Model):
    """Geographic city data model."""

    name = models.CharField(
        _("name"),
        max_length=250,
        help_text=_("City name"),
    )
    is_capital = models.BooleanField(
        _("is capital city"),
        default=False,
        help_text=_("Whether this is the capital city of the country"),
    )
    population = models.BigIntegerField(
        _("population"),
        help_text=_("Number of inhabitants"),
        validators=[MinValueValidator(0)],
    )
    country = models.ForeignKey(
        Country,
        related_name="cities",
        on_delete=models.CASCADE,
        verbose_name=_("country"),
        help_text=_("Country this city belongs to"),
    )

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
        unique_together = ("name", "country")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.country.name}" if self.country_id else self.name

    @property
    def formatted_population(self):
        """Format population with thousands separator."""
        return f"{self.population:,}"

    # formatted_population.short_description = _("Formatted Population")
