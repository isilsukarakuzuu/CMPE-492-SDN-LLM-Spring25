function [] = plotTaskFailureReason()

    plotGenericResult(1, 10, 'Failed Task due to VM Capacity (%)', 'ALL_APPS', 'percentage_for_failed');
    plotGenericResult(1, 10, 'Failed Task due to VM Capacity for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', 'percentage_for_failed');
    plotGenericResult(1, 10, 'Failed Task due to VM Capacity for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', 'percentage_for_failed');
    plotGenericResult(1, 10, 'Failed Task due to VM Capacity for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', 'percentage_for_failed');
    plotGenericResult(1, 10, 'Failed Task due to VM Capacity for Non-LLM App (%)', 'NON_LLM_APP', 'percentage_for_failed');

    plotGenericResult(1, 11, 'Failed Task due to Mobility (%)', 'ALL_APPS', 'percentage_for_failed');
    plotGenericResult(1, 11, 'Failed Task due to Mobility for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', 'percentage_for_failed');
    plotGenericResult(1, 11, 'Failed Task due to Mobility for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', 'percentage_for_failed');
    plotGenericResult(1, 11, 'Failed Task due to Mobility for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', 'percentage_for_failed');
    plotGenericResult(1, 11, 'Failed Task due to Mobility for Non-LLM App (%)', 'NON_LLM_APP', 'percentage_for_failed');

    plotGenericResult(5, 5, 'Failed Tasks due to WLAN failure (%)', 'ALL_APPS', 'percentage_for_failed');
    plotGenericResult(5, 5, 'Failed Tasks due to WLAN failure for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', 'percentage_for_failed');
    plotGenericResult(5, 5, 'Failed Tasks due to WLAN failure for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', 'percentage_for_failed');
    plotGenericResult(5, 5, 'Failed Tasks due to WLAN failure for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', 'percentage_for_failed');
    plotGenericResult(5, 5, 'Failed Tasks due to WLAN failure for Non-LLM App (%)', 'NON_LLM_APP', 'percentage_for_failed');

    plotGenericResult(5, 7, 'Failed Tasks due to WAN failure (%)', 'ALL_APPS', 'percentage_for_failed');
    plotGenericResult(5, 7, 'Failed Tasks due to WAN failure for Code Generator LLM App (%)', 'CODE_GENERATOR_LLM_APP', 'percentage_for_failed');
    plotGenericResult(5, 7, 'Failed Tasks due to WAN failure for General Use LLM App (%)', 'GENERAL_USE_LLM_APP', 'percentage_for_failed');
    plotGenericResult(5, 7, 'Failed Tasks due to WAN failure for Heavy Comp. LLM App (%)', 'HEAVY_COMP_LLM_APP', 'percentage_for_failed');
    plotGenericResult(5, 7, 'Failed Tasks due to WAN failure for Non-LLM App (%)', 'NON_LLM_APP', 'percentage_for_failed');

end