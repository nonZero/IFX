import movies.models
import people.models

ENTITY_MODELS = {
    'movie': movies.models.Movie,
    'person': people.models.Person,
}

ENTITY_MODELS_REVERSE = {v: k for k, v in ENTITY_MODELS.items()}
