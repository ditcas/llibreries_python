import pandas as pd

# READ AND SELECT
df = pd.read_excel("ex/example_CI.xlsx", sheet_name="Al Bundy", skiprows=2, header=1)

df = df.iloc[:, 1:]
df.rename(columns = {df.columns[11]:"Year"}, inplace = True)

df = df.loc[:, ["Country", "ProductID", "Gender", "Size (US)", "Year", "Month"]]

# for item in df.columns:
#     print(f"{item}: {df[item].dtype}")

df["Gender"].astype("category")

# print(df.head())

# FREQUENCY TABLE: TOTAL SALES BY SIZE AND MONTH, USA-Male-2015 i 2016

df_US = df[(df["Country"] == "United States") & (df["Gender"] == "Male") & ((df["Year"] == 2015) | (df["Year"] == 2016))]

df_size_month = df_US.loc[:, ["Size (US)", "Year", "Month"]]
sales_by_size_month = df_size_month.groupby(["Size (US)", "Year", "Month"]).value_counts()

sales_by_size_month.to_excel("ex/sales_by_size_month.xlsx")


df_US = df[(df["Country"] == "United States") & (df["Gender"] == "Male") & ((df["Year"] == 2015) | (df["Year"] == 2016))]

# TOTAL SALES MEAN and STD DEV BY SIZE

means_sizes = {}
dev_sizes = {}

for size in set(df_US[df_US["Gender"] == "Male"]["Size (US)"]):

    df_US_size = df_US[df_US["Size (US)"] == size]
    
    sales_by_month = df_US_size.groupby(["Year", "Month"])[["Year", "Month"]].value_counts() # Sumem ventes realitzades per any i mes

    if len(sales_by_month) < 24: # Si hi ha mesos que no hi ha venta, no apareix en la base de dades, i necessitem que consti el 0 en aquell mes.
        for item in range(len(sales_by_month)+1, 25):
            sales_by_month[f"{item}"] = 0    

    means_sizes[size] = round(sales_by_month.sum() / 24, 2) # 24 perquè estem contemplant 2015 i 2016
    dev_sizes[size] = round(sales_by_month.std() / 24**(1/2), 2)

print(means_sizes)
print(dev_sizes)

    
    



