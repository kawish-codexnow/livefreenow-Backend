from rest_framework.response import Response
from controllers.Classess.JWTConfig import JWT
from controllers.Classess import DPCS
from rest_framework.decorators import api_view
from controllers.APIs.usersApi import userApi
from controllers.Classess.pdfCaseSummary import pdfCaseSummary
from controllers.Classess.pdfCaseSumaryTagged import fetch_case_data_tagged
from controllers.Classess.lumbar_spine_flow_task import *
from controllers.Classess.SearchPortal import search_portal

jwt_auth = JWT()
sp = search_portal()
cs = ClinicalSummaryExtractor()


@api_view(['GET','POST'])
def auth(request):
    response = jwt_auth.login(request)
    return Response(response)

@api_view(['GET','POST'])
def getUser(request):
    token = jwt_auth.token_validation(request)
    if token["status"] == "False":
        return Response(token)
    response = jwt_auth.get_user(token)
    return Response(response)

@api_view(['GET', 'POST'])
def userapi(request):
    obj = userApi()
    result = obj.post(request)
    return Response(result)


@api_view(['GET'])
def FlushRedis(request):
    return Response(DPCS.DPCS().FlushRedis(0))


@api_view(['POST'])
def case_Summary(request):
    data = request.data
    if data["action"] == "get_all_case_no":
        return Response(pdfCaseSummary().get_all_case_no())
    elif data["action"] == "get_case_detail":
        return Response(pdfCaseSummary().fetch_case_data(data["case_number"]))
    elif data["action"] == "get_case_detail_tagged":
        return Response(fetch_case_data_tagged(data["case_number"],data["flag"]))


@api_view(['POST'])
def lumbar_spine_flow_task(request):

    data = request.data

    # new flow

    if data["action"] == "get_body_parts":
        return Response(cs.get_body_parts())
    elif data["action"] == "get_diseases":
        return Response(cs.get_diseases(data["body_part"]))
    elif data["action"] == "get_disease_data":
        return Response(cs.get_disease_data(data["diseases"]))
    elif data["action"] == "get_drugs":
        return Response(cs.get_drugs(data))
    elif data["action"] == "get_summary":
        return Response(cs.get_summary(data))

    # old flow

    # if data["action"] == "get_causes":
    #     return Response(get_causes_api(data["bodypart"]))
    # elif data["action"] == "get_symptoms_using_causes":
    #     return Response(get_symptom_using_causes(data["bodypart"],data["causes_name"]))
    # elif data["action"] == "get_disease_using_symptom":
    #     return Response(get_disease_using_symptom(data["symptom_name"]))
    # elif data["action"] == "get_drugs_ratio":
    #     return Response(get_drugs_ratio_api(data["disease_name"], data["symptom_name"]))
    # elif data["action"] == "get_treatments":
    #     return Response(get_treatments_of_disease(data["disease_name"]))
    # elif data["action"] == "get_clinical_summary":
    #     return Response(get_clinical_summary_without_causes(data["disease_name"], data["symptom_name"],data["drug_name"]))


    # Search Portal Api's

    elif data["action"] == "get_search_portal_columns":
        return Response(sp.get_column_names())
    elif data["action"] == "get_search_portal_sample_data":
        return Response(sp.reset_data())
    elif data["action"] == "get_search_portal_filter":
        return Response(sp.search_data(data['column_name'], data['val_to_search']))
    elif data["action"] == "reset_list":
        return Response(sp.reset_list())
    elif data["action"] == "get_list":
        return Response(sp.get_list())
    elif data["action"] == "get_search_portal_filter_new":
        return Response(sp.apply_search(data))
    elif data["action"] == "scheduler_search":
        return Response(sp.scheduler_search())
    elif data["action"] == "get_result":
        return Response(sp.get_result(data["result_code"]))