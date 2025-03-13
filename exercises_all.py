'''
Question 1
There is a file named transactions.csv which is a list of purchases and sales.

Write code that loads this data and calculates the total of these purchases
and sales.

Take two approaches - one using floats, and one using Decimal objects.
Calculate the difference between the two results.

Also, time how long it takes to run your code using floats and using Decimals.

Question 2
Using the same file (transactions.csv), we now want to calculate a fee on each
transaction.

Irrespective of whether the transaction was a credit or a debit, we will
calculate a 0.123% transaction fee for the (absolute) values of each
transaction.

Each fee calculation precision should be limited to 8 digits after the decimal
point (so use round(val, 8))

In addition, any rounding should always round ties away from 0 (ROUND_HALF_UP)
- and not use Banker's rounding (ROUND_HALF_EVEN).

Only implement this solution using Decimal objects, as floats do not offer a
rounding algorithm choice, and writing our own rounding algorithm can be
overly complicated.

Also calculate the different in the fee totals when using ROUND_HALF_UP vs
ROUND_HALF_EVEN
'''