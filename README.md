# fiery-modeling

# Alan Liu's Senior Project
# Predicting Wildfire Ignition Point and Final Size
# 2020-21


Abstract:
Especially in drought-prone regions like the Western US states, forest fires have been extremely prevalent. Across America in 2020, there were over 50,000 wildfire incidents reported with nearly 10,000 of them in California alone. What’s even more alarming is that a record 4.2 million acres in California were burned in 2020. The purpose of this project is to provide potential fire prevention insights for the future. More specifically, agencies may be able to support quicker suppression action and prevent the rapid spread of several fires in the future.

To accomplish this goal, my model will analyze the statistical significance of various fuel properties (e.g. vegetation, fuel moisture, dead fuel time lag) and features (e.g. temperature, humidity, precipitation, topography, fire size) by tracking climate data, wildfire stats, and fuels assessments from previous fires. I will be utilizing machine learning algorithms and statistical methods to assist in outputting predicted ignition point location. 

As an extension for my project, I may potentially seek to investigate the fluctuating spread rate of fires during the flashover, or flaming, stage by studying fire size and perimeters relative to time and intensity.


Files:
CalFire2017-19.txt - fire data
ca (folder) - RAWS station weather data
MesoWest (folder) - weather/miscellaneous data
RAWS_Stations_CountiesCA.txt - maps CA counties to respective indices
Stn_Name_ID_Match.txt - maps each station to its respective county in CA
WeatherFireSyncer.py - size dataset processing
IgnitionDataset.py - ignition dataset processing
Dataset_size.csv - size dataset
Dataset_ignition.csv - ignition point dataset
venv - libraries

Rest of the files may not be affiliated with the project.


Data_Sources:
CalFire archives (https://www.fire.ca.gov/incidents/)
RAWS database (https://raws.dri.edu/, https://fam.nwcg.gov/fam-web/weatherfirecd/state_data.htm#Weather%20Files)
MesoWest Utah (Mesowest.utah.edu/Cgi-Bin/Droman/Mesomap.cgi?State=CA&Rawsflag=3)
