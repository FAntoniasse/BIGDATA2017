--module Main where
import Data.List
import Data.Maybe
{-Exercício 01: Crie uma função divisivel20 x que retorna verdadeiro se x for divisível por todos os números de 1 a 20.-}

isdiv :: Int -> Int -> Bool
isdiv x y 
    | mod x y == 0 = True
    | otherwise = False

divisivel20 :: Int -> Bool
divisivel20 x = all (x`isdiv`) [1..20] 

{-Exercício 02: Crie uma função projectEuler5 que retorna o primeiro número natural que retorna True para 
a função do exercício anterior. Pense em como reduzir o custo computacional.-}

projectEuler5 :: Int -> Int
projectEuler5 x 
    | divisivel20 x = x
    | otherwise = projectEuler5 (x+1)

{-Exercício 03: Crie a lista de números de Fibonacci utilizando uma função geradora.-}

fib :: Int -> Int
fib x = floor ( (par1 - par2) / sqrt 5)
    where
        par1 = ((1 + sqrt(5))/2.0)**(fromIntegral) x
        par2 = ((1 - sqrt(5))/2.0)**(fromIntegral) x

listFib :: Int -> [Int]

listFib x = [fib xs | xs <-[1..x]]

{-Exercício 04: Utilizando a lista anterior, calcule a soma dos números de Fibonacci pares 
dos valores que não excedem 4.000.000. (Project Euler 2)-}

fsum :: Int -> Int
fsum x = sum $ listFib x

fes :: Int -> Int
fes x = foldl (\a b -> if (b <= 4000000 && isdiv b 2) then a+b else a ) 0 $ listFib x


{-Exercício 05: Faça uma função para calcular o produto escalar entre dois vetores.-}

prod :: Num a => [a] -> [a] -> a
prod [] [] = 0
prod (x:xs) (y:ys) = x*y + prod xs ys
 

{-Exercício 06: Crie a função collatz x que retorna x/2, se x for par e (3x+1) se for ímpar.-}

collatz :: Int ->  Int
collatz x    
    | mod x 2 == 0 = div x 2
    | otherwise = 1 + 3*x

{- Exercício 07: Implemente uma função collatzLen x que retorna o tamanho da lista formada pela aplicação repetida de collatz sobre o valor x até que essa chegue no número -}

collatzLen :: Int -> Int
collatzLen 2 = 1
collatzLen x = 1 + collatzLen (collatz x) 

{-Exercício 08: Encontre o número x entre 1 e 1.000.000 que tem a maior sequência de Collatz. -}




f =fromJust $ fmap ([1..1000000]!!) (elemIndex (maximum a) a) 
    where a = map collatzLen [1..1000000]
