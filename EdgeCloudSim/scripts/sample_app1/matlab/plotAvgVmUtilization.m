function [] = plotAvgVmUtilization()

    plotGenericResult(2, 8, 'Average VM Utilization (%)', 'ALL_APPS', '');
    plotGenericResult(2, 8, 'Average VM Utilization for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', '');
    plotGenericResult(2, 8, 'Average VM Utilization for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', '');
    plotGenericResult(2, 8, 'Average VM Utilization for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', '');
    plotGenericResult(2, 8, 'Average VM Utilization for Non-LLM App (%)', 'NON_LLM_APP', '');

end