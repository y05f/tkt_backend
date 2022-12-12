from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from entreprises.models import Entreprise, Result
import json


class EntrepriseListCreateTest(APITestCase):
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
            "name": "Muller Group",
            "sector": "Luxury",
            "siren": 175112687,
            "results": [
                {
                    "ca": 1399582,
                    "margin": 985314,
                    "ebitda": 725283,
                    "loss": 4266902,
                    "year": 2017,
                },
                {
                    "ca": 1916496,
                    "margin": 979357,
                    "ebitda": 942617,
                    "loss": 2478758,
                    "year": 2016,
                },
            ],
        }

        url = reverse("list-create-entreprise")
        response = self.client.post(url, NEW_DATA, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entreprise.objects.count(), 5)  # 5 instances now
        self.assertEqual(Result.objects.count(), 10)  # 10 results in total
        self.assertEqual(Entreprise.objects.get(siren=175112687).name, "Muller Group")
        self.assertEqual(
            Entreprise.objects.get(siren=175112687).results.get(year=2016).ca, 1916496
        )

    def test_get_list(self):
        """
        Ensure we can get a all entreprises.
        """
        url = reverse("list-create-entreprise")
        response = self.client.get(url, format="None")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(Entreprise.objects.get(siren=135694027).name, "Reinger Inc")
        self.assertEqual(Entreprise.objects.get(siren=115104805).name, "Towne-Dach")
