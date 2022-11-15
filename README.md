# Asynchronous Python wrapper for `https://agify.io/`'s API

## Example:
```python
import asyncio
from agify import GetAgeByName

if __name__ == "__main__":
	g = GetAgeByName({"alex", "aidar", "nina", "karen", "igor", "vasya", "Elon", "Elona"})
	print(asyncio.run(g.get_names_info()))
	# ->
	{'Elon': {'age': 66, 'count': 146},
	'Elona': {'age': 51, 'count': 694},  
	'aidar': {'age': 39, 'count': 241},  
	'alex': {'age': 45, 'count': 411442},
	'igor': {'age': 49, 'count': 30303}, 
	'karen': {'age': 65, 'count': 69828},
	'nina': {'age': 50, 'count': 76072}, 
	'vasya': {'age': 49, 'count': 720}}  
```