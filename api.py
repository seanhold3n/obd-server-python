import db
from flask import request, Response


def get_latlong_json():
    # Get speed and timestamp data from database
    db.getCur().execute(
        """SELECT unix_timestamp,latitude,longitude from obdreadings ORDER BY unix_timestamp DESC LIMIT 100;""")  # LIMIT 500 OFFSET 100;""")

    # Start with callback handler
    callback_str = request.args.get('callback')
    if callback_str is not None:
        result_str = callback_str
        print(callback_str)
    else:
        result_str = 'callback'

    result_str += '(['

    # TODO consider jsonify here
    for record in db.getCur():
        unix_time = record[0]
        lat = record[1]
        long = record[2]
        result_str += '[{},{},{}],\n'.format(unix_time, lat, long)

    # Append end part
    result_str += ']);'

    # Create and send response
    response = Response(result_str)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
