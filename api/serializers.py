from rest_framework import serializers
from entreprises.models import Entreprise, Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ["ca", "margin", "ebitda", "loss", "year"]


class EntrepriseSerializer(serializers.ModelSerializer):
    results = ResultSerializer(many=True)

    class Meta:
        model = Entreprise
        fields = ["name", "sector", "siren", "results"]

    def create(self, validated_data):
        results_data = validated_data.pop("results")
        entreprise = Entreprise.objects.create(**validated_data)
        for result_data in results_data:
            Result.objects.create(entreprise=entreprise, **result_data)
        return entreprise

    def update(self, entreprise, validated_data):
        results_data = validated_data.pop("results")
        # update the entreprise fields
        entreprise.name = validated_data.get("name", entreprise.name)
        entreprise.sector = validated_data.get("sector", entreprise.sector)
        entreprise.siren = validated_data.get("siren", entreprise.siren)
        entreprise.save()
        # update all the results of the entreprise
        results_with_same_entreprise = Result.objects.filter(entreprise=entreprise)
        results_year_pool = []
        for result in results_data:
            # update results that already exist
            if results_with_same_entreprise.filter(year=result["year"]).exists():
                result_instance = results_with_same_entreprise.get(year=result["year"])
                result_instance.ca = result.get("ca", result_instance.ca)
                result_instance.margin = result.get("margin", result_instance.margin)
                result_instance.ebitda = result.get("ebitda", result_instance.ebitda)
                result_instance.loss = result.get("loss", result_instance.loss)
                result_instance.save()
                results_year_pool.append(result_instance.year)
            # create new results that doesn't exist
            else:
                result_instance = Result.objects.create(entreprise=entreprise, **result)
                results_year_pool.append(result_instance.year)
        # delete results that weren't included in the update request
        for result in results_with_same_entreprise:
            if result.year not in results_year_pool:
                results_with_same_entreprise.filter(year=result.year).delete()

        return entreprise
