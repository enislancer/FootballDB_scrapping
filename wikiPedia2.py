from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import urllib
from googletrans import Translator
import json

from geopy.geocoders import Nominatim


def findInfo(url):
    sea_level, people, year, founding_year, link, area, region = "", "", "", "", "", "", ""
    try:
        html = request.urlopen(url)
    except(urllib.error.HTTPError):
        output = [" "] * 8
        return output

    soup = BeautifulSoup(html, "html.parser")

    for table in soup.find_all('table', class_="infobox geography vcard"):
        rowNumber = 1
        areaIndex = 0
        populationIndex = 0
        for row in table('tr'):
            # find the city website address
            if 'Website' in row.text:
                for avalue in row.find_all("a"):
                    if "href" in avalue.attrs:
                        link = avalue.attrs["href"]

            if 'Elevation' in row.text:
                sea_level = row.find_all('td')
                sea_level = sea_level[0].text

            if 'Area' in row.text:
                areaIndex = rowNumber
            if 'Total' in row.text and areaIndex + 1 == rowNumber:
                area = row.find_all('td')[0].text

            if 'State' in row.text or 'state' in row.text or 'Province' in row.text or 'Region' in row.text:
                region = row.find_all('td')[0].text

            if 'Settled by' in row.text:
                founding_year = row.find_all('td')[0].text.split('[')[0]

            if 'Population' in row.text:
                populationIndex = rowNumber
                year = row.text.split('(')[1].split(')')[0] if row.text.split("Population")[1] is not "" else " "

            if 'Total' in row.text and populationIndex + 1 == rowNumber:
                people = row.find_all('td')[0].text

            rowNumber += 1

        return sea_level, people, year, founding_year, link, area, region


def findFiveCountryName(cityName):
    translator = Translator()
    in_french = translator.translate(cityName, dest='fr')
    in_russia = translator.translate(cityName, dest='ru')

    in_chines = translator.translate(cityName, dest='zh-CN')

    in_garman = translator.translate(cityName, dest='de')

    in_spanish = translator.translate(cityName, dest='es')

    return [in_garman.text, in_spanish.text, in_french.text, in_russia.text, in_chines.text]


if __name__ == '__main__':

    if len(sys.argv) != 5:
        sys.exit("Not enough args")

    city_id  = str(sys.argv[1])
    city_name = str(sys.argv[2])
    lat = str(sys.argv[3])
    long = str(sys.argv[4])

    # city_id, city_name, lat, long = '1', 'Aachen', '50.77666667', '6.08361111'  # '5426', 'Zurmat', '33.43778000', '69.02774000'

    geolocator = Nominatim(user_agent="my-application", timeout=3)
    loc_dict_en = geolocator.reverse(lat + ',' + long, language='en').raw

    loc_name = loc_dict_en['address']['city'] if 'city' in loc_dict_en['address'] else "" + loc_dict_en['address'][
        'town'] if 'town' in loc_dict_en['address'] else "" + loc_dict_en['address'][
        'state_district'] if 'state_district' in loc_dict_en['address'] else ""

    # if city_name() != loc_name.replace(" ", "_").lower():
    #     sys.exit("City name and coordinates do not match...")

    query_original = loc_name
    query = query_original.replace(" ", "_")
    url = "https://en.wikipedia.org/wiki/" + ''.join(query)

    German, Spanish, French, Russian, Chinese = findFiveCountryName(query_original)

    sea_level, people, year, founding_year, link, area, region = findInfo(url)

    page_titles = query
    url = ('https://en.wikipedia.org/w/api.php'
           '?action=query'
           '&prop=info'
           '&inprop=subjectid'
           '&titles=' + ''.join(query) +
           '&format=json')
    json_response = requests.get(url).json()
    # print(json_response)

    page_id = [page_id for page_id, page_info in json_response['query']['pages'].items()]
    page_id = page_id[0]


    ##convert object to json
    myDictObj = {"City_id": city_id, "German": German, 'Spanish': Spanish, 'Frence': French, 'Russian': Russian,
                 'Chinese': Chinese, 'sea_level': sea_level.replace("\u00a0", " "),
                 'people': people, 'year': year, 'founding_year': founding_year, 'website': link,
                 'wiki_pageNum': page_id, 'Surface': area.replace("\u00a0", " "), 'Region': region}

    json_output = json.dumps(myDictObj, sort_keys=True, indent=3)
    print("Json output =", json_output)
