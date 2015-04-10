from json import loads as json_loads
from time import time
from urllib import urlencode
from urllib2 import urlopen

from bottle import route, run, get, static_file
from web import t
from web import html
from re import compile

import configuration

rex = compile('In current traffic: ([0-9]+) min')

@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static')

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static')

def get_forecast(lat, lon, name):
    return t.iframe(
        id="forecast_embed",
        type="text/html",
        frameborder="0",
        height="200",
        width="100%",
        src="http://forecast.io/embed/#lat={}&lon={}&name={}".format(
            lat,
            lon,
            name,
            ),
        )

def get_drive_times():
    def getMins(orig, dest):
        html = urlopen('https://www.google.com/maps/dir/{}/{}'.format(
            orig, dest)).read()
        mins = int(rex.search(html).group(1))
        def getClasses():
            yield 'mins'
            yield (
                'min-red' if mins >= 40 else
                'min-yellow' if mins >= 32 else
                'min-green'
                )
        return t.span(
            '{} mins'.format(mins),
            _class=' '.join(getClasses()),
            )
    def arrows():
        return t.div('>>>', style='color: #ddd;')
    return t.div(
        t.div('home'),
        arrows(),
        t.div(getMins(configuration.HOME, configuration.WORK)),
        arrows(),
        t.div('work'),
        arrows(),
        t.div(getMins(configuration.WORK, configuration.HOME)),
        arrows(),
        t.div('home', _class='tight'),
        _class='flex-row',
        )

@route('/')
def index():
    return html(
        t.head(
            t.meta(**{
                'http-equiv': "refresh",
                'content': str(60 * 5),
                }),
            t.script(
                type="text/javascript",
                src="https://maps.googleapis.com/maps/api/js?key={}".format(
                    configuration.GOOGLE_API_KEY),
                ),
            t.script(
                type="text/javascript",
                src='jquery.js',
                ),
            t.script(
                type="text/javascript",
                src='moment.js',
                ),
            t.script(
                type="text/javascript",
                src='main.js',
                ),
            t.link(
                rel='stylesheet',
                type='text/css',
                href='flex.css',
                ),
            ),
        t.body(
            t.div(
                t.div(
                    t.div(
                        get_forecast(
                            configuration.WEATHER_LAT,
                            configuration.WEATHER_LON,
                            configuration.WEATHER_LOC,
                            ),
                        _class='tight',
                        ),
                    t.iframe(
                        src=configuration.CAL_IFRAME,
                        style="border: 0",
                        width="100%",
                        height="100%",
                        frameborder="0",
                        scrolling="no",
                        ),
                    _class='flex-col',
                    ),
                t.div(
                    t.div('&nbsp;',  _class='clock tight'),
                    t.div(
                        get_drive_times(),
                        _class='tight',
                        ),
                    t.div(
                        'map',
                        id='map-canvas',
                        ),
                    _class='tight flex-col',
                    ),
                _class='flex-expand flex-row',
                ),
            ),
        )

run(host='localhost', port=configuration.PORT, reloader=configuration.DEBUG)
