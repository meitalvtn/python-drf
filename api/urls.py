from django.urls import path
from .views import TransactionAPIView, PolicyRuleAPIView, PolicyRuleDetailAPIView

urlpatterns = [
    path('transaction/', TransactionAPIView.as_view()),
    path('policy_rule/', PolicyRuleAPIView.as_view()),
    path('policy_rule/<int:id>', PolicyRuleDetailAPIView.as_view())
]