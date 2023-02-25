from email import message
from unicodedata import category
from .models import (
    AggregateCodes,
    Company,
    DataType,
    Ranges,
    Rates,
    Strategy,
    YearLimit,
    CFlow,
    Income,
    BSheet,
    Profile,
    KeyMetrics,
    FinGrowth,
    Institutional,
    KeyExecutives,
    IncomeGrowth,
    BSheetGrowth,
    CFlowGrowth,
    Ratios,
    RatiosTTM,
    EV,
    KeyMetricsTTM,
    MutualFund,
    Peers,
    Price,
    Dividend,
    AnalysisTools,
    CustomMetrics,
    CustomRatios,
    InvestingStyles,
    MetricsList,
)
import json
import uuid
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import DatabaseError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from numpy import dtype
import requests
import statistics
from django.apps import apps
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import render
import operator
from operator import itemgetter
from django.apps import apps
from .serializers import *
from rest_framework.views import APIView

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

# from .pagination import LargeResultsSetPagination

# importing function from python files
from .pyfiles.datatype import datatype_fun
from .pyfiles.fileupload import file_upload
from .pyfiles.analysis import analysis_function, custom_function, quote
from .pyfiles.analysis_latest import custom_function_latest, analysis_function_latest
from .pyfiles.financials import fin_func
from .pyfiles.reported_financials import reportedfin_func
from .pyfiles.profile_group import profile_func, profile_func2
from .pyfiles.keymetrics_group import keymetrics_func
from .pyfiles.rate_group import rate_func
from .pyfiles.financial_notes import financial_notes_func
from .pyfiles.market_data import market_data_func
from .pyfiles.smtp_send_email import sendMail
from .pyfiles.companyDetails import getCompanyMarketCap, getCompanyStockPrice, getCompaniesQuote, getScreenerCompaniesData

# from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression


# from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password

from rest_framework import generics

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework import status
from tickers.settings import GetConstants

# Create your views here.
global upload_data
data_json = []
upload_data = []
upload_columns = []
message_f = []
t_table = []

store_tables = [
    CFlow,
    Income,
    BSheet,
    Profile,
    KeyMetrics,
    FinGrowth,
    Institutional,
    KeyExecutives,
    IncomeGrowth,
    BSheetGrowth,
    CFlowGrowth,
    Ratios,
    RatiosTTM,
    EV,
    KeyMetricsTTM,
    MutualFund,
    Peers,
    Price,
    Dividend,
]

# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated, IsAdminUser)
#     serializer_class = UserSerializer
#     queryset = get_user_model().objects.all()

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)

#         serializer = UserSerializerWithToken(self.user).data
#         for k, v in serializer.items():
#             data[k] = v

#         return data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['role'] = "Admin" if user.is_superuser else "User"
    #     # ...

    #     return token
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['role'] = "Admin" if self.user.is_superuser else "User"
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ChangePasswordView(generics.UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgotPassword(request):
    data = request.data
    try:
        userObj = User.objects.filter(email=data['email'])
        if not userObj.exists():
            return Response({"message": ["Request failed please try again after sometime!"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            myuuid = uuid.uuid4()
            now = datetime.now()
            ForgotPassword.objects.create(
                userId=userObj[0].id,
                token=myuuid,
                used=False,
                generated_time=now
            )
            constants = GetConstants.getConstantsObj()
            sendMail("Invelp Forgotpassword Link", "<html><body><p>Here is the forgot password link to reset your password:</p> <br/> <h4><a href='" + constants['APP_BASE_URL'] + "/forgotpassword/update?token="+str(myuuid)+"'>Forgot Password</a></h4></html></body>", [data['email']], True)
            return Response({"response": "Email Sent Successfully! Check your mail for reset password link."})
    except Exception as e:
        return Response({"message": ["Request failed please try agian after sometime!"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgotPasswordValidateAndReset(request):
    data = request.data
    try:
        tokenObj = ForgotPassword.objects.filter(token=data['token'])
        if not tokenObj.exists():
            return Response({"message": ["Invalid Token"]}, status=status.HTTP_400_BAD_REQUEST)
        userObj = User.objects.filter(id=tokenObj[0].userId)
        if not userObj.exists():
            return Response({"message": ["Invalid Data"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = userObj[0]
            user.password = make_password(data['password'])
            user.save()
            return Response({"response": "Password Updated successfully"})
    except Exception as e:
        return Response({"message": ["Failed to reset password"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        firstName=data.get("firstname")
        lastName=data.get('lastname')
        userEmail=data.get('email')
        password = data.get('password')
        User.objects.create(
            first_name=firstName,
            last_name=lastName,
            username=userEmail,
            email=userEmail,
            is_staff=False,
            is_active=False,
            is_superuser=False,
            password=make_password(password)
        )
        mailContent = "New User Signed up for invelp app with Name: " + firstName + " " + lastName + " and email is: " + userEmail
        sendMail("Invelp New Member SignUp", mailContent, ['support@invelps.com'], False)
        return Response({"response": "User Registerd Successfully"})
    except Exception as e:
        message = e
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user

    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']

    user.save()

    return Response({"response": "User profile updated successfully"})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserPassword(request):
    user = request.user

    data = request.data
    user.password = make_password(data['password'])
    user.save()

    return Response({"response": "User password Reset successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)

    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']
    user.is_superuser = data['is_superuser']
    user.is_active = data['is_active']

    user.save()
    return Response({"response": "User Data Updated Successfully"})

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')


@api_view(['POST'])
def contactMailInfo(request):
    data = request.data
    try:
        now = datetime.now()
        ContactMailInfo.objects.create(
            email=data['email'],
            name=data['name'],
            subject=data['subject'],
            message=data['message'],
            timestamp=now
        )
        return Response({"response": "Information received successfully!"})
    except Exception as e:
        return Response({"message": ["Failed to Contact"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getContactMailInfo(request):
    try:
        respData = ContactMailInfo.objects.all()
        output = []
        get_data = [{"id": i.id, "email": i.email, "name": i.name, "subject": i.subject, "message": i.message, "timestamp": i.timestamp, "responded": i.responded} for i in respData]
        for emailData in get_data:
            emailData['isActive'] =  User.objects.filter(email=emailData['email']).exists()
            output.append(emailData)
        return Response({"response": output})
    except Exception as e:
        return Response({"message": ["Failed to get Contact Info"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateContactMailInfo(request):
    data = request.data
    try:
        respData = ContactMailInfo.objects.get(id=data['id'])
        respData.responded = data['responded']
        respData.save()
        return Response({"response": "Status Updated successfully!"})
    except Exception as e:
        print(e)
        return Response({"message": ["Failed to Update Status"]}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def analysisModel(request):
    return render(request, "pages/context_analysis_model.html")


@csrf_exempt
def investingStyle(request):
    return render(request, "pages/context_investing_style.html")


@csrf_exempt
def screenModel(request):
    return render(request, "pages/context_screen_model.html")


@csrf_exempt
def dpInvestingStyle(request):
    return render(request, "pages/dp_investing_style.html")


@csrf_exempt # This function is legacy should be deleted
def index(request):
    global t_table
    datatypes = DataType.objects.all()
    companies_list = Company.objects.distinct().values("company_name")
    exchanges = Company.objects.distinct().values("exchange")
    sectors = Company.objects.distinct().values("sector")
    industries = Company.objects.distinct().values("industry")
    years = YearLimit.objects.all()
    if request.method == "POST":
        p_data = request.POST
        p_company = p_data.get("Company")
        p_companies = p_data.get("companies")
        if (p_companies) is None:
            t_table = p_data.get("dtable")
            try:
                excel_file = request.FILES["excel_file"]
                global upload_data
                global upload_columns
                global message_f
                message_f, upload_data, upload_columns = file_upload(
                    t_table, excel_file
                )
                return redirect(upload_results)
            except Exception as e:
                print(e)
                return render(
                    request,
                    "pages/index.html",
                    {
                        "datatype": datatypes,
                        "years": years,
                        "file_m": "Error check again the uploaded file and its columns, columns name should be in lowercase.",
                    },
                )

        p_api = p_data.get("api")
        p_year = p_data.get("year")
        p_dtype = p_data.get("dtype")

        p_companies = [x.strip()
                       for x in p_companies.split(",")]
        p_companies = [x for x in p_companies if len(x) > 1]

        p_companies = [x.replace("\r", "") for x in p_companies]

        data_set = []
        global data_json
        companies = []
        for x in p_companies:
            _symbol = Company.objects.filter(company_name__istartswith=x)
            _symbol = _symbol[0]
            companies.append(_symbol.symbol)
            request.session["p_datatype"] = p_dtype
        result_got = datatype_fun(companies, p_dtype, p_year)
        if result_got == "api error":

            return render(
                request,
                "pages/index.html",
                {"datatype": datatypes, "years": years,
                    "companies": companies_list, "exchanges": exchanges,
                 "sectors": sectors,
                 "industries": industries,
                    "error": "API key invalid."},
            )
        elif result_got == "other error":
            return render(
                request,
                "pages/index.html",
                {
                    "datatype": datatypes,
                    "years": years,
                    "companies": companies_list, "exchanges": exchanges,
                    "sectors": sectors,
                    "industries": industries,
                    "error": "Error while retrievig data.",
                },
            )
        elif result_got == "not available":
            return render(
                request,
                "pages/index.html",
                {
                    "datatype": datatypes,
                    "years": years,
                    "companies": companies_list, "exchanges": exchanges,
                    "sectors": sectors, "industries": industries,
                    "error": f"{p_dtype} datatype is not avaibale right now.",
                },
            )
        else:
            global data_json
            data_json = result_got

            # return redirect(results)

    return render(request, "pages/index.html", {"datatype": datatypes, "companies": companies_list, "exchanges": exchanges,
                                                "sectors": sectors,
                                                "industries": industries, "years": years})


def results(request):
    datatypes = DataType.objects.all()
    years = YearLimit.objects.all()
    data_type = request.session["p_datatype"]
    global data_json

    paginator = Paginator(data_json, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "pages/result.html",
        {
            "dtype": data_type,
            "page_obj": page_obj,
            "datatype": datatypes,
            "years": years,
        },
    )


@csrf_exempt
def upload_results(request):
    datatypes = DataType.objects.all()
    years = YearLimit.objects.all()
    global upload_data

    global upload_columns

    global message_f

    global t_table

    count_ = len(upload_data)
    data_list = []
    try:
        model_name = upload_data[0]._meta.model.__name__
        if request.method == "POST":

            u_data = request.POST
            text_ = u_data.get("uploadarea")

            o_id = text_.split("\n")[0].split(",")[0].replace("[", "")

            n_text = text_.split("\n")[-1].split("   ")
            Model = apps.get_model("tick_app", model_name)
            entry = Model.objects.get(pk=o_id)
            for i, j in enumerate(upload_columns):
                setattr(entry, j, n_text[i])
            entry.save()

            upload_data = Model.objects.order_by("-id")[:count_][::-1]

        for j in upload_data:
            data_l = [getattr(j, "id")]
            for i in upload_columns:
                data_l.append(getattr(j, i))
            data_list.append(data_l)

        paginator = Paginator(data_list, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        codes_ = AggregateCodes.objects.filter(source=t_table)

        return render(
            request,
            "pages/upload_result.html",
            {
                "code": codes_,
                "count": count_,
                "model": model_name,
                "page_obj": page_obj,
                "datatype": datatypes,
                "years": years,
                "columns": upload_columns,
                "file_m": message_f,
            },
        )
    except Exception as e:

        print(e)

        return render(
            request,
            "pages/index.html",
            {
                "datatype": datatypes,
                "years": years,
                "file_m": f"Temporary upload data lost due to idleness. {e}",
            },
        )


def suggest(request, keyword):

    suggest_ = Company.objects.filter(company_name__istartswith=keyword)
    suggest_ = suggest_[:6]
    suggest_ = [x.company_name for x in suggest_]

    return JsonResponse(suggest_, safe=False)


def suggest_super(request, keyword):

    if "CustomRatios" in keyword:
        suggest_ = CustomRatios.objects.filter()

        suggest_ = list(set([x.measure for x in suggest_]))

    else:
        suggest_ = AnalysisTools.objects.filter(tools__istartswith=keyword)

        suggest_ = list(set([x.super_category for x in suggest_]))

    return JsonResponse(suggest_, safe=False)


def suggest_category(request, keyword):
    tool = keyword.split("-")[0]
    cat_ = keyword.split("-")[1]
    if "CustomRatios" in keyword:

        suggest_ = CustomRatios.objects.filter(measure__istartswith=cat_)

        suggest_ = list(set([x.category for x in suggest_]))

    else:
        suggest_ = AnalysisTools.objects.filter(tools__istartswith=tool).filter(
            super_category__istartswith=cat_
        )

        suggest_ = list(set([x.category for x in suggest_]))

    return JsonResponse(suggest_, safe=False)


def suggest_metrics(request, keyword):
    tool = keyword.split("-")[0]
    scat_ = keyword.split("-")[1]
    cat_ = keyword.split("-")[2]
    if "CustomRatios" in keyword:

        suggest_ = CustomRatios.objects.filter(measure__istartswith=scat_).filter(
            category__istartswith=cat_
        )

        suggest_ = list(set([x.metrics for x in suggest_]))
    else:

        suggest_ = (
            AnalysisTools.objects.filter(tools__istartswith=tool)
            .filter(super_category__istartswith=scat_)
            .filter(category__istartswith=cat_)
        )

        suggest_ = list(set([x.metrics for x in suggest_]))

    return JsonResponse(suggest_, safe=False)


def suggest_ranges(request, keyword):
    metrics_list = keyword.split(",")
    suggest_ranges = []
    for metric in metrics_list:
        filter_ranges = Ranges.objects.filter(metrics=metric)
        filter_ranges = [x.name for x in filter_ranges]
        suggest_ranges.extend(filter_ranges)

    return JsonResponse(suggest_ranges, safe=False)


@csrf_exempt
def data_processing(request):
    return render(request, "pages/data_processing.html")


@csrf_exempt # THIS FUNCTION IS LEGACY AND NEED TO BE DELETED 
def data_analysis(request):
    types = AnalysisTools.objects.all()
    ranges = Ranges.objects.all()
    ranges = list(set([x.name for x in ranges]))
    types = list(set([i.tools.lower() for i in types]))
    types.append("CustomRatios")
    if request.method == "POST":
        try:
            d_data = request.POST
            tool = d_data.get("types")
            scat = d_data.get("sc")
            cat = d_data.get("cat")

            d_companies = d_data.get("textarea")
            d_metrics = d_data.get("textmetrics")
            d_ranges = d_data.get("rangemetrics")
            from_ = d_data.get("from")
            to_ = d_data.get("to")
            date_range = list(range(int(from_), int(to_) + 1))
            date_range = [str(x) for x in date_range]
            n_years = len(date_range)
            # d_companies = [
            #     x.replace("|", "") for x in d_companies.split("|||||| ||||||")
            # ]
            d_companies = [x for x in d_companies if len(x) > 1]
            # d_metrics = [x.replace("|", "")
            #              for x in d_metrics.split("|||||| ||||||")]
            d_metrics = [x for x in d_metrics if len(x) > 1]
            # d_ranges = [x.replace("|", "")
            #             for x in d_ranges.split("|||||| ||||||")]
            d_ranges = [x for x in d_ranges if len(x) > 1]
            d_companies = [x.lstrip() for x in d_companies]
            d_companies = [x.rstrip() for x in d_companies]
            d_metrics = [x.lstrip() for x in d_metrics]
            d_metrics = [x.rstrip() for x in d_metrics]
            d_ranges = [x.lstrip() for x in d_ranges]
            d_ranges = [x.rstrip() for x in d_ranges]

            if "CustomRatios" in tool:
                return_list, plt_bar, plt_line = custom_function(
                    d_metrics, scat, cat, tool, d_companies, date_range, d_ranges
                )

            else:

                return_list, plt_bar, plt_line = analysis_function(
                    d_metrics, scat, cat, tool, d_companies, date_range, d_ranges
                )

            return render(
                request,
                "pages/danalysis.html",
                {
                    "ranges_": ranges,
                    "n_years": n_years,
                    "types": types,
                    "return_list": return_list,
                    "date_range": date_range,
                    "plot_bar": plt_bar,
                    "plot_line": plt_line,
                    "companies": ", ".join(d_companies),
                    "tool": tool,
                    "metrics": ", ".join(d_metrics),
                    "ranges": ", ".join(d_ranges),
                    "from": from_,
                    "to": to_,
                    "sc": scat,
                    "cat": cat,
                },
            )
        except Exception as e:
            print(str(e))

    return render(request, "pages/danalysis.html", {"types": types, "ranges_": ranges})


@csrf_exempt
def lregression(request):

    if request.method == "POST":

        d_data = request.POST
        p_company = d_data.get("company_name")
        from_ = d_data.get("from")
        to_ = d_data.get("to")
        p_api = d_data.get("api")
        p_symbol = Company.objects.filter(company_name__istartswith=p_company)
        p_symbol = p_symbol[0].symbol

        plt_line, table_df = quote(p_symbol, p_company, p_api, from_, to_)
        list_close = [float(x) for x in list(table_df["close"])]
        len_close = len(list(table_df["close"]))
        mean_ = sum(list_close) / len_close
        sd_ = statistics.stdev(list_close)
        rsd_ = sd_ / mean_
        sdt = 2 * sd_
        rsdt = 2 * rsd_

        tabledf = {
            "mean": round(mean_, 2),
            "sd": round(sd_, 2),
            "rsd": round(rsd_, 2),
            "2sd": round(sdt, 2),
            "2rsd": round(rsdt, 2),
        }
        return render(
            request,
            "pages/lregression.html",
            {"plot_line": plt_line, "tabledf": tabledf},
        )
    return render(request, "pages/lregression.html")


@csrf_exempt
def create_metrics(request):

    # import pdb; pdb.set_trace()
    custom_ratios = CustomRatios.objects.all()
    # print(custom_rat1ios)
    custom_metrics = CustomMetrics.objects.all()
    # calculate total no. of pages
    n = 15

    pagno = 1 if len(request.GET) == 0 else request.GET["id"]
    start = (int(pagno) - 1) * n
    end = start + n
    page = len(custom_ratios) // n
    rem = len(custom_ratios) % n
    if rem > 0:
        pages = int(page) + 1
    else:
        pages = int(page)

    c_tools = [
        x for x in list(set([x.tools for x in custom_metrics])) if "nan" not in x
    ][start:end]
    c_measure = [
        x for x in list(set([x.measure for x in custom_metrics])) if "nan" not in x
    ][start:end]
    c_metrics = [
        x for x in list(set([x.metrics for x in custom_metrics])) if "nan" not in x
    ][start:end]
    c_category = [
        x for x in list(set([x.category for x in custom_metrics])) if "nan" not in x
    ][start:end]

    if request.method == "POST":
        cm_data = request.POST
        cm_measure = cm_data.get("measure_input")
        cm_category = cm_data.get("category_input")
        cm_metric = cm_data.get("metric_input")
        cm_code = cm_data.get("code_input")
        cm_numerator = cm_data.get("numerator_input")
        cm_denominator = cm_data.get("denominator_input")

        if "add-new-metric" in cm_metric:
            cm_text = cm_data.get("textarea")
            cm_text = cm_text.split("|")
            r_id = cm_text[0]
            r_measure = cm_text[1]
            r_category = cm_text[2]
            r_metrics = cm_text[3]
            r_code = cm_text[4]
            r_numerator = cm_text[5]
            r_denominator = cm_text[6]

            row_entry = CustomRatios.objects.get(pk=r_id)

            row_entry.measure = r_measure
            row_entry.category = r_category
            row_entry.metrics = r_metrics
            row_entry.code = r_code
            row_entry.numerator = r_numerator
            row_entry.denominator = r_denominator

            row_entry.save()

        elif "del-metricrow" in cm_metric:
            pk_id = cm_metric.split("-")[-1]
            CustomRatios.objects.filter(id=pk_id).delete()

        else:

            cr_entry = CustomRatios(
                measure=cm_measure,
                category=cm_category,
                metrics=cm_metric,
                code=cm_code,
                denominator=cm_denominator,
                numerator=cm_numerator,
            )

            cr_entry.save()
            custom_ratios = CustomRatios.objects.all()

    p = Paginator(custom_ratios, 1)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get("id")
    if page_number == None:
        page_number = 1

    try:
        page_obj = page_number  # returns the desired page object
    except Exception as PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except Exception as EmptyPage:
        # if page is empty then return last page
        page_obj = page_number

    return render(
        request,
        "pages/createmetrics.html",
        {
            "c_ratios": custom_ratios[start:end],
            "c_tools": c_tools,
            "c_measure": c_measure,
            "c_metrics": c_metrics,
            "c_category": c_category,
            "pages": [i + 1 for i in range(pages)],
            "totalPages": int(len(custom_ratios) / n) + 1,
            "start": start,
            "end": end,
            "page_obj": int(page_obj),
            "index1": int(page_obj) - 2,
            "index2": int(page_obj) - 1,
        },
    )


@csrf_exempt
def financials(request):

    if request.method == "POST":
        f_data = request.POST
        f_company = f_data.get("company")
        f_table = f_data.get("table")
        f_from = f_data.get("from")
        f_to = f_data.get("to")

        fin_table, range_date = fin_func(f_company, f_table, f_from, f_to)
        f_data = {"company": f_company,
                  "table": f_table, "from": f_from, "to": f_to}
        return render(
            request,
            "pages/financial.html",
            {"date_range": range_date, "return_list": fin_table, "f_data": f_data},
        )

    return render(request, "pages/financial.html")


rf_table = ""
rf_data = ""
rf_columns = ""


@csrf_exempt
def reported_financials(request):
    global rf_table
    global rf_data
    global rf_columns

    if request.method == "POST":
        f_data = request.POST
        f_company = f_data.get("company")
        f_table = f_data.get("table")
        f_year = f_data.get("year")

        rf_table, rf_columns = reportedfin_func(f_company, f_table, f_year)
        rf_data = {"company": f_company, "table": f_table, "year": f_year}
        paginator = Paginator(rf_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/reported_financial.html",
            {"page_obj": page_object, "f_data": rf_data, "columns": rf_columns},
        )
    elif "page" in str(request):

        paginator = Paginator(rf_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/reported_financial.html",
            {"page_obj": page_object, "f_data": rf_data, "columns": rf_columns},
        )

    return render(request, "pages/reported_financial.html")


p_table = ""
p_data = ""
p_columns = ""


@csrf_exempt
def profile_group(request):
    global p_table
    global p_data
    global p_columns

    if request.method == "POST":
        f_data = request.POST
        f_company = f_data.get("company")
        f_table = f_data.get("table")

        p_table, p_columns = profile_func(f_company, f_table)
        p_data = {"company": f_company, "table": f_table}

        if "profile" in f_table:
            return render(
                request,
                "pages/profile_group.html",
                {"p_table": p_table, "f_data": p_data},
            )
        else:
            paginator = Paginator(p_table, 20)
            page_number = request.GET.get("page")
            page_object = paginator.get_page(page_number)
            return render(
                request,
                "pages/profile_group.html",
                {"page_obj": page_object, "f_data": p_data, "columns": p_columns},
            )
    elif "page" in str(request):

        paginator = Paginator(p_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/profile_group.html",
            {"page_obj": page_object, "f_data": p_data, "columns": p_columns},
        )

    return render(request, "pages/profile_group.html")


@csrf_exempt
def keymetrics_group(request):

    if request.method == "POST":
        f_data = request.POST
        f_company = f_data.get("company")
        f_table = f_data.get("table")

        k_table = keymetrics_func(f_company, f_table)
        k_data = {"company": f_company, "table": f_table}

        return render(
            request,
            "pages/keymetrics_group.html",
            {"p_table": k_table, "f_data": k_data},
        )

    return render(request, "pages/keymetrics_group.html")


r_table = ""
r_data = ""


@csrf_exempt
def rate_group(request):
    global r_table
    global r_data
    entries = Rates.objects.all()
    countries = list(set([str(x.country).strip() for x in entries]))
    rates = list(set([str(x.rate_type).lstrip() for x in entries]))

    if request.method == "POST":
        f_data = request.POST
        f_country = f_data.get("country")

        f_rate_type = f_data.get("rate_type")
        f_from = f_data.get("from")
        f_to = f_data.get("to")

        r_table = rate_func(f_country, f_rate_type, f_from, f_to)
        r_data = {"country": f_country, "from": f_from,
                  "to": f_to, "rate": f_rate_type}
        paginator = Paginator(r_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        return render(
            request,
            "pages/rate_group.html",
            {
                "page_obj": page_object,
                "f_data": r_data,
                "countries": countries,
                "rates": rates,
            },
        )

    elif "page" in str(request):

        paginator = Paginator(r_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/rate_group.html",
            {
                "countries": countries,
                "f_data": r_data,
                "rates": rates,
                "page_obj": page_object,
            },
        )

    return render(
        request, "pages/rate_group.html", {
            "countries": countries, "rates": rates}
    )


fn_data = ""
fn_table = ""
fn_columns = ""


# strategy_dp


@csrf_exempt
def strategies(request):

    return render(request, "pages/strategy_dp.html")


@csrf_exempt
def ranges_dp(request):
    return render(request, "pages/ranges_dp.html")


@csrf_exempt
def aggragate_fiancials(request):
    return render(request, "pages/aggragate_fiancials.html")


@csrf_exempt
def model_dp(request):
    return render(request, "pages/model_dp.html")


@csrf_exempt
def advancedRatios(request):
    return render(request, "pages/advancedRatios.html")


@csrf_exempt
def financial_notes(request):
    global fn_data
    global fn_columns
    global fn_table

    if request.method == "POST":
        f_data = request.POST
        f_company = f_data.get("company")

        f_table = f_data.get("table")
        f_from = f_data.get("from")
        f_to = f_data.get("to")

        fn_data = {"company": f_company, "from": f_from,
                   "to": f_to, "table": f_table}

        fn_table, fn_columns = financial_notes_func(
            f_company, f_table, f_from, f_to)

        paginator = Paginator(fn_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/financial_notes.html",
            {"page_obj": page_object, "f_data": fn_data, "columns": fn_columns},
        )

    elif "page" in str(request):

        paginator = Paginator(fn_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/financial_notes.html",
            {"page_obj": page_object, "f_data": fn_data, "columns": fn_columns},
        )

    return render(request, "pages/financial_notes.html")


@csrf_exempt
def ranges(request):
    ranges_list = Ranges.objects.all()
    metricslist = list(set([x.metrics for x in ranges_list]))

    if request.method == "POST":
        f_data = request.POST
        f_metric = f_data.get("metric")
        data = Ranges.objects.filter(metrics=f_metric)
        return render(
            request,
            "pages/ranges.html",
            {"data_list": data, "metric": f_metric, "metricslist": metricslist},
        )

    return render(request, "pages/ranges.html", {"metricslist": metricslist})


md_data = ""
md_table = ""
md_columns = ""


@csrf_exempt
def market_data(request):
    global md_data
    global md_table
    global md_columns

    if request.method == "POST":
        f_data = request.POST
        f_company = f_data.get("company")

        f_table = f_data.get("table")
        f_from = f_data.get("from")
        f_to = f_data.get("to")
        md_data = {"company": f_company, "from": f_from,
                   "to": f_to, "table": f_table}
        md_table, md_columns = market_data_func(
            f_company, f_table, f_from, f_to)

        paginator = Paginator(md_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/market_data.html",
            {"page_obj": page_object, "f_data": md_data, "columns": md_columns},
        )
    elif "page" in str(request):

        paginator = Paginator(md_table, 20)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(
            request,
            "pages/market_data.html",
            {"page_obj": page_object, "f_data": md_data, "columns": md_columns},
        )

    return render(request, "pages/market_data.html")


# screen 3
class StrategyView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    serializer_class = StrategySerializer

    def post(self, request):
        serializer = StrategySerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True",
                "strategy_data": serializer.data["strategy_details"]},
            status=status_code,
        )


class DeleteStrategyView(APIView):
    permission_classes = (IsAdminUser,)
    raise_exception=True
    serializer_class = DeleteStrategySerializer

    def post(self, request):
        serializer = DeleteStrategySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True", "message": "Strategy Deleted successfully"},
            status=status_code,
        )


class EditStrategyView(APIView):
    permission_classes = (IsAdminUser,)
    raise_exception=True
    serializer_class = EditStrategySerializer

    def post(self, request):
        serializer = EditStrategySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True",
                "edit_data": serializer.data["editstrategy_details"]},
            status=status_code,
        )


class GetStrategyView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    serializer_class = GetStrategySerializer

    def post(self, request):
        serializer = GetStrategySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "get_data": serializer.data["getstrategy_details"]
            },
            status=status_code,
        )

    def get(self, request):
        dropdown = []
        data = Strategy.objects.all()
        get_data = [{"strategy": i.strategy} for i in data]
        for i in get_data:
            get_strategy = i["strategy"]
            if get_strategy not in dropdown:
                dropdown.append(get_strategy)

        return Response(dropdown)
# Strategy Details for Context Page.
class GetScreenModelView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    serializer_class = GetScreenModelSerializer

    def post(self, request):
        serializer = GetScreenModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "get_data": serializer.data["getstrategy_details"]
            },
            status=status_code,
        )

# screen 4


class MetricView(APIView):
    serializer_class = MetricSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = MetricSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True",
                "metric_data": serializer.data["metric_details"]},
            status=status_code,
        )


class DeleteMetricView(APIView):
    serializer_class = DeleteMetricSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = DeleteMetricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True", "message": "metric Deleted successfully"},
            status=status_code,
        )


class EditMetricView(APIView):
    serializer_class = EditMetricSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = EditMetricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True",
                "edit_data": serializer.data["editmetric_details"]},
            status=status_code,
        )


class GetMetricView(APIView):

    serializer_class = GetMetricSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = GetMetricSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "get_data": serializer.data["getmetric_details"]
            },
            status=status_code,
        )

    def get(self, request):
        dropdown_metric = []
        dropdown_name = []
        data = Ranges.objects.all()
        get_data = [{"metric": i.metrics, "name": i.name} for i in data]
        for i in get_data:
            get_metric = i["metric"]
            get_name = i["name"]
            if get_metric not in dropdown_metric:
                dropdown_metric.append(get_metric)
            if get_name not in dropdown_name:
                dropdown_name.append(get_name)

        return Response(
            {"dropdown_metric": dropdown_metric, "dropdown_name": dropdown_name}
        )


# screen 5


class ModelView(APIView):
    serializer_class = ModelSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = ModelSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True",
                "model_data": serializer.data["model_details"]},
            status=status_code,
        )


class DeleteModelView(APIView):
    serializer_class = DeleteModelSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = DeleteModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True", "message": "Model Deleted Successfully"},
            status=status_code,
        )


class EditModelView(APIView):
    serializer_class = EditModelSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = EditModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK

        return Response(
            {"success": "True",
                "edit_data": serializer.data["editmodel_details"]},
            status=status_code,
        )


class GetModelView(APIView):
    serializer_class = GetModelSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = GetModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "get_data": serializer.data["getmodel_details"],
                # "page_data": serializer.data["pages_details"],
                # "current_page": serializer.data["current_page"],
            },
            status=status_code,
        )

    def get(self, request):
        dropdown_model = []
        dropdown_category = []
        data = Model.objects.all()
        get_data = [{"model": i.model, "category": i.category} for i in data]
        for i in get_data:
            get_model = i["model"]
            get_category = i["category"]
            if get_model not in dropdown_model:
                dropdown_model.append(get_model)
            if get_category not in dropdown_category:
                dropdown_category.append(get_category)

        return Response(
            {"dropdown_model": dropdown_model,
                "dropdown_category": dropdown_category}
        )


# screen 8


class GetDropView(APIView):
    serializer_class = GetDropSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def get(self, request):
        serializer = GetDropSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "measure": serializer.data["dropdown_measure"],
                "category": serializer.data["dropdown_category"],
                "operator": serializer.data["dropdown_operator"],
                "item": serializer.data["dropdown_item"],
            },
            status=status_code,
        )


class AdvanceratioView(APIView):
    serializer_class = AdvanceratioSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = AdvanceratioSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True",
                "measure_data": serializer.data["measure_details"]},
            status=status_code,
        )


class EditAdvanceratioView(APIView):
    serializer_class = EditAdvanceratioSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = EditAdvanceratioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK

        return Response(
            {
                "success": "True",
                "edit_data": serializer.data["editadvanceratio_details"],
            },
            status=status_code,
        )


class DeleteAdvanceratioView(APIView):
    serializer_class = DeleteAdvanceratioSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = DeleteAdvanceratioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True", "message": "Advanceratio Deleted successfully"},
            status=status_code,
        )


class GetadvanceratiodataView(APIView):
    serializer_class = GetAdvancedataSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = GetAdvancedataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "get_data": serializer.data["getadvanceratio_details"],
                "page_data": serializer.data["pages_details"],
                "current_page": serializer.data["current_page"],
            },
            status=status_code,
        )


# screen 6
class AggregateView(APIView):
    serializer_class = AggregatedviewSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = AggregatedviewSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "aggregate_data": serializer.data["aggregated_details"],
            },
            status=status_code,
        )


class AggregateDropView(APIView):
    serializer_class = AggregateDropSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def get(self, request):
        serializer = AggregateDropSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "dropdown_view": serializer.data["dropdown_view"],
                "dropdown_item": serializer.data["dropdown_item"],
                "dropdown_operator": serializer.data["dropdown_operator"],
            },
            status=status_code,
        )


class DeleteAggregateView(APIView):
    serializer_class = DeleteAggregateViewSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = DeleteAggregateViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True", "message": "AggregateView Deleted successfully"},
            status=status_code,
        )


class EditAggregateView(APIView):
    serializer_class = EditAggregateviewSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = EditAggregateviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "edit_data": serializer.data["editaggregateview_details"],
            },
            status=status_code,
        )


class GetAggregatedView(APIView):
    serializer_class = GetAggregatedViewSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = GetAggregatedViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "get_data": serializer.data["getaggregatedview_details"],
                "page_data": serializer.data["pages_details"],
                "current_page": serializer.data["current_page"],
            },
            status=status_code,
        )


# CONTEXT APIS
class InvestingStylesView(APIView):
    serializer_class = InvestingStyleSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True
    def post(self, request):
        serializer = InvestingStyleSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "investing_style_data": serializer.data["investing_style_data"],
            },
            status=status_code,
        )

class GetAllStylesView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        styles = []
        data = InvestingStyles.objects.all()
        get_data = [{"style": i.style} for i in data]
        for i in get_data:
            get_style = i["style"]
            if get_style not in styles:
                styles.append(get_style)

        return Response({"styleFilter": styles})


class GetMentorsListByStyleView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        mentors = []
        style = request.data.get("style", None)
        if style == None or str(style).strip() == "":
            data = InvestingStyles.objects.all()
        else:
            data = InvestingStyles.objects.filter(style=style)
        get_data = [{"mentor": i.mentor} for i in data]
        for i in get_data:
            get_mentors = i["mentor"]
            if get_mentors not in mentors:
                mentors.append(get_mentors)
        return Response({"mentorFilter": mentors})


class GetAnalysisModelsListByMentorView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        strategyNames = []
        mentor = request.data.get("mentor", None)
        if mentor == None or str(mentor).strip() == "":
            data = InvestingStyles.objects.all()
        else:
            data = InvestingStyles.objects.filter(mentor=mentor)
        get_data = [{"strategyName": i.strategy_name} for i in data]
        for i in get_data:
            get_strategyName = i["strategyName"]
            if get_strategyName not in strategyNames:
                strategyNames.append(get_strategyName)
        return Response({"strategyNameFilter": strategyNames})


class GetCategoryListByAnalysisModelView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        categories = []
        analysisModel = request.data.get("analysisModel", None)
        measureFilter = request.data.get("measureFilter", None)
        if (analysisModel != None and str(analysisModel).strip() != "" and str(analysisModel).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
            data = Model.objects.filter(model=analysisModel, measure=measureFilter)
        elif (analysisModel != None and str(analysisModel).strip() != "" and str(analysisModel).strip().lower() != "all"):
            data = Model.objects.filter(model=analysisModel)
        elif (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
            data = Model.objects.filter(measure=measureFilter)
        else:
            data = Model.objects.all()
        get_data = [{"category": i.category} for i in data]
        for i in get_data:
            get_category = i["category"]
            if get_category not in categories:
                categories.append(get_category)
        return Response({"categoryFilter": categories})


class GetMetricsListView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        metrics = []
        analysisModel = request.data.get("analysisModel", None)
        measureFilter = request.data.get("measureFilter", None)
        categoryFilter = request.data.get("categoryFilter", None)
        if (analysisModel != None and str(analysisModel).strip() != "" and str(analysisModel).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
            data = Model.objects.filter(model=analysisModel, measure=measureFilter, category=categoryFilter)
        elif (analysisModel != None and str(analysisModel).strip() != "" and str(analysisModel).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
            data = Model.objects.filter(model=analysisModel, measure=measureFilter)
        elif (analysisModel != None and str(analysisModel).strip() != "" and str(analysisModel).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
            data = Model.objects.filter(model=analysisModel, category=categoryFilter)
        elif (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
            data = Model.objects.filter(measure=measureFilter, category=categoryFilter)
        elif (analysisModel != None and str(analysisModel).strip() != "" and str(analysisModel).strip().lower() != "all"):
            data = Model.objects.filter(model=analysisModel)
        elif (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
            data = Model.objects.filter(category=categoryFilter)
        elif (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
            data = Model.objects.filter(measure=measureFilter)
        else:
            data = Model.objects.all()
        get_data = [{"metric": i.metric} for i in data]
        for i in get_data:
            get_metric = i["metric"]
            if get_metric not in metrics:
                metrics.append(get_metric)
        return Response({"metricFilter": metrics})

class GetMeasureListByAnalysisModelView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        measures = []
        analysisModel = request.data.get("analysisModel", None)
        if analysisModel == None or str(analysisModel).strip() == "":
            data = Model.objects.all()
        else:
            data = Model.objects.filter(model=analysisModel)
        get_data = [{"measure": i.measure} for i in data]
        for i in get_data:
            get_measure = i["measure"]
            if get_measure not in measures and get_measure is not None:
                measures.append(get_measure)
        return Response({"measureFilter": measures})

class GetCompanyMarketCap(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request, symbol):
        return Response(getCompanyMarketCap(symbol))

class GetCompanyStockPrice(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request, symbol):
        return Response(getCompanyStockPrice(symbol))

class GetCompaniesQuote(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request, symbols):
        return Response(getCompaniesQuote(symbols))
        
class GetScreenerCompaniesData(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        symbols = request.data.get("symbols")
        period = request.data.get("period")
        return Response(getScreenerCompaniesData(symbols, period))

class GetInvestingStylesView(APIView):
    serializer_class = GetInvestingStyleSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = GetInvestingStyleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "investing_style_data": serializer.data["investing_style_data"]
            },
            status=status_code,
        )


class DeleteInvestingStyleView(APIView):
    serializer_class = DeleteInvestingStylesViewSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = DeleteInvestingStylesViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {"success": "True", "message": "Investing Style Deleted successfully"},
            status=status_code,
        )


class EditInvestingStylesView(APIView):
    serializer_class = EditInvestingStylesviewSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True

    def post(self, request):
        serializer = EditInvestingStylesviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "edit_data": serializer.data["updated_investing_style_data"],
            },
            status=status_code,
        )


class GetContextAnalysisModelsView(APIView):
    serializer_class = GetContextAnnalysisModelsSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = GetContextAnnalysisModelsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "context_ananlysis_models_data": serializer.data["context_ananlysis_models_data"],
                # "page_data": serializer.data["pages_details"],
                # "current_page": serializer.data["current_page"],
            },
            status=status_code,
        )


class GetCompaniesByMetricsFilterView(APIView):
    serializer_class = GetCompaniesByMetricFiltersSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = GetCompaniesByMetricFiltersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "companies_data": serializer.data["companies_data"],
                "page_data": serializer.data["pages_details"],
                "current_page": serializer.data["current_page"],
            },
            status=status_code,
        )

class GetExchangesValuesView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        exchanges = Company.objects.distinct().values("exchange")
        return Response({"exchanges": exchanges})

class GetSectorByExchangeView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        exchange = request.data.get("exchange", None)
        if exchange != None and str(exchange).strip().lower() != "all":
            data = Company.objects.filter(
                exchange=exchange).distinct().values("sector")
        else:
            data = Company.objects.distinct().values("sector")
        return Response({"sectors": data})


class GetIndustryByExchangeSectorView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        exchange = request.data.get("exchange", None)
        sector = request.data.get("sector", None)
        if (exchange != None and str(exchange).strip().lower() != "all") and (sector != None and str(sector).strip().lower() != "all"):
            data = Company.objects.filter(
                exchange=exchange, sector=sector).distinct().values("industry")

        elif (exchange != None and str(exchange).strip().lower() != "all"):
            data = Company.objects.filter(
                exchange=exchange).distinct().values("industry")
        elif (sector != None and str(sector).strip().lower() != "all"):
            data = Company.objects.filter(
                sector=sector).distinct().values("industry")
        else:
            data = Company.objects.distinct().values("industry")
        return Response({"industries": data})


class GetCompanyByExchangeSectorIndustryView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        exchange = request.data.get("exchange", None)
        sector = request.data.get("sector", None)
        industry = request.data.get("industry", None)
        if (exchange != None and str(exchange).strip().lower() != "all") and (sector != None and str(sector).strip().lower() != "all") and (industry != None and str(industry).strip().lower() != "all"):
            data = Company.objects.filter(
                exchange=exchange, sector=sector, industry=industry).distinct().values("company_name", "symbol")
        elif (exchange != None and str(exchange).strip().lower() != "all") and (sector != None and str(sector).strip().lower() != "all"):
            data = Company.objects.filter(
                exchange=exchange, sector=sector).distinct().values("company_name", "symbol")

        elif (exchange != None and str(exchange).strip().lower() != "all") and (industry != None and str(industry).strip().lower() != "all"):
            data = Company.objects.filter(
                exchange=exchange, industry=industry).distinct().values("company_name", "symbol")

        elif (sector != None and str(sector).strip().lower() != "all") and (industry != None and str(industry).strip().lower() != "all"):
            data = Company.objects.filter(
                sector=sector, industry=industry).distinct().values("company_name", "symbol")

        elif (exchange != None and str(exchange).strip().lower() != "all"):
            data = Company.objects.filter(
                exchange=exchange).distinct().values("company_name", "symbol")

        elif (sector != None and str(sector).strip().lower() != "all"):
            data = Company.objects.filter(
                sector=sector).distinct().values("company_name", "symbol")

        elif (industry != None and str(industry).strip().lower() != "all"):
            data = Company.objects.filter(
                industry=industry).distinct().values("company_name", "symbol")
        else:
            data = Company.objects.distinct().values("company_name", "symbol")
        return Response({"companies": data})


class GetAllDistinctCompaniesView(APIView):
    serializer_class = GetAllDistinctCompaniesSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def get(self, request):
        serializer = GetAllDistinctCompaniesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                "companies_data": serializer.data["companies_data"],
            },
            status=status_code,
        )


class GetCompanyProfileBasedOnTable(APIView):
    serializer_class = profile_func2
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        serializer = profile_func2(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": "True",
                # "resp_data": serializer.data["resp_data"],
                "resp_data": serializer.data["resp_data"]
            },
            status=status_code,
        )

class data_analysis_process(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            types = AnalysisTools.objects.all()
            ranges = Ranges.objects.all()
            ranges = list(set([x.name for x in ranges]))
            types = list(set([i.tools.lower() for i in types]))
            types.append("CustomRatios")
            d_data = request.data
            tool = d_data.get("types")
            scat = d_data.get("sc", "")
            cat = d_data.get("cat", "")

            d_companies = d_data.get("companies")
            d_metrics = d_data.get("metrics")
            d_ranges = d_data.get("rangemetrics")
            from_ = d_data.get("from")
            to_ = d_data.get("to")
            filters = d_data.get("filters")
            date_range = list(range(int(from_), int(to_) + 1))
            date_range = [str(x) for x in date_range]
            n_years = len(date_range)
            mertricListData = MetricsList.objects.filter(metric=d_metrics[0])
            yUnit = ""
            if(len(mertricListData) > 0):
                yUnit = mertricListData[0].unit
            if ("CustomRatios" in tool):
                return_list = custom_function_latest(
                    d_metrics, tool, d_companies, date_range, d_ranges, filters, yUnit
                )
            else:
                return_list = analysis_function_latest(
                    d_metrics, scat, cat, tool, d_companies, date_range, d_ranges, filters, yUnit
                )
            return Response(
                {
                    "yUnit": yUnit,
                    "ranges_": ranges,
                    "n_years": n_years,
                    "types": types,
                    "return_list": return_list,
                    "date_range": date_range,
                    # "plot_bar": plt_bar,
                    # "plot_line": plt_line,
                    "companies": ", ".join(d_companies),
                    "tool": tool,
                    "metrics": ", ".join(d_metrics),
                    "ranges": ", ".join(d_ranges),
                    "from": from_,
                    "to": to_,
                    "sc": scat,
                    "cat": cat,
                },
            )
        except Exception as e:
            print(str(e))
        return Response({"types": types, "ranges_": ranges})

class DataAcquisitionAPIView(APIView):
    serializer_class = DataAcquisitionAPISerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True
    def post(self, request):
        serializer = DataAcquisitionAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK

        return Response(
            {
                "success": True,
            },
            status=status_code,
        )

class DataAcquisitionFileUploadView(APIView):
    parser_class = (MultiPartParser ,FormParser, )
    permission_classes = (IsAdminUser,)
    raise_exception=True
    def post(self, request, format=None, *args, **kwargs):
        t_table = request._request.POST['table']
        input_file = request._request.FILES['file']
        message_f, upload_data, upload_columns = file_upload(t_table, input_file)
        return Response(
            {
                "success": True,
                "data": request._request.POST,
                "files": str(request._request.FILES)
            }
        )

class DataAcquisitionAPITypesView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        dataTypes = DataType.objects.all()
        get_data = [{"type": i.type} for i in dataTypes]
        return Response({"dataTypes": get_data})

class DataAcquisitionAPIYearLimitsView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        limits = YearLimit.objects.all()
        get_data = [{"limit": i.limit} for i in limits]
        return Response({"yearLimits": get_data})

class DataAnalysisFinancialsView(APIView):
    serializers_class = DataAnalysisFinancialsSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer = DataAnalysisFinancialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "date_range": serializer.data["date_range"],
                "return_list": serializer.data["return_list"],
                "responseFileds": serializer.data["responseFileds"],
            },
            status=status_code,
        )

class DataAnalysisMarketDataView(APIView):
    serializers_class = DataAnalysisMarketDataSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    # pagination_class = LargeResultsSetPagination
    def post(self, request):
        serializer = DataAnalysisMarketDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["f_data"],
                "col_list": serializer.data["columns"],
            },
            status=status_code,
        )

class DataAnalysisKeyMetricsView(APIView):
    serializers_class = DataAnalysisKeyMetricsSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer = DataAnalysisKeyMetricsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["resp_data"],
            },
            status=status_code,
        )

class RangesMetricsListView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        ranges_list = Ranges.objects.all()
        metricslist = list(set([x.metrics for x in ranges_list]))
        return Response({
            "success": True,
            "resp_data": metricslist
        })

class DataAnalysisRangesView(APIView):
    serializers_class = DataAnalysisRangesSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer = DataAnalysisRangesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["resp_data"],
            },
            status=status_code,
        )

class DataAnalysisLinerRegressionView(APIView):
    serializers_class = DataAnalysisLinerRegressionSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer = DataAnalysisLinerRegressionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["table_data"],
                "regressionData": serializer.data["regressionData"],
                "company_name": serializer.data["company_name"],
            },
            status=status_code,
        )

class DataAnalysisReportedFinancialsView(APIView):
    serializers_class = DataAnalysisReportedFinancialsSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer = DataAnalysisReportedFinancialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["resp_data"],
                "columns": serializer.data["columns"]
            },
            status=status_code,
        )

class DataAnalysisFinancialNotesView(APIView):
    serializers_class = DataAnalysisFinancialNotesSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer = DataAnalysisFinancialNotesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["resp_data"],
                "columns": serializer.data["columns"]
            },
            status=status_code,
        )

class GetAvailableCountriesForRatesView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        countries = Rates.objects.distinct().values("country")
        return Response({"countries": { data['country'] : data for data in [{"country": country['country'].strip()} for country in countries]}.values()})

class GetRateTypesByCountryView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        country = request.data.get("country")
        rateTypes = Rates.objects.filter(country=country).distinct().values("rate_type")
        return Response({"rate_types": { data['rate_type'] : data for data in [{"rate_type": rateType['rate_type'].strip()} for rateType in rateTypes]}.values()})

class DataAnalysisRatesView(APIView):
    serializers_class = DataAnalysisRatesSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer =DataAnalysisRatesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["resp_data"]
            },
            status=status_code,
        )

class DPGetAdvancedRatiosView(APIView):
    serializers_class = DPGetAdvancedRatiosSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer =DPGetAdvancedRatiosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["advanced_ratios_data"]
            },
            status=status_code,
        )

class GetAllToolsView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        try:
            data = MetricsList.objects.distinct().values("tool")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetAllMetricsView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        try:
            data = MetricsList.objects.distinct().values("metric")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetAllMeasuresView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        try:
            data = MetricsList.objects.distinct().values("measure")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetAllCategoriesView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            type = request.data.get("table")
            if type == "Ratios":
                data = MetricsList.objects.filter(source="tick_app_ratios").distinct().values("category")
            else:
                data = MetricsList.objects.filter(source="tick_app_keymetrics").distinct().values("category")
            # if type == "Ratios":
            #     data = MetricsList.objects.filter(source="tick_app_ratios", tool="Ratios").distinct().values("category")
            # else:
            #     data = MetricsList.objects.filter(source="tick_app_keymetrics", tool="Metrics").distinct().values("category")
           
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetMeasuresByToolView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            tool = request.data.get("tool")
            data = MetricsList.objects.filter(tool=tool).distinct().values("measure")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetCategoryByMeasureView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            tool = request.data.get("tool", None)
            measure = request.data.get("measure", None)
            data = ""
            if(tool != None and  tool.lower() != 'all' and tool != '') and (measure != None and measure.lower() != 'all' and measure != ''):
                data = MetricsList.objects.filter(tool=tool, measure=measure).distinct().values("category")
            elif(tool != None and  tool.lower() != 'all' and tool != ''):
                data = MetricsList.objects.filter(tool=tool).distinct().values("category")
            elif(measure != None and measure.lower() != 'all' and measure != ''):
                data = MetricsList.objects.filter(measure=measure).distinct().values("category")
            else:
                data = MetricsList.objects.distinct().values("category")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetMetricByCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            tool = request.data.get("tool", None)
            measure = request.data.get("measure", None)
            category = request.data.get("category", None)
            if(tool != None and  tool.lower() != 'all' and tool != '') and (measure != None and measure.lower() != 'all' and measure != '') and (category != None and  category.lower() != 'all' and category != ''):
                data = MetricsList.objects.filter(tool=tool, measure=measure, category=category).distinct().values("metric")
            elif(tool != None and  tool.lower() != 'all' and tool != '') and (measure != None and measure.lower() != 'all' and measure != ''):
                data = MetricsList.objects.filter(tool=tool, measure=measure).distinct().values("metric")
            elif(tool != None and  tool.lower() != 'all' and tool != '') and (category != None and  category.lower() != 'all' and category != ''):
                data = MetricsList.objects.filter(tool=tool, category=category).distinct().values("metric")
            elif(measure != None and measure.lower() != 'all' and measure != '') and (category != None and  category.lower() != 'all' and category != ''):
                data = MetricsList.objects.filter(measure=measure, category=category).distinct().values("metric")
            elif(tool != None and  tool.lower() != 'all' and tool != ''):
                data = MetricsList.objects.filter(tool=tool).distinct().values("metric")
            elif(measure != None and measure.lower() != 'all' and measure != ''):
                data = MetricsList.objects.filter(measure=measure).distinct().values("metric")
            elif(category != None and category.lower() != 'all' and category != ''):
                data = MetricsList.objects.filter(category=category).distinct().values("metric")
            else:
                data = MetricsList.objects.distinct().values("metric")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetMetricsByToolView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            tool = request.data.get("tool", None)
            data = MetricsList.objects.filter(tool=tool).distinct().values("metric")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetMetricsByOnlyCategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            category = request.data.get("category", None)
            data = MetricsList.objects.filter(category=category).distinct().values("metric")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class DPGetFundamentalChartDataView(APIView):
    serializers_class = DPGetFundamentalChartDataSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        serializer = DPGetFundamentalChartDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["fundamental_chart_data"]
            },
            status=status_code,
        )

class DPCreateFundamentalChartDataView(APIView):
    serializers_class = DPCreateFundamentalChartDataSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True
    def post(self, request):
        serializer = DPCreateFundamentalChartDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["resp_details"]
            },
            status=status_code,
        )

class DPUpdateFundamentalChartDataView(APIView):
    serializers_class = DPUpdateFundamentalChartDataSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True
    def post(self, request):
        serializer = DPUpdateFundamentalChartDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True,
                "resp_data": serializer.data["resp_details"]
            },
            status=status_code,
        )

class DPDeleteFundamentalChartDataView(APIView):
    serializers_class = DPDeleteFundamentalChartDataSerializer
    permission_classes = (IsAdminUser,)
    raise_exception=True
    def post(self, request):
        serializer = DPDeleteFundamentalChartDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        return Response(
            {
                "success": True
            },
            status=status_code,
        )

class GetRangesNamesByMetricView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            metric = request.data.get("metric")
            data = Ranges.objects.filter(metrics=metric).distinct().values("name")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetExchangesByCompanyNameView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            name = request.data.get("companyName")
            data = Company.objects.filter(company_name=name).distinct().values("exchange")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetCompaniesCountries(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        try:
            data = Company.objects.distinct().values("country")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetExchangesByCountry(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            country = request.data.get("country")
            print("Countries are: ", country)
            country = country.split(",")
            print("Countries list are: ", country)
            data = Company.objects.filter(country__in=country).distinct().values("exchange")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetCityByCountryAndExchange(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            country = request.data.get("country")
            country = country.split(",")
            exchange = request.data.get("exchange")
            exchange = exchange.split(",")
            data = Company.objects.filter(country__in=country, exchange__in=exchange).distinct().values("city")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetScreenerCategories(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def get(self, request):
        try:
            data = MetricsList.objects.distinct().values("category")
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetScreenerMetricsByCategory(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            category = request.data.get("category")
            data = MetricsList.objects.filter(category=category).distinct().values("metric", "description","unit")
            for dat in data:
                ranges = Ranges.objects.filter(metrics=dat['metric']).distinct().values_list("min", "max")
                if(len(ranges)>0):
                    dat['min']=ranges[0][0]
                    dat['max']=ranges[0][1]
                    dat['range']='available'
                else:
                    dat['range']='not available'
            
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetCompaniesByFilters(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        try:
            country = request.data.get("country")
            # country = country.split(",")
            exchange = request.data.get("exchange")
            # exchange = exchange.split(",")
            city = request.data.get("city")
            # city = city.split(",")
            sector = request.data.get("sector")
            # sector = sector.split(",")
            industry = request.data.get("industry")
            # industry = industry.split(",")
            data = Company.objects.filter(country__in=country, exchange__in=exchange, city__in=city, sector__in=sector, industry__in=industry).values()
        except Exception as e:
            raise(e)
        return Response(
            {
                "success": True,
                "resp_data": data
            }
        )

class GetScreenerSectorByExchangeView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        exchange = request.data.get("exchange", None)
        exchange = exchange.split(",")
        city = request.data.get("city", None)
        city = city.split(",")
        data = ""
        if(exchange != None and  exchange.lower() != 'all' and exchange != '') and (city != None and city.lower() != 'all' and city != ''):
            data = Company.objects.filter(exchange=exchange, city=city).distinct().values("sector")
        elif(exchange != None and  exchange.lower() != 'all' and exchange != ''):
            data = Company.objects.filter(exchange=exchange).distinct().values("sector")
        elif(city != None and city.lower() != 'all' and city != ''):
            data = Company.objects.filter(city=city).distinct().values("sector")
        else:
            data = Company.objects.distinct().values("sector")
        return Response({"sectors": data})

class GetScreenerIndustryByExchangeSectorView(APIView):
    permission_classes = (IsAuthenticated,)
    raise_exception=True
    def post(self, request):
        exchange = request.data.get("exchange", None)
        exchange = exchange.split(",")
        city = request.data.get("city", None)
        city = city.split(",")
        sector = request.data.get("sector", None)
        sector = sector.split(",")
        if(exchange != None and  exchange.lower() != 'all' and exchange != '') and (city != None and city.lower() != 'all' and city != '') and (sector != None and  sector.lower() != 'all' and sector != ''):
                data = Company.objects.filter(exchange__in=exchange, city__in=city, sector__in=sector).distinct().values("industry")
        elif(exchange != None and  exchange.lower() != 'all' and exchange != '') and (city != None and city.lower() != 'all' and city != ''):
            data = Company.objects.filter(exchange__in=exchange, city__in=city).distinct().values("industry")
        elif(exchange != None and  exchange.lower() != 'all' and exchange != '') and (sector != None and  sector.lower() != 'all' and sector != ''):
            data = Company.objects.filter(exchange__in=exchange, sector__in=sector).distinct().values("industry")
        elif(city != None and city.lower() != 'all' and city != '') and (sector != None and  sector.lower() != 'all' and sector != ''):
            data = Company.objects.filter(city__in=city, sector__in=sector).distinct().values("industry")
        elif(exchange != None and  exchange.lower() != 'all' and exchange != ''):
            data = Company.objects.filter(exchange__in=exchange).distinct().values("industry")
        elif(city != None and city.lower() != 'all' and city != ''):
            data = Company.objects.filter(city__in=city).distinct().values("industry")
        elif(sector != None and sector.lower() != 'all' and sector != ''):
            data = Company.objects.filter(sector__in=sector).distinct().values("industry")
        else:
            data = Company.objects.distinct().values("industry")
        return Response({"industries": data})

class GetScreenerCompaniesByMetricsFilterView(APIView):
    serializer_class = GetScreenerCompaniesByMetricFiltersSerializer
    permission_classes = (IsAuthenticated,)
    raise_exception=True

    def post(self, request):
        print("SCREENER METRIC FILTERS VIEW TRIGGERED")
        print(request.data)
        serializer = GetScreenerCompaniesByMetricFiltersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        # print('inside view', serializer.data.get("companies_data", {}))
        return Response(
            {
                "success": "True",
                "companies_data": serializer.data["companies_data"],
                "page_data": serializer.data["pages_details"],
                "current_page": serializer.data["current_page"],
            },
            status=status_code,
        )

# class GetScreenerCompaniesPerformance(APIView):
#     serializers_class = GetScreenerCompaniesPerformanceSerializer
#     permission_classes = (IsAdminUser,)
#     raise_exception=True
#     def post(self, request):
#         serializer = GetScreenerCompaniesPerformanceSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         status_code = status.HTTP_200_OK
#         return Response(
#             {
#                 "success": True,
#                 "resp_data": serializer.data["resp_details"]
#             },
#             status=status_code,
#         )
