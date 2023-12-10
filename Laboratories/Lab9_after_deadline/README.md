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

We evaluate our results with 30 iterations on each experiments. Here we published the mean values.


PARENT_SELECTION = Roulette
MUTATION = One single bit
REPRODUCTION = Two cut


|          ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| ISLAND STRATEGY |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Base    | Fixed Generation | Random Swap |1.0|23'596.26|0.992|87'507.43|0.345|37'537.77|0.340|34'720.7|
| Base    | Fixed Generation | Ring Topology |1.0|31'325.4|0.9758|154'722.03|0.480|42'044.23|0.333|36'512.1|
| Base    | Fixed Generation | Best Fitness |1.0|33'409.56| 0.959|160'831.06|0.476|34'824.8|0.317|32070.7|
| Base    | Fitness Based | Random Swap |1.0|22'255.46|0.985|99'106.9|0.493|38'394.96|0.356|42'583.8|
| Base    | Fitness Based| Ring Topology |1.0|22'894.96|0.967|162'121.8|0.48539|36'711.3|0.351|45'035.7|
| Base    | Fitness Based | Best Fitness |1.0|22'840.26|0.862|115'951.26|0.507|33'822.43|0.353|39'653.3|

## ISLANDS SEGREGATION

We evaluate our results with 30 iterations on each experiments. Here we published the mean values.

WHEN TO SWAP = Fitness Based
MIGRATION = Random Swap


|          ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| ISLAND STRATEGY |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Island segregation    |Fitness Based | Random Swap |1.0|22941.66|0.9894|100'672.56|0.527|65'083.6|0.375|62'032.83|

## VALHALLA ISLAND

We evaluate our results with 30 iterations on each experiments. Here we published the mean values.


WHEN TO SWAP = Fitness Based
MIGRATION = Random Swap


|          ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| ISLAND STRATEGY |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Valhalla island    |Fitness Based | Random Swap |1.0|27052.68| 0.997 | 107739.93 | 0.495|30052.23|0.345|34369.7|

## EXPERT ISLANDS

We evaluate our results with 30 iterations on each experiments. Here we published the mean values.


WHEN TO SWAP = Fitness Based
MIGRATION = Random Swap


|          ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| ISLAND STRATEGY |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Expert islands    | - | - |0.612|17592.63|0.589|33882.2| 0.453 | 36734.83|0.326|28360.13|

Some hyperparameter tuning combinations:

MU = 15
LAMBDA = 30
COOLDOWN_TIME = 20
NUM_ISLANDS = 50

|          ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| ISLAND STRATEGY |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Expert islands    | - | - | 0.87 | 34896.86 | 0.833 | 34786.0 | 0.74 | 34938.93 | 0.775 | 34856.0 |

MU = 5
LAMBDA = 15
COOLDOWN_TIME = 20
NUM_ISLANDS = 100

|          ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| ISLAND STRATEGY |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Expert islands    | - | - | 1.0 | 16732.73 |1.0| 19462.13 | 1.0 | 18400.26| 0.996| 16953.56|

MU = 3
LAMBDA = 10
COOLDOWN_TIME = 5
NUM_ISLANDS = 250

|          ||| Problem 1 |         | Problem 2 |         | Problem 5 |         | Problem 10 |         |
|----------|-------|-------|-----------|---------|-----------|---------|-----------|---------|------------|---------|
| ISLAND STRATEGY |WHEN TO SWAP|MIGRATION| SCORE     | CALLS | SCORE     | CALLS | SCORE     | CALLS | SCORE      | CALLS |
| Expert islands    | - | - | 1.0 | 2490.06 |1.0| 2564.86 | 1.0 | 2536.93 | 1.0 | 2514.9 |
