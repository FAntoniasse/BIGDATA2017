import Data.Char
{-Exercício 01: Execute as seguintes operações utilizando o menor número de parênteses:-}

--2*3 + 5                 - OK
--2 + 2*3 + 1             - Ok
--3**4 + 5*2**5 + 1       - Ok
--Todas as sentenças não necessitam de parênteses




{-Exercício 02: Faça uma função mult3 x que retorne True caso a entrada seja múltiplo de 3 e False caso contrário.-}

mult3x :: Int -> Bool
mult3x x | mod x 3 ==0 = True
         | otherwise = False


{-
Exercício 03: Faça uma função mult5 x que retorne True caso a entrada seja múltiplo de 5 e False caso contrário.-}

mult5x :: Int -> Bool
mult5x x | rem x 5 ==0 = True
         | otherwise = False

{-
Exercício 04: Faça uma função mult35 x que retorne True caso a entrada seja múltiplo de 3 e 5 e False caso contrário.-}

mult35x :: Int -> Bool
mult35x x | mod x 3 == 0 && mod x 5 == 0 = True
          | otherwise = False

{-
Exercício 05: Faça um programa que retorne True caso a entrada seja menor que -1 ou (maior que 1 E múltiplo de 2), e False caso contrário.-}

verifica :: Int -> Bool
verifica x | x < -1 || (x > 1 && x`rem`2 == 0) = True
           | otherwise = False


{-Exercício 06: Faça uma função que recebe um tipo Integer e retorna ele dividido por 2:

div2d :: Integer -> Double-}

div2d :: Int -> Double
div2d x = (fromIntegral x) / 2


{-
Exercício 07: Faça uma função que receba um ângulo a e retorne uma tupla contendo o seno da metade desse ângulo utilizando a identidade:-}
seno :: Double -> Double
seno x = sqrt ((1 - cos (transf x))/2)
    where transf x = ( x * pi ) / 180

senoPorDois :: Double -> (Double,Double)
senoPorDois x = (seno x, - seno x)



{-
Exercício 08: Crie uma lista de anos bissextos desde o ano 1 até o atual.-}
bissex :: [Int] -> [Int] 
bissex xs = [x | x<-xs, (mod x 4 ==0) && ( (mod x 100 /=0) || (mod x 100 ==0 && mod x 400 /=0))]
bissex1 = do
    print (bissex [1..2017])


{-
Exercício 09: Encontre os 10 primeiros anos bissextos.-}
--bissex :: [Int] -> [Int] 
--bissex xs = [x | x<-xs, (mod x 4 ==0) && ( (mod x 100 /=0) || (mod x 100 ==0 && mod x 400 /=0))]
bissex2 = do
    print (take 10 $ bissex [1..2017])

{-
Exercício 09: Encontre os 10 últimos anos bissextos (dica: use a função length para determinar o tamanho da lista).-}
--bissex :: [Int] -> [Int] 
--bissex xs = [x | x<-xs, (mod x 4 ==0) && ( (mod x 100 /=0) || (mod x 100 ==0 && mod x 400 /=0))]
bissex3 = do
    print (take 10 $ bissex [2017,2016..])



{-
Exercício 10: Crie uma tupla em que o primeiro elemento tem metade dos anos bissextos e o segundo elemento a outra metade.-}
metade :: Int -> Int
metade x = div x 2

bissex4 = do
    print ( (bissex [1..metade 2017] , bissex [metade 2017 +1 .. 2017]  )  )


{-
Exercício 11: Crie um concatenador de strings que concatena duas strings separadas por espaço.-}
concat3 :: String -> String
concat3 = filter (`notElem` " ") 

{- Exercício 12: Dada a string “0123456789”, crie uma lista com os dígitos em formato Integer.-}



conv :: [Char] -> [Int]
conv [] = []
conv (x:xs) = digitToInt x:conv(xs) 

converter = do
   print (conv "0123456789")
