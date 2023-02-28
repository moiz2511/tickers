from dataclasses import fields
from unicodedata import category
from django.http import JsonResponse
from urllib import response
from django.core.exceptions import ValidationError
from numpy import trim_zeros
from .models import *
from rest_framework import serializers
from django.db import connection
from django.apps import apps
from shlex import quote
from .pyfiles.datatype import datatype_fun
from .pyfiles.financials import fin_func_latest
from .pyfiles.market_data import market_data_func_latest
from .pyfiles.keymetrics_group import keymetrics_func
from .pyfiles.analysis_latest import quote_latest
from .pyfiles.reported_financials import reportedfin_func_latest
from .pyfiles.financial_notes import financial_notes_func_latest
from .pyfiles.rate_group import rate_func_latest
import json
import math
import statistics
from operator import itemgetter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from tick_app.models import (
    AggregateCodes,
    Company,
    DataType,
    ReportedIncome,
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
    ReportedBSheet,
    ReportedCFlow,
    Rates,
    RevenueLocation,
    Ranges,
    RevenueSector,
    Pnl,
    FinBsheet,
    FinCflow,
)

global model_dict
model_dict = {
    "income-statement": Income,
    "balance-sheet-statement": BSheet,
    "cash-flow-statement": CFlow,
    "financial-growth": FinGrowth,
    "income-statement-growth": IncomeGrowth,
    "balance-sheet-statement-growth": BSheetGrowth,
    "cash-flow-statement-growth": CFlowGrowth,
    "revenue_sector": RevenueSector,
    "revenue_location": RevenueLocation,
    "reported_income": ReportedIncome,
    "reported_bsheet": ReportedBSheet,
    "reported_cflow": ReportedCFlow,
    "pnl": Pnl,
}

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = "__all__"
        # fields = ("id", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_active", "groups", "user_permissions")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser']

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
# screen 3


class StrategySerializer(serializers.Serializer):
    strategy = serializers.CharField(max_length=234, write_only=True)
    description = serializers.CharField(max_length=256, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    operator = serializers.CharField(max_length=234, write_only=True)
    range = serializers.FloatField(
        max_value=None, min_value=None, write_only=True)
    period = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    strategy_details = serializers.DictField(read_only=True)

    def validate(self, data):
        strategy = data.get("strategy", None)
        description = data.get("description", None)
        metric = data.get("metric", None)
        operator = data.get("operator", None)
        range = data.get("range", None)
        period = data.get("period", None)
        try:
            strat = Strategy.objects.create(
                strategy=strategy, description=description, metric=metric, operator=operator, range=range, period=period
            )
            strat.save()
        except:
            raise serializers.ValidationError("Strategy not created")
        strategy_data = {
            "id": strat.id,
            "strategy": strat.strategy,
            "description": strat.description,
            "metric": strat.metric,
            "operator": strat.operator,
            "range": strat.range,
            "period": strat.period
        }
        return {"strategy_details": strategy_data}


class DeleteStrategySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)

    def validate(self, data):
        id = data.get("id", None)

        try:
            if not Strategy.objects.filter(id=id).exists():
                raise serializers.ValidationError("strategy not exist")
            instance = Strategy.objects.get(id=id)
            instance.delete()

        except Strategy.DoesNotExist:
            raise serializers.ValidationError("strategy not present")
        return True


class EditStrategySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)
    strategy = serializers.CharField(max_length=234, write_only=True)
    description = serializers.CharField(max_length=256, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    operator = serializers.CharField(max_length=234, write_only=True)
    range = serializers.FloatField(
        max_value=None, min_value=None, write_only=True)
    period = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    editstrategy_details = serializers.DictField(read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        strategy = data.get("strategy", None)
        description = data.get("description", None)
        metric = data.get("metric", None)
        operator = data.get("operator", None)
        range = data.get("range", None)
        period = data.get("period", None)
        try:
            if not Strategy.objects.filter(id=id).exists():
                raise serializers.ValidationError("strategy not exist")
            data = Strategy.objects.get(id=id)
            print(type(data))
            data.strategy = strategy
            data.description = description
            data.metric = metric
            data.operator = operator
            data.range = range
            data.period = period
            data.save()
        except:
            raise serializers.ValidationError("Unable to update the strategy")
        edit_data = {
            "id": data.id,
            "strategy": data.strategy,
            "description": data.description,
            "metric": data.metric,
            "operator": data.operator,
            "range": data.range,
            "period": data.period,
        }
        return {"editstrategy_details": edit_data}


class GetStrategySerializer(serializers.Serializer):
    search_strategy = serializers.CharField(
        write_only=True, max_length=234, allow_null=True
    )
    getstrategy_details = serializers.ListField(read_only=True)

    def validate(self, data):
        strategy = data.get("search_strategy", None)
        try:
            if strategy is not None and strategy != "All":
                data = Strategy.objects.filter(strategy=strategy)

            else:
                data = Strategy.objects.all()

        except:
            raise serializers.ValidationError("strategy not present")
        get_data = [
            {
                "id": i.id,
                "strategy": i.strategy,
                "description": i.description,
                "metric": i.metric,
                "operator": i.operator,
                "range": i.range,
                "period": i.period,
            }
            for i in data
        ]
        return {
            "getstrategy_details": get_data
        }

class GetScreenModelSerializer(serializers.Serializer):
    search_strategy = serializers.CharField(
        write_only=True, max_length=234, allow_null=True
    )
    getstrategy_details = serializers.ListField(read_only=True)

    def validate(self, data):
        strategy = data.get("search_strategy", None)
        try:
            query = "SELECT tick_app_strategy.strategy,tick_app_strategy.description, tick_app_strategy.metric,tick_app_metricslist.label as 'metricLabel',tick_app_metricslist.category, tick_app_strategy.operator,tick_app_strategy.range,tick_app_strategy.period FROM tick_app_strategy inner join tick_app_ranges on tick_app_strategy.strategy = tick_app_ranges.name inner join tick_app_metricslist on tick_app_strategy.metric = tick_app_metricslist.metric whereConditionFilter group by tick_app_strategy.strategy, tick_app_strategy.metric;"
            if strategy is not None and strategy != "All":
                data = Strategy.objects.filter(strategy=strategy)
                query = query.replace("whereConditionFilter", " where tick_app_strategy.strategy='"+ strategy +"'")
            else:
                data = Strategy.objects.all()
                query = query.replace("whereConditionFilter", "")
            cursor = connection.cursor()
            cursor.execute(query)
            fields = [field_md[0] for field_md in cursor.description]
            result = [dict(zip(fields, row)) for row in cursor.fetchall()]
        except:
            raise serializers.ValidationError("Failed to fetch screen model data")
        return {
            "getstrategy_details": result
        }
# scree 4


class MetricSerializer(serializers.Serializer):
    metric = serializers.CharField(max_length=234, write_only=True)
    name = serializers.CharField(max_length=234, write_only=True)
    source = serializers.CharField(max_length=234, write_only=True)
    operator = serializers.CharField(max_length=128, write_only=True)
    min = serializers.FloatField(max_value=None, min_value=None, write_only=True)
    max = serializers.FloatField(max_value=None, min_value=None, write_only=True)
    analysis = serializers.CharField(max_length=234, write_only=True)
    metric_details = serializers.DictField(read_only=True)

    def validate(self, data):
        metric = data.get("metric", None)
        name = data.get("name", None)
        source = data.get("source", None)
        operator = data.get("operator", None)
        min = data.get("min", None)
        max = data.get("max", None)
        analysis = data.get("analysis", None)
        try:
            metric = Ranges.objects.create(
                metrics=metric,
                name=name,
                source=source,
                operator=operator,
                min=min,
                max=max,
                analysis=analysis
            )
            metric.save()
        except:
            raise serializers.ValidationError("metric not created")
        metric_data = {
            "id": metric.id,
            "metric": metric.metrics,
            "name": metric.name,
            "source": metric.source,
            "operator": metric.operator,
            "min": metric.min,
            "max": metric.max,
            "analysis": metric.analysis
        }
        return {"metric_details": metric_data}


class DeleteMetricSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)
    def validate(self, data):
        id = data.get("id", None)
        try:
            if not Ranges.objects.filter(id=id).exists():
                raise serializers.ValidationError("metric not exist")
            instance = Ranges.objects.get(id=id)
            instance.delete()
        except Strategy.DoesNotExist:
            raise serializers.ValidationError("metric not present")
        return True


class EditMetricSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    name = serializers.CharField(max_length=234, write_only=True)
    source = serializers.CharField(max_length=234, write_only=True)
    operator = serializers.CharField(max_length=128, write_only=True)
    min = serializers.FloatField(
        max_value=None, min_value=None, write_only=True)
    max = serializers.FloatField(
        max_value=None, min_value=None, write_only=True)
    analysis = serializers.CharField(max_length=234, write_only=True)
    editmetric_details = serializers.DictField(read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        new_metric = data.get("metric", None)
        new_name = data.get("name", None)
        new_source = data.get("source", None)
        new_operator = data.get("operator", None)
        new_min = data.get("min", None)
        new_max = data.get("max", None)
        new_analysis = data.get("analysis", None)

        try:
            if not Ranges.objects.filter(id=id).exists():
                raise serializers.ValidationError("metric not exist")
            data = Ranges.objects.get(id=id)
            data.metrics = new_metric
            data.name = new_name
            data.source = new_source
            data.operator = new_operator
            data.min = new_min
            data.max = new_max
            data.analysis = new_analysis
            data.save()
        except:
            raise serializers.ValidationError("Unable to update the metric")
        edit_data = {
            "id": data.id,
            "metric": data.metrics,
            "name": data.name,
            "source": data.source,
            "operator": data.operator,
            "min": data.min,
            "max": data.max,
            "analysis": data.analysis
        }
        return {"editmetric_details": edit_data}


class GetMetricSerializer(serializers.Serializer):
    search_metric = serializers.CharField(
        write_only=True, max_length=234, allow_null=True
    )
    search_name = serializers.CharField(
        write_only=True, max_length=234, allow_null=True
    )
    getmetric_details = serializers.ListField(read_only=True)

    def validate(self, data):
        metric = data.get("search_metric", None)
        name = data.get("search_name", None)
        try:
            if metric == "All" and name == "All":
                data = Ranges.objects.all()
            elif metric == "All" and name != None:
                data = Ranges.objects.filter(name=name)
            elif metric != None and name == "All":
                data = Ranges.objects.filter(metrics=metric)
            # elif metric or name == 'All':
            elif metric != None and name != None:
                data = Ranges.objects.filter(metrics=metric, name=name)
            else:
                data = Ranges.objects.all()
        except:
            raise serializers.ValidationError("metric not present")
        get_data = [
            {
                "id": i.id,
                "metric": i.metrics,
                "name": i.name,
                "source": i.source,
                "operator": i.operator,
                "min": i.min,
                "max": i.max,
                "analysis": i.analysis
            }
            for i in data
        ]
        return {
            "getmetric_details": get_data
        }


# screen 5


class ModelSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=234, write_only=True)
    category = serializers.CharField(max_length=234, write_only=True)
    question = serializers.CharField(max_length=234, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    tool = serializers.CharField(max_length=234, write_only=True)
    range = serializers.CharField(max_length=234, write_only=True)
    model_from = serializers.CharField(max_length=234, write_only=True)
    model_to = serializers.CharField(max_length=234, write_only=True)
    measure = serializers.CharField(max_length=234, write_only=True)
    model_details = serializers.DictField(read_only=True)

    def validate(self, data):
        model = data.get("model", None)
        category = data.get("category", None)
        question = data.get("question", None)
        metric = data.get("metric", None)
        tool = data.get("tool", None)
        range = data.get("range", None)
        model_from = data.get("model_from", None)
        model_to = data.get("model_to", None)
        measure = data.get("measure", None)
        try:
            model = Model.objects.create(
                model=model,
                category=category,
                question=question,
                metric=metric,
                tool=tool,
                range=range,
                model_from=model_from,
                model_to=model_to,
                measure=measure,
            )
            model.save()
        except:
            raise serializers.ValidationError("model not created")
        model_data = {
            "id": model.id,
            "model": model.model,
            "category": model.category,
            "question": model.question,
            "metric": model.metric,
            "tool": model.tool,
            "range": model.range,
            "model_from": model.model_from,
            "model_to": model.model_to,
            "measure": model.measure,
        }
        return {"model_details": model_data}


class DeleteModelSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)

    def validate(self, data):
        id = data.get("id", None)

        try:
            if not Model.objects.filter(id=id).exists():
                raise serializers.ValidationError("model not present")
            instance = Model.objects.get(id=id)
            instance.delete()
        except:
            raise serializers.ValidationError("Unable to delete the model")
        return True


class EditModelSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)
    model = serializers.CharField(max_length=234, write_only=True)
    category = serializers.CharField(max_length=234, write_only=True)
    question = serializers.CharField(max_length=234, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    tool = serializers.CharField(max_length=234, write_only=True)
    range = serializers.CharField(max_length=234, write_only=True)
    model_from = serializers.CharField(max_length=234, write_only=True)
    model_to = serializers.CharField(max_length=234, write_only=True)
    measure = serializers.CharField(max_length=234, write_only=True)
    editmodel_details = serializers.DictField(read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        new_model = data.get("model", None)
        new_category = data.get("category", None)
        new_question = data.get("question", None)
        new_metric = data.get("metric", None)
        new_tool = data.get("tool", None)
        new_range = data.get("range", None)
        new_model_from = data.get("model_from", None)
        new_model_to = data.get("model_to", None)
        measure = data.get("measure", None)

        try:
            if not Model.objects.filter(id=id).exists():
                raise serializers.ValidationError("Model not exist")
            data = Model.objects.get(id=id)
            data.model = new_model
            data.category = new_category
            data.question = new_question
            data.metric = new_metric
            data.tool = new_tool
            data.range = new_range
            data.model_from = new_model_from
            data.model_to = new_model_to
            data.measure = measure
            data.save()
        except:
            raise serializers.ValidationError("Unable to update the model")
        edit_data = {
            "id": data.id,
            "model": data.model,
            "category": data.category,
            "question": data.question,
            "metric": data.metric,
            "tool": data.tool,
            "range": data.range,
            "model_from": data.model_from,
            "model_to": data.model_to,
            "measure": data.measure,
        }
        return {"editmodel_details": edit_data}


class GetModelSerializer(serializers.Serializer):
    model = serializers.CharField(
        write_only=True, max_length=234, allow_null=True
    )
    category = serializers.CharField(
        write_only=True, max_length=234, allow_null=True
    )
    # page = serializers.IntegerField(
    #     max_value=None, min_value=None, write_only=True)
    getmodel_details = serializers.ListField(read_only=True)
    # pages_details = serializers.IntegerField(read_only=True)
    # current_page = serializers.IntegerField(read_only=True)

    def validate(self, data):
        model = data.get("model", None)
        category = data.get("category", None)
        # current_page = data.get("page", None)

        try:
            # n = 15
            # pagno = data.get("page", None)
            # start = (int(pagno) - 1) * n
            # end = start + n

            if model == "All" and category == "All":
                data = Model.objects.all()

            elif model == "All" and category != None:
                data = Model.objects.filter(category=category)

            elif model != None and category == "All":
                data = Model.objects.filter(model=model)

            # elif metric or name == 'All':
            elif model != None and category != None:
                data = Model.objects.filter(model=model, category=category)

            else:
                data = Model.objects.all()
        except:
            raise serializers.ValidationError("model not present")
        # page = len(data) // n
        # rem = len(data) % n
        # if rem > 0:
        #     pages = int(page) + 1
        # else:
        #     pages = int(page)

        get_data = [
            {
                "id": i.id,
                "model": i.model,
                "category": i.category,
                "question": i.question,
                "metric": i.metric,
                "tool": i.tool,
                "range": i.range,
                "model_from": i.model_from,
                "model_to": i.model_to,
                "measure": i.measure,
            }
            for i in data
        ]
        return {
            "getmodel_details": get_data,
            # "pages_details": pages,
            # "current_page": current_page,
        }


# screen 8


class GetDropSerializer(serializers.Serializer):
    dropdown_measure = serializers.ListField(read_only=True)
    dropdown_category = serializers.ListField(read_only=True)
    dropdown_operator = serializers.ListField(read_only=True)
    dropdown_item = serializers.ListField(read_only=True)

    def validate(self, request):

        dropdown_measure = []
        dropdown_category = []
        dropdown_operator = ["Plus", "minus", "multiply", "divide", "modulo"]
        dropdown_item = []
        data = CustomMetrics.objects.all()
        get_data = [
            {"measure": i.measure, "category": i.category, "metric": i.metrics}
            for i in data
        ]
        for i in get_data:
            get_measure = i["measure"]
            get_category = i["category"]
            get_metric = i["metric"]
            if get_measure not in dropdown_measure:
                dropdown_measure.append(get_measure)
            if get_category not in dropdown_category:
                dropdown_category.append(get_category)
            if get_metric not in dropdown_item:
                dropdown_item.append(get_metric)
        return {
            "dropdown_measure": dropdown_measure,
            "dropdown_category": dropdown_category,
            "dropdown_operator": dropdown_operator,
            "dropdown_item": dropdown_item,
        }


class AdvanceratioSerializer(serializers.Serializer):
    measure = serializers.CharField(max_length=234, write_only=True)
    category = serializers.CharField(max_length=234, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    item1 = serializers.CharField(max_length=234, write_only=True)
    operator1 = serializers.CharField(max_length=234, write_only=True)
    item2 = serializers.CharField(max_length=234, write_only=True)
    operator2 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    item3 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    operator3 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    item4 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    operator4 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    item5 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    measure_details = serializers.DictField(read_only=True)

    def validate(self, data):
        measure = data.get("measure", None)
        category = data.get("category", None)
        metric = data.get("metric", None)
        item1 = data.get("item1", None)
        operator1 = data.get("operator1", None)
        item2 = data.get("item2", None)
        operator2 = data.get("operator2", None)
        item3 = data.get("item3", None)
        operator3 = data.get("operator3", None)
        item4 = data.get("item4", None)
        operator4 = data.get("operator4", None)
        item5 = data.get("item5", None)

        try:
            measure = Advancedratio.objects.create(
                measure=measure,
                category=category,
                metric=metric,
                item1=item1,
                operator1=operator1,
                item2=item2,
                operator2=operator2,
                item3=item3,
                operator3=operator3,
                item4=item4,
                operator4=operator4,
                item5=item5,
            )
            measure.save()
        except:
            raise serializers.ValidationError("Advanceratio not created")
        measure_data = {
            "id": measure.id,
            "measure": measure.measure,
            "category": measure.category,
            "metric": measure.metric,
            "item1": measure.item1,
            "operator1": measure.operator1,
            "item2": measure.item2,
            "operator2": measure.operator2,
            "item3": measure.item3,
            "operator3": measure.operator3,
            "item4": measure.item4,
            "operator4": measure.operator4,
            "item5": measure.item5,
        }
        return {"measure_details": measure_data}


class EditAdvanceratioSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)
    measure = serializers.CharField(max_length=234, write_only=True)
    category = serializers.CharField(max_length=234, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    item1 = serializers.CharField(max_length=234, write_only=True)
    operator1 = serializers.CharField(max_length=234, write_only=True)
    item2 = serializers.CharField(max_length=234, write_only=True)
    operator2 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    item3 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    operator3 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    item4 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    operator4 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    item5 = serializers.CharField(max_length=234, write_only=True, allow_blank=True)
    editadvanceratio_details = serializers.DictField(read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        measure = data.get("measure", None)
        category = data.get("category", None)
        metric = data.get("metric", None)
        item1 = data.get("item1", None)
        operator1 = data.get("operator1", None)
        item2 = data.get("item2", None)
        operator2 = data.get("operator2", None)
        item3 = data.get("item3", None)
        operator3 = data.get("operator3", None)
        item4 = data.get("item4", None)
        operator4 = data.get("operator4", None)
        item5 = data.get("item5", None)

        try:
            if not Advancedratio.objects.filter(id=id).exists():
                raise serializers.ValidationError("advanceratio not present ")

            data = Advancedratio.objects.get(id=id)
            data.measure = measure
            data.category = category
            data.metric = metric
            data.item1 = item1
            data.operator1 = operator1
            data.item2 = item2
            data.operator2 = operator2
            data.item3 = item3
            data.operator3 = operator3
            data.item4 = item4
            data.operator4 = operator4
            data.item5 = item5
            data.save()

        except:
            raise serializers.ValidationError(
                "Unable to update the Advanceratio")
        edit_data = {
            "id": data.id,
            "measure": data.measure,
            "category": data.category,
            "metric": data.metric,
            "item1": data.item1,
            "operator1": data.operator1,
            "item2": data.item2,
            "operator2": data.operator2,
            "item3": data.item3,
            "operator3": data.operator3,
            "item4": data.item4,
            "operator4": data.operator4,
            "item5": data.item5,
        }
        return {"editadvanceratio_details": edit_data}


class DeleteAdvanceratioSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)

    def validate(self, data):
        id = data.get("id", None)

        try:
            if not Advancedratio.objects.filter(id=id).exists():
                raise serializers.ValidationError("advanceratio not present")
            instance = Advancedratio.objects.get(id=id)
            instance.delete()
        except:
            raise serializers.ValidationError(
                "Unable to delete the Advanceratio")
        return True


class GetAdvancedataSerializer(serializers.Serializer):
    page = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    getadvanceratio_details = serializers.ListField(read_only=True)
    pages_details = serializers.IntegerField(read_only=True)
    current_page = serializers.IntegerField(read_only=True)

    def validate(self, data):
        current_page = data.get("page", None)
        try:
            n = 15
            pagno = data.get("page", None)
            start = (int(pagno) - 1) * n
            end = start + n
            data = Advancedratio.objects.all()
            get_data = [
                {
                    "id": i.id,
                    "measure": i.measure,
                    "category": i.category,
                    "metric": i.metric,
                    "code": i.code,
                    "item1": i.item1,
                    "operator1": i.operator1,
                    "item2": i.item2,
                    "operator2": i.operator2,
                    "item3": i.item3,
                    "operator3": i.operator3,
                    "item4": i.item4,
                    "operator4": i.operator4,
                    "item5": i.item5,
                }
                for i in data
            ]
        except:
            raise serializers.ValidationError("unable to get the advanceratio")

        page = len(data) // n
        rem = len(data) % n
        if rem > 0:
            pages = int(page) + 1
        else:
            pages = int(page)

        return {
            "getadvanceratio_details": get_data[start:end],
            "pages_details": pages,
            "current_page": current_page,
        }


# screen 6


class AggregatedviewSerializer(serializers.Serializer):
    view = serializers.CharField(max_length=234, write_only=True)
    name = serializers.CharField(max_length=234, write_only=True)
    item1 = serializers.CharField(max_length=234, write_only=True)
    operator1 = serializers.CharField(max_length=234, write_only=True)
    item2 = serializers.CharField(max_length=234, write_only=True)
    operator2 = serializers.CharField(max_length=234, write_only=True)
    item3 = serializers.CharField(max_length=234, write_only=True)
    operator3 = serializers.CharField(max_length=234, write_only=True)
    item4 = serializers.CharField(max_length=234, write_only=True)
    operator4 = serializers.CharField(max_length=234, write_only=True)
    item5 = serializers.CharField(max_length=234, write_only=True)
    aggregated_details = serializers.DictField(read_only=True)

    def validate(self, data):
        view = data.get("view", None)
        name = data.get("name", None)
        item1 = data.get("item1", None)
        operator1 = data.get("operator1", None)
        item2 = data.get("item2", None)
        operator2 = data.get("operator2", None)
        item3 = data.get("item3", None)
        operator3 = data.get("operator3", None)
        item4 = data.get("item4", None)
        operator4 = data.get("operator4", None)
        item5 = data.get("item5", None)

        try:
            aggregate = AggregatedView.objects.create(
                view=view,
                name=name,
                item1=item1,
                operator1=operator1,
                item2=item2,
                operator2=operator2,
                item3=item3,
                operator3=operator3,
                item4=item4,
                operator4=operator4,
                item5=item5,
            )
            aggregate.save()

            model_select = model_dict[view]

            value1 = 0
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            item1_data = model_select.objects.filter(post_id=name).filter(
                aggregate_code=item1
            )

            for data_item in item1_data:
                value1 += data_item.value2
                print(value1)

            if item2 != None and operator1 != None:
                item2_data = model_select.objects.filter(post_id=name).filter(
                    aggregate_code=item2
                )
                for data_item in item2_data:
                    value2 += data_item.value2
                print("OPERATOR111", value2)
                calculated_value1 = calcuate(operator1, value1, value2)
                print(calculated_value1)

            if item3 != None and operator2 != None:
                item2_data = model_select.objects.filter(post_id=name).filter(
                    aggregate_code=item3
                )
                print(item2_data)
                for data_item in item2_data:
                    value3 += data_item.value2

                calculated_value2 = calcuate(
                    operator2, calculated_value1, value3)
                print(calculated_value2)

            if item4 != None and operator3 != None:
                item2_data = model_select.objects.filter(post_id=name).filter(
                    aggregate_code=item4
                )
                for data_item in item2_data:
                    value4 += data_item.value2

                calculated_value3 = calcuate(
                    operator3, calculated_value2, value4)
                print(calculated_value3)

            if item5 != None and operator4 != None:
                item2_data = model_select.objects.filter(post_id=name).filter(
                    aggregate_code=item5
                )
                for data_item in item2_data:
                    value5 += data_item.value2

                calculated_value4 = calcuate(
                    operator4, calculated_value3, value5)
                print(calculated_value4)

            # a = [ m._meta.db_table for c in apps.get_app_configs() for m in c.get_models() ]
            # tables_name = []
            # with connection.cursor() as cursor:
            #     data = cursor.execute("SHOW tables")
            #     for table in [tables[0] for tables in cursor.fetchall()]:
            #         tables_name.append(table)
            #     data = cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'u423088965_invelp_test'")
            # print('TABLESNAME',tables_name)
            # new_view = "tick_app_"+view
            # if new_view not in tables_name:
            #     with connection.cursor() as cursor:
            #         cursor.execute("CREATE TABLE {0} (revenue DECIMAL(5,2),operatingExpenses DECIMAL(5,2),ebidta DECIMAL(5,2),depreciationAndAmortization VARCHAR(255),ebidt DECIMAL(5,2),interestIncome DECIMAL(5,2),interestExpense DECIMAL(5,2),ebt DECIMAL(5,2),nonRecurring VARCHAR(255),taxes DECIMAL(5,2),effectiveTaxRate DECIMAL(5,2),nopat DECIMAL(5,2),netIncome DECIMAL(5,2))".format("tick_app_"+view))
            # else:
            #     print(new_view)
            #     with connection.cursor() as cursor:
            #         cursor.execute
        except:
            raise serializers.ValidationError("Aggregated view not created")
        aggregate_data = {
            "id": aggregate.id,
            "view": aggregate.view,
            "name": aggregate.name,
            "item1": aggregate.item1,
            "operator1": aggregate.operator1,
            "item2": aggregate.item2,
            "operator2": aggregate.operator2,
            "item3": aggregate.item3,
            "operator3": aggregate.operator3,
            "item4": aggregate.item4,
            "operator4": aggregate.operator4,
            "item5": aggregate.item5,
        }
        return {"aggregated_details": aggregate_data}


class AggregateDropSerializer(serializers.Serializer):
    dropdown_view = serializers.ListField(read_only=True)
    dropdown_operator = serializers.ListField(read_only=True)
    dropdown_item = serializers.ListField(read_only=True)

    def validate(self, request):

        dropdown_view = []
        dropdown_operator = ["Plus", "minus", "multiply", "divide", "modulo"]
        dropdown_item = []
        data = AggregateCodes.objects.all()
        get_data = [{"item": i.aggregate_code} for i in data]
        for i in get_data:
            get_item = i["item"]
            if get_item not in dropdown_item:
                dropdown_item.append(get_item)

        # data1 = CustomRatios.objects.all()
        # get_data1 = [{'view':i.measure} for i in data1]
        # for i in get_data1:
        #     get_view = i['view']
        #     if get_view not in dropdown_view:
        #         dropdown_view.append(get_view)
        # dropdown_view.remove("")
        # dropdown_view.remove(None)
        for x, y in model_dict.items():
            dropdown_view.append(x)

        return {
            "dropdown_view": dropdown_view,
            "dropdown_item": dropdown_item,
            "dropdown_operator": dropdown_operator,
        }


class DeleteAggregateViewSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)

    def validate(self, data):
        id = data.get("id", None)

        try:
            if not AggregatedView.objects.filter(id=id).exists():
                raise serializers.ValidationError("AggregatedView not present")
            instance = AggregatedView.objects.get(id=id)
            instance.delete()
        except:
            raise serializers.ValidationError(
                "Unable to delete the AggregatedView")
        return True


class EditAggregateviewSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)
    new_view = serializers.CharField(max_length=234, write_only=True)
    new_name = serializers.CharField(max_length=234, write_only=True)
    editaggregateview_details = serializers.DictField(read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        new_view = data.get("new_view", None)
        new_name = data.get("new_name", None)

        try:
            if not AggregatedView.objects.filter(id=id).exists():
                raise serializers.ValidationError(
                    "AggregatedView not present ")

            data = AggregatedView.objects.get(id=id)
            data.view = new_view
            data.name = new_name
            data.save()

        except:
            raise serializers.ValidationError(
                "Unable to update the AggregatedView")
        edit_data = {
            "id": data.id,
            "view": data.view,
            "name": data.name,
            "item1": data.item1,
            "operator1": data.operator1,
            "item2": data.item2,
            "operator2": data.operator2,
            "item3": data.item3,
            "operator3": data.operator3,
            "item4": data.item4,
            "operator4": data.operator4,
            "item5": data.item5,
        }
        return {"editaggregateview_details": edit_data}


class GetAggregatedViewSerializer(serializers.Serializer):
    page = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    getaggregatedview_details = serializers.ListField(read_only=True)
    pages_details = serializers.IntegerField(read_only=True)
    current_page = serializers.IntegerField(read_only=True)

    def validate(self, data):
        try:
            current_page = data.get("page", None)
            n = 15
            pagno = data.get("page", None)
            start = (int(pagno) - 1) * n
            end = start + n
            data = AggregatedView.objects.all()

            get_data = [
                {
                    "id": i.id,
                    "view": i.view,
                    "name": i.name,
                    "item1": i.item1,
                    "operator1": i.operator1,
                    "item2": i.item2,
                    "operator2": i.operator2,
                    "item3": i.item3,
                    "operator3": i.operator3,
                    "item4": i.item4,
                    "operator4": i.operator4,
                    "item5": i.item5,
                }
                for i in data
            ]
        except:
            raise serializers.ValidationError(
                "unable to get the AggregatedView")

        page = len(data) // n
        rem = len(data) % n
        if rem > 0:
            pages = int(page) + 1
        else:
            pages = int(page)

        return {
            "getaggregatedview_details": get_data[start:end],
            "pages_details": pages,
            "current_page": current_page,
        }


def calcuate(operator, value1, value2):
    if operator == "plus":
        total_value = value1 + value2
    elif operator == "minus":
        total_value = value1 - value2
    elif operator == "multiply":
        total_value = value1 * value2
    elif operator == "divide":
        total_value = value1 / value2
    else:
        total_value = value1 % value2
    return total_value


# CONTEXT INVESTING STYLE APIS

class InvestingStyleSerializer(serializers.Serializer):
    style = serializers.CharField(write_only=True)
    mentor = serializers.CharField(write_only=True)
    strategy_name = serializers.CharField(write_only=True)
    source = serializers.CharField(write_only=True)
    philosophy = serializers.CharField(write_only=True)
    riskTolerance = serializers.CharField(write_only=True)
    periodRange = serializers.CharField(write_only=True)
    fundReturn = serializers.CharField(write_only=True)
    marketReturn = serializers.CharField(write_only=True)
    investing_style_data = serializers.ListField(read_only=True)

    def validate(self, data):
        style = data.get("style", None)
        mentor = data.get("mentor", None)
        strategy_name = data.get("strategy_name", None)
        source = data.get("source", None)
        philosophy = data.get("philosophy", None)
        riskTolerance = data.get("riskTolerance", None)
        periodRange = data.get("periodRange", None)
        fundReturn = data.get("fundReturn", None)
        marketReturn = data.get("marketReturn", None)
        try:
            investingStyle = InvestingStyles.objects.create(
                style=style,
                mentor=mentor,
                strategy_name=strategy_name,
                source=source,
                philosophy=philosophy,
                riskTolerance=riskTolerance,
                periodRange=periodRange,
                fundReturn=fundReturn,
                marketReturn=marketReturn
            )
            print(investingStyle)
        except:
            raise serializers.ValidationError(
                "Error on creating investing style")
        return {"investing_style_data": "Investing Style Created Successfully"}


class GetInvestingStyleSerializer(serializers.Serializer):
    style = serializers.CharField(
        write_only=True, max_length=128, allow_null=True)
    mentor = serializers.CharField(
        write_only=True, max_length=128, allow_null=True)
    investing_style_data = serializers.ListField(read_only=True)

    def validate(self, data):
        style_filter = data.get("style", None)
        mentor_filter = data.get("mentor", None)
        try:
            if ((style_filter != None and style_filter != "All") and (mentor_filter != None and mentor_filter != "All")):
                data = InvestingStyles.objects.filter(
                    mentor=mentor_filter, style=style_filter)
            elif style_filter != None and style_filter != "All":
                data = InvestingStyles.objects.filter(style=style_filter)
            elif mentor_filter != "All" and mentor_filter != None:
                data = InvestingStyles.objects.filter(mentor=mentor_filter)
            else:
                data = InvestingStyles.objects.all()
            get_data = [
                {
                    "id": i.id,
                    "style": i.style,
                    "mentor": i.mentor,
                    "strategy_name": i.strategy_name,
                    "source": i.source,
                    "philosophy": i.philosophy,
                    "riskTolerance": i.riskTolerance,
                    "periodRange": i.periodRange,
                    "fundReturn": i.fundReturn,
                    "marketReturn": i.marketReturn
                }
                for i in data
            ]
        except:
            raise serializers.ValidationError(
                "unable to get the Investing Style Data")
        return {
            "investing_style_data": get_data
        }


class EditInvestingStylesviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(write_only=True)
    style = serializers.CharField(write_only=True)
    mentor = serializers.CharField(write_only=True)
    strategy_name = serializers.CharField(write_only=True)
    source = serializers.CharField(write_only=True)
    philosophy = serializers.CharField(write_only=True)
    riskTolerance = serializers.CharField(write_only=True)
    periodRange = serializers.CharField(write_only=True)
    fundReturn = serializers.CharField(write_only=True)
    marketReturn = serializers.CharField(write_only=True)
    updated_investing_style_data = serializers.DictField(read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        style = data.get("style", None)
        mentor = data.get("mentor", None)
        strategy_name = data.get("strategy_name", None)
        source = data.get("source", None)
        philosophy = data.get("philosophy", None)
        riskTolerance = data.get("riskTolerance", None)
        periodRange = data.get("periodRange", None)
        fundReturn = data.get("fundReturn", None)
        marketReturn = data.get("marketReturn", None)
        try:
            if not InvestingStyles.objects.filter(id=id).exists():
                raise serializers.ValidationError(
                    "Invalid INvesting Styles Input Data")
            print("Geeting Id Data")
            data = InvestingStyles.objects.get(id=id)
            print("Id is valid")
            data.style = style
            data.mentor = mentor
            data.strategy_name = strategy_name
            data.source = source
            data.philosophy = philosophy
            data.riskTolerance = riskTolerance
            data.periodRange = periodRange
            data.fundReturn = fundReturn
            data.marketReturn = marketReturn
            print(data)
            data.save()

        except:
            raise serializers.ValidationError(
                "Unable to update the Investing Style Data")
        response_data = {
            "id": data.id,
            "style": data.style,
            "mentor": data.mentor,
            "strategy_name": data.strategy_name,
            "source": data.source,
            "philosophy": data.philosophy,
            "riskTolerance": data.riskTolerance,
            "periodRange": data.periodRange,
            "fundReturn": data.fundReturn,
            "marketReturn": data.marketReturn
        }
        return {"updated_investing_style_data": response_data}


class DeleteInvestingStylesViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(write_only=True)

    def validate(self, data):
        id = data.get("id", None)

        try:
            if not InvestingStyles.objects.filter(id=id).exists():
                raise serializers.ValidationError(
                    "Investing Style not present")
            instance = InvestingStyles.objects.get(id=id)
            instance.delete()
        except:
            raise serializers.ValidationError(
                "Unable to delete the Investing Style")
        return True


class GetContextAnnalysisModelsSerializer(serializers.Serializer):
    # page = serializers.IntegerField(
    #     max_value=None, min_value=None, write_only=True)
    analysisModel = serializers.CharField(
        write_only=True, max_length=128, allow_null=True)
    category = serializers.CharField(
        write_only=True, max_length=128, allow_null=True)
    measure = serializers.CharField(
        write_only=True, max_length=128, allow_null=True)
    metric = serializers.CharField(
        write_only=True, max_length=128, allow_null=True)
    context_ananlysis_models_data = serializers.ListField(read_only=True)
    # pages_details = serializers.IntegerField(read_only=True)
    # current_page = serializers.IntegerField(read_only=True)

    def validate(self, data):
        analysisModel_filter = data.get("analysisModel", None)
        category_filter = data.get("category", None)
        measure_filter = data.get("measure", None)
        metric_filter = data.get("metric", None)
        # current_page = data.get("page", None)
        query = "select * from tick_app_model"
        isAndCondition = False
        try:
            query = "select * from tick_app_model"
            # pagno = data.get("page", None)
            # n = 15
            # start = (int(pagno) - 1) * n
            # end = start + n

            if analysisModel_filter != None and analysisModel_filter.lower() != "all" and analysisModel_filter.strip() != "":
                value = quote(analysisModel_filter)
                if value.startswith("'") or value.endswith("'"):
                    query = query + " where model=%s" % value
                else:
                    query = query + " where model='%s'" % value
                isAndCondition = True

            if category_filter != None and category_filter.lower() != "all" and category_filter.strip() != "":
                if isAndCondition:
                    query = query + " and "
                else:
                    query = query + " where "
                    isAndCondition = True
                value = quote(category_filter)
                if value.startswith("'") or value.endswith("'"):
                    query = query + "category=%s" % value
                else:
                    query = query + "category='%s'" % value

            if measure_filter != None and measure_filter.lower() != "all" and measure_filter.strip() != "":
                if isAndCondition:
                    query = query + " and "
                else:
                    query = query + " where "
                    isAndCondition = True
                value = quote(measure_filter)
                if value.startswith("'") or value.endswith("'"):
                    query = query + "measure=%s" % value
                else:
                    query = query + "measure='%s'" % value

            if metric_filter != None and metric_filter.lower() != "all" and metric_filter.strip() != "":
                if isAndCondition:
                    query = query + " and "
                else:
                    query = query + " where "
                value = quote(metric_filter)
                if value.startswith("'") or value.endswith("'"):
                    query = query + "metric=%s" % value
                else:
                    query = query + "metric='%s'" % value
            data = Model.objects.raw(query)
            get_data = [
                {
                    "id": i.id,
                    "model": i.model,
                    "category": i.category,
                    "question": i.question,
                    "metric": i.metric,
                    "tool": i.tool,
                    "range": i.range,
                    "model_from": i.model_from,
                    "model_to": i.model_to,
                    "display": i.display,
                    "measure": i.measure
                }
                for i in data
            ]
        except Exception as inst:
            print(inst)
            raise serializers.ValidationError(
                "unable to get the Investing Style Data")
        return {
            "context_ananlysis_models_data": get_data,
            # "pages_details": int(math.ceil(len(get_data)/n)),
            # "current_page": current_page,
        }

class GetCompaniesByMetricFiltersSerializer(serializers.Serializer):
    # data = serializers.
    page = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    filters = serializers.ListField(write_only=True)
    # operator = serializers.CharField(
    #     write_only=True, max_length=128, allow_null=True)
    # range = serializers.CharField(
    #     write_only=True, max_length=128, allow_null=True)
    companies_data = serializers.ListField(read_only=True)
    pages_details = serializers.IntegerField(read_only=True)
    current_page = serializers.IntegerField(read_only=True)

    def validate(self, data):
        customMetricsList = []
        yearPeriod = data.get("filters")[0]['period']
        res = list(map(itemgetter('metric'), data.get("filters")))
        query = "SELECT * FROM tick_app_metricslist WHERE metric in " + str(tuple(res)).replace(",)", ")")
        cursor = connection.cursor()
        cursor.execute(query)
        fields = [field_md[0] for field_md in cursor.description]
        result = [dict(zip(fields, row)) for row in cursor.fetchall()]
        resultDict = {}
        internalWhereCondition = ""
        avgMetricFilters = ""
        metricTableDict = {}
        advCondition = ""
        # advMetricsCount = 0
        advMetricTable = {}
        advMetricsList = []
        newQuery = """SELECT * FROM (SELECT A.symbol, A.company_name, A.exchange, A.sector, A.industry, A.country,
           avgMetricFilters FROM tick_app_company as A """
        for metricData in result:
            metric = metricData['metric']
            dataSource = metricData['source']
            dataTool = metricData['tool']
            if dataSource is not None and dataTool.lower() == "customratios":
                # advMetricsCount += 1
                customMetricsList.append(metric)
                nonEmptyItems = tuple()
                counter = 3
                advMetricDataResp = Advancedratio.objects.filter(metric=metric)
                advMetricData = advMetricDataResp[0]
                if (advMetricData.item1 is not None and advMetricData.item1 != "") and (advMetricData.operator1 is not None and advMetricData.operator1 != "") and (advMetricData.item2 is not None and advMetricData.item2 != ""):
                    advCondition += ", round(((((item1Table." + metric + advMetricData.item1 + self.getOperatorSymbol(advMetricData.operator1) + "item2Table." + metric + advMetricData.item2 + ")"
                    nonEmptyItems += (advMetricData.item1, advMetricData.item2,)
                    advMetricTable['item1Table' + metric] = advMetricData.item1
                    advMetricTable['item2Table' + metric] = advMetricData.item2
                if (advMetricData.item3 is not None and advMetricData.item3 != "") and (advMetricData.operator2 is not None and advMetricData.operator2 != ""):
                    advCondition += self.getOperatorSymbol(advMetricData.operator2) + "item3Table." + metric + advMetricData.item3 + ")"
                    nonEmptyItems += (advMetricData.item3,)
                    advMetricTable['item3Table' + metric] = advMetricData.item3
                    counter -= 1
                if (advMetricData.item4 is not None and advMetricData.item4 != "") and (advMetricData.operator3 is not None and advMetricData.operator3 != ""):
                    advCondition += self.getOperatorSymbol(advMetricData.operator3) + "item4Table." + metric + advMetricData.item4 + ")"
                    nonEmptyItems += (advMetricData.item4,)
                    advMetricTable['item4Table' + metric] = advMetricData.item4
                    counter -= 1
                if (advMetricData.item5 is not None and advMetricData.item5 != "") and (advMetricData.operator4 is not None and advMetricData.operator4 != ""):
                    advCondition += self.getOperatorSymbol(advMetricData.operator4) + "item5Table." + metric + advMetricData.item5 + ")"
                    nonEmptyItems += (advMetricData.item5,)
                    advMetricTable['item5Table' + metric] = advMetricData.item5
                    counter -= 1
                if(advCondition.strip() != ""):
                    while counter > 0:
                        advCondition +=")"
                        counter -= 1
                    advCondition += ", 2) as " + metric
                query = "SELECT * FROM tick_app_metricslist WHERE metric in " + str(nonEmptyItems)
                cursor = connection.cursor()
                cursor.execute(query)
                fields = [field_md[0] for field_md in cursor.description]
                AdvMetricResult = [dict(zip(fields, row)) for row in cursor.fetchall()]
                for advMetric in AdvMetricResult:
                    advDataSource =  advMetric['source']
                    if advDataSource in resultDict.keys():
                        resultDict[advDataSource] = resultDict[advDataSource] + ""
                        metricTableDict[advMetric['metric']] = advDataSource
                    else:
                        metricTableDict[advMetric['metric']] = advDataSource
                        resultDict[advDataSource] = " inner join " + advDataSource + " as " + advDataSource + " on A.symbol=" + advDataSource + ".symbol "
                        internalWhereCondition += " and year("+ advDataSource + ".date) >= year(sysdate() - interval '" + str(yearPeriod) +"' year)"
                # advMetricsList = list(advMetricTable.values())
                continue
            if dataSource in resultDict.keys():
                resultDict[dataSource] = resultDict[dataSource] + ""
                metricTableDict[metricData['metric']] = dataSource
            else:
                metricTableDict[metricData['metric']] = dataSource
                resultDict[dataSource] = " inner join " + dataSource + " as " + dataSource + " on A.symbol=" + dataSource + ".symbol "
                internalWhereCondition += " and year("+ dataSource + ".date) >= year(sysdate() - interval '" + str(yearPeriod) +"' year)"
        for metricTab in resultDict.values():
            newQuery += metricTab
        newQuery += " where " + internalWhereCondition.strip(" ").lstrip("and") + " group by A.company_name) as results where metricWhereCondition;"
        whereMetricsCondition = ""
        

        # if(len(advMetricsList) > 1):
        #     advWhereCondition = ""
        #     yearMetricTableList = []
        #     previousMetricCond = ""
        #     count = 1
        #     for advMetric in advMetricsList:
        #         if advMetric not in yearMetricTableList:
        #             if count < 3:
        #                 advWhereCondition += "year(" + metricTableDict[advMetric] + ".date) = "
        #             else:
        #                 advWhereCondition = advWhereCondition.rstrip().rstrip("=")
        #                 advWhereCondition += previousMetricCond + "year(" + metricTableDict[advMetric] + ".date)"
        #             if count == 1:
        #                 previousMetricCond = " and year(" + metricTableDict[advMetric] + ".date) = "
        #             yearMetricTableList.append(advMetric)
        #             count += 1
        #     whereMetricsCondition = advWhereCondition.rstrip().rstrip("=")

        current_page = data.get("page", None)
        n = 15
        try:
            for object in data.get("filters"):
                metric_filter = str(object.get("metric", None))
                operator_filter = object.get("operator", None)
                range_filter = object.get("range", None)
                if metric_filter not in customMetricsList:
                    avgMetricFilters += "avg(" + \
                        metricTableDict[metric_filter] + "." + metric_filter+") as " + metric_filter + ","
                if(str(operator_filter).strip().lower() == "greaterthan"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " > " + \
                        "'" + str(range_filter) + "'"
                elif(str(operator_filter).strip().lower() == "lessthan"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " < " + \
                        "'" + str(range_filter) + "'"
                elif(str(operator_filter).strip().lower() == "greaterthanorequal"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " >= " + \
                        "'" + str(range_filter) + "'"
                elif(str(operator_filter).strip().lower() == "lessthanorequal"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " <= " + \
                        "'" + str(range_filter) + "'"
            newQuery = newQuery.replace("metricWhereCondition", whereMetricsCondition.strip().lstrip("and"))
            if(advCondition is not None and advCondition.strip() != ""):
                newQuery = newQuery.replace("avgMetricFilters", avgMetricFilters + advCondition.lstrip(","))
            else:
                newQuery = newQuery.replace("avgMetricFilters", avgMetricFilters.rstrip(","))
            for cusMetric in customMetricsList:
                if('item1Table.' + cusMetric in newQuery):
                    newQuery = newQuery.replace("item1Table." + cusMetric, metricTableDict[advMetricTable['item1Table' + cusMetric]] + ".")
                if('item2Table.' in newQuery):
                    newQuery = newQuery.replace("item2Table." + cusMetric, metricTableDict[advMetricTable['item2Table' + cusMetric]] + ".")
                if('item3Table.' in newQuery):
                    newQuery = newQuery.replace("item3Table." + cusMetric, metricTableDict[advMetricTable['item3Table' + cusMetric]] + ".")
                if('item4Table.' in newQuery):
                    newQuery = newQuery.replace("item4Table." + cusMetric, metricTableDict[advMetricTable['item4Table' + cusMetric]] + ".")
                if('item5Table.' in newQuery):
                    newQuery = newQuery.replace("item5Table." + cusMetric, metricTableDict[advMetricTable['item5Table' + cusMetric]] + ".")
            cursor = connection.cursor()
            print("######## QUERY BEING EXECUTED #######")
            print(newQuery)
            print("######################################")
            cursor.execute(newQuery)
            fields = [field_md[0] for field_md in cursor.description]
            result = [dict(zip(fields, row)) for row in cursor.fetchall()]
        except Exception as inst:
            print(inst)
            raise serializers.ValidationError(
                "Error on Getting Companies by metrics")
        # print(data)
        return {
            "companies_data": result,
            "pages_details": int(math.ceil(len(result)/n)),
            "current_page": current_page,
        }
    def getOperatorSymbol(self, operatorName):
        operatorName = operatorName.lower()
        if(operatorName == "plus"):
            return "+"
        elif(operatorName == "minus"):
            return "-"
        elif(operatorName == "dividedby"):
            return "/"
        elif(operatorName == "multipliedby"):
            return "*"
        return ""


class GetAllDistinctCompaniesSerializer(serializers.Serializer):

    companies_data = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            data = Company.objects.distinct().values("company_name")
        except:
            raise serializers.ValidationError(
                "Unable to fetch companies")
        return {
            "companies_data": data,
        }

class DataAcquisitionAPISerializer(serializers.Serializer):
    type = serializers.CharField(
        write_only=True, max_length=128, allow_null=True)
    years = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    companies = serializers.ListField(write_only=True)
    def validate(self, data):
        try:
            p_year = data.get("years", None)
            p_dtype = data.get("type")
            companies = data.get("companies", None)
            print("#### COMPAINES IN VIEWS #####")
            print(companies)
            resp = datatype_fun(companies, p_dtype, p_year)
            print(resp)
            print("Retruned result")
        except:
            raise serializers.ValidationError(
                "Data Acquisition Failed")
        return {
            "success": True,
        }

class DataAnalysisFinancialsSerializer(serializers.Serializer):
    company = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    exchange = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    table = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    display = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    period = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    quarter = serializers.ListField(write_only=True, max_length=128, allow_null=True)
    from_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    to_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    date_range = serializers.ListField(read_only=True)
    return_list = serializers.ListField(read_only=True)
    responseFileds = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            company = data.get("company", None)
            exchange = data.get("exchange", None)
            table = data.get("table", None)
            display = data.get("display", None)
            period = data.get("period", None)
            quarter = data.get("quarter", None)
            from_year = data.get("from_year")
            to_year = data.get("to_year", None)
            fin_table, range_date, responseFileds = fin_func_latest(company, table, display, period, quarter, from_year, to_year, exchange)
        except:
            raise serializers.ValidationError(
                "Data Ananlysis Financials Failed")
        return {
            "success": True,
            "date_range": range_date,
            "return_list": fin_table,
            "responseFileds": responseFileds
        }

class DataAnalysisMarketDataSerializer(serializers.Serializer):
    company = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    exchange = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    table = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    from_date = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    to_date = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    date_range = serializers.ListField(read_only=True)
    f_data = serializers.ListField(read_only=True)
    columns = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            company = data.get("company", None)
            exchange = data.get("exchange", None)
            table = data.get("table", None)
            from_date = data.get("from_date")
            to_date = data.get("to_date", None)
            object_list, md_columns = market_data_func_latest(company, exchange, table, from_date, to_date)
        except:
            raise serializers.ValidationError(
                "Data Ananlysis MarketData Failed")
        return {
            "success": True,
            "f_data": object_list,
            "columns": md_columns,
        }


class DataAnalysisKeyMetricsSerializer(serializers.Serializer):
    company = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    exchange = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    table = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    category = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    frequency = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    quarter = serializers.ListField(write_only=True, max_length=128, allow_null=True)
    fromYear = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    toYear = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    resp_data = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            f_company = data.get("company")
            f_exchange = data.get("exchange")
            f_table = data.get("table")
            category = data.get("category")
            frequency = data.get("frequency")
            quarter = data.get("quarter")
            fromYear = data.get("fromYear")
            toYear = data.get("toYear")
            resp_data = data.get("resp_data")
            k_table = keymetrics_func(f_company, f_exchange, f_table, category, frequency, quarter, fromYear, toYear)
            print('>>>>>><<<<<<<<<<<<<')
            print(k_table[0]['metricsUnit'])
        except serializers.ValidationError as e :
            print(e)
            raise serializers.ValidationError(
                "Data Ananlysis KeyMetrics Failed")
        return {
            "success": True,
            "resp_data": k_table,
        }

class DataAnalysisRangesSerializer(serializers.Serializer):
    metric = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    resp_data = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            metric = data.get("metric")
            data = Ranges.objects.filter(metrics=metric)
            get_data = [
                {
                    "metrics": i.metrics,
                    "name": i.name,
                    "source": i.source,
                    "operator": i.operator,
                    "min": i.min,
                    "max": i.max,
                    "analysis": i.analysis,
                }
                for i in data
            ]
        except:
            raise serializers.ValidationError(
                "Data Ananlysis Ratios Failed")
        return {
            "success": True,
            "resp_data": get_data,
        }

class DataAnalysisLinerRegressionSerializer(serializers.Serializer):
    company = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    from_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    to_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    # date_range = serializers.ListField(read_only=True)
    regressionData = serializers.ListField(read_only=True)
    table_data = serializers.ListField(read_only=True)
    company_name = serializers.CharField(read_only=True)
    def validate(self, data):
        try:
            company = data.get("company", None)
            from_year = data.get("from_year", None)
            to_year = data.get("to_year", None)
            p_symbol = Company.objects.filter(company_name__istartswith=company)
            p_symbol = p_symbol[0].symbol
            table_df, regressionData = quote_latest(p_symbol, company, from_year, to_year)
            list_close = [float(x) for x in list(table_df["close"])]
            len_close = len(list(table_df["close"]))
            mean_ = sum(list_close) / len_close
            sd_ = statistics.stdev(list_close)
            rsd_ = sd_ / mean_
            sdt = 2 * sd_
            rsdt = 2 * rsd_
            tabledf = [{
                "mean": round(mean_, 2),
                "sd": round(sd_, 2),
                "rsd": round(rsd_*100, 2),
                "2sd": round(sdt, 2),
                "2rsd": round(rsdt*100, 2),
            }]
        except:
           raise serializers.ValidationError("Data Analysis LinerRegression Falied")
        return {
            "success": True,
            "company_name": company,
            "table_data": tabledf,
            "regressionData": regressionData
        }

class DataAnalysisReportedFinancialsSerializer(serializers.Serializer):
    company = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    table = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    regressionData = serializers.ListField(read_only=True)
    resp_data = serializers.ListField(read_only=True)
    columns = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            company = data.get("company", None)
            table = data.get("table", None)
            year = data.get("year", None)
            rf_table, rf_columns = reportedfin_func_latest(company, table, year)
        except:
           raise serializers.ValidationError("Data Analysis ReportedFinancials Falied")
        return {
            "success": True,
            "resp_data": rf_table,
            "columns": rf_columns
        }

class DataAnalysisFinancialNotesSerializer(serializers.Serializer):
    company = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    table = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    from_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    to_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    regressionData = serializers.ListField(read_only=True)
    resp_data = serializers.ListField(read_only=True)
    columns = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            company = data.get("company", None)
            table = data.get("table", None)
            from_year = data.get("from_year", None)
            to_year = data.get("to_year", None)
            fn_table, fn_columns = financial_notes_func_latest(company, table, from_year, to_year)
        except:
           raise serializers.ValidationError("Data Analysis FinancialNotes Falied")
        return {
            "success": True,
            "resp_data": fn_table,
            "columns": fn_columns
        }


class DataAnalysisRatesSerializer(serializers.Serializer):
    country = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    rateType = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    from_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    to_year = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    resp_data = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            country = data.get("country", None)
            rateType = data.get("rateType", None)
            from_year = data.get("from_year", None)
            to_year = data.get("to_year", None)
            response = rate_func_latest(country, rateType, from_year, to_year)
            get_data = [
                {
                    "country": i.country,
                    "year": i.year,
                    "rate": i.rate,
                    "rate_type": i.rate_type
                }
                for i in response
            ]
        except:
           raise serializers.ValidationError("Data Analysis FinancialNotes Falied")
        return {
            "success": True,
            "resp_data": get_data
        }

class DPGetAdvancedRatiosSerializer(serializers.Serializer):
    measure = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    category = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    metric = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    advanced_ratios_data = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            measureFilter = data.get("measure", None)
            categoryFilter = data.get("category", None)
            metricFilter = data.get("metric", None)
            if (metricFilter != None and str(metricFilter).strip() != "" and str(metricFilter).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = Advancedratio.objects.filter(metric=metricFilter, measure=measureFilter, category=categoryFilter)
            elif (metricFilter != None and str(metricFilter).strip() != "" and str(metricFilter).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
                data = Advancedratio.objects.filter(metric=metricFilter, measure=measureFilter)
            elif (metricFilter != None and str(metricFilter).strip() != "" and str(metricFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = Advancedratio.objects.filter(metric=metricFilter, category=categoryFilter)
            elif (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = Advancedratio.objects.filter(measure=measureFilter, category=categoryFilter)
            elif (metricFilter != None and str(metricFilter).strip() != "" and str(metricFilter).strip().lower() != "all"):
                data = Advancedratio.objects.filter(metric=metricFilter)
            elif (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = Advancedratio.objects.filter(category=categoryFilter)
            elif (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
                data = Advancedratio.objects.filter(measure=measureFilter)
            else:
                data = Advancedratio.objects.all()
            get_data = [
                {
                    "id": i.id,
                    "measure": i.measure,
                    "category": i.category,
                    "metric": i.metric,
                    "code": i.code,
                    "item1": i.item1,
                    "operator1": i.operator1,
                    "item2": i.item2,
                    "operator2": i.operator2,
                    "item3": i.item3,
                    "operator3": i.operator3,
                    "item4": i.item4,
                    "operator4": i.operator4,
                    "item5": i.item5,
                }
                for i in data
            ]
        except:
            raise serializers.ValidationError("unable to get the advanceratio")

        return {
            "advanced_ratios_data": get_data,
        }

class DPGetFundamentalChartDataSerializer(serializers.Serializer):
    measure = serializers.CharField(write_only=True, max_length=512, allow_null=True)
    category = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    tool = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    metric = serializers.CharField(write_only=True, max_length=128, allow_null=True)
    fundamental_chart_data = serializers.ListField(read_only=True)
    def validate(self, data):
        try:
            measureFilter = data.get("measure", None)
            categoryFilter = data.get("category", None)
            metricFilter = data.get("metric", None)
            toolFilter = data.get("tool", None)
            if (toolFilter != None and str(toolFilter).strip() != "" and str(toolFilter).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all") and (metricFilter != None and str(metricFilter).strip() != "" and str(metricFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(tool=toolFilter, measure=measureFilter, category=categoryFilter, metric=metricFilter)
            elif (toolFilter != None and str(toolFilter).strip() != "" and str(toolFilter).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(tool=toolFilter, measure=measureFilter, category=categoryFilter)
            elif (toolFilter != None and str(toolFilter).strip() != "" and str(toolFilter).strip().lower() != "all") and (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(tool=toolFilter, measure=measureFilter)
            elif (toolFilter != None and str(toolFilter).strip() != "" and str(toolFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(tool=toolFilter, category=categoryFilter)
            elif (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all") and (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(measure=measureFilter, category=categoryFilter)
            elif (toolFilter != None and str(toolFilter).strip() != "" and str(toolFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(tool=toolFilter)
            elif (categoryFilter != None and str(categoryFilter).strip() != "" and str(categoryFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(category=categoryFilter)
            elif (measureFilter != None and str(measureFilter).strip() != "" and str(measureFilter).strip().lower() != "all"):
                data = MetricsList.objects.filter(measure=measureFilter)
            else:
                data = MetricsList.objects.all()
            get_data = [
                {
                    "id": i.id,
                    "metric": i.metric,
                    "source": i.source,
                    "tool": i.tool,
                    "measure": i.measure,
                    "category": i.category,
                }
                for i in data
            ]
        except:
            raise serializers.ValidationError("unable to get the Fundemantal Chart Data")

        return {
            "fundamental_chart_data": get_data,
        }

class DPCreateFundamentalChartDataSerializer(serializers.Serializer):
    metric = serializers.CharField(max_length=234, write_only=True)
    source = serializers.CharField(max_length=234, write_only=True)
    tool = serializers.CharField(max_length=234, write_only=True)
    measure = serializers.CharField(max_length=234, write_only=True)
    category = serializers.CharField(max_length=234, write_only=True)
    resp_details = serializers.CharField(read_only=True)

    def validate(self, data):
        metric = data.get("metric", None)
        source = data.get("source", None)
        tool = data.get("tool", None)
        measure = data.get("measure", None)
        category = data.get("category", None)
        try:
            MetricsList.objects.create(
                metric=metric, 
                source=source, 
                tool=tool, 
                measure=measure,
                category=category,
            )
        except Exception as e:
            print(e)
            raise serializers.ValidationError("FundamentaChart Data not created")
        return {"resp_details": "Fundamental Chart Data Created Successfully!"}

class DPDeleteFundamentalChartDataSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)

    def validate(self, data):
        id = data.get("id", None)
        try:
            if not MetricsList.objects.filter(id=id).exists():
                raise serializers.ValidationError("MetricList Data not exist")
            instance = MetricsList.objects.get(id=id)
            instance.delete()
        except MetricsList.DoesNotExist:
            raise serializers.ValidationError("MetricList Data not present")
        return True


class DPUpdateFundamentalChartDataSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=None, write_only=True)
    metric = serializers.CharField(max_length=234, write_only=True)
    source = serializers.CharField(max_length=234, write_only=True)
    tool = serializers.CharField(max_length=234, write_only=True)
    measure = serializers.CharField(max_length=234, write_only=True)
    category = serializers.CharField(max_length=234, write_only=True)
    resp_details = serializers.ListField(read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        metric = data.get("metric", None)
        source = data.get("source", None)
        tool = data.get("tool", None)
        measure = data.get("measure", None)
        category = data.get("category", None)
        try:
            if not MetricsList.objects.filter(id=id).exists():
                raise serializers.ValidationError("MetricList not exist")
            data = MetricsList.objects.get(id=id)
            data.metric = metric
            data.source = source
            data.tool = tool
            data.measure = measure
            data.category = category
            data.save()
        except:
            raise serializers.ValidationError("Unable to update the MetricList")
        edit_data = {
            "id": data.id,
            "metric": data.metric,
            "source": data.source,
            "tool": data.tool,
            "measure": data.measure,
            "category": data.category,
        }
        return {"resp_details": edit_data}

class GetScreenerCompaniesByMetricFiltersSerializer(serializers.Serializer):
    # data = serializers.
    page = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    filters = serializers.ListField(write_only=True)
    companies = serializers.ListField(write_only=True)
    period = serializers.IntegerField(
        max_value=None, min_value=None, write_only=True)
    # operator = serializers.CharField(
    #     write_only=True, max_length=128, allow_null=True)
    # range = serializers.CharField(
    #     write_only=True, max_length=128, allow_null=True)
    companies_data = serializers.ListField(read_only=True)
    companies_all_data = serializers.ListField(read_only=True)
    pages_details = serializers.IntegerField(read_only=True)
    current_page = serializers.IntegerField(read_only=True)
    
    def validate(self, data):
        print("SCREENER METRIC FILTERS SERIALIZER TRIGGERED")
        customMetricsList = []
        yearPeriod = data.get("period")
        res = list(map(itemgetter('metric'), data.get("filters")))
        companies = data.get("companies")
        print("Company data to be retrieved", companies)
        query = "SELECT * FROM tick_app_metricslist WHERE metric in " + str(tuple(res)).replace(",)", ")")
        print("Metrics list Query", query)
        cursor = connection.cursor()
        cursor.execute(query)
        fields = [field_md[0] for field_md in cursor.description]
        result = [dict(zip(fields, row)) for row in cursor.fetchall()]
        print('printing first result')
        print(result)
        # resultDict = {}
        # internalWhereCondition = {}
        # avgMetricFilters = {}
        # metricTableDict = {}
        # advCondition = ""
        # # advMetricsCount = 0
        # advMetricTable = {}
        # advMetricsList = []
        
        # newResult={}

        # for metricData in result:
        #     metric = metricData['metric']
        #     dataSource = metricData['source']
        #     if dataSource in resultDict.keys():
        #         resultDict[dataSource] = resultDict[dataSource] + ""
        #         metricTableDict[metric] = dataSource
        #         # internalWhereCondition[metric] = " where year("+ dataSource + ".date) >= year(sysdate() - interval '" + str(yearPeriod) +"' year)"

        #     else:
        #         metricTableDict[metric] = dataSource
        #         resultDict[metric] = "inner join " + dataSource + " as " + dataSource + " on A.symbol=" + dataSource + ".symbol "
        #         internalWhereCondition[metric] = "where year("+ dataSource + ".date) >= year(sysdate() - interval '" + str(yearPeriod) +"' year)"
        
        # print("Result -----------#############  New")
        # # print(newQuery)
        # print(metricTableDict)
        # print(resultDict)
        # print(internalWhereCondition)
        # current_page = data.get("page", None)
        # n = 15
        # whereMetricsConditionDict = {}
        # for object in data.get("filters"):
        #     metric_filter = str(object.get("metric", None))
        #     whereMetricsCondition = ""

        #     operator_filter = object.get("operator", None)
        #     range_filter = object.get("value", None)
        #     if metric_filter not in customMetricsList:
        #         avgMetricFilters[metric_filter]= "avg(" + \
        #             metricTableDict[metric_filter] + "." + metric_filter+") as " + metric_filter + ","
        #     if(str(operator_filter).strip().lower() == "greaterthan"):
        #         whereMetricsCondition += " and " + \
        #             metric_filter + " > " + \
        #             "'" + str(range_filter) + "'"
        #     elif(str(operator_filter).strip().lower() == "lessthan"):
        #         whereMetricsCondition += " and " + \
        #             metric_filter + " < " + \
        #             "'" + str(range_filter) + "'"
        #     elif(str(operator_filter).strip().lower() == "greaterthanorequal"):
        #         whereMetricsCondition += " and " + \
        #             metric_filter + " >= " + \
        #             "'" + str(range_filter) + "'"
        #     elif(str(operator_filter).strip().lower() == "lessthanorequal"):
        #         whereMetricsCondition += " and " + \
        #             metric_filter + " <= " + \
        #             "'" + str(range_filter) + "'"
        #     print(whereMetricsCondition)
        #     whereMetricsConditionDict[metric_filter] = whereMetricsCondition
        # print(whereMetricsConditionDict)
        # for metric in whereMetricsConditionDict.keys():
        #     whereMetricsConditionDict[metric]= whereMetricsConditionDict[metric].strip().lstrip("and") + " and company_name in ("+ ', '.join(['"{}"'.format(value) for value in companies]) +")"

        # print("Printing metric",metricTableDict)
        
        categorized_data = {}
        for item in result:
            category = item['category']
            if category not in categorized_data:
                categorized_data[category] = []
            categorized_data[category].append(item)

        print("vategorized",categorized_data)
        newResult={}
        for category in categorized_data:
            print(category)
            resultDict = {}
            internalWhereCondition = ""
            avgMetricFilters = ""
            metricTableDict = {}
            advCondition = ""
            # advMetricsCount = 0
            advMetricTable = {}
            advMetricsList = []
            
            newQuery = """SELECT * FROM (SELECT A.symbol, A.company_name, A.exchange, A.sector, A.industry, A.country,
           avgMetricFilters FROM tick_app_company as A """
            for metricData in categorized_data[category]:
                # print(result)
                metric = metricData['metric']
                dataSource = metricData['source']
                if dataSource in resultDict.keys():
                    resultDict[dataSource] = resultDict[dataSource] + ""
                    metricTableDict[metric] = dataSource
                else:
                    metricTableDict[metric] = dataSource
                    resultDict[dataSource] = " inner join " + dataSource + " as " + dataSource + " on A.symbol=" + dataSource + ".symbol "
                    internalWhereCondition += " and year("+ dataSource + ".date) >= year(sysdate() - interval '" + str(yearPeriod) +"' year)"
            for metricTab in resultDict.values():
                newQuery += metricTab
            newQuery += " where " + internalWhereCondition.strip(" ").lstrip("and") + " group by A.company_name) as results where metricWhereCondition;"
            whereMetricsCondition = ""
            current_page = data.get("page", None)
            n = 15
            try:
                for object in data.get("filters"):
                    print('onject',object)
                    print(categorized_data[category])
                    if str(object.get("category", None))==category:
                        metric_filter = str(object.get("metric", None))
                        operator_filter = object.get("operator", None)
                        range_filter = object.get("value", None)
                        if metric_filter not in customMetricsList:
                            avgMetricFilters += "avg(" + \
                                metricTableDict[metric_filter] + "." + metric_filter+") as " + metric_filter + ","
                            if(str(operator_filter).strip().lower() == "greaterthan"):
                                whereMetricsCondition += " and " + \
                                    metric_filter + " > " + \
                                    "'" + str(range_filter) + "'"
                            elif(str(operator_filter).strip().lower() == "lessthan"):
                                whereMetricsCondition += " and " + \
                                    metric_filter + " < " + \
                                    "'" + str(range_filter) + "'"
                            elif(str(operator_filter).strip().lower() == "greaterthanorequal"):
                                whereMetricsCondition += " and " + \
                                    metric_filter + " >= " + \
                                    "'" + str(range_filter) + "'"
                            elif(str(operator_filter).strip().lower() == "lessthanorequal"):
                                whereMetricsCondition += " and " + \
                                    metric_filter + " <= " + \
                                    "'" + str(range_filter) + "'"
                        else:
                            print("else not")
                whereMetricsCondition = whereMetricsCondition.strip().lstrip("and") + " and company_name in ("+ ', '.join(['"{}"'.format(value) for value in companies]) +")"
                newQuery = newQuery.replace("metricWhereCondition", whereMetricsCondition.strip().lstrip("and"))
                if(advCondition is not None and advCondition.strip() != ""):
                    newQuery = newQuery.replace("avgMetricFilters", avgMetricFilters + advCondition.lstrip(","))
                else:
                    newQuery = newQuery.replace("avgMetricFilters", avgMetricFilters.rstrip(","))
                print("######## Inside Query BEING EXECUTED #######")
                print(category)
                print(newQuery)
                print("######################################")
                cursor = connection.cursor()
                cursor.execute(newQuery)
                fields = [field_md[0] for field_md in cursor.description]
                newResult[category] = [dict(zip(fields, row)) for row in cursor.fetchall()]
                        # print("######second quert result")
                    
                    
            except Exception as inst:
                print(inst)
                raise serializers.ValidationError(
                    "Error on Getting Companies by metrics")

        newResult_json = JsonResponse(newResult)
        
        
        resultDict = {}
        internalWhereCondition = ""
        avgMetricFilters = ""
        metricTableDict = {}
        advCondition = ""
        # advMetricsCount = 0
        advMetricTable = {}
        advMetricsList = []
        newQuery = """SELECT * FROM (SELECT A.symbol, A.company_name, A.exchange, A.sector, A.industry, A.country,
           avgMetricFilters FROM tick_app_company as A """
        for metricData in result:
            metric = metricData['metric']
            dataSource = metricData['source']
            if dataSource in resultDict.keys():
                resultDict[dataSource] = resultDict[dataSource] + ""
                metricTableDict[metric] = dataSource
            else:
                metricTableDict[metric] = dataSource
                resultDict[dataSource] = " inner join " + dataSource + " as " + dataSource + " on A.symbol=" + dataSource + ".symbol "
                internalWhereCondition += " and year("+ dataSource + ".date) >= year(sysdate() - interval '" + str(yearPeriod) +"' year)"
        for metricTab in resultDict.values():
            newQuery += metricTab
        newQuery += " where " + internalWhereCondition.strip(" ").lstrip("and") + " group by A.company_name) as results where metricWhereCondition;"
        whereMetricsCondition = ""
        current_page = data.get("page", None)
        n = 15
        try:
            for object in data.get("filters"):
                metric_filter = str(object.get("metric", None))
                operator_filter = object.get("operator", None)
                range_filter = object.get("value", None)
                if metric_filter not in customMetricsList:
                    avgMetricFilters += "avg(" + \
                        metricTableDict[metric_filter] + "." + metric_filter+") as " + metric_filter + ","
                if(str(operator_filter).strip().lower() == "greaterthan"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " > " + \
                        "'" + str(range_filter) + "'"
                elif(str(operator_filter).strip().lower() == "lessthan"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " < " + \
                        "'" + str(range_filter) + "'"
                elif(str(operator_filter).strip().lower() == "greaterthanorequal"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " >= " + \
                        "'" + str(range_filter) + "'"
                elif(str(operator_filter).strip().lower() == "lessthanorequal"):
                    whereMetricsCondition += " and " + \
                        metric_filter + " <= " + \
                        "'" + str(range_filter) + "'"
            whereMetricsCondition = whereMetricsCondition.strip().lstrip("and") + " and company_name in ("+ ', '.join(['"{}"'.format(value) for value in companies]) +")"
            newQuery = newQuery.replace("metricWhereCondition", whereMetricsCondition.strip().lstrip("and"))
            if(advCondition is not None and advCondition.strip() != ""):
                newQuery = newQuery.replace("avgMetricFilters", avgMetricFilters + advCondition.lstrip(","))
            else:
                newQuery = newQuery.replace("avgMetricFilters", avgMetricFilters.rstrip(","))
            print("######## QUERY BEING EXECUTED #######")
            print(newQuery)
            print("######################################")
            cursor = connection.cursor()
            cursor.execute(newQuery)
            fields = [field_md[0] for field_md in cursor.description]
            result = [dict(zip(fields, row)) for row in cursor.fetchall()]
        except Exception as inst:
            print(inst)
            raise serializers.ValidationError(
                "Error on Getting Companies by metrics  again")
        
        # newResult_again = JsonResponse(result)
        print(newResult)
        # print(newResult)
        return {
            "companies_data": newResult_json,
            "companies_all_data": result,
            "pages_details": int(math.ceil(len(result)/n)),
            "current_page": current_page,
        }

# class GetScreenerCompaniesPerformanceSerializer(serializers.Serializer):
#     companies = serializers.CharField(write_only=True, max_length=512, allow_null=True)
#     resp_data = serializers.ListField(read_only=True)
#     def validate(self, data):
#         try:
#             companies = data.get("country", None)
#             response = rate_func_latest(country, rateType, from_year, to_year)
#             get_data = [
#                 {
#                     "country": i.country,
#                     "year": i.year,
#                     "rate": i.rate,
#                     "rate_type": i.rate_type
#                 }
#                 for i in response
#             ]
#         except:
#            raise serializers.ValidationError("Data Analysis FinancialNotes Falied")
#         return {
#             "success": True,
#             "resp_data": get_data
#         }
