from modules import refactor,methylation_data
from parsers import refactor_parser
from numpy import loadtxt, array_equal
from utils import LinearRegression
import logging
from tests.test_tools import tools
from cPickle import load

class SenariosTester():
    DATA  = "tests/refactor/files/test_datafile.txt"
    COVAR  = "tests/refactor/files/test_datafile_covars.txt"
    PHENO  = "tests/refactor/files/test_datafile_phenos.txt" #two phenotypes (the second one is binary)
    RES1  = "tests/refactor/files/test_datafile.refactor.no_covars.components.txt" 
    RES2  = "tests/refactor/files/test_datafile.refactor.covars.components.txt" 
    RES3  = "tests/refactor/files/test_datafile.refactor.controls_covars.components.txt"
    RES4  = "tests/refactor/files/test_datafile.refactor.pheno_covars.components.txt" 
        
    def __init__(self):
        logging.info("Testing Started on SenariosTester")
        bad_probes = set()
        [bad_probes.update(loadtxt(probes_file, dtype=str)) for probes_file in refactor_parser.BAD_PROBES_FILES]
        self.bad_probes = list(bad_probes)
        self.meth_data = methylation_data.MethylationDataLoader(datafile = self.DATA, covarfiles = [self.COVAR], phenofile = [self.PHENO])
        self.test_senario1()
        self.test_senario2()
        self.test_senario3()
        self.test_senario4()
        logging.info("Testing Finished on SenariosTester")

    def test_senario1(self):
        logging.info("Testing clean refactor components...")
        refactor_meth_data = self.meth_data.copy()

        comp = loadtxt(self.RES1)

        module  = refactor.Refactor(methylation_data = refactor_meth_data, 
                                    k = 5, 
                                    t = 500, 
                                    minstd = 0,
                                    bad_probes_list = self.bad_probes,
                                    use_phenos = None,
                                    use_covars = None)
        
        module.run()
        assert module.components.shape == comp.shape
        for i in range(module.components.shape[1]):
            assert tools.correlation(module.components[:,i], comp[:,i])
        logging.info("PASS")

    def test_senario2(self):
        logging.info("Testing ReFACTor with covariates...")
        refactor_meth_data = self.meth_data.copy()

        comp = loadtxt(self.RES2)

        module  = refactor.Refactor(methylation_data = refactor_meth_data, 
                                    k = 5, 
                                    t=500, 
                                    minstd = 0,
                                    bad_probes_list = self.bad_probes,
                                    use_phenos = None,
                                    use_covars = [])
        
        module.run()
        assert module.components.shape == comp.shape

        for i in range(module.components.shape[1]):
            assert tools.correlation(module.components[:,i], comp[:,i])
        logging.info("PASS")

    def test_senario3(self):
        logging.info("Testing controls feature selection...")
        refactor_meth_data = self.meth_data.copy()

        comp = loadtxt(self.RES3)

        module  = refactor.Refactor(methylation_data = refactor_meth_data, 
                                    k = 5, 
                                    t=500, 
                                    minstd = 0,
                                    bad_probes_list = self.bad_probes,
                                    feature_selection = 'controls',
                                    use_phenos = ['p2'],
                                    use_covars = [])
        module.run()
        assert module.components.shape == comp.shape

        for i in range(module.components.shape[1]):
            assert tools.correlation(module.components[:,i], comp[:,i])
        logging.info("PASS")

    def test_senario4(self):
        logging.info("Testing phenotype feature selection...")
        refactor_meth_data = self.meth_data.copy()

        comp = loadtxt(self.RES4)

        module  = refactor.Refactor(methylation_data = refactor_meth_data, 
                                    k = 5, 
                                    t=500, 
                                    minstd = 0,
                                    bad_probes_list = self.bad_probes,
                                    feature_selection = 'phenotype',
                                    use_phenos = ['p1'],
                                    use_covars = [])
        module.run()
        assert module.components.shape == comp.shape

        for i in range(module.components.shape[1]):
            assert tools.correlation(module.components[:,i], comp[:,i])
        logging.info("PASS")


class RefactorTester():
    DEMO_SMALL_DATA = "tests/files/datafile2"
    DEMO_DATA_NO_BAD_PROBES = "tests/refactor/files/demofiles/datafile2_no_bad_probes"
    DEMO_COVAR = "tests/refactor/files/demofiles/covariates"
    DEMO_PHENO = "tests/refactor/files/demofiles/phenotype"
    DEMO_CELLPRO = "tests/refactor/files/demofiles/cellproportions"
    BAD_PROBES = "tests/refactor/files/demofiles/bad_probes"

    # senarios output
    COMP_K5_T400 = "tests/refactor/files/senarios_out/k5t400.out.components.txt"
    RANK_K5_T400 = "tests/refactor/files/senarios_out/k5t400.out.rankedlist.txt"
    
    COMP_K5_T400_stdth01numcomp7 = "tests/refactor/files/senarios_out/k5t400stdth0.1numcomp7.out.components.txt"
    RANK_K5_T400_stdth01numcomp7 = "tests/refactor/files/senarios_out/k5t400stdth0.1numcomp7.out.rankedlist.txt"
    
    COMP_K5_T400_stdth013 = "tests/refactor/files/senarios_out/k5t400stdth0.13.out.components.txt"
    RANK_K5_T400_stdth013 = "tests/refactor/files/senarios_out/k5t400stdth0.13.out.rankedlist.txt"
    
    COMP_K5_T400_covar = "tests/refactor/files/senarios_out/k5t400covar.out.components.txt"
    RANK_K5_T400_covar = "tests/refactor/files/senarios_out/k5t400covar.out.rankedlist.txt"
  
    COMP_K5_T400_stdth008covar = "tests/refactor/files/senarios_out/k5t400stdth0.08covar.out.components.txt"
    RANK_K5_T400_stdth008covar = "tests/refactor/files/senarios_out/k5t400stdth0.08covar.out.rankedlist.txt"

    def __init__(self):
        logging.info("Testing Started on RefactorTester")
        self.meth_data = methylation_data.MethylationData
        self.meth_data = methylation_data.MethylationDataLoader(datafile = self.DEMO_SMALL_DATA, covarfiles = [self.DEMO_COVAR], phenofile = [self.DEMO_PHENO])
        self.test_remove_covariates()
        self.test_low_rank_approx_distances()
        self.test_exclude_bad_probes()

        logging.info("Testing Finished on RefactorTester")

    def test_remove_covariates(self):
        logging.info("Testing removing covariates...")
        covar_meth_data = self.meth_data.copy()
        covar_meth_data.regress_out(self.meth_data.covar) # regress out all covariates

        coavr, covarnames = covar_meth_data._load_and_validate_covar([self.DEMO_COVAR], covar_meth_data.samples_size, covar_meth_data.samples_ids)
        
        # remove "manually"
        for i,site in enumerate(self.meth_data.data):
            residuals = LinearRegression.regress_out(site, coavr)
            assert len(residuals) == len(site)
            assert tools.correlation(residuals, covar_meth_data.data[i])

        logging.info("PASS")


    def test_low_rank_approx_distances(self):
        """
        tests that number of distances is as the number of sites (distance for every site)
        """
        logging.info("Testing low rank approx distances...")
        dis_meth_data = self.meth_data.copy()

        module  = refactor.Refactor(methylation_data = dis_meth_data, 
                                    k = 5)

        distances = module._calc_low_rank_approx_distances(dis_meth_data)
        assert distances.size == dis_meth_data.sites_size, "there must be distances as the number of sites"
        logging.info("PASS")

    
    def test_exclude_bad_probes(self):
        logging.info("Testing removing bad probes...")
        probes_meth_data = self.meth_data.copy()

        data_no_bad_probes = methylation_data.MethylationDataLoader(datafile = self.DEMO_DATA_NO_BAD_PROBES)

        bad_probes = load(open(self.BAD_PROBES,'r'))
        module  = refactor.Refactor(methylation_data = probes_meth_data, 
                                    k = 5, 
                                    bad_probes_list = bad_probes)

        module._exclude_bad_probes()


        assert array_equal(data_no_bad_probes.data, module.meth_data.data)

        # tests sites list has changed
        remove_count = len(bad_probes)
        orig_sites_before = []
        orig_sites_before.extend(self.meth_data.cpgnames)
        orig_sites_after = []
        orig_sites_after.extend(module.meth_data.cpgnames)
        for i in bad_probes:
            try:
                orig_sites_before.remove(i)
            except:
                remove_count -= 1
        assert orig_sites_after == orig_sites_before
        # test sites size
        assert self.meth_data.sites_size - remove_count == module.meth_data.sites_size

        logging.info("PASS")
