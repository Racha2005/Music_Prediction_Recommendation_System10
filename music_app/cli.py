from music_app.ml.recommender import recommend

if __name__=='__main__':
    print('Sample recommendations for track_1:')
    print(recommend('track_1', top_k=5))
