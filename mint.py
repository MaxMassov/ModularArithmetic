from functools import wraps
import inspect
from typing import Callable
import re

class mint(int):

    """Represents an integer number from the specified modular system."""

    #ToDo: property func or setter
    _DISABLE_MINT2INT_CONVERSION = False
    """
    Flag that defines behaviour of operations between int and mint. True means 
    these operations are undefined, False -- defined. Defaults to False.
    """

    def __new__(cls, value: int, mod: int):

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
        instance = super(mint, cls).__new__(cls, value % mod)
        instance._mod = mod # modulus cannot be changed
        return instance
    

    @property
    def mod(self):

        """Read-only property for modulus."""
        
        return self._mod
    

    def __setattr__(self, name, value):

        """
        Makes modulus read-only.
        
        Raises:
            AttributeError: When name == _mod
        """

        if hasattr(self, '_mod') and name == '_mod':
            raise AttributeError(f"{name} is read-only.")
        super().__setattr__(name, value)


    @property
    def mint2int(self) -> bool:

        """Access to mint._DISABLE_MINT2INT_CONVERSION value."""
        
        return mint._DISABLE_MINT2INT_CONVERSION


    @classmethod
    def set_mint2int(cls, value: bool):

        """
        Set mint._DISABLE_MINT2INT_CONVERSION to a `value`
        
        Arguments:
            value (bool): new value of mint._DISABLE_MINT2INT_CONVERSION 
                (can be int, but must be equal to either 1 or 0).
        
        Raises:
            ValueError: If value has not a relevant value.
        """

        if isinstance(value, int) and (value == 1 or value == 0):
            value = bool(value)
        if isinstance(value, bool):
            cls._DISABLE_MINT2INT_CONVERSION = value
        else:
            raise ValueError("mint._DISABLE_MINT2INT_CONVERSION must be bool.")
    

    @classmethod
    def change_mint2int(cls):

        """
        Set mint._DISABLE_MINT2INT_CONVERSION to the opposite value
        """
        
        cls._DISABLE_MINT2INT_CONVERSION = not cls._DISABLE_MINT2INT_CONVERSION


    @classmethod
    def activate_mint2int(cls):

        """
        Set mint._DISABLE_MINT2INT_CONVERSION to False
        """
        
        cls._DISABLE_MINT2INT_CONVERSION = False


    @classmethod
    def disable_mint2int(cls):

        """
        Set mint._DISABLE_MINT2INT_CONVERSION to True
        """
        
        cls._DISABLE_MINT2INT_CONVERSION = True


    def __neg__(self):

        """
        Implements unary minus - behaviour.
        
        Returns:
            mint: A new instance of the modular integer
                which is equal to -previous_value.
        """

        return self.__class__(-int(self), self._mod)
    

    def __invert__(self):
        
        """
        Implements modular int inversion (~ operation).
        
        Returns:
            mint: A new instance of the modular integer
                which is equal to inverted previous value.
        """

        return self.__class__(~int(self), self._mod)


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
                value (mint|int): the value to which the method will be applied.

            Returns:
                mint: A new instance of the modular integer
                    which is equal to result of applying
                    method to self value and given value.

            Raises:
                TypeError: If more or less than one arrgument is given.
                ValueError: If the given mint value is not from the same
                    modular system as self.
                TypeError: If the value is instance of int (not mint),
                    but int to mint conversion disabled.
            """

            value = None
            if len(args) == 1:
                value = args[0]
            elif len(kwargs.values()) == 1:
                value = kwargs.values()[0]
            if value is None:
                raise TypeError(f"Method {method.__name__}() takes one argument \
                                ({len(args) + len(kwargs.values())} given).")
            
            if isinstance(value, mint):
                if self._mod != value.mod:
                    raise ValueError(
                            '''You cannot directly operate on numbers from 
                                different modular systems without first aligning 
                                them to a common modulus.'''
                        )
                return method(self, value)
            if isinstance(value, float):
                value = int(value)
            elif isinstance(value, bool):
                value = int(value)
            if isinstance(value, int):
                if mint._DISABLE_MINT2INT_CONVERSION:
                    raise TypeError(f"Int to modular int conversion was disabled, \
                        so the {method.__name__}() cannot be done.")
                return method(self, self.__class__(value, self._mod))
            return NotImplemented
        return wrapper

    
    @_check_value
    def __add__(self, value):

        """
        Impements the addition of 2 modular integers or 
        modular integer and integer.

        See __check_value decorator
        """
        return self.__class__(super().__add__(value), self._mod)
    
    def __radd__(self, value):
        return NotImplemented
    
    def __sub__(self, value):
        return NotImplemented
    
    def __rsub__(self, value):
        return NotImplemented

    def __mul__(self, value):
        return NotImplemented
    
    def __rmul__(self, value):
        return NotImplemented
    
    def __pow__(self, value):
        return NotImplemented
    
    def __rpow__(self, value: int):
        return NotImplemented

    def __floordiv__(self, value):
        return NotImplemented
    
    def __rfloordiv__(self, value: int):
        return NotImplemented
    
    def __truediv__(self, value):
        return self.__floordiv__(value)
    
    def __rtruediv__(self, value: int):
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
    
    def __eq__(self, value: object):
        return NotImplemented
    
    def __ne__(self, value: object):
        return NotImplemented
    
    def __lt__(self, value: int):
        return NotImplemented
    
    def __le__(self, value: int):
        return NotImplemented
    
    def __gt__(self, value: int):
        return NotImplemented
    
    def __ge__(self, value: int):
        return NotImplemented
    
    def __float__(self) -> float:
        return NotImplemented
    

    def __int__(self) -> int:

        """
        Converts modular int to int
        
        Returns:
            int: modular int converted to int

        Raises:
            TypeError: When mint to int conversion was disabled
                and method was called out of the class
        """

        if mint._DISABLE_MINT2INT_CONVERSION:
            # Check the call stack
            stack = inspect.stack()
            caller_class = stack[1].frame.f_locals.get("self", None)
            
            if not isinstance(caller_class, mint):
                raise TypeError("mint to int conversion was disabled.")
            
        return super().__int__()
    

    def to_int(self, base: int = 10):

        """
        Custom method supporting base conversion.
        
        Returns:
            int: modular int with base `base` converted 
                to int with base 10
        
        Raises:
            See __int__() method 
        """

        if not (2 <= base <= 36):
            raise ValueError("Base must be between 2 and 36.")
        return int(str(self), base)
    
    
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

        return f"{int(self)}"
    

    def __repr__(self) -> str:

        """
        Prints out a number with modulus (formal style).
        
        Returns:
            str: A formal representation of the class instance.
        """

        return f"{self.__class__.__name__}({self}, mod={self._mod})"
    

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
        
        return f"{self} + {self._mod} * {param_name}"
