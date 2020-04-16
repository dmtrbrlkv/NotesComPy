from flask import request, jsonify
import utils


app, config, base_url, databases, separator = utils.init()

app.logger.info(f"Start with config: {config}")

@app.route(base_url + '/')
def index():
    return_databases = {}
    for dbname, config in databases.items():
        return_config = {}

        method_config = databases[dbname]["methods"]
        doc_info_config = databases[dbname]["doc_info"]

        if "view" in method_config:
            method_config["view"] = [v for v in method_config["view"]]

        return_config["methods"] = method_config
        return_config["doc_info"] = doc_info_config

        return_databases[dbname] = return_config

    return jsonify(return_databases)


@app.route(base_url + '/<dbname>/view/<viewname>')
def view(dbname, viewname):
    check = utils.check_method(dbname, "view", databases)

    if check:
        return check, 403

    view_config = databases[dbname]["methods"]["view"]
    if viewname not in view_config:
        return f"Not available view {viewname}", 403

    try:
        db = utils.get_db(dbname, databases)
    except:
        app.logger.exception(dbname)
        return f"Database {dbname} temporary not available",500

    view = db.get_view(view_config[viewname])
    if not view:
        app.logger.error(f"View {view_config[viewname]} from {db} not available")
        return f"View {viewname} temporary not available", 500

    if "keys" in request.headers:
        keys = request.headers["keys"]
        keys = keys.split(separator)
    else:
        keys = None

    fields, properties, formulas = utils.get_FPF(dbname, request.headers, databases, separator)

    if keys:
        try:
            col = view.get_all_documents_by_key(keys)
        except:
            app.logger.exception(" * Bad request")
            return f"Bad request, check keys", 400
        data = col.get_values(fields=fields, properties=properties, formulas=formulas)
    else:
        data = view.get_values()

    return jsonify(data)


@app.route(base_url + '/<dbname>/search')
def search(dbname):
    check = utils.check_method(dbname, "search", databases)

    if check:
        return check, 403

    if "search_formula" in request.headers:
        search_formula = request.headers["search_formula"]
    else:
        return f"Bad request, search formula not specified", 400

    try:
        db = utils.get_db(dbname, databases)
    except:
        app.logger.exception(dbname)
        return f"Database {dbname} temporary not available",500

    try:
        col = db.search(search_formula)
    except:
        app.logger.exception(" * Bad request")
        return f"Bad request, check search formula", 400

    fields, properties, formulas = utils.get_FPF(dbname, request.headers, databases, separator)

    try:
        data = col.get_values(fields=fields, properties=properties, formulas=formulas)
        return jsonify(data)
    except:
        app.logger.exception(" * Bad request")
        return f"Bad request, check properties and formulas", 400


@app.route(base_url + '/<dbname>/document/<doc_id>')
def document(dbname, doc_id):
    check = utils.check_method(dbname, "document", databases)

    if check:
        return check, 403

    try:
        db = utils.get_db(dbname, databases)
    except:
        app.logger.exception(dbname)
        return f"Database {dbname} temporary not available",500

    doc = db.get_document_by_unid(doc_id)

    if doc:
        fields, properties, formulas = utils.get_FPF(dbname, request.headers, databases, separator)

        try:
            data = doc.get_values(fields=fields, properties=properties, formulas=formulas)
            return jsonify(data)
        except:
            app.logger.exception(" * Bad request")
            return f"Bad request, check properties and formulas", 400

    return f"Document {doc_id} not available", 404


@app.route(base_url + '/<dbname>')
def db_info(dbname):
    if dbname not in databases:
        return "Not available db " + dbname

    try:
        db = utils.get_db(dbname, databases)
    except:
        app.logger.exception(dbname)
        return f"Database {dbname} temporary not available",500

    res = {"Documents": db.all_documents.count, "Size": db.size}
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)