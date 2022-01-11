from itertools import product

import numpy as np

from .abstract import RaggedArray


class RaggedIndexedContiguousArray(RaggedArray):
    """An underlying indexed contiguous ragged array.

    A collection of features, each of which is sequence of (vertical)
    profiles, stored using an indexed contiguous ragged array combines
    all feature elements along a single dimension (the "sample
    dimension") such that a contiguous ragged array representation is
    used for each profile and the indexed ragged array representation
    to organise the profiles into timeseries.

    The information needed to uncompress the data is stored in a
    "count variable" that gives the size of each profile; and in a
    "index variable" that specifies the feature that each profile
    belongs to.

    .. versionadded:: (cfdm) 1.7.0

    """

    def __init__(
        self,
        compressed_array=None,
        shape=None,
        size=None,
        ndim=None,
        count_variable=None,
        index_variable=None,
        source=None,
        copy=True,
    ):
        """**Initialisation**

        :Parameters:

            compressed_array: array_like
                The compressed array.

            shape: `tuple`
                The shape of the uncompressed array.

            count_variable: `Count`
                The count variable required to uncompress the data,
                corresponding to a CF-netCDF count variable.

            index_variable: `Index`
                The index variable required to uncompress the data,
                corresponding to a CF-netCDF CF-netCDF index variable.

            source: optional
                Initialise the array from the given object.

                {{init source}}

                .. versionadded:: (cfdm) 1.9.TODO.0

            copy: `bool`, optional
                If False then do not deep copy input parameters prior
                to initialisation. By default arguments are deep
                copied.

                .. versionadded:: (cfdm) 1.9.TODO.0

            size: `int`
                Deprecated at version 1.9.TODO.0. Ignored if set.

                Number of elements in the uncompressed array.

            ndim: `int`
                Deprecated at version 1.9.TODO.0. Ignored if set.

                The number of uncompressed array dimensions.

        """
        super().__init__(
            compressed_array=compressed_array,
            shape=shape,
            count_variable=count_variable,
            index_variable=index_variable,
            compressed_dimensions={0: (0, 1, 2)},
            source=source,
            copy=copy,
        )

    def subarrays(self):
        """Return descriptors for every subarray.

        Theses descriptors are used during subarray decompression.

        .. versionadded:: (cfdm) 1.9.TODO.0

        :Returns:

             4-`tuple` of iterators
                Each iterable iterates over a particular descriptor
                from each subarray.

                1. The indices of the uncompressed array that
                   correspond to each subarray.

                2. The shape of each uncompressed subarray.

                3. The indices of the compressed array that correspond
                   to each subarray.

                4. The location of each subarray on the uncompressed
                   dimensions.

        **Examples**

        An original 3-d array with shape (2, 3, 4) comprising 2
        timeSeriesProfile features has been compressed as an indexed
        contiguous ragged array. The first feature has 3 profiles with
        counts of 2, 4, and 3 elements, at compressed locations (4,
        5), (0, 1, 2, 3), and (9, 10, 11) respectively. The second
        feature has 1 profile with a count of 3 elements, at
        compressed locations (6, 7, 8).

        >>> u_indices, u_shapes, c_indices, locations = x.subarrays()
        >>> for i in u_indices:
        ...    print(i)
        ...
        (slice(0, 1, None), slice(0, 1, None), slice(None, None, None))
        (slice(0, 1, None), slice(1, 2, None), slice(None, None, None))
        (slice(0, 1, None), slice(2, 3, None), slice(None, None, None))
        (slice(1, 2, None), slice(0, 1, None), slice(None, None, None))
        (slice(1, 2, None), slice(1, 2, None), slice(None, None, None))
        (slice(1, 2, None), slice(2, 3, None), slice(None, None, None))
        >>> for i in u_shapes
        ...    print(i)
        ...
        (1, 1, 4)
        (1, 1, 4)
        (1, 1, 4)
        (1, 1, 4)
        (1, 1, 4)
        (1, 1, 4)
        >>> for i in c_indices:
        ...    print(i)
        ...
        (slice(4, 6, None),)
        (slice(0, 4, None),)
        (slice(9, 12, None),)
        (slice(6, 9, None),)
        (slice(0, 0, None),)
        (slice(0, 0, None),)
        >>> for i in locations:
        ...    print(i)
        ...
        (0, 0, 0)
        (0, 1, 0)
        (0, 2, 0)
        (1, 0, 0)
        (1, 1, 0)
        (1, 2, 0)

        """
        d1, (u_dim1, u_dim2, u_dim3) = self.compressed_dimensions().popitem()
        uncompressed_shape = self.shape

        n_features = uncompressed_shape[u_dim1]
        max_n_profiles = uncompressed_shape[u_dim2]

        # The indices of the uncompressed array that correspond to
        # each subarray
        ndim = self.ndim
        u_indices = [(slice(None),)] * ndim
        u_indices[u_dim1] = [slice(i, i + 1) for i in range(n_features)]
        u_indices[u_dim2] = [slice(j, j + 1) for j in range(max_n_profiles)]

        # The location of each subarray
        locations = [(0,)] * ndim
        locations[u_dim1] = [i for i in range(n_features)]
        locations[u_dim2] = [j for j in range(max_n_profiles)]

        # The shape of each uncompressed subarray
        u_shapes = [(n,) for n in uncompressed_shape]
        u_shapes[u_dim1] = (1,) * n_features
        u_shapes[u_dim2] = (1,) * max_n_profiles

        # The indices of the compressed array that correspond to each
        # subarray
        c_indices = [(slice(None),)] * self.source().ndim

        index = np.array(self.get_index())
        unique = np.unique(index).tolist()
        count_partial_sums = np.cumsum(np.array(self.get_count())).tolist()

        # Loop over features
        ind = []
        for i in unique:
            # find the locations in the count array for the profiles
            # in this feature.
            profile_locations = np.where(index == i)[0]

            for j in profile_locations:
                if not j:
                    start = 0
                else:
                    start = count_partial_sums[j - 1]

                ind.append(slice(start, count_partial_sums[j]))

            # Add zero-sized slices for this feature's "missing"
            # profiles
            ind.extend(
                (slice(0, 0),) * (max_n_profiles - profile_locations.size)
            )

        c_indices[d1] = ind

        return (
            product(*u_indices),
            product(*u_shapes),
            product(*c_indices),
            product(*locations),
        )
