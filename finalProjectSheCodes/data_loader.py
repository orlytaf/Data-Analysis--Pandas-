import pandas as pd

# reading the data from the excel file about area size - square km
google_data = pd.read_excel(r"C:\Users\User\Desktop\Final Project\Google_data.xlsx")

google_data.columnsIndex(['country', 'area'], dtype='object')

# reading the data from the excel file about Kaggle dataset
world_happiness = pd.read_excel(r"C:\Users\User\Desktop\Final Project\World_Happiness_2021_DB.xlsx")

# merging the data from Kaggle with the data from google, about area size
all_data = world_happiness.merge(google_data, how='left', left_on='Country name', right_on='country')
all_data.drop_duplicates(inplace=True)
all_data.drop(['country'], axis=1, inplace=True)

Avg_temprature = pd.read_excel(r"C:\Users\User\Desktop\Final Project\Average_Temp_Celsius.xlsx")
Avg_temp2=pd.read_excel(r"C:\Users\User\Desktop\Final Project\average_temprature_NOAA.xlsx")

# using formulas to convert Fahrenheit degrees to Celsius degrees
Avg_temp2['AvgTemp']= Avg_temp2['averageTemperature'].apply(lambda x:((x-32)*(5/9)))
Avg_temp2.drop(['averageTemperature'],axis=1,inplace=True)
Avg_temprature.rename({'Country Name':'country','Average yearly temperature (Celsius)':'AvgTemp'},inplace=True, axis=1)
all_temprature = Avg_temprature.append(Avg_temp2)

# reading information from excel and csv files
avg_precipitation = pd.read_excel(r"C:\Users\User\Desktop\Final Project\avg_precipitation_depth.xlsx")
unemploymentRate = pd.read_excel(r"C:\Users\User\Desktop\Final Project\unemployed_rate.xlsx")
dis_from_equator = pd.read_excel(r"C:\Users\User\Desktop\Final Project\distance_from_equator.xlsx")
population = pd.read_excel(r"C:\Users\User\Desktop\Final Project\population_number.xlsx")
life_level= pd.read_csv(r"C:\Users\User\Desktop\Final Project\life_level.csv")
continent= pd.read_csv(r"C:\Users\User\Desktop\Final Project\continent.csv")
independence_year= pd.read_csv(r"C:\Users\User\Desktop\Final Project\independence year.csv")

# dropping cells that have no information, type: NA
dis_from_equator.dropna(subset=['capital'],inplace=True)
avg_precipitation.dropna(subset=['avg precipitation'],inplace=True)
continent.dropna(subset=['country'],inplace=True)

# dropping unnecessary columns from dataset
dis_from_equator.drop(['city'], axis=1, inplace=True)
dis_from_equator.drop(['capital'], axis=1, inplace=True)

# changing the location of the columns in the dataset
dis_from_equator = dis_from_equator[['country', 'lat']]

# calculating the distance from the equator with latitude coordinate, and converting it from miles to km
dis_from_equator['disFromEquator'] = dis_from_equator['lat'].apply(lambda x:x*69*1.609344)
dis_from_equator.drop_duplicates(subset="country",inplace=True)

# after we calculated the distance from equator, we won't need the latitude column
dis_from_equator.drop(['lat'], axis=1, inplace=True)

# merging the data into one table and cleaning extra country columns
all_data = all_data.merge(population, how='left', left_on='Country name', right_on='Country Name')
all_data.drop(['Country Name'], axis=1, inplace=True)
all_data = all_data.merge(avg_precipitation, how='left', left_on='Country name', right_on='country')
all_data.drop(['country'], axis=1, inplace=True)
all_data = all_data.merge(dis_from_equator, how='left', left_on='Country name', right_on='country')
all_data.drop(['country'], axis=1, inplace=True)
all_data = all_data.merge(unemploymentRate, how='left', left_on='Country name', right_on='country')
all_data.drop(['country'], axis=1, inplace=True)
all_data = all_data.merge(all_temprature, how='left', left_on='Country name', right_on='country')
all_data.drop(['country'], axis=1, inplace=True)
all_data = all_data.merge(continent, how='left', left_on='Country name', right_on='country')
all_data.drop(['country'], axis=1, inplace=True)
all_data = all_data.merge(life_level, how='left', left_on='Country name', right_on='country')
all_data.drop(['country'], axis=1, inplace=True)
all_data = all_data.merge(independence_year, how='left', left_on='Country name', right_on='country')
all_data.drop(['country'], axis=1, inplace=True)

life_level['country'] = life_level['country'].apply(lambda x: x[4:])

# defining function for life level categorization
def func(standard_of_living):
       if (standard_of_living>=0.8):
           return 'good'
       if (standard_of_living<0.8 and standard_of_living>=0.6):
          return 'medium'
       else:
         return 'bad'

life_level['standard_of_living'] = life_level['standard_of_living'].apply(func)

# converting command from csv file wuth special string \xa0
life_level['country'] = life_level['country'].str.replace('\xa0', '').astype(str)

# changing the order of the columns in the main dataset
all_data = all_data[['Country name','continent','Regional indicator','Ladder score','Standard error of ladder score','upperwhisker','lowerwhisker','Logged GDP per capita','Social support','Healthy life expectancy','Freedom to make life choices','Generosity','Perceptions of corruption','Ladder score in Dystopia','Explained by: Log GDP per capita','Explained by: Social support','Explained by: Healthy life expectancy','Explained by: Freedom to make life choices','Explained by: Generosity','Explained by: Perceptions of corruption','Dystopia + residual','area','population (thousands)','avg precipitation','disFromEquator','unemployed_rate_2020','AvgTemp']]

# saving all_data df to csv file
all_data.to_csv(r"C:\Users\User\Desktop\Final Project\all_data.csv")