# 36 // DATA BROKER

```
[CHEESE SHOP] purchase: pandas ── input: coil_registry.csv ── 38,114 rows × 9 columns ── quality: "corporate"
```

**Package:** [`pandas`](https://pandas.pydata.org/docs/): labelled tables (DataFrames) for loading, cleaning, grouping, joining and summarising data.

The registry of every archived mind is a CSV export: names, IDs, racks, archive dates, the
handler assigned to each one, a status, and an "activity" score. It's full of the usual rot:
duplicate rows from a botched migration, missing scores, trailing spaces, and handlers who left
the company years ago.

> **WENSLEYDALE:** pandas is what everyone reaches for when data comes in rows and columns,
> sir. A DataFrame is like a spreadsheet you can program: filter it, group it, join it to
> another one, pivot it, chart it. Built on NumPy, so it's quick.
>
> **MONTY:** And it's the language of every data broker in the city. If you can read a
> DataFrame, you can read anyone's secrets.

---

## ▓ TECH BRIEFING

### Series and DataFrames

```python
import pandas as pd
df = pd.read_csv("registry.csv", parse_dates=["archived"])   # also read_json, read_excel, read_sql, read_parquet
df = pd.read_csv(io.StringIO(text))                          # from a string
df.shape, df.columns, df.dtypes, df.head(), df.info(), df.describe()
df["rack"]                     # a Series (one column)
df[["id", "rack"]]             # a DataFrame (several columns)
df.loc[5, "rack"]              # by label;   df.iloc[0, 1]  by position
df["wing"] = df["rack"].str[0]                 # new column; .str has string methods
df.assign(wing=df["rack"].str[0])              # the same, but returns a NEW frame
```

pandas 3 uses **copy-on-write**: modifying a filtered selection never changes the original
frame, and there's no more `SettingWithCopyWarning`.

### Filtering and sorting

```python
df[df["wing"] == "C"]                          # boolean mask
df[(df["wing"] == "C") & (df["activity"] > 0.9)]   # use & | ~ with parentheses, not and/or
df.query("wing == 'C' and activity > 0.9")
df[df["status"].isin(["archived", "held"])]
df.sort_values(["activity", "id"], ascending=[False, True])
df.nlargest(5, "activity")
```

### Cleaning

```python
df.drop_duplicates(subset="id", keep="last")
df["name"] = df["name"].str.strip()
df["activity"] = df["activity"].fillna(0.0)
df.dropna(subset=["rack"]), df.isna().sum()
df.rename(columns={"hid": "handler_id"}), df.astype({"n": "int64"})
```

### Grouping, joining, reshaping

```python
df.groupby("wing").size()                                  # rows per group
df.groupby("wing")["activity"].agg(["mean", "max"])       # several statistics
df.groupby("wing").agg(avg=("activity", "mean"), n=("id", "count"))   # named aggregations
df.merge(staff, on="handler_id", how="left")               # SQL-style joins: inner/left/right/outer
pd.concat([df1, df2])
df.pivot_table(index="wing", columns="status", values="id", aggfunc="count", fill_value=0)
df["archived"].dt.to_period("M")                           # .dt date accessors: .year, .month...
df.set_index("archived").resample("ME").size()             # time series by month-end
```

### Out

```python
df.to_csv("out.csv", index=False), df.to_dict("records"), df.to_json(), df["x"].tolist()
```

---

## ▓ THE JOB

The tests give you CSV text. In `job.py`, using **pandas**:

1. **`load(csv_text)`**: read it, parsing the `archived` column as dates.
2. **`clean(df)`**: strip the names, drop duplicate `id`s (keeping the **last**), fill missing `activity` with 0.0, and reset the index.
3. **`with_wing(df)`**: a *new* frame with a `wing` column (the rack's first letter).
4. **`ids_in_wing(df, wing)`**: the sorted ids in a wing.
5. **`count_by_wing(df)`**: `{wing: rows}`.
6. **`activity_summary(df)`**: a frame indexed by wing, with `mean` and `max` activity columns.
7. **`archived_per_month(df)`**: `{"2091-01": n, ...}`, in order.
8. **`with_handlers(df, staff)`**: a left join on `handler_id`, with missing handler names set to `"unassigned"`.
9. **`release_queue(df, n)`**: the first `n` ids by activity (highest first), ties broken by id.
10. **`status_table(df)`**: a pivot of wing × status counts, as a nested dict.
