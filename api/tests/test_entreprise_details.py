from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from entreprises.models import Entreprise, Result
import json


class EntrepriseDetailsTest(APITestCase):
    def setUp(self):
        f = open("test_data.json")
        rawdata = json.load(f)
        f.close()
        for entreprise_data in rawdata:
            results_data = entreprise_data.pop("results")
            entreprise = Entreprise.objects.create(**entreprise_data)
            for result_data in results_data:
                Result.objects.create(entreprise=entreprise, **result_data)

    def test_get_details(self):
        """
        Ensure we can get entreprise details by its SIREN.
        """
        url = reverse("entreprise-details", kwargs={"siren": "115104805"})
        response = self.client.get(url, fromat="None")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Towne-Dach")
        self.assertEqual(
            response.data["results"],
            [
                {
                    "ca": 2752578,
                    "margin": -147358,
                    "ebitda": 485891,
                    "loss": 331323,
                    "year": 2017,
                },
                {
                    "ca": 1686886,
                    "margin": -117670,
                    "ebitda": 390980,
                    "loss": 3205084,
                    "year": 2016,
                },
            ],
        )

    def test_put_details(self):
        """
        Ensure we can update entreprise details by its SIREN.
        """
        UPDATED_DATA = {
            "name": "Reinger Inc",
            "sector": "Luxury",
            "siren": 135694027,
            "results": [
                {
                    "ca": 2077357,
                    "margin": 497351,
                    "ebitda": 65952,
                    "loss": 858474,
                    "year": 2018,
                },
                {
                    "ca": 200000,
                    "margin": 400000,
                    "ebitda": 60000,
                    "loss": 800000,
                    "year": 2019,
                },
            ],
        }
        url = reverse("entreprise-details", kwargs={"siren": "135694027"})
        response = self.client.put(url, UPDATED_DATA, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Reinger Inc")
        self.assertEqual(
            response.data["results"],
            [
                {
                    "ca": 2077357,
                    "margin": 497351,
                    "ebitda": 65952,
                    "loss": 858474,
                    "year": 2018,
                },
                {
                    "ca": 200000,
                    "margin": 400000,
                    "ebitda": 60000,
                    "loss": 800000,
                    "year": 2019,
                },
            ],
        )

    def test_delete_details(self):
        """
        Ensure we can delete an entreprise by its SIREN.
        """
        entreprises = Entreprise.objects.all()
        url = reverse("entreprise-details", kwargs={"siren": 135694027})
        response = self.client.delete(url, format=None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
