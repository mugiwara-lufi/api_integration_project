from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_external_data, transform_data

class UnifiedWeatherView(APIView):
    def get(self, request):
        country = request.query_params.get('country')
        if not country:
            return Response({"error": "Missing 'country' parameter"}, status=400)

        c_raw, w_raw, error = get_external_data(country)
        if error:
            return Response({"error": error}, status=404)

        final_data = transform_data(c_raw, w_raw)
        return Response(final_data, status=200)