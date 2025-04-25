from django.utils.translation import gettext_lazy as _

from viewflow import Icon
from viewflow.contrib.import_export import ExportViewsetMixin
from viewflow.forms import Layout, FieldSet, Row, DependentModelSelect
from viewflow.urls import (
    Application,
    DetailViewMixin,
    DeleteViewMixin,
    ModelViewset,
    ReadonlyModelViewset,
)

from . import models, filters, forms


class CityViewset(ExportViewsetMixin, DetailViewMixin, DeleteViewMixin, ModelViewset):
    """
    A viewset for displaying, editing, deleting, and exporting city instances.

    Attributes:
        icon (Icon): An icon representing the viewset in the UI.
        model (models.City): The model class this viewset works with.
        list_columns (tuple): Columns to display in the list view.
        list_filter_fields (tuple): Fields to provide filtering capabilities in the list view.
        list_search_fields (list): Fields to provide search capabilities in the list view.
        queryset: The queryset used for list, detail, and other actions, optimized with select_related.
        form_widgets (dict, optional): Custom form widgets to use in forms. Uses AjaxModelSelect for country field to
                                       enable AJAX based selection.

    """

    icon = Icon("location_city")
    model = models.City
    list_columns = ("name", "country", "population")
    list_filter_fields = (
        "is_capital",
        "country",
    )
    list_search_fields = ["name"]
    queryset = model._default_manager.select_related("country")
    try:
        from viewflow.forms import AjaxModelSelect

        form_widgets = {"country": AjaxModelSelect(lookups=["name__istartswith"])}
    except ImportError:
        # pro-only
        pass

    def get_create_form_class(self, request):
        """
        Custom form class that restricts capital city creation to admin users
        """
        from django import forms
        from viewflow.forms import ModelForm

        class CityCreateForm(ModelForm):
            class Meta:
                model = self.model
                fields = ["name", "country", "population", "is_capital"]

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Only admin users can create capital cities
                if not request.user.is_superuser:
                    self.fields["is_capital"].disabled = True
                    self.fields["is_capital"].help_text = _(
                        "Only administrators can create capital cities"
                    )

        return CityCreateForm


class ContinentViewset(ExportViewsetMixin, ModelViewset):
    """
    A viewset for displaying and editing continent instances.

    Provides capabilities to list, create, and edit continents along with exporting functionality.

    Attributes:
        icon (Icon): An icon representing the viewset in the UI.
        model (models.Continent): The model class this viewset works with.
        list_columns (tuple): Columns to display in the list view.
        list_filter_fields (tuple): Fields to provide filtering capabilities in the list view.
        create_form_layout (Layout): Defines the layout of the form used for creating a continent.
        form_layout (Layout): Defines the layout of the form used for editing a continent.

    Methods:
        surrounded_oceans: Returns a string listing the names of oceans surrounding a continent.
    """

    icon = Icon("terrain")
    model = models.Continent
    list_columns = (
        "name",
        "surrounded_oceans",
        "countries_count",
        "area",
        "population",
    )
    list_filter_fields = ("oceans",)
    create_form_layout = Layout(
        "name",
        FieldSet(
            _("Details"),
            "area",
            Row("oceans", "hemisphere"),
            Row("population", "population_density"),
        ),
    )
    form_layout = Layout(
        "name",
        FieldSet(
            _("Details"),
            "area",
            Row("oceans", "hemisphere"),
            Row("population", "population_density"),
        ),
        FieldSet(
            _("Fun facts"),
            Row("largest_country", "biggest_mountain"),
            Row("biggest_city", "longest_river"),
        ),
    )

    def surrounded_oceans(self, continent):
        return ", ".join(ocean.name for ocean in continent.oceans.all())

    surrounded_oceans.short_description = _("Surrounded oceans")


class CountryViewset(DeleteViewMixin, ModelViewset):
    icon = Icon("nature_people")
    update_form_class = forms.CountryForm
    model = models.Country
    list_columns = (
        "tld",
        "name",
        "continent",
        "became_independent_in_20_century",
        "gay_friendly",
    )
    list_filter_fields = (
        "continent",
        "independence_day",
    )
    list_object_link_columns = ("tld", "name")
    queryset = model._default_manager.select_related("continent").order_by("name")

    def tld(self, country):
        return "." + country.code.lower()

    tld.short_description = "TLD"

    def became_independent_in_20_century(self, country):
        if country.independence_day:
            return 1900 <= country.independence_day.year <= 2000

    became_independent_in_20_century.short_description = _(
        "Became independent in XX century"
    )
    became_independent_in_20_century.boolean = True


ocean_viewset = ReadonlyModelViewset(
    app_name="ocean",
    icon=Icon("directions_boat"),
    model=models.Ocean,
    list_columns=(
        "name",
        "area",
    ),
)


class SeaViewset(DeleteViewMixin, ModelViewset):
    icon = Icon("beach_access")
    model = models.Sea
    list_columns = (
        "name",
        "parent_sea",
        "ocean",
        "sea_area",
    )
    list_filterset_class = filters.SeaFilterSet
    form_layout = Layout(
        "ocean",
        Row("name", "parent"),
        Row("area", "avg_depth", "max_depth"),
        "basin_countries",
    )
    form_widgets = {
        "parent": DependentModelSelect(
            depends_on="ocean",
            queryset=lambda parent: models.Sea.objects.filter(ocean=parent),
        )
    }

    def parent_sea(self, sea):
        return sea.parent

    def sea_area(self, sea):
        return None if sea.area == 0 else sea.area

    sea_area.empty_value = "-"
    sea_area.column_type = "numeric"

    def get_queryset(self, request):
        return self.model._default_manager.select_related("ocean", "parent")

    @property
    def list_filterset_initial(self):
        ocean = models.Ocean.objects.filter(name="Atlantic").first()
        if ocean:
            return {"ocean": ocean.pk}
        return None


class AtlasApp(Application):
    title = "CRUD sample"
    icon = Icon("extension")
    app_name = "atlas"
    permission = "atlas.can_view_city"
    viewsets = [
        CityViewset(),
        ContinentViewset(),
        CountryViewset(),
        ocean_viewset,
        SeaViewset(),
    ]
