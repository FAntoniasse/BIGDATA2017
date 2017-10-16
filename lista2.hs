{-Exercício 01: Crie uma função ehTriangulo que determina se três lados x, y, z podem formar um triângulo.-}
ehTriangulo :: Double -> Double -> Double -> Bool
ehTriangulo x y z = par1 && par2 && par3 where
    par1 = x + y > z
    par2 = x + z > y
    par3 = y + z > x 
    

{-Exercício 02: Crie uma função tipoTriangulo que determina o tipo do triângulo formado pelos três lados x, y, z.-}
data Tipo = Equilátero | Escaleno | Isósceles deriving (Show)

tipoTriangulo ::  Double -> Double -> Double -> Tipo
tipoTriangulo x y z 
    | par1 && par2 = Equilátero
    | par1 || par2 || par3 = Isósceles 
    | otherwise = Escaleno
    where
        par1 = x == y
        par2 = x == z
        par3 = y == z
{-Exercício 03: Implemente uma função que faz a multiplicação etíope entre dois números.-}
multEtp :: Int -> Int -> Int
multEtp 1 y = y
multEtp x y = multEtp (div x 2) (y * 2) +
    if mod x 2 == 0 then 0 else y

{-Exercício 04: Faça uma função que determine se um número é primo.-}
ehPrimo :: Int -> Bool
ehPrimo n = length [x | x <- [1..n], mod n x == 0] == 2


{-Exercício 05: Faça uma função que calcule a soma dos dígitos de um número.-}

somaDig :: Integral a => a -> a
somaDig 0 = 0
somaDig x = (mod x 10) + somaDig (div x 10)

{-Exercício 06: Faça uma função que calcule a persistência aditiva de um número.-}

persisAd :: Integral a => a -> a
persisAd 0 = 0
persisAd x = 1 + persisAd (div (somaDig x) 10)
    

{-Exercício 07: Faça uma função que calcule o coeficiente binomial de (m,n).-}

coefBin :: Double -> Double -> Double
coefBin n k =  fat n / (fat k * (fat (n-k)) )
    where fat 0 = 1
          fat x = x*fat (x-1) 

{-Exercício 08: Faça uma função que calcule o elemento (i,j) do triângulo de pascal. (i = 0, 1,..,n.  e  j = 0, 1,..,k)   -}

elemTriPascal :: Double -> Double -> Double
elemTriPascal i j = coefBin i j

