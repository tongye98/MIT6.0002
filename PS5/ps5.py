# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    models = []
    for deg in degs:
        model = pylab.polyfit(x,y,deg)
        models.append(model)
    return models



def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    error = ((y-estimated)**2).sum()
    meanError = ((y-y.mean())**2).sum()
    return 1-(error/meanError)

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for model in models:
        pylab.plot(x,y,'b.',label='Data')
        estimated = pylab.polyval(model,x)
        r2 = r_squared(y,estimated)
        pylab.plot(x,estimated,'r-',label='Estimated')
        pylab.legend(loc='best')
        pylab.xlabel('years')
        pylab.ylabel('degree Celsius')
        pylab.title('Fit of degree: '+str(len(model)-1) + "\n" + 'R2: '+str(round(r2,5)))
        pylab.show()

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    cities_avg = []
    for year in years:
        cities_all = 0
        for city in multi_cities:
            cities_all += climate.get_yearly_temp(city=city, year=year).mean()
        cities_avg.append(cities_all / len(multi_cities))
    return pylab.array(cities_avg)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    mov_avg = []
    for i in range(window_length):
        mov_avg.append(sum(y[0:i+1])/len(y[0:i+1]))
    for j in range(window_length,len(y)):
        mov_avg.append((sum(y[j-window_length+1:j+1])/window_length))
    assert len(mov_avg) == len(y)
    return pylab.array(mov_avg)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    return (sum((y-estimated)**2)/len(y))**0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    std_devs = []
    for year in years:
        daily_365 = pylab.zeros(365)
        daily_366 = pylab.zeros(366)
        for city in multi_cities:
            if len(climate.get_yearly_temp(city,year)) == 365:
                daily_365 += climate.get_yearly_temp(city,year)
            else:
                daily_366 += climate.get_yearly_temp(city,year)
        if sum(daily_365) > sum(daily_366):
            daily = daily_365
        else:
            daily = daily_366
        daily = daily / len(multi_cities)
        mean = pylab.mean(daily)
        std_devs.append((sum((daily - mean)**2)/len(daily))**0.5)
    return pylab.array(std_devs)
        
    

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for model in models:
        pylab.plot(x,y,'b.',label='Data')
        estimated = pylab.polyval(model,x)
        RMSE = rmse(y,estimated)
        pylab.plot(x,estimated,'r-',label='Estimated')
        pylab.legend(loc='best')
        pylab.xlabel('years')
        pylab.ylabel('degree Celsius')
        pylab.title('Fit of degree: '+str(len(model)-1) + "\n" + 'RMSE: '+str(round(RMSE,5)))
        pylab.show()

if __name__ == '__main__':

    pass 

    # Part A.4
    # TODO: replace this line with your code
    ### 4.1 January 10th
    # climate = Climate('data.csv')
    # daily_temperatures = []
    # for year in TRAINING_INTERVAL:
    #     daily_temperatures.append(climate.get_daily_temp(city='NEW YORK',month=1,day=10,year=year))
    # print(daily_temperatures)
    # model = generate_models(pylab.array(TRAINING_INTERVAL),pylab.array(daily_temperatures),degs=[1]) # only one model
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),pylab.array(daily_temperatures),model)

    ### 4.2 Annual Temperature
    # climate = Climate('data.csv')
    # yearly_temperatures = []
    # for year in TRAINING_INTERVAL:
    #     yearly_temperatures.append(climate.get_yearly_temp(city='NEW YORK', year=year).mean())
    # print(yearly_temperatures)
    # model = generate_models(pylab.array(TRAINING_INTERVAL),pylab.array(yearly_temperatures),degs=[1]) # only one model
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),pylab.array(yearly_temperatures),model)

    # Part B
    # TODO: replace this line with your code
    # climate = Climate('data.csv')
    # cities_average = gen_cities_avg(climate, CITIES,TRAINING_INTERVAL)
    # model = generate_models(pylab.array(TRAINING_INTERVAL),cities_average,degs=[1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),cities_average,model)

    # Part C
    # TODO: replace this line with your code
    # window_length = 5
    # climate = Climate('data.csv')
    # cities_average = gen_cities_avg(climate, CITIES,TRAINING_INTERVAL)
    # mov_avg = moving_average(cities_average,window_length)
    # model = generate_models(pylab.array(TRAINING_INTERVAL),mov_avg,degs=[1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),mov_avg,model)

    # Part D.2
    # TODO: replace this line with your code
    ### Generate more models
    # window_length = 5
    # climate = Climate('data.csv')
    # cities_average = gen_cities_avg(climate, CITIES,TRAINING_INTERVAL)
    # mov_avg = moving_average(cities_average,window_length)
    # models = generate_models(pylab.array(TRAINING_INTERVAL),mov_avg,degs=[1,2,20])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),mov_avg,models)
    # ### Predict the result
    # predict_cities_average = gen_cities_avg(climate,CITIES,TESTING_INTERVAL)
    # predict_mov_avg = moving_average(predict_cities_average,window_length)
    # evaluate_models_on_testing(pylab.array(TESTING_INTERVAL),predict_mov_avg,models)


    # Part E
    # TODO: replace this line with your code
    # climate = Climate('data.csv')
    # std_years = gen_std_devs(climate,CITIES,years=TRAINING_INTERVAL)
    # mov_avg_years = moving_average(std_years,window_length=5)
    # model = generate_models(pylab.array(TRAINING_INTERVAL),mov_avg_years,degs=[1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL),mov_avg_years,model)

