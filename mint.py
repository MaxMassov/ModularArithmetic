import re

class mint(int):

    """Represents an integer number from the specified modular system."""

    # Error raised when attempting operations between different modular systems
    __DIFFERENT_MODULAR_SYSTEMS_ERROR = ValueError(
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