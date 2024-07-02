import plotly.express as px

def generate_visualizations(df):
    df_atrasos = df[((df.status=='A') | (df.status=='C')) & (df.data_vencimento < '20240617')]
    # New visualization 1
    # df1 = series.groupby("parentalguide")["votes"].mean().reset_index(name="votes").sort_values(by=["votes"], ascending=False)
    df1 = df_atrasos["razao_cliente"].value_counts().head(15).reset_index(name='count')
    fig_bar_mean_votes = px.bar(df1, x="parentalguide", y="votes", title='Parental Guide by Mean Votes', color="votes")
    fig_bar_mean_votes.update_layout(template='plotly_dark', font=dict(color='yellow'))

    # New visualization 2
    # df2 = series.groupby("parentalguide").size().reset_index(name='count').sort_values(by=["count"], ascending=False)
    df2 = df_atrasos["razao_cliente"].value_counts().head(15).reset_index(name='count')
    fig_bar_count = px.bar(df2, x="parentalguide", y="count", title='Parental Guide by Count', color="count")
    fig_bar_count.update_layout(template='plotly_dark', font=dict(color='yellow'))

    return fig_bar_mean_votes, fig_bar_count