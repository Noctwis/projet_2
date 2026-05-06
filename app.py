import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
from zipfile import ZipFile


def main() :

    @st.cache
    def load_data():
    
        z = ZipFile("df_affichage.zip")
        sample = pd.read_csv(z.open('df_affichage.csv'), encoding ='utf-8')
       
        return sample



    @st.cache(allow_output_mutation=True)
    def load_knn(sample):
        knn = knn_training(sample)
        return knn



    def identite_client(data, id):
        data_client = data[data.index == int(id)]
        return data_client



    @st.cache
    def load_kmeans(sample, id, mdl):
        index = sample[sample.index == int(id)].index.values
        index = index[0]
        data_client = pd.DataFrame(sample.loc[sample.index, :])
        df_neighbors = pd.DataFrame(knn.fit_predict(data_client), index=data_client.index)
        df_neighbors = pd.concat([df_neighbors, data], axis=1)
        return df_neighbors.iloc[:,1:].sample(10)

    @st.cache
    def knn_training(sample):
        knn = KMeans(n_clusters=2).fit(sample)
        return knn 


    #######################################
    # SIDEBAR
    #######################################

    #Title display
    html_temp = """
    <div style="background-color: tomato; padding:10px; border-radius:10px">
    <h1 style="color: white; text-align:center">Trop bien ça marche !</h1>
    </div>
    <p style="font-size: 20px; font-weight: bold; text-align:center">Credit decision support…</p>
    """
    st.markdown(html_temp, unsafe_allow_html=True)


    title = sample.title
    #Customer ID selection
    st.sidebar.header("**General Information**")

    #Loading selectbox
    chk_id = st.sidebar.selectbox("Film selectionner", title)
 
    
        

    #######################################
    # HOME PAGE - MAIN CONTENT
    #######################################
    #Display Customer ID from Sidebar
    st.write("Selection du film :", chk_id)           
    

    #Similar customer files display
    chk_voisins = st.checkbox("Show similar movies files ?")

    if chk_voisins:
        knn = load_knn(sample)
        st.markdown("<u>List of the 10 movies closest to this movies :</u>", unsafe_allow_html=True)
        st.dataframe(load_kmeans(sample, chk_id, knn))
        #st.markdown("<i>Target 1 = Customer with default</i>", unsafe_allow_html=True)
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)
        
    
     
    chk_voisins2 = st.checkbox("Show similar movies by KNN?")   
    
    if chk_voisins2:

        # Transformation des genres en vecteurs (one-hot encoding)
        mlb = MultiLabelBinarizer()
        genre_matrix = mlb.fit_transform(sample["genres"])

        # Modèle KNN
        knn = NearestNeighbors(n_neighbors=10, metric='cosine')
        knn.fit(genre_matrix)


        # Index du film
        idx = sample[sample["title"] == chk_id].index[0]

        # Trouver les voisins
        distances, indices = knn.kneighbors([genre_matrix[idx]], n_neighbors=10)

        # Exclure le film lui-même
        recommendations = []
        for i in indices[0][1:]:
            recommendations.append(df.iloc[i]["title"])

        st.markdown(recommendations)
    else:
        st.markdown("<i>…</i>", unsafe_allow_html=True)
        
    st.markdown('***')


if __name__ == '__main__':
    main()