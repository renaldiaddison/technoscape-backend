from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
from .models import Model


class _ModelPredictAPIView(APIView):
    def post(request, *args, **kwargs):
        data = request.data.get('user_id')

        

        # load model
        model_instance = Model.get_instance()

        # predict model
        prediction = model_instance.predict()
        return Response({"result": prediction}, status=status.HTTP_200_OK)


model_predict_api_view = _ModelPredictAPIView.as_view()
