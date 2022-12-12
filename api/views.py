from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .serializers import EntrepriseSerializer, ResultSerializer
from entreprises.models import Entreprise, Result


class EntrepriseListCreate(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    get:
        Get all the entreprises with thier details and results
    post:
        Create an enreprise instance with details and results
    """

    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EntrepriseRetrieveUpdateDestroy(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    get:
        Get the entreprise with details and results using its SIREN number as lookup key
    put:
        Update entreprise data including results using its SIREN number as lookup key
    delete:
        Delete entreprise data using SIREN number
    """

    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    lookup_field = "siren"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EntrepriseNamesOnly(APIView):
    """
    get:
        get all the entreprise names or get entreprise details
    """

    def get(self, request):
        entreprises = (
            Entreprise.objects.values("name").annotate(count=Count("name")).order_by()
        )
        return Response(entreprises, status=status.HTTP_200_OK)


class EntrepriseNameDetails(APIView):
    """
    get:
        get entreprise details by name
    """

    def get(self, request, name):
        entreprise = Entreprise.objects.filter(name=name)
        serializer = EntrepriseSerializer(entreprise, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EntrepriseNameStats(APIView):
    """
    get:
        get entreprise stats by comparing the each year with the previous one.
    """

    def get(self, request, name):
        entreprise = Entreprise.objects.filter(name=name)
        serializer = EntrepriseSerializer(entreprise, many=True)
        for item in serializer.data:
            results = item["results"]
            # sort results by year
            results = sorted(results, key=lambda result: result["year"])
            stats = []  # stats will be the final list with results comparaison
            for prev_year_result, current_year_result in zip(results[:-1], results[1:]):
                # row contain the conparaison of between a year and its precedent
                row = {}
                ca = (
                    (current_year_result["ca"] - prev_year_result["ca"])
                    / prev_year_result["ca"]
                    * 100
                )
                margin = (
                    (current_year_result["margin"] - prev_year_result["margin"])
                    / prev_year_result["margin"]
                    * 100
                )
                ebitda = (
                    (current_year_result["ebitda"] - prev_year_result["ebitda"])
                    / prev_year_result["ebitda"]
                    * 100
                )
                loss = (
                    (current_year_result["loss"] - prev_year_result["loss"])
                    / prev_year_result["loss"]
                    * 100
                )
                row["year"] = (
                    str(prev_year_result["year"])
                    + "-"
                    + str(current_year_result["year"])
                )
                row["ca"] = "{plus_signal}{ca:.2f}%".format(
                    ca=ca, plus_signal="+" if ca > 0 else ""
                )
                row["margin"] = "{plus_signal}{margin:.2f}%".format(
                    margin=margin, plus_signal="+" if margin > 0 else ""
                )
                row["ebitda"] = "{plus_signal}{ebitda:.2f}%".format(
                    ebitda=ebitda, plus_signal="+" if ebitda > 0 else ""
                )
                row["loss"] = "{plus_signal}{loss:.2f}%".format(
                    loss=loss, plus_signal="+" if loss > 0 else ""
                )
                stats.append(row)
            item["results"] = stats

        return Response(serializer.data, status=status.HTTP_200_OK)
