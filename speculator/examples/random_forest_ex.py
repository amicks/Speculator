from speculator import market

# Init market raw data
m = market.Market(symbol='USDT_BTC', unit='month', count=6, period=86400)

# Parse features, x axis
x = m.features(partition=14)

# Parse targets, y axis
y = market.targets(x, delta=25)

# Create the random forest model
# The last entry doesn't have a target (can't predict yet), so skip over it
model = market.setup_model(x[:-1], y, model_type='random_forest', seed=1,
                           n_estimators=65, n_jobs=4)

# Predict the target test set from the features test set
pred = model.predict(model.features.test)

# Get accuracies
ftr_imps = model.feature_importances()
conf_mx = model.confusion_matrix(model.targets.test, pred)
acc = model.accuracy(model.targets.test, pred)

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
trend = market.target_code_to_name(model.predict(next_date)[0])
print('Trend: {0}'.format(trend))
print('Probability: {0}'.format(model.predict_proba(next_date)))
print('Log Probability: {0}'.format(model.predict_log_proba(next_date)))

