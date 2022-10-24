import pandas as pd

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
    Manipulate the DataFrame given, imported from the file ex/example_CI.xlsx, selecting columns and categorizing.
    
    :param df: DataFrame - readen from ex/example_CI.xlsx.

    :return df: DataFrame - edited.
    """
    df = df.iloc[:, 1:] # Select all rows, and after one columns.
    df.rename(columns = {df.columns[11]: "Year"}, inplace = True) # The variable Year was not named in the file.
    df = df.loc[:, ["Country", "ProductID", "Gender", "Size (US)", "Year", "Month"]] # Select only the columns we are going to use.

    # for item in df.columns: # Listing the type of the variables
    #     print(f"{item}: {df[item].dtype}")

    df["Gender"] = df["Gender"].astype("category") # Categorizing the variable Gender, which contains Male and Female.

    return df


def select_data(df, years, countries, gender):
    """
    Given the DataFrame edited and imported from the file ex/example_CI.xlsx, select a particular set of data.

    :param df: DataFrame - edited.
    :param years: list - which contains the year or years you want to select.
    :param country: list - country you want to select.
    :param gender: str - gender (male or female) you want to select.

    :return df_selected: DataFrame - with data selected.
    """
    df_years = pd.DataFrame()
    for year in years:
        df_years = pd.concat([df_years, df[df["Year"] == year]])
    
    df_years_countries = pd.DataFrame()
    for country in countries:
        df_years_countries = pd.concat([df_years_countries, df_years[df_years["Country"] == country]])

    df_selected = df_years_countries[df_years_countries["Gender"] == gender]

    return df_selected


# FREQUENCY TABLE

def freq_table(df, variable):
    """
    Return a frequency table for a chosen variable by year and month.

    :param df: DataFrame - containing the variable to study, and variables year and month.
    :param variable: str - variable's name you want to make the frequency.

    :return sales_by_month: Series - containing the frequency
    """
    df_var_month = df.loc[:, [variable, "Year", "Month"]]
    sales_by_month = df_var_month.groupby([variable, "Year", "Month"]).value_counts()

    return sales_by_month


def get_mean_by_var(freq_table):
    """
    Calculate the mean for each different value of the chosen variable in the frequency table.

    :param freq_table: Series - containing the frequency of the variable to study, and variables year and month.
    
    :return means_sorted: dictionary - with the mean of each variable's value.
    """

    years = set()
    for index in freq_table.index:
        years.add(index[1])
    years = sorted(years)

    variable_values = set()
    for index in freq_table.index:
        variable_values.add(index[0])
    variable_values = sorted(variable_values)

    means = {}

    for value in variable_values: # Per cada valor de la variable demanada, per exemple, la talla

        means[value] = round(freq_table[value].sum() / (len(years)*12), 2) # Calculem la mitjana dividint la suma entre el total de dades, i arrodonint a dos decimals

    means_sorted = dict(sorted(means.items()))

    return means_sorted


def get_stderror_by_var(freq_table):
    """
    Calculate the standard error for each different value of the chosen variable in the frequency table.

    :param freq_table: Series - containing the frequency of the variable to study, and variables year and month.
    
    :return std_error_sorted: dictionary - with the standard error of each variable's value.
    """

    years = set()
    for index in freq_table.index:
        years.add(index[1])
    years = sorted(years)

    variable_values = set()
    for index in freq_table.index:
        variable_values.add(index[0])
    variable_values = sorted(variable_values)

    std_error = {}

    for value in variable_values: # Per cada valor de la variable demanada, per exemple, la talla

        if len(freq_table[value]) < (len(years)*12): # Si hi ha mesos que no hi ha venta, no apareix en la base de dades, i necessitem que consti el 0 en aquell mes.
            for item in range(len(freq_table[value])+1, len(years)*12+1):
                freq_table[value, years[0], item] = 0

        std_error[value] = round(freq_table[value].std() / (len(years)*12)**(1/2), 2) # Calculem l'standard error fent la desviació típica i dividint-la per l'arrel quadrada del total de dades; arrodonim a dos decimals

    std_error_sorted = dict(sorted(std_error.items()))

    return std_error_sorted

def get_t_factor(degrees_of_freedom, alpha):
    """
    Return the factor from a T-student table given the degrees of freedom and the parameter alpha.

    :param degrees_of_freedom: int - between 1-120.
    :param alpha: float - 0.1, 0.05, 0.025, 0.01, 0.005. The significance level.
    
    :return t_factor: float - The T-student factor which corresponds to degrees of freedom and alpha.
    """
    t_table = read_excel_file("ex/The-t-table.xlsx", "t-table", skip_rows = 4, row_header = 1)
    t_table = t_table.set_index("d.f. / α")
    t_table = t_table.iloc[:-3, 1:]

    t_factor = t_table.loc[degrees_of_freedom, alpha]

    return t_factor


def get_reliability_factor(sample_size, confidence_level = 95):
    """
    Return the reliability factor from a T-student table given the sample size and the confidence level.

    :param sample_size: int - the size of the sample data.
    :param confidence_level: int - of grade 100. 
    
    :return reliability_factor: float - The T-student factor which corresponds to degrees of freedom (sample size -1) and alpha/2 (c.level = 1 - alpha)
    """

    degrees_of_freedom = sample_size - 1

    alpha = round(1 - (confidence_level / 100), 3)

    reliability_factor = get_t_factor(degrees_of_freedom, alpha/2)

    return reliability_factor


def get_margin_of_error(standard_error, sample_size, confidence_level = 95):
    """
    Return the margin of error, i.e., the standard error multiplied by the reliability factor (t-student factor).

    :param standard_error: dictionary - that contains the variable's value as the key and its standard error
    :param sample_size: int - the size of the sample data.
    :param confidence_level: int - of grade 100. 

    :return margin_of_error: dictionary - that contains the variable's value as the key and its margin of error.
    """
    reliability_factor = get_reliability_factor(sample_size, confidence_level)

    margin_of_error = {key: round(value * reliability_factor, 2) for key, value in standard_error.items()}

    return margin_of_error


def get_confidence_interval(means, margin_of_error):
    """
    Return the confidence interval given the point estimate (the mean) and the margin of error.

    :param means: dictionary -
    :param margin_of_error: dictionary -

    :return confidence_intervals: dictionary of lists - 
    """
    confidence_intervals = {}

    for key, value in means.items():
        confidence_intervals[key] = [round(value - margin_of_error[key], 2), round(value + margin_of_error[key], 2)]
    
    return confidence_intervals


# FREQUENCY TABLE: TOTAL SALES BY SIZE AND MONTH, USA - Male - 2015 i 2016

df = read_excel_file("ex/example_CI.xlsx", "Al Bundy", 2, 1)
df = prepare_dataframe(df)
df_USA = select_data(df, [2015, 2016], ["United States"], "Male")
sales_by_size = freq_table(df_USA, "Size (US)")

# TOTAL SALES STD ERROR, MARGIN OF ERROR, MEAN BY SIZE

standard_error = get_stderror_by_var(sales_by_size)

margin_of_error = get_margin_of_error(standard_error, 24, 95)

means = get_mean_by_var(sales_by_size)

# CONFIDENCE INTERVALS

print(get_confidence_interval(means, margin_of_error))