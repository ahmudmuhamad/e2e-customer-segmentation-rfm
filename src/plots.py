import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Define file paths
BASE_DIR = Path(__file__).resolve().parent.parent
FIGURES_PATH = BASE_DIR / "reports" / "figures"

# Ensure the figures directory exists
FIGURES_PATH.mkdir(parents=True, exist_ok=True)

def save_fig(fig_name, dpi=300):
    """
    Saves the current Matplotlib figure to the FIGURES_PATH.
    
    Args:
        fig_name (str): The name of the file (without extension).
        dpi (int): The resolution for the saved image.
    """
    path = FIGURES_PATH / f"{fig_name}.png"
    print(f"Saving figure to: {path}")
    plt.savefig(path, format='png', dpi=dpi, bbox_inches='tight')
    plt.close() # Close the plot to free memory

def plot_segment_distribution(df, fig_name):
    """
    Creates and saves a bar chart of the customer segment distribution.
    
    Args:
        df (pd.DataFrame): DataFrame containing the 'segment_name' column.
        fig_name (str): The name to save the figure as.
    """
    print(f"Plotting segment distribution and saving to {fig_name}...")
    segment_counts = df['segment_name'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        x=segment_counts.index, 
        y=segment_counts.values, 
        palette='viridis'
    )
    
    plt.title('Customer Segment Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Segment Name', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    
    # Add data labels
    for i, count in enumerate(segment_counts.values):
        plt.text(i, count + (segment_counts.values.max() * 0.01), 
                 str(count), 
                 ha='center', 
                 fontsize=10)
    
    # Save the figure
    save_fig(fig_name)