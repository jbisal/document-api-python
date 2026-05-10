from tableaudocumentapi.utils import _clean_aggregated_column_names


class Encoding(object):
    """A class representing one mark encoding on a worksheet pane.

    Wraps a child element of <pane>/<encodings> (e.g. <color>, <text>,
    <tooltip>, <size>, <lod>, <label>, <shape>, <detail>, <path>).
    Channel name is pass-through from Tableau, so any tag emitted under
    <encodings> is accepted.
    """

    def __init__(self, encoding_xml):
        self._xml = encoding_xml
        self._channel = encoding_xml.tag
        self._column = encoding_xml.get('column')

    @property
    def xml(self):
        return self._xml

    @property
    def channel(self):
        """The visual channel tag name as emitted by Tableau."""
        return self._channel

    @property
    def column(self):
        """The raw column reference (e.g. '[ds].[none:Country:nk]')."""
        return self._column

    @property
    def datasource(self):
        """Datasource name extracted from the column reference, or None."""
        if not self._column:
            return None
        ds, _ = _clean_aggregated_column_names(self._column)
        return ds

    @property
    def field(self):
        """Field name extracted from the column reference, or None."""
        if not self._column:
            return None
        _, field = _clean_aggregated_column_names(self._column)
        return field
