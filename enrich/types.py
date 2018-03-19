import typing

import movies.models
import people.models

IFXEntity = typing.Union[movies.models.Movie, people.models.Person]
