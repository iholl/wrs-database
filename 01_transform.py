import json
import arcgis
import pandas as pd
import geopandas as gpd

from decouple import config

# set arcgis online account information
PORTAL_URL = config("ARCGIS_ONLINE_URL")
PORTAL_USERNAME = config("ARCGIS_ONLINE_USERNAME")
PORTAL_PASSWORD = config("ARCGIS_ONLINE_PASSWORD")

# set the feature collection id
feature_layer_collection_id = config("ARCGIS_ONLINE_FEATURE_ID")

# log into arcgis online and get feature layer collection by id
gis = arcgis.GIS(PORTAL_URL, PORTAL_USERNAME, PORTAL_PASSWORD)
feature_layer_collection = gis.content.get(feature_layer_collection_id)

# loop through all the feature layers in the feature collection
for fl in range(len(feature_layer_collection.layers)):

  # get the layer from the feature layer collection array
  layer = feature_layer_collection.layers[fl]

  # get the layer name from the properties of the layer
  layer_name = layer.properties.name

  # query the layer to create a feature set
  feature_set = layer.query()

  # feature set to geojson string
  geojson_string = feature_set.to_geojson

  # load the geojson string into a dictionary
  geojson_dictionary = json.loads(geojson_string)

  # geojson dictionary to geodataframe
  gdf = gpd.GeoDataFrame.from_features(geojson_dictionary["features"])

  # convert the gdf to dataframe and drop unused columns
  df = pd.DataFrame(gdf.drop(columns=["geometry", "CreationDate", "Creator", "EditDate", "Editor"]))

  ##### FORMATING sighting TABLE ######
  if (layer_name == "Sighting"):
    df["SurveyID"] = df["SurveyIDRte"]
    df["x"] = df["BirdLocE"]
    df["y"] = df["BirdLocN"]
    for index, row in df.iterrows():
        if (df["SpeciesCode"].empty == True):
            df["Speices"] = df["SpeciesCode_other"]
        else:
            df["Species"] = df["SpeciesCode"]
    df[["SurveyID", "ObsTime", "Species", "ObsTotal", "activity", "ObsMPH", "distance", "SideRoad", "doubleback", "ObsComments", "x", "y"]].to_csv("sightings.csv", index=False)

  ##### FORMATING survey TABLE ######
  if (layer_name == "Winter_Raptor_Survey"):
    # replace na with 0, inplace = use/maintain df
    df.fillna(0, inplace=True)
    # loop through each row
    for index, row in df.iterrows():
        # check start easting
        if (row["StartLocE"] == 0):
            if (row["StartUTM83E"] == 0):
                print("No location information")
            else:
                df["x_start"] = df["StartUTM83E"]
        else:
            df["x_start"] = df["StartLocE"]
        # check start northing
        if (row["StartLocN"] == 0):
            if (row["StartUTM83N"] == 0):
                print("No location information")
            else:
                df["y_start"] = df["StartUTM83N"]
        else:
            df["y_start"] = df["StartLocN"]
        # check end easting
        if (row["EndLocE"] == 0):
            if (row["enad83EL"] == 0):
                print("No location information")
            else:
                df["x_end"] = df["enad83EL"]
        else:
            df["x_end"] = df["EndLocE"]
        # check end northing
        if (row["EndLocN"] == 0):
            if (row["nnad83EL"] == 0):
                print("No location information")
            else:
                df["y_end"] = df["nnad83EL"]
        else:
            df["y_end"] = df["EndLocN"]
        # check starting temperature
        if (df["StartTemp"].empty == False):
            temp_list = df["StartTemp"].values[0].replace("_", " ").split()
            start_total = 0
            for value in temp_list:
                start_total = start_total + int(value)
            average = start_total / len(temp_list)
            df["StartingTemp"] = average
        else:
            df["StartingTemp"] = df["ActualSTemp"]
        # check end temperature
        if (df["EndTemp"].empty == False):
            temp_list = df["EndTemp"].values[0].replace("_", " ").split()
            end_total = 0
            for value in temp_list:
                end_total = end_total + int(value)
            average = end_total / len(temp_list)
            df["EndingTemp"] = average
        else:
            df["EndingTemp"] = df["ActualETemp"]

    df[["SurveyID", "StartDate", "RouteID", "CrewLeader", "CLAffiliation", "CLPhone", "CLEmail", "TotalObs", "ObsNames","Precip", "Ice", "Fog", "SnowCover", "RteComplete"]].to_csv("surveys.csv", index=False)