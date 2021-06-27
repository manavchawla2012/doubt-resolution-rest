from typing import List

from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta

from cn_rest.utils import dict_to_json
from doubt.choices import DoubtStateChoices
from doubt.models import DoubtsModel, DoubtQnAModel
from doubt.serializers import DoubtQnASerializer, RaiseDoubtSerializer


class RaiseDoubtLCView(ListCreateAPIView):
    serializer_class = RaiseDoubtSerializer
    queryset = DoubtsModel.objects.order_by("-created_on")


class RaiseDoubtRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = RaiseDoubtSerializer
    queryset = DoubtsModel.objects
    lookup_field = "id"


class DoubtQnALCView(ListCreateAPIView):
    serializer_class = DoubtQnASerializer
    queryset = DoubtQnAModel.objects.order_by("-created_on")

    def get_queryset(self):
        query_params = self.request.query_params
        if "doubt" in query_params:
            self.queryset = self.queryset.filter(doubt=query_params["doubt"])
        return self.queryset


class DashboardView(APIView):

    def convert_ta_item(self, data):
        data["avg_time_taken"] = 0
        if data["doubts_solved"] > 0:
            data["avg_time_taken"] = int(data["total_time_taken"]/(60*data["doubts_solved"]))
        return data

    def get(self, *args, **kwargs):
        report = {
            "doubts_solved": 0,
            "doubts_asked": 0,
            "doubts_escalated": 0,
            "avg_doubt_resolution_time": 0,
            "ta_report": {}
        }
        all_doubts: List[DoubtsModel] = DoubtsModel.objects.all()
        time_taken_to_solve_doubts = timedelta(seconds=0)
        for doubt in all_doubts:
            ta = doubt.ta
            ta_id = ""
            if ta:
                ta_id = str(ta.id)
                if ta_id not in report["ta_report"]:
                    report["ta_report"][ta_id] = {
                        "doubts_accepted": 0,
                        "doubts_solved": 0,
                        "doubts_escalated": 0,
                        "total_time_taken": 0,
                        "username": ta.username,
                        "id": ta_id
                    }
            if ta:
                report["ta_report"][ta_id]["doubts_accepted"] += 1
            report["doubts_asked"] += 1
            if doubt.state == DoubtStateChoices.SOLVED:
                report["doubts_solved"] += 1
                time_diff = (doubt.resolved_on - doubt.picked_on)
                time_taken_to_solve_doubts += time_diff
                if ta:
                    report["ta_report"][ta_id]["doubts_solved"] += 1
                    report["ta_report"][ta_id]["total_time_taken"] += time_diff.total_seconds()
            elif doubt.state == DoubtStateChoices.ESCALATED:
                report["doubts_escalated"] += 1
                if ta:
                    report["ta_report"][ta_id]["doubts_escalated"] += 1
        avg_time_taken = 0
        if report["doubts_solved"] > 0:
            avg_time_taken = int(time_taken_to_solve_doubts.total_seconds() / (60 * report["doubts_solved"]))
        report["avg_doubt_resolution_time"] = int(avg_time_taken)
        new_ta_report = list(map(self.convert_ta_item, report["ta_report"].values()))
        report["ta_report"] = new_ta_report
        return Response(dict_to_json(report))
