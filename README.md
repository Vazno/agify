# Asynchronous Python wrapper for ![agify](https://agify.io/)'s name APIs (Genderize, Nationalize, Agify)

## Example:
```python
from agify import NameAPI
g = NameAPI({"Igor", "Alex", }, mode="*")
print(asyncio.run(g.get_names_info()))
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
```