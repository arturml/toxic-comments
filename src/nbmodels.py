from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_is_fitted
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from scipy import sparse
import numpy as np

class NbLogisticClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, C=1.0, dual=False, n_jobs=1):
        self.C = C
        self.dual = dual
        self.n_jobs = n_jobs

    def predict(self, X):
        # Verify that model has been fit
        check_is_fitted(self, ['_r', '_clf'])
        return self._clf.predict(X.multiply(self._r))

    def predict_proba(self, X):
        # Verify that model has been fit
        check_is_fitted(self, ['_r', '_clf'])
        return self._clf.predict_proba(X.multiply(self._r))

    def fit(self, X, y):
        # Check that X and y have correct shape
        # y = y.values
        X, y = check_X_y(X, y, accept_sparse=True)

        def pr(X, y_i, y):
            p = X[y == y_i].sum(0)
            return (p+1) / ((y==y_i).sum()+1)

        self._r = sparse.csr_matrix(np.log(pr(X,1,y) / pr(X,0,y)))
        X_nb = X.multiply(self._r)
        self._clf = LogisticRegression(C=self.C, dual=self.dual, n_jobs=self.n_jobs).fit(X_nb, y)
        return self


class NbSVMClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, params={}):
        self._params = params

    def predict(self, X):
        # Verify that model has been fit
        check_is_fitted(self, ['_r', '_clf'])
        return self._clf.predict(X.multiply(self._r))

    def predict_proba(self, X):
        # Verify that model has been fit
        check_is_fitted(self, ['_r', '_clf'])
        return self._clf.predict_proba(X.multiply(self._r))

    def fit(self, X, y):
        # Check that X and y have correct shape
        # y = y.values
        X, y = check_X_y(X, y, accept_sparse=True)

        def pr(X, y_i, y):
            p = X[y == y_i].sum(0)
            return (p+1) / ((y==y_i).sum()+1)

        self._r = sparse.csr_matrix(np.log(pr(X,1,y) / pr(X,0,y)))
        X_nb = X.multiply(self._r)
        print('fit...')
        print(self._params)
        print(SVC(**self._params))
        self._clf = SVC(**self._params).fit(X_nb, y)
        print('done fit')
        return self

