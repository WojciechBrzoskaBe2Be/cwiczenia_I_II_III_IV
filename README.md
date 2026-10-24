# Analiza plików pobieranych z URL

Projekt pobiera plik tekstowy z adresu URL, przetwarza jego zawartość wiersz po wierszu i zapisuje wyniki analizy w plikach CSV. Odczyt jest leniwy, dzięki czemu dane nie muszą być wczytywane w całości do pamięci.

## Przepływ działania

1. `url_files_processor` pobiera plik z wybranego adresu URL i zapisuje go lokalnie.
2. `read_file_lazy` udostępnia kolejne wiersze pliku jako generator.
3. `get_some_statistics` oblicza dla każdego wiersza sumę, wartość `avg` i wykrywa brakujące wartości oznaczone znakiem `-`. Dla maksymalnie 30 wartości liczbowych `avg` jest sumą podzieloną przez ich liczbę pomniejszoną o jeden; przy większej liczbie dzielnikiem jest ich liczba.
4. `report` zapisuje wyniki w dwóch raportach CSV: jeden zawiera statystyki liczbowe, a drugi indeksy kolumn z brakującymi danymi.

## Moduły

- `main.py` — przykład uruchomienia procesu pobrania, analizy i raportowania; zawiera przykładowe adresy URL oraz ścieżki plików.
- `file_processor.py` — pobieranie pliku, leniwy odczyt, obliczanie statystyk i zapis raportów.
- `custom_errors.py` — bazowy wyjątek pobierania oraz wyjątki dla odpowiedzi HTTP 404 i 403.
- `utils.py` — dekorator mierzący czas wykonania funkcji.
- `src/cwiczenia_i_ii_iii_iv/__init__.py` — moduł pakietu z funkcją `main` używaną przez skonfigurowany skrypt konsolowy.

## Wymagania i uruchomienie

Projekt wymaga Pythona 3.13 lub nowszego oraz biblioteki `requests` (deklarowanej jako zależność projektu). Przykładowy przepływ można uruchomić poleceniem:

```powershell
python main.py
```

Przed uruchomieniem sprawdź ścieżki plików ustawione w `main.py` i w razie potrzeby dostosuj je do swojego środowiska. Skrypt pobiera dane z `URL_OK`, a następnie zapisuje lokalny plik wejściowy oraz oba raporty.

Skonfigurowany w `pyproject.toml` skrypt konsolowy `cwiczenia-i-ii-iii-iv` uruchamia osobną funkcję `main` z modułu pakietu; obecnie wyświetla ona komunikat powitalny i nie uruchamia powyższego procesu analizy.