import sys
import pandas as pd
import openpyxl

MODEL = sys.argv[1]
OUT = 'analysis_out'
DATASETS = ['trivia_qa', 'squad', 'bioasq', 'nq', 'svamp']
KS = [10, 20, 30, 40, 50]
xlsx = f'{OUT}/count_index_all_{MODEL}.xlsx'

readme = pd.DataFrame({'item': [
    'Model / sampling', 'Per-question sheets', 'Index columns', 'Example (K=10)',
    'question / id', 'is_correct', 'num_clusters', 'count_min/max/mean/std',
    'lik_min/max/mean/std', 'discrete_entropy', 'semantic_entropy', 'Summary_by_K', 'Projection'],
 'meaning': [
    f'{MODEL}, temperature 1.0, 50 samples per question; K = number of samples used (the first K of the 50)',
    'One sheet per dataset and K. Each row is one question (400 per dataset, 300 for svamp).',
    'Columns K, K-1, ..., 1. The value under column s is the number of clusters that contain exactly s samples.',
    'Clusters of sizes 5, 3, 2 give: 0 0 0 0 0 1 0 1 1 0 (under columns 10 9 8 7 6 5 4 3 2 1)',
    'Question number and the dataset question id',
    '1 if the model low-temperature answer matched the reference, 0 if wrong',
    'Sum of the index row = number of clusters',
    'Min, max, mean, std of the count-based cluster probabilities (cluster size / K), computed from the index',
    'Same four stats for the likelihood-based cluster probabilities (from the model token probabilities)',
    'Entropy of the count-based cluster probabilities',
    'Entropy of the likelihood-based cluster probabilities (the paper main metric)',
    'Averages of the stats over questions, by dataset, group (all/correct/wrong) and K',
    'Not included. Only measured values.']})

with pd.ExcelWriter(xlsx, engine='openpyxl') as w:
    readme.to_excel(w, sheet_name='README', index=False)
    pd.read_csv(f'{OUT}/count_index_summary_by_K_{MODEL}.csv').round(4).to_excel(w, sheet_name='Summary_by_K', index=False)
    for ds in DATASETS:
        for K in KS:
            pd.read_csv(f'{OUT}/count_index_{MODEL}_{ds}_K{K}.csv').round(4).to_excel(w, sheet_name=f'{ds}_K{K}', index=False)
    for ws in w.book.worksheets:
        ws.freeze_panes = 'A2'
    w.book['README'].column_dimensions['A'].width = 26
    w.book['README'].column_dimensions['B'].width = 120

wb = openpyxl.load_workbook(xlsx, read_only=True)
print(len(wb.sheetnames), 'sheets saved to', xlsx)
