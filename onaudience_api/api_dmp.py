import requests
import json
import time


class DatapointAssignmentController:
    """
    Class working along with panel OnAudience API to assign datapoints to users

    This class is created to assign different types of datapoints and attributes
    (if needed) to users in case of custom datapoint assignments. There is a possibility
    to assign regular datapoint events, datapoint events containing number attributes,
    but also datapoint events containig string attributes.

    ...

    Attributes
    ----------
    username : str
        Valid email adress used to log into panel.onaudience.com

    password : str
        Valid password used to log into panel.onaudience.com

    cmPartnerId : int
        CloudTechnologies data supplier Id, as for internal use default value
        set as '1' - CloudTechnologies Id

    content_type : str
        String sent along with a file indicating the type of the file.
        Fixed value set in API. Default as 'application/json' (do not change)

    response_content_type : str
        No clue, but fixed in API

    Methods
    -------

    get_headers_with_token(self)
        Takes as input panel OnAudience credentials (username, password),
        post it to API, receives token authorization and returns with
        entire header.

    assign_event_to_user(self, userId, datapoint)
        Takes as input list of userId's and int-like already existing in panel
        datapoint which is about to be assigned to those id's without any extra
        information (like attributes).

    assign_events_to_user(self, userId, datapointsList)
        Takes as input list of userId's and list of already existing in panel
        datapoints that are meant to be assigned to those datapoints. Similar
        to mentioned above method, but use in case of assigning MULTIPLE
        number of datapoints without any extra information (like attributes).

    assign_number_attribute(self, userId, datapoint, attribute_value)
        Takes as input list of userId's, int-like already existing datapoint
        and int-like attribute value that are meant to be assigned to listed
        id's

    assign_number_attributes(self, userId, datapointsList, attribute_values)
        Takes as input list of userId's, list of already existing datapoints
        and list of number attribiutes (consecutively assigned to datapoints)
        that are meant to be assigned to given list of id's

    assign_string_attribute(self, userId, datapoint, string_value)
        Takes as input list of userId's, int-like already existing datapoint
        and str-like attribute value that are meant to be assigned to given
        id's

    assign_string_attributes(self, userId, datapointsList, string_values)
        Takes as input list of userId's, list of already existing datapoints
        and list of str-like attributes (consecutively assigned to datapoints)
        that are meant to be assigned to given list of id's.

    """

    def __init__(self, username, password, cmPartnerId=1,
                 content_type='application/json', response_content_type='*/*'):
        assert isinstance(username, str)
        assert isinstance(password, str)
        assert isinstance(cmPartnerId, int)
        assert isinstance(content_type, str)
        assert isinstance(response_content_type, str)

        # username and password used to log into panel.onaudience.com
        self.username = username
        self.password = password
        self.cmPartnerId = cmPartnerId
        self.content_type = content_type
        self.response_content_type = response_content_type

    def get_headers_with_token(self):
        ''' Post credentials to API and returns header with authorization token

        Description
        -----------
        Results in dict-like format placed in RAM. Function mainly used by other
        functions.

        '''

        # link to dmp API
        url = 'https://dmp-api.cloudtechnologies.dev/login?email={}&password={}'
        # post credentials to API (usign requests library)
        r = requests.post(url.format(self.username, self.password))
        # getting and saving authorization token from header json-like file
        token = r.headers.get('X-Auth-Token')

        # creates returned header needed for below functions
        headers = {'accpet': self.response_content_type,
                   'X-Auth-Token': token,
                   'Content-Type': self.content_type}

        return headers

    def tohex(self, val, nbits):
        h = hex((val + (1 << nbits)) % (1 << nbits))[2:]
        return h.zfill(16)

    def assign_event_to_user(self, userId, datapoint):
        ''' Assigning datapoint to list of userId's

        Description
        -----------
        Assigning already existing single datapoint to provided list of users.
        '''
        assert isinstance(userId, list)
        assert isinstance(datapoint, int)

        # converting id's from decimal to heximal format (as this one is used in DMP)
        h_userId = [self.tohex(val, 63) for val in userId]
        # getting header by executing previously written function
        headers = self.get_headers_with_token()
        # declaring payload format
        payload = {'body': {'id': datapoint}}
        url = 'https://dmp-api.cloudtechnologies.dev/event?cmPartnerId={}&userId={}'

        # assigning payload to every userId (in hex format)
        for i in h_userId:
            r = requests.post(url.format(self.cmPartnerId, i),
                              headers=headers,
                              data=json.dumps(payload))
            print("{} : {}".format(i, r))
            time.sleep(0.8)

    def assign_events_to_user(self, userId, datapointsList):
        assert isinstance(userId, list)
        assert isinstance(datapointsList, list)

        # converting id's from decimal to heximal format (as this one is used in DMP)
        h_userId = [self.tohex(val, 63) for val in userId]
        # creating list containing dict-like format datapoints
        key_datapoints = []
        for i in datapointsList:
            key_datapoints.append({"id": i})

        # getting header by executing previously written function
        headers = self.get_headers_with_token()
        # declaring payload format
        # key_datapoints - list of dicts containing datapoints
        payload = {'body': key_datapoints}
        url = 'https://dmp-api.cloudtechnologies.dev/events?cmPartnerId={}&userId={}'

        # assigning payload to every userId (in hex format)
        for i in h_userId:
            r = requests.post(url.format(self.cmPartnerId, i),
                              headers=headers,
                              data=json.dumps(payload))
            print("{} : {}".format(i, r))
            time.sleep(0.8)

    def assign_number_attribute(self, userId, datapoint,
                                attribute_value):
        assert isinstance(userId, list)
        assert isinstance(datapoint, int)
        assert isinstance(attribute_value, int)

        # converting id's from decimal to heximal format (as this one is used in DMP)
        h_userId = [self.tohex(val, 63) for val in userId]
        url = 'https://dmp-api.cloudtechnologies.dev/number-attribute?cmPartnerId={}&userId={}'
        # getting header by executing previously written function
        headers = self.get_headers_with_token()
        # declaring payload format
        payload = {'body': {'id': datapoint, 'value': attribute_value}}

        # assigning payload to every userId (in hex format)
        for i in h_userId:
            r = requests.post(url.format(self.cmPartnerId, i),
                              headers=headers,
                              data=json.dumps(payload))
            print("{} : {}".format(i, r))
            time.sleep(0.8)

    def assign_number_attributes(self, userId, datapointsList,
                                 attribute_values):
        assert isinstance(userId, list)
        assert isinstance(datapointsList, list)
        assert isinstance(attribute_values, list)

        # converting id's from decimal to heximal format (as this one is used in DMP)
        h_userId = [self.tohex(val, 63) for val in userId]
        url = 'https://dmp-api.cloudtechnologies.dev/number-attributes?cmPartnerId={}&userId={}'
        # creating list containing dict-like format datapoints and number attribute values
        # assigning consecutively attribute to datapoint
        key_datapoints_values = []
        for i in range(len(datapointsList)):
            key_datapoints_values.append({'id': datapointsList[i],
                                          'value': attribute_values[i]})

        # getting header by executing previously written function
        headers = self.get_headers_with_token()
        # declaring payload format
        payload = {'body': key_datapoints_values}

        # assigning payload to every userId (in hex format)
        for i in h_userId:
            r = requests.post(url.format(self.cmPartnerId, i),
                              headers=headers,
                              data=json.dumps(payload))
            print("{} : {}".format(i, r))
            time.sleep(0.8)

    def assign_string_attribute(self, userId, datapoint,
                                string_value):
        assert isinstance(userId, list)
        assert isinstance(datapoint, int)
        assert isinstance(string_value, str)

        # converting id's from decimal to heximal format (as this one is used in DMP)
        h_userId = [self.tohex(val, 63) for val in userId]
        url = 'https://dmp-api.cloudtechnologies.dev/string-attribute?cmPartnerId={}&userId={}'
        # getting header by executing previously written function
        headers = self.get_headers_with_token()
        # declaring payload format
        payload = {'body': {'id': datapoint, 'value': string_value}}

        # assigning payload to every userId (in hex format)
        for i in h_userId:
            r = requests.post(url.format(self.cmPartnerId, i),
                              headers=headers,
                              data=json.dumps(payload))
            print("{} : {}".format(i, r))
            time.sleep(0.8)

    def assign_string_attributes(self, userId, datapointsList,
                                 string_values):
        assert isinstance(userId, list)
        assert isinstance(datapointsList, list)
        assert isinstance(string_values, list)

        # converting id's from decimal to heximal format (as this one is used in DMP)
        h_userId = [self.tohex(val, 63) for val in userId]
        url = 'https://dmp-api.cloudtechnologies.dev/string-attributes?cmPartnerId={}&userId={}'
        # creating list containing dict-like format datapoints and string attribute values
        # assigning consecutively attribute to datapoint
        key_datapoints_strings = []
        for i in range(len(datapointsList)):
            key_datapoints_strings.append({'id': datapointsList[i],
                                           'value': string_values[i]})

        # getting header by executing previously written function
        headers = self.get_headers_with_token()
        payload = {'body': key_datapoints_strings}

        # assigning payload to every userId (in hex format)
        for i in h_userId:
            r = requests.post(url.format(self.cmPartnerId, i),
                              headers=headers,
                              data=json.dumps(payload))
            print("{} : {}".format(i, r))
            time.sleep(0.8)
