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

def edit_df(df):
    """
    Edit the DataFrame given, imported from the file ex/example_CI.xlsx, selecting columns and categorizing.
    
    :param df: DataFrame - readen from ex/example_CI.xlsx.

    :return df: DataFrame - edited.
    """
    df = df.iloc[:, 1:] # Select all rows, and after one columns.
    df.rename(columns = {df.columns[11]: "Year"}, inplace = True) # The variable Year was not named in the file.
    df = df.loc[:, ["Country", "ProductID", "Gender", "Size (US)", "Year", "Month"]] # Select only the columns we are going to use.

    # for item in df.columns: # Listing the type of the variables
    #     print(f"{item}: {df[item].dtype}")

    df["Gender"].astype("category") # Categorizing the variable Gender, which contains Male and Female.

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


# FREQUENCY TABLE: TOTAL SALES BY SIZE AND MONTH, USA - Male - 2015 i 2016

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


df = read_excel_file("ex/example_CI.xlsx", "Al Bundy", 2, 1)
df = edit_df(df)
df_USA = select_data(df, [2015, 2016], ["United States"], "Male")
print(freq_table(df_USA, "Size (US)"))


# TOTAL SALES MEAN and STD DEV BY SIZE

def mean_by_var(file = "ex/example_CI.xlsx", sheet = "Al Bundy", skiprows = 2, header = 1, years = [2015, 2016], country = ["United States"], gender = "Male", variable = "Size (US)"):

    df = read_excel_file(file, sheet, skiprows, header)
    df = edit_df(df)
    df_selection = select_data(df, years, country, gender)

    means = {}

    for value in set(df_selection[variable]): # Per cada valor de la variable demanada, per exemple, la talla

        df_selection_var = df_selection[df_selection[variable] == value]
    
        sales_by_month = df_selection_var.groupby(["Year", "Month"])[["Year", "Month"]].value_counts() # Sumem ventes realitzades per any i mes

        means[value] = round(sales_by_month.sum() / (len(years)*12), 2) # Calculem la mitjana dividint la suma entre el total de dades, i arrodonint a dos decimals

    return means

def stderror_by_var(file = "ex/example_CI.xlsx", sheet = "Al Bundy", skiprows = 2, header = 1, years = [2015, 2016], country = ["United States"], gender = "Male", variable = "Size (US)"):

    df = read_excel_file(file, sheet, skiprows, header)
    df = edit_df(df)
    df_selection = select_data(df, years, country, gender)

    std_error = {}

    for value in set(df_selection[variable]): # Per cada valor de la variable demanada, per exemple, la talla

        df_selection_var = df_selection[df_selection[variable] == value]
    
        sales_by_month = df_selection_var.groupby([variable, "Year", "Month"])[["Year", "Month"]].value_counts() # Sumem ventes realitzades per any i mes

        if len(sales_by_month) < (len(years)*12): # Si hi ha mesos que no hi ha venta, no apareix en la base de dades, i necessitem que consti el 0 en aquell mes.
            for item in range(len(sales_by_month)+1, len(years)*12+1):
                sales_by_month[f"{item}"] = 0    

        std_error[value] = round(sales_by_month.std() / (len(years)*12)**(1/2), 2) # Calculem la mitjana dividint la suma entre el total de dades, i arrodonint a dos decimals

    return std_error

stderror_by_var()