from argparse import ArgumentParser
from notescompy import session
import logging
from flask import Flask
import json


def get_config():
    ap = ArgumentParser()
    ap.add_argument("-c", "--config", action="store", default="config.json")
    ap.add_argument("-p", "--password", action="store", default="")

    options = ap.parse_args()
    with open(options.config) as cf:
        config = json.load(cf)
    if options.password:
        config["password"] = options.password
    return config

def check_method(dbname, method, databases):
    if dbname not in databases:
        return "Not available db " + dbname

    method_config = databases[dbname]["methods"]

    if method not in method_config or not method_config[method]:
        return f"{method.capitalize()} method not available"

    return ""


def get_db(dbname, databases):
    db_config = databases[dbname]
    db = session.open_database(db_config["server"], db_config["filepath"])
    if not db.is_open:
        raise RuntimeError(f"{dbname} has not been opened yet")
    return db


def get_FPF(dbname, headers, databases, separator):
    doc_info_config = databases[dbname]["doc_info"]
    if "fields" in doc_info_config and doc_info_config["fields"] and "fields" in headers:
        fields = headers["fields"]
        fields = fields.split(separator)
    else:
        fields = None

    if "properties" in doc_info_config and doc_info_config["properties"] and "properties" in headers:
        properties = headers["properties"]
        properties = properties.split(separator)
    else:
        properties = None

    if "formulas" in doc_info_config and doc_info_config["formulas"] and "formulas" in headers:
        formulas = headers["formulas"]
        formulas = formulas.split(separator)
    else:
        formulas = None

    return fields, properties, formulas


def init():
    config = get_config()
    if config["global_session"]:
        s = session.Session(config["password"])
    base_url = config["url"]
    databases = config["databases"]
    separator = config["separator"]
    app = Flask(__name__)
    logging.basicConfig(filename=config["log"], level=logging.INFO if not config["debug"] else logging.DEBUG,
                        format=config["log_format"], datefmt=config["log_date"])

    if "password" in config:
        del config["password"]
    return app, config, base_url, databases, separator
