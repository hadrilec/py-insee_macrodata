# -*- coding: utf-8 -*-
from functools import lru_cache

@lru_cache(maxsize=None)
def _get_insee_one_area(area_type, codearea):
    
    import pandas as pd 
    from pynsee.utils._request_insee import _request_insee
    from pynsee.local.get_area_list import get_area_list
    
    df_list = get_area_list(area_type)
    list_available_codeareas = df_list.code.to_list()
    
    list_ZE20 = ['ZE2020', 'zonesDEmploi2020', 'ZoneDEmploi2020']
    list_AAV20 = ['AAV2020', 'airesDAttractionDesVilles2020', 'AireDAttractionDesVilles2020']
    list_UU20 = ['UU2020' ,'unitesUrbaines2020', 'UniteUrbaine2020']
    
    list_ZE20 = [s.lower() for s in list_ZE20]
    list_AAV20 = [s.lower() for s in list_AAV20]
    list_UU20 = [s.lower() for s in list_UU20]
    
    if area_type.lower().isin(list_ZE20) :
        type2 = 'zoneDEmploi2020'
    if area_type.lower().isin(list_AAV20):
        type2 = 'aireDAttractionDesVilles2020'
    if area_type.lower().isin(list_UU20):
        type2 = 'uniteUrbaine2020'
        
    if codearea in list_available_codeareas:
        api_url = 'https://api.insee.fr/metadonnees/V1/geo/'
        api_url = api_url  + type2 + '/' + codearea + '/descendants'
        request = _request_insee(api_url = api_url,  file_format = 'application/json')
        
        data = request.json()
        list_data_area = []
        for i in range(len(data)):
            df = pd.DataFrame(data[i], index=[0])
            list_data_area.append(df)
            
        data_area = pd.concat(list_data_area).reset_index(drop=True)
        
        ref_area_label = df_list.loc[df_list.code == codearea].intitule
        ref_area_label = ref_area_label.reset_index(drop=True)[0]
        
        data_area = data_area.assign(ref_area_code = codearea,
                                     ref_area_label = ref_area_label)
    else:
        print('{} is not available in get_area_list({})'.format(codearea, area_type))
    
    return(data_area)