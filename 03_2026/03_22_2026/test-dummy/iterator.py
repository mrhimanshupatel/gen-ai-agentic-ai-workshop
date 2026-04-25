class Iterator:
    """A basic iterator class that iterates over a range of values."""
    
    def __init__(self, start_val, end_val):
        """Initialize the iterator with start and end values."""
        self.start_val = start_val
        self.end_val = end_val
        self.current = start_val
    
    def __iter__(self):
        """Return the iterator object itself."""
        return self
    
    def __next__(self):
        """Return the next value in the iteration."""
        if self.current >= self.end_val:
            raise StopIteration
        
        value = self.current
        self.current += 1
        return value


# Example usage
if __name__ == "__main__":
    # Create an iterator from 1 to 5
    my_iter = Iterator(1, 6)
    
    print("Iterating from 1 to 5:")
    for num in my_iter:
        print(num)
    
    # Create another iterator from 10 to 15
    my_iter2 = Iterator(10, 16)
    
    print("\nIterating from 10 to 15:")
    for num in my_iter2:
        print(num)
