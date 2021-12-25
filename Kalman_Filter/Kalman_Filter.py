import numpy as np
import json

class Kalman_Filter:
    """
    Die Klasse des Kalman Filters (KF)
    """


    def factorial(self, x: int):
        """
        Private Funktion um die Fakultät auszurechnen. Sollte eigentlich nicht benutzt werden \n


        Parameters: \n
        x: Integer Wert, dessen Fakultät ausgerechnet werden soll \n

        Returns: \n 
        int: x! wird zurückgegeben \n
        """

        f = 0.0
        if x == 0 or x == 1:
            f = 1.0
        else:
            f = factorial(x-1) * x
        return f

 
    def __init__(self):
        """
        Konstruktor des Kalman Filters. \n
        """

        self.PI = 3.14159265359
        self.EULER = 2.71828182846
        self.configured = False
        self.is_dynamic_update = False
        self.can_update_Q_matrix = False


    def configure(self, path_to_config_file: str, x0=None):
        """
        Funktion um die Konfiguration des Kalman Filters vorzunehmen. \n 
        Hier werden alle wichtigen Parameter gesetzt. Daher kann der Kalman Filter nicht ohne die Konfiguration gestarted werden!\n


        Parameters:\n
        path_to_config_file: String der den Pfad zur Konfigurationsdatei angibt. Die Datei muss eine .json Datei sein\n
        x0: Initialer Zustandsvektor des Kalman Filters. x0 muss vom Typ ulab.ndarray() sein\n

        Folgende Parameter können/müssen in der .json Datei gesetzt werden\n
        dt: Zeiteinheit zwischen 2 KF Updates. Als Default Wert empfielt sich eine 1 \n
        n: Dimension des Zustandraums. Muss ein Integer sein\n
        m: Dimension des Beobachtungs- oder Messraums. Muss ein Integer sein\n
        A: Koeffizienten der Zustandsübergangsmatrix. Muss eine nXn Matrix sein\n
        At: Optionale Matrix für die Zeitabhängigkeiten in der Zustandsübergangsmatrix. Muss eine nXn Matrix sein.\n
        C: Beobachtungsmatrix für die Überführung vom Zustand zur Messung. Muss eine mxn Matrix sein.\n
        Q: Zustandskovarianzmatrix für die Modelierung der Zustandsunsicherheit. Dieser Teil ist Zeitunabhängig. Muss eine nxn Matrix sein.\n
        Q_coeff: Matrix für Koeffizienten der zeitabhängigen Anteile in der Zustandskovarianzmatrix. Muss eine nxn Matrix sein.\n
        Q_variance: Skalarer Wert für die Varianz der Zustandsunsicherheit. Wird im Programm mit der Zustandskovarianzmatrix multipliziert. Muss ein Skalar sein.\n
        Q_exponent: Matrix für die Exponenten von t für die Zustandsunsicherheit. Muss eine nxn Matrix sein.\n
        R: Sensorkovarianzmatrix für die Modelierung des Sensorrauschens. Muss eine mxm Matrix sein.\n
        P: Fehlermatrix. Sollte als Identitätsmatrix oder Nullmatrix gewählt werden und hält die aktuelle Fehlermatrix. Wird bei Berechnungen überschrieben und ist daher ein optionaler Parameter. Muss beim Setzen aber eine nxn Matrix sein.\n
        P0: Initialer Wert der Fehlermatrix, falls man diese zurücksetzen möchte. Ist ein optionaler Parameter, muss aber beim Setzen eine nxn Matrix sein.\n
        x0: Anfangszustand für den Kalman Filter. Wird der x0 Wert des Methodenkopfes nicht genutzt muss dieser in der .json Datei gesetzt werden.\n
        """

        with open(path_to_config_file) as parameter_file:
            parameters = json.load(parameter_file)
            assert (parameters['dt'] > 0 and parameters['n'] > 0 and parameters['m']  > 0)
            self.dt = parameters['dt']
            self.n = parameters['n']
            self.m = parameters['m']

            self.gatingMatrix = np.zeros((self.n, self.n))

            self.A = np.array(parameters['A']).reshape((self.n, self.n))

            try:
                self.At = np.array(parameters['At']).reshape((self.n, self.n))
                self.is_dynamic_Update = True
            except KeyError as missing_key:
                print(str(missing_key) + " is not used")

            self.C = np.array(parameters['C']).reshape((self.m, self.n))

            self.Q = np.array(parameters['Q']).reshape((self.n, self.n))

            if (self.is_dynamic_Update):
                try:
                    self.Q_coeff = np.array(parameters['Q_coeff']).reshape((self.n, self.n))
                except KeyError as missing_key:
                    self.is_dynamic_Update = False
                    print(str(missing_key) + " is missing and therefore dynamic update is disabled")

            if (self.is_dynamic_Update):
                self.Q_variance = parameters['Q_variance']
                self.Q_exponent = np.array(parameters['Q_exponent']).reshape((self.n, self.n))
                self.can_update_Q_matrix = True

            self.R = np.array(parameters['R']).reshape((self.m, self.m))

            self.P = np.array(parameters['P']).reshape((self.n, self.n))
            self.P0 = np.array(parameters['P']).reshape((self.n, self.n))


            if x0:
                assert x0.shape == (self.n,)
                self.x_hat = x0.transpose()
                self.x0 = self.x_hat
            else:
                self.x_hat = np.array(parameters['x0']).transpose()
                self.x0 = self.x_hat

            self.configured = True


    def computePrediction(self, delta_t=None):
        """
        Funktion um eine Vorhersage des Kalman Filters zu generieren. Dabei wird die P-Matrix nicht geupdated\n


        Parameters:\n
        delta_t: Optionaler Parameter für die Zeitdauer zwischen 2 Funktionsaufrufen. Falls delta_t im Methodenkopf nicht genutzt wird, wird dt aus der Konfigurationsdatei genutzt.\n
        
        Returns:\n
        Der nächste erwartete Zustand.\n
        """
        if self.configured:
            A_t = np.zeros(self.At.shape())
            if delta_t is None:
                delta_t = self.dt
            for i in range(self.n):
                for j in range(self.n):
                    if (self.At[i][j] > 0.0):
                        A_t[i][j] = (delta_t ** self.At[i][j]) / self.factorial(self.At[i,j])
            out = np.linalg.dot(A_t + self.A,self.x_hat)
            return out
        else:
            print("Kalman Filter is not configured")


    def predict(self):
        """
        Funktion um eine Vorhersage des Kalman Filters zu generieren. Dabei wird die P-Matrix geupdated\n


        Parameters:\n
        
        Returns:\n
        Der nächste erwartete Zustand.\n
        """
        if self.configured:
            self.x_hat = np.linalg.dot(self.A, self.x_hat)
            self.P = np.linalg.dot(self.A, np.linalg.dot(self.P, self.A.transpose())) + self.Q

            return self.x_hat
        else:
            print("Kalman Filter is not configured")


    def update(self, data_in, delta_t=None, update_Q_Matrix=False, R_loc=None):
        """
        Funktion für einen Update-Schritt des Kalman Filters. In dieser Funktion wird sowohl die A-, Q-, P- und die Gatingmatrix und der Zustand x_hat geupdated.\n


        Parameters:\n
        data_in: Aktuelle Messung. Muss ein mx1 Vektor sein.\n
        delta_t: Optionaler Parameter für die vergangene Zeit zwischen dem letzten Methodenaufruf. Falls dieser Wert nicht genutzt wird, wird stattdessen der dt Wert aus der Konfigurationsdatei verwendet. \n
        update_Q_Matrix: Optionaler Parameter für das Überschreiben der Q Matrix.\n
        R_Loc: Optionaler Parameter für das Setzen der R Matrix. Dieser Parameter sollte genutzt werden, falls die R Matrix nicht konstant ist. Ansonsten sollte die R Matrix in der Konfigurationsdatei gesetzt werden.\n

        Returns:\n
        Der gefilterte geschätzte Zustand\n
        """
        if self.configured:
            assert data_in.shape() == (self.m, 1)
            if delta_t is None:
                delta_t = self.dt
            A_t = np.zeros(self.At.shape())
            for i in range(self.n):
                for j in range(self.n):
                    #There has to be a better way to do this!
                    if (self.At[i][j] > 0.0):
                        A_t[i][j] = (delta_t ** self.At[i][j]) / self.factorial(self.At[i][j])


            Q_updated = np.zeros(self.Q.shape())
            if self.can_update_Q_matrix and update_Q_Matrix:
                for i in range(self.n):
                    for j in range(self.n):
                        Q_updated[i][j] = self.Q[i][j] + self.Q_variance * self.Q_coeff[i][j] * (delta_t ** self.Q_exponent[i][j])


            R_used = self.R
            if R_loc is not None and self.R.shape == R_loc.shape() and not (np.numerical.max(R_loc) > 0):
                R_used = R_loc

            x_hat_new = np.linalg.dot(self.A + A_t, self.x_hat)
            self.P = np.linalg.dot(self.A + A_t, np.linalg.dot(self.P, (self.A + A_t).transpose())) + Q_updated
            self.gatingMatrix = np.linalg.dot(self.C, np.linalg.dot(self.P, self.C.transpose())) + R_used
            self.K = np.linalg.dot(self.P, np.linalg.dot(self.C.transpose(), np.linalg.inv(self.gatingMatrix)))
            x_hat_new = x_hat_new + np.linalg.dot(self.K, data_in - np.linalg.dot(self.C, x_hat_new))
            self.P = np.linalg.dot(np.eye(self.n) - np.linalg.dot(self.K, self.C),self.P)

            self.x_hat = x_hat_new
            return self.x_hat

        else:
            print("Kalman Filter is not configured")


    def getErrorCovarianceMatrix(self):
        """
        Getter Funktion für die Fehlermatrix.\n


        
        Returns:\n
        Die P Matrix\n
        """
        if self.configured:
            return self.P
        else:
            print("Kalman Filter is not configured")


    def getCurrentState(self):
        """
        Funktion für das Rücksetzen der Fehlermatrix und des geschätzten Zustandes.\n
        Diese Funktion kann genutzt werden, falls der Kalman Filter wegen schlechten Eingabewerten, einer ungenauen Systemgleichung o.ä. von der gewünschten Lösung divergiert.\n

        Returns:\n
        Den aktuellen Zustand
        """
        if self.configured:
            return self.x_hat
        else:
            print("Kalman Filter is not configured")


    def resetErrorCovAndState(self):
        """
        Funktion für das Rücksetzen der Fehlermatrix und des geschätzten Zustandes.\n
        Diese Funktion kann genutzt werden, falls der Kalman Filter wegen schlechten Eingabewerten, einer ungenauen Systemgleichung o.ä. von der gewünschten Lösung divergiert.\n

        Parameters:\n
        """
        if self.configured:
            self.P = self.P0
            self.x_hat = self.x0
        else:
            print("Kalman Filter is not configured")


    def likelihood(self,data_in):
        """
        Funktion um die Likelihood für eine Messung zu berechnen.\n

        Parameters:\n
        data_in: Messung deren Likelihood berechnet werden soll.\n

        Returns:\n
        Likelihood der gegebenen Messung\n
        """
        if self.configured:
            assert data_in.shape() == (self.m, 1)
            prediction = np.linalg.dot(self.C, np.linalg.dot(self.A, self.x_hat))

            continuousPrediction = prediction - np.linalg.dot(self.C, self.x_hat)

            timeShiftedPrediction = (np.linalg.dot(self.C, self.x_hat) + (np.array([self.dt]) * continuousPrediction))

            d = timeShiftedPrediction - data_in

            exp = np.array([-0.5]) * np.linalg.dot(d.transpose(), np.linalg.dot(np.linalg.inv(self.gatingMatrix), d))

            data_out = (self.EULER ** exp[0]) / (((2 * self.PI) ** (0.5 * int(self.m))) * (np.linalg.det(self.gatingMatrix)))

            return data_out

        else:
            print("Kalman Filter is not configured")
