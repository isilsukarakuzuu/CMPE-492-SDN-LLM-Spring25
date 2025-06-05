function [] = plotAvgNetworkDelay()

    plotGenericResult(1, 7, 'Average Network Delay (sec)', 'ALL_APPS', '');
    plotGenericResult(1, 7, 'Average Network Delay for Code Generator LLM App (sec)', 'CODE_GENERATOR_LLM_APP', '');
    plotGenericResult(1, 7, 'Average Network Delay for General Use LLM App (sec)', 'GENERAL_USE_LLM_APP', '');
    plotGenericResult(1, 7, 'Average Network Delay for Heavy Comp. LLM App (sec)', 'HEAVY_COMP_LLM_APP', '');
    plotGenericResult(1, 7, 'Average Network Delay for Non-LLM App (sec)', 'NON_LLM_APP', '');

    plotGenericResult(5, 1, 'Average WLAN Delay (sec)', 'ALL_APPS', '');
    plotGenericResult(5, 1, 'Average WLAN Delay for Code Generator LLM App (sec)', 'CODE_GENERATOR_LLM_APP', '');
    plotGenericResult(5, 1, 'Average WLAN Delay for General Use LLM App (sec)', 'GENERAL_USE_LLM_APP', '');
    plotGenericResult(5, 1, 'Average WLAN Delay for Heavy Comp. LLM App (sec)', 'HEAVY_COMP_LLM_APP', '');
    plotGenericResult(5, 1, 'Average WLAN Delay for Non-LLM App (sec)', 'NON_LLM_APP', '');

    plotGenericResult(5, 3, 'Average WAN Delay (sec)', 'ALL_APPS', '');
    plotGenericResult(5, 3, 'Average WAN Delay for Code Generator LLM App (sec)', 'CODE_GENERATOR_LLM_APP', '');
    plotGenericResult(5, 3, 'Average WAN Delay for General Use LLM App (sec)', 'GENERAL_USE_LLM_APP', '');
    plotGenericResult(5, 3, 'Average WAN Delay for Heavy Comp. LLM App (sec)', 'HEAVY_COMP_LLM_APP', '');
    plotGenericResult(5, 3, 'Average WAN Delay for Non-LLM App (sec)', 'NON_LLM_APP', '');

end
