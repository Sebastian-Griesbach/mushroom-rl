import numpy as np
from sklearn import preprocessing


class Regressor(object):
    """
    Regressor class used to preprocess input and output before passing them
    to the desired approximator.
    """
    def __init__(self, approximator_class, **params):
        """
        Constructor.

        # Arguments
            approximator_class (object): the approximator class to use.
            params (dict): other parameters.
        """
        self.features = params.pop('features', None)
        self.input_scaled = params.pop('input_scaled', False)
        self.output_scaled = params.pop('output_scaled', False)

        self.model = approximator_class(**params)

    def fit(self, x, y, exclude_actions=False, **fit_params):
        """
        Preprocess the input and output if requested and fit the model using
        its fit function.

        # Arguments
            x (np.array): input dataset containing states (and action, if
                action regression is not used).
            y (np.array): target.
            exclude_actions (bool): whether to consider action as input or not.
            fit_params (dict): other parameters.
        """
        if not exclude_actions:
            x = np.concatenate((x[0], x[1]), axis=1)
        else:
            x = x[0]

        if self.features:
            x = self.features.fit_transform(x)

        if self.input_scaled:
            self.pre_x = preprocessing.StandardScaler()
            x = self.pre_x.fit_transform(x)

        if self.output_scaled:
            self.pre_y = preprocessing.StandardScaler()
            y = self.pre_y.fit_transform(y.reshape(-1, 1))

        self.model.fit(x, y, **fit_params)

    def predict(self, x, exclude_actions=False):
        """
        Preprocess the input and output if requested and make the prediction.

        # Arguments
            x (np.array): input dataset containing states (and action, if
                action regression is not used).
            exclude_actions (bool): whether to consider action as input or not.

        # Returns
            The prediction of the model.
        """
        if not exclude_actions:
            x = np.concatenate((x[0], x[1]), axis=1)
        else:
            x = x[0]

        if self.features:
            x = self.features.transform(x)

        if self.input_scaled:
            x = self.pre_x.transform(x)

        y = self.model.predict(x)

        return self.pre_y.inverse_transform(y) if self.output_scaled else y

    def __str__(self):
        return str(self.model)
