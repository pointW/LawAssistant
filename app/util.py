from flask import jsonify


def json_data(code, data=None):
    if code == 1:
        if data:
            return jsonify({'code': 1, 'data': data})
        else:
            return jsonify({'code': 1})
    else:
        return jsonify({'code': 0, 'msg': data})

