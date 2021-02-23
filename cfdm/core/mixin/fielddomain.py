class FieldDomain:
    """Mixin class for methods common to field and domain constructs.

    .. versionadded:: (cfdm) 1.9.0.0

    """

    def __docstring_package_depth__(self):
        """Returns the package depth for {{package}} substitutions.

        See `_docstring_package_depth` for details.

        """
        return 1

    # ----------------------------------------------------------------
    # Attributes
    # ----------------------------------------------------------------
    @property
    def constructs(self):
        """Return the metdata constructs.

        .. versionadded:: (cfdm) 1.7.0

        :Returns:

            `Constructs`
                The constructs.

        **Examples:**

        >>> f = {{package}}.example_field(0)
        >>> print(f.constructs)
        Constructs:
        {'cellmethod0': <{{repr}}CellMethod: area: mean>,
         'dimensioncoordinate0': <{{repr}}DimensionCoordinate: latitude(5) degrees_north>,
         'dimensioncoordinate1': <{{repr}}DimensionCoordinate: longitude(8) degrees_east>,
         'dimensioncoordinate2': <{{repr}}DimensionCoordinate: time(1) days since 2018-12-01 >,
         'domainaxis0': <{{repr}}DomainAxis: size(5)>,
         'domainaxis1': <{{repr}}DomainAxis: size(8)>,
         'domainaxis2': <{{repr}}DomainAxis: size(1)>}
        >>> print(f.domain.constructs)
        Constructs:
        {'dimensioncoordinate0': <{{repr}}DimensionCoordinate: latitude(5) degrees_north>,
         'dimensioncoordinate1': <{{repr}}DimensionCoordinate: longitude(8) degrees_east>,
         'dimensioncoordinate2': <{{repr}}DimensionCoordinate: time(1) days since 2018-12-01 >,
         'domainaxis0': <{{repr}}DomainAxis: size(5)>,
         'domainaxis1': <{{repr}}DomainAxis: size(8)>,
         'domainaxis2': <{{repr}}DomainAxis: size(1)>}

        """
        return self._get_component("constructs")

    # ----------------------------------------------------------------
    # Methods
    # ----------------------------------------------------------------
    def get_construct(self, key, default=ValueError()):
        """Return a metadata construct.

        .. versionadded:: (cfdm) 1.7.0

        .. seealso:: `constructs`, `del_construct`, `has_construct`,
                     `set_construct`

        :Parameters:

            key: `str`
                The key of the metadata construct.

                *Parameter example:*
                  ``key='domainaxis1'``

            default: optional
                Return the value of the *default* parameter if the
                construct does not exist.

                {{default Exception}}

        :Returns:

                The metadata construct.

        **Examples:**

        >>> f.constructs()
        {'auxiliarycoordinate0': <{{repr}}AuxiliaryCoordinate: latitude(10, 9) degree_N>,
         'auxiliarycoordinate1': <{{repr}}AuxiliaryCoordinate: longitude(9, 10) degreeE>,
         'auxiliarycoordinate2': <{{repr}}AuxiliaryCoordinate: long_name:greek_letters(10) >,
         'coordinatereference1': <{{repr}}CoordinateReference: rotated_latitude_longitude>,
         'dimensioncoordinate1': <{{repr}}DimensionCoordinate: grid_latitude(10) degrees>,
         'dimensioncoordinate2': <{{repr}}DimensionCoordinate: grid_longitude(9) degrees>,
         'domainaxis1': <{{repr}}DomainAxis: 10>,
         'domainaxis2': <{{repr}}DomainAxis: 9>}
        >>> f.get_construct('dimensioncoordinate1')
        <{{repr}}DimensionCoordinate: grid_latitude(10) degrees>

        """

        c = self.constructs.get(key)
        if c is None:
            return self._default(
                default, message=f"{key!r} construct does not exist"
            )

        return c

    def has_construct(self, key):
        """Whether a metadata construct exists.

        .. versionadded:: (cfdm) 1.7.0

        .. seealso:: `constructs`, `del_construct`, `get_construct`,
                     `set_construct`

        :Parameters:

            key: `str`
                The identifier of the metadata construct.

                *Parameter example:*
                  ``key='auxiliarycoordinate0'``

        :Returns:

            `bool`
                True if the construct exists, otherwise False.

        **Examples:**

        >>> f.has_construct('dimensioncoordinate1')
        True

        >>> f.has_construct('dimensioncoordinate99')
        False

        """
        return key in self.constructs

    def set_construct(self, construct, key=None, axes=None, copy=True):
        """Set a metadata construct.

        .. versionadded:: (cfdm) 1.7.0

        .. seealso:: `constructs`, `del_construct`, `get_construct`,
                     `set_data_axes`

        :Parameters:

            construct:
                The metadata construct to be inserted.

            key: `str`, optional
                The construct identifier to be used for the
                construct. If not set then a new, unique identifier is
                created automatically. If the identifier already
                exists then the existing construct will be replaced.

                *Parameter example:*
                  ``key='cellmeasure0'``

            axes: (sequence of) `str`, optional
                The construct identifiers of the domain axis
                constructs spanned by the data array. An exception is
                raised if used for a metadata construct that can not
                have a data array, i.e. domain axis, cell method and
                coordinate reference constructs.

                *Parameter example:*
                  ``axes='domainaxis1'``

                *Parameter example:*
                  ``axes=['domainaxis1']``

                *Parameter example:*
                  ``axes=['domainaxis1', 'domainaxis0']``

            copy: `bool`, optional
                If True then set a copy of the construct. By default
                the construct is copied.

        :Returns:

             `str`
                The construct identifier for the construct.

        **Examples:**

        >>> key = f.set_construct(c)
        >>> key = f.set_construct(c, copy=False)
        >>> key = f.set_construct(c, axes='domainaxis2')
        >>> key = f.set_construct(c, key='cellmeasure0')

        """
        return self.constructs._set_construct(
            construct, key=key, axes=axes, copy=copy
        )

    def get_data_axes(self, key, default=ValueError):
        """Gets the keys of the axes spanned by the construct data.

        Specifically, returns the keys of the domain axis constructs
        spanned by the data of a metadata construct.

        .. versionadded:: (cfdm) 1.7.0

        .. seealso:: `del_data_axes`, `has_data_axes`, `set_data_axes`

        :Parameters:

            key: `str`
                Specify a metadata construct.

                *Parameter example:*
                  ``key='auxiliarycoordinate0'``

            default: optional
                Return the value of the *default* parameter if the
                data axes have not been set.

                {{default Exception}}

        :Returns:

            `tuple`
                The keys of the domain axis constructs spanned by the
                data.

        **Examples:**

        >>> f.set_data_axes(['domainaxis0', 'domainaxis1'])
        >>> f.get_data_axes()
        ('domainaxis0', 'domainaxis1')
        >>> f.del_data_axes()
        ('domainaxis0', 'domainaxis1')
        >>> print(f.del_dataxes(None))
        None
        >>> print(f.get_data_axes(default=None))
        None

        """
        try:
            return self.constructs.data_axes()[key]
        except KeyError:
            return self._default(
                default,
                message=(
                    f"{self.__class__.__name__!r} has no data axes for "
                    f"the metadata construct {key!r}"
                ),
            )

    def del_data_axes(self, key, default=ValueError()):
        """Removes the keys of the axes spanned by the construct data.

        Specifically, removes the keys of the domain axis constructs
        spanned by the data of a metadata construct.

        .. versionadded:: (cfdm) 1.7.0

        .. seealso:: `get_data_axes`, `has_data_axes`, `set_data_axes`

        :Parameters:

            key: `str`
                Specify a metadata construct, instead of the field
                construct.

                *Parameter example:*
                  ``key='auxiliarycoordinate0'``

            default: optional
                Return the value of the *default* parameter if the
                data axes have not been set.

                {{default Exception}}

        :Returns:

            `tuple`
                The removed keys of the domain axis constructs spanned
                by the data.

        **Examples:**

        >>> f.del_data_axes(key='dimensioncoordinate2')
        ('domainaxis1',)

        >>> f.has_data_axes(key='auxiliarycoordinate0')
        False
        >>> f.has_data_axes(key='auxiliarycoordinate0', default='no axes')
        'no axes'

        """
        try:
            data_axes = self.constructs.data_axes()[key]
        except KeyError:
            return self._default(
                default,
                message=(
                    f"{self.__class__.__name__!r} has no data axes for the "
                    f"metadata construct {key!r}"
                ),
            )
        else:
            self.constructs._del_data_axes(key)

        return data_axes

    def has_data_axes(self, key):
        """Whether the axes spanned by the construct data have been set.

        Specifically, whether the domain axis constructs spanned by the
        data of a metadata construct have been set.

        .. versionadded:: (cfdm) 1.7.0

        .. seealso:: `del_data_axes`, `get_data_axes`, `set_data_axes`

        :Parameters:

            key: `str`
                Specify a metadata construct.

                *Parameter example:*
                  ``key='domainancillary1'``

        :Returns:

            `bool`
                True if domain axis constructs that span the data been
                set, otherwise False.

        **Examples:**

        >>> f.set_data_axes(['domainaxis0', 'domainaxis1'])
        >>> f.get_data_axes()
        ('domainaxis0', 'domainaxis1')
        >>> f.del_data_axes()
        ('domainaxis0', 'domainaxis1')
        >>> print(f.del_dataxes(None))
        None
        >>> print(f.get_data_axes(default=None))
        None

        """
        axes = self.get_data_axes(key, default=None)
        return axes is not None

    def set_data_axes(self, axes, key):
        """Sets domain axis constructs spanned by the construct data.

        .. versionadded:: (cfdm) 1.7.0

        .. seealso:: `data`, `del_data_axes`, `get_data`, `get_data_axes`,
                     `has_data_axes`

        :Parameters:

             axes: sequence of `str`
                The identifiers of the domain axis constructs spanned
                by the data of the field or of a metadata construct.

                *Parameter example:*
                  ``axes='domainaxis1'``

                *Parameter example:*
                  ``axes=['domainaxis1']``

                *Parameter example:*
                  ``axes=['domainaxis1', 'domainaxis0']``

             key: `str`
                Specify a metadata construct.

                *Parameter example:*
                  ``key='domainancillary1'``

        :Returns:

            `None`

        **Examples:**

        >>> f.set_data_axes(['domainaxis0', 'domainaxis1'])
        >>> f.get_data_axes()
        ('domainaxis0', 'domainaxis1')
        >>> f.del_data_axes()
        ('domainaxis0', 'domainaxis1')
        >>> print(f.del_dataxes(None))
        None
        >>> print(f.get_data_axes(None))
        None

        """
        self.constructs._set_construct_data_axes(key=key, axes=axes)
