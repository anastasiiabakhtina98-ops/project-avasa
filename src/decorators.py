"""Decorators for command handlers."""


def input_error(func):
    """Decorator for handling errors in command functions."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError as e:
            return f"Error: {e}"
        except IndexError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    return inner