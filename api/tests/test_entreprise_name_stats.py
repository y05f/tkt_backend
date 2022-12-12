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
        Ensure we can get a all names of entreprises.
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
