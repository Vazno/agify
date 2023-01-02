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
		self.client = httpx.Client()

		self.names = names

		if mode == "*":
			self.URL = [self.AGIFY_URL, self.NATIONALIZE_URL, self.GENDERIZE_URL]
		elif mode == "age":
			self.URL = [self.AGIFY_URL]
		elif mode == "nation":
			self.URL = [self.NATIONALIZE_URL]
		elif mode == "gender":
			self.URL = [self.GENDERIZE_URL]

		self.api_key = f"&apikey={api_key}" if api_key != None else ""
		self.country_id = f"&country_id={country_id}" if country_id != None else ""
		self.ignore_errors = bool(ignore_errors)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc, tb):
		self.client.close()

	def __send_requests(self) -> List[httpx.Response]:
		responses = list()
		for multi_req_url in self._gen_urls():
			responses.append(self.client.get(multi_req_url))
		return responses

	def get_names_info(self, names: Union[List[str], str] = None) -> Dict:
		'''Returns dictionary with info about names'''
		if names != None:
			self.names = names
			responses = self.__send_requests()
			return super()._merge_dicts(responses)
		elif names == None and self.names != None:
			responses = self.__send_requests()
			return super()._merge_dicts(responses)
		else:
			raise ValueError("Please provide names to check, names parameter is empty.")

	def get_headers(self) -> httpx.Headers:
		'''Returns response's headers
			
			Each call decreases amount of total available calls by 1'''
		response = self.client.get(f"{self.URL[0]}&name=Test")
		return response.headers

	def get_limit_reset(self) -> int:
		'''Seconds remaining until a new time window opens
			
			Each call decreases amount of total available calls by 1'''
		response = self.client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_RESET])

	def get_limit(self) -> int:
		'''The amount of names available in the current time window
			
			Each call decreases amount of total available calls by 1'''
		response = self.client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_LIMIT])

	def get_limit_remaining(self) -> int:
		'''The number of names left in the current time window
			
			Each call decreases amount of total available calls by 1'''
		response = self.client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_REMAINING])

	def _check_errors(self, responses: List[httpx.Response]) -> None:
		'''Checks if there are any errors in request.'''
		for response in responses:
			if response.status_code != 200:
				raise ValueError(response.json()["error"])

	def _merge_dicts(self, responses: List[httpx.Response]) -> Dict:
		'''Merges responses' dicts to one dict'''
		dict_ = dict()
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

	def _gen_urls(self) -> List[str]:
		'''Generates urls with MAX_PER_REQUEST names in single url'''
		if type(self.names) == str:
			self.names = [self.names]
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
	def __init__(self, names: Union[Iterable[str], str] = None,
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
		self.client = httpx.AsyncClient()

	async def __aenter__(self):
		return self

	async def __aexit__(self, exc_type, exc, tb):
		await self.client.aclose()

	async def __send_requests(self) -> List[httpx.Response]:
		tasks = list()
		for multi_req_url in super()._gen_urls():
			tasks.append(asyncio.create_task(self.client.get(multi_req_url)))
		responses = await asyncio.gather(*tasks)
		return responses

	async def get_names_info(self, names: Union[List[str], str] = None) -> Dict:
		'''Returns dictionary with info about names'''
		if names != None:
			self.names = names
			responses = await self.__send_requests()
			return super()._merge_dicts(responses)
		elif names == None and self.names != None:
			responses = await self.__send_requests()
			return super()._merge_dicts(responses)
		else:
			raise ValueError("Please provide names to check, names parameter is empty.")

	async def get_headers(self) -> httpx.Headers:
		'''Returns response's headers
			
			Each call decreases amount of total available calls by 1'''
		response = await self.client.get(f"{self.URL[0]}&name=Test")
		return response.headers

	async def get_limit_reset(self) -> int:
		'''Seconds remaining until a new time window opens
			
			Each call decreases amount of total available calls by 1'''
		response = await self.client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_RESET])

	async def get_limit(self) -> int:
		'''The amount of names available in the current time window
			
			Each call decreases amount of total available calls by 1'''
		response = await self.client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_LIMIT])

	async def get_limit_remaining(self) -> int:
		'''The number of names left in the current time window
			
			Each call decreases amount of total available calls by 1'''
		response = await self.client.get(f"{self.URL[0]}&name=Test")
		return int(response.headers[self.X_RATE_LIMIT_REMAINING])

