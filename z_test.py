from numpy import sqrt
import scipy.stats as scs


def z_test(old_conversion, new_conversion, old_nrow, new_nrow,
           effect_size=0., two_tailed=True, alpha=.05):
    """z-test"""
    conversion = (old_conversion * old_nrow + new_conversion * new_nrow) / \
                 (old_nrow + new_nrow)

    se = sqrt(conversion * (1 - conversion) * (1 / old_nrow + 1 / new_nrow))

    z_score = (new_conversion - old_conversion - effect_size) / se

    if not two_tailed:
        p_val = 1 - scs.norm.cdf(abs(z_score))
    else:
        p_val = (1 - scs.norm.cdf(abs(z_score))) * 2

    reject_null = p_val < alpha
    print 'z-score: %s, p-value: %s, reject null: %s' % (z_score, p_val, reject_null)
    return z_score, p_val, reject_null

if __name__ == '__main__':
    old_p = 100. / 1000
    new_p = 105. / 1000
    old_row = 1000.
    new_row = 1000.
    z_test(old_p, new_p, old_row, new_row)