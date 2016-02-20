#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from string import Template
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
    html = Template('''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
    <h2 class="text-center">${texto}</h2>
    <p class="text-center">${legenda}</p>
    ''')
    with open(arquivo, encoding = "ISO-8859-1") as matriculacsv:
        reader = csv.DictReader(matriculacsv)
        for linha in reader:
            if linha['cpf'] == cpf:
                return html.substitute(
                                texto='Sua nova matrícula: <pre class="bg-success">%s</pre>' % linha['matricula'],
                                legenda='(Cadastre-se <a href=http://sigaa.ifal.edu.br/sigaa/public/cadastro/discente.jsf>aqui</a>)'
                            )
                break
        else:
            return html.substitute(
                            texto='CPF não encontrado.',
                            legenda=' Contate o coordenador (<code>marcilio@ifal.edu.br</code>).'
                        )

if __name__ == '__main__':
    app.debug = True
    app.use_reloader = True
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.run(host='0.0.0.0', port=8080)
