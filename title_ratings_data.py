"""Clean non-commercial data from title.ratings.tsv from IMDb site and prepare for loading into a
database."""

from imdb_data import IMDbData


class TitleRatingsData(IMDbData):
    """Title Ratings cleaner for IMDb data"""

    # title.ratings.tsv.gz columns from https://developer.imdb.com/non-commercial-datasets/

    #     tconst (string) - alphanumeric unique identifier of the title
    #     averageRating – weighted average of all the individual user ratings
    #     numVotes - number of votes the title has received

    def __init__(self, init_df):
        df_name = "title_ratings"
        super().__init__(init_df, df_name)
