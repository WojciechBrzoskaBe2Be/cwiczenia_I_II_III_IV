"""Uruchomienie przykładowego procesu pobrania i analizy pliku.

Skrypt pobiera dane z adresu URL, odczytuje je wiersz po wierszu,
oblicza statystyki i zapisuje raporty CSV.
"""

from file_processor import url_files_processor
from utils import operation_duration

# Adresy testowe zwracające odpowiednio błędy HTTP 404, 403 oraz poprawny plik.
URL_TO_FORCE_ERROR_404 = "https://oleksandr-fedoruk.com/sggw/podyplomowe/404"
URL_TO_FORCE_ERROR_403 = "https://oleksandr-fedoruk.com/sggw/podyplomowe/403"
URL_OK = "https://oleksandr-fedoruk.com/sggw/podyplomowe/file"




if __name__ == '__main__':
    try:
        file_to_get=url_files_processor(URL_OK)

        sciezka = r'C:\\Users\\wbrzo\\OneDrive\\Pulpit\\rozne\\wyniki_badan.txt'

        file_to_get.get_file_from_url(sciezka)

        #pipeline processing read_file_lazy->get_some_statistics->report

        file_to_get.report(file_to_get.get_some_statistics(file_to_get.read_file_lazy(sciezka)),
                           'C:\\Users\\wbrzo\\OneDrive\\Pulpit\\rozne\\report.csv',
                           'C:\\Users\\wbrzo\\OneDrive\\Pulpit\\rozne\\missing_values.csv')

    except Exception as e:
        raise Exception(f'Error:{e}')
    finally:
        print(f"No matter what happened : it is time to clean up!")
