#Color schemes

import geopandas as gpd
import matplotlib.pyplot as plt
import os


# Function to list available shapefiles
def list_shapefiles(directory):

    all_files = os.listdir(directory)
    shapefiles = [file for file in all_files if file.endswith((".shp", ".SHP"))]
    return shapefiles


# Function to load a shapefile
def load_shapefile(file_name, directory):
    try:
        path = os.path.join(directory, file_name)
        gdf = gpd.read_file(path)
        print(f"Loaded {file_name} successfully!")
        return gdf
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        return None


# Function to choose a colormap
def choose_colormap(scheme_type, palette=None):

    if scheme_type == "sequential":
        return palette if palette else "Blues"
    elif scheme_type == "divergent":
        return palette if palette else "RdBu"
    elif scheme_type == "qualitative":
        return palette if palette else "Set3"
    else:
        raise ValueError("Invalid scheme type. Choose 'sequential', 'divergent', or 'qualitative'.")


# Function to plot the GeoDataFrame
def plot_geodataframe(gdf, column, scheme_type="sequential", palette=None):

    cmap = choose_colormap(scheme_type, palette)  # Get the colormap based on the scheme type and palette

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    gdf.plot(
        ax=ax,
        column=column,  # Color by the selected column
        cmap=cmap,  # Use the selected colormap
        edgecolor="black",  # Black boundaries
        legend=True  # Display legend
    )
    ax.set_title(f"Map USA {column} ({scheme_type.capitalize()})", fontsize=12)
    plt.show()


# Main script
directory = input("Enter the directory where your shapefiles are located: ")
if not os.path.exists(directory):
    print(f"Error: The directory '{directory}' does not exist.")
    exit()

shapefiles = list_shapefiles(directory)
if not shapefiles:
    print(f"No shapefiles found in the directory '{directory}'.")
    exit()

print("Available shapefiles:")
for i, shapefile in enumerate(shapefiles, 1):
    print(f"{i}. {shapefile}")

# Prompt user to select a shapefile
try:
    shapefile_index = int(input("Enter the number corresponding to the shapefile you want to use: ")) - 1
    selected_shapefile = shapefiles[shapefile_index]
except (IndexError, ValueError):
    print("Invalid selection. Exiting...")
    exit()

# Load the selected shapefile
gdf = load_shapefile(selected_shapefile, directory)

if gdf is not None:
    print("Columns available in the shapefile:")
    print(gdf.columns)  # Display available columns to the user

    # Ask the user for input
    column = input("Enter the column name to visualize: ")

    # ColorBrewer links for guidance
    print("\nChoose a colormap type from the following options:")
    print("Sequential : for data that progresses (e.g., population density) _ https://colorbrewer2.org/#type=sequential&scheme=Blues&n=3")
    print("Divergent : for data with a central point (e.g., temperatures) _ https://colorbrewer2.org/#type=diverging&scheme=RdBu&n=3")
    print("Qualitative : for categorical data (e.g., land use types) _ https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=3\n")

    scheme_type = input("Choose a colormap type (sequential, divergent, qualitative): ").lower()
    palette = input(f"Choose a palette for {scheme_type} (or press Enter for default): ")

    # Check if the column exists
    if column in gdf.columns:
        plot_geodataframe(gdf, column, scheme_type, palette)
    else:
        print(f"Error: Column '{column}' does not exist in the shapefile.")
else:
    print("Error: Could not load the shapefile.")