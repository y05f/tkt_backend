from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from entreprises.models import Entreprise, Result
import json


class EntrepriseListPostTest(APITestCase):
    def setUp(self):
        f = open("test_data.json")
        rawdata = json.load(f)
        f.close()
        for entreprise_data in rawdata:
            results_data = entreprise_data.pop("results")
            entreprise = Entreprise.objects.create(**entreprise_data)
            for result_data in results_data:
                Result.objects.create(entreprise=entreprise, **result_data)

    def test_create(self):
        """
        Ensure we can create a new entreprise object.
        """
        NEW_DATA = {
            "name": "McKenzie LLC",
            "sector": "Services",
            "siren": "130812670",
            "results": [
                {
                    "ca": 1911099,
                    "margin": 883920,
                    "ebitda": 886652,
                    "loss": 7726955,
                    "year": 2016,
                },
                {
                    "ca": 1980600,
                    "margin": 95338,
                    "ebitda": 499775,
                    "loss": 8330251,
                    "year": 2017,
                },
            ],
        }

        url = reverse("list-post-entreprise")
        response = self.client.post(url, NEW_DATA, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entreprise.objects.count(), 4)  # 4 instances now
        self.assertEqual(Result.objects.count(), 8)  # 8 results in total
        self.assertEqual(Entreprise.objects.get(siren=130812670).name, "McKenzie LLC")
        self.assertEqual(
            Entreprise.objects.get(siren=130812670).results.get(year=2016).ca, 1911099
        )

    def test_get_list(self):
        """
        Ensure we can get a all entreprises.
        """
        url = reverse("list-post-entreprise")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(Entreprise.objects.get(siren=135694027).name, "Reinger Inc")

    def test_get_details(self):
        """
        Ensure we can get a all entreprises.
        """
        url = reverse("entreprise-details")
        response = self.client.get(url, {"siren": "130812670"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "McKenzie LLC")
