import pandas as pd
import numpy as np

def scatter_comparison_data(data, question = 'turnover'):
    #format data for scatter comparison plots 
    d = data.copy()
    tot_groups = d.groupby('source').size().reset_index()
       
    if question == 'turnover':
        q = [f'turnover_priorities_{i}' for i in range(1,9)]
        map_labels = {'turnover_priorities_1':'Cost savings', 
              'turnover_priorities_2':'Vehicle reliability',
              'turnover_priorities_3':'Emissions reduction',
              'turnover_priorities_4':'Regulatory compliance',
              'turnover_priorities_5':'Operational efficiency',
              'turnover_priorities_6':'Driver comfort and satisfaction',
              'turnover_priorities_7':'Technology integration', 
              'turnover_priorities_8':'Brand image'}
        column_name = 'Priorities'
    elif question == 'financial':
        q = [f'turnover_financial_{i}' for i in range(1,10)]
        map_labels = {'turnover_financial_1':'Upfront vehicle acquisition', 
              'turnover_financial_2':'Fuel and energy',
              'turnover_financial_3':'Maintenance and repairs',
              'turnover_financial_4':'Depreciation',
              'turnover_financial_5':'Insurance premiums',
              'turnover_financial_6':'Tax incentives',
              'turnover_financial_7':'Financing or leasing terms', 
              'turnover_financial_8':'Lifecycle cost optimization', 
            'turnover_financial_9':'Budget stability'}
        column_name = "Financial"
    elif question == 'barriers':
        q=  [f'renewal_barriers_{i}' for i in range(1,12)]
        map_labels = {'renewal_barriers_1':'Capital costs<br> for new vehicles', 
              'renewal_barriers_2':'Limited availability of<br> suitable models',
              'renewal_barriers_3':'Operational disruptions<br> during the transition',
              'renewal_barriers_4':'Uncertainty around future<br> regulations',
              'renewal_barriers_5':'Insufficient charging/fueling<br> infrastructure',
              'renewal_barriers_6':'Limited internal capacity<br> for planning and implementation',
              'renewal_barriers_7':'Lack of access to <br>financing or incentives', 
              'renewal_barriers_8':'Concerns about vehicle <br>performance or reliability', 
            'renewal_barriers_9':'Data or technology <br>integrations challenges',
               'renewal_barriers_10': 'Resistance to change <br>within the organization',
                    'renewal_barriers_11': 'Other'}
        column_name = "Barriers"
    else: 
        return None

    d = d.groupby('source')[q].sum().reset_index()
    d['total'] = tot_groups[0]

    for c in q:
        d[c] = 100*d[c]/d['total']

    d = d.drop('total', axis = 1).pivot_table(columns = 'source').reset_index()
    d['index'] = d['index'].map(map_labels)
    ordered_df = d.sort_values(by='Fleet managers').rename(columns = {'index': column_name}).reset_index(drop = True)
    
    return ordered_df

def likert_data(data, question = 'decision_tools', source = 'Fleet managers'):
    d = data.copy()

    if question == "decision_tools":
        q = [c for c in d.columns if c.startswith(question)&(c != 'decision_tools_other')]
        likert_map = {2: "Rarely or never", 3: "Sometimes", 4: "Often"}
        top_labels = ['Rarely or never', 'Sometimes', 'Often']
        q_labels = {'decision_tools_cost':'Cost analysis tools', 
            'decision_tools_maintenance': 'Maintenance and <br> performance tracking', 
            'decision_tools_telematics':'Telematics or vehicle <br>usage data', 
            'decision_tools_emissions':'Emissions performance <br> or reduction target', 
            'decision_tools_regulations':'Regulatory compliance<br> assessment',
            'decision_tools_consulting': 'External consulting <br> or advisory services',
            'decision_tools_AI': 'A.I. tools'}

    elif question == "innovation": 
        q = [c for c in d.columns if c.startswith(question)&(c not in ['innovation_other', 'innovation_other_TEXT', 'innovation_best_TEXT', 'innovation_worst_TEXT'])]
        likert_map = {1: "Not likely", 2: "Somewhat likely", 3: "Very likely"}
        top_labels = ['Not likely', 'Somewhat likely', 'Very likely']
        q_labels = {'innovation_ice': 'Replacing older ICE <br>with newer ICE',
            'innovation_hybrid':'Transitioning to <br>hybrid vehicles', 
            'innovation_bev':'Transitioning to BEV',  
            'innovation_hydrogen':'Transitioning to hydrogen<br> fuel cell vehicles', 
            'innovation_telematic': 'Adopting telematics, <br>smart fleet management tools', 
            'innovation_ai': 'Adopting A.I. tools for <br>planning and operations', 
            'innovation_route':'Implementing route optimization<br> and logistics innovation'}

    d = d[[c for c in d.columns if c=='source' or c in q]]

    d = d.melt(id_vars="source", var_name="question", value_name="response")
    d["response"] = d["response"].map(likert_map)

    group_counts = d.groupby(["source", "question", "response"]).size().reset_index(name="count")

    # Pivot for stacked bar plot (absolute counts)
    group_props = group_counts.pivot_table(index=["source", "question"],columns="response",values="count",fill_value=0)

    # Normalize to proportions 
    group_props_norm = group_props.div(group_props.sum(axis=1), axis=0).reset_index()

    for col in top_labels:
        group_props_norm[col] = group_props_norm[col]*100

    d = group_props_norm[group_props_norm.source == source].sort_values(by = top_labels[-1])
    xdata = d[top_labels].values
    ydata = [q_labels[x] for x in d['question'].values]

    return xdata, ydata, top_labels


def timeline_data(data, question = 'replace'):

    d = data.copy()

    if question == "replace":
        column = "replace_pre2010"
    elif question == "expand":
        column = "expand_fleet"

    d = d.groupby(['source', column]).size().reset_index(name="count")
    d = d[d[column] != 5] #remove non applicable answers 

    labels = {1: 'Yes, within <br>the next 3 years', 2:'Yes, in more <br> than 3 years', 3: 'No', 4: 'Not sure'}
    d[column] = d[column].map(labels)

    d = d.pivot_table(index="source",columns=column,values="count",fill_value=0)
    d = d.div(.01*d.sum(axis=1), axis=0).reset_index()

    top_labels = ['No', 'Not sure',  'Yes, in more <br> than 3 years', 'Yes, within <br>the next 3 years']
    xdata = d[top_labels].values
    ydata = d.source.values    
    return xdata, ydata, top_labels


def ranking_data(data, source = "Fleet managers"):
    d = data.copy()
    rank_support_q = [c for c in d.columns if c.startswith('rank_support')]
    rank_support_q = rank_support_q[:-1]

    if source == "All":
        tot = len(d[~d['rank_support_financial'].isna()])
    else:
        d = d[d.source == source]
        tot = len(d[(~d['rank_support_financial'].isna())& (d.source == source)])
    
    d = d.melt(id_vars = ['id'], value_vars = rank_support_q, var_name = 'question', value_name = 'response').dropna()
    d = d.groupby(['question', 'response']).size().reset_index().rename(columns = {0: 'counts'})
    dmax = d.groupby(['question', 'response'])['counts'].sum().reset_index()
    dmax['percentage'] = 100*dmax['counts']/tot

    dfirst = dmax[dmax.response == 1].sort_values(by = 'counts', ascending = False).reset_index(drop=True)

    return dfirst