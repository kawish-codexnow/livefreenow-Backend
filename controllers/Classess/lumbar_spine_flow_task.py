import ast
import pickle
import pandas as pd
from tqdm.auto import tqdm
from spacy.lang.pt.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
import pt_core_news_sm

nlp = pt_core_news_sm.load()
tqdm.pandas()


class ClinicalSummaryExtractor:

    def __init__(self):
        self.med_df = pd.read_csv('./iponymData/csvstore/medical_data_cleaned1.csv')
        self.bdy_df = pd.read_csv('./iponymData/csvstore/bdy_part_data.csv')
        f = open('./iponymData/drug_symptoms/Drugs_Wiki_heading_names.pickle', 'rb')
        self.drugs = pickle.load(f)
        self.drugs = list(set([x.lower() for x in list(self.drugs.keys()) + list(self.drugs.values())]))

    def get_body_parts(self):
        try:
            body_parts = list(self.bdy_df['body_part'].unique())
            return {"msg": list(set(body_parts)), "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def get_diseases(self, body_part_name):
        try:
            self.selected_body_part = body_part_name
            self.filtered_bdy = self.bdy_df[self.bdy_df['body_part'] == body_part_name]
            diseases = list(self.bdy_df[self.bdy_df['body_part'] == body_part_name]['disease'].unique())
            return {"msg": list(set(diseases)), "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def get_disease_data(self, disease_names):

        try:
            self.selected_diseases = disease_names
            # filter data by selected disease
            self.filtered_bdy = self.filtered_bdy[self.filtered_bdy['disease'].str.contains(r'|'.join(disease_names))]
            # get causes from filtered data
            total_causes = [item for sublist in
                            list(self.bdy_df[self.bdy_df['disease'].str.contains(r'|'.join(disease_names))]['causes'])
                            for item in ast.literal_eval(sublist)]
            total_symptoms = [item for sublist in
                              list(self.bdy_df[self.bdy_df['disease'].str.contains(r'|'.join(disease_names))]['symptoms'])
                              for item in ast.literal_eval(sublist)]
            total_treatments = [item for sublist in
                                list(self.bdy_df[self.bdy_df['disease'].str.contains(r'|'.join(disease_names))][
                                         'treatments'])
                                for item in ast.literal_eval(sublist)]
            total_diagnosis = [item for sublist in
                               list(self.bdy_df[self.bdy_df['disease'].str.contains(r'|'.join(disease_names))]['diagnosis'])
                               for item in ast.literal_eval(sublist)]

            data_dict = {'causes': list(set(total_causes)), 'symptoms': list(set(total_symptoms)),
                         'treatments': list(set(total_treatments)), 'diagnosis': list(set(total_diagnosis))}
            return {"msg": data_dict, "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def get_drugs(self, selections):
        try:
            df_drugs = self.__get_clinical_summary(selections)
            drugs = list(set([x for x in self.drugs for y in df_drugs['clinical_summary'] if x in y]))
            return {"msg": list(set(drugs)), "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}


    def __get_clinical_summary(self, selections):
        body_part = selections['body_part']
        diseases = selections['diseases']
        causes = selections['causes']
        symptoms = selections['symptoms']
        treatments = selections['treatments']
        if 'diagnosis' in selections:
            diagnosis = selections['diagnosis']
        if 'drugs' in selections:
            drugs = selections['drugs']

        filtered_med = self.med_df[self.med_df['clinical_summary'].str.contains(body_part)]
        filtered_med = filtered_med[filtered_med['clinical_summary'].str.contains(r'|'.join(diseases))]
        filtered_med = filtered_med[filtered_med['clinical_summary'].str.contains(r'|'.join(causes))]
        filtered_med = filtered_med[filtered_med['clinical_summary'].str.contains(r'|'.join(symptoms))]
        filtered_med = filtered_med[filtered_med['clinical_summary'].str.contains(r'|'.join(treatments))]

        if 'diagnosis' in selections:
            filtered_med = filtered_med[filtered_med['clinical_summary'].str.contains(r'|'.join(diagnosis))]

        if 'drugs' in selections:
            filtered_med = filtered_med[filtered_med['clinical_summary'].str.contains(r'|'.join(drugs))]

        return filtered_med

    def generate_summary(self, collective_summary):
        doc = nlp(collective_summary)
        corpus = [sent.text.lower() for sent in doc.sents]
        cv = CountVectorizer(stop_words=list(STOP_WORDS))
        cv_fit = cv.fit_transform(corpus)
        word_list = cv.get_feature_names();
        count_list = cv_fit.toarray().sum(axis=0)
        word_frequency = dict(zip(word_list, count_list))
        val = sorted(word_frequency.values())
        higher_word_frequencies = [word for word, freq in word_frequency.items() if freq in val[-3:]]

        # gets relative frequency of words
        higher_frequency = val[-1]
        for word in word_frequency.keys():
            word_frequency[word] = (word_frequency[word] / higher_frequency)
        sentence_rank = {}
        for sent in doc.sents:
            for word in sent:
                if word.text.lower() in word_frequency.keys():
                    if sent in sentence_rank.keys():
                        sentence_rank[sent] += word_frequency[word.text.lower()]
                    else:
                        sentence_rank[sent] = word_frequency[word.text.lower()]
        top_sentences = (sorted(sentence_rank.values())[::-1])
        sent_len = len(top_sentences)

        if sent_len > 0:
            rank_to_take = ((sent_len * 10) / 100)
            rank_to_take = int(rank_to_take)
        if rank_to_take == 0:
            rank_to_take = 1

        top_sent = top_sentences[:3]
        summary = []
        for sent, strength in sentence_rank.items():
            if strength in top_sent:
                summary.append(sent)
            else:
                continue
        summary_to_show = []
        for i in summary:
            summary_to_show.append(str(i))

        return " ".join(summary_to_show)


    def get_summary(self, selections):
        try:
            df_cs = self.__get_clinical_summary(selections)
            if len(df_cs) > 5:
                df_cs = df_cs.head(5)
            case_decisions = list(df_cs['decision'].unique())
            case_summaries = {}
            for x in case_decisions:
                collective_summary = ' '.join(list(df_cs[df_cs['decision'] == x]['clinical_summary']))
                case_summaries[x] = self.generate_summary(collective_summary)
            return {"msg": case_summaries, "status": "True"}

        except Exception as e:
            return {"msg": e.__str__(), "status": "False"}
