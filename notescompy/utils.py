from .session import Session
from .document import Document


def evaluate(formula, doc=None):
    handle = doc.handle if isinstance(doc, Document) else doc
    return Session().handle.Evaluate(formula, handle)