import pandas as pd
from power_functions import ProportionPower
import scipy.stats as scs
import numpy as np
from numpy import sqrt


class ABTest(object):
    """This class reads in a csv file, cleans the data and executes functions
    related to AB testing"""
    def __init__(self, filename, effect_size, alpha=.05,
                 power=.8, two_tailed=True):
        self.data = pd.read_csv(filename)
        self.alpha = alpha
        self.power = power
        self.effect_size = effect_size
        self.two_tailed = two_tailed

        # Variables to be filled in after preprocessing
        self.old_nrow, self.new_nrow = float(), float()
        self.old_convert, self.new_convert = float(), float()
        self.old_conversion, self.new_conversion = float(), float()
        self.new_adj_convert = float()
        self.nrow = int()

    def count_mismatch(self):
        """INPUT:
        - self.data(PANDAS DATAFRAME)

        OUTPUT:
        - NONE

        Compare the control/treatment label to the old/new landing page
        label to see if they match up
        """
        print 'ab column counts:'
        print self.data['ab'].value_counts()
        print 'landing_page column counts:'
        print self.data['landing_page'].value_counts()

    def find_mismatch(self, ab_cell, landing_page_cell):
        """INPUT:
        - ab_cell(STR) [A cell in the ab column]
        - landing_page_cell(STR) [A cell in the landing_page column]

        OUTPUT:
        - (INT) [0 or 1 depending on match or mismatch]

        Function that is used to create a new column to indicate if
        the ab / landing_page columns are mismatched(See drop_mismatch)
        """
        if ab_cell == 'treatment' and landing_page_cell == 'new_page':
            return 0
        elif ab_cell == 'control' and landing_page_cell == 'old_page':
            return 0
        else:
            return 1

    def drop_mismatch(self):
        """INPUT:
        - self.data(PANDAS DATAFRAME)

        OUTPUT:
        - self.data(PANDAS DATAFRAME)

        Function drop the mismatched rows and assign the new dataframe to
        instance variable self.data
        """
        print 'Dropping treatment / control and landing page mismatch...'
        # Function that will be applied to the 2 columns
        func = lambda row: self.find_mismatch(row['ab'], row['landing_page'])
        # axis=1 means iterate the rows in the dataframe
        self.data['mismatch'] = self.data.apply(func, axis=1)

        # Calculate the percentage of cells that have been mislabelled
        mismatched = self.data[self.data['mismatch'] == 1]
        percent = (len(mismatched) / (len(self.data['mismatch']) * 1.) * 100)
        print 'Percentage mismatched:', percent

        # Drop the mismatched rows and assign to instance variable
        self.data = self.data[self.data['mismatch'] == 0]

    def drop_duplicate_users(self):
        """INPUT:
        - self.data(PANDAS DATAFRAME)

        OUTPUT:
        - self.drop_mismatch(PANDAS DATAFRAME)

        Function drop the mismatched rows and assign the new dataframe to
        instance variable self.drop_mismatch
        """
        # Print the number of total user and unique users
        total_users = self.data['user_id'].shape[0]
        group_user = self.data.groupby('user_id')
        unique_users = len(group_user)
        print 'Total number of users: %s\nUnique number of users %s' % \
              (total_users, unique_users)

        # Drop duplicate users
        if unique_users <= total_users:
            print 'Dropping duplicate users...'
            duplicate_users = []
            # groups() of a groupby object gives a dict of the groupby key
            # to the value which is a list of indexes of the relevant rows
            for user, entry_lst in group_user.groups.iteritems():
                if len(entry_lst) > 1:
                    duplicate_users.append(user)

        # Reassign to instance variable
        self.data = self.data[~self.data['user_id'].isin(duplicate_users)]

    def calculate_conversion(self):
        """Calculate metrics neccessary for performing the z-test and
        chi-square test"""
        print 'Calculating conversion figures...'
        old = self.data[self.data['landing_page'] == 'old_page']
        new = self.data[self.data['landing_page'] == 'new_page']
        self.old_nrow = old.shape[0] * 1.
        self.new_nrow = new.shape[0] * 1.
        self.old_convert = old[old['converted'] == 1].shape[0]
        self.new_convert = new[new['converted'] == 1].shape[0]
        self.old_conversion = self.old_convert / self.old_nrow
        self.new_conversion = self.new_convert / self.new_nrow
        self.nrow = self.data.shape[0]
        print 'Control conversion: %s\nTreatment conversion: %s' % \
               (self.old_conversion, self.new_conversion)

    def preprocessing(self):
        """Handles all the prepreprocessing"""
        self.count_mismatch()
        self.drop_mismatch()
        self.drop_duplicate_users()
        self.calculate_conversion()

    def get_min_sample(self):
        """p_c, p_t, effect_size, alpha=.05,
         power=None, total=None, two_tailed=True
        """
        power_obj = ProportionPower(self.old_conversion, self.new_conversion,
                                    self.effect_size, self.alpha, self.power,
                                    two_tailed=self.two_tailed)
        return power_obj.calc_min_sample()

    def get_power(self):
        """p_c, p_t, effect_size, alpha=.05,
         power=None, total=None, two_tailed=True
        """
        power_obj = ProportionPower(self.old_conversion, self.new_conversion,
                                    self.effect_size, self.alpha,
                                    total=self.nrow,
                                    two_tailed=self.two_tailed)
        return power_obj.calc_power()

    def z_test(self):
        """Return p value from z-test comparing the proportion of convert
        between the old page and new page"""

        # Calculate all the necessary figures

        # Calculate an overall conversion assuming same conversion
        # between old and new page
        conversion = (self.old_convert + self.new_convert) \
                     / (self.old_nrow + self.new_nrow)

        se = sqrt(conversion * (1 - conversion)
                  * (1 / self.old_nrow + 1 / self.new_nrow))

        # Calculate z-score and get p-value from standard normal
        z_score = (self.new_conversion - self.old_conversion
                   - self.effect_size) / se
        p_val = 1 - scs.norm.cdf(abs(z_score))
        if self.two_tailed:
            reject_null = p_val < (self.alpha / 2)
        else:
            reject_null = p_val < self.alpha
        print 'z-score: %s, p-value: %s, reject null: %s' % \
                (z_score, p_val, reject_null)
        return z_score, p_val, reject_null

if __name__ == '__main__':
    # filename, lift, alpha=.05, power=.8, two_tailed=True
    ab_test = ABTest('data/sample.csv', 0.001)
    ab_test.preprocessing()
    print 'The minimum requred sample size:', ab_test.get_min_sample()
    print 'The current power:', ab_test.get_power()
    ab_test.z_test()
