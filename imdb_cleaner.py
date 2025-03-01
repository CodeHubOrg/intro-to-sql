"""Clean generic data from IMDb site"""

from tqdm import tqdm


class IMDbCleaner:
    """Base cleaner for IMDb data"""

    def __init__(self, data_generator, tsv_name):
        self.data_generator = data_generator
        self.tsv_name = tsv_name

    def replace_null(self, df):
        """Function to replace '\\N' which IMDb uses for null values with an empty string"""
        clean_df = df.replace("\\N", None)
        return clean_df

    def clean_data(self):
        """Clean the data."""
        # Create a progress bar
        bar_format = "Progress: {l_bar}{bar} | Completed: {n_fmt} | Time: [{elapsed}]"
        rows_progress = tqdm(
            bar_format=bar_format,
            desc=f"Processing {self.tsv_name}",
        )
        # Pull a chunk of data from the supplied data generator
        for df in self.data_generator:
            # Clean the data and then yield it to be written
            clean_df = self.clean_chunk(df)
            yield clean_df
            # Update the progress bar with the number of rows written
            rows_progress.update(len(df))

    def clean_chunk(self, df):
        """Clean a single chunk of data."""
        df = self.replace_null(df)
        return df


class TitleBasicsCleaner(IMDbCleaner):
    """Title Basics cleaner for IMDb data that filters out adult titles"""

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
        "titleType",
        "primaryTitle",
        "originalTitle",
        "startYear",
        "endYear",
        "runtimeMinutes",
        "genres",
    ]

    def clean_chunk(self, df):
        """Clean a single chunk of data."""
        # Filter out rows where 'isAdult' and rows where 'titleType' is 'movie'
        # Keep only desired columns
        filtered_df = df.loc[
            (df["isAdult"] == 0) & (df["titleType"] == "movie"), self.DESIRED_COLUMNS
        ]
        # Call the base class's replace_null method
        cleaned_df = self.replace_null(filtered_df)

        return cleaned_df


class TitleCrewCleaner(IMDbCleaner):
    """Title crew cleaner for IMDb data that filters out rows with no writer or director"""

    # title.crew.tsv.gz columns from https://developer.imdb.com/non-commercial-datasets/
    # tconst (string) - alphanumeric unique identifier of the title
    # directors (array of nconsts) - director(s) of the given title
    # writers (array of nconsts) – writer(s) of the given title

    def clean_chunk(self, df):
        """Clean a single chunk of data. Filter out rows where both 'directors' and 'writers' are
        '\\N'"""
        filtered_df = df.loc[~((df["directors"] == "\\N") & (df["writers"] == "\\N"))]
        # Call the base class's replace_null method
        cleaned_df = self.replace_null(filtered_df)

        return cleaned_df


class TitleEpisodeCleaner(IMDbCleaner):
    """Title episode cleaner for IMDb data that filters out rows with no episode or season number"""

    # title.episode.tsv.gz columns from https://developer.imdb.com/non-commercial-datasets/
    # tconst (string) - alphanumeric identifier of episode
    # parentTconst (string) - alphanumeric identifier of the parent TV Series
    # seasonNumber (integer) – season number the episode belongs to
    # episodeNumber (integer) – episode number of the tconst in the TV series

    def clean_chunk(self, df):
        """Clean a single chunk of data. Filter out rows where both 'seasonNumber' and
        'episodeNumber' are '\\N'"""
        filtered_df = df.loc[
            ~((df["seasonNumber"] == "\\N") & (df["episodeNumber"] == "\\N"))
        ]
        # Call the base class's replace_null method
        cleaned_df = self.replace_null(filtered_df)

        return cleaned_df
