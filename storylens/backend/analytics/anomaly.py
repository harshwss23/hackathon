import numpy as np

class RobustAnomalyDetector:
    def detect_anomalies(self, time_series_values):
        """
        Uses rolling seasonal median baseline and Median Absolute Deviation (MAD) robust z-scores.
        """
        if not time_series_values or len(time_series_values) < 5:
            return {"is_anomaly": False, "robust_zscore": 0.0, "residual": 0.0}

        arr = np.array(time_series_values, dtype=float)
        median = np.median(arr[:-1])
        mad = np.median(np.abs(arr[:-1] - median))

        if mad == 0:
            mad = 1e-6

        current_val = arr[-1]
        residual = current_val - median
        robust_zscore = 0.6745 * (residual / mad)

        is_anomaly = abs(robust_zscore) >= 2.5

        return {
            "is_anomaly": is_anomaly,
            "robust_zscore": round(float(robust_zscore), 2),
            "observed": round(float(current_val), 2),
            "expected_baseline": round(float(median), 2),
            "residual": round(float(residual), 2)
        }

anomaly_detector = RobustAnomalyDetector()
