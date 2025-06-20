import inspect


class Integration:
    def describe_methods(self):
        methods = {}
        ignored = {"describe_methods", "call", "name"}

        for attr in dir(self):
            if attr.startswith("_") or attr in ignored:
                continue

            fn = getattr(self, attr)
            if callable(fn):
                try:
                    sig = str(inspect.signature(fn))
                except Exception:
                    sig = "()"
                methods[f"{self.name().lower()}.{attr}"] = sig

        return methods

    def call(self, method, **kwargs):
        fn = getattr(self, method, None)
        if fn is None or not callable(fn):
            raise Exception(
                f"Method '{method}' not found in integration '{self.name()}'"
            )
        return fn(**kwargs)

    def name(self):
        return self.__class__.__name__
