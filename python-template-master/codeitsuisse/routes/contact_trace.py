import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def contact_trace():
    data = request.get_json();
    def compareString(String1, String2):
        # return number of alteration and isNonSalient point
        # String1->String2,,,,, String1 is infected by String 2
        totalIteration = 0
        Salientiteration = 0
        for i in range(len(String1)):
            if String1[i] != String2[i]:
                totalIteration += 1
                if i % 4 == 0:
                    Salientiteration += 1
        return totalIteration, Salientiteration > 1

    InfectedWithOrigin = compareString(data.get("infected").get("genome"), data.get("origin").get("genome"))
    InfectedWithClusterList = []
    ClusterWithWithOrigin = []
    for i in data.get("cluster"):
        InfectedWithClusterList.append(compareString(data.get("infected").get("genome"), i['genome']))
        ClusterWithWithOrigin.append(compareString(data.get("origin").get("genome"), i['genome']))

    result = []
    for i in range(len(InfectedWithClusterList)):
        if InfectedWithClusterList[i][0] <= 2:
            # already with cluster, check if it is with origin.

            if ClusterWithWithOrigin[i][0] <= 2:
                # clutser with origin
                if ClusterWithWithOrigin[i][0] == 0:
                    # cluster is the same as origin
                    if InfectedWithOrigin[1]:
                        result.append(data.get("infected").get("name") + " *-> " + data.get("origin").get("name"))
                        result.append(data.get("infected").get("name") + " *-> " + data.get("cluster")[i]['name'])
                    else:
                        result.append(data.get("infected").get("name") + " -> " + data.get("origin").get("name"))
                        result.append(data.get("infected").get("name") + " -> " + data.get("cluster")[i]['name'])

                else:

                    if ClusterWithWithOrigin[i][1]:
                        # cluster got * or not
                        if InfectedWithClusterList[i][1]:
                            # ifected got * or not
                            result.append(data.get("infected").get("name") + " *-> " + data.get("cluster")[i][
                                'name'] + " *-> " + data.get("origin").get("name"))
                        else:
                            result.append(data.get("infected").get("name") + " -> " + data.get("cluster")[i][
                                'name'] + " *-> " + data.get("origin").get("name"))
                    else:
                        if InfectedWithClusterList[i][1]:
                            # ifected got * or not
                            result.append(data.get("infected").get("name") + " *-> " + data.get("cluster")[i][
                                'name'] + " -> " + data.get("origin").get("name"))
                        else:
                            result.append(data.get("infected").get("name") + " -> " + data.get("cluster")[i][
                                'name'] + " -> " + data.get("origin").get("name"))
            else:
                # cluster and infected
                if InfectedWithClusterList[i][1]:
                    result.append(data.get("infected").get("name") + " *-> " + data.get("cluster")[i]['name'])
                else:
                    result.append(data.get("infected").get("name") + " -> " + data.get("cluster")[i]['name'])

                # not with origin only infected and cluster
        else:
            if InfectedWithOrigin[0] <= 2:
                if InfectedWithOrigin[1]:
                    result.append(data.get("infected").get("name") + " *-> " + data.get("origin").get("name"))
                else:
                    result.append(data.get("infected").get("name") + " -> " + data.get("origin").get("name"))
            # check if the guy in cluster is also connected to the origin if it is origin ->clutser-infected, then only this,
    return json.dump(result)


