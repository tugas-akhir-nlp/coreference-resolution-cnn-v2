from tensorflow.python.framework.ops import Tensor
from tensorflow.keras.layers import Input
from typing import Tuple


class BaseTensorBuilder:
    variables = []

    def __init__(self, input_shape: tuple = None) -> None:
        self.input_shape = input_shape

    def create_tensor(self, input_tensor: Tensor = None, input_only: bool = False, **kwargs) -> Tuple[Tensor, Tensor]:
        self.check_variables()

        temp = {}

        for variable in self.variables:
            if variable in kwargs:
                temp[variable] = getattr(self, variable)
                setattr(self, variable, kwargs[variable])

        if input_tensor is None:
            input_tensor = self.create_input_tensor()

        tensor = input_tensor if input_only else self.create_processing_tensor(input_tensor)

        for variable in temp.keys():
            setattr(self, variable, temp[variable])

        return input_tensor, tensor

    def check_variables(self) -> None:
        for variable in self.variables:
            if getattr(self, variable, None) is None:
                raise Exception('Variable %s is None' % variable)

    def create_input_tensor(self) -> Tensor:
        if getattr(self, 'input_shape', None) is None:
            raise Exception('Variable input_shape is None')

        return Input(self.input_shape)

    def create_processing_tensor(self, input_tensor: Tensor) -> Tensor:
        raise NotImplementedError()
