library(TSP, lib.loc = "~/R/local-packages/")

coordinates <- read.csv("djibouti.csv", sep=";", header=FALSE)
colnames(coordinates) <- c("X", "Y")

etsp <- ETSP(coordinates)
tour <- solve_TSP(etsp, method="nn", start=1)

write("--RESULTADO DA BIBLIOTECA 'TSP' DO R--", file = "r-tsp-results.txt", append = FALSE)
write("--CAMINHO ENCONTRADO--", file = "r-tsp-results.txt", append = TRUE)
write(as.integer(tour), sep = "-", file = "r-tsp-results.txt", append = TRUE, ncolumns = 100)
write("--CUSTO--", file = "r-tsp-results.txt", append = TRUE)
write(tour_length(tour), file = "r-tsp-results.txt", append = TRUE)
