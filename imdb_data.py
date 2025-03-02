"""Clean non-commercial data from IMDb site and prepare for loading into a database."""

import pandas as pd


class IMDbData:
    """Base class for cleaning and storing IMDb data"""

    def __init__(self, init_df, tsv_name):
        # Clean the data and load it into a DataFrame
        self.data_frame = self.clean_data(init_d)
        self.tsv_name = tsv_name

    def replace_null(self, input_df):
        """Function to replace '\\N' which IMDb uses for null values with an empty string"""
        return input_df.replace(to_replace={"\\N": None})

    def clean_data(self, input_df):
        """Clean the data."""
        return self.replace_null(input_df)

    def split_column(self, input_df, column_name):
        """Split column that contain multiple values separated by commas"""
        split_df = input_df[column_name].str.split(",", expand=True)
        # Prefix the column names with the original column name
        return split_df.add_prefix(column_name + "_")

    def split_columns(self, input_df, columns):
        """Split multiple columns that contain multiple values separated by commas"""
        new_df = input_df
        for column in columns:
            # Split the column
            split_df = self.split_column(new_df, column)
            # Drop the original column and concatenate the split columns
            new_df = pd.concat([new_df.drop(column, axis=1), split_df], axis=1)
            print(new_df.head())
        return new_df


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

    DESIRED_COLUMNS = [
        "tconst",
        "primaryTitle",
        "originalTitle",
        "startYear",
        "runtimeMinutes",
        "genres",
        "isAdult",
    ]

    def clean_data(self, input_df):
        """Filter out rows where 'isAdult' is 1 and keep rows where 'titleType' is 'movie'
        Keep only desired columns"""
        # TODO: Filter out adult titles - not working for some reason
        filtered_df = input_df.loc[input_df["titleType"] == "movie"]
        appropriate_df = filtered_df.loc[filtered_df["isAdult"] == 0]
        subset_df = appropriate_df[self.DESIRED_COLUMNS]

        return self.replace_null(subset_df)


class TitleCrewData(IMDbData):
    """Title crew cleaner for IMDb data that filters out rows with no writer or director"""

    # title.crew.tsv.gz columns from https://developer.imdb.com/non-commercial-datasets/
    # tconst (string) - alphanumeric unique identifier of the title
    # directors (array of nconsts) - director(s) of the given title
    # writers (array of nconsts) – writer(s) of the given title

    def clean_data(self, input_df):
        """Filter out rows where both 'directors' and 'writers' are '\\N'"""
        filtered_df = input_df.loc[
            ~((input_df["directors"] == "\\N") & (input_df["writers"] == "\\N"))
        ]
        return self.replace_null(filtered_df)
