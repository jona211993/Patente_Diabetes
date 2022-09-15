import matplotlib.pyplot as plt
import skfuzzy as fuzz
import numpy as np
from run import app, db
from models.entities.Prueba import Prueba, prueba_esquema


def createTest(body):
    comida = body['comida']
    herencia = body['herencia']
    glucosa = body['glucosa']
    physicalActivity = body['physicalActivity']

    # Rango de la alimentación
    x_alimentacion = np.arange(0, 8, 0.1)
    # x_qual = np.linspace(0,10,11)
    # Rango de glucosa
    x_glucosa = np.arange(0, 201, 1)
    # Rango de Genetica
    x_genetica = np.arange(0, 6, 0.1)
    # Rango de Actividad Fisica
    x_a_fisica = np.arange(0, 8, 0.1)
    # ==============================
    # Rango del porcentaje de Riesgo
    x_riesgo = np.arange(0, 2, 0.01)

    # NADA
    nada = fuzz.trapmf(x_alimentacion, [0, 0, 0, 1.35])  # —- 0-1 5-0 \

    # POCO
    poco = fuzz.trimf(x_alimentacion, [1, 2, 3])  # —- 0-1 5-0 \

    # MUCHO
    mucho = fuzz.trapmf(x_alimentacion, [2, 3, 7, 7])  # —- 0-1 5-0 \

    # NORMAL
    g_normal = fuzz.trapmf(x_glucosa, [0, 0, 0, 90])  # —- 0-1 5-0 \

    # PREOCUPANTE
    preocupante = fuzz.trimf(x_glucosa, [85, 105, 126])  # —- 0-1 5-0 \

    # MUY PREOCUPANTE
    muy_preocu = fuzz.trapmf(x_glucosa, [110, 160, 200, 200])  # —- 0-1 5-0 \

    # NINGUNO
    ninguno = fuzz.trapmf(x_genetica, [0, 0, 0, 1.2])  # —- 0-1 5-0 \

    # LEVE
    leve = fuzz.trimf(x_genetica, [1, 2, 3])  # —- 0-1 5-0 \

    # GRAVE
    grave = fuzz.trapmf(x_genetica, [2, 3, 5, 5])  # —- 0-1 5-0 \

    # BAJO
    a_bajo = fuzz.trapmf(x_a_fisica, [0, 0, 0, 1.8])  # —- 0-1 5-0 \

    # NORMAL
    a_normal = fuzz.trimf(x_a_fisica, [1, 2, 3])  # —- 0-1 5-0 \

    # ALTO
    a_alto = fuzz.trapmf(x_a_fisica, [2, 3, 7, 7])  # —- 0-1 5-0 \

    # Salida
    # BAJO
    bajo = fuzz.trapmf(x_riesgo, [0, 0, 0.01, 0.1])

    # NORMAL
    normal = fuzz.trimf(x_riesgo, [0.05, 0.15, 0.3])

    # ALTO
    alto = fuzz.trimf(x_riesgo, [0.2, 0.5, 0.6])

    # CRITICO
    critico = fuzz.trapmf(x_riesgo, [0.5, 0.65, 1, 1])

    # Añadimos las funciones anteriores al dominio de cada variable de entrada
    # En la funcion se manda Vector de los X , luego la funcion , el valor de entrada
    u_nada = fuzz.interp_membership(x_alimentacion, nada, comida)
    u_poco = fuzz.interp_membership(x_alimentacion, poco, comida)
    u_mucho = fuzz.interp_membership(x_alimentacion, mucho, comida)

    u_g_normal = fuzz.interp_membership(x_glucosa, g_normal, glucosa)
    u_preocupante = fuzz.interp_membership(x_glucosa, preocupante, glucosa)
    u_muy_preocu = fuzz.interp_membership(x_glucosa, muy_preocu, glucosa)

    u_ninguno = fuzz.interp_membership(x_genetica, ninguno, herencia)
    u_leve = fuzz.interp_membership(x_genetica, leve, herencia)
    u_grave = fuzz.interp_membership(x_genetica, grave, herencia)

    u_a_bajo = fuzz.interp_membership(x_a_fisica, a_bajo, physicalActivity)
    u_a_normal = fuzz.interp_membership(x_a_fisica, a_normal, physicalActivity)
    u_a_alto = fuzz.interp_membership(x_a_fisica, a_alto, physicalActivity)

    # REGLA 0:
    active_rule0 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 1
    salida_activation_0 = np.fmin(active_rule0, normal)

    # REGLA 1:
    active_rule1 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 1
    salida_activation_1 = np.fmin(active_rule1, normal)

    # REGLA 2:
    active_rule2 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 2
    salida_activation_2 = np.fmin(active_rule2, bajo)

    # REGLA 3:
    active_rule3 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 3
    salida_activation_3 = np.fmin(active_rule3, normal)

    # REGLA 4:
    active_rule4 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 4
    salida_activation_4 = np.fmin(active_rule4, normal)

    # REGLA 5:
    active_rule5 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 5
    salida_activation_5 = np.fmin(active_rule5, normal)

    # REGLA 6:
    active_rule6 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 6
    salida_activation_6 = np.fmin(active_rule6, alto)

    # REGLA 7:
    active_rule7 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 7
    salida_activation_7 = np.fmin(active_rule7, alto)

    # REGLA 8:
    active_rule8 = np.fmin(np.fmin(u_nada, u_g_normal),
                           np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 8
    salida_activation_8 = np.fmin(active_rule8, normal)

    # REGLA 9:
    active_rule9 = np.fmin(np.fmin(u_nada, u_preocupante),
                           np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 9
    salida_activation_9 = np.fmin(active_rule9, normal)

    # REGLA 10:
    active_rule10 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 10
    salida_activation_10 = np.fmin(active_rule10, normal)

    # REGLA 11:
    active_rule11 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 11
    salida_activation_11 = np.fmin(active_rule11, normal)

    # REGLA 12:
    active_rule12 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 12
    salida_activation_12 = np.fmin(active_rule12, alto)

    # REGLA 13:
    active_rule13 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 13
    salida_activation_13 = np.fmin(active_rule13, alto)

    # REGLA 14:
    active_rule14 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 14
    salida_activation_14 = np.fmin(active_rule14, normal)

    # REGLA 15:
    active_rule15 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 15
    salida_activation_15 = np.fmin(active_rule15, critico)

    # REGLA 16:
    active_rule16 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 16
    salida_activation_16 = np.fmin(active_rule16, critico)

    # REGLA 17:
    active_rule17 = np.fmin(np.fmin(u_nada, u_preocupante),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 17
    salida_activation_17 = np.fmin(active_rule17, alto)

    # REGLA 18:
    active_rule18 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 18
    salida_activation_18 = np.fmin(active_rule18, critico)

    # REGLA 19:
    active_rule19 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 19
    salida_activation_19 = np.fmin(active_rule19, critico)

    # REGLA 20:
    active_rule20 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 20
    salida_activation_20 = np.fmin(active_rule20, alto)

    # REGLA 21:
    active_rule21 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 21
    salida_activation_21 = np.fmin(active_rule21, critico)

    # REGLA 22:
    active_rule22 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 22
    salida_activation_22 = np.fmin(active_rule22, critico)

    # REGLA 23:
    active_rule23 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 23
    salida_activation_23 = np.fmin(active_rule23, alto)

    # REGLA 24:
    active_rule24 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 24
    salida_activation_24 = np.fmin(active_rule24, critico)

    # REGLA 25:
    active_rule25 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 25
    salida_activation_25 = np.fmin(active_rule25, critico)

    # REGLA 26:
    active_rule26 = np.fmin(np.fmin(u_nada, u_muy_preocu),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 26
    salida_activation_26 = np.fmin(active_rule26, critico)

    # REGLA 27:
    active_rule27 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 27
    salida_activation_27 = np.fmin(active_rule27, normal)

    # REGLA 28:
    active_rule28 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 28
    salida_activation_28 = np.fmin(active_rule28, normal)

    # REGLA 29:
    active_rule29 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 29
    salida_activation_29 = np.fmin(active_rule29, bajo)

    # REGLA 30:
    active_rule30 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 30
    salida_activation_30 = np.fmin(active_rule30, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 31:
    active_rule31 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 31
    salida_activation_31 = np.fmin(active_rule31, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 32:
    active_rule32 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 32
    salida_activation_32 = np.fmin(active_rule32, bajo)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 33:
    active_rule33 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 33
    salida_activation_33 = np.fmin(active_rule33, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 34:
    active_rule34 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 34
    salida_activation_34 = np.fmin(active_rule34, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 35:
    active_rule35 = np.fmin(np.fmin(u_poco, u_g_normal),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 35
    salida_activation_35 = np.fmin(active_rule35, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 36:
    active_rule36 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 36
    salida_activation_36 = np.fmin(active_rule36, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 37:
    active_rule37 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 37
    salida_activation_37 = np.fmin(active_rule37, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 38:
    active_rule38 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 38
    salida_activation_38 = np.fmin(active_rule38, bajo)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 39:
    active_rule39 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 39
    salida_activation_39 = np.fmin(active_rule39, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 40:
    active_rule40 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 40
    salida_activation_40 = np.fmin(active_rule40, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 41:
    active_rule41 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 41
    salida_activation_41 = np.fmin(active_rule41, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 42:
    active_rule42 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 42
    salida_activation_42 = np.fmin(active_rule42, critico)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 43:
    active_rule43 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 43
    salida_activation_43 = np.fmin(active_rule43, critico)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 44:
    active_rule44 = np.fmin(np.fmin(u_poco, u_preocupante),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 44
    salida_activation_44 = np.fmin(active_rule44, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 45:
    active_rule45 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 45
    salida_activation_45 = np.fmin(active_rule45, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 46:
    active_rule46 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 46
    salida_activation_46 = np.fmin(active_rule46, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 47:
    active_rule47 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 47
    salida_activation_47 = np.fmin(active_rule47, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 48:
    active_rule48 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 48
    salida_activation_48 = np.fmin(active_rule48, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 49:
    active_rule49 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 49
    salida_activation_49 = np.fmin(active_rule49, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 50:
    active_rule50 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 50
    salida_activation_50 = np.fmin(active_rule50, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 51:
    active_rule51 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 51
    salida_activation_51 = np.fmin(active_rule51, critico)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 52:
    active_rule52 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 52
    salida_activation_52 = np.fmin(active_rule52, critico)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 53:
    active_rule53 = np.fmin(np.fmin(u_poco, u_muy_preocu),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 53
    salida_activation_53 = np.fmin(active_rule53, critico)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 54:
    active_rule54 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 54
    salida_activation_54 = np.fmin(active_rule54, bajo)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_54)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 55:
    active_rule55 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 55
    salida_activation_55 = np.fmin(active_rule55, bajo)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 56:
    active_rule56 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 56
    salida_activation_56 = np.fmin(active_rule56, bajo)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 57:
    active_rule57 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 57
    salida_activation_57 = np.fmin(active_rule57, normal)
   

    # REGLA 58:
    active_rule58 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 58
    salida_activation_58 = np.fmin(active_rule58, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 59:
    active_rule59 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 59
    salida_activation_59 = np.fmin(active_rule59, bajo)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 60:
    active_rule60 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 60
    salida_activation_60 = np.fmin(active_rule60, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 61:
    active_rule61 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 61
    salida_activation_61 = np.fmin(active_rule61, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 62:
    active_rule62 = np.fmin(np.fmin(u_mucho, u_g_normal),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 62
    salida_activation_62 = np.fmin(active_rule62, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 63:
    active_rule63 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 63
    salida_activation_63 = np.fmin(active_rule63, normal)
    

    # REGLA 64:
    active_rule64 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 64
    salida_activation_64 = np.fmin(active_rule64, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_64)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 65:
    active_rule65 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 65
    salida_activation_65 = np.fmin(active_rule65, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_65)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 66:
    active_rule66 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 66
    salida_activation_66 = np.fmin(active_rule66, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 67:
    active_rule67 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 67
    salida_activation_67 = np.fmin(active_rule67, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 68:
    active_rule68 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 68
    salida_activation_68 = np.fmin(active_rule68, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 69:
    active_rule69 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 69
    salida_activation_69 = np.fmin(active_rule69, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 70:
    active_rule70 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 70
    salida_activation_70 = np.fmin(active_rule70, alto)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 71:
    active_rule71 = np.fmin(np.fmin(u_mucho, u_preocupante),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 71
    salida_activation_71 = np.fmin(active_rule71, normal)
    # plt.style.use('default')
    # fig=plt.figure(figsize=(6,4))
    # plt.plot(x_riesgo,salida_activation_normal)
    # plt.axis([0,1,0,1])
    # plt.show()

    # REGLA 72:
    active_rule72 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_bajo))
    # Clipping en la regla 72
    salida_activation_72 = np.fmin(active_rule72, alto)

    # REGLA 73:
    active_rule73 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_normal))
    # Clipping en la regla 73
    salida_activation_73 = np.fmin(active_rule73, alto)

    # REGLA 74:
    active_rule74 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_ninguno, u_a_alto))
    # Clipping en la regla 74
    salida_activation_74 = np.fmin(active_rule74, normal)

    # REGLA 75:
    active_rule75 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_leve, u_a_bajo))
    # Clipping en la regla 75
    salida_activation_75 = np.fmin(active_rule75, alto)

    # REGLA 76:
    active_rule76 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_leve, u_a_normal))
    # Clipping en la regla 76
    salida_activation_76 = np.fmin(active_rule76, alto)

    # REGLA 77:
    active_rule77 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_leve, u_a_alto))
    # Clipping en la regla 77
    salida_activation_77 = np.fmin(active_rule77, normal)

    # REGLA 78:
    active_rule78 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_grave, u_a_bajo))
    # Clipping en la regla 78
    salida_activation_78 = np.fmin(active_rule78, critico)

    # REGLA 79:
    active_rule79 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_grave, u_a_normal))
    # Clipping en la regla 79
    salida_activation_79 = np.fmin(active_rule79, critico)

    # REGLA 80:
    active_rule80 = np.fmin(np.fmin(u_mucho, u_muy_preocu),
                            np.fmin(u_grave, u_a_alto))
    # Clipping en la regla 80
    salida_activation_80 = np.fmin(active_rule80, alto)

    a1 = np.fmax(salida_activation_75, np.fmax(salida_activation_76, np.fmax(salida_activation_77,
                                                                             np.fmax(salida_activation_78, np.fmax(salida_activation_79, salida_activation_80)))))
    a2 = np.fmax(salida_activation_69, np.fmax(salida_activation_70, np.fmax(salida_activation_71,
                                                                             np.fmax(salida_activation_72, np.fmax(salida_activation_73, salida_activation_74)))))
    a3 = np.fmax(salida_activation_63, np.fmax(salida_activation_64, np.fmax(salida_activation_65,
                                                                             np.fmax(salida_activation_66, np.fmax(salida_activation_67, salida_activation_68)))))
    a4 = np.fmax(salida_activation_57, np.fmax(salida_activation_58, np.fmax(salida_activation_59,
                                                                             np.fmax(salida_activation_60, np.fmax(salida_activation_61, salida_activation_62)))))
    a5 = np.fmax(salida_activation_51, np.fmax(salida_activation_52, np.fmax(salida_activation_53,
                                                                             np.fmax(salida_activation_54, np.fmax(salida_activation_55, salida_activation_56)))))
    a6 = np.fmax(salida_activation_45, np.fmax(salida_activation_46, np.fmax(salida_activation_47,
                                                                             np.fmax(salida_activation_48, np.fmax(salida_activation_49, salida_activation_50)))))
    a7 = np.fmax(salida_activation_39, np.fmax(salida_activation_40, np.fmax(salida_activation_41,
                                                                             np.fmax(salida_activation_42, np.fmax(salida_activation_43, salida_activation_44)))))
    a8 = np.fmax(salida_activation_33, np.fmax(salida_activation_34, np.fmax(salida_activation_35,
                                                                             np.fmax(salida_activation_36, np.fmax(salida_activation_37, salida_activation_38)))))
    a9 = np.fmax(salida_activation_27, np.fmax(salida_activation_28, np.fmax(salida_activation_29,
                                                                             np.fmax(salida_activation_30, np.fmax(salida_activation_31, salida_activation_32)))))
    a10 = np.fmax(salida_activation_21, np.fmax(salida_activation_22, np.fmax(salida_activation_23, np.fmax(
        salida_activation_24, np.fmax(salida_activation_25, salida_activation_26)))))
    a11 = np.fmax(salida_activation_15, np.fmax(salida_activation_16, np.fmax(salida_activation_17, np.fmax(
        salida_activation_18, np.fmax(salida_activation_19, salida_activation_20)))))
    a12 = np.fmax(salida_activation_9, np.fmax(salida_activation_10, np.fmax(salida_activation_11, np.fmax(
        salida_activation_12, np.fmax(salida_activation_13, salida_activation_14)))))
    a13 = np.fmax(salida_activation_3, np.fmax(salida_activation_4, np.fmax(
        salida_activation_5, np.fmax(salida_activation_6, np.fmax(salida_activation_7, salida_activation_8)))))
    a14 = np.fmax(salida_activation_0, np.fmax(
        salida_activation_1, salida_activation_2))

    # UNIENDO:
    A1 = np.fmax(a6, np.fmax(a5, np.fmax(a4, np.fmax(a3, np.fmax(a1, a2)))))
    A2 = np.fmax(a12, np.fmax(a11, np.fmax(a10, np.fmax(a9, np.fmax(a8, a7)))))
    A3 = np.fmax(a13, a14)

    aggregated = np.fmax(A1, np.fmax(A2, A3))
    # la funcion de defuzzificacion son: lom, som,mom, centroid, bisector
    centroidAbsoluteValue = fuzz.defuzz(x_riesgo, aggregated, 'centroid')
    y = fuzz.interp_membership(x_riesgo, aggregated, centroidAbsoluteValue)

    # Hallar el nivel de pertinencia
    lowPertenenceGrade = fuzz.interp_membership(
        x_riesgo, bajo, centroidAbsoluteValue)
    midPertenenceGrade = fuzz.interp_membership(
        x_riesgo, normal, centroidAbsoluteValue)
    highPertenenceGrade = fuzz.interp_membership(
        x_riesgo, alto, centroidAbsoluteValue)
    criticalPertenenceGrade = fuzz.interp_membership(
        x_riesgo, critico, centroidAbsoluteValue)

    labelValue = ''

    if (lowPertenenceGrade > midPertenenceGrade and lowPertenenceGrade > highPertenenceGrade and lowPertenenceGrade > criticalPertenenceGrade):
        labelValue = 'RIESGO BAJO'
    if (midPertenenceGrade > lowPertenenceGrade and midPertenenceGrade > highPertenenceGrade and midPertenenceGrade > criticalPertenenceGrade):
        labelValue = "RIESGO NORMAL"
    if (highPertenenceGrade > lowPertenenceGrade and highPertenenceGrade > midPertenenceGrade and highPertenenceGrade > criticalPertenenceGrade):
        labelValue = "RIESGO ALTO"
    if (criticalPertenenceGrade > lowPertenenceGrade and criticalPertenenceGrade > midPertenenceGrade and criticalPertenenceGrade > highPertenenceGrade):
        labelValue = "RIESGO CRITICO"

    newTest = Prueba().setNombre(body['name']).setEdad(int(body['edad'])).setNumeroDocumentoDni(body['numero_documento_dni']).setComida(comida).setHerencia(
        herencia).setGlucosa(glucosa).setEjercicio(physicalActivity).setValorAbsoluto(centroidAbsoluteValue).setGradoPertenenciaBajo(lowPertenenceGrade).setGradoPertenenciaNormal(midPertenenceGrade).setGradoPertenenciaAlto(highPertenenceGrade).setGradoPertenenciaCritico(criticalPertenenceGrade).setTextoResultado(labelValue).setUsuarioId(1)

    db.session.add(newTest)
    db.session.commit()

    return prueba_esquema.jsonify(newTest)
