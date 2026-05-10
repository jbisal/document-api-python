class Sort(object):
    """A class representing a sort specification on a worksheet.

    Wraps one of three Tableau sort tags: <computed-sort>, <manual-sort>,
    or <shelf-sort-v2>.
    """

    def __init__(self, sort_xml):
        self._xml = sort_xml
        self._sort_type = sort_xml.tag

    @property
    def xml(self):
        return self._xml

    @property
    def sort_type(self):
        """'computed-sort', 'manual-sort', or 'shelf-sort-v2'"""
        return self._sort_type

    @property
    def column(self):
        """The dimension being sorted."""
        return self._xml.get('column') or self._xml.get('dimension-to-sort')

    @property
    def direction(self):
        """'ASC' or 'DESC'"""
        return self._xml.get('direction')

    @property
    def sort_by(self):
        """The measure used for sorting (computed-sort and shelf-sort-v2)."""
        return self._xml.get('using') or self._xml.get('measure-to-sort-by')

    @property
    def manual_order(self):
        """List of values for manual sort, or empty list. Excludes the %all% bucket."""
        buckets = self._xml.findall('.//bucket')
        return [b.text.strip('"') for b in buckets if b.text and b.text != '%all%']

    @property
    def shelf(self):
        """Which shelf this sort applies to (shelf-sort-v2 only)."""
        return self._xml.get('shelf')


def _parse_sorts(root_node):
    sorts = []
    paths = (
        'table/view/computed-sort',
        'table/view/manual-sort',
        'table/view/shelf-sorts/shelf-sort-v2',
    )
    for path in paths:
        for el in root_node.findall(path):
            sorts.append(Sort(el))
    return sorts
