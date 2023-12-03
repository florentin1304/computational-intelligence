# Lab09 done with [Claudio Savelli](https://github.com/ClaudioSavelli/computational-intelligence-PoliTO/tree/main/Laboratory%20Activities/Lab3), [Luca Catalano](https://github.com/LucaCatalano13/Computational-Intelligence/tree/main)!

# BASELINE

We evaluate our results with 10 iterations on each experiments. Here we published the mean values.

HYPERPARAMETER

MU = 15

LAMBDA = 30

MUTATION_PROB = 0.2

DYNAMIC_MUTATION_PROB = True

DIVERSITY_THRESHOLD = 20

LENGTH_SOLUTION = 1000

NUMBER_GENERATIONS = 3_000

COOLDOWN_TIME = 100

|          |                  |                 |                   | Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|------------------|---------------- |-------------------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| STRATEGY | PARENT SELECTION | MUTATION        | REPRODUCTION      | SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Comma    | Roulette         | One single bit  | Uniform crossover |0.999|14771|0.512|7038|0.361|9916|0.215|19588|       |         |
| Comma    | Roulette         | One single bit  | One cut           |0.995|18574|0.520|6849|0.341|13047|0.208|21881|       |         |
| Comma    | Roulette         | One single bit  | Two cut           |0.999|6480|0.788|9218|0.429|7454|0.324|5828|       |         |
| Comma    | Roulette         | 3 bit           | Uniform crossover |0.988|15770|0.518|9170|0.451|5024|0.358|7052|       |         |
| Comma    | Roulette         | 3 bit           | One cut           |0.944|18239|0.519|7003|0.456|6469|0.300|6696|         |
| Comma    | Roulette         | 3 bit           | Two cut           |0.993|8761|0.706|5984|0.467|6986|0.3413|7334|       |         |
| Comma    | Torunament       | One single bit  | Uniform crossover |0.999|15240|0.518|7505|0.282|3182|0.170|3320|       |         |
| Comma    | Torunament       | One single bit  | One cut           |0.997|22151|0.515|7271|<span style="color:green">**0.270**</span>|<span style="color:green">**3176**</span>|0.172|12037|       |         |
| Comma    | Torunament       | One single bit  | Two cut           |0.999|8698|0.729|7826|0.386|6092|0.324|7226|       |         |
| Comma    | Torunament       | 3 bit           | Uniform crossover |0.991|16358|0.493|8744|0.228|3236|<span style="color:green">**0.209**</span>|<span style="color:green">**3218**</span>|       |         |
| Comma    | Torunament       | 3 bit           | One cut           |0.940|18645|0.513|8052|0.276|3318|0.239|3665|       |         |
| Comma    | Torunament       | 3 bit           | Two cut           |0.992|10705|0.691|9746|0.375|5816|<span style="color:red">**0.371**</span>|<span style="color:red">**8486**</span>|       |         |
| Plus     | Roulette       | One single bit    | Uniform crossover |1.0|11372|<span style="color:green">**0.561**</span>|<span style="color:green">**3471**</span>|0.293|12338|0.208|18163|       |         |
| Plus     | Roulette       | One single bit  | One cut           |0.999|14080|0.529|5106|0.338|12670|0.188|22267|       |         |
| Plus     | Roulette       | One single bit  | Two cut           |<span style="color:red">**1.0**</span>|<span style="color:green">**5213**</span>|0.843|14273|0.411|15367|0.317|11821|       |         |
| Plus     | Roulette       | 3 bit           | Uniform crossover |0.996|16628|0.778|15241|<span style="color:red">**0.543**</span>|<span style="color:red">**65352**</span>|0.277|67285|       |         |
| Plus     | Roulette       | 3 bit           | One cut           |0.992|25869|0.572|5758|0.526|74580|0.291|68960|       |         |
| Plus     | Roulette       | 3 bit           | Two cut           |0.998|8952|0.768|13075|0.449|8303|0.305|4422|       |         |
| Plus     | Torunament         | One single bit  | Uniform crossover |1.0|13495|0.891|33415|0.423|15736|0.263|13852|       |         |
| Plus     | Torunament         | One single bit  | One cut           |1.0|18762|0.895|43254|0.266|19080|0.231|21508|       |         |
| Plus     | Torunament         | One single bit  | Two cut           |1.0|6260|<span style="color:red">**0.999**</span>|<span style="color:red">**23795**</span>|0.419|6450|0.302|6599|       |         |
| Plus     | Torunament         | 3 bit  | Uniform crossover |0.999|15831|0.799|32837|0.484|46579|0.309|51759|       |         |
| Plus     | Torunament         | 3 bit           | One cut           |0.999|30925|0.880|52846|0.533|83469|0.266|58839|       |         |
| Plus     | Torunament         | 3 bit           | Two cut           |0.999|10689|0.995|31199|0.391|7752|0.305|6406|       |         |


## ISLANDS

We evaluate our results with 10 iterations on each experiments. Here we published the mean values.

HYPERPARAMETER

MU = 15

LAMBDA = 30

MUTATION_PROB = 0.2

DYNAMIC_MUTATION_PROB = True

DIVERSITY_THRESHOLD = 20

LENGTH_SOLUTION = 1000

NUMBER_GENERATIONS = 3_000

COOLDOWN_TIME = 100

NUM_ISLANDS = 5

|          |                  |                 |                   ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|------------------|---------------- |-------------------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| STRATEGY | PARENT SELECTION | MUTATION        | REPRODUCTION      |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Plus    | Roulette         | One single bit  | Two cut            |Fitness |Fitness |0.753|112338|0.769|79672|0.4624|32396|0.357|43093|

## ISLANDS SEGREGATION

We evaluate our results with 10 iterations on each experiments. Here we published the mean values.

HYPERPARAMETER

MU = 15

LAMBDA = 30

MUTATION_PROB = 0.2

DYNAMIC_MUTATION_PROB = True

DIVERSITY_THRESHOLD = 20

LENGTH_SOLUTION = 1000

NUMBER_GENERATIONS = 3_000

COOLDOWN_TIME = 100

|          |                  |                 |                   ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|------------------|---------------- |-------------------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| STRATEGY | PARENT SELECTION | MUTATION        | REPRODUCTION      |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Plus    | Roulette         | One single bit  | Two cut            |Fitness |Fitness |<span style="color:red">**1.0**</span>|<span style="color:red">**22378**</span>|<span style="color:red">**0.999**</span>|<span style="color:red">**72020**</span>|<span style="color:red">**0.565**</span>|<span style="color:red">**51970**</span>|<span style="color:red">**0.443**</span>|<span style="color:red">**70072**</span>|