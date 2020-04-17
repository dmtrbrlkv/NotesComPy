from . import session

class IterDocMixin:
    def __init__(self, first_func="GetFirstDocument:get_first_document", next_func="GetNextDocument:get_next_document", iter_cls=None):
        self._current_handle = None
        self._first_func = first_func.split(":")[0]
        self._next_func = next_func.split(":")[0]
        if iter_cls is None:
            from .document import Document
            self._iter_cls = Document
        else:
            self._iter_cls = iter_cls

        self.__dict__[first_func.split(":")[0]] = self._get_first
        self.__dict__[next_func.split(":")[0]] = self._get_next
        self.__dict__[first_func.split(":")[1]] = self._get_first
        self.__dict__[next_func.split(":")[1]] = self._get_next

    def _get_first(self):
        iterator = iter(self)
        return next(iterator)

    def _get_next(self):
        try:
            return next(self)
        except StopIteration:
            return None



    def __iter__(self):
        self._current_handle = None
        return self

    def __next__(self):
        if not self._current_handle:
            first_func = getattr(self.handle, self._first_func)
            if session.Session().session_type == session.SessionType.LotusNotesSession:
                doc_handle = first_func()
            else:
                doc_handle = first_func
        else:
            next_func = getattr(self.handle, self._next_func)
            doc_handle = next_func(self._current_handle.handle)
        if not doc_handle:
            self._current_handle = None
            raise StopIteration
        self._current_handle = self._iter_cls(doc_handle)
        return self._current_handle