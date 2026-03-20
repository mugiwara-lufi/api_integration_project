from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_external_data, transform_data

# --- ADD THESE TWO IMPORTS ---
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UnifiedWeatherView(APIView):
    
    # --- ADD THIS DECORATOR HERE ---
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'country', 
                openapi.IN_QUERY, 
                description="Name of the country (e.g., Philippines, Japan)", 
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: 'Success: Returns combined country and weather data',
            400: 'Bad Request: Missing country parameter',
            404: 'Not Found: Country does not exist'
        }
    )
    def get(self, request):
        country = request.query_params.get('country')
        if not country:
            return Response({"error": "Missing 'country' parameter"}, status=400)

        c_raw, w_raw, error = get_external_data(country)
        if error:
            return Response({"error": error}, status=404)

        final_data = transform_data(c_raw, w_raw)
        return Response(final_data, status=200)