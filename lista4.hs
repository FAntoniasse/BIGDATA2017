{-Exercício 01: Faça uma função que gere uma matriz identidade de tamanho n.-}

matrixId :: Int -> [[Int]]
matrixId n = [[if i ==j then 1 else 0|j<-[1..n]]|i<-[1..n]]


{-Exercício 02: Faça uma função que calcule a soma da diagonal principal de uma matriz.-}

somaDiagPrinc :: Num a => [[a]] -> a
somaDiagPrinc [] = 0
somaDiagPrinc ((i:_):xs) = i + somaDiagPrinc (map (drop 1) xs)

{-Exercício 03: Faça uma função que calcule a soma da diagonal secundária de uma matriz.-}
somaDiagSec :: Num a => [[a]] -> a
somaDiagSec x = (somaDiagPrinc.reverse) x
