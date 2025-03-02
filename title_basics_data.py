"""Clean non-commercial data from names.basics.tsv from IMDb site and prepare for loading into a
database."""

from imdb_data import IMDbData


class TitleBasicsData(IMDbData):
    """Title Basics cleaner for IMDb data that filters out adult titles and non-movies"""

    # title.basics.tsv.gz columns from https://developer.imdb.com/non-commercial-datasets/
    # * tconst (string) - alphanumeric unique identifier of the title
    # * titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode,
    #   video, etc)
    # * primaryTitle (string) – the more popular title / the title used by the filmmakers on
    #   promotional materials at the point of release
    # * originalTitle (string) - original title, in the original language
    # * isAdult (boolean) - 0: non-adult title; 1: adult title
    # * startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is
    #   the series start year
    # * endYear (YYYY) – TV Series end year. '\N' for all other title types
    # * runtimeMinutes – primary runtime of the title, in minutes
    # * genres (string array) – includes up to three genres associated with the title

    def __init__(self, init_df):
        df_name = "title_basics"
        self.desired_columns = [
            "tconst",
            "primaryTitle",
            "originalTitle",
            "startYear",
            "runtimeMinutes",
            "genres",
        ]
        super().__init__(init_df, df_name)
        # Clean the data and load it into a DataFrame
        self.data_frames[df_name] = self.split_columns(
            self.data_frames[df_name], ["genres"]
        )

    def clean_data(self, input_df):
        """Filter out rows where 'isAdult' is 1 and keep rows where 'titleType' is 'movie'
        Keep only desired columns"""
        filtered_df = input_df[input_df.titleType == "movie"]
        print(filtered_df["isAdult"].value_counts())
        appropriate_df = filtered_df[filtered_df["isAdult"] == "0"]
        subset_df = appropriate_df[self.desired_columns]

        return self.replace_null(subset_df)
