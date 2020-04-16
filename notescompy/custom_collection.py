from . import iterdoc, utils, collection, document, view


class SaveExeption(Exception):
    def __init__(self, msg, not_restored, not_removed):
        self.msg = msg
        self.not_restored = not_restored
        self.not_removed = not_removed

class CustomCollection():
    def __init__(self, expanded=False):
        self._col = []
        self.expanded = expanded

    def __str__(self):
        return f"{self.count} documents"

    @property
    def count(self):
        count = 0
        for obj in self._col:
            if isinstance(obj, document.Document):
                count += 1
            if isinstance(obj, collection.DocumentCollection):
                count += obj.count
            if isinstance(obj, view.View):
                count += obj.entry_count
        return count

    def __iter__(self):
        for obj in self._col:
            if isinstance(obj, document.Document):
                yield obj
            if isinstance(obj, (collection.DocumentCollection, view.View)):
                for doc in obj:
                    yield doc


    def append(self, obj):
        if self.expanded:
            if isinstance(obj, document.Document):
                self._col.append(obj)
            if isinstance(obj, (collection.DocumentCollection, view.View)):
                self._col.extend(obj)
        else:
            self._col.append(obj)

    def remove(self, obj):
        self._col.remove(obj)


    def GetValues(self, fields=None, properties=None, formulas=None, formulas_names=None, no_list=False, sep=None):
        res = {}

        for doc in self:
            doc_res = doc.get_values(fields, properties, formulas, formulas_names, no_list, sep)
            res[doc.UniversalID] = doc_res

        return res

    def to_json(self, fields=None, properties=None, formulas=None, formulas_names=None, no_list=True, sep=None, default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, no_list, sep)
        return utils.to_json(values, default, sort_keys, indent)

    def save_to_json(self, fp, fields=None, properties=None, formulas=None, formulas_names=None, no_list=True, sep=None, default=str, sort_keys=True, indent=4):
        values = self.GetValues(fields, properties, formulas, formulas_names, no_list, sep)
        utils.save_to_json(values, fp, default, sort_keys, indent)

    def save(self):
        saved = []

        for doc in self:
            if not doc.IsNewNote:
                doc.create_backup()

        try:
            for doc in self:
                doc.Save()
                saved.append(doc)
        except Exception as e:
            for_remove = []
            for_restore = []
            not_restored = []
            not_removed = []

            for doc in saved:
                if doc.has_backup:
                    doc.restore_backup()
                    for_restore.append(doc)
                else:
                    for_remove.append(doc)

            for doc in for_restore:
                try:
                    doc.Save()
                except:
                    not_restored.append(doc)

            for doc in for_remove:
                try:
                    doc.Remove(True)
                except:
                    not_removed.append(doc)

            msg = ""
            if not_restored:
                msg = "Not all modified documents restored ("
                for doc in not_restored:
                    msg = msg + " " + str(doc) + ", "
                msg = msg + " )"

            if not_removed:
                if msg:
                    msg = msg + ", not all new documents removed("
                msg = "Not all new documents removed ("

                for doc in not_removed:
                    msg = msg + " " + str(doc) + ", "
                msg = msg + " )"

            if not not_restored and not not_removed:
                msg = "All documents restored"

            raise SaveExeption(msg, not_restored, not_removed) from e

    def stamp_all(self, field_name, value):
        if not self.expanded:
            self._expand()

        for doc in self:
            doc.ReplaceItemValue(field_name, value)

    def _expand(self):
        if not self.expanded:
            col = [doc for doc in self]
            self._col = col
            self.expanded = True