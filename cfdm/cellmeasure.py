import logging

from . import mixin
from . import core

from .decorators import _manage_log_level_via_verbosity


logger = logging.getLogger(__name__)


class CellMeasure(mixin.NetCDFVariable,
                  mixin.NetCDFExternal,
                  mixin.PropertiesData,
                  core.CellMeasure):
    '''A cell measure construct of the CF data model.

    A cell measure construct provides information that is needed about
    the size or shape of the cells and that depends on a subset of the
    domain axis constructs. Cell measure constructs have to be used
    when the size or shape of the cells cannot be deduced from the
    dimension or auxiliary coordinate constructs without special
    knowledge that a generic application cannot be expected to have.

    The cell measure construct consists of a numeric array of the
    metric data which spans a subset of the domain axis constructs,
    and properties to describe the data. The cell measure construct
    specifies a "measure" to indicate which metric of the space it
    supplies, e.g. cell horizontal areas, and must have a units
    property consistent with the measure, e.g. square metres. It is
    assumed that the metric does not depend on axes of the domain
    which are not spanned by the array, along which the values are
    implicitly propagated. CF-netCDF cell measure variables correspond
    to cell measure constructs.

    **NetCDF interface**

    The netCDF variable name of the construct may be accessed with the
    `nc_set_variable`, `nc_get_variable`, `nc_del_variable` and
    `nc_has_variable` methods.

    The netCDF variable group structure may be accessed with the
    `nc_set_variable`, `nc_get_variable`, `nc_variable_groups`,
    `nc_clear_variable_groups` and `nc_set_variable_groups` methods.

    .. versionadded:: (cfdm) 1.7.0

    '''
    def __init__(self, measure=None, properties=None, data=None,
                 source=None, copy=True, _use_data=True):
        '''**Initialisation**

    :Parameters:

        measure: `str`, optional
            Set the measure that indicates which metric given by the
            data array. Ignored if the *source* parameter is set.

            The measure may also be set after initialisation with the
            `set_measure` method.

            *Parameter example:*
              ``measure='area'``

        {{init properties: `dict`, optional}}

           *Parameter example:*
             ``properties={'standard_name': 'cell_area'}``

        {{init data: data_like, optional}}

        source: optional
            Initialize the measure, properties and data from those of
            *source*.

        {{init copy: `bool`, optional}}

        '''
        super().__init__(measure=measure, properties=properties,
                         data=data, source=source, copy=copy,
                         _use_data=_use_data)

        self._initialise_netcdf(source)

    def creation_commands(self, representative_data=False,
                          namespace=None, indent=0, string=True,
                          name='c', data_name='d'):
        '''Return the commands that would create the cell measure construct.

    .. versionadded:: (cfdm) 1.8.7.0

    .. seealso:: `{{package}}.Data.creation_commands`,
                 `{{package}}.Field.creation_commands`

    :Parameters:

        {{representative_data: `bool`, optional}}

        {{namespace: `str`, optional}}

        {{indent: `int`, optional}}

        {{string: `bool`, optional}}

    :Returns:

        {{returns creation_commands}}

    **Examples:**

        TODO

        '''
        out = super().creation_commands(
            representative_data=representative_data, indent=indent,
            namespace=namespace, string=False, name=name,
            data_name=data_name)

        measure = self.get_measure(None)
        if measure is not None:
            out.append("{}.set_measure({!r})".format(name, measure))

        if string:
            out[0] = indent+out[0]
            out = ('\n'+indent).join(out)

        return out

    def dump(self, display=True, _omit_properties=None, _key=None,
             _level=0, _title=None, _axes=None, _axis_names=None):
        '''A full description of the cell measure construct.

    Returns a description of all properties, including those of
    components, and provides selected values of all data arrays.

    .. versionadded:: (cfdm) 1.7.0

    :Parameters:

        display: `bool`, optional
            If False then return the description as a string. By
            default the description is printed.

    :Returns:

        {{returns dump}}

        '''
        if _title is None:
            name = self.identity(default=self.get_property('units', ''))
            _title = 'Cell Measure: ' + name

        if self.nc_get_external():
            if not (self.has_data() or self.properties()):
                ncvar = self.nc_get_variable(None)
                if ncvar is not None:
                    ncvar = 'ncvar%'+ncvar
                else:
                    ncvar = ''
                _title += ' (external variable: {0})'.format(ncvar)
        # --- End: if

        return super().dump(display=display, _key=_key,
                            _omit_properties=_omit_properties,
                            _level=_level, _title=_title,
                            _axes=_axes, _axis_names=_axis_names)

    @_manage_log_level_via_verbosity
    def equals(self, other, rtol=None, atol=None, verbose=None,
               ignore_data_type=False, ignore_fill_value=False,
               ignore_properties=(), ignore_compression=True,
               ignore_type=False):
        '''Whether two cell measure constructs are the same.

    Equality is strict by default. This means that:

    * the same descriptive properties must be present, with the same
      values and data types, and vector-valued properties must also have
      same the size and be element-wise equal (see the *ignore_properties*
      and *ignore_data_type* parameters), and

    ..

    * if there are data arrays then they must have same shape and data
      type, the same missing data mask, and be element-wise equal (see the
      *ignore_data_type* parameter).

    {{equals tolerance}}

    {{equals compression}}

    Any type of object may be tested but, in general, equality is only
    possible with another cell measure construct, or a subclass of
    one. See the *ignore_type* parameter.

    {{equals netCDF}}

    .. versionadded:: (cfdm) 1.7.0

    :Parameters:

        other:
            The object to compare for equality.

        {{atol: number, optional}}

        {{rtol: number, optional}}

        {{ignore_fill_value: `bool`, optional}}

        {{verbose: `int` or `str` or `None`, optional}}

        ignore_properties: sequence of `str`, optional
            The names of properties to omit from the comparison.

        {{ignore_data_type: `bool`, optional}}

        {{ignore_compression: `bool`, optional}}

        {{ignore_type: `bool`, optional}}

    :Returns:

        `bool`
            Whether the two cell measure constructs are equal.

    **Examples:**

    >>> f.equals(f)
    True
    >>> f.equals(f.copy())
    True
    >>> f.equals('not a cell measure')
    False

    >>> g = f.copy()
    >>> g.set_property('foo', 'bar')
    >>> f.equals(g)
    False
    >>> f.equals(g, verbose=3)
    CellMeasure: Non-common property name: foo
    CellMeasure: Different properties
    False

        '''
        if not super().equals(other,
                              rtol=rtol, atol=atol,
                              verbose=verbose,
                              ignore_data_type=ignore_data_type,
                              ignore_fill_value=ignore_fill_value,
                              ignore_properties=ignore_properties,
                              ignore_compression=ignore_compression,
                              ignore_type=ignore_type):
            return False

        measure0 = self.get_measure(None)
        measure1 = other.get_measure(None)
        if measure0 != measure1:
            logger.info("{0}: Different measure ({1} != {2})".format(
                self.__class__.__name__, measure0, measure1))
            return False

        return True

    def identity(self, default=''):
        '''Return the canonical identity.

    By default the identity is the first found of the following:

    * The measure, preceeded by ``'measure:'``.
    * The ``standard_name`` property.
    * The ``cf_role`` property, preceeded by 'cf_role='.
    * The ``long_name`` property, preceeded by 'long_name='.
    * The netCDF variable name, preceeded by 'ncvar%'.
    * The value of the default parameter.

    .. versionadded:: (cfdm) 1.7.0

    .. seealso:: `identities`

    :Parameters:

        default: optional
            If no identity can be found then return the value of the
            default parameter.

    :Returns:

            The identity.

    **Examples:**

    >>> c.get_measure()
    'area'
    >>> c.properties()
    {'long_name': 'Area',
     'standard_name': 'cell_area'}
    >>> c.nc_get_variable()
    'areacello'
    >>> c.identity(default='no identity')
    'measure:area'
    >>> c.del_measure()
    'area'
    >>> c.identity()
    'cell_area'
    >>> c.del_property('standard_name')
    'cell_area'
    >>> c.identity()
    'long_name=Area'
    >>> c.del_properly('long_name')
    'Area'
    >>> c.identity()
    'ncvar%areacello'
    >>> c.nc_del_variable()
    'areacello'
    >>> c.identity()
    ''
    >>> c.identity(default='no identity')
    'no identity'

        '''
        n = self.get_measure(None)
        if n is not None:
            return 'measure:{0}'.format(n)

        n = self.get_property('standard_name', None)
        if n is not None:
            return n

        for prop in ('cf_role', 'long_name'):
            n = self.get_property(prop, None)
            if n is not None:
                return '{0}={1}'.format(prop, n)
        # --- End: for

        n = self.nc_get_variable(None)
        if n is not None:
            return 'ncvar%{0}'.format(n)

        return default

    def identities(self):
        '''Return all possible identities.

    The identities comprise:

    * The measure property, preceeded by ``'measure:'``.
    * The ``standard_name`` property.
    * All properties, preceeded by the property name and a colon,
      e.g. ``'long_name:Air temperature'``.
    * The netCDF variable name, preceeded by ``'ncvar%'``.

    .. versionadded:: (cfdm) 1.7.0

    .. seealso:: `identity`

    :Returns:

        `list`
            The identities.

    **Examples:**

    >>> f.properties()
    {'foo': 'bar',
     'long_name': 'Area of cells',
     'standard_name': 'cell_area'}
    >>> f.nc_get_variable()
    'areacello'
    >>> f.identities()
    ['measure:area',
     'cell_area',
     'long_name=Area of cells',
     'foo=bar',
     'standard_name=cell_area',
     'ncvar%areacello']

        '''
        out = super().identities()

        n = self.get_measure(None)
        if n is not None:
            out.insert(0, 'measure:{0}'.format(n))

        return out

# --- End: class
