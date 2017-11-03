library(TSP, lib.loc = "~/R/local-packages/")

costs_dframe <- read.csv("cost_matrix.csv", sep=";", header=FALSE)
costs_matrix <- as.matrix(costs_dframe, dimnames=list(1:38, 1:38))

dimnames(costs_matrix) <- list(1:38, 1:38)

atsp <- ATSP(costs_matrix)
tour <- solve_TSP(atsp, method = "nn", start=1L)

write("--RESULTADO DA BIBLIOTECA 'TSP' DO R--", file = "r-tsp-results.txt", append = FALSE)
write("--CAMINHO ENCONTRADO--", file = "r-tsp-results.txt", append = TRUE)
write(as.integer(tour), sep = "-", file = "r-tsp-results.txt", append = TRUE, ncolumns = 100)
write("--CUSTO--", file = "r-tsp-results.txt", append = TRUE)
write(tour_length(tour), file = "r-tsp-results.txt", append = TRUE)

