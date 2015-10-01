from pyramda import curry


@curry
def create_model(model_class, data, session):
    session.add(model_class(**data))
