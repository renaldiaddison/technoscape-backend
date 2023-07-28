from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
from .models import Model


class _ModelPredictAPIView(APIView):
    def post(request, *args, **kwargs):
        # get request data
        # data = request.data.get('asd')

        # load model
        model_instance = Model.get_instance()

        # predict model
        prediction = model_instance.predict()
        return Response({"refresh_token": prediction}, status=status.HTTP_200_OK)


model_predict_api_view = _ModelPredictAPIView.as_view()
