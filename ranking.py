import pandas as pd
import inflect
p = inflect.engine()

name = 'Jason'

data = pd.read_csv('atla.csv', index_col=0)
tmp = pd.DataFrame(data)
# is there a tie ?
ties = tmp["wins"].duplicated(keep=False)
# calculate rankings
ranks = tmp["wins"].rank(method="dense", ascending=False)
tmp["position"] = (
    ranks.where(~ties, ranks.astype(str).radd("T"))
    .astype(str)
    .replace(".0$", "", regex=True)
)
df = tmp.sort_values(by="wins", ascending=False)
position = (df.at[name, 'position'])
total = len(df)
if position.startswith('T') is True:

    tied_ranking = position.replace('T', '')
    ranking = p.ordinal(tied_ranking)
    print(f"You are currently tied {ranking} in the rankings out of {total} users.")

else:
    ranking = p.ordinal(df.at['Lianne', 'position'])
    total = len(df)
    print(f"You are currently ranked {ranking} of {total} users.")

input = ("Would you like to see the rankings? [yes or no]")