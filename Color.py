import geopandas as gpd
import matplotlib.pyplot as plt
import os
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
import colorcet as cc  # For interactive color palettes


# Function to list shapefiles
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
def choose_colormap(scheme_type, palette=None, custom_colors=None):
    """
    Choose a colormap based on scheme type, palette, or custom color stops.
    """
    if scheme_type == "dual_gradient":
        if not custom_colors or len(custom_colors) != 2:
            raise ValueError("Dual gradient requires exactly two colors (start and end).")
        return LinearSegmentedColormap.from_list("dual_gradient", custom_colors)
    if custom_colors:
        return LinearSegmentedColormap.from_list("custom", custom_colors)
    if scheme_type == "interactive":
        print("Available palettes from Colorcet:")
        print(cc.palette.keys())
        palette = input("Enter a palette name: ")
        return cc.palette.get(palette, "Blues")
    if scheme_type == "sequential":
        return palette if palette else "Blues"
    elif scheme_type == "divergent":
        return palette if palette else "RdBu"
    elif scheme_type == "qualitative":
        return palette if palette else "Set3"
    else:
        raise ValueError("Invalid scheme type. Choose 'sequential', 'divergent', 'qualitative', or 'dual_gradient'.")


# Function to plot GeoDataFrame with enhancements
def plot_geodataframe(
        gdf, column, scheme_type="sequential", palette=None, legend_bins=None, custom_colors=None, vmin=None, vmax=None
):
    cmap = choose_colormap(scheme_type, palette, custom_colors)

    # Normalize the data for the colorbar
    norm = Normalize(vmin=vmin if vmin else gdf[column].min(), vmax=vmax if vmax else gdf[column].max())

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the GeoDataFrame without the automatic legend
    gdf.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        edgecolor="black",
        linewidth=0.2,
        legend=False,  # Suppress automatic legend
        norm=norm
    )
    ax.set_title(f"Map: {column} ({scheme_type.replace('_', ' ').capitalize()})", fontsize=12)

    # Create a ScalarMappable for the colorbar
    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])  # Required for ScalarMappable
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical")
    cbar.set_label(column, fontsize=12)

    # Save option
    save_option = input("Do you want to save the map? (yes/no): ").lower()
    if save_option == "yes":
        output_file = input("Enter the filename to save (e.g., map.png): ")
        fig.savefig(output_file, dpi=500)
        print(f"Map saved as {output_file}.")

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
    print(gdf.columns)

    # Ask the user for input
    column = input("Enter the column name to visualize: ")

    # ColorBrewer links for guidance
    print("\nChoose a colormap type from the following options:")
    print("Sequential : for data that progresses (e.g., population density) _ https://colorbrewer2.org/#type=sequential&scheme=Blues&n=3")
    print("Divergent : for data with a central point (e.g., temperatures) _ https://colorbrewer2.org/#type=diverging&scheme=RdBu&n=3")
    print("Qualitative : for categorical data (e.g., land use types) _ https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=3")
    print("Dual Gradient : for a custom gradient between two colors (e.g., red to yellow)")
    print("Interactive : for exploratory visualization\n")

    scheme_type = input("Choose a colormap type (sequential, divergent, qualitative, interactive, dual_gradient): ").lower()
    palette = None
    custom_colors = None

    if scheme_type == "dual_gradient":
        print("Dual Gradient: Provide two colors for the gradient.")
        start_color = input("Enter the start color (e.g., #d7191c): ")
        end_color = input("Enter the end color (e.g., #fdae61): ")
        custom_colors = [start_color, end_color]

    elif scheme_type in ["sequential", "divergent", "qualitative"]:
        palette = input(f"Choose a palette for {scheme_type} (or press Enter for default): ")

    elif input("Do you want to use custom color stops? (yes/no): ").lower() == "yes":
        custom_colors = input("Enter custom colors as a comma-separated list (e.g., #d7191c,#fdae61,#2b83ba): ").split(",")

    legend_bins = input("Enter number of bins for the legend (or press Enter for default): ")
    legend_bins = int(legend_bins) if legend_bins else None

    vmin = input("Enter minimum value for the gradient (or press Enter for default): ")
    vmin = float(vmin) if vmin else None

    vmax = input("Enter maximum value for the gradient (or press Enter for default): ")
    vmax = float(vmax) if vmax else None

    # Check if the column exists
    if column in gdf.columns:
        plot_geodataframe(
            gdf, column, scheme_type, palette, legend_bins, custom_colors=custom_colors,
            vmin=vmin, vmax=vmax
        )
    else:
        print(f"Error: Column '{column}' does not exist in the shapefile.")
else:
    print("Error: Could not load the shapefile.")
