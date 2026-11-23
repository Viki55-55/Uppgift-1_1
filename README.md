# Hälsodata – statistisk analys

Projektet täcker Del 1 och de synliga kraven i Del 2: beskrivande statistik,
grafer, simulering, konfidensintervall, hypotesprövning, power-simulering,
funktioner, klass och linjär regression.

## Projektstruktur

```text
health-analysis-project/
├── data/
│   └── health_study_dataset.csv  # lägg datasetet här
├── notebooks/
│   └── del1_analysis.ipynb
├── src/
│   ├── __init__.py
│   └── health_analyzer.py
├── del2_pipeline.py
├── KODFORKLARING.md          # svenska förklaringar till centrala kodblock
├── ANALYSRESULTAT.md          # färdig resultattext från bifogade data
├── requirements.txt
└── README.md
```

## Förutsättningar

CSV-filen ska minst innehålla:

`age`, `weight`, `height`, `systolic_bp`, `cholesterol`, `disease`, `smoker`

För boxploten används även `sex`. I det bifogade datasetet är `disease` kodad
som 0/1 och `smoker` som `Yes/No`; koden hanterar dessa format.

## Installation i VS Code

1. Installera Python 3.11 eller senare, Git och VS Code.
2. Installera VS Code-tilläggen **Python** och **Jupyter** från Microsoft.
3. Öppna projektmappen i VS Code via **File → Open Folder**.
4. Öppna terminalen via **Terminal → New Terminal**.
5. Skapa virtuell miljö:

   Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

6. Installera paketen:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Tryck `Ctrl+Shift+P`, välj **Python: Select Interpreter** och välj `.venv`.
8. Lägg den bifogade CSV-filen som `data/health_study_dataset.csv`.
9. Öppna `notebooks/del1_analysis.ipynb`, välj `.venv` som kernel och kör **Run All**.

## GitHub och branch del1

Skapa först ett tomt repository på GitHub, utan README eller `.gitignore`. Kör sedan:

```bash
git init
git add .
git commit -m "Skapa grundstruktur för hälsodataanalys"
git branch -M main
git remote add origin https://github.com/DITT-NAMN/DITT-REPO.git
git push -u origin main

git switch -c del1
git add notebooks/del1_analysis.ipynb README.md requirements.txt
git commit -m "Genomför del 1 statistisk analys"
git push -u origin del1
```

Ersätt `DITT-NAMN/DITT-REPO` med din GitHub-adress. Kontrollera på GitHub att
branchen `del1` innehåller notebooken och att alla celler visar sparade resultat.

## Del 2

Byt tillbaka till main och skapa en separat branch:

```bash
git switch main
git switch -c del2
python del2_pipeline.py
git add .
git commit -m "Strukturera analysen i funktioner och klass"
git push -u origin del2
```

## Viktigt i inlämningen

- Kör alla notebookceller i ordning och spara notebooken.
- Beskriv effekten i originalenheten, inte bara p-värdet.
- Redovisa osäkerheten med konfidensintervall.
- Ange metod och varför den valts.
- Skriv begränsningar: observationsdata visar inte orsak, saknade värden kan
  påverka resultatet, testets antaganden måste kontrolleras och simuleringen
  förenklar verkligheten genom att anta samma sannolikhet för alla personer.

Läs `KODFORKLARING.md` för en svensk genomgång av kodblocken, klassen och de
viktigaste statistiska funktionerna.

