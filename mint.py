from functools import wraps
import inspect
import re

class mint(int):

    """Represents an integer number from the specified modular system."""

    #ToDo: property func or setter; make mod final
    DISABLE_INT2MINT_CONVERSION = False
    """
    Flag that defines behaviour of operations between int and mint. True means 
    these operations are undefined, False -- defined. Defaults to False.
    """

    # Error raised when attempting operations between different modular systems
    _DIFFERENT_MODULAR_SYSTEMS_ERROR = ValueError(
            '''You cannot directly operate on numbers from 
                different modular systems without first aligning 
                them to a common modulus.'''
        )


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
        instance.mod = mod
        return instance
    

    def __neg__(self):

        """
        Implements unary minus - behaviour.
        
        Returns:
            mint: A new instance of the modular integer
                which is equal to -previous_value.
        """

        return self.__class__(-int(self), self.mod)
    

    def __invert__(self):
        
        """
        Implements modular int inversion (~ operation).
        
        Returns:
            mint: A new instance of the modular integer
                which is equal to inverted previous value.
        """

        return self.__class__(~int(self), self.mod)


    @staticmethod
    def _check_value(method):

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
                if self.mod != value.mod:
                    raise mint._DIFFERENT_MODULAR_SYSTEMS_ERROR
                return method(self, value)
            elif isinstance(value, int):
                if mint.DISABLE_INT2MINT_CONVERSION:
                    raise TypeError(f"Int to modular int conversion was disabled, \
                        so the {method.__name__}() cannot be done.")
                return method(self, self.__class__(value, self.mod))
            return NotImplemented
        return wrapper

    
    @_check_value
    def __add__(self, value):

        """
        Impements the addition of 2 modular integers or 
        modular integer and integer.

        See __check_value decorator
        """
        return self.__class__(super().__add__(value), self.mod)
    
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

        if mint.DISABLE_INT2MINT_CONVERSION:
            # Check the call stack
            stack = inspect.stack()
            caller_class = stack[1].frame.f_locals.get("self", None)
            
            if not isinstance(caller_class, mint):
                raise TypeError("mint to int conversion was disabled.")
            
        return super().__int__()
    
    
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

        return f"{self.__class__.__name__}({self}, mod={self.mod})"
    

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
        
        return f"{self} + {self.mod} * {param_name}"