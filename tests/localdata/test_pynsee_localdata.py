# -*- coding: utf-8 -*-
 
from unittest import TestCase
from pandas import pandas as pd
import geopandas as gpd
import sys

from pynsee.localdata._get_geo_relation import _get_geo_relation
from pynsee.localdata.get_insee_local import get_insee_local
from pynsee.localdata.get_included_area import get_included_area

from pynsee.localdata.get_geo_list import get_geo_list
from pynsee.localdata.get_nivgeo_list import get_nivgeo_list
from pynsee.localdata.get_area_list import get_area_list

from pynsee.localdata.get_local_metadata import get_local_metadata

from pynsee.localdata.get_map_link import get_map_link
from pynsee.localdata.get_map import get_map

class TestFunction(TestCase):

    version_3_7 = (sys.version_info[0]==3) & (sys.version_info[1]==7)
    
    if version_3_7:
    
        def test_get_geo_list_1(self):        
            list_available_geo = ['communes', 'regions', 'departements',
                                'communesDeleguees', 'communesAssociees',
                                'arrondissements', 'arrondissementsMunicipaux']   
      
            list_geo_data = []
            for geo in list_available_geo:
                list_geo_data.append(get_geo_list(geo))            
            df = pd.concat(list_geo_data)
    
            self.assertTrue(isinstance(df, pd.DataFrame))
        
        def test_get_geo_list_2(self):   
            self.assertRaises(ValueError, get_geo_list, 'a') 
    
        def test_get_geo_relation_1(self):    
            df1 = _get_geo_relation('region', "11", 'descendants')
            df2 = _get_geo_relation('departement', "91", 'ascendants')
            test = isinstance(df1, pd.DataFrame) & isinstance(df2, pd.DataFrame)
            self.assertTrue(test)        
        
        def test_get_nivgeo_list(self):
            data = get_nivgeo_list()
            self.assertTrue(isinstance(data, pd.DataFrame))
        
        def test_get_local_metadata(self):
            data = get_local_metadata()
            self.assertTrue(isinstance(data, pd.DataFrame))
    
        def test_get_insee_local_1(self):  
    
            dep = get_geo_list('departements')
    
            variables = 'AGESCOL-SEXE-ETUD'
            dataset = 'GEO2019RP2011'
            # codegeo = ['91', '976']
            codegeos = list(dep.CODE)
            codegeos = dep.CODE.to_list()
            geo = 'DEP'
            data = get_insee_local(variables=variables,
                                   dataset_version=dataset, nivgeo=geo, geocodes = codegeos)
    
            self.assertTrue(isinstance(data, pd.DataFrame))
            
            
        def test_get_insee_local_all(self):
                        
            data = get_insee_local(dataset_version='GEO2020RP2017',
                                   variables =  'SEXE-DIPL_19',
                                   nivgeo = 'DEP',
                                   geocodes = ['91','92', '976'])
            test1 = isinstance(data, pd.DataFrame)
            
            data = get_insee_local(dataset_version='GEO2020FILO2018',
                                   variables =  'INDICS_FILO_DISP_DET-TRAGERF',
                                   nivgeo = 'REG',
                                   geocodes = ['11', '01'])
            test2 = isinstance(data, pd.DataFrame)
            
            data = get_insee_local(dataset_version='BDCOM2017',
                                   variables =  'INDICS_BDCOM',
                                   nivgeo = 'REG',
                                   geocodes = ['11'])
            test3 = isinstance(data, pd.DataFrame)
            
            data = get_insee_local(dataset_version= 'GEO2019RFD2011',
                                   variables = 'INDICS_ETATCIVIL',
                                   nivgeo = 'REG',
                                   geocodes = ['11'])
            test4 = isinstance(data, pd.DataFrame)
            
            data = get_insee_local(dataset_version= 'TOUR2019',
                                   variables = 'ETOILE',
                                   nivgeo = 'REG',
                                   geocodes = ['11'])
            test5 = isinstance(data, pd.DataFrame)
            
            data = get_insee_local(dataset_version= 'GEO2020FLORES2017',
                                   variables = 'EFFECSAL5T_1_100P',
                                   nivgeo = 'REG',
                                   geocodes = ['11'])
            test6 = isinstance(data, pd.DataFrame)
            
            data = get_insee_local(dataset_version= 'GEO2019REE2018',
                                   variables = 'NA5_B',
                                   nivgeo = 'REG',
                                   geocodes = ['11'])
            test7 = isinstance(data, pd.DataFrame)
            
            data = get_insee_local(dataset_version= 'POPLEG2018',
                                   variables = 'IND_POPLEGALES',
                                   nivgeo = 'COM',
                                   geocodes = ['91477'])
            test8 = isinstance(data, pd.DataFrame)
            
            test = test1 & test2 & test3 & test4 & test5 & test6 & test7 & test8 
            self.assertTrue(test)
    
        def test_get_map_link(self):
            map_file = get_map_link('communes')
            map = gpd.read_file(map_file)
            self.assertTrue(isinstance(map, gpd.geodataframe.GeoDataFrame))
        
        def test_get_map(self):
            map = get_map('arrondissements-municipaux')
            self.assertTrue(isinstance(map, gpd.geodataframe.GeoDataFrame))
        
        def test_get_area_list_1(self):                 
            def get_area_list_test():
                get_area_list('a')    
            self.assertRaises(ValueError, get_area_list_test)
        
        def test_get_included_area(self):   
              
            list_available_area = ['zonesDEmploi2020', 
                                   'airesDAttractionDesVilles2020',
                                   'unitesUrbaines2020']
            list_data = []
            
            for a in list_available_area:
                df_list = get_area_list(a)
                code = df_list.CODE[:3].to_list()
                data = get_included_area(area_type=a, codeareas=code)
                list_data.append(data)
                
            data_final = pd.concat(list_data)
            
            self.assertTrue(isinstance(data_final, pd.DataFrame))