class mint(int):

    """Represents an integer number from the specified modular system."""

    # Error raised when attempting operations between different modular systems
    __DIFFERENT_MODULAR_SYSTEMS_ERROR = ValueError(
            '''You cannot directly operate on numbers from 
                different modular systems without first aligning 
                them to a common modulus.'''
        )

    def __new__(cls, value: int, modulus: int):

        """
        Initializes a mint instance.

        Args:
            value (int): the integer number's value.
            modulus (int): the modulus of the system. Must be an integer 
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
        
        if not isinstance(modulus, int):
            raise ValueError("Modulus must be int and not less than 2")
        
        if modulus <= 1:
            raise ValueError("Modulus must be at least 2")
        
        # initializing mint instance
        instance = super(mint, cls).__new__(cls, value % modulus)
        instance.modulus = modulus
        return instance
    
    def __str__(self):

        """Prints out a number without modulus (informal style)."""

        return f"{int(self)}"
    
    def __repr__(self):

        """Prints out a number with modulus (formal style)."""

        return f"{self.__class__.__name__}({self}, mod={self.modulus})"