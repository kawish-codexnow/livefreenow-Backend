import ast
import numpy as np
import pandas as pd
import pickle
from spacy.lang.pt.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
import pt_core_news_sm
nlp = pt_core_news_sm.load()

causes_df = pd.read_csv('./iponymData/csvstore/causes_1.csv')
symptoms_df = pd.read_csv('./iponymData/csvstore/symptoms_1.csv')
bodyparts_df = pd.read_csv('./iponymData/csvstore/body_parts.csv')
drug_disease_df = pd.read_csv('./iponymData/csvstore/lumbar_data_n_1.csv')
drug_causes_df = pd.read_csv('./iponymData/csvstore/lumbar_data_causes_n_1.csv')



def get_symptoms(data):
    di_data = data.copy(deep=True)
    di_data = di_data[di_data['SYMPTOMS'].notna()]
    symptoms_list = list(di_data['SYMPTOMS'])
    flat_list = [item for sublist in symptoms_list for item in ast.literal_eval(sublist)]
    flat_list = list(set(flat_list))
    return flat_list


def get_bodyparts(data):
    body_parts = list(data['body_parts'])
    return body_parts

def get_causes(data):
    causes = list(data['CAUSES'])
    flat_list = []
    for x in causes:
        if x is not np.nan:
            flat_list.append(ast.literal_eval(x))
    flat_list = [item for sublist in flat_list for item in sublist]
    flat_list = list(set(flat_list))
    return flat_list


def get_all_diseases(data):
    disease_list = list(data['DISEASES'])
    flat_list = []
    for x in disease_list:
        if x is not np.nan:
            flat_list.append(ast.literal_eval(x))
    flat_list = [item for sublist in flat_list for item in sublist]
    flat_list = list(set(flat_list))
    flat_list = [x for x in flat_list if len(x.split()) <=3]
    return flat_list


def get_symptom_by_causes(data, cause_name):
    di_data = data.copy(deep=True)
    di_data = di_data[di_data['CAUSES'].notna()]
    try:
        causes = ast.literal_eval(cause_name)
    except:
        causes = cause_name

    if type(causes) is str:
        disease_data = di_data[di_data['CAUSES'].str.contains(causes)]
    elif type(causes) is list:
        di_data['Filtered'] = di_data['CAUSES'].str.findall('(' + '|'.join(causes) + ')')
        disease_data = di_data[di_data['Filtered'].astype(bool)]

    total = len(disease_data)
    approved = len(disease_data[disease_data['case_outcome'].str.contains('Overturn')])
    ratio = (approved / total) * 100
    disease_list = list(disease_data['SYMPTOMS'])
    flat_list = []
    for x in disease_list:
        if x is not np.nan:
            flat_list.append(ast.literal_eval(x))
    flat_list = [item for sublist in flat_list for item in sublist]
    flat_list = list(set(flat_list))
    return flat_list, ratio, disease_data


def get_disease_by_symptom(data, symptom_name):
    di_data = data.copy(deep=True)
    di_data = di_data[di_data['SYMPTOMS'].notna()]
    try:
        symptoms = ast.literal_eval(symptom_name)
    except:
        symptoms = symptom_name

    if type(symptoms) is str:
        disease_data = di_data[di_data['SYMPTOMS'].str.contains(symptoms)]
    elif type(symptoms) is list:
        di_data['Filtered'] = di_data['SYMPTOMS'].str.findall('(' + '|'.join(symptoms) + ')')
        disease_data = di_data[di_data['Filtered'].astype(bool)]

    total = len(disease_data)
    approved = len(disease_data[disease_data['case_outcome'].str.contains('Overturn')])
    ratio = (approved / total) * 100
    disease_list = list(disease_data['DISEASES'])
    flat_list = []
    for x in disease_list:
        if x is not np.nan:
            flat_list.append(ast.literal_eval(x))
    flat_list = [item for sublist in flat_list for item in sublist]
    flat_list = list(set(flat_list))
    return flat_list, ratio, disease_data


def get_drugs(data, disease_name):
    di_data = data.copy(deep=True)
    di_data = di_data[di_data['DISEASES'].notna()]
    try:
        diseases = ast.literal_eval(disease_name)
    except:
        diseases = disease_name

    if type(diseases) is str:
        disease_data = di_data[di_data['DISEASES'].str.contains(diseases)]
    elif type(diseases) is list:
        di_data['Filtered'] = di_data['DISEASES'].str.findall('(' + '|'.join(diseases) + ')')
        disease_data = di_data[di_data['Filtered'].astype(bool)]

    total = len(disease_data)
    approved = len(disease_data[disease_data['case_outcome'].str.contains('Overturn')])
    ratio = (approved / total) * 100
    disease_list = list(disease_data['DRUGS'])
    flat_list = []
    for x in disease_list:
        if x is not np.nan:
            flat_list.append(ast.literal_eval(x))
    flat_list = [item for sublist in flat_list for item in sublist]
    flat_list = list(set(flat_list))
    return flat_list, ratio, disease_data


#def get_specific_disease_cases(data, disease_name):
#    try:
#        print(type(disease_name))
#        print(disease_name)
#        di_data = data.copy(deep=True)
#        di_data = di_data[di_data['DISEASES'].notna()]
#        disease_data = di_data[di_data['DISEASES'].str.contains(disease_name)]
#        disease_cases = list(disease_data['case_number'])
#        return disease_cases
#    except Exception as e:
#        raise

def get_specific_disease_cases(data, disease_name):
    try:
        di_data = data.copy(deep=True)
        di_data = di_data[di_data['DISEASES'].notna()]
        try:
            diseases = ast.literal_eval(disease_name)
        except:
            diseases = disease_name

        if type(diseases) is str:
            disease_data = di_data[di_data['DISEASES'].str.contains(diseases)]
        elif type(diseases) is list:
            di_data['Filtered'] = di_data['DISEASES'].str.findall('(' + '|'.join(diseases) + ')')
            disease_data = di_data[di_data['Filtered'].astype(bool)]

        # disease_data = di_data[di_data['DISEASES'].str.contains(disease_name)]
        disease_cases = list(disease_data['case_number'])
        return disease_cases
    except Exception as e:
        raise

def get_drug_outcome(df, drugs, col_name):
    drug_outcome = {}
    for drug in drugs:
        x = 0
        total = 0
        if drug not in drug_outcome:
            drug_outcome[drug] = {'Overturn': 0, 'Uphold': 0, 'Total': 0}
        for case_drug in list(df[col_name]):
            if case_drug is np.nan:
                continue
            dr = ast.literal_eval(case_drug)
            if drug in dr and df['case_outcome'][x] == 'Overturn':
                drug_outcome[drug]['Overturn'] += 1
                total += 1
            elif drug in dr and df['case_outcome'][x] == 'Uphold':
                drug_outcome[drug]['Uphold'] += 1
                total += 1
            x += 1
        if total > 0:
            drug_outcome[drug]['Total'] = total
            drug_outcome[drug]['Ratio'] = drug_outcome[drug]['Overturn'] / total

    return drug_outcome


def get_drug_ratio(df, drugs, disease_name):
    disease_cases = get_specific_disease_cases(df, disease_name)

    df = df[df['case_number'].isin(disease_cases)]
    df.reset_index(inplace=True)

    drug_ratio = {}
    drug_outcome = get_drug_outcome(df, drugs, 'DRUGS')
    drug_not = []
    for x in drug_outcome.keys():
        if 'Ratio' in drug_outcome[x]:
            drug_ratio[x] = drug_outcome[x]['Ratio']
        else:
            drug_not.append(x)
    return drug_ratio


def get_causes_api(body_part):
    try:
        return {"msg": get_causes(drug_causes_df), "status": "True"}
    except Exception as e:
        return {"msg": e.__str__(), "status": "False"}


def get_symptom_using_causes(body_part, causes_name):
    try:
        diseases, ratio, data_df = get_symptom_by_causes(drug_causes_df, causes_name)
        # diseases = list(filter(None, diseases))
        return {"msg": {"symptoms": diseases, "ratio": round(ratio, 2)}, "status": "True"}
    except Exception as e:
        return {"msg": e.__str__(), "status": "False"}


def get_disease_using_symptom(symptom_name):
    try:
        diseases, ratio, data_diseases = get_disease_by_symptom(drug_disease_df, symptom_name)

        pickle_in = open("controllers/Classess/diseases_treatment.pickle", "rb")
        example_dict2 = pickle.load(pickle_in)
        final_final = []
        for x in diseases:
            if x in example_dict2.keys():
                final_final.append(x)
                diseases.remove(x)
        return {"msg": {"diseases": final_final + diseases, "ratio": round(ratio, 2)}, "status": "True"}
    except Exception as e:
        return {"msg": e.__str__(), "status": "False"}


def get_drugs_ratio_api(post_disease_name, post_symptom_name):
    try:
        diseases, ratio, data_diseases = get_disease_by_symptom(drug_disease_df, post_symptom_name)
        drugs, ratio, data_drugs = get_drugs(data_diseases, post_disease_name)
        return_lst = []

        # drugs = drugs[:random.randint(25,40)]
        #drug_ratio = get_drug_ratio(drug_disease_df, drugs, post_disease_name)
        #for k, v in drug_ratio.items():
        #    return_lst.append({"drug_name": str(k), "ratio": round(drug_ratio[k]  * 100 , 2)})

        drug_ratio = [0.0] * len(drugs)
        for x in range(0, len(drugs)):
             return_lst.append({"drug_name": drugs[x], "ratio": drug_ratio[x]})

        return {"msg": return_lst, "status": "True"}
    except Exception as e:
        #raise
        return {"msg": e.__str__(), "status": "False"}


def get_treatments_of_disease(post_disease_name):
    try:
        pickle_in = open("controllers/Classess/diseases_treatment.pickle", "rb")
        example_dict = pickle.load(pickle_in)
        treatments_list = []
        if type(post_disease_name) is str:
            treatments_list = example_dict[post_disease_name]
        elif type(post_disease_name) is list:
            for x in post_disease_name:
                if x in example_dict.keys():
                    treatments_list = treatments_list + example_dict[x]
        return {"msg": treatments_list, "status": "True"}

    except Exception as e:
        return {"msg": treatments_list, "status": "True"}
        # return {"msg": e.__str__(), "status": "False"}





# Clinical Summary extraction and summarization


def get_cs(data, drug_name):
    data_to_filter = data.copy(deep=True)
    data_to_filter = data_to_filter[data_to_filter['DRUGS'].notna()]

    try:
        drugs = ast.literal_eval(drug_name)
    except:
        drugs = drug_name

    if type(drugs) is str:
        disease_data = data_to_filter[data_to_filter['DRUGS'].str.contains(drugs)]
    elif type(drugs) is list:
        data_to_filter['Filtered'] = data_to_filter['DRUGS'].str.findall('(' + '|'.join(drugs) + ')')
        disease_data = data_to_filter[data_to_filter['Filtered'].astype(bool)]

    return disease_data


def generate_summary(collective_summary):
    doc = nlp(collective_summary)
    corpus = [sent.text.lower() for sent in doc.sents ]
    cv = CountVectorizer(stop_words=list(STOP_WORDS))
    cv_fit=cv.fit_transform(corpus)
    word_list = cv.get_feature_names();
    count_list = cv_fit.toarray().sum(axis=0)
    word_frequency = dict(zip(word_list,count_list))
    val=sorted(word_frequency.values())
    higher_word_frequencies = [word for word,freq in word_frequency.items() if freq in val[-3:]]

    # gets relative frequency of words
    higher_frequency = val[-1]
    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word]/higher_frequency)
    sentence_rank={}
    for sent in doc.sents:
        for word in sent :
            if word.text.lower() in word_frequency.keys():
                if sent in sentence_rank.keys():
                    sentence_rank[sent]+=word_frequency[word.text.lower()]
                else:
                    sentence_rank[sent]=word_frequency[word.text.lower()]
    top_sentences=(sorted(sentence_rank.values())[::-1])
    sent_len = len(top_sentences)

    if sent_len > 0:
        rank_to_take = ((sent_len * 10)/100)
        rank_to_take = int(rank_to_take)
    if rank_to_take == 0:
        rank_to_take = 1

    top_sent=top_sentences[:3]
    summary=[]
    for sent,strength in sentence_rank.items():
        if strength in top_sent:
            summary.append(sent)
        else:
            continue
    summary_to_show = []
    for i in summary:
        summary_to_show.append(str(i))

    return " ".join(summary_to_show)



def get_summary(data, drug):

    df_cs = get_cs(data, drug)
    case_decisions = list(df_cs['case_outcome'].unique())
    case_summaries = {}
    for x in case_decisions:
        collective_summary = ' '.join(list(df_cs[df_cs['case_outcome'] == x]['clinical_summary']))
        case_summaries[x] = generate_summary(collective_summary)
    return case_summaries



def get_clinical_summary_without_causes(post_disease_name, post_symptom_name, drug_name):
    try:
        diseases, ratio, data_diseases = get_disease_by_symptom(drug_disease_df, post_symptom_name)
        drugs, ratio, data_drugs = get_drugs(data_diseases, post_disease_name)
        return {"msg": get_summary(data_drugs, drug_name), "status": "True"}
    except Exception as e:
        return {"msg": e.__str__(), "status": "False"}