
# Import Libraries
# We require few libraries to read and analyse the data. In this section, all the required libraries are imported.

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import numpy as np
import plotly
import kaleido


# Data Understanding
# Initially we are reading the data related to Corona cases and vacctination provided by our-world-in-data. To be up-to-date we directly assign the dataset URL so that when ever we run this cell latest updated data is pulled.

# collecting the data
csv_url="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

# reading the data
df = pd.read_csv(csv_url)

# just showing the output of the data collected
df.head()

# As we can see above, the dataset has many columns like iso_code, location, total_cases, etc. and the table also shows that there are many null/zero values. Donot worry about the NaN values we will clean it in later steps. We will get the overview of data like data type of features, a number of null values in each column, etc. using **info()**

df.info()

# We can get the statistics of each feature present in our dataset by using describe() function in pandas. Some of the information that we get include count, max, min, standard deviation, median, etc.

df.describe()

# Few details of the dataset that we require

print('1. The current dataset has all the data collected from',df.date.min(),'till',df.date.max())
print('2. Total number of countries registering COVID-19 cases are:',len(df.location.unique()))
print('3. The total number cases all over the world till now:',df.total_cases.max(), 'and total number of deaths till now are:', 
         df.total_deaths.max())
print('4. Total number of people fully vaccinated till now are:',len(df.people_fully_vaccinated.unique()))


# ..........................................................................................................................................................................................................................

# Data Preperation
# Different people follow different steps of data preperation

# Select Data

# We will select the data that we are intrested to work with from the above read dataset which makes data handling easy
# We will be only working with the data three countries but before that let's have some fun by visulaizing all the countries in the form of art by using WorldCLoud library. The text size of each country depends on how many times the country is repeated in the dataset.

wordCloud = WordCloud(
    background_color='white',
    max_font_size = 50).generate(' '.join(df.location))
plt.figure(figsize=(17,9))
plt.axis('off')
plt.imshow(wordCloud)
plt.savefig("Art of countries list")
plt.show()

# selecting the data of 3 countries that we are interested in
df_GER=df['location']=='Germany'
df_IND=df['location']=='India'
df_USA=df['location']=='United States'

df_countries= df_GER | df_IND | df_USA

df_total_list=df[df_countries]

df_total_list.head()


# as stated above there are lot of NaN values in the dataset and we will be cleaning the dataset below

#Data Cleaning
#There are many ways of cleaning the datasets. Some of the steps among them are shown below
# * Handling and Filling null values

# getting sum of all the null values in each column
df_total_list.isnull().sum()
# filling out the NaN values with values=0
df_cleaned = df_total_list.fillna(value=0, inplace=True)

df_total_list.head()

# Now, in the above table you can see that all the NaN values are replaced with 0.0 (float64 type).
# Even we change the data type of a feature in the following way

# * Change the data type of features
# changing the feature type , this can be done to features that you are interested to work with, 
# but I will be handling with float64 values
df_total_list.people_vaccinated = df_total_list.people_vaccinated.astype(int)


# #### ..........................................................................................................................................................................................................................

# Data Visualization
#We have prepared the data that we want to analyze and now its time to visualize the desired data
# We will try to plot an bar graph showing total cases resgistered till now in the countries that we selected above.

total_cases_country_wise={} # initially an empty dictionary is assigned
for location in df_total_list.location.unique():       # to loop among the list of countries we selected above
#for location in df.location.unique():                 # to loop amaong all the countries in the dataset
    total_corona_cases = 0
    for i in range(len(df)) :
        if df.location[i] == location:
            total_corona_cases += df_total_list.new_cases[i]      # appending and summing up new cases to get total cases registered till now
    total_cases_country_wise[location] = total_corona_cases
    # made an saperate dictionary from df and converting it to a data frame
    df_total_cases_country_wise = pd.DataFrame.from_dict(total_cases_country_wise,
                                                         orient='index',
                                                         columns = ['total no. of cases'])
df_total_cases_country_wise.sort_values(by = 'total no. of cases', ascending = False, inplace = True)


# plotting the graph using plotly express package
fig1 = px.bar(df_total_cases_country_wise, y='total no. of cases', x=df_total_cases_country_wise.index, color='total no. of cases', color_discrete_sequence= px.colors.sequential.Viridis_r )
fig1.update_layout(
    title={
            'text' : "Total Covid-19 cases till now",
            'y':0.95,
            'x':0.5
        },
    xaxis_title="Countries",
    yaxis_title="Total cases",
    legend_title="Total cases"
)
#saving image
fig1.write_image("Total number of cases country wise till now.jpeg")
fig1.show()


# We can also visualize the COVID-19 cases increasing every month for selected countries as shown in *fig2*
fig2=px.line(df_total_list, x= "date", y= "total_cases",color='location', title= "COVID-19 infection rate ")
fig2.write_image("COVID-19 infection rate.jpeg")
fig2.show()


# We will visualize the rate of corona cases increse with respective to population in *fig3*
df_total_list['total_infection_mean']=df_total_list['total_cases']/df_total_list['population']

fig3=px.line(df_total_list, x= "date", y= "total_infection_mean",color='location', title= "COVID-19 infection rate w.r.t population")
fig3.update_xaxes(range=["2020-04-01","2022-06-25"]) # this range is selected because In most countries corona cases started 
                                                     # registering from March 2020
fig3.write_image("COVID-19 infection rate w.r.t population.jpeg")
fig3.show()


# We can also visualize the vaccination rate same as corona cases fot the countries selected. Before plotting we will again replace 0.0 with NaN by loading dataset again and then fill the Nan values with the preceeding number using forwardfill(*ffill*) in pandas
# replace the nan values again with 0 
#df_total_list['people_fully_vaccinated'].replace(to_replace=0.0, value=np.nan)#, method='ffill') #TODO
df_total_list=df[df_countries]
# now filling the Nan values with the forward/pre values in column so that while visualization line doesnot again go to zero line
df_total_list.loc[:,['people_fully_vaccinated']]= df_total_list.loc[:,['people_fully_vaccinated']].ffill()
df_total_list['total_vaccination_mean']=df_total_list['people_fully_vaccinated']/df_total_list['population']

fig4=px.line(df_total_list, x= "date", y= "total_vaccination_mean",color='location', title= "Vaccination rate w.r.t population")
fig4.update_xaxes(range=["2021-03-01","2022-06-25"])
fig4.update_yaxes(range=[0,1])
fig4.write_image("Vaccination rate w.r.t population.jpeg")
fig4.show()


# ## .............................................................Thank you........................................................................
