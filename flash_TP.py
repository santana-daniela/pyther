import numpy as np


class Flash_TP(object):
    """docstring for ClassName"""

    def __init__(self, arg):
        # super(ClassName, self).__init__()
        self.arg = arg

    def wilson(self, Pc, Tc, w, T):
        # Ecuación wilson
        lnKi = np.log(Pc / self.P) + 5.373 * (1 + w) * (1 - Tc / self.T)
        self.Ki = np.exp(lnKi)
        return self.Ki

    def beta(self, zi):
        self.zi = zi
        self.Ki = self.wilson(Pc, Tc, w, T)
        Bmin = np.divide((self.Ki * self.zi - 1), (self.Ki - 1))
        #print (("Bmin_inter = ", Bmin))
        Bmax = np.divide((1 - self.zi), (1 - self.Ki))
        #print (("Bmax_inter = ", Bmax))
        self.Bini = (np.max(Bmin) + np.min(Bmax)) / 2
        return self.Bini

    def rice(self, zi, Ki, Bini):
        self.zi = zi
        self.Bini = Bini
        self.Ki = Ki
        self.fg = np.sum(self.zi * (self.Ki - 1) / (1 - self.Bini + self.Bini * self.Ki))
        self.dfg = - np.sum(self.zi * (self.Ki - 1) ** 2 / (1 - self.Bini + self.Bini * self.Ki) ** 2)
        #print g, dg
        return self.fg, self.dfg

    def flash_ideal(self):
        self.Bini = self.beta(zi)
        self.Ki = self.wilson(self.Pc, self.Tc, self.w, self.T)
        print ("Ki_(P, T) = ", self.Ki)
        Eg = self.rice(zi, self.Ki, self.Bini)
        errorEq = abs(Eg[0])
        i, s = 0, 1

        while errorEq > ep:
            Eg = self.rice(zi, self.Ki, self.Bini)
            self.Bini = self.Bini - s * Eg[0] / Eg[1]
            errorEq = abs(Eg[0])
            i += 1
            if i >= 50:
                break

        xy = self.composicion_xy(zi, self.Ki, self.Bini)
        print ("Metano, Butano, Hexano")
        print ("-------------Composición de fase líquida------------------------")
        print ("xi = ", xy[0])
        print ("Sxi = ", np.sum(xy[0]))
        print ("-------------Composición de fase vapor------------------------")
        print ("yi = ", xy[1])
        print ("Syi = ", np.sum(xy[1]))

        return Eg[0], Eg[1], self.Bini

    def flash_PT(self):
        flashID = self.flash_ideal()
        print ("flash (P, T, zi)")
        print ("g, dg, B = ", flashID)
        print ("---------------------------------------------------------------")

        self.Bini = flashID[2]
        print ("Beta_r ini = ", self.Bini)
        moles = self.composicion_xy(zi, self.Ki, self.Bini)

        self.xi, self.yi = moles[0], moles[1]
        nil, niv = moles[2], moles[3]

        fi_F = self.fugac()

        #print "nil = ", nil, np.sum(nil)
        #print "Snil = ", np.sum(nil)
        #print "niv", niv, np.sum(niv)
        #print "Sniv = ", np.sum(niv)

        #nF = 2
        #CoeFugi = np.ones((nF, nC))

        #for i in range(nF):
        #    if i == 1:
        #        self.ni = nil
        #        self.nT = np.sum(self.ni)
        #    elif i == 2:
        #        self.ni = niv
        #        self.nT = np.sum(self.ni)

        #    Flug_i = self.fluido(self.P)
        #    CoeFugi[i, :] = Flug_i[1]

        #print CoeFugi
        #self.Ki = CoeFugi[0, :] / CoeFugi[1, :]

        self.Ki = fi_F[0] / fi_F[1]

        L = 1.0

        self.Ki = self.Ki * L

        Ki_1 = self.Ki
        print ("Ki_(P, T, ni) primera = ", self.Ki)

        print ("----------------------------------------------------------------")

        #self.Ki = np.array([1.729, 0.832, 0.640])

        #self.Ki = self.wilson(self.Pc, self.Tc, self.w, self.T)
        #print "Ki_(P, T) = ", self.Ki

        while 1:
            i, s = 0, 0.1

            while 1:
                Eg = self.rice(zi, self.Ki, self.Bini)
                print (Eg)
                self.Bini = self.Bini - s * Eg[0] / Eg[1]
                print (self.Bini)
                errorEq = abs(Eg[0])
                i += 1
                #print i

                #if self. Bini < 0 or self.Bini > 1:
                    #break
                #    self.Bini = 0.5
                if i >= 50:
                    pass
                    #break
                if errorEq < 1e-5:
                    break

            print ("Resultado Real = ", Eg)
            print (" Beta r = ", self.Bini)

            moles = self.composicion_xy(zi, self.Ki, self.Bini)
            self.xi, self.yi = moles[0], moles[1]

            #xy = self.composicion_xy(zi, self.Ki, self.Bini)

            print ("C1 -i-C4 n-C4")
            print ("-----------Composición de fase líquida----------------------")
            print ("xi = ", moles[0])
            print ("Sxi = ", np.sum(moles[0]))
            print ("-----------Composición de fase vapor------------------------")
            print ("yi = ", moles[1])
            print ("Syi = ", np.sum(moles[1]))

            fi_F = self.fugac()

            self.Ki = fi_F[0] / fi_F[1]
            Ki_2 = self.Ki
            dKi = abs(Ki_1 - Ki_2)
            Ki_1 = Ki_2
            print ("Ki_(P, T, ni) = ", self.Ki)

            fun_Ki = np.sum(dKi)
            print ("fun_Ki = ", fun_Ki)

            if fun_Ki < 1e-5:
                break

        return flashID



    def composicion_xy(self, zi, Ki, Bini):
        self.zi = zi
        self.Ki = Ki
        self.Bini = Bini
        self.xi = zi / (1 - self.Bini + self.Bini * self.Ki)
        self.yi = (zi * self.Ki) / (1 - self.Bini + self.Bini * self.Ki)
        self.li = (zi * (1 - self.Bini)) / (1 - self.Bini + self.Bini * self.Ki)
        self.vi = (zi * self.Bini * self.Ki) / (1 - self.Bini + self.Bini * self.Ki)

        return self.xi, self.yi, self.li, self.vi
