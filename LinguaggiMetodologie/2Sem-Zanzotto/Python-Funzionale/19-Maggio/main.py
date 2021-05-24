convertiAInt = lambda n: n(lambda x: x + 1)(0)

zero = lambda f: lambda x: x
uno = lambda f: lambda x: f(x)

successore = lambda n: lambda f: lambda x: f(n(f)(x))

# lambda n: lambda f: lambda x: f( (n) (f) (x) )  (lambda f: lambda x: x) <- zero
# lambda f: lambda x: f( ((lambda f: lambda x: x)) (f) (x) )
# lambda f: lambda x: f( (lambda x: x) (x) )
# lambda f: lambda x: f(x) <- uno!!!

# la somma non la capisco. è un mindfuck

print(convertiAInt(successore(successore(successore(uno)))))
