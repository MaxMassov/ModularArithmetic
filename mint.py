from functools import wraps
import inspect
from typing import Callable
import re
from math import gcd

class mint:

    """Represents an integer number from the specified modular system."""

    __slots__ = ("_value", "_mod", "_gcd")

    #ToDo: property func or setter
    _DISABLE_INT2MINT_CONVERSION = False
    """
    Flag that defines behaviour of operations between int and mint. True means 
    these operations are undefined, False -- defined. Defaults to False.
    """

    def __init__(self, value: int, mod: int):
        """
        Initializes a mint instance.

        Args:
            value (int): The integer number's value.
            mod (int): The modulus of the system. Must be an integer 
                greater than 1.

        Returns:
            mint: A new instance of the modular integer.

        Raises:
            ValueError: If either `value` or `modulus` is not an integer, 
                or if `modulus` is less than 2.
        """
        # checking args values
        if not isinstance(value, int):
            raise ValueError("Value must be integer")
        
        if not isinstance(mod, int):
            raise ValueError("Modulus must be int and not less than 2")
        
        if mod <= 1:
            raise ValueError("Modulus must be at least 2")
        
        # initializing mint instance
        self._value = value % mod
        self._mod = mod
        self._gcd = gcd(self._value, self._mod)
    
    @property
    def value(self):
        """Read-only property for value."""
        return self._value

    @property
    def mod(self):
        """Read-only property for modulus."""
        return self._mod  
    
    @property
    def vm_gcd(self):
        """Read-only property for value-modulus gcd."""
        return self._gcd  

    def __setattr__(self, name, value):
        """
        Makes attributes read-only.
        
        Raises:
            AttributeError: When method is called out of the class
        """
        stack = inspect.stack()
        caller_class = stack[1].frame.f_locals.get("self", None)
        if not isinstance(caller_class, mint):
            raise AttributeError(f"{name} is read-only.")
        super().__setattr__(name, value)

    @property
    def int2mint(self) -> bool:
        """Access to mint._DISABLE_INT2MINT_CONVERSION value."""
        return not mint._DISABLE_INT2MINT_CONVERSION

    @classmethod
    def set_int2mint(cls, value: bool):
        """
        Set mint._DISABLE_INT2MINT_CONVERSION to a !`value`
        
        Arguments:
            value (bool): new value of mint._DISABLE_INT2MINT_CONVERSION 
                (can be int, but must be equal to either 1 or 0).
        
        Raises:
            ValueError: If value has not a relevant value.
        """
        if isinstance(value, int) and (value == 1 or value == 0):
            value = bool(value)
        if isinstance(value, bool):
            cls._DISABLE_INT2MINT_CONVERSION = not value
        else:
            raise ValueError("mint._DISABLE_INT2MINT_CONVERSION must be bool.")  

    @classmethod
    def change_int2mint(cls):
        """
        Set mint._DISABLE_INT2MINT_CONVERSION to the opposite value
        """
        cls._DISABLE_INT2MINT_CONVERSION = not cls._DISABLE_INT2MINT_CONVERSION

    @classmethod
    def activate_int2mint(cls):
        """
        Set mint._DISABLE_INT2MINT_CONVERSION to False
        """
        cls._DISABLE_INT2MINT_CONVERSION = False

    @classmethod
    def disable_int2mint(cls):
        """
        Set mint._DISABLE_INT2MINT_CONVERSION to True
        """
        cls._DISABLE_INT2MINT_CONVERSION = True

    def __neg__(self):
        """
        Implements unary minus - behaviour.
        
        Returns:
            mint: A new instance of the modular integer
                which is equal to -previous_value.
        """
        return self.__class__(-self._value, self._mod)

    def __invert__(self):
        """
        Implements modular int inversion (~ operation).
        
        Returns:
            mint: A new instance of the modular integer
                which is equal to inverted previous value.
        """
        return self.__class__(~self._value, self._mod)

    @staticmethod
    def _check_value(method: Callable):
        """
        Decorator that checks if the method called with a relevant value.

        Args:
            method (function): A mint method between two values.

        Returns:
            wrapper (function): A function that checks if the method called 
                with a relevant value.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            """
            Function that checks if the method called with a relevant value.

            Args:
                value (mint|int|float|bool): the value to which the method will be applied.

            Returns:
                mint: A new instance of the modular integer
                    which is equal to result of applying
                    method to self value and given value.

            Raises:
                TypeError: If more or less than one arrgument is given.
                ValueError: If the given mint value is not from the same
                    modular system as self.
                TypeError: If the value is instance of int|float|bool,
                    but int to mint conversion disabled, 
                    and the value is not being used as an argument of the 
                    following methods: __mul__, __rmul__, __pow__, __floordiv__, 
                    __truediv__, __rfloordiv__, __rtruediv__
            """
            value = None
            if len(args) == 1:
                value = args[0]
            elif len(kwargs.values()) == 1:
                value = kwargs.values()[0]
            if value is None:
                raise TypeError(f"""Method {method.__name__}() takes one argument 
                                ({len(args) + len(kwargs.values())} given).""")
            if isinstance(value, mint):
                if self._mod != value.mod:
                    raise ValueError(
                            """You cannot directly operate on numbers from 
                                different modular systems without first aligning 
                                them to a common modulus."""
                        )
                return method(self, value)
            if isinstance(value, float):
                value = int(value)
            elif isinstance(value, bool):
                value = int(value)
            if isinstance(value, int):
                if method.__name__ in ["__mul__", "__rmul__", "__pow__", 
                                       "__floordiv__", "__truediv__",
                                       "__rfloordiv__", "__rtruediv__"]:
                    return method(self, value)
                if mint._DISABLE_INT2MINT_CONVERSION:
                    raise TypeError(f"""Int to modular int conversion was disabled, 
                                    so the {method.__name__}() cannot be done.""")
                return method(self, self.__class__(value, self._mod))
            return NotImplemented
        return wrapper
    
    @_check_value
    def __add__(self, value):
        """
        Implements the addition of 2 modular integers or 
        a modular integer and an integer|float|bool.

        See __check_value decorator
        """
        return self.__class__(self._value + value.value, self._mod)  

    @_check_value
    def __radd__(self, value):
        """
        Implements the addition of an integer|float|bool and a modular integer.

        See __check_value decorator
        """
        return self.__class__(value.value + self._value, self._mod)

    @_check_value
    def __sub__(self, value):
        """
        Implements the subtraction of of 2 modular integers or 
        a modular integer and an integer|float|bool.

        See __check_value decorator
        """
        return self.__class__(self._value - value.value, self._mod)
    
    @_check_value
    def __rsub__(self, value):
        """
        Implements the subtraction of an integer|float|bool and a modular integer.

        See __check_value decorator
        """
        return self.__class__(value.value - self._value, self._mod)

    @_check_value
    def __mul__(self, value):
        """
        Implements the multiplication of 2 modular integers or 
        a modular integer and an integer|float|bool.

        See __check_value decorator
        """
        if isinstance(value, int):
            if value == 0:
                return self.__class__(0, self._mod)
            return self.__class__(self._value * value, self._mod * value)
        return self.__class__(self._value * value.value, self._mod)  
    
    def __rmul__(self, value):
        """
        Implements the multiplications of an integer|float|bool and a modular integer.

        See __check_value decorator
        """
        return self.__mul__(value)  
    
    @_check_value
    def __pow__(self, value):
        """
        Implements the raising modular integer to the power 
        of mint|integer|float|bool.

        Raises:
            ValueError: When the value is less than 0 and modular integer
                is not invertable.

        See __check_value decorator
        """
        if isinstance(value, int):
            if value < 0 and self._gcd != 1:
                raise ValueError(f"""base is not invertible for the given modulus 
                                 (gcd({self._value}, {self._gcd}) = {self._gcd})""")
            return self.__class__(pow(self._value, value, self._mod), self._mod)
        return self.__class__(pow(self._value, value.value, self._mod), self._mod)  
    
    @_check_value
    def __rpow__(self, value):
        """
        Implements the raising integer|float|bool 
        to the power of mint.

        See __check_value decorator
        """
        return self.__class__(pow(value.value, self._value, self._mod), self._mod)  

    def __floordiv__(self, value):
        """
        Implements the floor division of modular integer by 
        mint|integer|float|bool.

        See __truediv__ method
        """
        return self.__truediv__(value)
    
    def __rfloordiv__(self, value):
        """
        The floor division of modular integer
        by mint|integer|float|bool is not defined.
        """
        return NotImplemented
    
    @_check_value
    def __truediv__(self, value):
        """
        Implements the division of modular integer by 
        mint|integer|float|bool.

        Raises:
            ValueError: If divider is negative
            ZeroDivisionError: If divider is equal to 0.
            ValueError: If mint value is not divisible by a divider.

        See __check_value decorator
        """
        divider = value if isinstance(value, int) else value.value
        if divider < 0:
            raise ValueError("Not modular integer divider must be positive")
        if divider == 0:
            raise ZeroDivisionError("division by zero.")
        if self._value % divider != 0:
            raise ValueError(f"{self._value} is not divisible by {divider}.")
        return self.__class__(self._value // divider, self._mod // gcd(self._mod, divider))
    
    def __rtruediv__(self, value):
        """
        The division of mint|integer|float|bool
        by modular integer is not defined.
        """
        return NotImplemented
    
    def __mod__(self, value: int):
        return NotImplemented
    
    def __rmod__(self, value: int):
        return NotImplemented
    
    def __divmod__(self, value: int, /) -> tuple:
        return NotImplemented
    
    def __rdivmod__(self, value: int):
        return NotImplemented
    
    def __and__(self, value: int):
        return NotImplemented
    
    def __or__(self, value: int):
        return NotImplemented
    
    def __xor__(self, value: int):
        return NotImplemented

    def __lshift__(self, value: int):
        return NotImplemented
    
    def __rshift__(self, value: int):
        return NotImplemented
    
    def __rand__(self, value: int):
        return NotImplemented
    
    def __ror__(self, value: int):
        return NotImplemented
    
    def __rxor__(self, value: int):
        return NotImplemented
    
    def __rlshift__(self, value: int):
        return NotImplemented
    
    def __rrshift__(self, value: int):
        return NotImplemented
    
    def __pos__(self):
        return NotImplemented
    
    def __trunc__(self):
        return NotImplemented
    
    def __ceil__(self):
        return NotImplemented
    
    def __floor__(self):
        return NotImplemented
    #def __round__(self, ndigits: SupportsIndex = ..., /) -> int: ...

    def __getnewargs__(self) -> tuple:
        return NotImplemented
    
    def __eq__(self, value: object) -> bool:
        """
        Implements the logic of equality.

        Args:
            value (object): value to compare.

        Returns:
            bool: If the value is equal to self
                (for mint -- equality of values and moduluses,
                for int and mint to int is not disabled
                -- equality of value mod modulus, otherwise -- false).
        """
        if isinstance(value, mint):
            return self._value == value.value and self._mod == value.mod
        if isinstance(value, int):
            return self._value == value % self._mod and not mint._DISABLE_INT2MINT_CONVERSION
        return False        
    
    def __ne__(self, value: object) -> bool:
        """
        Implements the logic of unequality.

        Args:
            value (object): value to compare.

        Returns:
            bool: inverted value of __eq__ method.
        """
        return not self.__eq__(value)
    
    @_check_value
    def __lt__(self, value) -> bool:
        """
        Implements the logic of comparasion (less).

        Args:
            value (mint|int|bool|float): value to compare.

        Returns:
            bool: If self is less than the value.
        """
        return self._value < value.value
    
    @_check_value
    def __le__(self, value) -> bool:
        """
        Implements the logic of comparasion (less or equal).

        Args:
            value (mint|int|bool|float): value to compare.

        Returns:
            bool: If self is less than or equal to the value.
        """
        return self._value <= value.value
    
    @_check_value
    def __gt__(self, value) -> bool:
        """
        Implements the logic of comparasion (greater).

        Args:
            value (mint|int|bool|float): value to compare.

        Returns:
            bool: If self is greater than the value.
        """
        return self._value > value.value
    
    @_check_value
    def __ge__(self, value: int) -> bool:
        """
        Implements the logic of comparasion (greater or equal).

        Args:
            value (mint|int|bool|float): value to compare.

        Returns:
            bool: If self is greater than equal to the value.
        """
        return self._value >= value.value
    
    def __float__(self) -> float:
        """
        Converts modular int to float
        
        Returns:
            float: modular int converted to float
        """
        return float(self._value)

    def __int__(self) -> int:
        """
        Converts modular int to int
        
        Returns:
            int: modular int converted to int
        """
        return self._value
    
    def to_int(self, base: int = 10):
        """
        Custom method supporting base conversion.
        
        Returns:
            int: modular int with base `base` converted 
                to int with base 10
        """
        if not (2 <= base <= 36):
            raise ValueError("Base must be between 2 and 36.")
        return int(str(self._value), base)
    
    def __abs__(self):
        return NotImplemented
    
    def __hash__(self) -> int: 
        return NotImplemented
    
    def __bool__(self) -> bool:
        return NotImplemented
    
    def __index__(self) -> int:
        return NotImplemented

    def __str__(self) -> str:
        """
        Prints out a number without modulus (informal style).

        Returns:
            str: A number value converted to a string.
        """
        return f"{self._value}"

    def __repr__(self) -> str:
        """
        Prints out a number with modulus (formal style).
        
        Returns:
            str: A formal representation of the class instance.
        """
        return f"{self.__class__.__name__}({self._value}, mod={self._mod})"
    
    def parametric(self, param_name : str = "k") -> str:
        """
        Prints out a number with a variable part.

        Args:
            param_name (str, optional): The variable name for the output.
                Must be represented by one word (no whitespace characters).
                Defaults to "k".
        
        Returns:
            str: A number value with mod * variable.

        Raises:
            ValueError: If there are any whitespace characters in the param_name.
        """
        if re.search(r"\s", param_name):
            raise ValueError("param_name must be represented by one word.")
        
        return f"{self._value} + {self._mod} * {param_name}"
