#Instructions to run the application.


> Checkout the git folder as is.
> Load the Data_Cleaning.ipynb to your Jupyter Notebook along with original_dataset.csv
> Running Data_Cleaning.ipynb cell by cell will result in producing intermittent files along the way that can determine the progress and also be used to understand the changes at each step.

Understanding the output files:
> The other files in the folder are essentially the output files produced when we ran our code.
> > dirty_dataset.csv is produced after inducing the initial errors intentionally corrupting the dataset. We will try to clean this dirty_dataset.csv
> > {column_name}_cleaned_group.csv consists of the clean records (the records that pass all the integrity rules) for the column with column name as {column_name}.
> > {column_name}_abnormal_group.csv consists of the records that have abnormal values (the records that do not pass the integrity rules) for the column with column name as {column_name}.
> > {column_name}_abnormal_group_updated.csv consists of the abnormalities fixed according to the MLN indexing and similarity scores defined.
> > final_combined_dataset.csv consists of the final cleaned data that used to compare with the benchmark dataset original_dataset.csv
