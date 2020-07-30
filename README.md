# Mathematics Dataset translated into Russian

This is a Russian version of Mathematics Dataset. 
Original dataset - https://github.com/deepmind/mathematics_dataset/

This dataset was created by manually translating the math question templates used in the original dataset. I tried to go for a literal translation where it was possible, however some changes had to be made due to language difference (Russian has cases and grammatical gender, noun agreement rules are more complicated, pm/am is not used when describing time etc.). All the other components of the original work (inference rules, coverage of mathematical areas, validation) were left intact. 

## Example questions (English and Russian for comparison)

```
Question: Solve -42*r + 27*c = -1167 and 130*r + 4*c = 372 for r.  
Вопрос: Решите -42*r + 27*c = -1167 и 130*r + 4*c = 372 для r.  
Answer: 4. 
Ответ: 4. 

Question: Calculate -841880142.544 + 411127.  
Вопрос: Вычислите -841880142.544 + 411127.  
Answer: -841469015.544 
Ответ: -841469015.544 

Question: Let x(g) = 9*g + 1. Let q(c) = 2*c + 1. Let f(i) = 3*i - 39. Let w(j) = q(x(j)). Calculate f(w(a)).  
Вопрос: Пусть x(g) = 9*g + 1. Пусть q(c) = 2*c + 1. Пусть f(i) = 3*i - 39. Пусть w(j) = q(x(j)). Вычислите f(w(a)).  
Answer: 54*a - 30  
Ответ: 54*a - 30  

Question: Let e(l) = l - 6. Is 2 a factor of both e(9) and 2?  
Вопрос: Пусть e(l) = l - 6. Является ли 2 делителем e(9) и 2?
Answer: False
Ответ: False

Question: What is 0.000006070099 rounded to six decimal places?
Вопрос: Сколько получится, если 0.000006070099 округлить до шести знаков после запятой?  
Answer:  0.000006
Ответ: 0.000006

```

## Pre-generated data

Pre-generated dataset of 11 mln question can be downloaded from here - https://drive.google.com/file/d/1sTDX80Jj5z0M_caoHWjvh7EQVG6Qn_Fc/view?usp=sharing


## Usage

This dataset can be used the same way as the original. 

```shell
python mathematics_dataset_russian/generate.py --filter=linear_1d
```

```shell
python mathematics_dataset_russian/generate_to_file.py --output_dir=dataset/numbers --filter=numbers
```

### Install

You can install it by cloning the mathematics_dataset_russian
repository (no pip installation so far):

```shell
$ git clone https://github.com/mannefedov/mathematics_dataset_russian
```


