def test_2d_psystem():
    """test_2d_psystem"""

    def verify_data():
        def verify(controller):
            """ verifies gauge values generated by 2d psystem application 
            from a previously verified run """
            
            import os
            import numpy as np
            from clawpack.pyclaw.util import check_diff

            test_state = controller.solution.state

            gauge_files = test_state.grid.gauge_files
            test_gauge_data_mem = test_state.gauge_data
            expected_gauges=[]
            thisdir = os.path.dirname(__file__)
            
            expected_list=[]
            error_list=[]
            test_passed = True
            if test_gauge_data_mem is not None:
                for i, gauge in enumerate(gauge_files):
                    test_gauge_data_io = np.loadtxt(gauge.name)
                    verify_file = os.path.join(thisdir,'verify_' +
                                               gauge.name.split('/')[-1])
                    expected_gauges.append(np.loadtxt(verify_file))
                    return_value_mem = check_diff(expected_gauges[i], 
                                                  test_gauge_data_mem[i], 
                                                  reltol=1e-4)
                    return_value_io = check_diff(expected_gauges[i], 
                                                 test_gauge_data_io, 
                                                 reltol=1e-4)
                    
                    if (return_value_mem is not None or
                        return_value_io is not None):
                        expected_list.append(return_value_mem[0])
                        error_list.append([return_value_mem[1],return_value_io[1]])
                        test_passed = False


                if test_passed:
                    return None
                else:
                    return(expected_list, error_list,return_value_io[2] ,'')
            else:
                return
                
        return verify

    from clawpack.pyclaw.util import gen_variants
    import psystem_2d
    import shutil
    tempdir = './_for_temp_pyclaw_test'
    classic_tests = gen_variants(psystem_2d.setup, verify_data(),
                                 kernel_languages=('Fortran',), 
                                 solver_type='classic', 
                                 outdir=tempdir, cells_per_layer=6,
                                 tfinal=1.)
    from itertools import chain

    try:
        for test in chain(classic_tests):
            yield test

    finally:
        
        try:
            from petsc4py import PETSc
            PETSc.COMM_WORLD.Barrier()
        except ImportError:
            print """Unable to import petsc4py.
                   This should not be a problem unless you
                   are trying to run in parallel."""
        
        
        ERROR_STR= """Error removing %(path)s, %(error)s """
        try:         
            shutil.rmtree(tempdir )
        except OSError as (errno, strerror):
            print ERROR_STR % {'path' : tempdir, 'error': strerror }
            
        

if __name__=='__main__':
    f = test_2d_psystem()
    for test in f:
        test()
