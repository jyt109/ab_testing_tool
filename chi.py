    # def chi_sq_test(self):
    #     """Return p value from chi-sq test comparing the proportion of convert
    #     between the old page and new page"""

    #     # Calculate all the necessary figures
    #     self.calculate_conversion()

    #     # List of observed values from the data
    #     obs = np.array([self.old_convert, (self.old_nrow - self.old_convert),
    #                     self.new_convert, (self.new_nrow - self.new_convert)])

    #     # List of expected value based on the null hypothesis
    #     exp_new_conversion = self.old_conversion + self.lift
    #     exp_new_convert = exp_new_conversion * self.new_nrow
    #     exp = np.array([self.old_convert, (self.old_nrow - self.old_convert),
    #                     exp_new_convert, (self.new_nrow - exp_new_convert)])

    #     chi2, p_val = scs.chisquare(obs, f_exp=exp, ddof=1)
    #     if self.two_tailed:
    #         reject_null = p_val < (self.alpha / 2)
    #     else:
    #         reject_null = p_val < self.alpha
    #     print 'ch-sq: %s,   p-value: %s, reject null: %s' % \
    #             (chi2, p_val, reject_null)
    #     return chi2, p_val, reject_null
