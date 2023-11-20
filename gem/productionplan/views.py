import json
import logging

from http import HTTPStatus

from django.http import JsonResponse

from .models import Payload, PayloadException

logger = logging.getLogger(__name__)


def production_plan(request):
	solution = {}

	# Check HTTPmethod
	if request.method != 'POST':
		logger.error(f"Provided method {request.method} not supported")
		return JsonResponse(solution, status=HTTPStatus.METHOD_NOT_ALLOWED)

	# Parse JSON data 
	try:
		payload = json.loads(request.body)
	except json.JSONDecodeError:
		logger.error(f"Provided data is not a valid JSON document. Data: {request.body}")
		return JsonResponse(solution, status=HTTPStatus.INTERNAL_SERVER_ERROR)

	# Parse payload
	logger.info(f"DATA: {payload}")
	try:
		solution = Payload.solve(payload)
		logger.info(f"SOLUTION: {solution}")
	except PayloadException as err:
		logger.error(f"Cannot parse payload. Reason: {err}")
		return JsonResponse(solution, status=HTTPStatus.INTERNAL_SERVER_ERROR)

	return JsonResponse(solution, safe=False)
