import pandas as pd
import spacy
from spacy import displacy
import re
import fnmatch

df = pd.read_csv('./iponymData/medical_data.csv')

def clean_txt(x):
    x = str(x)
    x = x.lower()
    start = x.find(' male ')

    if start == -1:
        start = x.find(' female ')
        if start != -1:
            x = x[start:]
    else:
        x = x[start:]

    x = x.replace('public copy v. 1.0', ' ')
    x = re.sub('[0-9]{2}[\/,:][0-9]{2}[\/,:][0-9]{2,4}', '', x)
    x = re.sub(" \d+", " ", x)
    x = re.sub("\d+", " ", x)
    x = re.sub('[^A-Za-z0-9]+', ' ', x)
    x = x.replace('\n', ' ')
    x = x.replace('\r', ' ')
    x = x.replace('\x0c', ' ')
    x = " ".join(x.split())
    x = x.split()
    x = [''.join(filter(str.isalnum, val)) for val in x]
    x = ' '.join(x)
    x = x.lower()
    txt = x.split()
    x = [x for x in txt if not x.isdigit() and fnmatch.fnmatch(x.lower(),'cm*') == False]
    x = ' '.join(x)


    return x


# In[5]:


def load_models():
    entity_model = spacy.load("en_core_sci_lg")
    chemical_model = spacy.load("en_ner_bc5cdr_md")
    organ_model = spacy.load("en_ner_bionlp13cg_md")
    protein_model = spacy.load('en_ner_jnlpba_md')
    bio_model = spacy.load('en_ner_craft_md')
    return entity_model, bio_model, chemical_model,protein_model, organ_model


# In[6]:


def get_entity_tags(case_number, nlp_core):
    record = df[df['case_number'] == case_number]
    record.reset_index(inplace=True)
    hifd = record['how_imr_final_determ'][0]
    cs = record['clinical_simmary'][0]
    ide = record['imr_decision_explan'][0]
    ids = record['imr_decision_summary'][0]

    hifd = clean_txt(hifd)
    cs = clean_txt(cs)
    ide = clean_txt(ide)
    ids = clean_txt(ids)

    entity_record = {}

    entity_doc = nlp_core(hifd)
    entity_record['how_imr_final_determination'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_core(cs)
    entity_record['clinical_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_core(ide)
    entity_record['imr_decision_explanation'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_core(ids)
    entity_record['imr_decision_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    return entity_record


# In[7]:


def get_chemical_tags(case_number, nlp_bc5):
    record = df[df['case_number'] == case_number]
    record.reset_index(inplace=True)
    hifd = record['how_imr_final_determ'][0]
    cs = record['clinical_simmary'][0]
    ide = record['imr_decision_explan'][0]
    ids = record['imr_decision_summary'][0]

    hifd = clean_txt(hifd)
    cs = clean_txt(cs)
    ide = clean_txt(ide)
    ids = clean_txt(ids)

    chemical_record = {}

    entity_doc = nlp_bc5(hifd)
    chemical_record['how_imr_final_determination'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_bc5(cs)
    chemical_record['clinical_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_bc5(ide)
    chemical_record['imr_decision_explanation'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_bc5(ids)
    chemical_record['imr_decision_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    return chemical_record


# In[8]:


def get_bio_tags(case_number, nlp_craft):
    record = df[df['case_number'] == case_number]
    record.reset_index(inplace=True)
    hifd = record['how_imr_final_determ'][0]
    cs = record['clinical_simmary'][0]
    ide = record['imr_decision_explan'][0]
    ids = record['imr_decision_summary'][0]

    hifd = clean_txt(hifd)
    cs = clean_txt(cs)
    ide = clean_txt(ide)
    ids = clean_txt(ids)

    bio_record = {}

    entity_doc = nlp_craft(hifd)
    bio_record['how_imr_final_determination'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_craft(cs)
    bio_record['clinical_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_craft(ide)
    bio_record['imr_decision_explanation'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_craft(ids)
    bio_record['imr_decision_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    return bio_record


# In[9]:


def get_protein_tags(case_number, nlp_jnl):
    record = df[df['case_number'] == case_number]
    record.reset_index(inplace=True)
    hifd = record['how_imr_final_determ'][0]
    cs = record['clinical_simmary'][0]
    ide = record['imr_decision_explan'][0]
    ids = record['imr_decision_summary'][0]

    hifd = clean_txt(hifd)
    cs = clean_txt(cs)
    ide = clean_txt(ide)
    ids = clean_txt(ids)

    protein_record = {}

    entity_doc = nlp_jnl(hifd)
    protein_record['how_imr_final_determination'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_jnl(cs)
    protein_record['clinical_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_jnl(ide)
    protein_record['imr_decision_explanation'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_jnl(ids)
    protein_record['imr_decision_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    return protein_record


# In[14]:


def get_organ_tags(case_number, nlp_cg13):
    record = df[df['case_number'] == case_number]
    record.reset_index(inplace=True)
    hifd = record['how_imr_final_determ'][0]
    cs = record['clinical_simmary'][0]
    ide = record['imr_decision_explan'][0]
    ids = record['imr_decision_summary'][0]

    hifd = clean_txt(hifd)
    cs = clean_txt(cs)
    ide = clean_txt(ide)
    ids = clean_txt(ids)

    organ_record = {}

    entity_doc = nlp_cg13(hifd)
    organ_record['how_imr_final_determination'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_cg13(cs)
    organ_record['clinical_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_cg13(ide)
    organ_record['imr_decision_explanation'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    entity_doc = nlp_cg13(ids)
    organ_record['imr_decision_summary'] = displacy.render(entity_doc, jupyter = False, style = 'ent').replace('\n', '')

    return organ_record



def soft_clean(x):
    x = str(x).replace("\\","")
    x = str(x).replace("\ ","")
    x = str(x).replace(" \ ","")
    return x


entity_model, bio_model, chemical_model,protein_model, organ_model  = load_models()

def fetch_case_data_tagged(case_number, flag):
    try:
        if flag=="entity_tags":
            entity_tags = get_entity_tags(case_number, entity_model)
            print(entity_tags.keys())
            return {"msg":soft_clean("CLINICAL SUMMARY:   " + entity_tags["clinical_summary"] + "   IMR FINAL:  " + entity_tags["how_imr_final_determination"] + "     IMR DECISION EXPLANATION:     " + entity_tags["imr_decision_explanation"]+ "   IMR DECISION SUMMARY:   " + entity_tags["imr_decision_summary"])
,"status":"True"}

        elif flag=="bio_tags":
            bio_tags = get_bio_tags(case_number, bio_model)
            return {"msg":soft_clean("CLINICAL SUMMARY:   " + bio_tags["clinical_summary"] + "   IMR FINAL:  " + bio_tags["how_imr_final_determination"] + "     IMR DECISION EXPLANATION:     " + bio_tags["imr_decision_explanation"]+ "   IMR DECISION SUMMARY:   " + bio_tags["imr_decision_summary"])
,"status":"True"}

        elif flag=="chemical_tags":
            chemical_tags = get_chemical_tags(case_number, chemical_model)
            return {"msg":soft_clean("CLINICAL SUMMARY:   " + chemical_tags["clinical_summary"] + "   IMR FINAL:  " + chemical_tags["how_imr_final_determination"] + "     IMR DECISION EXPLANATION:     " + chemical_tags["imr_decision_explanation"]+ "   IMR DECISION SUMMARY:   " + chemical_tags["imr_decision_summary"])
,"status":"True"}

        elif flag=="protein_tags":
            protein_tags = get_protein_tags(case_number, protein_model)
            return {"msg":soft_clean("CLINICAL SUMMARY:   " + protein_tags["clinical_summary"] + "   IMR FINAL:  " + protein_tags["how_imr_final_determination"] + "     IMR DECISION EXPLANATION:     " + protein_tags["imr_decision_explanation"]+ "   IMR DECISION SUMMARY:   " + protein_tags["imr_decision_summary"])
,"status":"True"}

        elif flag=="organ_tags":
            organ_tags = get_organ_tags(case_number, organ_model)
            return {"msg":soft_clean("CLINICAL SUMMARY:   " + organ_tags["clinical_summary"] + "   IMR FINAL:  " + organ_tags["how_imr_final_determination"] + "     IMR DECISION EXPLANATION:     " + organ_tags["imr_decision_explanation"]+ "   IMR DECISION SUMMARY:   " + organ_tags["imr_decision_summary"]),"status":"True"}

    except Exception as e:
        return {"msg": e.__str__(), "status": "False"}





