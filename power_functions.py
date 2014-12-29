import scipy.stats as scs
from numpy import sqrt


class ProportionPower(object):
    """ProportionPower calculate the power and minimum sample size
    when comparing two proportions"""
    def __init__(self, p_samc, p_samt, effect_size, alpha=.05, power=None,
                 total=None, two_tailed=True):
        """
        Sample / Alternative parameters:
        - p_samc: proportion in the control group
        - p_samt: proportion in the treatment group
        - p_samd: (p_t - p_c), i.e. the difference caused by treatment
        - total: sum of sample size of control and treatment groups

        Population / Null parameters:
        - p_popd: effect_size, i.e the hypothesized difference caused by
          treatment
        - p_popc: Equals to p_samc
        - p_popt: (p_popc + p_popd), i.e. the hypothesize proportion in the
          treatment group

        """
        # Sample parameters
        self.p_samc = p_samc
        self.p_samt = p_samt
        self.p_samd = p_samt - p_samc

        # Population parameters
        self.p_popd = effect_size
        self.p_popc = p_samc
        self.p_popt = self.p_popc + self.p_popd
        self.p_popa = (self.p_popc + self.p_popt) / 2.

        # Difference between population and sample proportion
        self.p_delta = abs(self.p_samd - self.p_popd)

        # Significance and power parameters
        self.alpha = alpha
        self.power = power
        self.total = total
        self.two_tailed = two_tailed
        self.z_alpha = self.calc_z_alpha()

    def calc_z_alpha(self):
        """Calculate critical z value given significance level"""
        if self.two_tailed:
            # Get the z value at the corresponding significance level
            # ppf is percent point function. Inverse of cdf
            z_alpha = scs.norm.ppf((1 + (1 - self.alpha)) / 2)
        else:
            z_alpha = scs.norm.ppf(1 - self.alpha)
        return z_alpha

    def calc_min_sample(self):
        """Calculate minimum sample size"""
        if self.power:
            z_beta = scs.norm.ppf(self.power)
        else:
            print 'Please specify power for minimum sample size calculation.'
            raise

        a_sqrt = sqrt(2 * self.p_popa * (1 - self.p_popa))
        b_sqrt = sqrt(self.p_samc * (1 - self.p_samc) +
                      self.p_samt * (1 - self.p_samt))

        return (self.z_alpha * a_sqrt / self.p_delta +
                z_beta * b_sqrt / self.p_delta) ** 2

    def calc_power(self):
        """Calculate power based on sample size and alpha"""
        if self.total:
            pass
        else:
            print 'Please specify total for power calculation.'
            raise

        a_sqrt = sqrt(2 * self.p_popa * (1 - self.p_popa))
        b_sqrt = sqrt(self.p_samc * (1 - self.p_samc) +
                      self.p_samt * (1 - self.p_samt))

        z_beta = (sqrt(self.total) -
                  self.z_alpha * a_sqrt / self.p_delta) * \
                  self.p_delta / b_sqrt
        return scs.norm.cdf(z_beta)

if __name__ == '__main__':
    # Testing on known example
    # p_c, p_t, effect_size, alpha=.05, power=None, total=None, two_tailed=True
    p_samc = .259
    p_samt = .213
    effect_size = 0
    alpha = .05
    power = .8
    pp_obj = ProportionPower(p_samc, p_samt, effect_size,
                             alpha=alpha, power=power)
    total = pp_obj.calc_min_sample()  # 1396
    print 'total', total
    pp_obj.total = total
    print pp_obj.calc_power()  # .8


