from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .scheme_fetcher import LoanSchemeFetcher
from loan_project.settings import CSV_DATA_SOURCE_URL

import json

def index(request):
	return HttpResponse("Test home page")

def emi_schemes(request):
	amount = request.GET.get('amount')
	loan_scheme = LoanSchemeFetcher(CSV_DATA_SOURCE_URL)
	return loan_scheme.get_loan_schemes(amount)