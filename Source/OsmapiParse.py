#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Anton Kustov <snowfall.irk@gmail.com> 2014                 ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

import imp
import os

def OsmapiParse(TileCoordinates, TileSource):
    
    if TileSource == 'Local':
        OsmApi = imp.load_source('OsmApi', os.path.join(os.path.abspath(''), 'Source', 'OsmapiLocal.py'))
    elif TileSource == 'Internet':
        OsmApi = imp.load_source('OsmApi', os.path.join(os.path.abspath(''), 'Source', 'OsmapiInternet.py'))
    
    Osm = OsmApi.OsmApi()
    OsmMap = Osm.Map(TileCoordinates, TileSource)
    NodeList     = []
    WayList      = []
    RelationList = []
    
    # Sepatate list OsmMap into lists NodeList, WayList, RelationsList
    for Dict in OsmMap:
        if Dict['type'] == 'node':
            NodeList.append(Dict)
            continue
        elif Dict['type'] == 'way':
            WayList.append(Dict)
            continue
        elif Dict['type'] == 'relation':
            RelationList.append(Dict)
            continue

    # Extract nodes from list OsmMap and make dict NodeDict
    NodeCount = 0
    NodeDict1 = {}
    NodeDict2 = {}
    NodeDict  = {}
    for i in NodeList:
        NodeCount += 1
        i['type'] += str(NodeCount)
        NodeDict1[i.pop('type')] = i
        i.update()
    for i in NodeDict1:
        NodeDict2.update({i: NodeDict1[i]['data']})
    for i in iter(NodeDict2):
        NodeDict.update({NodeDict2[i]['id']: NodeDict2[i]})
    
    # Extract ways from list OsmMap and make dict WayDict
    WayCount = 0
    WayDict1 = {}
    WayDict2 = {}
    WayDict  = {}
    for i in WayList:
        WayCount += 1
        i['type'] += str(WayCount)
        WayDict1[i.pop('type')] = i
        i.update()

    for i in WayDict1:
        WayDict2.update({i: WayDict1[i]['data']})

    for i in iter(WayDict2):
        WayDict.update({WayDict2[i]['id']: WayDict2[i]})
    
    # Extract relations from list OsmMap and make dict RelationDict
    RelationCount = 0
    RelationDict1 = {}
    RelationDict2 = {}
    RelationDict  = {}
    for i in RelationList:
        RelationCount += 1
        i['type'] += str(RelationCount)
        RelationDict1[i.pop('type')] = i
        i.update()

    for i in RelationDict1:
        RelationDict2.update({i: RelationDict1[i]['data']})

    for i in iter(RelationDict2):
        RelationDict.update({RelationDict2[i]['id']: RelationDict2[i]})
    return NodeDict, WayDict, RelationDict