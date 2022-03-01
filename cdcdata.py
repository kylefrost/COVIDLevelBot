import json
import datetime
import logging
import credentials

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

class CDCData:
    def get_current_version(self):
        f = open(credentials.cdcfile)
        cdcdata = json.load(f)
        data_version = datetime.datetime.strptime(cdcdata['dataFileName'].partition('.')[0][-8:], '%Y%m%d').strftime('%b %-d, %Y')
        f.close()
        return data_version

    def get_current_status(self, county, state):
        if len(state) == 2:
            logger.info("Converting " + state + " to full name.")
            state = self.map_abb(state.upper())

        logger.info("Getting data for " + county + ", " + state) 

        f = open(credentials.cdcfile)
        cdcdata = json.load(f)
        i = 0
        for c in cdcdata['data']:
            if c['County'] == county + ', ' + state + ', US':
                break
            else:
                i = i + 1

        countydata = cdcdata['data'][i]['COVID-19 Community Level']
        f.close()
        return countydata

    def map_abb(self, abb):
        us_state_to_abbrev = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "District of Columbia": "DC",
            "American Samoa": "AS",
            "Guam": "GU",
            "Northern Mariana Islands": "MP",
            "Puerto Rico": "PR",
            "United States Minor Outlying Islands": "UM",
            "U.S. Virgin Islands": "VI",
        }

        # invert the dictionary
        abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

        return abbrev_to_us_state[abb]
