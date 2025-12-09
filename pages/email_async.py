# email_async.py
from django.db import transaction

def run_async(fn, *args, **kwargs):
    """
    Versión síncrona: ejecuta la función directamente.
    (Antes lanzaba un hilo en segundo plano.)
    """
    fn(*args, **kwargs)

def run_after_commit(fn, *args, **kwargs):
    """
    Ejecuta la función después de que se confirme la transacción,
    pero ahora de forma síncrona (sin threads).
    """
    transaction.on_commit(lambda: fn(*args, **kwargs))