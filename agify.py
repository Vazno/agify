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

	def __init__(self, names: Union[Iterable[str], str],
					mode: Literal["age", "nation", "gender", "*"] = "*",
					api_key: str = None,
					country_id: str = None,
					ignore_errors: bool = False) -> None:
		'''Predict current age by name.
			Python wrapper for https://agify.io/ https://genderize.io/ https://nationalize.io/
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

	async def __send_requests(self) -> List[httpx.Response]:
		async with httpx.AsyncClient() as client:
			tasks = list()
			for multi_req_url in self.__gen_urls():
				tasks.append(asyncio.create_task(client.get(multi_req_url)))
			t = await asyncio.gather(*tasks)
		return t

	async def get_names_info(self) -> Dict:
		'''Returns dictionary {'name': {}}'''
		dict_ = dict()
		responses = await self.__send_requests()

		if self.ignore_errors is False:
			self.__check_errors(responses)
			for response in responses:
				for d in response.json():
					d_name = d["name"]
					del d["name"]
					try:
						dict_[d_name] = dict_[d_name] | d
					except KeyError:
						dict_[d_name] = d

		elif self.ignore_errors is True:
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

	def __check_errors(self, responses: List[httpx.Response]) -> None:
		'''Checks if there are any errors in request.'''
		for response in responses:
			if response.status_code != 200:
				raise ValueError(response.json()["error"])

	def __gen_urls(self):
		'''Generates url requests with MAX_PER_REQUEST names'''
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
