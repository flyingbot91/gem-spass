import logging

from enum import Enum
from typing import Dict, List

logger = logging.getLogger(__name__)


class PlantType(Enum):
    GASFIRED = 'gasfired'
    TURBOJET = 'turbojet'
    WINDTURBINE = 'windturbine'


class PayloadException(Exception):
    pass


class Payload:

	@staticmethod
	def get_sorted_costs(fuels: Dict) -> List[PlantType]:
		"""Determine the fuel costs, from lower to higher, sorted by PlantType."""
		sorted_costs = [
			PlantType.WINDTURBINE
		]

		cost_gas = fuels["gas(euro/MWh)"]
		cost_kerosine = fuels["kerosine(euro/MWh)"]

		if cost_gas < cost_kerosine:
			sorted_costs.append(PlantType.GASFIRED)
			sorted_costs.append(PlantType.TURBOJET)
		else:
			sorted_costs.append(PlantType.TURBOJET)
			sorted_costs.append(PlantType.GASFIRED)

		return sorted_costs

	@staticmethod
	def solve(payload):
		"""Determine the production plan."""
		# Production plan
		solution = []
		required = payload['load']
		# Maximum available load by all powerplants working at Pmax
		max_available_load = 0

		try:
			# Sort fuel types by powerplant cost
			costs = Payload.get_sorted_costs(payload['fuels'])

			# Iterate until all required load is met.
			for cost in costs:
				logger.debug(cost)
				for powerplant in payload['powerplants']:

					max_available_load += powerplant['pmax']

					if powerplant['type'] == cost.value:
						if required >= powerplant['pmax']:
							to_be_generated = powerplant['pmax']
						elif powerplant['pmin'] <= required < powerplant['pmax']:
							to_be_generated = required
						elif powerplant['pmin'] < required < 0:
							#FIXME: In this case, the power production exceeds the demand!
							to_be_generated = powerplant['pmin']
						else:
							# Do nothing
							to_be_generated = 0

						# Adjust generation
						if powerplant['type'] == PlantType.WINDTURBINE.value:
							to_be_generated = to_be_generated * payload['fuels']['wind(%)']/100

						logger.debug(f"  {powerplant['name']}, {required}, {to_be_generated}")

						solution.append({
							'name': powerplant['name'],
							'p': to_be_generated 
						})

						if required < 0:
							required = 0
						else:
							required -= to_be_generated

			# Cornercases
			# a) Production exceeds demand 
			if required < 0:
				logger.error(f"Production exceeds demand in {required}")

			# b) Demand exceeds the maximum available load
			if payload['load'] > max_available_load:
				logger.error(f"Load {load} exceeds max. available load {max_available_load}")

		except Exception as err:
			raise PayloadException(err)

		return solution
