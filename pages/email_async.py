import threading
from django.db import transaction

def run_async(fn, *args, **kwargs):
    """Ejecuta la función en un hilo en segundo plano (no bloquea la request)."""
    t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    t.start()

def run_after_commit(fn, *args, **kwargs):
    """Ejecuta la función después de que se confirme la transacción."""
    def _launch():
        run_async(fn, *args, **kwargs)
    transaction.on_commit(_launch)