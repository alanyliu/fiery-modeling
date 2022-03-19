# fiery-modeling

# Alan Liu's Senior Project
# Predicting Wildfire Ignition Point and Final Size
# 2020-21


## Abstract:
Especially in drought-prone regions like the Western US states, forest fires have been extremely prevalent. Across America in 2020, there were over 50,000 wildfire incidents reported with nearly 10,000 of them in California alone. What’s even more alarming is that a record 4.2 million acres in California were burned in 2020. The purpose of this project is to provide potential fire prevention insights for the future. More specifically, agencies may be able to support quicker suppression action and prevent the rapid spread of several fires in the future.

To accomplish this goal, my model will analyze the statistical significance of various fuel properties (e.g. vegetation, fuel moisture, dead fuel time lag) and features (e.g. temperature, humidity, precipitation, topography, fire size) by tracking climate data, wildfire stats, and fuels assessments from previous fires. I will be utilizing machine learning algorithms and statistical methods to assist in outputting predicted ignition point location. 

As an extension for my project, I may potentially seek to investigate the fluctuating spread rate of fires during the flashover, or flaming, stage by studying fire size and perimeters relative to time and intensity.


## Results:
After fine tuning of parameters, the best fit for the final size NN model returned an MSE loss of 0.1808, while the ignition point model outputted a cross-entropy loss of 0.935. The predicted vs true output graphs for each model contained several outliers as expected due to the unpredictable aspects and nature of wildfire spread (e.g. human impact such as accidents, "rare event" weather conditions, etc.), but overall, it can be determined that there is some correlation between the features. For more details on results, see blog linked below.


## Project Blog:
https://siliconvalley.basisindependent.com/author/alanl/?_ga=2.217753302.1749328986.1647666744-254722908.1647666744


## Files:
- CalFire2017-19.txt: fire data
- ca (folder): RAWS station weather data
- MesoWest (folder): weather/miscellaneous data obtained from MesoWest Utah
- RAWS_Stations_CountiesCA.txt: file that maps CA counties to respective indices
- Stn_Name_ID_Match.txt: file that maps each station to its respective county in CA
- WeatherFireSyncer.py: size dataset processing
- IgnitionDataset.py: ignition dataset processing
- Dataset_size.csv: size dataset
- Dataset_ignition.csv: ignition point dataset
- venv: libraries

Rest of the files are not necessarily affiliated with the project.


## Data Sources:
- CalFire archives (https://www.fire.ca.gov/incidents/)
- RAWS database (https://raws.dri.edu/; https://fam.nwcg.gov/fam-web/weatherfirecd/state_data.htm#Weather%20Files)
- MesoWest Utah (Mesowest.utah.edu/Cgi-Bin/Droman/Mesomap.cgi?State=CA&Rawsflag=3)


## Credits:
Special thanks to the following advisors!
- Dr. Swetha Bhattacharya, Internal Advisor, BISV
- Mao Ye, Statistical Learning & AI Group @ UT Austin
- Dr. Adam Kochanski, SJSU Wildfire Interdisciplinary Research Center
- Robert Baird, Director, US Pacific Southwest, USFS
