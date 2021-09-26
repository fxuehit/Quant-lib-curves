import math
import matplotlib.pyplot as plt
import QuantLib as QL
import datetime as dt
import json

from QuantLib import Date, Days, Weeks, Months, Years, Period, January, February, March, April, May, June, \
    July, August, September, October, December, November
from QuantLib import SimpleQuote, DepositRateHelper, FraRateHelper, SwapRateHelper, OISRateHelper, \
    DatedOISRateHelper, PiecewiseFlatForward, PiecewiseCubicZero, RelinkableYieldTermStructureHandle, QuoteHandle
from QuantLib import Eonia, Euribor, Euribor3M, Euribor1M, Euribor6M
from QuantLib import Simple, Actual365Fixed, Actual360, Thirty360, Annual, Unadjusted, Following
from QuantLib import TARGET


def build_eur():
    # MARKET DATA

    Curves = dict()

    calendar = TARGET()
    today = Date(11, December, 2012)
    QL.Settings.instance().evaluationDate = today
    fixingDays = 2
    settlementDate = calendar.adjust(calendar.advance(today, fixingDays, Days))

    print('Today: {}'.format(today.weekday()))
    print('Settlement date:: {}'.format(settlementDate.weekday()))

    depositDayCounter = Actual360()
    termStructureDayCounter = Actual365Fixed()

    # deposit
    dONRate = QuoteHandle(SimpleQuote(0.0004))
    dTNRate = QuoteHandle(SimpleQuote(0.0004))
    dSNRate = QuoteHandle(SimpleQuote(0.0004))

    # OIS swap
    ois1WRate = QuoteHandle(SimpleQuote(0.00070))
    ois2WRate = QuoteHandle(SimpleQuote(0.00069))
    ois3WRate = QuoteHandle(SimpleQuote(0.00078))
    ois1MRate = QuoteHandle(SimpleQuote(0.00074))
    ois15MRate = QuoteHandle(SimpleQuote(0.00002))
    ois18MRate = QuoteHandle(SimpleQuote(0.00008))
    ois21MRate = QuoteHandle(SimpleQuote(0.00021))
    ois2YRate = QuoteHandle(SimpleQuote(0.00036))
    ois3YRate = QuoteHandle(SimpleQuote(0.00127))
    ois4YRate = QuoteHandle(SimpleQuote(0.00274))
    ois5YRate = QuoteHandle(SimpleQuote(0.00456))
    ois6YRate = QuoteHandle(SimpleQuote(0.00647))
    ois7YRate = QuoteHandle(SimpleQuote(0.00827))
    ois8YRate = QuoteHandle(SimpleQuote(0.00996))
    ois9YRate = QuoteHandle(SimpleQuote(0.01147))
    ois10YRate = QuoteHandle(SimpleQuote(0.0128))
    ois11YRate = QuoteHandle(SimpleQuote(0.01404))
    ois12YRate = QuoteHandle(SimpleQuote(0.01516))
    ois15YRate = QuoteHandle(SimpleQuote(0.01764))
    ois20YRate = QuoteHandle(SimpleQuote(0.01939))
    ois25YRate = QuoteHandle(SimpleQuote(0.02003))
    ois30YRate = QuoteHandle(SimpleQuote(0.02038))

    # Meeting date swap
    oisDated1Rate = QuoteHandle(SimpleQuote(0.000460))
    oisDated2Rate = QuoteHandle(SimpleQuote(0.000160))
    oisDated3Rate = QuoteHandle(SimpleQuote(-0.000070))
    oisDated4Rate = QuoteHandle(SimpleQuote(-0.000130))
    oisDated5Rate = QuoteHandle(SimpleQuote(-0.000140))

    # Deposit Instrument

    dON = DepositRateHelper(dONRate, Period(1, Days), 0, TARGET(), Following, False, depositDayCounter)
    dTN = DepositRateHelper(dTNRate, Period(1, Days), 1, TARGET(), Following, False, depositDayCounter)
    dSN = DepositRateHelper(dSNRate, Period(1, Days), 2, TARGET(), Following, False, depositDayCounter)

    # OIS Swap Instrument
    eonia = Eonia()
    ois1W = OISRateHelper(2, Period(1, Weeks), ois1WRate, eonia)
    ois2W = OISRateHelper(2, Period(2, Weeks), ois2WRate, eonia)
    ois3W = OISRateHelper(2, Period(3, Weeks), ois3WRate, eonia)
    ois1M = OISRateHelper(2, Period(1, Months), ois1MRate, eonia)

    ois15M = OISRateHelper(2, Period(15, Months), ois15MRate, eonia)
    ois18M = OISRateHelper(2, Period(18, Months), ois18MRate, eonia)
    ois21M = OISRateHelper(2, Period(21, Months), ois21MRate, eonia)
    ois2Y = OISRateHelper(2,Period(2, Years), ois2YRate, eonia)
    ois3Y = OISRateHelper(2, Period(3, Years), ois3YRate, eonia)
    ois4Y = OISRateHelper(2, Period(4, Years), ois4YRate, eonia)
    ois5Y = OISRateHelper(2, Period(5, Years), ois5YRate, eonia)
    ois6Y = OISRateHelper(2, Period(6, Years), ois6YRate, eonia)
    ois7Y = OISRateHelper(2, Period(7, Years), ois7YRate, eonia)
    ois8Y = OISRateHelper(2, Period(8, Years), ois8YRate, eonia)
    ois9Y = OISRateHelper(2, Period(9, Years), ois9YRate, eonia)
    ois10Y = OISRateHelper(2, Period(10, Years), ois10YRate, eonia)
    ois11Y = OISRateHelper(2, Period(11, Years), ois11YRate, eonia)
    ois12Y = OISRateHelper(2, Period(12, Years), ois12YRate, eonia)
    ois15Y = OISRateHelper(2, Period(15, Years), ois15YRate, eonia)
    ois20Y = OISRateHelper(2, Period(20, Years), ois20YRate, eonia)
    ois25Y = OISRateHelper(2, Period(25, Years), ois25YRate, eonia)
    ois30Y = OISRateHelper(2, Period(30, Years), ois30YRate, eonia)


    # Dated OIS Swap Instrument
    oisDated1 = DatedOISRateHelper(Date(16, January, 2013), Date(13, February, 2013), oisDated1Rate, eonia)
    oisDated2 = DatedOISRateHelper(Date(13, February, 2013), Date(13, March, 2013), oisDated2Rate, eonia)
    oisDated3 = DatedOISRateHelper(Date(13, March, 2013), Date(10, April, 2013), oisDated3Rate, eonia)
    oisDated4 = DatedOISRateHelper(Date(10, April, 2013), Date(8, May, 2013), oisDated4Rate, eonia)
    oisDated5 = DatedOISRateHelper(Date(8, May, 2013), Date(12, June, 2013), oisDated5Rate, eonia)

    # Curve building
    tolerance = 1e-15
    eoniaInstruments = list()
    eoniaInstruments.append(dON)
    eoniaInstruments.append(dTN)
    eoniaInstruments.append(dSN)
    eoniaInstruments.append(ois1W)
    eoniaInstruments.append(ois2W)
    eoniaInstruments.append(ois3W)
    eoniaInstruments.append(ois1M)
    eoniaInstruments.append(oisDated1)
    eoniaInstruments.append(oisDated2)
    eoniaInstruments.append(oisDated3)
    eoniaInstruments.append(oisDated4)
    eoniaInstruments.append(oisDated5)
    eoniaInstruments.append(ois15M)
    eoniaInstruments.append(ois18M)
    eoniaInstruments.append(ois21M)
    eoniaInstruments.append(ois2Y)
    eoniaInstruments.append(ois3Y)
    eoniaInstruments.append(ois4Y)
    eoniaInstruments.append(ois5Y)
    eoniaInstruments.append(ois6Y)
    eoniaInstruments.append(ois7Y)
    eoniaInstruments.append(ois8Y)
    eoniaInstruments.append(ois9Y)
    eoniaInstruments.append(ois10Y)
    eoniaInstruments.append(ois11Y)
    eoniaInstruments.append(ois12Y)
    eoniaInstruments.append(ois15Y)
    eoniaInstruments.append(ois20Y)
    eoniaInstruments.append(ois25Y)
    eoniaInstruments.append(ois30Y)

    eoniaTermStructure = PiecewiseFlatForward(0, TARGET(), eoniaInstruments, termStructureDayCounter)
    eoniaTermStructure.enableExtrapolation()
    Curves['eur.eonia.1b'] = eoniaTermStructure

    discountingTermStructure = RelinkableYieldTermStructureHandle()
    forecastTermStructure = RelinkableYieldTermStructureHandle()
    discountingTermStructure.linkTo(eoniaTermStructure)

    # EURIBOR
    euribor6M = Euribor6M()
    d6MRate = QuoteHandle(SimpleQuote(0.00312))

    fra1Rate = QuoteHandle(SimpleQuote(0.002930))
    fra2Rate = QuoteHandle(SimpleQuote(0.002720))
    fra3Rate = QuoteHandle(SimpleQuote(0.002600))
    fra4Rate = QuoteHandle(SimpleQuote(0.002560))
    fra5Rate = QuoteHandle(SimpleQuote(0.002520))
    fra6Rate = QuoteHandle(SimpleQuote(0.002480))
    fra7Rate = QuoteHandle(SimpleQuote(0.002540))
    fra8Rate = QuoteHandle(SimpleQuote(0.002610))
    fra9Rate = QuoteHandle(SimpleQuote(0.002930))
    fra10Rate = QuoteHandle(SimpleQuote(0.002790))
    fra11Rate = QuoteHandle(SimpleQuote(0.002910))
    fra12Rate = QuoteHandle(SimpleQuote(0.003030))
    fra13Rate = QuoteHandle(SimpleQuote(0.003180))
    fra14Rate = QuoteHandle(SimpleQuote(0.003350))
    fra15Rate = QuoteHandle(SimpleQuote(0.003520))
    fra16Rate = QuoteHandle(SimpleQuote(0.003710))
    fra17Rate = QuoteHandle(SimpleQuote(0.003890))
    fra18Rate = QuoteHandle(SimpleQuote(0.004090))

    s3yRate = QuoteHandle(SimpleQuote(0.004240))
    s4yRate = QuoteHandle(SimpleQuote(0.005760))
    s5yRate = QuoteHandle(SimpleQuote(0.007620))
    s6yRate = QuoteHandle(SimpleQuote(0.009540))
    s7yRate = QuoteHandle(SimpleQuote(0.011350))
    s8yRate = QuoteHandle(SimpleQuote(0.013030))
    s9yRate = QuoteHandle(SimpleQuote(0.014520))
    s10yRate = QuoteHandle(SimpleQuote(0.015840))
    s12yRate = QuoteHandle(SimpleQuote(0.018090))
    s15yRate = QuoteHandle(SimpleQuote(0.020370))
    s20yRate = QuoteHandle(SimpleQuote(0.021870))
    s25yRate = QuoteHandle(SimpleQuote(0.022340))
    s30yRate = QuoteHandle(SimpleQuote(0.022560))
    s35yRate = QuoteHandle(SimpleQuote(0.022950))
    s40yRate = QuoteHandle(SimpleQuote(0.023480))
    s50yRate = QuoteHandle(SimpleQuote(0.024210))
    s60yRate = QuoteHandle(SimpleQuote(0.024630))

    d6M = DepositRateHelper(d6MRate, Period(6, Months), 3, calendar, Following, False, depositDayCounter)

    fra1 = FraRateHelper(fra1Rate, 1, euribor6M)
    fra2 = FraRateHelper(fra2Rate, 2, euribor6M)
    fra3 = FraRateHelper(fra3Rate, 3, euribor6M)
    fra4 = FraRateHelper(fra4Rate, 4, euribor6M)
    fra5 = FraRateHelper(fra5Rate, 5, euribor6M)
    fra6 = FraRateHelper(fra6Rate, 6, euribor6M)
    fra7 = FraRateHelper(fra7Rate, 7, euribor6M)
    fra8 = FraRateHelper(fra8Rate, 8, euribor6M)
    fra9 = FraRateHelper(fra9Rate, 9, euribor6M)
    fra10 = FraRateHelper(fra10Rate, 10, euribor6M)
    fra11 = FraRateHelper(fra11Rate, 11, euribor6M)
    fra12 = FraRateHelper(fra12Rate, 12, euribor6M)
    fra13 = FraRateHelper(fra13Rate, 13, euribor6M)
    fra14 = FraRateHelper(fra14Rate, 14, euribor6M)
    fra15 = FraRateHelper(fra15Rate, 15, euribor6M)
    fra16 = FraRateHelper(fra16Rate, 16, euribor6M)
    fra17 = FraRateHelper(fra17Rate, 17, euribor6M)
    fra18 = FraRateHelper(fra18Rate, 18, euribor6M)


    # setup swaps Frequency
    swFixedLegFrequency = Annual
    swFixedLegConvention = Unadjusted
    swFixedLegDayCounter = Thirty360(Thirty360.European)

    swFloatingLegIndex = Euribor6M()

    s3y = SwapRateHelper(s3yRate, Period(3, Years), calendar, swFixedLegFrequency,  swFixedLegConvention, swFixedLegDayCounter,
                         swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s4y = SwapRateHelper(s4yRate, Period(3, Years), calendar, swFixedLegFrequency,  swFixedLegConvention, swFixedLegDayCounter,
                         swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s5y = SwapRateHelper(s5yRate, Period(5, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                         swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s6y = SwapRateHelper(s6yRate, Period(6, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                         swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s7y = SwapRateHelper(s7yRate, Period(6, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                         swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s8y = SwapRateHelper(s8yRate, Period(6, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                         swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s9y = SwapRateHelper(s9yRate, Period(9, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                         swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s10y = SwapRateHelper(s10yRate, Period(10, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s12y = SwapRateHelper(s12yRate, Period(12, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s15y = SwapRateHelper(s15yRate, Period(15, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s20y = SwapRateHelper(s20yRate, Period(20, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s25y = SwapRateHelper(s25yRate, Period(25, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s30y = SwapRateHelper(s30yRate, Period(30, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s35y = SwapRateHelper(s35yRate, Period(35, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s40y = SwapRateHelper(s40yRate, Period(40, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s50y = SwapRateHelper(s50yRate, Period(50, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex, QuoteHandle(), Period(0, Days), discountingTermStructure)
    s60y = SwapRateHelper(s60yRate, Period(60, Years), calendar, swFixedLegFrequency, swFixedLegConvention, swFixedLegDayCounter,
                          swFloatingLegIndex,QuoteHandle(), Period(0, Days), discountingTermStructure)

    euribor6MInstruments = list()
    euribor6MInstruments.append(d6M)
    euribor6MInstruments.append(fra1)
    euribor6MInstruments.append(fra2)
    euribor6MInstruments.append(fra3)
    euribor6MInstruments.append(fra4)
    euribor6MInstruments.append(fra5)
    euribor6MInstruments.append(fra6)
    euribor6MInstruments.append(fra7)
    euribor6MInstruments.append(fra8)
    euribor6MInstruments.append(fra9)
    euribor6MInstruments.append(fra10)
    euribor6MInstruments.append(fra11)
    euribor6MInstruments.append(fra12)
    euribor6MInstruments.append(fra13)
    euribor6MInstruments.append(fra14)
    euribor6MInstruments.append(fra15)
    euribor6MInstruments.append(fra16)
    euribor6MInstruments.append(fra17)
    euribor6MInstruments.append(fra18)
    euribor6MInstruments.append(s3y)
    euribor6MInstruments.append(s4y)
    euribor6MInstruments.append(s5y)
    euribor6MInstruments.append(s6y)
    euribor6MInstruments.append(s7y)
    euribor6MInstruments.append(s8y)
    euribor6MInstruments.append(s9y)
    euribor6MInstruments.append(s10y)
    euribor6MInstruments.append(s12y)
    euribor6MInstruments.append(s15y)
    euribor6MInstruments.append(s20y)
    euribor6MInstruments.append(s25y)
    euribor6MInstruments.append(s30y)
    euribor6MInstruments.append(s35y)
    euribor6MInstruments.append(s40y)
    euribor6MInstruments.append(s50y)
    euribor6MInstruments.append(s60y)

    euribor6MTermStructure = PiecewiseCubicZero(settlementDate, euribor6MInstruments, termStructureDayCounter)
    Curves['eur.euribor.6m'] = euribor6MTermStructure

    return Curves


def pricing_test(curves):
    eonia_curve = curves['eur.eonia.1b']
    today = eonia_curve.referenceDate()

    end = today + Period(30, Years)
    dates = [Date(serial) for serial in range(today.serialNumber(), end.serialNumber() + 1, 10)]
    rates_c = [eonia_curve.forwardRate(d, TARGET().advance(d, 1, Days), Actual360(), Simple).rate() for d in dates]
    fig, ax = plt.subplots()
    new_dates = [ql_to_datetime(d) for d in dates]
    serial_dates = [serial for serial in range(today.serialNumber(), end.serialNumber() + 1, 10)]

    ax.plot(new_dates, rates_c)
    fig.autofmt_xdate()
    plt.show()

    zeroRate = dict(zip(serial_dates, rates_c))
    with open("curve_eur.txt", 'w') as fout:
        json_dumps_str = json.dumps(zeroRate, indent=4)
        print(json_dumps_str, file=fout)


def ql_to_datetime(d):
    return dt.datetime(d.year(), d.month(), d.dayOfMonth())


if __name__ == '__main__':

    curves = build_eur()
    pricing_test(curves)
