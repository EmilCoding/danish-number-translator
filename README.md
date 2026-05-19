# Number in Danish

Have you ever wondered what a number is called in Danish? Yes? Then you should definitly check out this package. Here you can convert any positive number (up to a given limit) into its Danish word representation.


## Notation

The translator function $T: \mathbb{N} \rightarrow str$ maps any positive integer (in principle) to a string representation.

## The small numbers

| Number | Danish | Number | Danish |
| ------ | ------ | ------ | ------ |
| 0      | Nul    | 10     | Ti     |
| 1      | En/Et  | 11     | Elleve |
| 2      | To     | 12     | Tolv   |
| 3      | Tre    | 13     | Tretten|
| 4      | Fire   | 14     | Fjorten|
| 5      | Fem    | 15     | Femten |
| 6      | Seks   | 16     | Seksten|
| 7      | Syv    | 17     | Sytten |
| 8      | Otte   | 18     | Atten  |
| 9      | Ni     | 19     | Nitten |

## The tens

The way Danish construct their numbers between twenty and a hundret, is to take the ones part and the tens part and combine them like this:

$$
    \text{Ones} + "\text{og}" + \text{tens}
$$

The tens can be found in the look-up table below.

| Number | Danish     | Number | Danish     |
| ------ | ------     | ------ | ------     |
| 10     | Ti         | 60     | Tres       |
| 20     | Tyve       | 70     | Halvfjerds |
| 30     | Tredive    | 80     | Firs       |
| 40     | Fyre       | 90     | Halvfems   |
| 50     | Halvtreds  |

An example is

$$
    55 = "Fem" + "og" + "Halvtreds" = "femoghalvtreds"
$$


## From a 100 to 1000

A hundret in Danish is *hundrede*. To construct a number between 100 og 1000 there are different variations. In general, the number is constructed as
$$
    T(abc) = T(a) + "hundrede" + T(bc)
$$
where *a*, *b*, and *c* are digites and $a \ne 0$. An example can be
$$
    T(288) = "To" + "hundrede" + "otto" + "og" + "firs"
$$

Variations:

- You can add a "et" before *hundrede* when naming numbers between 100 and 200. So 101 would be "Et-hundrede-en".
- You can add a *og* between the hundrets part and the tens part. So 151 would be *hundrede-og-en-og-halvtreds*.


## Higher order

Danish uses the long form of naming numbers. That is a thousand millions (*tusind millioner*) is called *en milliard* and thousand of those are called *en billion*. Compared to english where it goes
$$
    Million \rightarrow Billion \rightarrow Trillion \rightarrow ...
$$
the long form add extra form in between,
$$
    Million \rightarrow Milliard \rightarrow Billion \rightarrow Billiard \rightarrow Trillion \rightarrow ...
$$

| Number    | Danish      | Number    | Danish          |
| -----     | ------      | -----     | ------          |
| $10^{6}$  | Million     | $10^{9}$  | Million         |
| $10^{12}$ | Billion     | $10^{15}$ | Billiard        |
| $10^{18}$ | Trillion    | $10^{21}$ | Trilliard       |
| $10^{24}$ | Kvadrillion | $10^{27}$ | Kvardrilliard   |
| $10^{30}$ | Kvintillion | $10^{33}$ | Kvintilliard    |
| $10^{36}$ | Sekstillion | $10^{39}$ | Sekstilliard    |


## Even higher powers

Following the pattern in the large numbers, the pattern is every sixth order of ten yields a new prefix. The prefix pattern in

$$
    Bi- \rightarrow Tri- \rightarrow Kvart- \rightarrow Kvint- \rightarrow Seks- \rightarrow Sep- \rightarrow Okt- \rightarrow ...
$$


| Order | Prefix       | Order | Prefix       |
| ----- | ---          | ----- | ---          |
| 1     | Mi           | 11    | undeci       |
| 2     | Bi           | 12    | duodeci      |
| 3     | Tri          | 13    | tredeci      |
| 4     | Kvart        | 14    | quattuordeci |
| 5     | Kvint        | 15    | quindeci     |
| 6     | Seks         | 16    | sedeci       |
| 7     | Sep          | 17    | septendeci   |
| 8     | Okt          | 18    | octodeci     |
| 9     | Non          | 19    | novendeci    |
| 10    | Dec          | 20    | viginti      |


21 unvigintillion
22 duovigintillion
23 tresvigintillion
24 quattuor­vigint­illion
25 quinvigintillion
26 sesvigintillion
27 septemvigintillion
28 octovigintillion
29 novemvigintillion

30	trigintillion
40	quadragintillion
50	quinquagintillion
60	sexagintillion
70	septuagintillion
80	octogintillion
90	nonagintillion
100	centillion



Source:
- [1] [Long and short scales](https://en.wikipedia.org/wiki/Names_of_large_numbers)
- [2] [Names of large numbers](https://en.wikipedia.org/wiki/Names_of_large_numbers)
- [3] [Den lange og den korte skala for store tal](https://da.wikipedia.org/wiki/Den_lange_og_den_korte_skala_for_store_tal)
