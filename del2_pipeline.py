from pathlib import Path

import pandas as pd

from src.health_analyzer import HealthAnalyzer


DATA_PATH = Path("data/health_study_dataset.csv")


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    analyzer = HealthAnalyzer(df, seed=42)

    columns = ["age", "weight", "height", "systolic_bp", "cholesterol"]
    print("Beskrivande statistik:\n", analyzer.descriptive_statistics(columns))
    print("Normal-KI:", analyzer.normal_ci("systolic_bp"))
    print("Bootstrap-KI:", analyzer.bootstrap_ci("systolic_bp"))
    print("Hypotesprov:", analyzer.smokers_vs_nonsmokers())

    model, r2 = analyzer.linear_regression(["age", "weight"])
    print("Regressionskoefficienter:", model.coef_)
    print("Intercept:", model.intercept_)
    print("R²:", r2)


if __name__ == "__main__":
    main()

