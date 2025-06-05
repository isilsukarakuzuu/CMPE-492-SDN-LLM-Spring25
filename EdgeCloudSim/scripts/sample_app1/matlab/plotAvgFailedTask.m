function [] = plotAvgFailedTask()

    plotGenericResult(1, 2, 'Failed Tasks (%)', 'ALL_APPS', 'percentage_for_all');
    plotGenericResult(1, 2, 'Failed Tasks for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', 'percentage_for_all');
    plotGenericResult(1, 2, 'Failed Tasks for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', 'percentage_for_all');
    plotGenericResult(1, 2, 'Failed Tasks for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', 'percentage_for_all');
    plotGenericResult(1, 2, 'Failed Tasks for Non-LLM App (%)', 'NON_LLM_APP', 'percentage_for_all');

    plotGenericResult(2, 2, 'Failed Tasks on Edge (%)', 'ALL_APPS', 'percentage_for_all');
    plotGenericResult(2, 2, 'Failed Tasks on Edge for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', 'percentage_for_all');
    plotGenericResult(2, 2, 'Failed Tasks on Edge for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', 'percentage_for_all');
    plotGenericResult(2, 2, 'Failed Tasks on Edge for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', 'percentage_for_all');
    plotGenericResult(2, 2, 'Failed Tasks on Edge for Non-LLM App (%)', 'NON_LLM_APP', 'percentage_for_all');

    plotGenericResult(3, 2, 'Failed Tasks on Cloud (%)', 'ALL_APPS', 'percentage_for_all');
    plotGenericResult(3, 2, 'Failed Tasks on Cloud for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', 'percentage_for_all');
    plotGenericResult(3, 2, 'Failed Tasks on Cloud for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', 'percentage_for_all');
    plotGenericResult(3, 2, 'Failed Tasks on Cloud for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', 'percentage_for_all');
    plotGenericResult(3, 2, 'Failed Tasks on Cloud for Non-LLM App (%)', 'NON_LLM_APP', 'percentage_for_all');

end
