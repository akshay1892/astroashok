from src.service.jhora import const, utils
from src.service.jhora.panchanga import drik
from src.service.jhora.horoscope.chart import  charts
from src.service.jhora.horoscope.chart import house
import json
_lang_path = const._LANGUAGE_PATH

def get_prediction_resources(language='en'):
    """
        get resources from prediction_msgs_<lang>.txt
        @param language: Two letter language code. en, hi, ka, ta, te
        @return json strings from the resource file as dictionary 
    """
    json_file = _lang_path + const._DEFAULT_PREDICTION_JSON_FILE_PREFIX+language+'.json'
    print('JSON_FILE_PATH', json_file)
    f = open(json_file,"r",encoding="utf-8")
    msgs = json.load(f)
    return msgs

def _get_general_lagna_rasi_prediction(jd,place,prediction_msgs,language=const._DEFAULT_LANGUAGE):
    janma_rasi = drik.raasi(jd, place)[0]-1
    results = {}
    source_count = 2
    for s in range(source_count):
        ks = utils.resource_strings['janma_rasi_str']+'_'+str(s+1)
        results[ks] = "<html><b>"+utils.resource_strings['general_prediction_str']+"</b><br>"
        #results[ks] += "<b>"+prediction_msgs['general_prediction_caution']+"</b><br>"
        results[ks] += "<b>"+prediction_msgs['janma_raasi_'+str(s+1)]['source']+"</b><br>"
        pdict = prediction_msgs['janma_raasi_'+str(s+1)][str(janma_rasi+1)]
        for k,v in pdict.items():
            results[ks] += "<b>"+k+"</b><br>"+v+"<br>"
    return results

def _get_planets_in_houses_prediction(planet_positions,prediction_msgs):
    p_to_h = utils.get_planet_house_dictionary_from_planet_positions(planet_positions)
    lagna_house = p_to_h['L']
    ks = utils.resource_strings['planets_str']
    results = {}
    results[ks] = "<html>"#<b>"+ks+"</b><br>"
    #results[ks] += "<b>"+utils.resource_strings['general_prediction_caution']+"</b><br>"
    planet_msgs = prediction_msgs['planets_in_houses']
    #print('planet msgs',planet_msgs)
    for planet in [*range(9)]:
        planet_house = house.get_relative_house_of_planet(lagna_house,p_to_h[planet])
        pl_msg = planet_msgs[str(planet_house)][planet]
        #print(planet,planet_house,pl_msg)
        key = const.PLANET_NAMES[planet]+'-'+utils.resource_strings['house_str']+'#'+str(planet_house)+":"
        results[ks] += "<b>"+key+"</b><br>"+pl_msg+"<br>"
    return results
def _get_lords_in_houses_prediction(planet_positions,prediction_msgs):
    p_to_h = utils.get_planet_house_dictionary_from_planet_positions(planet_positions)
    lagna_house = p_to_h['L']
    ks = utils.resource_strings['houses_str']
    results = {}
    results[ks] = "<html>"#<b>"+ks+"</b><br>"
    #results[ks] += "<b>"+utils.resource_strings['general_prediction_caution']+"</b><br>"
    planet_msgs = prediction_msgs['lord_of_a_house_joining_lord_of_another_house']
    #print('planet msgs',planet_msgs)
    for h in [*range(12)]:
        lord = const._house_owners_list[(h+lagna_house)%12]
        house_of_lord = house.get_relative_house_of_planet(lagna_house,p_to_h[lord])
        key = "Lord of House#"+str(h+1)+" in house#"+str(house_of_lord)
        #print('key',key)
        pl_msg = planet_msgs[str(h+1)][house_of_lord-1]
        results[ks] += "<b>"+key+"</b><br>"+pl_msg+"<br>"
    return results


@staticmethod
def _get_location(place_name):
    result = utils.get_location(place_name)
    print('RESULT',result)
    if result:
        _place_name,_latitude,_longitude,_time_zone = result
        # _place_text.setText(_place_name)
        # _lat_text.setText(str(_latitude))
        # _long_text.setText(str(_longitude))
        # _tz_text.setText(str(_time_zone))
        print(_place_name,_latitude,_longitude,_time_zone)
        return _place_name,_latitude,_longitude,_time_zone
    else:
        msg = place_name+" could not be found in OpenStreetMap.\nTry entering latitude and longitude manually.\nOr try entering nearest big city"
        print(msg)
        return None
        # QMessageBox.about(self,"City not found",msg)
    #     _lat_text.setText('')
    #     _long_text.setText('')
    # _reset_place_text_size()


def get_prediction_details(jd_at_dob,place,language=const._DEFAULT_LANGUAGE):
    prediction_msgs = get_prediction_resources(language=language)
    print('prediction keys',prediction_msgs.keys())
    results = {}
    planet_positions = charts.rasi_chart(jd_at_dob, place)
    results1 = _get_general_lagna_rasi_prediction(jd_at_dob,place,prediction_msgs,language=language)
    print('results1',results1)
    results.update(results1)
    results2 = _get_planets_in_houses_prediction(planet_positions,prediction_msgs)
    results.update(results2)
    results3 = _get_lords_in_houses_prediction(planet_positions,prediction_msgs)
    results.update(results3)
    return results

def get_prediction_resources(language='en'):
    """
        get resources from prediction_msgs_<lang>.txt
        @param language: Two letter language code. en, hi, ka, ta, te
        @return json strings from the resource file as dictionary 
    """
    json_file = _lang_path + const._DEFAULT_PREDICTION_JSON_FILE_PREFIX+language+'.json'
    print('JSON_FILE_PATH', json_file)
    f = open(json_file,"r",encoding="utf-8")
    msgs = json.load(f)
    return msgs

def get_all_predictions(day, month,year, _tob_text, place_name='Indore, India'):
 
    birth_date = drik.Date(int(year),int(month),int(day))
    # user_age = min(datetime.now().year - birth_date.year, const.annual_maximum_age) + 1
    dob = (int(year),int(month),int(day))
    tob = tuple([int(x) for x in _tob_text.split(':')])
    print('*DOB', dob)
    print('*TOB', tob)

    _birth_julian_day = utils.julian_day_number(dob, tob)
    print('*Julian Day', _birth_julian_day)
    _place_name,_latitude,_longitude,_time_zone= _get_location(place_name)
    place = drik.Place(_place_name,_latitude,_longitude,_time_zone)
    print('*Place', place)
    results = get_prediction_details(_birth_julian_day,place,language='en')

    return results['Janma rasi_2']
        

