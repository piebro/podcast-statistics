import pandas as pd
import matplotlib.pyplot as plt
import os
import ast

# Create 'plots' directory if it doesn't exist
os.makedirs('plots', exist_ok=True)

# Read the CSV file
result_df = pd.read_csv('results.csv')

# Convert 'Datum' to datetime
result_df['Datum'] = pd.to_datetime(result_df['Datum'])

# Function to safely evaluate string as list and clean up the data
def eval_and_clean(x):
    try:
        items = ast.literal_eval(x)
        return [item.strip() for item in items if item.strip()] if isinstance(items, list) else []
    except (ValueError, SyntaxError):
        return []

# Function to split and count values
def split_and_count(series):
    return pd.Series([item for items in series.dropna() for item in eval_and_clean(items)]).value_counts()

# Calculate statistics for each person
def calculate_stats(name, total_proposals_all):
    proposals = result_df[result_df['Vorgeschlagen_von'] == name]
    total_proposals = len(proposals)
    approved_proposals = proposals['Endergebnis'].sum()
    approved_percentage = approved_proposals / total_proposals * 100 if total_proposals > 0 else 0
    #all_proposals = len(result_df)
    supported_proposals = sum(name in eval_and_clean(row) for row in result_df['Dafür'])
    opposed_proposals = sum(name in eval_and_clean(row) for row in result_df['Dagegen'])
    total_supported_opposed = supported_proposals + opposed_proposals
    supported_percentage = supported_proposals / total_supported_opposed * 100 if total_supported_opposed > 0 else 0
    opposed_percentage = opposed_proposals / total_supported_opposed * 100 if total_supported_opposed > 0 else 0
    
    return {
        'Anzahl an Vorschlägen': f"{total_proposals} ({total_proposals/total_proposals_all*100:.1f}%)",
        'Angenommene Vorschläge': f"{approved_proposals} ({approved_percentage:.1f}%)",
        'Vorschläge befürwortet': f"{supported_proposals} ({supported_percentage:.1f}%)",
        'Vorschläge nicht befürwortet': f"{opposed_proposals} ({opposed_percentage:.1f}%)"
    }

# Get unique names
names = set(result_df['Vorgeschlagen_von'].tolist() +
            sum((eval_and_clean(row) for row in result_df['Dafür'].dropna()), []) +
            sum((eval_and_clean(row) for row in result_df['Dagegen'].dropna()), []))

# Calculate total proposals for percentage calculation
total_proposals_all = len(result_df)

# Create the new table
new_table = pd.DataFrame([calculate_stats(name, total_proposals_all) for name in names])
new_table.set_index(pd.Index(names), inplace=True)

# Sort the table by 'Anzahl an Vorschlägen' (descending)
new_table = new_table.sort_values('Anzahl an Vorschlägen', key=lambda x: pd.to_numeric(x.str.split().str[0]), ascending=False)

# Generate the rest of the statistics
approved_proposals = result_df['Endergebnis'].sum()
rejected_proposals = total_proposals_all - approved_proposals
avg_proposals_per_episode = total_proposals_all / result_df['Episode'].nunique()

# Function to convert DataFrame to markdown table
def df_to_markdown(df):
    return df.to_markdown()

results = f"""# Zustimmungsrate Statistiken

## Allgemeine Statistiken
- Gesamtanzahl Vorschläge: {total_proposals_all}
- Angenommene Vorschläge: {approved_proposals} ({approved_proposals/total_proposals_all:.1%})
- Abgelehnte Vorschläge: {rejected_proposals} ({rejected_proposals/total_proposals_all:.1%})
- Anzahl der Episoden: {result_df['Episode'].nunique()}
- Zeitraum der Daten: von {result_df['Datum'].min().date()} bis {result_df['Datum'].max().date()}
- Durchschnittliche Anzahl Vorschläge pro Episode: {avg_proposals_per_episode:.2f}

## Detaillierte Statistiken pro Person
{df_to_markdown(new_table)}
"""

# Save statistics to results.md
with open('plots/Ergebnisse.md', 'w') as f:
    f.write(results)

# Plotting (keeping the original plot)
plt.figure(figsize=(12, 6))
result_df.groupby(result_df['Datum'].dt.to_period('M'))['Endergebnis'].mean().plot()
plt.title('Trend der Zustimmungsrate über Zeit')
plt.xlabel('Datum')
plt.ylabel('Zustimmungsrate')
plt.savefig('plots/approval_trend.png')
plt.close()

# New plot: Approval rate bar plot per number
approval_rates = result_df.groupby('Nummer')['Endergebnis'].mean()

plt.figure(figsize=(15, 8))
approval_rates.plot(kind='bar')
plt.title('Zustimmungsrate pro Vorschlagsnummer')
plt.xlabel('Vorschlagsnummer')
plt.ylabel('Zustimmungsrate')
plt.ylim(0, 1)  # Set y-axis limits from 0 to 1
plt.axhline(y=approval_rates.mean(), color='r', linestyle='--', label='Durchschnittliche Zustimmungsrate')
plt.legend()
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('plots/approval_rate_by_number.png')
plt.close()

# New code to create a list of accepted proposals
# Filter the DataFrame to include only accepted proposals
accepted_proposals = result_df[result_df['Endergebnis']]

# Sort the filtered DataFrame by date in descending order
sorted_proposals = accepted_proposals.sort_values('Datum', ascending=False)

# Create the content for the new markdown file
proposal_list = "# Liste der angenommenen Vorschläge\n\n"
for _, row in sorted_proposals.iterrows():
    proposal_list += f"{row['Datum'].strftime('%Y-%m-%d')}: {row['Beschreibung']}\n\n"

# Save the proposal list to a new markdown file
with open('plots/Angenommene_Vorschlagsliste.md', 'w') as f:
    f.write(proposal_list)

print("Plots and markdown files have been saved in the 'plots' directory.")