# Asynchronous Python wrapper for (![Genderize](https://genderize.io/), ![Nationalize](https://nationalize.io/), ![Agify](https://agify.io/))
A simple API for predicting the age, gender, and country of a person by their name.

The API is free for up to 1000 names/day. No sign up or API key needed. So go ahead and try it out.

# Instalation
`pip install agify`

## Usage example:
### async version:
```python
from agify import AsyncNameAPI
g = AsyncNameAPI(["Igor", "Alex"], mode="*")
print(asyncio.run(g.get_names_info()))
# ->
{'Alex': {'age': 45,
          'count': 1114390,
          'country': [{'country_id': 'CZ', 'probability': 0.082},
                      {'country_id': 'UA', 'probability': 0.045},
                      {'country_id': 'RO', 'probability': 0.033},
                      {'country_id': 'RU', 'probability': 0.031},
                      {'country_id': 'IL', 'probability': 0.028}],
          'gender': 'male',
          'probability': 0.96},
 'Igor': {'age': 49,
          'count': 168019,
          'country': [{'country_id': 'UA', 'probability': 0.169},
                      {'country_id': 'RS', 'probability': 0.113},
                      {'country_id': 'RU', 'probability': 0.093},
                      {'country_id': 'HR', 'probability': 0.084},
                      {'country_id': 'SK', 'probability': 0.062}],
          'gender': 'male',
          'probability': 1.0}}

a = AsyncNameAPI(["Ivan"], "gender")
print(asyncio.run(a.get_names_info()))
# ->
{'Ivan': {'count': 425630, 'gender': 'male', 'probability': 1.0}}

a = AsyncNameAPI()
print(asyncio.run(a.get_limit_remaining()))
# ->
987
```

### usual version:
```python
from agify import NameAPI
g = NameAPI(["Igor", "Alex"], mode="*")
print(g.get_names_info())
# ->
{'Alex': {'age': 45,
          'count': 1114390,
          'country': [{'country_id': 'CZ', 'probability': 0.082},
                      {'country_id': 'UA', 'probability': 0.045},
                      {'country_id': 'RO', 'probability': 0.033},
                      {'country_id': 'RU', 'probability': 0.031},
                      {'country_id': 'IL', 'probability': 0.028}],
          'gender': 'male',
          'probability': 0.96},
 'Igor': {'age': 49,
          'count': 168019,
          'country': [{'country_id': 'UA', 'probability': 0.169},
                      {'country_id': 'RS', 'probability': 0.113},
                      {'country_id': 'RU', 'probability': 0.093},
                      {'country_id': 'HR', 'probability': 0.084},
                      {'country_id': 'SK', 'probability': 0.062}],
          'gender': 'male',
          'probability': 1.0}}

a = NameAPI(["Ivan"], "gender")
print(a.get_names_info())
# ->
{'Ivan': {'count': 425630, 'gender': 'male', 'probability': 1.0}}

a = NameAPI()
print(a.get_limit_remaining())
# ->
987
```

---
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
