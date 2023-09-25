class Model:

    def __init__(self):
        self._model = None


    def experiment(self, variations):
        def decorator(func):
            return func(*args, **kwargs)
        return decorator


    def get_variation(self):
        return self._model

