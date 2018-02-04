from django.http import HttpResponse, JsonResponse

import csv
import urllib2
import json


class LoanSchemeFetcher:
	def __init__(self, url=''):
		self.url = url
		self.amount = 0

	def get_all_schemes(self):
		response = []
		try:
			response = urllib2.urlopen(self.url)
		except Exception as ex:
			return response
		schemes = list(csv.reader(response))
		if len(schemes) > 1:
			schemes = schemes[1:]	
		return schemes

	def get_loan_schemes(self, amount):
		self.amount = int(amount)
		status_code = 500
		if self.amount <= 0:
			status_code = 400
			return JsonResponse(
					{
						'error' : 'Invalid Request', 
						'message' : 'Invalid amount entered'
					},
					status = status_code
				)
		schemes = self.get_all_schemes()
		if schemes is None or len(schemes) < 2:
			status_code = 404
			return JsonResponse(
					{
						'error' : 'HTTP Error 404',
						'message': 'Resource not found'
					},
					status = status_code
				)
		final_scheme = []
		bank_tenure_dict = {}
		for scheme in schemes:
			if int(scheme[3]) == self.amount:
				tenure = {
					'months' : int(scheme[1]),
					'rate' : int(scheme[2]),
					'minimum_amount' : int(scheme[3])
				}
				tenures = bank_tenure_dict.get(scheme[0])
				if tenures:
					bank_tenure_dict[scheme[0]].append(tenure)
				else:
					tenures = [tenure]
					bank_tenure_dict[scheme[0]] = tenures
		for bank in bank_tenure_dict:
			scheme_json = {
				'bank' : bank,
				'tenures' : bank_tenure_dict[bank]
			}
			final_scheme.append(scheme_json)
		return HttpResponse(json.dumps(final_scheme, indent=2))

