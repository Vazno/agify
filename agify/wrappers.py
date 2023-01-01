import asyncio
import httpx
from typing import List, Dict, Union, Iterable
from typing import Literal
from copy import copy

class NameAPI():
	MAX_PER_REQUEST = 9
	AGIFY_URL = "https://api.agify.io/?"
	NATIONALIZE_URL = "https://api.nationalize.io?"
	GENDERIZE_URL = "https://api.genderize.io?"

	X_RATE_LIMIT_RESET = "x-rate-limit-reset"
	X_RATE_LIMIT_LIMIT = "x-rate-limit-limit"
	X_RATE_LIMIT_REMAINING = "x-rate-limit-remaining"

	def __init__(self, names: Union[Iterable[str], str] = [],
					mode: Literal["age", "nation", "gender", "*"] = "*",
					country_id: str = None,
					api_key: str = None,
					ignore_errors: bool = False) -> None:
		'''Predict current age, nation, gender by name.
			Python wrapper for these API's: https://agify.io/ https://genderize.io/ https://nationalize.io/
		The API follows ISO 3166-1 alpha-2 for country codes.
			List https://agify.io/our-data of supported countries.
		'''
		if type(names) == str: # If there is only one name
			self.names = [names]
		else:
			self.names = list(names)

		if mode == "*":
			self.URL = [self.AGIFY_URL, self.NATIONALIZE_URL, self.GENDERIZE_URL]
		elif mode == "age":
			self.URL = [self.AGIFY_URL]
		elif mode == "nation":
			self.URL = [self.NATIONALIZE_URL]
		elif mode == "gender":
			self.URL = [self.GENDERIZE_URL]

		self.api_key = f"&apikey={api_key}" if api_key != None else ""
		self.country_id = f"&country_id={country_id}" if api_key != None else ""
		self.ignore_errors = bool(ignore_errors)

	def __send_requests(self) -> List[httpx.Response]:
		with httpx.Client() as client:
			responses = list()
			for multi_req_url in self._gen_urls():
				responses.append(client.get(multi_req_url))
		return responses

	def get_names_info(self) -> Dict:
		'''Returns dictionary with info about names'''
		if self.names == []:
			raise ValueError("Please provide names to check, names parameter is empty.")
		dict_ = dict()
		responses = self.__send_requests()

		if self.ignore_errors is False:
			self._check_errors(responses)
			for response in responses:
				for d in response.json():
					d_name = d["name"]
					del d["name"]
					try:
						dict_[d_name] = dict_[d_name] | d
					except KeyError:
						dict_[d_name] = d
		else:
			for response in responses:
				for d in response.json():
					try:
						d_name = d["name"]
						del d["name"]
						try:
							dict_[d_name] = dict_[d_name] | d
						except KeyError:
							dict_[d_name] = d
					except TypeError:
						pass
		return dict_

	def get_headers(self) -> httpx.Headers:
		'''Returns response's headers
			
			Each call decreases amount of total available calls by 1'''
		with httpx.Client() as client:
			response = client.get(f"{self.URL[0]}&name=Test")
		return response.headers

	def get_limit_reset(self) -> int:
		'''Seconds remaining until a new time window opens
			
			Each call decreases amount of total available calls by 1'''
		with httpx.Client() as client:
			response = client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_RESET])

	def get_limit(self) -> int:
		'''The amount of names available in the current time window
			
			Each call decreases amount of total available calls by 1'''
		with httpx.Client() as client:
			response = client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_LIMIT])

	def get_limit_remaining(self) -> int:
		'''The number of names left in the current time window
			
			Each call decreases amount of total available calls by 1'''
		with httpx.Client() as client:
			response = client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_REMAINING])

	def _check_errors(self, responses: List[httpx.Response]) -> None:
		'''Checks if there are any errors in request.'''
		for response in responses:
			if response.status_code != 200:
				raise ValueError(response.json()["error"])

	def _gen_urls(self) -> List[str]:
		'''Generates urls with MAX_PER_REQUEST names in single url'''
		url_lists = list()
		for url in self.URL:
			names = copy(self.names)
			while names != []:
				for name in range(self.MAX_PER_REQUEST):
					try:
						url += f"&name[]={names.pop(0)}"
					except IndexError:
						break
				url += self.api_key + self.country_id
				url_lists.append(url)
		return url_lists

class AsyncNameAPI(NameAPI):
	def __init__(self, names: Union[Iterable[str], str] = [],
					mode: Literal["age", "nation", "gender", "*"] = "*",
					country_id: str = None,
					api_key: str = None,
					ignore_errors: bool = False) -> None:
		'''Predict current age, nation, gender by name.
			An asynchronous Python wrapper for these API's: https://agify.io/ https://genderize.io/ https://nationalize.io/
		The API follows ISO 3166-1 alpha-2 for country codes.
			List https://agify.io/our-data of supported countries.
		'''
		super().__init__(names, mode, country_id, api_key, ignore_errors)

	async def __send_requests(self) -> List[httpx.Response]:
		async with httpx.AsyncClient() as client:
			tasks = list()
			for multi_req_url in super()._gen_urls():
				tasks.append(asyncio.create_task(client.get(multi_req_url)))
			responses = await asyncio.gather(*tasks)
		return responses

	async def get_names_info(self) -> Dict:
		'''Returns dictionary with info about names'''
		if self.names == []:
			raise ValueError("Please provide names to check, names parameter is empty.")
		dict_ = dict()
		responses = await self.__send_requests()

		if self.ignore_errors is False:
			super()._check_errors(responses)
			for response in responses:
				for d in response.json():
					d_name = d["name"]
					del d["name"]
					try:
						dict_[d_name] = dict_[d_name] | d
					except KeyError:
						dict_[d_name] = d
		else:
			for response in responses:
				for d in response.json():
					try:
						d_name = d["name"]
						del d["name"]
						try:
							dict_[d_name] = dict_[d_name] | d
						except KeyError:
							dict_[d_name] = d
					except TypeError:
						pass
		return dict_

	async def get_headers(self) -> httpx.Headers:
		'''Returns response's headers
			
			Each call decreases amount of total available calls by 1'''
		async with httpx.AsyncClient() as client:
			response = await client.get(f"{self.URL[0]}&name=Test")
		return response.headers

	async def get_limit_reset(self) -> int:
		'''Seconds remaining until a new time window opens
			
			Each call decreases amount of total available calls by 1'''
		async with httpx.AsyncClient() as client:
			response = await client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_RESET])

	async def get_limit(self) -> int:
		'''The amount of names available in the current time window
			
			Each call decreases amount of total available calls by 1'''
		async with httpx.AsyncClient() as client:
			response = await client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_LIMIT])

	async def get_limit_remaining(self) -> int:
		'''The number of names left in the current time window
			
			Each call decreases amount of total available calls by 1'''
		async with httpx.AsyncClient() as client:
			response = await client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_REMAINING])
