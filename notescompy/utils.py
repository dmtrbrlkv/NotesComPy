from . import session, document, const
import datetime


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
        ndt = session.Session().CreateDateTime(value.isoformat())
        ndt.SetAnyTime()
        v = ndt
    elif isinstance(value, datetime.time):
        ndt = session.Session().CreateDateTime(value.isoformat())
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


def evaluate(formula, doc=None, as_text=False, sep=", "):
    handle = doc.handle if isinstance(doc, document.Document) else doc
    value = session.Session().handle.Evaluate(formula, handle)

    values = [convert_item_value(v) for v in value]
    if not as_text:
        return values

    values = [item_value_to_str(v) for v in values]
    return sep.join(values)