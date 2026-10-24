"""Wyjątki domenowe zgłaszane podczas pobierania plików."""

class DownloadError(Exception):
    """Bazowy wyjątek dla błędów związanych z pobieraniem plików."""
    pass


# 2. Stworzenie dwóch klas wyjątków dziedziczących po DownloadError
class NotFoundError(DownloadError):
    """Wyjątek rzucany w przypadku błędu 404 (Not Found)."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(f'Brak wymaganego pliku :{self.message}')



class AccessDeniedError(DownloadError):
    """Wyjątek rzucany w przypadku błędu 403 (Forbidden)."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f'Dostęp zabroniony:{self.message}')