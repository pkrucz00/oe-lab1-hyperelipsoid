```markdown
# Projekt Algorytm Genetyczny

Projekt oparty na Flask, który implementuje algorytm genetyczny do optymalizacji funkcji wielu zmiennych. Aplikacja umożliwia konfigurację parametrów algorytmu (np. metoda selekcji, krzyżowania, mutacji, inwersji) poprzez przesyłanie JSON-a z formularza.

## Wymagania

- Python 3.7+
- Flask
- Inne zależności zapisane w `requirements.txt`

## Instalacja

1. **Sklonuj repozytorium:**

   ```bash
   git clone <adres_repozytorium>
   cd <nazwa_repozytorium>
   ```

2. **Utwórz środowisko wirtualne i zainstaluj zależności:**

   ```bash
   python -m venv venv
   # Na Linux/macOS:
   source venv/bin/activate
   # Na Windows:
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Uruchomienie aplikacji

1. **Uruchom serwer Flask:**

   ```bash
   python app.py
   ```

2. Aplikacja będzie dostępna pod adresem:  
   `http://127.0.0.1:5000`

## Testowanie API

- **Endpoint:**  
  `POST http://127.0.0.1:5000/api/ga/run`

- **Przykładowy JSON do wysłania (np. w Postmanie):**

  ```json
  {
    "function": "hyperellipsoid",
    "variables": 10,
    "population_size": 100,
    "epochs": 50,
    "search_range": [-65.536, 65.536],
    "precision": 6,
    "optimization_type": "minimization",
    "tournament_size": 3,
    "crossover_probability": 0.8,
    "mutation_probability": 0.1,
    "inversion_probability": 0.05,
    "elitism_count": 2,
    "selection_method": "tournament",
    "crossover_method": "one_point",
    "mutation_method": "one_point",
    "inversion_method": "simple"
  }
  ```

- **Opis:**  
  Po wysłaniu żądania aplikacja uruchamia algorytm genetyczny i zwraca JSON z:
  - `best_fitness` – najlepsza wartość funkcji celu,
  - `best_individual` – zdekodowaną wartość (x) najlepszego osobnika,
  - `history` – lista epok z najlepszymi wartościami (x oraz f(x)),
  - `time` – czas wykonania obliczeń.

## Struktura projektu

```
backend/
 ├── app.py                # Punkt wejścia do aplikacji Flask
 ├── controllers/          # Endpointy (np. ga_controller.py)
 ├── models/               # Modele: Chromosome, Individual, Population, FitnessFunction
 └── services/             # Logika algorytmu genetycznego (ga_service.py) i operatorzy (operators.py)
```

## Uwagi

- Aplikacja wykorzystuje mechanizm Blueprint do modularnej organizacji endpointów.
- Parametry algorytmu (metody selekcji, krzyżowania, mutacji, inwersji) są dynamicznie dobierane na podstawie JSON-a przesłanego przez użytkownika.
- Projekt można łatwo rozbudować o dodatkowe funkcjonalności, np. zapis wyników do bazy danych lub generowanie wykresów historii ewolucji.

```
