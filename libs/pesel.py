'''
    PESEL number class
'''
import random
import datetime
from libs.gender import Gender

class Pesel():
    '''
        Constructor for class Pesel
    '''
    def __init__(self, timestamp: datetime.datetime, gender: Gender):
        date_part = self.pesel_date_gen(timestamp)
        order_part = self.pesel_order_number_gen()
        gender_part = self.pesel_gender_number_gen(gender)
        control_part = self.pesel_control_sum_gen(''.join(date_part) + order_part + gender_part)
        self.year = date_part[0]
        self.month = date_part[1]
        self.day = date_part[2]
        self.order = order_part
        self.gender = gender_part
        self.control = control_part

    @staticmethod
    def pesel_date_gen(timestamp: datetime.datetime):
        '''
            Generate pesel date from timestamp
            Source of data: https://www.gov.pl/web/gov/czym-jest-numer-pesel
        '''
        day = str(timestamp.day).zfill(2)
        month = timestamp.month
        year = timestamp.year

        if(year <= 1899):
            month += 80
        elif(year <= 1999):
            pass # random_month += 0
        elif(year <= 2099):
            month += 20
        elif(year <= 2199):
            month += 40
        else: #(random_year <= 2299)
            month += 60
        return [str(elem) for elem in (year,month,day)]

    @staticmethod
    def pesel_gender_number_gen(gender_type: Gender):
        '''
            Generate gender number from enum
        '''
        if(gender_type == Gender.Female):
            return random.choice(['0','2','4','6','8'])
        else: #(gender_type == Gender.Male)
            return random.choice(['1','3','5','7','9'])

    @staticmethod
    def pesel_order_number_gen():
        '''
            Generate order number
        '''
        return str(random.randint(0,999)).zfill(3)

    @staticmethod
    def pesel_control_sum_gen(ten_digit_pesel):
        '''
            Generate control sum digit
            Source: https://www.gov.pl/web/gov/czym-jest-numer-pesel
                    http://www.elektronik.lodz.pl/wbrzo/index.php?l1=02&l2=07&l3=00
        '''
        weights = [1,3,7,9]
        weights_len = len(weights)
        index = 0
        sum = 0
        for digit in ten_digit_pesel:
            int_digit = int(digit)
            sum += (int_digit * weights[index]) % 10
            index = (index + 1) % weights_len
        sum %= 10
        return str((10 - sum)%10)

    def __str__(self):
        '''
            String representation of pesel number
        '''
        return "".join([self.year[:2],self.month.zfill(2),self.day.zfill(2),self.order,self.gender,self.control])

    def __int__(self):
        '''
            Converting to int value
        '''
        return int(self.__str__())