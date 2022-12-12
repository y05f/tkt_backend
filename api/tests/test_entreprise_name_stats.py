from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from entreprises.models import Entreprise, Result
import json


class EntrepriseNameStatsTest(APITestCase):
    def setUp(self):
        f = open("test_data.json")
        rawdata = json.load(f)
        f.close()
        for entreprise_data in rawdata:
            results_data = entreprise_data.pop("results")
            entreprise = Entreprise.objects.create(**entreprise_data)
            for result_data in results_data:
                Result.objects.create(entreprise=entreprise, **result_data)

    def test_get_name_list(self):
        """
        Ensure we can get all names of entreprises.
        """
        url = reverse("list-entreprise-name")
        response = self.client.get(url, format="None")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # 3 names "McKenzie LLC" is duplicated
        self.assertEqual(
            response.data[:],
            [
                {"name": "McKenzie LLC", "count": 2},
                {"name": "Towne-Dach", "count": 1},
                {"name": "Reinger Inc", "count": 1},
            ],
        )

    def test_get_name_details(self):
        """
        Ensure we can get all details of entreprise by name.
        """
        url = reverse("entreprise-name-details", kwargs={"name": "Reinger Inc"})
        response = self.client.get(url, format="None")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "name": "Reinger Inc",
                    "sector": "Services",
                    "siren": "135694027",
                    "results": [
                        {
                            "ca": 2077357,
                            "margin": 497351,
                            "ebitda": 65952,
                            "loss": 858474,
                            "year": 2017,
                        },
                        {
                            "ca": 432070,
                            "margin": 427778,
                            "ebitda": 290433,
                            "loss": 8023406,
                            "year": 2016,
                        },
                    ],
                }
            ],
        )

    def test_get_name_stats(self):
        """
        Ensure we can get all details of entreprise by name.
        """
        url = reverse("entreprise-name-stats", kwargs={"name": "Reinger Inc"})
        response = self.client.get(url, format="None")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "name": "Reinger Inc",
                    "sector": "Services",
                    "siren": "135694027",
                    "results": [
                        {
                            "year": "2016-2017",
                            "ca": "+380.79%",
                            "margin": "+16.26%",
                            "ebitda": "-77.29%",
                            "loss": "-89.30%",
                        }
                    ],
                }
            ],
        )
