from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
from .models import Model
from django.shortcuts import get_object_or_404
from user.models import User, UserApproval
from loan.models import LoanApproval
from utils import responses


class _ModelPredictAPIView(APIView):
    def post(request, *args, **kwargs):
        user_id = request.data.get('user')
        user = get_object_or_404(User, uid=user_id)
        user_approval: UserApproval = user.user_approval

        # approval_request = get_object_or_404(UserApproval, pk=user.approve_user)
        model_instance = Model.get_instance()
        loan_approval: LoanApproval = LoanApproval.objects.filter(
            user_id=user_id)
        # 	Gender, Married, Dependent, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area
        prediction = model_instance.predict(
            # [0.0 , 0.0, 0.0, 1,0.0, 1811, 1666.0, 54.0, 360.0, 1.0, 2])
            [[user.gender, user_approval.married, user_approval.dependent, user_approval.education, user_approval.self_employed, user_approval.income, user_approval.coappliciant_income, loan_approval.loan_amount, loan_approval.loan_days_term, user_approval.credit_history, user_approval.property_area]])
        print(prediction)
        if prediction[0] == 0:
            return responses.error_response(error_message="anda miskin")

        return Response({"result": prediction}, status=status.HTTP_200_OK)


model_predict_api_view = _ModelPredictAPIView.as_view()
