# Implementação inicial de busca tabu em TSP
# Requisitos
*   Python 3.x (testado na versão 3.6);
*   `numpy`.

# Como é que eu rodo isso?
Copiado da ajuda do `argparse`...
```
usage: busca.py [-h] [-i I] [-l L] [-v] [-o] [-s S] DATA

positional arguments:
  DATA        Caminho do arquivo de dados

optional arguments:
  -h, --help  show this help message and exit
  -i I        Número de iterações
  -l L        Comprimento da lista tabu
  -v          Habilitar modo verboso
  -o          Retornar caminho e custo apenas
  -s S        Valor do 'seed'
```

Um exemplo de execução usando o ```bash```

```bash
python3 busca.py -i 50 -l 25 -s 1 djibuti.txt
```
