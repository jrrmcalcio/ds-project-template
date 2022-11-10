"""
This is the demo code that uses hydra to access the parameters in under the directory config.

Author: Julio Rodas
"""

import re
import json
import sklearn
import warnings
from types import SimpleNamespace

  
def load_config():
    """
    Loads the configuration files for the project
    """
    f = open('../config/main.json')
    o = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
    
    for key, value in o.load.__dict__.items():
        sf = open('../config/' + key + '/' + value + '.json')
        o  = mergeObject(o, json.loads(sf.read(), object_hook=lambda d: SimpleNamespace(**d)))
        sf.close()
    
    f.close()
    
    return o

def mergeObject(original, merge):
    """
    Used to copy properties from one object to another if there isn't a naming conflict;
    """
    for property in original.__dict__:
        #Check to make sure it can't be called... ie a method.
        #Also make sure the object merge doesn't have a property of the same name.
        if not callable(original.__dict__[property]) and not hasattr(merge, property):
            setattr(merge, property, getattr(original, property))

    return merge

def drop_columns(df, config, whitelist):
    """
    Remove columns that are not needed
    """
    # Remove unecesary fields
    exclude = [i for i in df.columns 
                   if i.endswith('_1') or 
                      i.startswith('dt') or
                      i.startswith('int') or
                      i.startswith('dec') or
                      re.match('^char\d.*', i)] + \
              [i for i in config.exclude 
                   if i in df.columns and 
                      i not in whitelist]

    return df.drop(exclude, axis=1)

def get_pipe_names(column_transformer, categorical_props):
    """Get feature names from all transformers.
    Returns
    -------
    feature_names : list of strings
        Names of the features produced by transform.
    """
    # Remove the internal helper function
    #check_is_fitted(column_transformer)
    
    # Turn loopkup into function for better handling with pipeline later
    def get_names(trans):
        # >> Original get_feature_names() method
        if trans == 'drop' or (
                hasattr(column, '__len__') and not len(column)):
            return []
        if trans == 'passthrough':
            if hasattr(column_transformer, '_df_columns'):
                if ((not isinstance(column, slice))
                        and all(isinstance(col, str) for col in column)):
                    return column
                else:
                    return column_transformer._df_columns[column]
            else:
                indices = np.arange(column_transformer._n_features)
                return ['x%d' % i for i in indices[column]]
        if not hasattr(trans, 'get_feature_names'):
        # >>> Change: Return input column names if no method avaiable
            # Turn error into a warning
            warnings.warn("Transformer %s (type %s) does not "
                                 "provide get_feature_names. "
                                 "Will return input column names if available"
                                 % (str(name), type(trans).__name__))
            # For transformers without a get_features_names method, use the input
            # names to the column transformer
            if column is None:
                return []
            else:
                return [f for f in column]

        return [f for f in trans.get_feature_names()]
    
    ### Start of processing
    feature_names = []
    
    # Allow transformers to be pipelines. Pipeline steps are named differently, so preprocessing is needed
    if type(column_transformer) == sklearn.pipeline.Pipeline:
        l_transformers = [(name, trans, None, None) for step, name, trans in column_transformer._iter()]
    else:
        # For column transformers, follow the original method
        l_transformers = list(column_transformer._iter(fitted=True))
    
    
    for name, trans, column, _ in l_transformers: 
        if type(trans) == sklearn.pipeline.Pipeline:
            # Recursive call on pipeline
            _names = get_pipe_names(trans, categorical_props)
            # if pipeline has no transformer that returns names
            if len(_names)==0:
                _names = [f for f in column]
            feature_names.extend(_names)
        else:
            feature_names.extend(get_names(trans))
    
    #processing one hot encoded names that were replaced with x<numer>_<value>
    xn_    = list(dict.fromkeys([c.split('_')[0] + '_' for c in feature_names if re.match('^x\d+_', c)]))
    xn_dic = dict(zip(xn_, categorical_props))
    fns    = feature_names.copy()

    for key, value in xn_dic.items():
        fns = [c.replace(key, value + '_').lower() for c in fns]
        fns = [re.sub(r'[^a-zA-Z0-9]','_',c) for c in fns]
        fns = [re.sub('_+' ,'_' ,c) for c in fns]
    
    feature_names = fns
    return feature_names