self.analytics = DataAnalytics.do_analytics(DIR_DATA_MESSAGES)
analytics = DataAnalytics.do_analytics(DIR_DATA_MESSAGES)
analytics.dataframe.to_pickle(f"{DIR_DATA_ANALYTICS}/analytics.pickle")
with open(path.join(DIR_DATA_ANALYTICS, "all_orders.json"), 'w') as file:
  file.write(json.dumps(analytics.orders))