def numbers_in_thousands(num,pos):
    '''
    Divides a list of numbers per thousands to format numbers in the chart axes
    '''
    num = num/1000
    num = int(num)
    return '{}'.format(num)
    
