"""Clean non-commercial data from names.basics.tsv from IMDb site and prepare for loading into a
database."""

from imdb_data import IMDbData


class NameBasicsData(IMDbData):
    """Class for cleaning and storing IMDb data in name.basics.tsv"""

    # name.basics.tsv

    # nconst (string) - alphanumeric unique identifier of the name/person
    # primaryName (string)– name by which the person is most often credited
    # birthYear – in YYYY format
    # deathYear – in YYYY format if applicable, else '\N'
    # primaryProfession (array of strings)– the top-3 professions of the person
    # knownForTitles (array of tconst values) – titles the person is known for

    def __init__(self, init_df):
        df_name = "name_basics"
        super().__init__(init_df, df_name)
        self.desired_columns = [
            "primaryName",
            "birthYear",
            "deathYear",
        ]
        # Assign an index to the DataFrame
        self.data_frames[df_name].set_index("nconst", inplace=True)
        # Explode one compound columns and store as a new table. The other compound column is split
        # into multiple columns
        self.data_frames[df_name] = self.split_columns(
            self.data_frames[df_name], ["primaryProfession"]
        )
        # Convert knownForTitles to a column of lists
        self.data_frames[df_name]["knownForTitles"] = self.data_frames[df_name][
            "knownForTitles"
        ].str.split(",")
        # Explode the knownForTitles column into a new data-frame and drop the other columns
        known_for_titles = self.data_frames[df_name].explode("knownForTitles")
        known_for_titles = known_for_titles["knownForTitles"]
        # Drop the knownForTitles column from the name_basics data-frame
        self.data_frames[df_name] = self.data_frames[df_name][self.desired_columns]
        self.data_frames["known_for_titles"] = known_for_titles
