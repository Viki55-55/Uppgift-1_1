from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression


class HealthAnalyzer:
    """Samlar de viktigaste analyserna för hälsodatasetet.

    Klassen gör att vi slipper upprepa kod. När ett DataFrame-objekt har
    skickats in kan samma objekt användas för statistik, simulering,
    konfidensintervall, hypotesprov och regression.
    """

    def __init__(self, data: pd.DataFrame, seed: int = 42):
        # copy() skyddar originaldata från oavsiktliga ändringar.
        self.data = data.copy()
        # En fast seed gör att simuleringarna går att återskapa.
        self.rng = np.random.default_rng(seed)

    def descriptive_statistics(self, columns: list[str]) -> pd.DataFrame:
        """Returnerar medelvärde, median, min och max för valda kolumner."""
        return self.data[columns].agg(["mean", "median", "min", "max"]).T

    def disease_share(self, disease_col: str = "disease") -> float:
        """Beräknar andelen ettor i en binär sjukdomskolumn."""
        return float(self.data[disease_col].mean())

    def binary_column(self, column: str) -> pd.Series:
        """Gör om vanliga Ja/Nej-värden till 1/0.

        Datasetets smoker-kolumn innehåller 'Yes' och 'No'. Metoden fungerar
        även om en kolumn redan består av 1 och 0.
        """
        values = self.data[column]
        if pd.api.types.is_numeric_dtype(values):
            return values.astype(float)
        mapping = {"yes": 1, "no": 0, "ja": 1, "nej": 0}
        converted = values.astype(str).str.strip().str.lower().map(mapping)
        if converted.isna().any():
            raise ValueError(f"Kolumnen {column!r} innehåller oväntade värden.")
        return converted

    def simulate_disease(self, n: int = 1000, disease_col: str = "disease") -> np.ndarray:
        """Simulerar n personer med samma sjukdomssannolikhet som i data."""
        p = self.disease_share(disease_col)
        return self.rng.binomial(1, p, size=n)

    def normal_ci(self, column: str, confidence: float = 0.95) -> tuple[float, float]:
        """Beräknar konfidensintervall för medelvärdet med normalapproximation."""
        values = self.data[column].dropna().to_numpy()
        mean = values.mean()
        se = stats.sem(values)
        z = stats.norm.ppf(1 - (1 - confidence) / 2)
        return float(mean - z * se), float(mean + z * se)

    def bootstrap_ci(
        self, column: str, confidence: float = 0.95, n_boot: int = 10_000
    ) -> tuple[float, float]:
        """Beräknar ett percentilbaserat bootstrapintervall för medelvärdet."""
        values = self.data[column].dropna().to_numpy()
        boot_means = np.empty(n_boot)
        for i in range(n_boot):
            boot_means[i] = self.rng.choice(values, size=len(values), replace=True).mean()
        alpha = 1 - confidence
        low, high = np.quantile(boot_means, [alpha / 2, 1 - alpha / 2])
        return float(low), float(high)

    def smokers_vs_nonsmokers(
        self, smoker_col: str = "smoker", bp_col: str = "systolic_bp"
    ) -> dict[str, float]:
        """Jämför blodtryck med ett ensidigt Welch-test."""
        smoker_binary = self.binary_column(smoker_col)
        smokers = self.data.loc[smoker_binary == 1, bp_col].dropna()
        nonsmokers = self.data.loc[smoker_binary == 0, bp_col].dropna()
        # Welch-test: kräver inte samma varians i grupperna.
        result = stats.ttest_ind(smokers, nonsmokers, equal_var=False, alternative="greater")
        return {
            "mean_smokers": float(smokers.mean()),
            "mean_nonsmokers": float(nonsmokers.mean()),
            "effect": float(smokers.mean() - nonsmokers.mean()),
            "t_statistic": float(result.statistic),
            "p_value": float(result.pvalue),
        }

    def linear_regression(
        self, predictors: list[str], target: str = "systolic_bp"
    ) -> tuple[LinearRegression, float]:
        """Tränar en enkel linjär modell och returnerar modellen samt R²."""
        clean = self.data[predictors + [target]].dropna()
        x = clean[predictors].to_numpy()
        y = clean[target].to_numpy()
        model = LinearRegression().fit(x, y)
        return model, float(model.score(x, y))

