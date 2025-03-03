"""Clean non-commercial data from title.crew.tsv from IMDb site and prepare for loading into a
database."""

from imdb_data import IMDbData


class TitleCrewData(IMDbData):
    """Title crew cleaner for IMDb data that filters out rows with no writer or director"""

    # title.crew.tsv.gz columns from https://developer.imdb.com/non-commercial-datasets/
    # tconst (string) - alphanumeric unique identifier of the title
    # directors (array of nconsts) - director(s) of the given title
    # writers (array of nconsts) – writer(s) of the given title
    def __init__(self, init_df):
        df_name = "title_crew"
        super().__init__(init_df, df_name)
        # Assign an index to the DataFrame
        self.data_frames[df_name].set_index("tconst", inplace=True)
        # Convert directors to a new data frame called title_directors
        self.data_frames["title_directors"] = self.explode_columns(
            self.data_frames[df_name], "directors"
        )
        # Convert writers to a new data frame called title_writers
        self.data_frames["title_writers"] = self.explode_columns(
            self.data_frames[df_name], "writers"
        )
        # Delete the original data frame
        self.data_frames.pop(df_name)

    def clean_data(self, input_df):
        """Filter out rows where both 'directors' and 'writers' are '\\N'"""
        filtered_df = input_df.loc[
            ~((input_df["directors"] == "\\N") & (input_df["writers"] == "\\N"))
        ]
        return self.replace_null(filtered_df)
