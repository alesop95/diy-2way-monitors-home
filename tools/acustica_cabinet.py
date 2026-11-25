"""Circuiti e aperture ideali: nessuna risposta di un esemplare o livello qualificato.

Reflex da circuito concentrato con sola perdita resistiva nel condotto.
Non comprende perdite della cassa, induttanza, compressione o diffrazione.
"""
import math
import numpy as np

SOUND_SPEED = 343.0
AIR_DENSITY = 1.204


def _positive(*values):
    if any(not math.isfinite(float(v)) or v <= 0 for v in values):
        raise ValueError('Parametri finiti e positivi richiesti')


def _frequency(values):
    values = np.asarray(values, dtype=float)
    if np.any(~np.isfinite(values)) or np.any(values <= 0):
        raise ValueError('Frequenze finite e positive richieste')
    return values


def vented_box(frequency, fs, qts, vas_l, vb_l, fb_hz, port_q):
    """Risposta normalizzata al passabanda: total=cone+port, con fase.

    port_q=inf elimina la resistenza del condotto. Il circuito e' risolto
    per ammettenza: non divide per l'ammettenza nulla all'accordo ideale.
    """
    _positive(fs, qts, vas_l, vb_l, fb_hz)
    if math.isnan(port_q) or port_q <= 0:
        raise ValueError('Q del condotto positivo o infinito richiesto')
    s = 2j * math.pi * _frequency(frequency)
    ws, wb = 2*math.pi*fs, 2*math.pi*fb_hz
    vent_admittance = wb**2 / (s + wb/port_q)
    enclosure_admittance = s + vent_admittance
    mechanical = s + ws/qts + ws**2/s
    denominator = mechanical*enclosure_admittance + ws**2*vas_l/vb_l
    cone = s*enclosure_admittance / denominator
    port = -s*vent_admittance / denominator
    return {'cone': cone, 'port': port, 'total': s*s/denominator}


def port_geometry(volume_l, fb_hz, diameter_mm, wall_mm=2., end_factor=1.46,
                  panel_thickness_mm=0.):
    """Tubo rettilineo: accordo e volume sottratto sono risolti insieme.

    volume_l e' il volume disponibile PRIMA del tubo; end_factor moltiplica
    il raggio interno per ottenere la correzione totale delle due estremita'.
    Parete e correzione sono ipotesi, non misure di un condotto commerciale.
    """
    _positive(volume_l, fb_hz, diameter_mm)
    if any(not math.isfinite(v) or v < 0 for v in (wall_mm, end_factor, panel_thickness_mm)):
        raise ValueError('Parete e correzione finite e non negative richieste')
    radius = diameter_mm/2000
    inner_area = math.pi*radius**2
    outer_area = math.pi*(radius + wall_mm/1000)**2
    end = end_factor*radius
    k = SOUND_SPEED**2*inner_area / (2*math.pi*fb_hz)**2
    initial = volume_l/1000
    # Vnet^2 - (Viniziale + Aesterna*end)*Vnet + Aesterna*k = 0.
    panel = panel_thickness_mm/1000
    b = initial + outer_area*(end+panel)
    discriminant = b*b - 4*outer_area*k
    if discriminant <= 0:
        raise ValueError('Nessun accordo con volume residuo fisico')
    net = (b + math.sqrt(discriminant))/2
    effective = k/net
    length = effective - end
    if length <= panel or net <= 0 or net > initial:
        raise ValueError('Lunghezza fisica del tubo non positiva')
    return {'net_volume_l': net*1000, 'length_mm': length*1000,
            'effective_length_mm': effective*1000, 'area_m2': inner_area,
            'outer_diameter_mm': diameter_mm + 2*wall_mm,
            'internal_length_mm': (length-panel)*1000,
            'tube_displacement_l': outer_area*(length-panel)*1000}


def piston_directivity(argument):
    """2 J1(x)/x, conservando segno e valore unitario in x=0.

    Integrale dell'apertura circolare con quadratura Chebyshev di seconda
    specie a 128 nodi. Intervallo verificato |x|<=64, sufficiente al modello
    fino a 20 kHz per i driver qui candidati. Nessuna dipendenza SciPy.
    """
    x = np.asarray(argument, dtype=float)
    if np.any(~np.isfinite(x)) or np.any(abs(x) > 64):
        raise ValueError('Argomento del pistone finito, modulo massimo 64')
    phase = np.arange(1, 129)*math.pi/129
    return (2/129*np.cos(x[..., None]*np.cos(phase))*np.sin(phase)**2).sum(axis=-1)


def two_way_response(frequency, angle_deg, woofer_sd_cm2, tweeter_sd_cm2,
                     spacing_mm, crossover_hz, offset_mm, plane='vertical',
                     capacitor_uf=None, tweeter_re_ohm=3.2):
    """Due pistoni ideali con LR4 elettrico, centri e offset ipotetici.

    Sd=0 e' il limite puntiforme. Offset positivo avvicina il tweeter;
    l'interasse contribuisce al cammino nel solo piano verticale.
    Non ricostruisce fase, breakup o risposta reale dai grafici di targa.
    """
    _positive(crossover_hz)
    for value in (woofer_sd_cm2, tweeter_sd_cm2, spacing_mm):
        if not math.isfinite(value) or value < 0:
            raise ValueError('Area e interasse finiti e non negativi richiesti')
    if not math.isfinite(offset_mm) or plane not in ('vertical', 'horizontal'):
        raise ValueError('Offset finito e piano verticale/orizzontale richiesti')
    f, angle = np.broadcast_arrays(_frequency(frequency), np.asarray(angle_deg, dtype=float))
    if np.any(~np.isfinite(angle)) or np.any(abs(angle) > 90):
        raise ValueError('Angolo fra -90 e 90 gradi richiesto')
    theta = np.deg2rad(angle)
    k = 2*math.pi*f/SOUND_SPEED
    radii = [math.sqrt(area*1e-4/math.pi) for area in (woofer_sd_cm2, tweeter_sd_cm2)]
    directivity = [piston_directivity(k*r*np.sin(theta)) for r in radii]
    s = 1j*f/crossover_hz
    denominator = (s*s + math.sqrt(2)*s + 1)**2
    low, high = 1/denominator, s**4/denominator
    if capacitor_uf is not None:
        high *= series_capacitor_response(f, tweeter_re_ohm, capacitor_uf)
    path = offset_mm/1000*np.cos(theta)
    if plane == 'vertical':
        path += spacing_mm/1000*np.sin(theta)
    return low*directivity[0] + high*directivity[1]*np.exp(1j*k*path)


def dbu_to_vrms(level_dbu):
    if not math.isfinite(level_dbu):
        raise ValueError('Livello dBu finito richiesto')
    return math.sqrt(.6)*10**(level_dbu/20)


def series_capacitor_response(frequency, resistance_ohm, capacitance_uf):
    """Solo carico resistivo dichiarato; nessuna impedenza reale dedotta."""
    _positive(resistance_ohm, capacitance_uf)
    s_rc = 2j*math.pi*_frequency(frequency)*resistance_ohm*capacitance_uf*1e-6
    return s_rc/(1+s_rc)
