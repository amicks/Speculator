from speculator import market

# Init market raw data
m = market.Market(symbol='USDT_BTC', unit='month', count=6, period=86400)

# Parse features, x axis
x = m.set_features(partition=14)

# Parse targets, y axis
y = market.set_targets(x, delta=25)

# Close is a useless statistic in predicting trends
x = x.drop(['close'], axis=1)

# Create the random forest model
# The last entry doesn't have a target (can't predict yet), so skip over it
model = market.setup_model(x[:-1], y, model_type='random_forest', seed=1,
                           n_estimators=65, n_jobs=4)

# Predict the target test set from the features test set
trends = model._predict_trends(model.features.test)

# Get accuracies
ftr_imps = model.feature_importances()
conf_mx = model.confusion_matrix(model.targets.test, trends)
acc = model.accuracy(model.features.test, model.targets.test)

# Display accuracies
print('##################')
print('# TEST SET       #')
print('##################')
print('Accuracy: {0:.3f}%'.format(100 * acc))
print('\nConfusion Matrix:')
print(conf_mx)
print(market.TARGET_CODES)
print('\nFeature Importance:')
for ftr, imp in ftr_imps:
    print('  {0}: {1:.3f}%'.format(ftr, 100 * imp))

print()

# Display prediction and probabilities for the next trend
print('##################')
print('# PREDICTED NEXT #')
print('##################')
next_date = x.tail(1) # Remember the entry we didn't train?  Predict it.

trends = model._predict_trends(next_date)
print('Predicted Trend: {0}'.format(market.target_code_to_name(trends[0])))

probas = model._predict_probas(next_date)
print('Probability: {0}'.format(probas[0]))

logs = model._predict_logs(next_date)
print('Log Probability: {0}'.format(logs[0]))

