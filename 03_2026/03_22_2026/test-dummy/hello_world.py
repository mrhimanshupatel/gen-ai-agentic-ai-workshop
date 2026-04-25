from calculator import Calculator
from iterator import Iterator

# Create an instance of Calculator and call the add method
calc = Calculator()
result = calc.add(10, 20)
print(f"The sum of 10 and 20 is: {result}")

# Test with more numbers
result2 = calc.add(5, 10, 15, 20, 25, 30)
print(f"The sum of numbers passed is: {result2}")

#Test iterator
print("\nTesting the Iterator class:")
my_iter = Iterator(1, 6)
for num in my_iter:
    print(num)