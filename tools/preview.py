import matplotlib.pyplot as plt
import os
import json


def load_database(database_to_load):
    if (database_to_load != "" and os.path.exists(database_to_load)): # Check to see if the ALPR camera database exists.
        loaded_alpr_camera_database = json.load(open(database_to_load)) # Load the ALPR database.
    else:
        loaded_alpr_camera_database = {} # Load a blank database, since the actual database couldn't be loaded.
        if (database_to_load == ""): # The database entry was left empty.
            print("No database was specified")
        elif (os.path.exists(database_to_load) == False): # The specified database specified does not exist.
            print("The specified database does not exist.")
        else:
            print("An unknown error occurred")

    return loaded_alpr_camera_database # Return the loaded database information.


database_to_load = input("Database: ")
loaded_database = load_database(database_to_load)


x = []
y = []

for entry in loaded_database["entries"]:
    x.append(entry["longitude"])
    y.append(entry["latitude"])


plt.scatter(x, y, label = "Title", color = "green", marker = "X", s = 30)
plt.ylabel('Longitude')
plt.xlabel('Latitude')
# plot title
plt.title('Title')
# showing legend
#plt.legend()
  
# function to show the plot
plt.show()
