"""Clean generic data from IMDb site"""

from tqdm import tqdm


class IMDbCleaner:
    """Base cleaner for IMDb data"""

    def __init__(self, data_generator, tsv_name):
        self.data_generator = data_generator
        self.tsv_name = tsv_name

    def replace_null(self, dataframe):
        """Function to replace '\\N' which IMDb uses for null values with an empty string"""
        dataframe.replace("\\N", "", inplace=True)

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
            self.clean_chunk(df)
            yield df
            # Update the progress bar with the number of rows written
            rows_progress.update(len(df))

    def clean_chunk(self, df):
        """Clean a single chunk of data."""
        self.replace_null(dataframe=df)
        return df
