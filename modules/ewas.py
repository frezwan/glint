from utils import LinearRegression #, plot
from numpy import column_stack, ones, savetxt, array
from module import Module
from utils import common, plot
import logging

"""
copy meth_data in advance
"""
class EWAS(Module):
    AVALIABLE_TESTS = ['linear_regression', 'logistic_regression']
    TEST_FUNC_NAME_FORMAT = "_{test_name}_test"   # feature selections function name format

    def __init__(self, methylation_data, tests_list):
        self.meth_data = methylation_data
        self.test_handlers = self._get_test_handler(tests_list)

    def run(self):
        logging.info('starting EWAS...');
        results = [test_handler(output_filename = 'ewas_' + test_name) for (test_name,test_handler) in self.test_handlers]
        logging.info('EWAS is Done!')

    def _get_test_handler(self, tests_list):
        # check that the tests in test_list are all optional tests (found in AVALIABLE_TESTS)
        if set(set(tests_list).difference(set(self.AVALIABLE_TESTS))) == 0:
            common.terminate('tests %s are not available' % str(set(tests_list).difference(set(self.AVALIABLE_TESTS))))

        return [(test,getattr(self, self.TEST_FUNC_NAME_FORMAT.format(test_name=test))) for test in tests_list]

    def _logistic_regression_test(self, output_filename = None):
        pass
        
    def _linear_regression_test(self, output_filename = None):
        """
        linear regression test
        """
        logging.info("running linear regression test...")
        output = []
        if self.meth_data.covar is not None:
            for i, site in enumerate(self.meth_data.data):
                test = column_stack((ones(len(site)), site, self.meth_data.covar))
                lin_reg = LinearRegression(self.meth_data.phenotype, test)
                output.append([self.meth_data.cpgnames[i], lin_reg.p_value, lin_reg.t_statistic, lin_reg.coef])
        else:
            for i, site in enumerate(self.meth_data.data):
                test = column_stack((ones(len(site)), site))
                lin_reg = LinearRegression(self.meth_data.phenotype, test)
                output.append([self.meth_data.cpgnames[i], lin_reg.p_value, lin_reg.t_statistic, lin_reg.coef])
        
        
        output.sort(key = lambda x: x[1]) # sort output by p-value
        output = array(output)

        if output_filename:
            qqplot_out = output_filename + '_qqplot' # TODO change this?
            logging.info("savings results to %s and qq-plot to %s" % (output_filename, qqplot_out))  
            savetxt(output_filename, output, fmt='%s')
            # plot the p-value
            qqplot = plot.QQPlot(save_file = qqplot_out)
            qqplot.draw(output[:,1].astype(float), title = "TODO CHANGE THIS", xtitle="TODO change this x", ytitle = "TODO change this y")

        return output

