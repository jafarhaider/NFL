# graph all the data into four graphs

from main import *

FONT = fm.FontProperties(fname='/Library/Fonts/Lato-Medium.ttf')

G1 = '#979797'
G2 = '#4D4D4D'
G3 = '#7A7A7A'
G4 = '#222222'
font_color = '#FFFFFF'
font_color2 = G4
call_color = '#fb8072'

brewer2 = [
    '#66c2a5',
    '#fc8d62',
    '#8da0cb',
    '#e78ac3',
    '#a6d854',
    '#ffd92f',
    '#e5c494',
    '#b3b3b3'
    ]
palette = ["#C7D1FA",
    "#35DD40",
    "#B53F01",
    "#3B082F",
    "#BB5FF1",
    "#62710E",
    "#A2F8C0",
    "#F587AA",
    "#31270E",
    "#D5A41D",
    "#289A7F",
    "#BFF058",
    "#EEAE9F",
    "#42F4EA",
    "#46B1D5",
    "#7C000D",
    "#833AA6",
    "#14731C",
    "#FB794C",
    "#59480F",
    "#6C1656"]

xStart = firstYear - .3
xEnd = lastYear + .3
yStart = -3.3
yEnd = 3.3

# change p to statistic_name
def find_y(stat, y_pos, col):
    if stat == 'pass_yds':
        if col == 'New England Patriots':
            y_pos += .075
        elif col == 'San Diego Chargers':
            y_pos -= .075
        elif col == 'Detroit Lions':
            y_pos -= .15
        elif col == 'Green Bay Packers':
            y_pos += .025
        elif col == 'Arizona Cardinals':
            y_pos += .05
        elif col == 'Dallas Cowboys':
            y_pos -= .05
        elif col == 'Kansas City Chiefs':
            y_pos -= .05
        elif col == 'Seattle Seahawks':
            y_pos -= .1
        elif col == 'Tennessee Titans':
            y_pos += .05
        elif col == 'Baltimore Ravens':
            y_pos += .05
        elif col == 'Chicago Bears':
            y_pos -= .05
        elif col == 'Cleveland Browns':
            y_pos -= .05
        elif col == 'Jacksonville Jaguars':
            y_pos += .05
    elif stat == 'pass_yds_per_att':
        if col == 'San Diego Chargers':
            y_pos += .1
        elif col == 'Atlanta Falcons':
            y_pos -= .05
        elif col == 'San Francisco 49ers':
            y_pos += .075
        elif col == 'Carolina Panthers':
            y_pos -= .1
        elif col == 'Philadelphia Eagles':
            y_pos -= .05
        elif col == 'Tampa Bay Buccaneers':
            y_pos -= .075
        elif col == 'Miami Dolphins':
            y_pos += .075
        elif col == 'Cleveland Browns':
            y_pos += .05
        elif col == 'Baltimore Ravens':
            y_pos += .05
        elif col == 'Arizona Cardinals':
            y_pos -= .05
        elif col == 'Detroit Lions':
            y_pos += .075
        elif col == 'Cincinnati Bengals':
            y_pos -= .075
    return y_pos

def create(titleText, subTitleText):
    fig = plt.figure(figsize=(18,12), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    # plot dotted line across
    for y in xrange(-3, 4, 1):
        ax.plot(range(firstYear, lastYear), [y] * len(range(firstYear, lastYear)), "--",
            lw=1.5, color=G3, alpha=.75)
    for x in xrange(firstYear,lastYear):
        ax.plot(range(-3,4,1), [x] * len(range(-3, 4)), "|",
            lw=1.5, color=G3, alpha=.75)

    # titles & axes
    ax.set_xlim(xStart, xEnd)
    ax.set_ylim(yStart, yEnd)

    ax.set_xticks(list(xrange(firstYear, lastYear, 2)))

    ax.tick_params(
        axis='both',
        which='both',
        bottom='off',
        top='off',
        left='off',
        right='off')

    # set color
    fig.patch.set_facecolor(G4)
    ax.patch.set_facecolor(G4)

    # remove borders!
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # format ticks
    a = fig.gca()
    a.set_xticklabels(a.get_xticks(), fontproperties=FONT, size=16, color=font_color)
    a.set_yticklabels(a.get_yticks(), fontproperties=FONT, size=16, color=font_color)

    fig.subplots_adjust(left=0.05, right=0.9, top=0.9, bottom=0.05)

    # title and subtitle
    ax.text(.5*(firstYear+lastYear), 3.8,titleText, color=font_color, fontproperties=FONT,
        horizontalalignment='center', verticalalignment='center', size=24)
    ax.text(.5*(firstYear+lastYear), 3.5,subTitleText, color=font_color, fontproperties=FONT,
        horizontalalignment='center', verticalalignment='center', size=20)

    ax.text(lastYear - .5, -3.25, 'Source:\n    Pro Football Reference\nAuthor:\n    Jafar Haider',
        fontsize=14, color=G3, fontproperties=FONT, verticalalignment='center', horizontalalignment='left')

    return fig, ax

def save(fig, stat, _title_, _type_):
    # path
    outpng1 = "%smatplotlib/%s/%s/png/" % (output_prefix, stat, _type_)
    outpdf1 = "%smatplotlib/%s/%s/pdf/" % (output_prefix, stat, _type_)
    # ensure folder exists
    for x in [outpng1]: #, outpdf1]:
        try:
            os.makedirs(x)
        except OSError:
            if not os.path.isdir(x):
                raise

    my_dpi = 96
    outpng2 = '%s%s.png' % (outpng1, _title_)
    outpdf2 = '%s%s.pdf' % (outpdf1, _title_)
    fig.savefig(outpng2, facecolor=fig.get_facecolor(), edgecolor='none', figsize=(1800/my_dpi, 1200/my_dpi), dpi=my_dpi)
    # fig.savefig(outpdf2, facecolor=fig.get_facecolor(), edgecolor='none', figsize=(1800/my_dpi, 1200/my_dpi), dpi=my_dpi)

    plt.close('all')

def quarter(cumAvgDF, stat, _title_, _sub_, _numLow_, _numHigh_, _seasons_, _avg_):

    # s2 = pd.DataFrame(zscore(curDF.loc[(curDF['season'] == yr)][stat])).mean()
    # sort in order to grab the right quartile
    # grab the relevant times for the given statistic
    sortDF = cumAvgDF.sort(stat, ascending=False)[_numLow_:_numHigh_]
    # top = original.sort(stat, ascending=False)[_numLow_:_numHigh_]
    curTeams = list(sortDF['Tm'])
    print curTeams

    df = original.loc[original['Tm'].isin(curTeams)]

    # convert the DF to something useable
    df = df[['Tm','season', stat]]
    df = df.pivot('season', 'Tm', stat)
    # df.to_csv(test_csv)

    # initalize variables
    titleText = '%s Ranked Teams' % _title_
    fileText = titleText
    subTitleText = 'Z-Score of %s by season (1998-2014)' % _sub_

    # create fig and ax
    fig,ax = create(titleText,subTitleText)

    # plot lines
    for i, col in enumerate(df.columns):
        ax.plot(_seasons_, df[col], linewidth=3.75, label=col,
                solid_joinstyle='round', solid_capstyle='round',
                color=brewer2[i],
                marker='o', markersize=7.5, markeredgecolor='none'
                )
        # ax.scatter(seasons, df[col], c=brewer2[i], s=250, alpha=1)

        # # create an inline legend
        # y_pos determines vertical position of text
        y_pos = df[col].tail(1)
        y_pos = find_y(stat,y_pos, col)
        ax.text(lastYear - .5, y_pos, col, fontsize=16, color=brewer2[i],
                fontproperties=FONT, verticalalignment='center')

    avgText = 'Average %s\n    per Season' % _sub_
    ax.text(lastYear - .5, 3.15, avgText, fontsize=12,color=font_color,fontproperties=FONT,
        verticalalignment='center', horizontalalignment='left')

    # print the season averages!
    for j, season in enumerate(_seasons_):
        locale.setlocale(locale.LC_ALL, 'en_US')
        val = _avg_[_avg_.columns[j]].values.round(0).astype(int)
        val = locale.format("%d",val,grouping=True)
        val = str(val).replace('[','').replace(']','')
        ax.text(season, 3.15, val, fontproperties=FONT, fontsize=12, color=font_color,
            verticalalignment='center', horizontalalignment='center')

    save(fig, stat, _title_, 'quarter')

def callout(stat, _teamNum_, _sub_, _seasons_, df):

    # grab the current team name
    curTeam = df.columns[_teamNum_]

    # initalize variables
    titleText = '%s' % curTeam
    fileText = titleText
    subTitleText = 'Z-Score of %s by season (1998-2014)' % _sub_
    xText = 'Season'
    yText = "Team's %s Z-Score" % _sub_

    # create fig and ax
    fig, ax = create(titleText, subTitleText)

    # plot lines
    for i, col in enumerate(df.columns):
        if _teamNum_ == i:
            # plot line
            ax.plot(_seasons_,df[col], linewidth=7.5, label=col,
            solid_joinstyle='round', solid_capstyle='round',
            color = call_color,
            marker='o', markersize=25, markeredgecolor='none', zorder=3
            )

            # plot text
            for i, row in enumerate(df[col].values):
                ax.annotate(row.round(1), xy=(df.index[i],row),
                    ha='center', va='center',
                    fontproperties=FONT, color=font_color2, fontsize=12)

            # set inline legend
            y_pos = df[col].tail(1)
            ax.text(lastYear - .5, y_pos, col, fontsize=18, color=call_color,
                fontproperties=FONT, verticalalignment='center')

        else:
            ax.plot(_seasons_,df[col], linewidth=3.75, label=col,
                solid_joinstyle='round', solid_capstyle='round',
                color = G2,
                marker='o', markersize=7.5, markeredgecolor='none', zorder=2
                )

    addPlayoffs(ax, _seasons_, curTeam)
    # save
    save(fig, stat, curTeam, 'callout')

def team_specific(j, team):
    print '\t%s' % team

    fig, ax = create(team, 'All Metrics')

    for i, stat in enumerate(statistic_names):

        z = original[var_dict[stat]['z']]
        seasons = list(z.columns.values)
        seasons = [int(item[:4]) for item in seasons]
        df = original.loc[original['team'] == team]
        df = df[var_dict[stat]['z']]
        df = df.transpose()

        ax.plot(seasons,df, linewidth=3.75, color = palette[i],
            solid_joinstyle='round', solid_capstyle='round', marker='o', markersize=7.5, markeredgecolor='none', alpha=.75)
        y_pos = df[j].tail(1)
        y_pos = find_y(stat,y_pos, team)
        ax.text(lastYear - .5, y_pos, stat, fontsize=16, color=palette[i],
                fontproperties=FONT, verticalalignment='center')
    addPlayoffs(ax, seasons, team)
    save(fig, 'team', team, 'team')

    plt.close('all')

def addPlayoffs(ax, seasons, team):
    # print playoff standings to figure
    playoffDF = pd.read_csv(playoffs_csv)
    for season in seasons:
        status = ''
        getSeason = playoffDF.loc[playoffDF['season']==season]
        if team in getSeason['lost'].values:
            # getSeason.set_index('lost')
            status = list(getSeason['round'][playoffDF['lost']==team])[0]
            ax.text(season, 3.3, 'Lost:', fontsize=12, color=font_color,
            fontproperties=FONT, verticalalignment='center', ha='center',alpha = .75)

        elif team in getSeason['won'].values:
            sortedDF = getSeason.sort(ascending=False)
            status = list(getSeason['round'][sortedDF['won']==team])
            status = status[len(status) - 1]
            ax.text(season, 3.3, 'Won:', fontsize=12, color=font_color,
            fontproperties=FONT, verticalalignment='center', ha='center', alpha = .75)

        if status != '':
            status = status.replace('ConfChamp', 'Champ')
        ax.text(season, 3.15, status, fontsize=12, color=font_color,
            fontproperties=FONT, verticalalignment='center', ha='center',alpha = .75)


# read in the analysis file as a df
infile = '%sdf.csv' % data_prefix
original = pd.read_csv(infile)
# statistic_names.remove('pass_yds_per_g')
# get the header names which start with a z_ - these are your seasons
# saved as ints - used for the x axis in the line graph

def main():
    stats = [
        "Cmp",
        "Att",
        "Cmp%",
        "Yds",
        "TD",
        "TD%",
        "Int",
        "Int%",
        "Y/A",
        "Y/C",
        "Y/G"
        ]

    # list of the z variables
    z_stats = ['z_' + x for x in stats]

    # list of the seasons being used
    # type int, 1998-2014
    seasons = [x for x in range(firstYear, lastYear)]

    # list of teams
    teams = list(unique_everseen([x for x in original['Tm']]))

    stats = ['Yds']
    z_stats = ['z_Yds']
    # quarter
    for i, stat in enumerate(stats):

        graph_title = stat\
            .replace('Cmp%', 'Completion Percentage')\
            .replace('Int%', 'interception Percentage')\
            .replace('TD%', 'Touchdown Percentage')\
            .replace('Cmp','CompletionS')\
            .replace('Att', 'Attempts')\
            .replace('%',' Percentage')\
            .replace('TD', 'Touchdowns')\
            .replace('Int', 'interceptions')\
            .replace('Yds', 'yards')\
            .replace('Y', 'yards')\
            .replace('/A', '/Attempt')\
            .replace('/C', '/Completion')\
            .replace('/G', '/Game')\
            .title()

        print '%s: quarter' % graph_title

        # quarter
        # z = original[var_dict[stat]['z']]

        # find an average and add that to the figure
        avg = pd.DataFrame(columns=original.columns.values)
        avg = avg.append(original.mean(axis=0), ignore_index=True)
        print avg
        avg = avg[[stat]]
        avg.to_csv(test_csv)

        my_dpi=96
        # z_stats[i]
        quarter(cumAvgDF, 'z_Yds', 'Top 8', graph_title, 0, 8, seasons, avg)
        """
        quarter(stat, '9-16', graph_title, 8, 16, seasons, avg)
        quarter(stat, '17-24', graph_title, 16, 24, seasons, avg)
        quarter(stat, 'Bottom 8', graph_title, 24, 32, seasons, avg)
        plt.close('all')
        """
        """
        # callouts
        print 'callouts'

        # get the header names which start with a z_ - these are your seasons
        # saved as ints - used for the x axis in the line graph

        z = original[var_dict[stat]['z']]
        seasons = list(z.columns.values)
        seasons = [int(item[:4]) for item in seasons]

        # after sorting, the top 8 teams are the top 1/4
        top = original.sort(var_dict[stat]['z_avg'], ascending=False)

        # rename the columns without the z
        df = top[var_dict[stat]['z']]
        new = df.columns.values
        new = [item[:4] for item in new]
        df.columns = new

        # transpose and modify the df as necessary
        df = df.join(top['team'])
        df = df.set_index('team')
        df = df.transpose()
        df = df.reset_index()
        df = df.rename(columns={'index':'year'})
        df = df.set_index('year')

        cols = df.columns.tolist()
        # for team in xrange(0,1):
        for team in xrange(0,len(df.columns)):
            print '\t%s' % cols[team]
            callout(stat, team, graph_title, seasons, df)

    print 'team specific'
    teams = original['team']
    # teams = ['Arizona Cardinals']
    # print len(statarams)

    for j, team in enumerate(teams):
        team_specific(j, team)

    volume_stats = [
        'pass_att',
        'pass_cmp',
        # 'pass_int',
        'pass_td',
        'pass_yds',
        ]

    efficiency_stats = [
        'pass_yds_per_att',
        'pass_yds_per_cmp',
        'pass_yds_per_g',
        'pass_td_perc',
        'pass_cmp_perc',
        # 'pass_int_perc',
        ]

    stat_type = {'Volume Statistics': volume_stats, 'Efficiency Statistics': efficiency_stats}
    # stat_type = {'Volume Statistics': volume_stats}
    z = original[var_dict['pass_yds']['z']]
    seasons = list(z.columns.values)
    seasons = [int(item[:4]) for item in seasons]
    teams = original['team']


    for j, team in enumerate(teams):

        for key, value in stat_type.items():
            teamDF = pd.DataFrame()
            for stat in value:
                df = original.loc[original['team'] == team]
                df = df[var_dict[stat]['z']]
                teamDF = teamDF.append(df)
                teamDF = teamDF.groupby(teamDF.index).max()


            for season in seasons:
                season = str(season)
                newCol = 'mean_%s_%s' % (season, key)
                teamDF[newCol] = teamDF.filter(regex=season).mean(axis=1)

            teamDF = teamDF.filter(regex='mean_')
            new = teamDF.columns.values
            new = [item[5:9] for item in new]
            teamDF.columns = new
            teamDF = teamDF.transpose()

                curColor = '#66c2a5'
                fig, ax = create(team, 'Comparison')

            else:
                curColor = '#fc8d62'

            ax.plot(seasons,teamDF, linewidth=7.5, color = curColor,
                    solid_joinstyle='round', solid_capstyle='round', marker='o', markersize=25, markeredgecolor='none', alpha=.75)

            for i, row in enumerate(teamDF[j].values):
                ax.annotate(\
                    row.round(1),
                    xy=(teamDF[j].index[i], row), \
                    ha='center', \
                    va='center', \
                    fontproperties=FONT, \
                    color=font_color2, \
                    fontsize=12,\
                    alpha = .75
                    )

            y_pos = teamDF[j].tail(1)
            y_pos = find_y(stat,y_pos, team)
            ax.text(lastYear - .5, y_pos, key, fontsize=16, color=curColor,
                    fontproperties=FONT, verticalalignment='center', alpha = .75)

        addPlayoffs(ax, seasons, team)
        save(fig, 'comparison', team, 'team')
        """

if __name__ == '__main__':
    main()
