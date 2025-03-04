'''
Question 1
There is a file named transactions.csv which is a list of purchases and sales.

Write code that loads this data and calculates the total of these purchases and sales.

Take two approaches - one using floats, and one using Decimal objects. Calculate the difference between the two results.

Also, time how long it takes to run your code using floats and using Decimals.

Solution
Let's inspect the file first before we load it:

with open('transactions.csv') as f:
    for _ in range(8):
        print(next(f).strip())
timestamp,account,amount
2020-11-03T02:01:50,6136306,-11.022038
2020-06-19T07:32:00,3369009,-56.825416
2021-01-29T13:29:17,4366765,-87.430871
2020-03-31T09:27:11,3298760,16.161836
2021-01-01T16:05:22,6136306,38.132664
2020-04-06T02:08:50,3369009,-50.402044
2020-01-24T09:28:10,2315918,-29.852735
We can see the CSV format is the standard one, and we have three columns with the headers in the first row.

We could write a function that loads the entire data set into memory and then processes it (adding the amount), but that's inefficient - we could just read the file row by row and keep a cumulative sum of the amount field.

Also, instead of writing two separate functions, one to cast the amount value to a float andthe other to cast it to a Decimal, we'll implement it as a single function and pass to the function an argument indicating whether we want to work with floats, or with Decimals.

import csv
from decimal import Decimal

def sum_amount(f_name, *, as_decimal=False):
    total = 0

    with open(f_name) as f:
        reader = csv.reader(f)
        next(f)  # skip header row
        for row in reader:
            amount_str = row[-1]
            if as_decimal:
                total += Decimal(amount_str)
            else:
                total += float(amount_str)
    return total
Let's run our code for both float and Decimal:

f_name = 'transactions.csv'

total_float = sum_amount(f_name)
print(type(total_float), total_float)
<class 'float'> 116387.51306500046
total_decimal = sum_amount(f_name, as_decimal=True)
print(type(total_decimal), total_decimal)
<class 'decimal.Decimal'> 116387.513065
As you can see, cumulative representation errors, even with two million transactions, is quite close to the exact value we obtained using Decimal objects.

Let's see how timing is impacted by using one versus the other:

from timeit import timeit
time_float = timeit('sum_amount(f_name)', globals=globals(), number=5)
time_float
8.843322478
time_decimal = timeit('sum_amount(f_name, as_decimal=True)', globals=globals(), number=5)
time_decimal
10.276017692
As a percentage:

round((time_decimal - time_float) / time_float * 100, 1)
16.2
So using Decimal was slower than using floats (and of course as the number of transactions increase we can expect this value to grow larger), and the loss of precision was likely acceptable in this particular scenario.

Question 2
Using the same file (transactions.csv), we now want to calculate a fee on each transaction.

Irrespective of whether the transaction was a credit or a debit, we will calculate a 0.123% transaction fee for the (absolute) values of each transaction.

Each fee calculation precision should be limited to 8 digits after the decimal point (so use round(val, 8))

In addition, any rounding should always round ties away from 0 (ROUND_HALF_UP) - and not use Banker's rounding (ROUND_HALF_EVEN).

Only implement this solution using Decimal objects, as floats do not offer a rounding algorithm choice, and writing our own rounding algorithm can be overly complicated.

Also calculate the different in the fee totals when using ROUND_HALF_UP vs ROUND_HALF_EVEN

Solution
Here we'll take the same approach as before - we'll load the file and process rows one by one, keeping a running total of the commissions.

Let's write the basic code first, and we'll worry about rounding later.

def sum_fees(f_name, fee_perc='0.00123'):
    fee_perc = Decimal(fee_perc)
    total = 0

    with open(f_name) as f:
        reader = csv.reader(f)
        next(f)  # skip header row
        for row in reader:
            amount_str = row[-1]
            amount = Decimal(amount_str)
            fee = abs(fee_perc * amount)
            total += fee

    return total
Now, we still have to restrict our fee calculation to 8 digits after the decimal point, and we do not want to use Banker's rounding - instead we need to round ties away from zero always.

Note: we have to round after we calculate the absolute value, otherwise we'll round in the wrong direction for fees on negative amounts.

For Decimal objects changing the rounding is easy, we can use a context to set the rounding mechanism - in this case we'll want to use ROUND_HALF_UP.

Since we want to compare the two rounding methods, we'll pass that in as an argument as well.

import decimal

def sum_fees(f_name, fee_perc='0.00123', *, round_method=decimal.ROUND_HALF_UP, ndigits=8):
    with decimal.localcontext() as ctx:
        ctx.rounding = round_method

        fee_perc = Decimal(fee_perc)
        total = 0

        with open(f_name) as f:
            reader = csv.reader(f)
            next(f)  # skip header row
            for row in reader:
                amount_str = row[-1]
                amount = Decimal(amount_str)
                fee = round(abs(fee_perc * amount), ndigits)
                total += fee

        return total
fees_round_half_up = sum_fees('transactions.csv')
fees_round_half_up
Decimal('125501.66978197')
And now let's specify ROUND_HALF_EVEN for rounding mechanism:

fees_round_half_even = sum_fees('transactions.csv', round_method=decimal.ROUND_HALF_EVEN)
fees_round_half_even
Decimal('125501.66977180')
And the difference between the two results is:

fees_round_half_up - fees_round_half_even
Decimal('0.00001017')
'''