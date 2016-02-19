#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': request.url + ': ' + str(error),
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/novamatricula/<cpf>', methods = ['GET'])
def nova_matricula(cpf):
    arquivo = 'novamatricula.csv'
    with open(arquivo, encoding = "ISO-8859-1") as matriculacsv:
        reader = csv.DictReader(matriculacsv)
        for linha in reader:
            if linha['cpf'] == cpf:
                return jsonify({"matricula":linha['matricula']})
    return not_found()

if __name__ == '__main__':
    app.debug = True
    app.use_reloader = True
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.run(host='0.0.0.0', port=8080)
