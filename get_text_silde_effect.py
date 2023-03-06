import pandas as pd
from bs4 import BeautifulSoup
import regex as re
import numpy as np

df_chidinh = pd.read_excel('D:/FRT/5.Python/tac_dung_phu/Frequent_less_rare/Frequent_less_rarely.xlsx')
df_disease = pd.read_excel('D:/FRT/5.Python/tac_dung_phu/Frequent_less_rare/Side_Effect.xlsx')


def new_trim_text(txt):
    words_list = txt.split(' ')
    remove_consecutive_space = ' '.join([word for word in words_list if word != ''])
    return remove_consecutive_space



def html_to_text_clean(filename):
    # remove_html_tags = BeautifulSoup(filename, 'lxml').text
    # replace_non_breaking_space = remove_html_tags.replace('\xa0', ' ')
    # remove_consecutive_space = new_trim_text(replace_non_breaking_space)
    uppercase = filename.upper()
    return uppercase


df_disease['disease_name'] = df_disease.Name.apply(lambda x: new_trim_text(x.upper()) if isinstance(x, str) else x)
df_disease.rename(columns={'Id': 'disease_id'}, inplace=True)
disease_list = df_disease.disease_name.dropna().drop_duplicates().to_list()

def extract_disease(txt):
    txt = new_trim_text(txt)
    diseases = list(filter(lambda x: re.findall(r'\b{}\b'.format(x), txt) != [],
                           disease_list))
    distinct_disease = []
    for disease in diseases:
        if disease not in distinct_disease:
            distinct_disease.append(disease)
    return '~'.join(distinct_disease)



def disease_family_lev(disease, disease_list):
    list_a = list(filter(lambda x: dq_fm_ldist_token_set_ratio(disease.split(' '), x.split(' ')) == 1, disease_list))
    list_b = filter(lambda x: len(x) == max(map(lambda x: len(x), list_a)), list_a)
    return '~'.join(list(list_b))


def dq_fm_LevenshteinDistance(token1, token2):
    """
    * Data Quality Function - Fuzzy Matching
    * dq_fm_LevenshteinDistance
    * Based off of https://gist.github.com/andrei-m/982927
    * input: Two strings to compare the edit distance of.
    * returns: Integer of the edit distance.
    * substitution: nltk.edit_distance(token1, token2) // Levenshtein.distance(token1, token2)
    """
    distances = np.zeros((len(token1) + 1, len(token2) + 1))


    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
      for t2 in range(1, len(token2) + 1):
        if (token1[t1 - 1] == token2[t2 - 1]):
            distances[t1][t2] = distances[t1 - 1][t2 - 1]
        else:
            a = distances[t1][t2 - 1]
            b = distances[t1 - 1][t2]
            c = distances[t1 - 1][t2 - 1]

            distances[t1][t2] = min(a, b, c) + 1

    return distances[len(token1)][len(token2)]

def dq_fm_ldist_ratio(in_a, in_b):
    """
    * Data Quality Function - Fuzzy Matching
    * dq_fm_ldist_ratio
    * input: Two strings to compare.
    * returns: The Levenshtein similarity ratio.
    """
    len_a = len(in_a)
    len_b = len(in_b)
    ratio = 1 - dq_fm_LevenshteinDistance(in_a, in_b) / (len_a + len_b)
    return ratio


def dq_trim(a):
    """
    * (Helper) Data Quality Function
    * dq_trim
    * This function converts all multiple consecutive spaces into single ones.
    * input: Uncleaned string
    * returns: String with a single space between each 2 words.
    """
    _list = a.split(' ')
    blank_removed = filter(lambda x: x != '', _list)
    merged = ' '.join(blank_removed)
    return merged



def dq_hf_gh_clean_tokenize(a):
    """
    * (Helper) Data Quality Function
    * dq_hf_gh_clean_tokenize
    * This function removes all non-alphanumeric characters.
    * input: Uncleaned string
    * returns: String of tokenized and cleaned string.
    """
    _accent = a  ##unidecode(a)
    _upper = _accent.upper().strip()
    _non_alpha_removed = re.sub(r'[^\p{L}0-9 ]+', '', _upper)
    _strip = dq_trim(_non_alpha_removed)
    _split = re.split(' ', _strip)
    return _split


def dq_distinct_list(arr):
    """
    * (Helper) Data Quality Function
    * dq_distinct_list
    * This function removes all duplicates of items in a list, preserves the order.
    * input: list
    * returns: List with unique order-preserved items.
    """
    unique_list = []
    for item in arr:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def dq_hf_gh_find_array_difference(arr_a, arr_b):
    """
    * (Helper) Data Quality Function
    * dq_hf_gh_find_array_difference
    * input: Two arrays to compare
    * returns: Array with elements a - b.
    """
    set_a = dq_distinct_list(arr_a)
    set_b = dq_distinct_list(arr_b)
    diff = list(filter(lambda x: x not in set_b, set_a))
    return diff



def dq_hf_gh_find_array_intersection(arr_a, arr_b):
    """
    * (Helper) Data Quality Function
    * dq_hf_gh_find_array_intersection
    * input: Two arrays to compare
    * returns: Array with the common elements
    """
    set_a = dq_distinct_list(arr_a)
    set_b = dq_distinct_list(arr_b)
    same = list(filter(lambda x: x in set_b, set_a))
    return same


def dq_fm_ldist_token_ratio(in_a, in_b):
    """
    * Data Quality Function - Fuzzy Matching
    * dq_fm_ldist_token_ratio
    * input: Two strings to compare.
    * returns: The Levenshtein similarity ratio with tokens.
    """
    token_a = ''.join(dq_hf_gh_clean_tokenize(in_a))
    token_b = ''.join(dq_hf_gh_clean_tokenize(in_b))
    ratio = dq_fm_ldist_ratio(token_a, token_b)
    return ratio



def dq_fm_ldist_token_set_ratio(in_a, in_b):
    """
    * Data Quality Function - Fuzzy Matching
    * dq_fm_ldist_token_set_ratio
    * input: Two strings to compare.
    * returns: The Levenshtein similarity of the maximum ratio
    * between the different token sets.
    """
    token_a = dq_hf_gh_clean_tokenize(' '.join(in_a))
    token_b = dq_hf_gh_clean_tokenize(' '.join(in_b))
    intersection = dq_hf_gh_find_array_intersection(token_a, token_b)
    intersection_str = ''.join(intersection)
    difference_ab = dq_hf_gh_find_array_difference(token_a, token_b)
    difference_ab_str = ''.join(difference_ab)
    difference_ba = dq_hf_gh_find_array_difference(token_b, token_a)
    difference_ba_str = ''.join(difference_ba)
    # First ratio is intersection and combined A diff B
    inter_diff_ab_ratio = dq_fm_ldist_ratio(intersection_str, intersection_str + difference_ab_str)
    # Second ratio is intersection and combined B diff A
    inter_diff_ba_ratio = dq_fm_ldist_ratio(intersection_str, intersection_str + difference_ba_str)
    # Third ratio is A diff B and B diff A
    inter_diff_abba_ratio = dq_fm_ldist_ratio(intersection_str + difference_ab_str,
                                              intersection_str + difference_ba_str)
    return max(inter_diff_ab_ratio, inter_diff_ba_ratio, inter_diff_abba_ratio)

df_chidinh['description'] =  df_chidinh.iloc[:, -4:].applymap(
    lambda x: html_to_text_clean(x) if isinstance(x, str) else ' ').sum(axis=1).str.strip()
df_chidinh['disease_group'] = df_chidinh.description.apply(lambda x: extract_disease(x))

initial_columns = df_chidinh.columns
temp = df_chidinh.disease_group.str.split('~', expand=True)
df_chidinh[temp.columns] = temp
df_chidinh = df_chidinh.melt(id_vars=initial_columns, value_vars=temp.columns, var_name='disease_order',
                             value_name='disease_name')
df_chidinh = df_chidinh[~df_chidinh.disease_name.isnull()].drop_duplicates().sort_values(by=['Code', 'disease_order'],
                                                                                         ascending=[True,
                                                                                                    True]).reset_index(
    drop=True)

df_chidinh['disease_lev'] = (df_chidinh.disease_name + '#' + df_chidinh.disease_group).apply(
    lambda x: disease_family_lev(x.split('#')[0], x.split('#')[1].split('~')))
temp = df_chidinh.disease_lev.str.split('~', expand=True)
df_chidinh[temp.columns] = temp
df_chidinh = df_chidinh.melt(id_vars=initial_columns, value_vars=temp.columns, var_name='disease_lev_order',
                             value_name='disease_lev_name')
df_chidinh = df_chidinh.merge(df_disease[['disease_name', 'disease_id']], left_on='disease_lev_name',
                              right_on='disease_name', how='left')
df_chidinh = df_chidinh[~df_chidinh.disease_lev_name.isnull()].drop_duplicates().sort_values(
    by=['Code', 'disease_lev_order'], ascending=[True, True]).reset_index(drop=True)
df_chidinh.drop_duplicates().to_excel('D:/FRT/5.Python/Template_boc_text/ketqua_vs_v3.xlsx', index=False)