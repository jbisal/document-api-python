class DatasourceDependency(object):
    """ A class representing a datasource dependency in a dashboard or worksheet"""
    def __init__(self, dependency_xml):
        """ Initialize DatasourceDependency from XML Element
        
        Args:
            dependency_xml: XML element representing the datasource dependency
        """
        self._xml = dependency_xml
        self._datasource = dependency_xml.get('datasource')
        self._columns = self._parse_columns()
        self._column_instances = self._parse_column_instances()
        
    @property
    def xml(self):
        """Return xml of the datsource dependency """
        return self._xml
    
    @property
    def datasource(self):
        """Return datasource name of the dependency """
        return self._datasource
    
    @property
    def columns(self):
        """Return columns of the datsource dependency """
        return self._columns
    
    @property
    def column_instances(self):
        """Return columns of the datsource dependency """
        return self._column_instances
    
    def _parse_columns(self):
        columns = []
        for column in self._xml.findall('column'):
            name = column.get('name')
            if name:
                columns.append(name)
        return columns
    
    
    def _parse_column_instances(self):
        column_instances = {}
        for column_instance in self._xml.findall('column-instance'):
            col_attrib = column_instance.get('column')
            if col_attrib:
                instance = dict(column_instance.attrib)
                tc = column_instance.find('table-calc')
                if tc is not None:
                    instance['table_calc'] = dict(tc.attrib)
                    addr = tc.find('address')
                    if addr is not None:
                        instance['table_calc']['address_values'] = [
                            v.text for v in addr.findall('value') if v.text
                        ]
                else:
                    instance['table_calc'] = None
                column_instances[col_attrib] = instance
        return column_instances
    
