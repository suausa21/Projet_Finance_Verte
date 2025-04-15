import pandas as pd
import streamlit as st
import numpy as np
from scipy.stats import norm
import statsmodels.api as sm
import matplotlib.pyplot as plt
import yfinance as yf

class strategies: #backtest une stratégie saisie par l'utilisateur

    def __init__(self, actifs:list, entrants : str, df_test: pd.DataFrame, df_strat: pd.DataFrame): #df test (rendements): data frame de données pour déterminer les pondérations du portefeuille ; df_strat : data frame de données pour calculer la performance du portefeuille
        self.actifs_user = actifs
        self.entrants = entrants #entrants de la stratégie/choix de l'utilisateur (ex : minimisation, ratio...)
        self.df_test = df_test
        self.df_strat = df_strat #données réelles
        return
    
    def calcul_resultat(self): 
        strategie = self.strategie_index()
        strategie_reelle = self.strategie_stats_reelles(strategie)
        perf_esperee = self.calculate_portfolio_stats(strategie, "Espérée", self.df_test)
        perf_reelle = self.calculate_portfolio_stats(strategie_reelle, "Réelle", self.df_strat)
        performance = self.perf(perf_esperee,perf_reelle)
        weights = strategie["Weight"].to_dict()
        df_combined = self.portfolio_benchmark(self.df_strat, weights)
        print(self.portfolio_alpha_beta(df_combined))
        plot = self.plot_portfolio_vs_benchmark(df_combined)
        return strategie, performance, plot
    
    #Fonction calculant les statistiques descriptives à partir des données des actions
    def calcul_stats_descriptives(self, rf: float = 0.02) -> pd.DataFrame:
        df_rendements = self.df_test.copy()
        stats = pd.DataFrame()
        stats['Rendement moyen annualisé'] = df_rendements.mean() * 252
        stats['Volatilité annualisée'] = df_rendements.std() * np.sqrt(252)
        stats['Skewness'] = df_rendements.skew()
        stats['Kurtosis'] = df_rendements.kurtosis()
        stats['Rendement minimum'] = df_rendements.min()
        stats['Rendement maximum'] = df_rendements.max()
        stats['Sharpe Ratio'] = (stats['Rendement moyen annualisé'] - rf) / stats['Volatilité annualisée']
        cumul_perf = (1 + df_rendements).cumprod()
        max_drawdowns = cumul_perf / cumul_perf.cummax() - 1
        stats['Max Drawdown'] = max_drawdowns.min()

        return stats

    def strategie_index(self) -> pd.DataFrame: #A afficher dans les résultats
        objective = self.entrants
     
        df_portfolio = self.calcul_stats_descriptives().copy()
        # Vérifier que le DataFrame contient les colonnes nécessaires
        colonnes_requises = ["Rendement moyen annualisé", "Volatilité annualisée", "Sharpe Ratio", "Skewness"]
        #Vérification 
        for col in colonnes_requises:
            if col not in df_portfolio.columns:
                raise ValueError(f"Colonne requise '{col}' manquante dans le DataFrame.")

        if objective == 'Rendement moyen annualisé':
            # Poids proportionnels aux rendements annualisés
            col_returns = "Rendement moyen annualisé"
            df_portfolio["Weight"] = df_portfolio[col_returns] / df_portfolio[col_returns].sum()

        elif objective == 'Sharpe Ratio':
            # Poids proportionnels au ratio de Sharpe
            col_sharpe = "Sharpe Ratio"
            df_portfolio["Weight"] = df_portfolio[col_sharpe] / df_portfolio[col_sharpe].sum()

        elif objective == 'Volatilité annualisée':
        # Poids proportionnels à 1 / volatilité
        # (les actifs avec une faible volatilité obtiennent un poids plus élevé)
            col_vol = "Volatilité annualisée"
            df_portfolio["InvVol"] = 1.0 / df_portfolio[col_vol]
            df_portfolio["Weight"] = df_portfolio["InvVol"] / df_portfolio["InvVol"].sum()
            df_portfolio.drop(columns=["InvVol"], inplace=True)
        
        elif objective == "Skewness":
            df_portfolio = df_portfolio[df_portfolio["Skewness"]>=0]
            df_portfolio["Weight"] = df_portfolio["Skewness"]/df_portfolio["Skewness"].sum()
        
        else:
            raise ValueError("L'objectif doit être l'une des valeurs suivantes : 'Rendement moyen annualisé', 'Ratio de sharpe', 'Volatilité', 'Skewnesss")

       
        # Forcer les poids négatifs à 0
        df_portfolio["Weight"] = df_portfolio["Weight"].clip(lower=0)
    
        # Renormaliser pour que la somme des poids soit égale à 1
        total_weight = df_portfolio["Weight"].sum()
        if total_weight > 0:
            df_portfolio["Weight"] = df_portfolio["Weight"] / total_weight
        else:
            raise ValueError("Tous les poids sont nuls après suppression des valeurs négatives.")
        
        return df_portfolio
    
    def strategie_stats_reelles(self, strategie:pd.DataFrame)-> pd.DataFrame:
        #Calcul des statistiques descriptives avec les données de marchés
        statistiques = self.calcul_stats_descriptives()
        #Concaténation entre poids et données stats descriptives
        strat_perf = pd.merge(statistiques, strategie["Weight"], right_index = True, left_index = True)
        return strat_perf

    #Calcule les statistiques du portefeuille à partir d'un DataFrame.
    def calculate_portfolio_stats(self, df: pd.DataFrame, strat:str, donnees: pd.DataFrame) -> pd.DataFrame:
        df_resultats = pd.DataFrame(index=["Rendement", "Volatilité", "Ratio de Sharpe", "Skewness", "Kurtosis", "VaR à 95%"], columns=[f"Performance {strat}"])
       #Rendement
        print(df)
        port_return = (df["Weight"] * df["Rendement moyen annualisé"]).sum()
        df_resultats.loc["Rendement",f"Performance {strat}"] = port_return
        #Volatilité
        matrice = donnees.loc[:,donnees.columns.intersection(df.index)]
        Matrice_Cov = matrice.cov()
        cov_matrix = df["Weight"].values @ Matrice_Cov @ df["Weight"].values.T
        port_volatility = np.sqrt(cov_matrix)
        df_resultats.loc["Volatilité",f"Performance {strat}"] = port_volatility
        #Ratio de Sharpe
        df_resultats.loc["Ratio de Sharpe",f"Performance {strat}"] = port_return / port_volatility if port_volatility != 0 else None
        #Skewness
        df_resultats.loc["Skewness",f"Performance {strat}"] = (df["Weight"] * df["Skewness"]).sum()
        #Kurtosis
        df_resultats.loc["Kurtosis",f"Performance {strat}"] = (df["Weight"] * df["Kurtosis"]).sum()
        #VaR à 95%
        df_resultats.loc["VaR à 95%",f"Performance {strat}"] = -port_return + norm.ppf(0.05) * port_volatility
        return df_resultats

   #Fonction pour avoir un bel affichage
    def perf(self, portf_esp,portf_reelles) -> pd.DataFrame:
        performance = pd.merge(portf_esp,portf_reelles, right_index = True, left_index = True)
        return performance
    
    def portfolio_benchmark(self, df_rendements: pd.DataFrame, weights: dict,benchmark_ticker:str = "^GSPC") -> pd.DataFrame:
        # Déterminer la plage de dates à partir du DataFrame du portefeuille
        start_date = self.df_strat.index.min().strftime('%Y-%m-%d')
        end_date = self.df_strat.index.max().strftime('%Y-%m-%d')

        # Télécharger les données du benchmark pour la même période
        benchmark_data = yf.download(benchmark_ticker, start=start_date, end=end_date, auto_adjust=True)
        if benchmark_data.empty:
            raise ValueError(f"Aucune donnée pour le benchmark {benchmark_ticker}.")  
        
        # Calculer les rendements quotidiens du benchmark (à partir des prix de clôture ajustés)
        benchmark_data["Daily_Return"] = benchmark_data["Close"].pct_change()
        benchmark_returns = benchmark_data["Daily_Return"].dropna()

        # Vérifier que toutes les actions présentes dans le dictionnaire de poids se trouvent dans le df
        missing_cols = [stock for stock in weights if stock not in df_rendements.columns]
        if missing_cols:
            raise ValueError(f"Les colonnes suivantes sont manquantes dans df_rendements: {missing_cols}")
    
        # Calculer les rendements quotidiens du portefeuille en faisant la somme pondérée
        # On sélectionne les colonnes qui correspondent aux actions en portefeuille, et on élimine les dates avec des NaN.
        df_portfolio = df_rendements[list(weights.keys())].dropna().copy()
        # Initialiser une colonne pour le rendement du portefeuille
        df_portfolio["Portfolio_return"] = 0.0
        for stock, w in weights.items():
            df_portfolio["Portfolio_return"] += df_portfolio[stock] * w

        # Aligner les dates entre le rendement du portefeuille et du benchmark
        df_combined = df_portfolio.join(benchmark_returns, how='inner')

        return df_combined

    #Fonction pour comparer le portefeuille à un benchmark
    def portfolio_alpha_beta(self,df_combined: pd.DataFrame,freq: int = 252) -> dict:
    # La colonne provenant du benchmark est nommée "Daily_Return"
    
    # Régression linéaire : rendement du portefeuille = alpha_daily + beta * rendement benchmark
        y = df_combined['Portfolio_return']
        X = df_combined['Daily_Return']
        X = sm.add_constant(X)   # Ajoute une constante pour estimer l'intercept (alpha)
    
        model = sm.OLS(y, X).fit()
    
        alpha_daily = model.params['const']
        beta = model.params['Daily_Return']
    
    # Annualiser l'alpha quotidien : (1 + alpha_daily)^freq - 1
        if (1 + alpha_daily) > 0:
            alpha_annualized = (1 + alpha_daily)**freq - 1
        else:
            alpha_annualized = np.nan  # Si alpha_daily est très négatif, l'exponentiation n'est pas valide

        return {
            "Alpha Annualized": alpha_annualized,
            "Beta": beta,
        }
    
    def plot_portfolio_vs_benchmark(self,df_combined: pd.DataFrame, benchmark_ticker:str = "^GSPC") -> plt.Figure:
    # Créer le graphique
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(df_combined.index, df_combined["Portfolio_return"], label="Rendement Portefeuille", color="blue")
        ax.plot(df_combined.index, df_combined["Daily_Return"], label=f"Rendement Benchmark ({benchmark_ticker})", color="red")
    
        ax.set_title("Rendements Quotidiens : Portefeuille vs Benchmark")
        ax.set_xlabel("Date")
        ax.set_ylabel("Rendements Quotidiens (exprimés en décimal)")
        ax.legend()
        ax.grid(True)
    # Retourner la figure pour qu'elle puisse être affichée ou enregistrée
        return fig

