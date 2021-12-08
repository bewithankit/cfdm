import numpy as np

from .abstract import CompressedArray
from .mixin import Subsampled
from .subarray import SubsampledQuadraticSubarray


class SubsampledQuadraticArray(Subsampled, CompressedArray):
    """An subsampled array with quadratic interpolation.

    The information needed to uncompress the data is stored in a tie
    point index variable that defines the relationship between the
    indices of the subsampled dimension and the indices of the
    corresponding interpolated dimension.

    >>> coords = cfdm.SubsampledQuadraticArray(
    ...     compressed_array=cfdm.Data([15, 135, 225, 255, 345]),
    ...     shape=(12,),
    ...     ndim=1,
    ...     size=12,
    ...     tie_point_indices={0: cfdm.TiePointIndex(data=[0, 4, 7, 8, 11])},
    ...     parameters={
    ...       "w": cfdm.InterpolationParameter(data=[5, 10, 5])
    ...     },
    ...     parameter_dimensions={"w": (0,)},
    ... )
    >>> print(coords[...])
    [ 15.          48.75        80.         108.75       135.
     173.88888889 203.88888889 225.         255.         289.44444444
     319.44444444 345.        ]


    **Cell boundaries**

    If the subsampled array represents cell boundaries, then the
    *shape*, *ndim* and *size* parameters that describe the
    uncompressed array will include the required trailing size 2
    dimension.

    >>> bounds = cfdm.SubsampledQuadraticArray(
    ...     compressed_array=cfdm.Data([0, 150, 240, 240, 360]),
    ...     shape=(12, 2),
    ...     ndim=2,
    ...     size=24,
    ...     tie_point_indices={0: cfdm.TiePointIndex(data=[0, 4, 7, 8, 11])},
    ...     parameters={
    ...       "w": cfdm.InterpolationParameter(data=[5, 10, 5])
    ...     },
    ...     parameter_dimensions={"w": (0,)},
    ... )
    >>> print(bounds[...])
    [[  0.          33.2       ]
     [ 33.2         64.8       ]
     [ 64.8         94.8       ]
     [ 94.8        123.2       ]
     [123.2        150.        ]
     [150.         188.88888889]
     [188.88888889 218.88888889]
     [218.88888889 240.        ]
     [240.         273.75      ]
     [273.75       305.        ]
     [305.         333.75      ]
     [333.75       360.        ]]

    .. versionadded:: (cfdm) 1.9.TODO.0

    """

    def __new__(cls, *args, **kwargs):
        """Store component classes.

        .. note:: If a child class requires different component
                  classes than the ones defined here, then they must
                  be redefined in the __new__ method of the child
                  class.

        """
        instance = super().__new__(cls)
        instance._Subarray = SubsampledQuadraticSubarray
        return instance

    def __init__(
        self,
        compressed_array=None,
        shape=None,
        size=None,
        ndim=None,
        computational_precision=None,
        tie_point_indices={},
        parameters={},
        parameter_dimensions={},
    ):
        """**Initialisation**

        :Parameters:

            compressed_array: `Data`
                The tie points array.

            shape: `tuple`
                The uncompressed array dimension sizes.

            size: `int`
                Number of elements in the uncompressed array.

            ndim: `int`
                The number of uncompressed array dimensions.

            compressed_axes: sequence of `int`
                The position of the compressed axis in the tie points
                array.

                *Parameter example:*
                  ``compressed_axes=[1]``

            tie_point_indices: `dict`, optional
                TODO

            tie_point_indices: `dict`
                The tie point index variable for each subsampled
                dimension. A key indentifies a subsampled dimension by
                its integer position in the compressed array, and its
                value is a `TiePointIndex` variable.

                *Parameter example:*
                  ``tie_point_indices={1: cfdm.TiePointIndex(data=[0, 16])}``

            computational_precision: `str`, optional
                The floating-point arithmetic precision used during
                the preparation and validation of the compressed
                coordinates.

                *Parameter example:*
                  ``computational_precision='64'``

        """
        super().__init__(
            compressed_array=compressed_array,
            shape=shape,
            size=size,
            ndim=ndim,
            compression_type="subsampled",
            interpolation_name="quadratic",
            computational_precision=computational_precision,
            tie_point_indices=tie_point_indices.copy(),
            parameters=parameters.copy(),
            parameter_dimensions=parameter_dimensions.copy(),
            compressed_dimensions=tuple(tie_point_indices),
            one_to_one=True,
        )
