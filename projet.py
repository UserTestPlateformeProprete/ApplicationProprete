import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

#df = pd.read_csv("https://raw.githubusercontent.com/UserTestPlateformeProprete/ApplicationProprete/main/grille_salaires_proprete.csv", sep=";")
df = pd.read_csv("grille_salaires_proprete.csv", sep=";")


def calculateur():
    st.title("Calculateur de salaires dans le cadre d'un contrat à temps partiel dans le domaine de la propreté")
    salaire_horaire = st.number_input("Entrez votre salaire brut horaire :")
    heures_contractuelles = st.number_input("Entrez le nombre d'heures mensuelles contractuelles :")
    heures_effectuees = st.number_input("Entrez le nombre d'heures réellement effectuées ce mois-ci :")

    heures_complementaires = heures_effectuees-heures_contractuelles
    
    heures_tranche11 = 0.1*heures_contractuelles
    heures_tranche25 = heures_effectuees-(heures_contractuelles+heures_tranche11)

    st.write("Votre nombre d'heures complémentaires effectuées ce mois-ci est de : ",heures_complementaires," heures.")
    st.write("Vous avez effectué ",heures_tranche11, " heures dans la tranche valorisée à 11%")
    st.write("Vous avez effectué ",heures_tranche25, " heures dans la tranche valorisée à 25%")

    salaire = salaire_horaire * heures_contractuelles + heures_tranche11*(salaire_horaire*1.11) + heures_tranche25*(salaire_horaire*1.25)
    st.write("Votre salaire brut mensuel est de :", salaire, "euros.")

def niveau():
    # Créer l'interface utilisateur
    st.title('Calculateur de salaire')

    # Obtenir les valeurs uniques de la colonne "CATEGORIE"
    categorie_unique = df['CATEGORIE'].unique().tolist()

    # Ajouter un selectbox pour que l'utilisateur choisisse une catégorie
    categorie_selectionnee = st.selectbox('Sélectionnez une catégorie', categorie_unique)

  
    categorie_df = df[df['CATEGORIE'] == categorie_selectionnee]

    # Obtenir les valeurs uniques de la colonne "NIVEAU / ECHELON"
    echelon_niveau_unique = categorie_df['NIVEAU / ECHELON'].unique().tolist()

    # Ajouter un selectbox pour que l'utilisateur choisisse une information
    echelon_niveau_selectionnee = st.selectbox('Sélectionnez échelon / niveau', echelon_niveau_unique)

    # Filtrer le DataFrame pour n'inclure que les lignes correspondant à la catégorie et à l'échelon/niveau sélectionnés
    echelon_niveau_df = categorie_df[categorie_df['NIVEAU / ECHELON'] == echelon_niveau_selectionnee]


    # Obtenir la liste des colonnes restantes
    colonnes_restantes = [colonne for colonne in df.columns if colonne not in ['CATEGORIE', 'NIVEAU / ECHELON']]

    # Ajouter un selectbox pour que l'utilisateur choisisse un taux horaire
    taux_horaire_selectionne = st.selectbox('Sélectionnez un taux horaire', echelon_niveau_df[colonnes_restantes].columns.tolist())

    # Afficher les informations correspondantes à la catégorie, l'échelon/niveau et le taux horaire sélectionnés
    #st.write(echelon_niveau_df[['CATEGORIE', 'NIVEAU / ECHELON', taux_horaire_selectionne]])
    #st.write(taux_horaire_selectionne)
    echelon_niveau_df=echelon_niveau_df[['CATEGORIE', 'NIVEAU / ECHELON', taux_horaire_selectionne]]
    salaire=echelon_niveau_df.iloc[:,-1:]
    salaire_valeur=salaire.values[0][0]
    st.write('Votre salaire horaire est de : ', salaire_valeur, ' €')

def manque_a_gagner():
    st.title("Manque à gagner")
    temps_travail_mensuel = st.number_input("Entrez le nombre d'heures mensuelles")
    pourcentage = st.number_input("En moyenne, votre rémunération a été supérieure au SMIC de : (en %)")
    pourcentage=pourcentage/100

    # Les données sont stockées dans un DataFrame Pandas pour faciliter les calculs
    data = pd.DataFrame({
        'annee': range(1999, 2024),
        'smic_horaire': [40.72, 42.02, 43.72, 6.83, 7.19, 7.61, 8.03, 8.27, 8.44, 8.71, 8.63, 8.82, 8.86, 9.22, 9.43, 9.53, 9.61, 9.67, 9.76, 9.88, 10.03, 10.15, 10.48, 11.07, 11.27],
        'inflation': [0.5, 1.7, 1.6, 1.9, 2.1, 2.1, 1.7, 1.7, 1.5, 2.8, 0.1, 1.5, 2.1, 2.0, 0.9, 0.5, 0.0, 0.2, 1.0, 1.8, 1.1, 0.5, 1.6, 5.2, np.nan],
        'abattement': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.09, 0.08, 0.07, 0.06]
    })

    # Calcul du salaire brut et net annuel pour chaque année
    data['salaire_net']=(data['smic_horaire'] * (1+pourcentage))
    data['salaire_brut_mensuel'] = (data['salaire_net'] * temps_travail_mensuel)
    data['salaire_brut_annuel'] = data['salaire_net'] * temps_travail_mensuel * 12
    data['inflation_multiplicateur']=1+(data['inflation']/100)
    
    facteur_inflation_cumul=[]
    resultat=1
    facteur_inflation_cumul.insert(0,np.nan)
    for i in reversed(range(len(data['inflation_multiplicateur'])-1)):
        resultat = resultat * data['inflation_multiplicateur'][i]
        facteur_inflation_cumul.insert(0,resultat)
    
    data['facteur_inflation_cumul'] = facteur_inflation_cumul

    data['salaire_annuel_brut_apres_abat']= data['salaire_brut_annuel']*(1-data['abattement'])
    data['brut_non_abattu']=data['salaire_brut_annuel']* data['facteur_inflation_cumul']
    data['brut_non_abattu_euro']=data['brut_non_abattu']
    data['brut_non_abattu_euro'][:3] = [x/6.56 for x in data['brut_non_abattu_euro'][:3]]
    data['brut_abattu']=data['brut_non_abattu']*(1-data['abattement'])
    data['brut_abattu_euro']=data['brut_abattu']
    data['brut_abattu_euro'][:3] = [x/6.56 for x in data['brut_abattu_euro'][:3]]
    data['smic_brut']=data['smic_horaire']*temps_travail_mensuel*data['facteur_inflation_cumul']*12
    data['smic_brut_euro']= data['smic_brut']
    data['smic_brut_euro'][:3] = [x/6.56 for x in data['smic_brut_euro'][:3]]

    data['colonne_s']= data['brut_abattu_euro']*0.8+( data['brut_non_abattu_euro']-data['brut_abattu_euro'])
    data['colonne_t']= data['brut_non_abattu_euro']*0.8
    data['colonne_u']=data['colonne_s']-data['colonne_t']
    data['colonne_v']=data['colonne_u']/12

    moyenne_salaire_brut_non_abattu_euro = data['brut_non_abattu_euro'].mean()
    moyenne_salaire_brut_abattu_euro = data['brut_abattu_euro'].mean()
    moyenne_smic_brut = data['smic_brut_euro'].mean()
    moyenne_somme_cotisations_sans_abattement=data['colonne_s'].mean()
    moyenne_somme_cotisations_avec_abattement=data['colonne_t'].mean()
    moyenne_economie_cotisations_court_terme_an=data['colonne_u'].mean()
    moyenne_economie_cotisations_court_terme_mois=data['colonne_v'].mean()
    # Affichage des résultats
    st.write('Voici la grille de salaires :')
    df=data[['annee', 'smic_horaire','salaire_net','salaire_brut_mensuel','salaire_brut_annuel','inflation','facteur_inflation_cumul','abattement','salaire_annuel_brut_apres_abat','brut_non_abattu','brut_non_abattu_euro','brut_abattu','brut_abattu_euro','smic_brut','smic_brut_euro','colonne_s','colonne_t','colonne_u','colonne_v']]
    df.columns = ['Année', 'Smic Horaire', 'Salaire Net', 'Salaire Brut Mensuel', 'Salaire Brut Annuel', 'Inflation', "Facteur d'Inflation Cumulé", 'Abattement', 'Salaire Annuel Brut après Abattement', 'Brut Non Abattu', 'Brut Non Abattu en Euro', 'Brut Abattu', 'Brut Abattu en Euro', 'Smic Brut', 'Smic Brut en Euro','Somme des cotisations sans abattement','Somme des cotisations avec abattement','Economie de cotisations salariales à court terme par an','Par mois']
    st.write(df.style.format({"Smic Horaire": "{:.2f}", "Salaire Net": "{:.2f}", "Salaire Brut Mensuel": "{:.2f}", "Salaire Brut Annuel": "{:.2f}", "Inflation": "{:.2f}", "Multiplicateur d'Inflation": "{:.3f}", "Facteur d'Inflation Cumulé": "{:.2f}", "Abattement": "{:.2f}", "Salaire Annuel Brut après Abattement": "{:.2f}", "Brut Non Abattu": "{:.2f}", "Brut Non Abattu en Euro": "{:.2f}", "Brut Abattu": "{:.2f}","Brut Abattu en Euro": "{:.2f}", "Smic Brut": "{:.2f}","Smic Brut en Euro": "{:.2f}"}))
    st.write("Salaire annuel moyen brut non abattu","%.2f" % moyenne_salaire_brut_non_abattu_euro," € (Sur la période de 1999 à 2023)")
    st.write("Salaire annuel moyen brut abattu","%.2f" % moyenne_salaire_brut_abattu_euro," € (Sur la période de 1999 à 2023)")
    st.write("Moyenne somme des cotisations sans abattement","%.2f" % moyenne_somme_cotisations_sans_abattement," € (Sur la période de 1999 à 2023)")
    st.write("Moyenne somme des cotisations avec abattement","%.2f" % moyenne_somme_cotisations_avec_abattement," € (Sur la période de 1999 à 2023)")
    st.write("Moyenne économie de cotisations salariales à court terme par an","%.2f" % moyenne_economie_cotisations_court_terme_an," € (Sur la période de 1999 à 2023)")
    st.write("Moyenne économie de cotisations salariales à court terme par mois","%.2f" % moyenne_economie_cotisations_court_terme_mois," € (Sur la période de 1999 à 2023)")

def about():
    st.write("Plateforme support pour l'aide au calcul et à la compréhension des salaires dans le cadre des métiers de la propreté. Réalisé dans le cadre de l'UV Projet de l'IMT Nord Europe, par Thambirajah Shayuren et Melikechi Nael encadrés par Devetter François-Xavier et Lazes Julie.")



def main():
    st.set_page_config(page_title="Importation de fichier Excel avec Streamlit et Pandas",layout="wide")
    with st.sidebar:
        selected = option_menu("Menu Principal", ["Calculateur","Rémunération","Manque à gagner","A propos"], 
            icons=['calculator', 'currency-euro','graph-down', 'info-square'], menu_icon="list", default_index=0)
        #selected
    # Ajout du sidebar de navigation
    if selected == "Calculateur":
        calculateur()
    elif selected =="Rémunération":
        niveau()
    elif selected =="Manque à gagner":
        manque_a_gagner()
    elif selected =="A propos":
        about()



if __name__ == '__main__':
    main()
