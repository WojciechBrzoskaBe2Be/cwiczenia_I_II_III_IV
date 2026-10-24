"""Pobieranie plików oraz ich analiza i raportowanie wyników.

Moduł udostępnia procesor plików pobieranych z adresu URL, generator
wierszy, obliczanie statystyk oraz zapis raportów CSV.
"""

import time
import requests
import csv
from typing import Generator, Dict
from custom_errors import DownloadError, NotFoundError, AccessDeniedError
from pathlib import Path
from utils import operation_duration

class url_files_processor:
    """Pobiera pliki z URL i udostępnia operacje analizy ich zawartości."""

    url: str

    def __init__(self, url: str):
        """Zapisuje adres URL, z którego będą pobierane pliki."""
        self.url = url

    @operation_duration
    def get_file_from_url(self, file_name='latest.txt'):
        """Pobiera plik z przypisanego URL i zapisuje go pod wskazaną ścieżką.

        Parametr `file_name` określa ścieżkę docelową. Statusy 404 i 403 są
        sprawdzane przed zapisem, a pozostałe błędy HTTP przechodzą przez
        mechanizm biblioteki `requests`.
        """
        try:
            response = requests.get(self.url, stream=True)

            # 3. Obsługa kodów odpowiedzi serwera 404 i 403
            if response.status_code == 404:
                raise NotFoundError(f"(kod 404 dla URL: {self.url})")
            elif response.status_code == 403:
                raise AccessDeniedError(f"(kod 403 dla URL: {self.url})")

            # Dla pozostałych błędów HTTP (np. 500) używamy standardowego mechanizmu requests
            response.raise_for_status()
            """
                Gdy odpowiedź jest poprawna (kody sukcesu 2xx, np. 200 OK): Metoda nic nie robi – kod wykonuje się dalej 
                bez przerw.
                Gdy wystąpił błąd klienta lub serwera (kody 4xx lub 5xx, np. 404 Not Found, 500 Internal Server Error):
                Metoda natychmiast zgłasza wyjątek typu (tu błedy rodzaju 403 i  404 zostały przechwycone wcześniej)
                Oznacza to, że ta cześc kodu nie musi być 'przedłużeniem' 3. Obsługi kodów odpowiedzi serwera 404 i 403 i 
                działa niezaleznie
            """
            with open(file_name, 'wb') as f:
                for any_chunk in response.iter_content(chunk_size=8192):
                    if any_chunk:
                        f.write(any_chunk)

            print(f"Plik został pomyślnie pobrany i zapisany jako: {file_name}")

        # Przechwytywanie naszych zdefiniowanych wyjątków
        except NotFoundError as e:
            raise NotFoundError(f"[BŁĄD 404]: {e}")
            #print(f"[BŁĄD 404]: {e}")
        except AccessDeniedError as e:
            raise NotFoundError("[BŁĄD 403]: {e}")
            #print(f"[BŁĄD 403]: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Wystąpił inny błąd sieciowy/HTTP: {e}")
        finally:
            pass


    @staticmethod
    @operation_duration
    def read_file_lazy(file_name: str):
        """Zwraca kolejne wiersze pliku jako generator.

        Odczyt jest leniwy — wiersze są udostępniane po kolei, bez
        wczytywania całego pliku do pamięci.
        """
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            for row in f:
                yield row


    @staticmethod
    @operation_duration
    def get_some_statistics(sequence: Generator):
        """Oblicza statystyki liczbowe i wskazuje brakujące wartości w wierszach.

        Dla każdego wiersza zwraca jego indeks, wartość `avg`, sumę wartości
        liczbowych oraz indeksy kolumn oznaczonych znakiem `-`. Dla maksymalnie
        30 wartości liczbowych `avg` jest sumą podzieloną przez ich liczbę
        pomniejszoną o jeden; przy większej liczbie dzielnikiem jest ich liczba.
        """
        current_idx = 0
        for line in sequence:
            current_idx += 1
            numeric_values = [float(v) for v in line.split(',') if v not in ['-', '-\n']]
            total_numeric_values = sum(numeric_values)
            get_avg = lambda total, n: total / (n - 1) if n <= 30 else total / n
            avg = get_avg(total_numeric_values, len(numeric_values))
            not_numeric_values = [i for i, v in enumerate(line.split(',')) if v in ['-', '-\n']]
            yield {'idx_line': current_idx, 'avg': avg, 'total_numeric_values': total_numeric_values,
                   'not_numeric_values_columns': not_numeric_values}


    @staticmethod
    @operation_duration
    def report(sequence: Generator, numeric_values_report: str, missing_values_report: str):
        """Zapisuje wyniki analizy do raportów wartości i braków w formacie CSV.

        Istniejące pliki raportów są usuwane przed rozpoczęciem zapisu.
        `numeric_values_report` przechowuje indeks wiersza, średnią i sumę;
        `missing_values_report` przechowuje indeks wiersza oraz indeksy
        kolumn z brakującymi wartościami.
        """
        file_path_num_values_report = Path(numeric_values_report)
        file_path_missing_values_report = Path(missing_values_report)
        try:
            # Check if it exists and remove it

            if file_path_num_values_report.exists():
                file_path_num_values_report.unlink()

            if file_path_missing_values_report.exists():
                file_path_missing_values_report.unlink()

            i = 0
            for result in sequence:
                if i == 0:
                    with open(numeric_values_report, "w", newline="\n", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([result['idx_line'], result['avg'], result['total_numeric_values']])
                    with open(missing_values_report, "w", newline="\n", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([result['idx_line']]+ result['not_numeric_values_columns'])
                else:
                    with open(numeric_values_report, "a", newline="\n", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([result['idx_line'], result['avg'], result['total_numeric_values']])
                    with open(missing_values_report, "a", newline="\n", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([result['idx_line']]+ result['not_numeric_values_columns'])
                i += 1
        except FileNotFoundError:
            raise FileNotFoundError(f"Brak jednego ze wskazanych katalogów:{file_path_num_values_report}\n{file_path_missing_values_report}")
