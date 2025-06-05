function [] = plotAvgServiceTime()

    plotGenericResult(1, 5, 'Service Time (sec)', 'ALL_APPS', '');
    plotGenericResult(1, 5, 'Service Time for Code Generator LLM App (sec)', 'CODE_GENERATOR_LLM_APP', '');
    plotGenericResult(1, 5, 'Service Time for General Use LLM App (sec)', 'GENERAL_USE_LLM_APP', '');
    plotGenericResult(1, 5, 'Service Time for Heavy Comp. LLM App (sec)', 'HEAVY_COMP_LLM_APP', '');
    plotGenericResult(1, 5, 'Service Time for Non-LLM App (sec)', 'NON_LLM_APP', '');

    plotGenericResult(2, 5, 'Service Time on Edge (sec)', 'ALL_APPS', '');
    plotGenericResult(2, 5, 'Service Time on Edge for Code Generator LLM App (sec)', 'CODE_GENERATOR_LLM_APP', '');
    plotGenericResult(2, 5, 'Service Time on Edge for General Use LLM App (sec)', 'GENERAL_USE_LLM_APP', '');
    plotGenericResult(2, 5, 'Service Time on Edge for Heavy Comp. LLM App (sec)', 'HEAVY_COMP_LLM_APP', '');
    plotGenericResult(2, 5, 'Service Time on Edge for Non-LLM App (sec)', 'NON_LLM_APP', '');

    plotGenericResult(3, 5, 'Service Time on Cloud (sec)', 'ALL_APPS', '');
    plotGenericResult(3, 5, 'Service Time on Cloud for Code Generator LLM App (sec)', 'CODE_GENERATOR_LLM_APP', '');
    plotGenericResult(3, 5, 'Service Time on Cloud for General Use LLM App (sec)', 'GENERAL_USE_LLM_APP', '');
    plotGenericResult(3, 5, 'Service Time on Cloud for Heavy Comp. LLM App (sec)', 'HEAVY_COMP_LLM_APP', '');
    plotGenericResult(3, 5, 'Service Time on Cloud for Non-LLM App (sec)', 'NON_LLM_APP', '');

end