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

import bpy
import imp
import math
import mathutils
import os
import struct

def ConvertPolarEuclid(LongitudePolar, LatitudePolar, start_lon, start_lat):
    
    ConstantEarthRadius = 6371000
    ConvertPolarEuclidRatio = 2 * math.pi * ConstantEarthRadius / 360
    
    LongitudeEuclid = round((LongitudePolar - float(start_lon)) * ConvertPolarEuclidRatio * math.cos(math.radians(LatitudePolar)), 2)
    LatitudeEuclid  = round((LatitudePolar  - float(start_lat)) * ConvertPolarEuclidRatio                                        , 2)
    
    return LongitudeEuclid, LatitudeEuclid

def ImportOsm(TileCoordinates, TileSource, ReplaceExisting, MaterialsSet, LandscapeAlign, OsmParameters):
    
    min_lon = TileCoordinates[0]
    min_lat = TileCoordinates[1]
    max_lon = TileCoordinates[2]
    max_lat = TileCoordinates[3]
    
    OsmapiParse = imp.load_source('OsmapiParse', os.path.join(os.path.abspath(''), 'Source', 'OsmapiParse.py'))
    NodeDict, WayDict, RelationDict = OsmapiParse.OsmapiParse(TileCoordinates, TileSource)
    
    ObjectNewCount = 0
    
    for Way in iter(WayDict):
        
        SceneBpy = bpy.context.scene
        ObjectNewName = str(Way)
        print(ObjectNewCount, ' of ', len(WayDict), ObjectNewName)
        
        # Remove object if already exists
        ReplaceExistingCheck = False
        
        for ObjectIterate in SceneBpy.objects:
            
            '''if ObjectNewName in ObjectIterate:
                
                if ReplaceExisting == False:
                    
                    ReplaceExistingCheck = True
                    continue
                
                bpy.ops.object.select_all(action = 'DESELECT')
                bpy.ops.object.select_pattern(pattern = ObjectIterate)
                SceneBpy.objects.active = bpy.data.objects[ObjectIterate]
                bpy.ops.object.delete()
                
                # Unlink mesh
                for Mesh in bpy.data.meshes:
                    if not ObjectNewName in Mesh.name:
                        continue
                    
                    if Mesh.users != 0:
                        continue
                    
                    bpy.data.meshes.remove(Mesh)
                
                # TODO add replacement object on the same layer
        
        if ReplaceExistingCheck == True:
            continue'''
        
        # Create new mesh and object
        ObjectNewMesh = bpy.data.meshes.new(ObjectNewName)
        ObjectNew = bpy.data.objects.new(ObjectNewName, ObjectNewMesh)
        ObjectNew.location = mathutils.Vector((0.0, 0.0, 0.0))
        SceneBpy.objects.link(ObjectNew)
        SceneBpy.objects.active = ObjectNew
        ObjectNew.select = True
        ObjectNewMeshVerticesCount = 0
        ObjectNewMeshVertices = []
        ObjectNewMeshEdges    = []
        ObjectNewMeshFaces    = []
        
        # New object's mesh
        for WayNode in WayDict[Way]['nd']:
            LongitudePolar = float(NodeDict[WayNode]['lon'])
            LatitudePolar  = float(NodeDict[WayNode]['lat'])
            LongitudeEuclid, LatitudeEuclid = ConvertPolarEuclid(LongitudePolar, LatitudePolar, start_lon, start_lat)
            
            ObjectNewMeshVertices.append((LongitudeEuclid, LatitudeEuclid, 0.0),)
            
            ObjectNewMeshVerticesCount += 1
            if ObjectNewMeshVerticesCount > 1:
                ObjectNewMeshEdges = ObjectNewMeshEdges + [(ObjectNewMeshVerticesCount - 2, ObjectNewMeshVerticesCount - 1)]
        
        ObjectNewMesh.from_pydata(ObjectNewMeshVertices, ObjectNewMeshEdges, ObjectNewMeshFaces)
        ObjectNewMesh.update()
        
        # Remove double vertices
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.remove_doubles(threshold = 0.0001, use_unselected = False)
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        if 'barrier' in WayDict[Way]['tag']:
            
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.fill(use_beauty = False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # TODO fix barrier LandscapeAlign
            '''if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
                print(ObjectNewCount, ' of ', len(WayDict), ', Area, ', ObjectNewName)'''
            
            # Flip normals upwards
            if len(ObjectNewMesh.polygons) != 0:
                if ObjectNewMesh.polygons[0].normal.z > 0:
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
            
            #TODO Remove only inside faces
            
            # Extrude upwards
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv = None, TRANSFORM_OT_translate = {"value":mathutils.Vector((0.0, 0.0, OsmParameters['BarrierHeight']))})
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # TODO thickness, double sided if thickness == 0
            
            # Material depending on type
            if MaterialsSet == 'Scheme':
                bpy.context.object.data.materials.append(bpy.data.materials['BuildingGarage'])
            
            elif MaterialsSet == 'Realistic':
                bpy.context.object.data.materials.append(bpy.data.materials['BuildingRealistic'])
            
            bpy.ops.object.select_all(action = 'DESELECT')
            bpy.ops.object.select_pattern(pattern = ObjectNewName)
            SceneBpy.objects.active = ObjectNew
        
        if 'amenity' in WayDict[Way]['tag'] and not 'building' in WayDict[Way]['tag']:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.fill(use_beauty = False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
            
            # Flip normals upwards
            if len(ObjectNewMesh.polygons) != 0:
                if ObjectNewMesh.polygons[0].normal.z > 0:
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # TODO triangulate modifier, beauty
            
            # Extrude upwards
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = OsmParameters['AmenityThickness']
            ObjectNew.modifiers['Solidify'].offset = -1
            # TODO do not fill rim
            
            # TODO shade smooth
            
            # Material depending on type
            if MaterialsSet == 'Scheme':
                
                if 'fuel' in WayDict[Way]['tag']['amenity']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LanduseCommercial'])
                
                elif 'hospital' in WayDict[Way]['tag']['amenity']:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenityHospital'])
                
                elif 'kindergarten' in WayDict[Way]['tag']['amenity']:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenityKindergarten'])
                
                elif 'parking' in WayDict[Way]['tag']['amenity']:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenityParking'])
                
                elif 'place_of_worship' in WayDict[Way]['tag']['amenity']:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenityPlace_of_worship'])
                
                elif 'prison' in WayDict[Way]['tag']['amenity']:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenityPrison'])
                
                elif 'school' in WayDict[Way]['tag']['amenity']:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenitySchool'])
                
                else:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenityUnknown'])
            
            elif MaterialsSet == 'Realistic':
                bpy.context.object.data.materials.append(bpy.data.materials['AmenityRealistic'])
        
        elif 'area' in WayDict[Way]['tag']:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.fill(use_beauty = False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
            
            # Flip normals upwards
            if len(ObjectNewMesh.polygons) != 0:
                if ObjectNewMesh.polygons[0].normal.z > 0:
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
        
        elif 'building' in WayDict[Way]['tag']:
            RelationTag = []
            ImportOsmBuilding(WayDict, 
                              Way, 
                              MaterialsSet, 
                              ObjectNewName, 
                              OsmParameters, 
                              RelationTag)
        
        elif 'highway' in WayDict[Way]['tag']:
            
            # Extrude upwards
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv = None, TRANSFORM_OT_translate = {"value":mathutils.Vector((0.0, 0.0, 0.1))})
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # Extrude sideways
            HighwayLanes = 1
            if 'lanes' in WayDict[Way]['tag']:
                HighwayLanes = int(WayDict[Way]['tag']['lanes'])
            
            if 'footway' in WayDict[Way]['tag']['highway'] or 'steps' in WayDict[Way]['tag']['highway']:
                HighwayLaneWidthOverride = OsmParameters['HighwayWidthFootway']
            else:
                HighwayLaneWidthOverride =  OsmParameters['HighwayLaneWidth']
            
            bpy.ops.object.modifier_add(type = 'SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = HighwayLaneWidthOverride * HighwayLanes
            ObjectNew.modifiers['Solidify'].offset = 0
            ObjectNew.modifiers['Solidify'].use_even_offset = True
            
            bpy.ops.object.modifier_apply(modifier="Solidify")
            
            # Remove top layer of vertices
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            for ObjectNewVertice in ObjectNew.data.vertices:
                if round(ObjectNewVertice.co.z, 1) == OsmParameters['HighwayThickness']:
                    ObjectNewVertice.select = True
            
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.delete(type='VERT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # Align to landscape
            if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
                print(ObjectNewCount, ' of ', len(WayDict), ', Highway, ', ObjectNewName)
            
            # Extrude upwards again
            bpy.ops.object.modifier_add(type = 'SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = OsmParameters['HighwayThickness']
            ObjectNew.modifiers['Solidify'].use_even_offset = True
            
            # Material
            if MaterialsSet == 'Scheme':
                
                if   'secondary' in WayDict[Way]['tag']['highway']:
                    bpy.context.object.data.materials.append(bpy.data.materials['HighwaySecondary'])
                
                elif 'tertiary' in WayDict[Way]['tag']['highway']:
                    bpy.context.object.data.materials.append(bpy.data.materials['HighwayTertiary'])
                
                else:
                    bpy.context.object.data.materials.append(bpy.data.materials['HighwayUnknown'])
            
            elif MaterialsSet == 'Realistic':
                bpy.context.object.data.materials.append(bpy.data.materials['HighwayRealistic'])
        
        elif 'railway' in WayDict[Way]['tag']:
            
            
            # Extrude upwards
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv = None, TRANSFORM_OT_translate = {"value":mathutils.Vector((0.0, 0.0, OsmParameters['HighwayThickness']))})
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # Extrude sideways
            RailwayLaneWidth = OsmParameters['RailwayWidth']
            if 'tram' in WayDict[Way]['tag']['railway']:
                RailwayLaneWidth = OsmParameters['RailwayWidthTram']
            
            bpy.ops.object.modifier_add(type = 'SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = RailwayLaneWidth
            ObjectNew.modifiers['Solidify'].offset = 0
            ObjectNew.modifiers['Solidify'].use_even_offset = True
            
            bpy.ops.object.modifier_apply(modifier="Solidify")
            
            # Remove top layer of vertices
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            for ObjectNewVertice in ObjectNew.data.vertices:
                if round(ObjectNewVertice.co.z, 1) == OsmParameters['HighwayThickness']:
                    ObjectNewVertice.select = True
            
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.delete(type='VERT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # Align to landscape
            if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
                print(ObjectNewCount, ' of ', len(WayDict), ', Highway, ', ObjectNewName)
            
            # Extrude upwards again
            bpy.ops.object.modifier_add(type = 'SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = OsmParameters['HighwayThickness']
            ObjectNew.modifiers['Solidify'].use_even_offset = True
            
            # Material
            if MaterialsSet == 'Scheme':
                bpy.context.object.data.materials.append(bpy.data.materials['HighwayUnknown'])
            
            elif MaterialsSet == 'Realistic':
                bpy.context.object.data.materials.append(bpy.data.materials['HighwayRealistic'])
        
        elif 'leisure' in WayDict[Way]['tag']:
            
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.fill(use_beauty = False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
                print(ObjectNewCount, ' of ', len(WayDict), ', Area, ', ObjectNewName)
            
            # Flip normals upwards
            if len(ObjectNewMesh.polygons) != 0:
                if ObjectNewMesh.polygons[0].normal.z > 0:
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # Extrude up
            
            if   'pitch'      in WayDict[Way]['tag']['leisure']:
                LeisureThickness = OsmParameters['LeisureThicknessPitch']
            
            elif 'playground' in WayDict[Way]['tag']['leisure']:
                LeisureThickness = OsmParameters['LeisureThicknessPlayground']
            
            else:
                LeisureThickness = OsmParameters['LeisureThickness']
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = LeisureThickness
            ObjectNew.modifiers['Solidify'].offset = -1
            
            # Material
            if MaterialsSet == 'Scheme':
                
                if 'nature_reserve' in WayDict[Way]['tag']['leisure']:
                    bpy.context.object.data.materials.append(bpy.data.materials['NaturalWood'])
                
                elif 'park' in WayDict[Way]['tag']['leisure']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LeisurePark'])
                
                elif 'pitch' in WayDict[Way]['tag']['leisure']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LeisurePitch'])
                
                elif 'playground' in WayDict[Way]['tag']['leisure']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LeisurePlayground'])
                
                elif 'track' in WayDict[Way]['tag']['leisure']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LeisurePitch'])
            
            elif MaterialsSet == 'Realistic':
                bpy.context.object.data.materials.append(bpy.data.materials['LeisureRealistic'])
        
        elif 'landuse' in WayDict[Way]['tag']:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.fill(use_beauty = False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
            
            # Flip normals upwards
            if len(ObjectNewMesh.polygons) != 0:
                if ObjectNewMesh.polygons[0].normal.z > 0:
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
            
            # Extrude up
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = OsmParameters['LanduseThickness']
            ObjectNew.modifiers['Solidify'].offset = -1
            
            # Material depending on type
            if MaterialsSet == 'Scheme':
                if 'allotments' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['NaturalWood'])
                
                elif 'cemetery' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['AmenityPlace_of_worship'])
                
                elif 'commercial' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LanduseCommercial'])
                
                elif 'construction' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LanduseConstruction'])
                
                elif 'forest' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['NaturalWood'])
                
                elif 'garages' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LanduseGarages'])
                
                elif 'grass' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LeisurePark'])
                
                elif 'greenfield' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LeisurePark'])
                
                elif 'industrial' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LanduseIndustrial'])
                
                elif 'railway' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LanduseGarages'])
                
                elif 'residential' in WayDict[Way]['tag']['landuse']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LanduseResidential'])
        
        elif 'natural' in WayDict[Way]['tag']:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.fill(use_beauty = False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            if LandscapeAlign == True:
                ObjectVerticeName = ObjectNewName
                ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
                AlignLandscapeArea(ObjectVerticeName, ObjectFaceName)
            
            # Flip normals upwards
            if len(ObjectNewMesh.polygons) != 0:
                if ObjectNewMesh.polygons[0].normal.z > 0:
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
            
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            ObjectNew.modifiers['Solidify'].thickness = 0.1
            ObjectNew.modifiers['Solidify'].offset = -1
            
            # Material depending on type
            if MaterialsSet == 'Scheme':
                if   'grassland' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['LeisurePark'])
                
                elif 'water' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['NaturalWater'])
                
                elif 'wetland' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['NaturalWetland'])
                
                elif 'wood' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['NaturalWood'])
            
            elif MaterialsSet == 'Realistic':
                if   'grassland' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['GrassRealistic'])
                
                elif 'water' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['WaterRealistic'])
                
                elif 'wetland' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['GrassRealistic'])
                
                elif 'wood' in WayDict[Way]['tag']['natural']:
                    bpy.context.object.data.materials.append(bpy.data.materials['GrassRealistic'])
        
        ObjectNewCount += 1
    
    for Relation in iter(RelationDict):
        
        if 'type' not in RelationDict[Relation]['tag']:
            continue
        
        if RelationDict[Relation]['tag']['type'] == 'multipolygon':
            
            for RelationMember in RelationDict[Relation]['member']:
                
                if RelationMember['type'] != 'way' or RelationMember['ref'] not in WayDict:
                    continue
                
                Way = RelationMember['ref']
                ObjectNewName = str(RelationMember['ref'])
                RelationTag = []
                
                if 'building' in RelationDict[Relation]['tag']:
                    
                    RelationTag = RelationDict[Relation]['tag']
                    
                    ImportOsmBuilding(WayDict,
                                      Way, 
                                      MaterialsSet, 
                                      ObjectNewName, 
                                      OsmParameters, 
                                      RelationTag)

def ImportOsmBuilding(WayDict, 
                      Way, 
                      MaterialsSet, 
                      ObjectNewName, 
                      OsmParameters, 
                      RelationTag):
    
    ObjectNew = bpy.data.objects[ObjectNewName]
    bpy.ops.object.select_pattern(pattern=ObjectNewName)
    SceneBpy = bpy.context.scene
    SceneBpy.objects.active = ObjectNew
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.fill(use_beauty = False)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if len(bpy.data.objects[ObjectNewName].data.polygons) > 0 and bpy.data.objects[ObjectNewName].data.polygons[0].normal.z < 0:
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if LandscapeAlign == True:
        ObjectVerticeName = ObjectNewName
        ObjectFaceName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
        MeshStep = 100
        AlignLandscapeBuilding(ObjectVerticeName, ObjectFaceName, MeshStep)
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    ObjectNew.modifiers['Solidify'].thickness = OsmParameters['BuildingLevelHeight']
    ObjectNew.modifiers['Solidify'].offset = 1
    
    if 'building:levels' in WayDict[Way]['tag']:
        ObjectNew.modifiers['Solidify'].thickness = OsmParameters['BuildingLevelHeight'] * float(WayDict[Way]['tag']['building:levels'])
    if RelationTag != []:
        if 'building:levels' in RelationTag:
            ObjectNew.modifiers['Solidify'].thickness = OsmParameters['BuildingLevelHeight'] * float(RelationTag['building:levels'])
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if len(bpy.data.objects[ObjectNewName].data.polygons) > 0 and bpy.data.objects[ObjectNewName].data.polygons[0].normal.z < 0:
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if RelationTag == []:
        Tag = WayDict[Way]['tag']
    else:
        Tag = RelationTag
    
    # Material
    if MaterialsSet == 'Scheme':
        
        if   'amenity' in Tag['building']:
            
            if   'hospital' in Tag['amenity']:
                bpy.context.object.data.materials.append(bpy.data.materials['AmenityHospital'])
            
            elif 'kindergarten' in Tag['amenity']:
                bpy.context.object.data.materials.append(bpy.data.materials['BuildingKindergarten'])
            
            elif 'university' in Tag['amenity']:
                bpy.context.object.data.materials.append(bpy.data.materials['BuildingUniversity'])
        
        elif 'apartments' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingApartments'])
        
        elif 'chirch' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingChirch'])
        
        elif 'commercial' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingCommercial'])
        
        elif 'dormitory' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingDormitory'])
        
        elif 'garage' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingGarage'])
        
        elif 'garages' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingGarage'])
        
        if   'hospital' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['AmenityHospital'])
        
        if   'office' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingOffice'])
        
        elif 'retail' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingCommercial'])
        
        elif 'residential' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingResidential'])
        
        elif 'school' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingSchool'])
        
        elif 'shop' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingCommercial'])
        
        elif 'university' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingUniversity'])
        
        elif 'warehouse' in Tag['building']:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingGarage'])
        
        else:
            bpy.context.object.data.materials.append(bpy.data.materials['BuildingUnknown'])
    
    elif MaterialsSet == 'Realistic':
        bpy.context.object.data.materials.append(bpy.data.materials['BuildingRealistic'])

def ImportSrtm3(start_lon, min_lon, max_lon, start_lat, min_lat, max_lat):
    ObjectNewName = min_lon + ',' + min_lat + ',' + max_lon + ',' + max_lat
    
    start_lon = float(start_lon)
    min_lon   = float(min_lon)
    max_lon   = float(max_lon)
    start_lat = float(start_lat)
    min_lat   = float(min_lat)
    max_lat   = float(max_lat)
    
    if min_lon <= -100:
        LongitudePrefix = 'W'
    elif min_lon > -100 and min_lon <= -10:
        LongitudePrefix = 'W0'
    elif min_lon > -10 and min_lon < 0:
        LongitudePrefix = 'W00'
    elif min_lon >= 0 and min_lon < 10:
        LongitudePrefix = 'E00'
    elif min_lon >= 10 and min_lon < 100:
        LongitudePrefix = 'E0'
    elif min_lon >= 100:
        LongitudePrefix = 'E'
    
    if min_lat <= -10:
        LatitudePrefix = 'S'
    elif min_lat > -10 and min_lat < 0:
        LatitudePrefix = 'S0'
    elif min_lat >= 0 and min_lat < 10:
        LatitudePrefix = 'N0'
    elif min_lat >= 10:
        LatitudePrefix = 'N'
    
    SceneBpy = bpy.context.scene
    ObjectNewMesh = bpy.data.meshes.new(ObjectNewName)
    ObjectNew = bpy.data.objects.new(ObjectNewName, ObjectNewMesh)
    ObjectNew.location = mathutils.Vector((0.0, 0.0, 0.0))
    SceneBpy.objects.link(ObjectNew)
    SceneBpy.objects.active = ObjectNew
    ObjectNew.select = True
    ObjectNewMeshVertices = []
    ObjectNewMeshEdges    = []
    ObjectNewMeshFaces    = []
    
    TileName = LatitudePrefix + str(abs(int(min_lat))) + LongitudePrefix + str(abs(int(min_lon)))
    tile = os.path.join(os.path.abspath(''), 'Data', 'Srtm3', TileName + ".hgt")
    TileLonMin = int(       1200 * (min_lon - math.modf(min_lon)[1]))
    TileLonMax = int(round((1200 * (max_lon - math.modf(min_lon)[1])), 0))
    TileLatMin = 1200 - int(round((1200 * (max_lat - math.modf(min_lat)[1])), 0))
    TileLatMax = 1200 - int(       1200 * (min_lat - math.modf(min_lat)[1]))
    
    count = -1
    with open(tile, "rb") as f:
        for i in range(TileLatMin, TileLatMax + 1):
            for j in range(TileLonMin, TileLonMax + 1):
                
                f.seek((i * (1200 + 1) + j) * 2)  # go to the right spot,
                buf = f.read(2)  # read two bytes and convert them:
                val = struct.unpack('>h', buf)  # ">h" is a signed two byte integer
                
                LongitudePolar = int(min_lon) + j          / 1200
                LatitudePolar  = int(min_lat) + (1200 - i) / 1200
                LongitudeEuclid, LatitudeEuclid = ConvertPolarEuclid(LongitudePolar, LatitudePolar, start_lon, start_lat)
                
                ObjectNewMeshVertices.append((LongitudeEuclid,LatitudeEuclid, val[0]))
                
                count += 1
                if count > (TileLonMax - TileLonMin + 1) and count % (TileLonMax - TileLonMin + 1) != 0:
                    ObjectNewMeshFaces.append((count, count - 1, count - 1 - (TileLonMax - TileLonMin + 1)                                       ))
                    ObjectNewMeshFaces.append((count,            count - 1 - (TileLonMax - TileLonMin + 1), count - (TileLonMax - TileLonMin + 1)))
    
    ObjectNewMesh.from_pydata(ObjectNewMeshVertices, ObjectNewMeshEdges, ObjectNewMeshFaces)
    ObjectNewMesh.update()

def AlignLandscapeBuilding(ObjectVerticeName, ObjectFaceName, MeshStep):
    
    ObjectVertice = bpy.data.objects[ObjectVerticeName]
    ObjectFace    = bpy.data.objects[ObjectFaceName]
    
    bpy.ops.object.select_pattern(pattern=ObjectVerticeName)
    
    if len(ObjectVertice.data.polygons) != 0:
        if ObjectVertice.data.polygons[0].normal.z < 0:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.mode_set(mode = 'OBJECT')
    
    HeightMaximum = 9000
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    ObjectVertice.modifiers['Solidify'].thickness = HeightMaximum
    ObjectVertice.modifiers['Solidify'].offset = 1.0
    
    bpy.ops.object.modifier_add(type='BOOLEAN')
    ObjectVertice.modifiers['Boolean'].operation = 'INTERSECT'
    ObjectVertice.modifiers['Boolean'].object = ObjectFace
    
    bpy.ops.object.modifier_apply(modifier="Solidify")
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for ObjectVerticeVertice in ObjectVertice.data.vertices:
        if round(ObjectVerticeVertice.co.z, 0) == 0 or round(ObjectVerticeVertice.co.z, 0) == HeightMaximum:
            ObjectVerticeVertice.select = True
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    # Move all vertices to Z pozition of lower vertice
    ObjectVerticeVerticeLowerZ = HeightMaximum
    for ObjectVerticeVertice in ObjectVertice.data.vertices:
        if ObjectVerticeVertice.co.z < ObjectVerticeVerticeLowerZ:
            ObjectVerticeVerticeLowerZ = ObjectVerticeVertice.co.z
    
    for ObjectVerticeVertice in ObjectVertice.data.vertices:
        ObjectVerticeVertice.co.z = ObjectVerticeVerticeLowerZ

def AlignLandscapeLine(ObjectVerticeName, ObjectFaceName):
    ObjectVertice = bpy.data.objects[ObjectVerticeName]
    ObjectFace    = bpy.data.objects[ObjectFaceName]
    
    bpy.ops.object.select_pattern(pattern=ObjectVerticeName)
    
    # Collect middle points of edges
    ObjectVerticeEdgeCollect = []
    for ObjectVerticeEdge in ObjectVertice.data.edges:
        ObjectVerticeEdgeCollect.append((
                                         round(
                                               (ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[0]].co.x + 
                                                ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[1]].co.x) / 2, 
                                               2), 
                                         round(
                                               (ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[0]].co.y + 
                                                ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[1]].co.y) / 2, 
                                               2)
                                       ),)
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.fill(use_beauty = False)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    if len(ObjectVertice.data.polygons) != 0:
        if ObjectVertice.data.polygons[0].normal.z < 0:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.mode_set(mode = 'OBJECT')
    
    HeightMaximum = 9000
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    ObjectVertice.modifiers['Solidify'].thickness = HeightMaximum
    ObjectVertice.modifiers['Solidify'].offset = 1.0
    
    bpy.ops.object.modifier_add(type='BOOLEAN')
    ObjectVertice.modifiers['Boolean'].operation = 'INTERSECT'
    ObjectVertice.modifiers['Boolean'].object = ObjectFace
    
    bpy.ops.object.modifier_apply(modifier="Solidify")
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.remove_doubles(threshold = 0.0001, use_unselected = False)
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    # Remove bottom and top layer of vertices
    for ObjectVerticeVertice in ObjectVertice.data.vertices:
        if round(ObjectVerticeVertice.co.z, 0) == 0 or round(ObjectVerticeVertice.co.z, 0) == HeightMaximum:
            ObjectVerticeVertice.select = True
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    # Compare middle points of new edges with middle poinds of original edges and remove not matching
    for ObjectVerticeEdge in ObjectVertice.data.edges:
        ObjectVerticeEdgeMatch = False
        for ObjectVerticeEdgeCollectEdge in ObjectVerticeEdgeCollect:
            if (
                round(
                      (ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[0]].co.x + 
                       ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[1]].co.x) / 2, 
                      2), 
                round(
                      (ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[0]].co.y + 
                       ObjectVertice.data.vertices[ObjectVerticeEdge.vertices[1]].co.y) / 2, 
                      2)
               ) == ObjectVerticeEdgeCollectEdge:
                ObjectVerticeEdgeMatch = True
        if ObjectVerticeEdgeMatch == False:
            ObjectVerticeEdge.select = True
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='EDGE')
    bpy.ops.object.mode_set(mode = 'OBJECT')

def AlignLandscapeArea(ObjectVerticeName, ObjectFaceName):
    ObjectVertice = bpy.data.objects[ObjectVerticeName]
    ObjectFace    = bpy.data.objects[ObjectFaceName]
    
    bpy.ops.object.select_pattern(pattern=ObjectVerticeName)
    
    if len(ObjectVertice.data.polygons) != 0:
        if ObjectVertice.data.polygons[0].normal.z < 0:
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.mode_set(mode = 'OBJECT')
    
    HeightMaximum = 9000
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    ObjectVertice.modifiers['Solidify'].thickness = HeightMaximum
    ObjectVertice.modifiers['Solidify'].offset = 1.0
    
    bpy.ops.object.modifier_add(type='BOOLEAN')
    ObjectVertice.modifiers['Boolean'].operation = 'INTERSECT'
    ObjectVertice.modifiers['Boolean'].object = ObjectFace
    
    bpy.ops.object.modifier_apply(modifier="Solidify")
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for ObjectVerticeVertice in ObjectVertice.data.vertices:
        if round(ObjectVerticeVertice.co.z, 0) == 0 or round(ObjectVerticeVertice.co.z, 0) == HeightMaximum:
            ObjectVerticeVertice.select = True
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode = 'OBJECT')

#######################################################################
# Preferences                                                         #
#######################################################################

# 'Osm', 'Srtm', 'Osm and Srtm'
MapType = 'Osm'

start_lon = '104.300000'
min_lon   = '104.300000'
max_lon   = '104.350000'

start_lat =  '52.280000'
min_lat   =  '52.200000'
max_lat   =  '52.250000'

# 'Local', 'Internet'
TileSource = 'Internet'

ReplaceExisting = False

# 'None', 'Scheme', 'Realistic'
MaterialsSet = 'Scheme'

OsmParameters = {
    'AmenityThickness'          : 0.075,
    'LanduseThickness'          : 0.05,
    'LeisureThickness'          : 0.05,
    'LeisureThicknessPitch'     : 0.06,
    'LeisureThicknessPlayground': 0.075,
    'HighwayThickness'         : 0.1,
    'HighwayThicknessPrimary'  : 0.25,
    'HighwayThicknessSecondary': 0.2,
    'HighwayThicknessTertiary' : 0.15,
    
    'HighwayLaneWidth': 3,
    'HighwayWidthFootway': 2,
    
    'RailwayWidth': 2,
    'RailwayWidthTram': 1.5,
    
    'BuildingLevelHeight': 3,
    
    'BarrierHeight': 3,
    }

TileCoordinates = [min_lon, min_lat, max_lon, max_lat]

if MapType == 'Osm and Srtm':
    LandscapeAlign = True
else:
    LandscapeAlign = False

#######################################################################
# Import map tile                                                     #
#######################################################################
if MapType == 'Osm':
    ImportOsm(TileCoordinates, TileSource, ReplaceExisting, MaterialsSet, LandscapeAlign, OsmParameters)

elif MapType == 'Srtm':
    ImportSrtm3(start_lon, min_lon, max_lon, start_lat, min_lat, max_lat)

elif MapType == 'Osm and Srtm':
    ImportSrtm3(start_lon, min_lon, max_lon, start_lat, min_lat, max_lat)
    ImportOsm(TileCoordinates, TileSource, ReplaceExisting, MaterialsSet, LandscapeAlign, OsmParameters)
