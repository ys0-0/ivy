# global

# local
import ivy
import ivy.functional.frontends.tensorflow as tf_frontend
from ivy.functional.frontends.tensorflow.func_wrapper import to_ivy_dtype, _to_ivy_array
from ivy.functional.frontends.numpy.creation_routines.from_existing_data import array


class EagerTensor:
    def __init__(self, array):
        self._ivy_array = (
            ivy.array(array) if not isinstance(array, ivy.Array) else array
        )

    def __repr__(self):
        return (
            repr(self.ivy_array).replace(
                "ivy.array", "ivy.frontends.tensorflow.EagerTensor"
            )[:-1]
            + ", shape="
            + str(self.shape)
            + ", dtype="
            + str(self.dtype)
            + ")"
        )

    # Properties #
    # ---------- #

    @property
    def ivy_array(self):
        return self._ivy_array

    @property
    def device(self):
        return self.ivy_array.device

    @property
    def dtype(self):
        return tf_frontend.DType(
            tf_frontend.tensorflow_type_to_enum[self.dtype]
        )

    @property
    def shape(self):
        return self.ivy_array.shape

    # Instance Methods #
    # ---------------- #

    def get_shape(self):
        return tf_frontend.raw_ops.Shape(input=self)

    def set_shape(self, shape):
        if shape is None:
            return

        x_shape = self.shape
        if len(x_shape) != len(shape):
            raise ValueError(
                f"Tensor's shape {x_shape} is not compatible with supplied shape "
                f"{shape}."
            )
        for i, v in enumerate(x_shape):
            if v != shape[i] and (shape[i] is not None):
                raise ValueError(
                    f"Tensor's shape {x_shape} is not compatible with supplied shape "
                    f"{shape}."
                )

    def numpy(self):
        return array(self.ivy_array)

    def __add__(self, y, name="add"):
        return self.__radd__(y)

    def __div__(self, y, name="div"):
        if "int" in self.dtype:
            return tf_frontend.raw_ops.FloorDiv(x=self, y=y, name=name)
        ret = tf_frontend.math.divide(self, y, name=name)
        return tf_frontend.cast(ret, self.dtype)

    def __and__(self, y, name="and"):
        return self.__rand__(y)

    def __array__(self, dtype=None, name="array"):
        dtype = to_ivy_dtype(dtype)
        return array(ivy.asarray(self.ivy_array, dtype=dtype))

    def __bool__(self, name="bool"):
        if isinstance(self.ivy_array, int):
            return self.ivy_array != 0

        temp = ivy.squeeze(ivy.asarray(self.ivy_array), axis=None)
        shape = ivy.shape(temp)
        if shape:
            raise ValueError(
                "The truth value of an array with more than one element is ambiguous. "
                "Use a.any() or a.all()"
            )

        return temp != 0

    def __eq__(self, other):
        return tf_frontend.raw_ops.Equal(
            x=self, y=other, incompatible_shape_error=False
        )

    def __floordiv__(self, y, name="floordiv"):
        return tf_frontend.raw_ops.FloorDiv(x=self, y=y, name=name)

    def __ge__(self, y, name="ge"):
        return tf_frontend.raw_ops.GreaterEqual(x=self, y=y, name=name)

    def __getitem__(self, slice_spec, var=None, name="getitem"):
        ivy_args = ivy.nested_map([self, slice_spec], _to_ivy_array)
        ret = ivy.get_item(*ivy_args)
        return EagerTensor(ret)

    def __gt__(self, y, name="gt"):
        return tf_frontend.raw_ops.Greater(x=self, y=y, name=name)

    def __invert__(self, name="invert"):
        return tf_frontend.raw_ops.Invert(x=self, name=name)

    def __le__(self, y, name="le"):
        return tf_frontend.raw_ops.LessEqual(x=self, y=y, name=name)

    def __lt__(self, y, name="lt"):
        return tf_frontend.raw_ops.Less(x=self, y=y, name=name)

    def __matmul__(self, y, name="matmul"):
        return self.__rmatmul__(y)

    def __mul__(self, y, name="mul"):
        return tf_frontend.math.multiply(self, y, name=name)

    def __mod__(self, y, name="mod"):
        return tf_frontend.floormod(self, y, name=name)

    def __ne__(self, other):
        return tf_frontend.raw_ops.NotEqual(
            x=self, y=other, incompatible_shape_error=False
        )

    def __neg__(self, name="neg"):
        return tf_frontend.raw_ops.Neg(x=self, name=name)

    __nonzero__ = __bool__

    def __or__(self, y, name="or"):
        return self.__ror__(y)

    def __pow__(self, y, name="pow"):
        return tf_frontend.math.pow(x=self, y=y, name=name)

    def __radd__(self, x, name="radd"):
        return tf_frontend.math.add(self, x, name=name)

    def __rand__(self, x, name="rand"):
        return tf_frontend.math.logical_and(self, x, name=name)

    def __rfloordiv__(self, x, name="rfloordiv"):
        _, x = tf_frontend.check_tensorflow_casting(
            self, x.ivy_array if hasattr(x, "ivy_array") else x
        )
        return tf_frontend.raw_ops.FloorDiv(x=x, y=self, name=name)

    def __rmatmul__(self, x, name="rmatmul"):
        _, x = tf_frontend.check_tensorflow_casting(
            self, x.ivy_array if hasattr(x, "ivy_array") else x
        )
        return tf_frontend.raw_ops.MatMul(a=x, b=self, name=name)

    def __rmul__(self, x, name="rmul"):
        return tf_frontend.raw_ops.Mul(x=self, y=x, name=name)

    def __ror__(self, x, name="ror"):
        return tf_frontend.raw_ops.LogicalOr(x=self, y=x, name=name)

    def __rpow__(self, x, name="rpow"):
        _, x = tf_frontend.check_tensorflow_casting(
            self, x.ivy_array if hasattr(x, "ivy_array") else x
        )
        return tf_frontend.raw_ops.Pow(x=x, y=self, name=name)

    def __rsub__(self, x, name="rsub"):
        _, x = tf_frontend.check_tensorflow_casting(
            self, x.ivy_array if hasattr(x, "ivy_array") else x
        )
        return tf_frontend.math.subtract(x, self, name=name)

    def __rtruediv__(self, x, name="rtruediv"):
        _, x = tf_frontend.check_tensorflow_casting(
            self, x.ivy_array if hasattr(x, "ivy_array") else x
        )
        return tf_frontend.math.truediv(x, self, name=name)

    def __rxor__(self, x, name="rxor"):
        return tf_frontend.math.logical_xor(self, x, name=name)

    def __sub__(self, y, name="sub"):
        return tf_frontend.math.subtract(self, y, name=name)

    def __truediv__(self, y, name="truediv"):
        dtype = ivy.dtype(self.ivy_array)
        if str(dtype) in ["uint8", "int8", "uint16", "int16"]:
            return tf_frontend.math.truediv(
                tf_frontend.cast(self, ivy.float32),
                tf_frontend.cast(y, ivy.float32),
                name=name,
            )
        if str(dtype) in ["uint32", "int32", "uint64", "int64"]:
            return tf_frontend.math.truediv(
                tf_frontend.cast(self, ivy.float64),
                tf_frontend.cast(y, ivy.float64),
                name=name,
            )
        return tf_frontend.math.truediv(self, y, name=name)

    def __len__(self):
        return len(self.ivy_array)

    def __xor__(self, y, name="xor"):
        return self.__rxor__(y)

    def __setitem__(self, key, value):
        raise ivy.utils.exceptions.IvyException(
            "ivy.functional.frontends.tensorflow.EagerTensor object "
            "doesn't support assignment"
        )


# Dummy Tensor class to help with compilation, don't add methods here
class Tensor(EagerTensor):
    pass
