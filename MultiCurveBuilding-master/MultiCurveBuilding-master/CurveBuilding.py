import QuantLib as ql
import CurveSet as cs
import ZeroCurve as zc
import xlwings as xw
import csv
from numpy.linalg import inv
from pandas import DataFrame as df


def saveToCSV(data, path=None):
    writer = csv.writer(open("test1.csv", "w"))
    writer.writerows(data)


if __name__ == "__main__":
    QLdaycount = {
        'ACT360': ql.Actual360(),
        'ACT365': ql.Actual365Fixed(),
        'Thirty360': ql.Thirty360()
    }
    QLbusiness_convention = {
        'Following': ql.Following,
        'ModifiedFollowing': ql.ModifiedFollowing
    }
    QLcalendar = {
        'UnitedStates': ql.UnitedStates(),
        'Target': ql.TARGET(),
        'Singapore': ql.Singapore(),
        'UnitedKingdom': ql.UnitedKingdom()
    }
    valuationdate = ql.Date(13, 7, 2017)
    ql.Settings.instance().evaluationDate = valuationdate
    currencies = ['USD', 'SGD']
    curveset = cs.CurveSet(valuationdate)
    print(valuationdate)
    # define calendars
    UScalendar = QLcalendar['UnitedStates']
    SGcalendar = QLcalendar['Singapore']
    UKcalendar = QLcalendar['UnitedKingdom']
    USSGcalendar = ql.JointCalendar(UScalendar, SGcalendar, ql.JoinHolidays)
    USUKcalendar = ql.JointCalendar(UScalendar, UKcalendar)
    # construct the curve set on the valuationdate
    curveset = cs.CurveSet(valuationdate)
    # There are following six curves to be built
    # USDOIS: OIS zero curve for USD
    # USD3M: USD LIBOR 3M zero curve
    # USD6M: USD LIBOR 6M curve as a zero spread curve
    # SGD6M: SOR6M curve
    # SGDFX: SGDFX curve
    # SGDCCS: SGD cross currency curve

    curvelist = []
    curvelist.append('USDOIS')
    curvelist.append('USD3M')
    curvelist.append('USD6M')
    curvelist.append('SGD6M')
    curvelist.append('SGDFX')
    curvelist.append('SGDCCS')
    marketQuote = dict()

    initguessrate = 0.02
    initguessspread = 0.01
    print('instruments for USDOIS')
    tenors = ['ON', 'TN', '1W', '1M', '2M', '3M', '6M',
              '9M', '1Y', '18M', '2Y', '3Y', '4Y', '5Y',
              '6Y', '7Y', '8Y', '9Y', '10Y', '12Y', '15Y',
              '20Y', '25Y', '30Y']
    types = ['DEPO', 'DEPO', 'OIS', 'OIS', 'OIS', 'OIS', 'OIS',
             'OIS', 'OIS', 'OIS', 'OIS', 'OIS', 'OIS', 'OIS',
             'OIS', 'OIS', 'OIS', 'OIS', 'OIS', 'OIS', 'OIS',
             'OIS', 'OIS', 'OIS']
    quotes = [0.445, 0.46, 0.375, 0.38, 0.3815, 0.381, 0.383,
              0.394, 0.403, 0.4245, 0.4435, 0.495, 0.544,
              0.602, 0.669, 0.736, 0.8, 0.858, 0.91, 1.012,
              1.12, 1.236, 1.295, 1.323]
    quote = list(zip(tenors, types, quotes))
    marketQuote['USDOIS'] = quote

    zeros = []
    tenordates = []
    for i in range(len(tenors)):
        zeros.append(initguessrate)
        if types[i] == 'DEPO':
            daycount = QLdaycount['ACT360']
            calendar = UScalendar
            discurve = 'USDOIS'
            settledays = 2
            depo = cs.Deposit(valuationdate, quotes[i] / 100., tenors[i], settledays,
                              daycount, calendar, discurve)
            curveset.addinstrument(depo)
            tenordates.append(depo.enddate)
        elif types[i] == 'OIS':
            daycount = QLdaycount['ACT360']
            calendar = UScalendar
            settledays = 2
            Frequency = '1Y'
            businessday_convention = QLbusiness_convention['ModifiedFollowing']
            curve = 'USDOIS'
            paymentlag = 2
            ois = cs.OIS(valuationdate,
                         quotes[i] / 100,
                         tenors[i],
                         daycount,
                         calendar,
                         settledays,
                         paymentlag,
                         businessday_convention,
                         Frequency,
                         curve)
            curveset.addinstrument(ois)
            tenordates.append(ois.enddate)
    curve = zc.ZeroCurve(curvelist[0], valuationdate, tenors, tenordates, zeros)
    curveset.addcurve(curvelist[0], curve)

    # adding USD3M curve and its instruments to the curve set
    print('instruments for USD3M')
    # all swap quotes
    # tenors=['3M','6M',
    #        '9M','1Y','18M','2Y','3Y','4Y','5Y',
    #        '6Y','7Y','8Y','9Y','10Y','11Y','12Y','13Y','14Y','15Y',
    #        '20Y','30Y']
    # types=['SWAP','SWAP','SWAP','SWAP','SWAP','SWAP',
    #       'SWAP','SWAP','SWAP','SWAP','SWAP','SWAP',
    #       'SWAP','SWAP','SWAP','SWAP','SWAP','SWAP',
    #       'SWAP','SWAP','SWAP']
    # quotes=[0.6646,0.678,0.6925,0.7055,0.733,0.7613,
    #        0.8173,0.8773,0.9408,1.0152,1.0842,1.1552,
    #        1.2157,1.2653,1.3195,1.368,1.411,1.4485,
    #        1.4777,1.595,1.6857]
    #
    # futures & swap
    # tenors=['fut1','fut2',
    #        'fut3','fut4','fut5','fut6','fut7','fut8','3Y','4Y','5Y',
    #        '6Y','7Y','8Y','9Y','10Y','11Y','12Y','13Y','14Y','15Y',
    #        '20Y','30Y']
    # types=['FUT','FUT','FUT','FUT','FUT','FUT','FUT','FUT',
    #       'SWAP','SWAP','SWAP','SWAP','SWAP','SWAP',
    #       'SWAP','SWAP','SWAP','SWAP','SWAP','SWAP',
    #       'SWAP','SWAP','SWAP']
    # quotes=[99.7875,99.6875,99.4875,99.3875,99.2875,99.2875,99.2875,99.1875,
    #        0.8173,0.8773,0.9408,1.0152,1.0842,1.1552,
    #        1.2157,1.2653,1.3195,1.368,1.411,1.4485,
    #        1.4777,1.595,1.6857]

    # fra & swap
    tenors = ['fra0x3', 'fra3x6', 'fra6x9',
              '1Y', '18M', '2Y', '3Y', '4Y', '5Y',
              '6Y', '7Y', '8Y', '9Y', '10Y', '11Y', '12Y', '13Y', '14Y', '15Y',
              '20Y', '30Y']
    types = ['FRA', 'FRA', 'FRA', 'SWAP', 'SWAP', 'SWAP',
             'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP',
             'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP',
             'SWAP', 'SWAP', 'SWAP']
    quotes = [0.6646, 0.678, 0.6925, 0.7055, 0.733, 0.7613,
              0.8173, 0.8773, 0.9408, 1.0152, 1.0842, 1.1552,
              1.2157, 1.2653, 1.3195, 1.368, 1.411, 1.4485,
              1.4777, 1.595, 1.6857]
    quote = list(zip(tenors, types, quotes))
    marketQuote['USD3M'] = quote

    zeros = []
    tenordates = []
    for i in range(len(tenors)):
        zeros.append(initguessrate)
        if types[i] == 'FUT':
            daycount = QLdaycount['ACT360']
            calendar = UScalendar
            discurve = 'USD3M'
            settledays = 2
            futureindexstr = tenors[i].lstrip('fut')
            futureindex = int(futureindexstr)
            fut = cs.Futures(valuationdate, quotes[i] / 100., settledays,
                             3, calendar, daycount, discurve, futureindex)
            curveset.addinstrument(fut)
            tenordates.append(fut.enddate)
        elif types[i] == 'FRA':
            daycount = QLdaycount['ACT360']
            calendar = UScalendar
            discurve = 'USD3M'
            settledays = 2
            fratenor = tenors[i].lstrip('fra')
            startend = fratenor.split('x')
            startmonth = int(startend[0])
            endmonth = int(startend[1])
            fra = cs.FRA(valuationdate, quotes[i] / 100., settledays,
                         startmonth, endmonth, daycount, calendar, discurve)
            curveset.addinstrument(fra)
            tenordates.append(fra.enddate)
        elif types[i] == 'SWAP':
            daycount = QLdaycount['ACT360']
            calendar = UScalendar
            settledays = 2
            Leg1Frequency = '1Y'
            Leg1forcurve = 'None'
            Leg2Frequency = '3M'
            Leg2forcurve = 'USD3M'
            businessday_convention = QLbusiness_convention['ModifiedFollowing']
            discurve = 'USDOIS'
            swap = cs.Swap(valuationdate,
                           quotes[i] / 100,
                           tenors[i],
                           calendar,
                           calendar,
                           settledays,
                           businessday_convention,
                           daycount,
                           Leg1Frequency,
                           Leg1forcurve,
                           discurve,
                           daycount,
                           Leg2Frequency,
                           Leg2forcurve,
                           discurve)
            curveset.addinstrument(swap)
            tenordates.append(swap.enddate)
    curve = zc.ZeroCurve(curvelist[1], valuationdate, tenors, tenordates, zeros)
    curveset.addcurve(curvelist[1], curve)

    # adding USD6M curve and its instrument to curveset
    print('instruments for USD6M')
    tenors = ['6M', '1Y', '18M', '2Y', '3Y', '4Y', '5Y',
              '6Y', '7Y', '8Y', '9Y', '10Y', '12Y', '15Y',
              '20Y', '30Y']
    types = ['BSSWAP', 'BSSWAP', 'BSSWAP', 'BSSWAP', 'BSSWAP', 'BSSWAP',
             'BSSWAP', 'BSSWAP', 'BSSWAP', 'BSSWAP', 'BSSWAP', 'BSSWAP',
             'BSSWAP', 'BSSWAP', 'BSSWAP', 'BSSWAP']
    quotes = [0.25875, 0.24125, 0.2275, 0.2175, 0.1975, 0.18375, 0.17375,
              0.17, 0.16625, 0.16583, 0.1654117, 0.165, 0.1713, 0.1725,
              0.1738, 0.17375]
    quote = list(zip(tenors, types, quotes))
    marketQuote['USD6M'] = quote

    zeros = []
    tenordates = []
    for i in range(len(tenors)):
        zeros.append(initguessspread)
        daycount = QLdaycount['ACT360']
        calendar = UScalendar
        settledays = 2
        Leg1Frequency = '3M'
        Leg1forcurve = 'USD3M'
        Leg2Frequency = '6M'
        Leg2forcurve = 'USD6M'
        businessday_convention = QLbusiness_convention['ModifiedFollowing']
        discurve = 'USDOIS'
        paymentlag = 2
        bsswap = cs.BasisSwap(valuationdate,
                              quotes[i] / 100,
                              tenors[i],
                              daycount,
                              calendar,
                              settledays,
                              businessday_convention,
                              Leg1Frequency,
                              Leg1forcurve,
                              discurve,
                              Leg2Frequency,
                              Leg2forcurve,
                              discurve)
        curveset.addinstrument(bsswap)
        tenordates.append(bsswap.enddate)
    curve = zc.ZeroSpreadCurve(curvelist[2], curvelist[1], valuationdate, tenors, tenordates, zeros)
    curveset.addcurve(curvelist[2], curve)

    print('instruments for SGD6M')
    tenors = ['6M', '1Y', '18M', '2Y', '3Y', '4Y',
              '5Y', '6Y', '7Y', '10Y', '12Y', '15Y',
              '20Y', '25Y', '30Y']
    types = ['SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP',
             'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP',
             'SWAP', 'SWAP', 'SWAP']
    quotes = [1.105449, 1.2075, 1.2725, 1.32375, 1.4475, 1.54375,
              1.61125, 1.69375, 1.78875, 1.9775, 2.0675, 2.17,
              2.2275, 2.2575, 2.2875]
    quote = list(zip(tenors, types, quotes))
    marketQuote['SGD6M'] = quote

    zeros = []
    tenordates = []
    for i in range(len(tenors)):
        zeros.append(initguessrate)
        daycount = QLdaycount['ACT365']
        calendar = SGcalendar
        settledays = 2
        Leg1Frequency = '6M'
        Leg1forcurve = 'None'
        Leg2Frequency = '6M'
        Leg2forcurve = 'SGD6M'
        businessday_convention = QLbusiness_convention['ModifiedFollowing']
        discurve = 'SGDCCS'
        swap = cs.Swap(valuationdate,
                       quotes[i] / 100,
                       tenors[i],
                       calendar,
                       calendar,
                       settledays,
                       businessday_convention,
                       daycount,
                       Leg1Frequency,
                       Leg1forcurve,
                       discurve,
                       daycount,
                       Leg2Frequency,
                       Leg2forcurve,
                       discurve)
        curveset.addinstrument(swap)
        tenordates.append(swap.enddate)
    curve = zc.ZeroCurve(curvelist[3], valuationdate, tenors, tenordates, zeros)
    curveset.addcurve(curvelist[3], curve)

    print('instruments for SGDFX')
    tenors = ['ON', 'TN', 'SN', '1W', '2W', '1M', '2M', '3M', '6M',
              '9M', '1Y']
    types = ['DEPO', 'DEPO', 'DEPO', 'DEPO', 'DEPO', 'DEPO',
             'DEPO', 'DEPO', 'DEPO', 'DEPO', 'DEPO']
    quotes = [-0.0111586, 0.0333629, 0.0150204, 0.2013789, 0.3761605, 0.3852778,
              0.4352381, 0.4562263, 0.5430637, 0.5926593, 0.6412572]
    quote = list(zip(tenors, types, quotes))
    marketQuote['SGDFX'] = quote

    zeros = []
    tenordates = []
    for i in range(len(tenors)):
        zeros.append(initguessrate)
        daycount = QLdaycount['ACT365']
        calendar = USSGcalendar
        discurve = 'SGDFX'
        settledays = 2
        depo = cs.Deposit(valuationdate, quotes[i] / 100., tenors[i], settledays,
                          daycount, calendar, discurve)
        curveset.addinstrument(depo)
        tenordates.append(depo.enddate)
    curve = zc.ZeroCurve(curvelist[4], valuationdate, tenors, tenordates, zeros)
    curveset.addcurve(curvelist[4], curve)
    print('instruments for SGDCCS')
    tenors = ['18M', '2Y', '3Y', '4Y', '5Y', '6Y',
              '7Y', '10Y', '12Y', '15Y', '20Y', '30Y']
    types = ['SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP',
             'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP', 'SWAP']
    quotes = [-0.01375, -0.01625, -0.0775, -0.1725, -0.25, -0.29,
              -0.345, -0.5275, -0.6375, -0.6775, -0.73, -0.73]
    quote = list(zip(tenors, types, quotes))
    marketQuote['SGDCCS'] = quote

    zeros = []
    tenordates = []
    for i in range(len(tenors)):
        zeros.append(initguessspread)
        Leg1daycount = QLdaycount['ACT365']
        Leg2daycount = QLdaycount['ACT360']
        paymentcalendar = USSGcalendar
        Leg1fixingcalendar = SGcalendar
        Leg2fixingcalendar = UScalendar
        settledays = 2
        Leg1Frequency = '6M'
        Leg1forcurve = 'SGD6M'
        Leg1discurve = 'SGDCCS'
        Leg2Frequency = '6M'
        Leg2forcurve = 'USD6M'
        Leg2discurve = 'USDOIS'
        businessday_convention = QLbusiness_convention['ModifiedFollowing']
        ccs = cs.CCS(valuationdate,
                     quotes[i] / 100,
                     tenors[i],
                     settledays,
                     businessday_convention,
                     Leg1daycount,
                     Leg1Frequency,  # following arguments are for swaps
                     Leg1forcurve,  # forcasting curve name
                     Leg1discurve,  # discounting curve name
                     Leg1fixingcalendar,
                     paymentcalendar,
                     Leg2daycount,
                     Leg2Frequency,
                     Leg2forcurve,
                     Leg2discurve,
                     Leg2fixingcalendar,
                     paymentcalendar)
        curveset.addinstrument(ccs)
        tenordates.append(ccs.enddate)
    curve = zc.ZeroSpreadCurve(curvelist[5], 'SGDFX',
                               valuationdate,
                               tenors, tenordates, zeros, nullbeforefirstpillar=True)
    curveset.addcurve(curvelist[5], curve)
    curveset.bootstrap()

    # save out put
    save_output = True
    if save_output:
        output = []
        label = ['curve name', 'value date', 'tenor', 'tenor start', 'tenor end', 'quote', 'zero rate', 'error']
        for curveName in curveset.curveset.keys():
            print(curveName)
            # print(curveset.curveset[curveName].zerorates)
            market = marketQuote[curveName]
            zeroCurve = curveset.curveset[curveName]
            if len(market) != len(zeroCurve.zerorates):
                raise RuntimeError('market quote and zero rate size not same!')

            for i, zr in enumerate(zeroCurve.zerorates):
                if market[i][0] == zeroCurve.tenors[i]:
                    row = curveName, zeroCurve.tenors[i], market[i][1], '', \
                          zeroCurve.tenordates[i].serialNumber(), market[i][2], zr, 0.0
                    output.append(row)
            output.append(label)

        result = df.from_records(output, columns=label)
        result.to_csv('zero_rates1.csv')

        # print('Jacobian Matrix dR/dZ')
        # print(curveset.DRDZ)
        data = curveset.DRDZ
        jac = df(data[0:, 0:])
        jac.to_csv('Jacobian_dRdZ.csv')
        print('Jacobian Matrix dZ/dR')
        print(inv(curveset.DRDZ))
        data_ = inv(curveset.DRDZ)
        jac_inv = df(data_[0:, 0:])
        jac_inv.to_csv('Jacobian_dZdR.csv')

    # some test
    usd_6m_2y = cs.Swap(valuationdate=valuationdate,
                        quote=1.0,
                        maturity='2Y',
                        paymentcalendar=UScalendar,
                        fixingcalendar=USUKcalendar,
                        settledays=2.0,
                        businessday_convention=QLbusiness_convention['ModifiedFollowing'],
                        Leg1daycount=QLdaycount['ACT360'],
                        Leg1Frequency='6M',  # following arguments are for swaps
                        Leg1forcurve=None,  # forcasting curve name
                        Leg1discurve='USDOIS',  # discounting curve name
                        Leg2daycount=QLdaycount['ACT360'],
                        Leg2Frequency='6M',
                        Leg2forcurve='USD6M',  # must be provided
                        Leg2discurve='USDOIS')

    usd_6m_2y.assigncurves(curveset.curveset)
    print('USD LIBOR 6M 2Y Par Rate:\t{0:.4f}%'.format(usd_6m_2y.impliedquote() * 100.0))

    usd_3m_1y = cs.Swap(valuationdate=valuationdate,
                        quote=1.0,
                        maturity='1Y',
                        paymentcalendar=UScalendar,
                        fixingcalendar=USUKcalendar,
                        settledays=2.0,
                        businessday_convention=QLbusiness_convention['ModifiedFollowing'],
                        Leg1daycount=QLdaycount['ACT365'],
                        Leg1Frequency='1y',  # following arguments are for swaps
                        Leg1forcurve=None,  # forcasting curve name
                        Leg1discurve='USDOIS',  # discounting curve name
                        Leg2daycount=QLdaycount['ACT360'],
                        Leg2Frequency='3M',
                        Leg2forcurve='USD3M',  # must be provided
                        Leg2discurve='USDOIS')

    usd_3m_1y.assigncurves(curveset.curveset)
    print('USD LIBOR AMQM 1Y Par Rate:\t{0:.4f}%'.format(usd_3m_1y.impliedquote() * 100.0))

    usd_3m_18m = cs.Swap(valuationdate=valuationdate,
                        quote=1.0,
                        maturity='1y6m',
                        paymentcalendar=UScalendar,
                        fixingcalendar=USUKcalendar,
                        settledays=2.0,
                        businessday_convention=QLbusiness_convention['ModifiedFollowing'],
                        Leg1daycount=QLdaycount['ACT360'],
                        Leg1Frequency='3m',  # following arguments are for swaps
                        Leg1forcurve=None,  # forcasting curve name
                        Leg1discurve='USDOIS',  # discounting curve name
                        Leg2daycount=QLdaycount['ACT360'],
                        Leg2Frequency='3M',
                        Leg2forcurve='USD3M',  # must be provided
                        Leg2discurve='USDOIS')

    usd_3m_18m.assigncurves(curveset.curveset)
    print('USD LIBOR 3M 1Y6M Par Rate:\t{0:.4f}%'.format(usd_3m_18m.impliedquote() * 100.0))

    usd_3m_30y = cs.Swap(valuationdate=valuationdate,
                         quote=1.0,
                         maturity='30y',
                         paymentcalendar=UScalendar,
                         fixingcalendar=USUKcalendar,
                         settledays=2.0,
                         businessday_convention=QLbusiness_convention['ModifiedFollowing'],
                         Leg1daycount=QLdaycount['ACT360'],
                         Leg1Frequency='1y',  # following arguments are for swaps
                         Leg1forcurve=None,  # forcasting curve name
                         Leg1discurve='USDOIS',  # discounting curve name
                         Leg2daycount=QLdaycount['ACT360'],
                         Leg2Frequency='3M',
                         Leg2forcurve='USD3M',  # must be provided
                         Leg2discurve='USDOIS')

    usd_3m_30y.assigncurves(curveset.curveset)
    print('USD LIBOR 3M 31Y Par Rate:\t{0:.4f}%'.format(usd_3m_30y.impliedquote() * 100.0))

    usd_3s6s_1y = cs.BasisSwap(
        valuationdate=valuationdate,
        quote=0.0,
        maturity='1y',
        daycount=QLdaycount['ACT360'],
        calendar=UScalendar,
        settledays=2,
        businessday_convention=QLbusiness_convention['ModifiedFollowing'],
        Leg1Frequency='6m',
        Leg1forcurve='USD3M',
        Leg1discurve='USDOIS',
        Leg2Frequency='6M',
        Leg2forcurve='USD6M',
        Leg2discurve='USDOIS')

    usd_3s6s_1y.assigncurves(curveset.curveset)
    print('USD LIBOR 3S6S 1Y Par Spread:\t{0:.4f}%'.format(usd_3s6s_1y.impliedquote() * 100.0))

    usdsgd_ccs_2y =\
        cs.CCS(valuationdate=valuationdate,
               quote=0.0,
               maturity='2y',
               settledays=2,
               businessday_convention=QLbusiness_convention['ModifiedFollowing'],
               Leg1Daycount=QLdaycount['ACT365'],
               Leg1Frequency='6m',
               Leg1forcurve='None',
               Leg1discurve='SGDCCS',
               Leg1FixingCalendar=UKcalendar,
               Leg1PaymentCalendar=USSGcalendar,

               Leg2Daycount=QLdaycount['ACT360'],
               Leg2Frequency='6m',
               Leg2forcurve='USD6M',
               Leg2discurve='USDOIS',
               Leg2FixingCalendar=UKcalendar,
               Leg2PaymentCalendar=USSGcalendar,
               resettable=True,
               resettableleg=1)

    usdsgd_ccs_2y.assigncurves(curveset.curveset)
    print('USDSGD CCS 2Y Par Rate:\t{0:.4f}%'.format(usdsgd_ccs_2y.impliedquote() * 100.0))

    usdsgd_ccbs_2y = \
        cs.CCBS(valuationdate=valuationdate,
               quote=0.0,
               maturity='2y',
               settledays=2,
               businessday_convention=QLbusiness_convention['ModifiedFollowing'],
               Leg1Daycount=QLdaycount['ACT365'],
               Leg1Frequency='6m',
               Leg1forcurve='SGD6M',
               Leg1discurve='SGDCCS',
               Leg1FixingCalendar=SGcalendar,
               Leg1PaymentCalendar=USSGcalendar,

               Leg2Daycount=QLdaycount['ACT360'],
               Leg2Frequency='6m',
               Leg2forcurve='USD6M',
               Leg2discurve='USDOIS',
               Leg2FixingCalendar=UKcalendar,
               Leg2PaymentCalendar=USSGcalendar,
               resettable=True,
               resettableleg=1)

    usdsgd_ccbs_2y.assigncurves(curveset.curveset)
    print('USDSGD CCBS 2Y Par Spread:\t{0:.4f}%'.format(usdsgd_ccbs_2y.impliedquote() * 100.0))




