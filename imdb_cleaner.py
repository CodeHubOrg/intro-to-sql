"""Clean generic data from IMDb site"""

from tqdm import tqdm


class IMDbCleaner:
    """Base cleaner for IMDb data"""

    def __init__(self, data_generator, tsv_name):
        self.data_generator = data_generator
        self.tsv_name = tsv_name

    def replace_null(self, df):
        """Function to replace '\\N' which IMDb uses for null values with an empty string"""
        clean_df = df.replace("\\N", "")
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
        # TODO work out which of these reassignments are needed if this finally works
        # Filter out rows where 'isAdult' and keep only desired columns
        filtered_df = df.loc[df["isAdult"] == 0, self.DESIRED_COLUMNS]
        # Call the base class's replace_null method
        cleaned_df = self.replace_null(filtered_df)

        return cleaned_df


class TitleCrewCleaner(IMDbCleaner):
    """Title crew cleaner for IMDb data that filters out rows with no writer or director"""

    def clean_chunk(self, df):
        """Clean a single chunk of data."""
        # Filter out rows where both 'directors' and 'writers' are '\N'
        filtered_df = df.loc[~((df["directors"] == "\\N") & (df["writers"] == "\\N"))]
        # Call the base class's replace_null method
        cleaned_df = self.replace_null(filtered_df)

        return cleaned_df
