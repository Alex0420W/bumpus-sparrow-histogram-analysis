import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

try:
    df = pd.read_excel('bumpus-data.xls', header=None, engine='xlrd')
except ImportError:
    df = pd.read_excel('bumpus-data.xls', header=None, engine='openpyxl')

# Filter for female sparrows (column 1 = 'f') and extract relevant columns
# Column 1: sex, Column 3: survival status (T=died, F=survived), Column 12: keel length
female_data = df[df.iloc[:, 1] == 'f'].copy()

# Separate died (T) and survived (F) groups
died_group = female_data[female_data.iloc[:, 3] == 'T']
survived_group = female_data[female_data.iloc[:, 3] == 'F']

# keel lengths (column 12)
keel_died = died_group.iloc[:, 12].dropna()
keel_survived = survived_group.iloc[:, 12].dropna()

print(f"Female sparrows analysis:")
print(f"Total females: {len(female_data)}")
print(f"Died: {len(keel_died)} | Survived: {len(keel_survived)}")
print(f"\nKeel length statistics:")
print(f"Died - Mean: {keel_died.mean():.4f}, Range: {keel_died.min():.3f} - {keel_died.max():.3f}")
print(f"Survived - Mean: {keel_survived.mean():.4f}, Range: {keel_survived.min():.3f} - {keel_survived.max():.3f}")

# Create histogram with 0.05 inch bins as suggested
bin_size = 0.05
min_val = min(keel_died.min(), keel_survived.min())
max_val = max(keel_died.max(), keel_survived.max())

# Create bin edges
bins = np.arange(np.floor(min_val/bin_size)*bin_size, 
                np.ceil(max_val/bin_size)*bin_size + bin_size, 
                bin_size)

# Create the histogram plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('Keel Length Distribution in Female House Sparrows\n(Bumpus 1898 Data)', 
             fontsize=14, fontweight='bold')

# Plot for birds that died
ax1.hist(keel_died, bins=bins, alpha=0.7, color='red', edgecolor='black', linewidth=0.5)
ax1.set_title(f'Birds that Died (n={len(keel_died)})', fontsize=12, color='red')
ax1.set_ylabel('Frequency')
ax1.set_xlim(min_val-0.02, max_val+0.02)
ax1.grid(True, alpha=0.3)

# Plot for birds that survived
ax2.hist(keel_survived, bins=bins, alpha=0.7, color='blue', edgecolor='black', linewidth=0.5)
ax2.set_title(f'Birds that Survived (n={len(keel_survived)})', fontsize=12, color='blue')
ax2.set_xlabel('Keel Length (inches)')
ax2.set_ylabel('Frequency')
ax2.set_xlim(min_val-0.02, max_val+0.02)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Create overlaid histogram for easier comparison
plt.figure(figsize=(10, 6))
plt.hist([keel_died, keel_survived], bins=bins, alpha=0.6, 
         color=['red', 'blue'], label=['Died (n=21)', 'Survived (n=28)'],
         edgecolor='black', linewidth=0.5)
plt.title('Keel Length Distribution: Died vs Survived Female House Sparrows', 
          fontsize=14, fontweight='bold')
plt.xlabel('Keel Length (inches)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


print(f"\nStatistical Analysis:")
print(f"T-test p-value: {stats.ttest_ind(keel_died, keel_survived)[1]:.4f}")
print(f"Mean difference (died - survived): {keel_died.mean() - keel_survived.mean():.4f}")

print(f"\nSelection Analysis:")
print(f"The histograms show the distribution of keel lengths in female sparrows.")
print(f"Mean keel length:")
print(f"- Died: {keel_died.mean():.4f} inches")  
print(f"- Survived: {keel_survived.mean():.4f} inches")
print(f"- Difference: {abs(keel_died.mean() - keel_survived.mean()):.4f} inches")

# Determining selection type based on the pattern
if abs(keel_died.mean() - keel_survived.mean()) < 0.01:
    selection_type = "stabilizing"
    explanation = "Both groups have very similar mean values, suggesting intermediate keel lengths were favored."
else:
    if keel_died.mean() < keel_survived.mean():
        selection_type = "directional (favoring larger keel lengths)"
        explanation = "Birds with smaller keel lengths were more likely to die, suggesting larger keel lengths were advantageous."
    else:
        selection_type = "directional (favoring smaller keel lengths)" 
        explanation = "Birds with larger keel lengths were more likely to die, suggesting smaller keel lengths were advantageous."

print(f"\nConclusion:")
print(f"Selection type: {selection_type}")
print(f"Explanation: {explanation}")