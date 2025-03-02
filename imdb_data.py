"""Clean non-commercial data from IMDb site and prepare for loading into a database."""

import re
import pandas as pd


class IMDbData:
    """Base class for cleaning and storing IMDb data"""

    def __init__(self, init_df, df_name):
        # Clean the data and load it into a DataFrame stored in a dictionary
        self.data_frames = {}
        self.data_frames[df_name] = self.clean_data(init_df)

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
        return new_df

    def explode_columns(self, input_df, column_name):
        """Explode a column that contains comma separated values into separate rows.
        Must have an index set."""
        # Create a new DataFrame with lists of values
        input_df[column_name] = input_df[column_name].str.split(",")
        # Explode the list of values into separate rows in a new data-frame
        exploded_df = input_df.explode(column_name)
        # Select only the column that was exploded, filter empty rows and convert it into a
        # data-frame
        filtered_series = exploded_df[column_name].dropna()
        filtered_df = filtered_series.to_frame(name=column_name)

        return filtered_df
