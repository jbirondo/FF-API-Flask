import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

ADP_URL = 'https://www.fantasypros.com/nfl/adp/ppr-overall.php'


res = requests.get(ADP_URL)
soup = BS(res.content, 'html.parser')
table = soup.find('table', {'id': 'data'})

adp_df = pd.read_html(str(table))[0]

adp_df['Team'] = adp_df['Player Team (Bye)'].apply(lambda x: x.split()[-2])
adp_df['Player'] = adp_df['Player Team (Bye)'].apply(lambda x: ' '.join(x.split()[:-2]))

adp_df['Player'] = adp_df['Player'].apply(lambda x: ' '.join(x.split()[:2]))

adp_df['POS'] = adp_df['POS'].apply(lambda x: x[:2])
adp_df = adp_df.loc[:, ['Player', 'Team', 'POS', 'AVG']]

adp_df['ADP_RANK'] = adp_df['AVG'].rank(method='first')



for format in ["standard", "halfppr", "ppr"]:

    df = pd.read_csv('https://raw.githubusercontent.com/fantasydatapros/2021-VOR-Model/master/data/all_compiled.csv', thousands=',')

    df = df.iloc[:, 1:]

    scoring_weights = {
        'receiving_yds': 0.1,
        'receiving_td': 6,
        'FL': -2, #fumbles lost
        'rushing_yds': 0.1,
        'rushing_td': 6,
        'passing_yds': 0.04,
        'passing_td': 6,
        'int': -2
    }

    if format == "standard":
        scoring_weights["receptions"] = 0.0
    elif format == "halfppr":
        scoring_weights["receptions"] = 0.5
    else:
        scoring_weights["receptions"] = 1.0
   
    df['FantasyPoints'] = (
        df['REC']*scoring_weights['receptions'] + \
        df['REC_YD']*scoring_weights['receiving_yds'] + \
        df['REC_TD']*scoring_weights['receiving_td'] + \
        df['FL']*scoring_weights['FL'] + \
        df['RUSH_YD']*scoring_weights['rushing_yds'] + \
        df['RUSH_TD']*scoring_weights['rushing_td'] + \
        df['PASS_YD']*scoring_weights['passing_yds'] + \
        df['PASS_TD']*scoring_weights['passing_td'] + \
        df['INTS']*scoring_weights['int'] 
        )


    # adp_df['ADP RANK'] = adp_df['AVG'].rank()

    adp_df_cutoff = adp_df[:100]

    replacement_players = {
        'RB': '',
        'QB': '',
        'WR': '',
        'TE': ''
    }

    for _, row in adp_df_cutoff.iterrows():
        
        position = row['POS']
        player = row['Player']
        
        if position in replacement_players:
            replacement_players[position] = player 

    df = df[['Player', 'POS', 'FantasyPoints']]


    replacement_values = {} 

    for position, player_name in replacement_players.items():
        
        player = df.loc[df['Player'] == player_name]
        
        replacement_values[position] = player['FantasyPoints'].tolist()[0]

    pd.set_option('chained_assignment', None)

    df = df.loc[df['POS'].isin(['QB', 'RB', 'WR', 'TE'])]


    df['VOR'] = df.apply(
        lambda row: row['FantasyPoints'] - replacement_values.get(row['POS']), axis=1
    )

    pd.set_option('display.max_rows', None) 

    df['VOR Rank'] = df['VOR'].rank(ascending=False)

    df['VOR'] = df['VOR'].apply(lambda x: (x - df['VOR'].min()) / (df['VOR'].max() - df['VOR'].min()))

    df = df.sort_values(by='VOR Rank')

    df = df.rename({
        'VOR': 'Value',
        'VOR Rank': 'Value Rank'
    }, axis=1) 

    adp_df = adp_df.rename({
        'AVG': 'Average ADP',
        'ADP_RANK': 'ADP Rank'
    }, axis=1) 

    final_df = df.merge(adp_df, how='left', on=['Player', 'POS'])
    final_df = final_df.rename({
        'POS': 'Pos'
    })
    final_df['Diff in ADP and Value'] = final_df['ADP Rank'] - final_df['Value Rank']

    draft_pool = final_df.sort_values(by='ADP Rank')[:196]

    rb_draft_pool = draft_pool.loc[draft_pool['POS'] == 'RB']
    qb_draft_pool = draft_pool.loc[draft_pool['POS'] == 'QB']
    wr_draft_pool = draft_pool.loc[draft_pool['POS'] == 'WR']
    te_draft_pool = draft_pool.loc[draft_pool['POS'] == 'TE']

    sleeper_rbs = rb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]
    overvalued_rbs = rb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]

    sleeper_wrs = wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]
    overvalued_wrs = wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]

    sleeper_tes = wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]
    overvalued_tes = wr_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]

    sleeper_qbs = qb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=False)[:10]
    overvalued_qbs = qb_draft_pool.sort_values(by='Diff in ADP and Value', ascending=True)[:10]

    json = final_df[:].to_json(orient="records")

    f = open("2021_{name}".format(name=format) + ".json", "w")
    print ("Writing {}...".format(format))
    f.write(json)
    f.close()






