# How numbers are named in Danish.

## Numbers less than 10

The first ten numbers is named as so:

| ------ | ------ | ------- |
| Number | Danish | English |
| 0      | Nul    | Zero    |
| 1      | En/Et  | One     |
| 2      | To     | Two     |
| 3      | Tre    | Three   |
| 4      | Fire   | Four    |
| 5      | Fem    | Five    |
| 6      | Seks   | Six     |
| 7      | Syv    | Seven   |
| 8      | Otte   | Eight   |
| 9      | Ni     | Nine    |

The first thing to notice is that the number look an aweful lot like english, but also that we have two different named for 1. It can loosly be compared to the english use of "a" and "an". In danish, every word has a gender being either "intetkøn" (neutrum) og "fælleskøn" (utrum).


| Gender | 1 | Example I | Example II |
| ------ | - | --------- | ---------- |
| Fælleskøn (utrum)  | En | En cykel (A bicycle) | Dreng<em>en</em> (The boy) |
| Intetkøn (neutrum) | Et | Et hus (A house) | Bord*et* (The table)|

These are covered by the functions `danish_names_below_10` and `danish_number_name`.

Sources:

- \[1\] [Fælleskøn](https://da.wikipedia.org/wiki/F%C3%A6llesk%C3%B8n)
- \[2\] [Intetkøn](https://da.wikipedia.org/wiki/Intetk%C3%B8n)

## Number below 20

Below twenty, the number goes like this:

| Number | Danish | English  |
| ------ | ------ | -------  |
| 10     | Ti     | Ten      |
| 11     | Elleve | Elleven  |
| 12     | Tolv   | Twelve   |
| 13     | Tretten| Thirteen |
| 14     | Fjorten| Fourteen |
| 15     | Femten | Fifteen  |
| 16     | Seksten| Sixteen  |
| 17     | Sytten | Seventeen|
| 18     | Atten  | Eightteen|
| 19     | Nitten | Nineteen |

Just like in english, we also see that in danish, the words for 11 and 12 special while the numbers from 13 to 19 are the numbers between 3 to 9 with a "ten" added as a suffix with a twist of language history.

These are covered by the functions `danish_names_below_20` and `danish_number_name`.

## Number below 100

### The tens

Starting with then tens, then the naming pattern goes like:

| Number | Danish    | English  |
| ------ | ------    | -------  |
| 10     | Ti        | Ten      |
| 20     | Tyve      | Twenty   |
| 30     | Tredive   | Thirty   |
| 40     | Fyrre     | Fourty   |
| 50     | Halvtreds | Fifty    |
| 60     | Tres      | Sixty    |
| 70     | Halvfjerds| Seventy  |
| 80     | Firs      | Eighty   |
| 90     | Halvfems  | Ninety   |

Here we se the first big difference between danish and english number-names. In engish we simply take the base number, such as eight, and then add the suffix *-ty* to get *eighty* (80). In danish though, the names are much more interesting.


The keen eyed amoung you would notice the prefix of *halv-* before 50, 70, and 90. If you are really observant, then you would have noticed that the end of "halvtreds" (50) and "treds" (60) look a bit similar. Likewise with 70 and 80. Why is that? We will get to this, but first, lets talk about

#### 10, 20, 30, and 40.

- *Ti* (10) comes from the old norse word *tíu*. \[[3](https://ordnet.dk/ddo/ordbog/ti)\]
- *Tyve* (20) comes from the old norse word *tuttugu* meaning two tens. \[[4](https://ordnet.dk/ddo/ordbog/Tyve)\]
- *Tredive* (30) comes from the old norse word *þrír tigir* meaning three tens. \[[5](https://ordnet.dk/ddo/ordbog/tredive)\]
- *Fyrre* (40) is a short version of *fyrretyve* \[[6](https://ordnet.dk/ddo/ordbog/fyrre)\] which comes from *fjórir tigir* meaning four times ten\[[7](https://ordnet.dk/ddo/ordbog/fyrre?entry_id=11016583)\]. 

#### 60 and 80

- *Treds* (60) is a short version of *tresenstyvende* \[[8](https://ordnet.dk/ddo/ordbog/tres)\] which comes from three times twenty. The same is true *firs* (80) being four times twenty.

#### 50, 70, and 90.

To explain the name of 50, 70, and 90, we first have to know how some fractions are named. 

If you have a half, that is called "en halv" in danish, if you have one-and-a-half, then you would have "halvanden", and if you have two-and-a-half, then you would have "halvtredje" in danish. To explain the origin, lets use two-and-a-half as an example. If you have two-and-a-half kegs of beer, then you will have two full kegs and half of the third. Or in danish *"to hele tønder og **halvdelen** af den **tredje** tønde"*. That sentence is too long, so we short it to *"**halvtredje** tønde".* The same is true for 2.5, 3.5, etc. In summary:

- 0.5 - *En halv* (A half)
- 1.5 - *Halvanden* (One-and-a-half)
- 2.5 - *Halvtredje* (Two-and-a-half)
- 3.5 - *Halvfjerde* (Three-and-a-half)
- 4.5 - *Halvfemte* (Four-and-a-half)

How does that explain the tens? Well 50 is 2.5 times 20, and 70 is 3.5 times 20, and 90 is 4.5 times 20. Combining this with the old danish word *snes* being a substitude for twenty, then 50 is 2.5 times 20, which is *"halvtredje snes"* which shortens to *halvtreds.* The same is true for 70 and 90 being *"halvfjerde snes"* (halvfjerds) and *"halvfemte snes"* (halvfems).

### Combining tens and ones

In english, the name of 51 is simply *fifty* and *one*. In danish, we have a similar system, except that the order is reversed. So 51 is 1 and 50, which translates to "enoghalvtreds". Here the word *og* simply means "and". Another example is 99, which is *nioghalvtems*.

Using these rules all numbers below 100 can be translated into Danish easily.

All numbers below 100 are covered by the functions `danish_names_below_100` and `danish_number_name`.

## Numbers between 100 and 1000.

The danish name for 100 is "hundrede". You count in the same ways as in english, so 100 is "ethundred" (one hundret), 200 is "tohundred" (two hundred), etc. When you have a number such as 521, you will write "femhunderedeogenogtyve". Lets splits that up in parts

- "fem" is five
- "hunderede" is hundred
- "enogtyve" is one-and-twenty so 21.

In summary, if A, B, and C are digits, then **ABC** is "**A** + "hundrede" + **BC**. These are covered by the functions `danish_names_below_1000` and `danish_number_name`. There is an exception though.

For numbers such as 101, you are free to choose if you put an "et" before "hundrede" or not. 101 can therefore either be 'ethundredeoget' or "hundredeoget".

To make both options possible, the `et_before_hundrede` flag can be toggled in the `danish_names_below_1000` and `danish_number_name` functions.

## Numbers below a million

...


## Above a millon

| Order | Number | Danish       | English       |
| ----- | ------ | ------       | -------       |
| (1,1) | $10^{6}$   | Million      | Million       |
| (1,2) | $10^{9}$   | Milliard     | Billion       |
| (2,1) | $10^{12}$  | Billion      | Trillion      |
| (2,2) | $10^{15}$  | Billiard     | Quadrillion   |
| (3,1) | $10^{18}$  | Trillion     | Quintillion   |
| (3,2) | $10^{21}$  | Trilliard    | Sextillion    |
| (4,1) | $10^{24}$  | Kvadrillion  | Heptillion    |
| (4,2) | $10^{27}$  | Kvadrilliard | Octillion     |
| (5,1) | $10^{30}$  | Kvintillion  | Nonillion     |
| (5,2) | $10^{33}$  | Kvintilliard | ...           |
| (6,1) | $10^{36}$  | Sekstillion  | ...           |
| (6,2) | $10^{39}$  | Sekstilliard | ...           |
| (7,1) | $10^{42}$  | Heptillion   | ...           |
| (7,2) | $10^{45}$  | Heptilliard  | ...           |
| (8,1) | $10^{48}$  | Oktillion    | ...           |
| (8,2) | $10^{51}$  | Oktilliard   | ...           |
| (9,1) | $10^{54}$  | Nonillion    | ...           |
| (9,2) | $10^{57}$  | Nonilliard   | ...           |


