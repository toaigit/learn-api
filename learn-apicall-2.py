# EXAMPLE API CALL WITH HEADER AND PAYLOAD
import requests

API_KEY = 'a4686973206973206d7920415049204b6579'
USER_AGENT = 'Dataquest'

headers = {
    'user-agent': USER_AGENT
}

payload = {
    'api_key': API_KEY,
    'method': 'chart.gettopartists',
    'format': 'json'
}

r = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
print (r.status_code)

#  write a subroutine for reuse - notice mulple line of payload line
def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

#   print - need to convert JSON python object to text with json.dumps
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

r = lastfm_get({ 'method': 'chart.gettopartists' })
print (r.status_code)

jprint(r.json())

{
    "artists": {
        "@attr": {
            "page": "1",
            "perPage": "50",
            "total": "2901036",
            "totalPages": "58021"
        },
        "artist": [
            {
                "image": [
                    {
                        "#text": "https://lastfm-img2.akamaized.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "small"
                    },
                    {
                        "#text": "https://lastfm-img2.akamaized.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "medium"
                    },
                    {
                        "#text": "https://lastfm-img2.akamaized.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "mega"
                    }
                ],
                "listeners": "1957174",
                "mbid": "b7539c32-53e7-4908-bda3-81449c367da6",
                "name": "Lana Del Rey",
                "playcount": "232808939",
                "streamable": "0",
                "url": "https://www.last.fm/music/Lana+Del+Rey"
            },
            {
                "image": [
                    {
                        "#text": "https://lastfm-img2.akamaized.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "small"
                    },
                    {
                        "#text": "https://lastfm-img2.akamaized.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "extralarge"
                    },
                    {
                        "#text": "https://lastfm-img2.akamaized.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                        "size": "mega"
                    }
                ],
                "listeners": "588883",
                "mbid": "",
                "name": "Billie Eilish",
                "playcount": "35520548",
                "streamable": "0",
                "url": "https://www.last.fm/music/Billie+Eilish"
           }
        ]
    }

jprint(r.json()['artists']['@attr'])

    "artists": {
        "@attr": {
            "page": "1",
            "perPage": "50",
            "total": "2901036",
            "totalPages": "58021"
        }
