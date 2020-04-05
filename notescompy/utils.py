from . import session, document, const
import datetime
import json


def item_value_to_str(value):
    if isinstance(value, str):
        v = value
    elif isinstance(value, (int, float)):
        v = str(value)
    elif isinstance(value, datetime.datetime):
        v = value.isoformat()
    else:
        v = str(value)
    return v


def convert_item_value(value):
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        ndt = session.Session().notes_property.CreateDateTime(value.isoformat())
        ndt.SetAnyTime()
        v = ndt
    elif isinstance(value, datetime.time):
        ndt = session.Session().notes_property.CreateDateTime(value.isoformat())
        ndt.SetAnyDate()
        v = ndt
    elif isinstance(value, const.PyWinDatetime):
        v = datetime.datetime(
            year=value.year,
            month=value.month,
            day=value.day,
            hour=value.hour,
            minute=value.minute,
            second=value.second
        )
    else:
        v = value

    return v


def evaluate(formula, doc=None, no_list=False, sep=None):
    handle = doc.handle if isinstance(doc, document.Document) else doc
    value = session.Session().handle.Evaluate(formula, handle)

    values = [convert_item_value(v) for v in value]

    if sep is None:
        if no_list and len(values) == 1:
            values = values[0]
        return values

    values = [item_value_to_str(v) for v in values]
    return sep.join(values)


def to_json(values, default, sort_keys, indent):
    return json.dumps(values, default=default, sort_keys=sort_keys, indent=indent)


def save_to_json(values, fp, default=str, sort_keys=True, indent=4):
    if isinstance(fp, str):
        with open(fp, mode="w") as f:
            json.dump(values, f, default=default, sort_keys=sort_keys, indent=indent)
    else:
        json.dump(values, fp, default=default, sort_keys=sort_keys, indent=indent)