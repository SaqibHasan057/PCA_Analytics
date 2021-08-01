from sklearn import decomposition
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


class PcaRealTime:
    def robust_real_time_PCA_target_dimension(self,input_data,block_size, output_dimension):
        output_matrix = []
        input_dimension = input_data.shape[1]
        eigen_vectors = np.zeros((input_dimension,output_dimension))
        identity_matrix = np.identity(input_dimension)

        #Initial_Block
        block = input_data[0:block_size]
        reconstruction_error = np.matmul(block,identity_matrix - np.matmul(eigen_vectors,np.transpose(eigen_vectors)))
        pca = decomposition.PCA(n_components=output_dimension)
        pca.fit(reconstruction_error)
        eigen_vectors,eigen_values = pca.components_,pca.explained_variance_
        eigen_vectors = np.transpose(eigen_vectors)
        output_row = np.matmul(block,eigen_vectors)
        for i in output_row:
            output_matrix.append(np.array([i]))


        for i in range(block_size,input_data.shape[0]):
            #Construct new row
            xt = input_data[i]
            xt = np.array([xt])

            #Construct new window
            block = np.append(block,xt,axis=0)
            block = np.delete(block,0,0)

            min_eigen_value, minIndex = eigen_values.min(),output_dimension-1

            #top eigenvector
            reconstruction_error = np.matmul(block,identity_matrix - np.matmul(eigen_vectors,np.transpose(eigen_vectors)))
            pca = decomposition.PCA(n_components=output_dimension)
            pca.fit(reconstruction_error)
            dummy_eigen_vector,dummy_eigen_values = pca.components_,pca.explained_variance_
            dummy_eigen_vector = np.transpose(dummy_eigen_vector)
            max_eigen_value = dummy_eigen_values[0]
            max_eigen_vector = dummy_eigen_vector[:,[0]]

            if(max_eigen_value>min_eigen_value):
                eigen_vectors = np.transpose(eigen_vectors)
                eigen_vectors = np.delete(eigen_vectors,eigen_vectors.shape[0]-1,0)
                eigen_vectors = np.append(eigen_vectors,np.transpose(max_eigen_vector),axis=0)
                eigen_vectors = np.transpose(eigen_vectors)

            output_row = np.matmul(xt,eigen_vectors)
            output_matrix.append(output_row)

        output_matrix = np.squeeze(np.array(output_matrix))
        return output_matrix,eigen_vectors,eigen_values


    def convert_text_to_vector(self,text_data):

        vectorizer = CountVectorizer()
        vectorizer.fit(text_data)
        vector = vectorizer.transform(text_data)
        vector = vector.toarray()
        frequency_per_word = vector.sum(axis=0)
        temp = vectorizer.vocabulary_
        dict = {v: k for k, v in temp.items()}
        return dict,vector,frequency_per_word

    def maximum_from_eigen_vector(self,eigenvector,dictionary,frequency_per_word):
        max_value_of_each_eigenvector = np.max(eigenvector,axis=0)
        index_of_max_value = np.argmax(eigenvector,axis=0)
        words = []
        frequency = []

        data = []

        for x in index_of_max_value:
            words_dictionary = {}
            words.append(dictionary[x])
            frequency.append(str(frequency_per_word[x]))
            words_dictionary["Name"]= dictionary[x]
            words_dictionary["Count"] = str(frequency_per_word[x])
            data.append(words_dictionary)

        return max_value_of_each_eigenvector,index_of_max_value,words,frequency,data

