import pandas as pd
import numpy as np

class indice_score:
    def __init__(self, donnees:pd.DataFrame):
        self.df = donnees
        self.actifs = donnees[["Company Name", "HQ"]] #Pour avoir actif + pays
        return
    
    def run(self):
        data_score = self.data_score(self.df)
        score = self.actifs_fonds(data_score)
        return score

    def data_score(self, donnees) -> pd.DataFrame:
        # Définition des groupes de colonnes selon la classification ESG (indices)
        colonnes_impact_direct = [16, 10, 12]
        colonnes_impact_indirect = [14, 15, 20]
        colonnes_risques_non_climatiques = [8, 9, 18]

    # Extraction des sous-tableaux correspondant à ces groupes
        groupe_impact_direct = donnees.iloc[:, colonnes_impact_direct].reset_index(drop=True)
        groupe_impact_indirect = donnees.iloc[:, colonnes_impact_indirect].reset_index(drop=True)
        groupe_risques = donnees.iloc[:, colonnes_risques_non_climatiques].reset_index(drop=True)

    # Récupération de la liste des entreprises
        entreprises = donnees["Company Name"].reset_index(drop=True)

    # Fonction de normalisation des chiffres (plus haut = meilleur score)
        def normalisation(serie):
            serie = serie.astype(str).str.strip()                        # Nettoyage des espaces
            serie = pd.to_numeric(serie, errors='coerce')               # Conversion en numérique
            if serie.max() == serie.min():                              # Cas où tous les chiffres sont égaux
                return pd.Series([1.0] * len(serie), index=serie.index)
            else:
                return (serie - serie.min()) / (serie.max() - serie.min())

    # Fonction de calcul des sous-scores à partir d’un groupe
        def calculer_sous_score(group):
            scores_colonnes = []
            for _, colonne in group.items():                            # On récupère les colonnes du groupe
                score_normalisé = normalisation(colonne)
                scores_colonnes.append(score_normalisé)
            return pd.concat(scores_colonnes, axis=1).mean(axis=1, skipna=True), pd.concat(scores_colonnes, axis=1)  # Moyenne des colonnes (par entreprise) + les sous groupes

    # Calcul de chaque sous-score (impact direct / indirect / risques non-climatiques)
        score_impact_direct, sous_score_direct = calculer_sous_score(groupe_impact_direct)
     
        sous_score_direct.columns = [
            ("Impact Climatique", "Émissions"),
            ("Impact Climatique", "Politique d’efficacité énergétique"),
            ("Impact Climatique", "Part des énergies renouvelables")
            ]   
        sous_score_direct[("Impact Climatique", "Total")] = score_impact_direct
        
        score_impact_indirect, sous_scores_indirect = calculer_sous_score(groupe_impact_indirect)

        sous_scores_indirect.columns = [
            ("Impact Indirect", "Gestion chaîne d'approvisionnement"),
            ("Impact Indirect", "Surveillance environnementale"),
            ("Impact Indirect", "Minimisation impact produit")
        ]
        sous_scores_indirect[("Impact Indirect", "Total")] = score_impact_indirect

        score_risques, sous_scores_risques = calculer_sous_score(groupe_risques)

        sous_scores_risques.columns = [
            ("Risques non climatiques", "Utilisation des ressources"),
            ("Risques non climatiques", "Politique d’efficacité de l’eau"),
            ("Risques non climatiques", "Réduction des déchets électroniques")
        ]   
        sous_scores_risques[("Risques non climatiques", "Total")] = score_risques

        df_base = pd.DataFrame({
            ("Innovation", "Innovation Environnementale"): donnees.iloc[:, 7].reset_index(drop=True),
            ("ESG Général", "ESG Indice"): donnees.iloc[:, 6].reset_index(drop=True),
        }, index=entreprises)

        # Fusionner tous les blocs pour avoir le data frame multi-index
        df_presentation = pd.concat([sous_score_direct, sous_scores_indirect, sous_scores_risques], axis=1)
        df_presentation.insert(0, ("ESG Général", "ESG Indice"), donnees.iloc[:, 6])
        df_presentation.insert(1, ("Innovation", "Innovation Environnementale"), donnees.iloc[:, 7])
        df_presentation.columns = pd.MultiIndex.from_tuples(df_presentation.columns)
        df_presentation.index.name = "Company Name"
        df_presentation.index=entreprises

        return df_presentation

    #Fonction qui renvoie les actifs qui on un score > 0.5 (par defaut)
    def actifs_fonds(self, df_score:pd.DataFrame, seuil : float = 0.5) -> tuple[pd.DataFrame, pd.DataFrame]:
        totaux_multi = [col for col in df_score.columns if isinstance(col, tuple) and col[1] == 'Total']
        colonnes_globales = [col for col in df_score.columns if isinstance(col, tuple) and col[0] in ['ESG Général', 'Innovation']]
        colonnes_à_moyenner = totaux_multi + colonnes_globales
        df_score['Score'] = df_score[colonnes_à_moyenner].mean(axis=1)
        list_actif = df_score.index.tolist()
        actifs = self.actifs.copy()
        actifs_pays = actifs[actifs["Company Name"].isin(list_actif)]
        return df_score, actifs_pays
    


class indice_user:
    def __init__(self, df_home : pd.DataFrame, poids:list):
        #Liste des poids saisie par l'utilisateur
        self.poids = poids
        #Définition du profil de l'utilisateur
        if len(poids)> 5:
            self.profil = "Expert"
        else:
            self.profil = "Normal"
        self.df_fonds = df_home
        return 
    
    def scoring(self):
        if self.profil == "Expert":
            df_score = self.score_expert()
        else:
            df_score = self.score_normal()
        list_actifs = self.actifs_users(df_score)[0]
        return df_score, list_actifs

 #Fonction qui calcule le score normal 
    def score_normal(self) -> pd.DataFrame:
        df_score = self.df_fonds.copy()
        totaux_multi = [col for col in df_score.columns if isinstance(col, tuple) and col[1] == 'Total']
        colonnes_globales = [col for col in df_score.columns if col[0] in ['ESG Général', 'Innovation']]
        colonnes_utiles = totaux_multi + colonnes_globales

        if len(self.poids) != len(colonnes_utiles):
            raise ValueError(f"Nombre de poids ({len(self.poids)}) ≠ nombre de critères ({len(colonnes_utiles)}).")

        # Calcul du score utilisateur
        data = df_score.loc[:, colonnes_utiles].values.astype(float)
        weights = np.array(self.poids, dtype=float)
        all_nan = np.isnan(data).all(axis=1)
        data_filled = np.where(np.isnan(data), 0, data)
        weights_matrix = np.broadcast_to(weights, data.shape)
        weights_effective = np.where(np.isnan(data), 0, weights_matrix)
        weighted_sum = np.sum(data_filled * weights_effective, axis=1)
        weight_sum = np.sum(weights_effective, axis=1)
        score_utilisateur = weighted_sum / weight_sum
        score_utilisateur[all_nan] = np.nan
        df_score['Score_utilisateur'] = score_utilisateur

        return df_score
    
    #Fonction qui calcule le score expert
    def score_expert(self) -> pd.DataFrame:
        df_score = self.df_fonds.copy()
        sous_groupes = [col for col in df_score.columns 
                        if col[1] not in ['Total'] 
                        and col[0] in ['Impact Climatique', 'Impact Indirect', 'Risques non climatiques']]
        colonnes_globales = [col for col in df_score.columns if col[0] in ['ESG Général', 'Innovation']]
        colonnes_utiles = sous_groupes + colonnes_globales
        print(len(colonnes_utiles))
        if len(self.poids) != len(colonnes_utiles):
            raise ValueError(f"Nombre de poids ({len(self.poids)}) ≠ nombre de critères ({len(colonnes_utiles)}).")

        # Calcul du score utilisateur
        data = df_score.loc[:, colonnes_utiles].values.astype(float)
        weights = np.array(self.poids, dtype=float)
        all_nan = np.isnan(data).all(axis=1)
        data_filled = np.where(np.isnan(data), 0, data)
        weights_matrix = np.broadcast_to(weights, data.shape)
        weights_effective = np.where(np.isnan(data), 0, weights_matrix)
        weighted_sum = np.sum(data_filled * weights_effective, axis=1)
        weight_sum = np.sum(weights_effective, axis=1)
        score_utilisateur = weighted_sum / weight_sum
        score_utilisateur[all_nan] = np.nan
        df_score['Score_utilisateur'] = score_utilisateur

        return df_score

    #Fonction qui renvoie les actifs sélectionnés par l'utilisateur
    def actifs_users(self, df_score: pd.DataFrame) -> tuple[list, pd.DataFrame]:
        actifs_selectionnes = df_score.sort_values('Score_utilisateur', ascending=False).index.tolist()
        return actifs_selectionnes, df_score

        

