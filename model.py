import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Model:
    def __init__(self):
        self.read_data()
        self.refactor_data()
        self.vectoriz()



    def read_data(self):
        self.data = pd.read_csv("data/all_games.csv")

    def refactor_data(self):
        self.search_data = self.data.drop_duplicates(subset='name', keep="last")
        self.new_data = self.data.drop_duplicates(subset='name', keep="last")
        #self.new_data["summary"] = self.new_data["summary"].astype(str) + " " + self.new_data["name"].astype(str).str.zfill(6)


    def vectoriz(self):
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.new_data['summary'] = self.new_data['summary'].fillna('')
        self.overview_matrix = self.tfidf.fit_transform(self.new_data['summary'])

        self.similarity_matrix = linear_kernel(self.overview_matrix, self.overview_matrix)

    def mapping(self):
        self.mapping = pd.Series(self.new_data.index, index=self.new_data['name'])

    def recommend_games(self, game_input):
        self.mapping()
        game_index = self.mapping[game_input]
        similarity_score = list(enumerate(self.similarity_matrix[game_index]))
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        similarity_score = similarity_score[1:6]
        game_indices = [i[0] for i in similarity_score]

        return (self.search_data['name'].iloc[game_indices])

    def to_list(self, temp):
        temp = temp.tolist()
        return temp



    def getInfo(self, game):
        temp = self.search_data.loc[self.search_data['name'] == game]
        platform = temp['platform'].to_string(index=False)
        date = temp['release_date'].to_string(index=False)
        userScore = temp['user_review'].to_string(index=False)
        metaScore = temp['meta_score'].to_string(index=False)

        result = platform + "$" + date + "$" + str(int(float(userScore)*10)) + "$" + metaScore


        return result




