import statistics
import pandas as pd
import scipy.stats as stats

# READ AND SELECT

def read_excel_file(file_name, sheet_file, skip_rows, row_header):
    """
    Read a particular sheet of an excel file.

    :param file: str - excel file you want to read.
    :param sheet: str - file's sheet you want to read.
    :param skiprows: int - number of rows from the begining you don't want to read.
    :param header: int - which row, after the skiprows, contains the index of the columns.

    :return df: DataFrame - contains the readen data.
    """
    df = pd.read_excel(file_name, sheet_name = sheet_file, skiprows = skip_rows, header = row_header)

    return df


def prepare_dataframe(df):
    """
    Manipulate the DataFrame given, imported from the file ex/example_HT.xlsx, selecting columns and categorizing.
    
    :param df: DataFrame - readen from ex/example_HT.xlsx.

    :return df: DataFrame - edited.
    """
    df = df.iloc[:, 1:-1] # Select all rows, and all columns except first an last one.
    df = df.loc[:, ["Age", "Gender", "Country", "Ethnicity", "Salary"]] # Select only the columns we are going to use.

    df["Gender"].astype("category") # Categorizing the variable Gender, which contains Male and Female.
    df["Ethnicity"].astype("category") # Categorizing the variable Gender, which contains Male and Female.

    return df


def select_ethnicity(df):
    """
    Given the DataFrame edited and imported from the file ex/example_HT.xlsx, select people by its ethnicity (white or not).

    :param df: DataFrame - edited.

    :return df_white: DataFrame - with data of white people.
    :return df_nonwhite: DataFrame - with data of non white people.
    """

    df_white = df[df["Ethnicity"] == "White"]
    df_nonwhite = df[df["Ethnicity"] != "White"]

    return df_white, df_nonwhite

def get_df_size(df):
    """
    Calculate the size of the DataFrame, i.e. the sample's size.

    :param df: DataFrame - containing the data of the sample.

    :return: int - sample's size
    """
    return len(df.index)

def get_diff_mean_salary(df_x, df_y):
    """
    Calculate the Salary mean of each sample (two independent samples) and then make the difference.

    :param df_x: DataFrame - containing data of one sample.
    :param df_y: DataFrame - containing data of the other sample.
    
    :return diff_mean: float - the difference of the two sample's Salary mean.
    """

    mean_df_x = df_x["Salary"].mean()
    mean_df_y = df_y["Salary"].mean()

    return mean_df_x - mean_df_y

def get_pooled_variance(df_x, df_y):
    """
    Calculate the pooled variance of two independent samples with variance unknown.

    :param df_x: DataFrame - containing data of one sample.
    :param df_y: DataFrame - containing data of the other sample.
    
    :return pooled_variance: float - pooled variance result
    """

    var_df_x = statistics.variance(df_x["Salary"])
    var_df_y = statistics.variance(df_y["Salary"])
    x_size = get_df_size(df_x)
    y_size = get_df_size(df_y)

    return ((x_size - 1) * var_df_x + (y_size - 1) * var_df_y)/(x_size + y_size -2)


def get_stderror(x_sample_size, y_sample_size, pooled_variance):
    """
    Calculate the standard error of two independent samples with variance unknown.

    :param x_sample_size: int - sample's size of one DataFrame
    :param y_sample_size: int - sample's size of another DataFrame
    :param pooled_variance: float - pooled variance of two independent samples

    :return std_error: float - standard error result
    """

    return (pooled_variance/x_sample_size + pooled_variance/y_sample_size)**(1/2)


def get_t_score(d_mean, null_hyp_mean, std_error):
    """
    Calculate the T-score as we have two independent samples with variance unkwnown.

    :param d_mean: float - the difference of the two sample's mean.
    :param null_hyp_mean: float - The mean of Null Hypothesis, mu0.
    :param std_error: float - the standard error of two samples.

    :return: float - the T-score value.
    
    """

    return (d_mean-null_hyp_mean)/std_error


df = read_excel_file("ex/example_HT.xlsx", "Dataset", 2, 1)
df = prepare_dataframe(df)
df_white, df_nonwhite = select_ethnicity(df)


d_mean = get_diff_mean_salary(df_white, df_nonwhite)
pool_var = get_pooled_variance(df_white, df_nonwhite)
white_size = get_df_size(df_white)
nonwhite_size = get_df_size(df_nonwhite)
std_error = get_stderror(white_size, nonwhite_size, pool_var)
t_score = get_t_score(d_mean, 0, std_error)

# Per calcular el p-value usem la llibreria stats de scipy. Només requereix les dades de les dues mostres independents, i retorna el T-score i el p-value. Per defecte considera variància desconeguda però assumim que igual. Per defecte també considea two-sided test. Així que en realitat les funcions d'abans seria per fer-ho manual fins a obtenir el T-score. 
print(stats.ttest_ind(df_white["Salary"], df_nonwhite["Salary"]))
