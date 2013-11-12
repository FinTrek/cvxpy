"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
from sparse_bool_mat import SparseBoolMat

def vstack(values):
    """Vertically concatenates bool matrices.

    Args:
        values: A list of bool Numpy ndarrays and SparseBoolMats.

    Returns:
        A Numpy bool ndarray.
    """
    matrices = []
    for value in values:
        if isinstance(value, np.ndarray):
            matrices.append( value.value )
        else:
            mat = value.todense()
            matrices.append( mat.value )
    return np.vstack(matrices)

def dot(lh_mat, rh_mat):
    """Multiply two matrices/scalars.

    Args:
        lh_mat: A bool Numpy ndarray, SparseBoolMat, or Numpy bool_.
        rh_mat: A bool Numpy ndarray, SparseBoolMat, or Numpy bool_.

    Returns:
        A bool Numpy ndarray, SparseBoolMat, or Numpy bool_.
    """
    # Reduce to elementwise AND if one side is a bool.
    if isinstance(lh_mat, np.bool_) or isinstance(rh_mat, np.bool_):
        return lh_mat & rh_mat
    elif isinstance(lh_mat, SparseBoolMat) and \
         isinstance(rh_mat, SparseBoolMat):
        return lh_mat * rh_mat
    # If only one side is sparse, convert it to an ndarray.
    elif isinstance(lh_mat, SparseBoolMat):
        lh_mat = lh_mat.todense()
    elif isinstance(rh_mat, SparseBoolMat):
        rh_mat = rh_mat.todense()
    return np.dot(lh_mat, rh_mat)

def promote(value, rows, cols):
    """Promotes a scalar to a matrix of the desired size.

    Has no effect on non-scalar values.

    Args:
        value: The scalar to promote.
        rows: The number of rows in the promoted matrix.
        cols: The number of columns in the promoted matrix.

    Returns:
        A Numpy bool ndarray.
    """
    size = (rows, cols)
    if size != (1, 1) and value.size == 1:
        value = to_scalar(value)
        mat = np.empty(size, dtype='bool')
        mat.fill(value)
        return mat
    else:
        return value

def to_scalar(value):
    """Converts a 1x1 matrix to a scalar.

    Args:
        value: A Numpy ndarray, SparseBoolMat, or Numpy bool_.

    Returns:
        A Numpy bool_ equal to the value.
    """
    if value.size == 1 and isinstance(value, (np.ndarray, SparseBoolMat)):
        return np.bool_(value.any())
    else:
        return value