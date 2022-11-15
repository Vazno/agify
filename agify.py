import asyncio
import httpx
from typing import List, Dict, Union, Iterable

class GetAgeByName():
	MAX_PER_REQUEST = 9
	URL = "https://api.agify.io/?"
	def __init__(self, names: Union[Iterable[str], str],
					api_key: str = None,
					country_id: str = None,
					ignore_errors: bool = False) -> None:
		'''Predict current age by name.
			Python wrapper for https://agify.io/
		The API follows ISO 3166-1 alpha-2 for country codes.
			List https://agify.io/our-data of supported countries.
		'''
		if type(names) == str: # If there is only one name
			self.names = [names]
		else:
			self.names = list(names)
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
					dict_[d_name] = d

		elif self.ignore_errors is True:
			for response in responses:
				for d in response.json():
					try:
						d_name = d["name"]
						del d["name"]
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
		while self.names != []:
			url = self.URL
			for name in range(self.MAX_PER_REQUEST):
				try:
					url += f"&name[]={self.names.pop(0)}"
				except IndexError:
					break
			url += self.api_key + self.country_id
			url_lists.append(url)
		return url_lists
